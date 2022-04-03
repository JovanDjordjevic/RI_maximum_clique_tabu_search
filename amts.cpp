#include "GraphClass.hpp"
#include <algorithm>
#include <iostream>
#include <random>
#include <tuple>
#include <unordered_set>
#include <unordered_map>
#include <vector>

bool isValid(int fS, int k) {
    return fS == k * (k - 1) / 2;
}


int f(Graph& g, std::unordered_set<int>& S) {
    std::vector<std::vector<int>> adjMatrix = g.getAdjacencyMatrix();
    int f = 0; 
    for(auto& i : S){
        for(auto& j : S) {
            if(adjMatrix[i][j] == 1) {
                ++f;
            }
        }
    }
    f /= 2;
    return f;
}


void constructInitialSolution(std::unordered_set<int>& S, std::unordered_set<int>& notInS, Graph& g, std::vector<int>& frequencies, int k) {
    // za random
    std::random_device rd;
    std::mt19937 generator(rd());

    //int V = g.getNodeCount();
    //std::vector<std::vector<int>> adjMatrix = g.getAdjacencyMatrix();

    int minFrequency = std::numeric_limits<int>::max();

    // kljuc je frekvencija a vrednost su cvorovi koji imaju tu frekvenciju
    std::unordered_map<int, std::vector<int>> frequencyGroups;
    for(size_t i = 1; i < frequencies.size(); ++i) {
        int freq = frequencies[i];
        frequencyGroups[freq].emplace_back(i);
        if(freq < minFrequency) {
            minFrequency = freq;
        }
    }
    
    // za prvi cvor u S se uzima neki random iz grupe cvorova koji imaju tu najmanju frekvenciju
    std::vector<int> minFreqGroup = frequencyGroups[minFrequency];
    std::uniform_int_distribution<int> firstNodeDistr(0, minFreqGroup.size() - 1);

    int nodeToAdd = minFreqGroup[firstNodeDistr(generator)];
    S.emplace(nodeToAdd);
    notInS.erase(nodeToAdd);
    ++frequencies[nodeToAdd];

    std::vector<std::vector<int>> adjMatrix = g.getAdjacencyMatrix();

    int V = g.getNodeCount() + 1;

    // mapa gde je kljuc stepen cvora ka S, a vrednsot skup cvorova sa tim stepeno
    std::unordered_map<int, std::unordered_set<int>> degreeSets{};
    std::vector<int> degreesTowardsS(V, 0);
    int maxDegree = 0;

    for(auto& i : notInS) {
        for(auto&j : S) {
            if(adjMatrix[i][j] == 1) {
                ++(degreesTowardsS[i]);
            }
        }

        degreeSets[degreesTowardsS[i]].emplace(i);

        if(degreesTowardsS[i] > maxDegree) {
            maxDegree = degreesTowardsS[i];
        }
    }

    while(S.size() < static_cast<size_t>(k)) {
        std::vector<int> candidates{};
        int minFreq = std::numeric_limits<int>::max();

        for(auto& i : degreeSets[maxDegree]) {
            if(frequencies[i] < minFreq) {
                minFreq = frequencies[i];
                candidates = {};
                candidates.emplace_back(i);
            }
            else if(frequencies[i] == minFreq) {
               candidates.emplace_back(i);
            }
        }
        
        // vidi da li ovaj deo treba negde dugde da se izmesti
        std::random_device rd;
        std::mt19937 generator(rd());
        std::uniform_int_distribution<int> distribution(0, candidates.size() - 1);

        nodeToAdd = candidates[distribution(generator)];

        S.emplace(nodeToAdd);
        notInS.erase(nodeToAdd);
        ++frequencies[nodeToAdd];

        degreesTowardsS[nodeToAdd] = 0;

        degreeSets[maxDegree].erase(nodeToAdd);
        while(degreeSets[maxDegree].size() == 0) {
            --maxDegree;
        }

        for(auto& i : notInS) {
            if(adjMatrix[i][nodeToAdd] == 1) {
                degreeSets[degreesTowardsS[i]].erase(i);
                ++degreesTowardsS[i];
                degreeSets[degreesTowardsS[i]].emplace(i);
                if(degreesTowardsS[i] > maxDegree) {
                    maxDegree = degreesTowardsS[i];
                }
            }
        }
    }

    return;
}


template<typename CN = std::vector<std::tuple<int, int, int>>, typename VECT = std::vector<int>, typename SET = std::unordered_set<int>>
std::tuple<CN, VECT, VECT, int, int> generateConstrainedNeighborhood(VECT& tabuList, Graph& g, SET& S, SET& notInS, VECT& degreesTowardsS, int currentIteration) {
    int minInS = std::numeric_limits<int>::max();
    int maxOutS = std::numeric_limits<int>::min();

    std::vector<std::vector<int>> adjMatrix = g.getAdjacencyMatrix();

    for(auto& i : S) {
        if(tabuList[i] < currentIteration && degreesTowardsS[i] < minInS) {
            minInS = degreesTowardsS[i];
        }
    }

    for(auto& i : notInS) {
        if(tabuList[i] < currentIteration && degreesTowardsS[i] > maxOutS) {
            maxOutS = degreesTowardsS[i];
        }
    }

    std::vector<int> A{};
    for(auto& u : S) {
        if(tabuList[u] < currentIteration && degreesTowardsS[u] == minInS) {
            A.emplace_back(u);
        }
    }

    std::vector<int> B{};
    for(auto& v : notInS) {
        if(tabuList[v] < currentIteration && degreesTowardsS[v] == maxOutS) {
            B.emplace_back(v);
        }
    }

    // constrained neigborhood je lista svih mogucih zamenena cvora iz A sa cvorom iz B
    // delta je promena vrednosti funkcije f(S) ako se taj potez primeni, f(newS) = f(S) + delta
    std::vector<std::tuple<int, int, int>> constrainedNeighborhood{};
    for(auto& i : A) {
        for(auto& j : B) {
            int delta = maxOutS - minInS;
            if(adjMatrix[i][j] == 1) {
                --delta;
            }
            constrainedNeighborhood.emplace_back(i, j, delta);
        }
    }

    return std::make_tuple(constrainedNeighborhood, A, B, minInS, maxOutS);
}


std::pair<int, int> calcTenures(int fS, int k) {
    std::random_device rd;
    std::mt19937 generator(rd());

    int l = std::min(10, k * (k - 1) / 2 - fS);
    int C = std::max(static_cast<int>(std::floor(k / 40)), 6);

    std::uniform_int_distribution<int> distr_U(1, C - 1);
    int tabuTenureU = (l + distr_U(generator));

    std::uniform_int_distribution<int> distr_V(1, static_cast<int>(std::floor(0.6 * (C - 1))));
    int tabuTenureV = static_cast<int>(std::floor(0.6 * l + distr_V(generator)));

    return std::make_pair(tabuTenureU, tabuTenureV);
}


// param L je za otkrivanje stagnacije
std::pair<std::unordered_set<int>, int> ts_0(Graph& g, std::unordered_set<int>& S, std::unordered_set<int>& notInS, std::vector<int>& frequencies, int k, int L, int iteration, int maxIters) {
    // za random 
    std::random_device rd;
    std::mt19937 generator(rd());
    
    // br uzastpnih iteracija koje se funkc f(S) nije poboljsala
    int tabuIters = 0;

    std::unordered_set<int> bestS(S);
    int fS = f(g, S);
    int fBestS = fS;
    
    // za signaliziranje da treba ponovo da se racunaji tabuTenureU i tabuTenureV
    bool fBestChanged = false;

    std::vector<std::vector<int>> adjMatrix = g.getAdjacencyMatrix();

    int V = g.getNodeCount() + 1;

    std::vector<int> tabuList(V, 0); 

    // move je (u, v) tj zamenimo u sa v
    // u stoji u tabu listi tabuTenureU iteracija, tj u sledecoj zameni, (u1, v1) ne moze da bude v1=u nerednih tabuTenureU iteracija   (tj u ne mzoe da se ubaci u naredna resenja)
    // V stoji u tabu listi tabuTenureV iteracija, tj u sledecoj zameni, (u1, v1) ne moze da bude u1=v nerednih tabuTenureV iteracija   (tj v ne moze da se izbaci iz trenutnog resenja)  
    auto tenures = calcTenures(fS, k);
    int tabuTenureU = std::get<0>(tenures);
    int tabuTenureV = std::get<1>(tenures);

    // racunacemo ovo inkrementalno umesto svaki put prilikom poziva generateConstrainedNeighborhood
    std::vector<int> degreesTowardsS(V, 0);
    for(int i = 1; i < V; ++i) {
        for(auto& j : S) {
            if(adjMatrix[i][j] == 1) {
                ++degreesTowardsS[i];
            }
        }
    }
    
    while(tabuIters < L && tabuIters < maxIters) {
        // posto l i C zavise od funkcije fS, ima smisla ne racunati ih stalno vec 
        // fS = fBestS samo kada se nadje novi najbolji
        if(fBestChanged) {
            fBestChanged = false;
            auto tenures = calcTenures(fS, k);
            tabuTenureU = std::get<0>(tenures);
            tabuTenureV = std::get<1>(tenures);
        }

        auto [CN, A, B, minInS, maxOutS] = generateConstrainedNeighborhood(tabuList, g, S, notInS, degreesTowardsS, iteration);
        
        int desireableDelta = maxOutS - minInS;

        std::vector<std::tuple<int, int, int>> T{};
        for(auto [i, j, delta] : CN) {
            if(delta == desireableDelta) {
                T.emplace_back(i, j, delta);
            }
        }

        // temp vrednost
        std::tuple<int, int, int> bestMove {-1, -1, -1};

        // NOTE: deo u radu o biranju sledeceg poteza moze se protumaciti na 2 nacina 
        if(T.size() != 0) {
            std::uniform_int_distribution<int> distr_move(0, T.size() - 1);
            bestMove = T[distr_move(generator)];
        }
        else {
            int l = std::min(10, k * (k - 1) / 2 - fS);
            double p = std::min(0.1, static_cast<double>((l + 2) / g.getNodeCount()));

            int u = -1;
            int v = -1;

            std::uniform_real_distribution<double> distr_p(0, std::nextafter(1, std::numeric_limits<double>::max()));

            // provera za A i B je dodata jer u slucaju da su 0, random index bude negativan i onda bude segfault
            if(A.size() == 0 || B.size() == 0 || distr_p(generator) < p) {
                // ovde mi treba u= random iz skupa S, nema lep nacin u c++ tako da pravim vektor u kom su vrednsoti iz S pa cu iz njega da odaberem ]
                std::vector<int> choiceVector(std::begin(S), std::end(S));
                std::uniform_int_distribution<int> distr_choiceVector(0, choiceVector.size() - 1);
                u = choiceVector[distr_choiceVector(generator)];
                
                double kDens = std::floor(k * g.getDensity());
                std::vector<int> probV{};
                for(auto& v : notInS) {
                    if(degreesTowardsS[v] < kDens) {
                        probV.emplace_back(v);
                    }
                }

                // isto i ovde za probV, recimo samo da cemo uzeti random cvor za v
                if(probV.size() == 0) {
                    v = choiceVector[distr_choiceVector(generator)];
                }
                else {
                    std::uniform_int_distribution<int> distr_probV(0, probV.size() - 1);
                    v = probV[distr_probV(generator)];
                }
            }
            else {
                std::uniform_int_distribution<int> distr_A(0, A.size() - 1);
                u = A[distr_A(generator)];                    
                std::uniform_int_distribution<int> distr_B(0, B.size() - 1);
                v = B[distr_B(generator)];
            }

            int delta = maxOutS - minInS;
            if(adjMatrix[u][v] == 1) {
                --delta;
            }

            bestMove = {u, v, delta};
        }

        auto [u, v, delta] = bestMove;

        S.erase(u);
        S.emplace(v);

        notInS.erase(v);
        notInS.emplace(u);

        fS += delta;

        tabuList[u] = tabuTenureU + iteration;
        tabuList[v] = tabuTenureV + iteration;

        ++frequencies[u];
        ++frequencies[v];

        for(int i = 1; i < V; ++i) {
            if(adjMatrix[i][v] == 1) {
                ++degreesTowardsS[i];
            }

            if(adjMatrix[i][u] == 1) {
                --degreesTowardsS[i];
            }
        }

        if(isValid(fS, k)) {
            return {S, iteration};
        }

        ++iteration;
        if(fS > fBestS) {
            fBestChanged = true;
            bestS = S;
            fBestS = fS;
            tabuIters = 0;
        }
        else {
            ++tabuIters;
        }
    }

    return std::make_pair(bestS, iteration);
}


std::pair<std::unordered_set<int>, int> amts(Graph& g, int k, int L, int maxIters) {
    std::vector<int> frequencies(g.getNodeCount() + 1, 0);

    std::unordered_set<int> S{};
    std::unordered_set<int> notInS = g.getNodeSet();

    constructInitialSolution(S, notInS, g, frequencies, k);

    int iters = 1;

    while(iters < maxIters) {
        auto [newS, passedIters] = ts_0(g, S, notInS, frequencies, k, L, iters, maxIters);
        iters = passedIters;

        if(isValid(f(g, newS), k)) {
            return std::make_pair(newS, iters);
        }
        else {
            // ako su sve frekvencije vece od k, niz treab da se resetuje
            // osim na nultom mestu, tu uvek treba da bude 0
            bool shouldResetFrequencies = true;
            for (size_t i = 1; i < frequencies.size(); ++i) {
                if(frequencies[i] < k) {
                    shouldResetFrequencies = false;
                    break;
                }
            }

            if(shouldResetFrequencies) {
                std::fill(std::begin(frequencies), std::end(frequencies), 0);
            }

            S = {};
            notInS = g.getNodeSet(); 
            constructInitialSolution(S, notInS, g, frequencies, k);
        }
    }

    // ako se desi da prodje maxIters, vracamo prazan set kako bi signalizirali neuspeh
    return std::make_pair(std::unordered_set<int>{}, iters);
}