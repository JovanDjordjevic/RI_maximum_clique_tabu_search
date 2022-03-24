#include "GraphClass.hpp"
#include <chrono>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <tuple>
#include <utility>

class Graph;
std::pair<std::unordered_set<int>, int> amts(Graph&g, int k, int L, int maxIters);

// NOTE: ovako kako je sad, procice kroz sve grafove u data folderu 
// i probace samo jednom da nadje max clique za njih pocevsi od 3 pa dok ne fejluje
// mozemo posle da probamo u npr 50 pokusaja posto je program brzi nego u pajtonu

int main() {
    std::filesystem::path dataPath("./data");
    for(const auto& dirEntry : std::filesystem::directory_iterator(dataPath)) {
        if(dirEntry.path().extension() == ".mtx") {
            Graph g(dirEntry.path());
            // std::cout << dirEntry.path() << std::endl;
            // std::cout << g << std::endl;
            
            std::vector<double> times{};
            std::vector<int> iterCounts{};
            std::vector<int> cliqueSizes{};

            int maxIters = 100000;
            int L = g.getNodeCount();

            auto start = std::chrono::high_resolution_clock::now();

            int currentCliqueSize = 3;
            int maxFoundCliqueSize = 0;
            int totalIterations = 0;

            
            std::cout << "--------------------------------------------------------------------------" << std::endl;
            std::cout << "Finding maximum clique in graph: " << dirEntry.path().stem() << std::endl;
            std::cout << "--------------------------------------------------------------------------" << std::endl;

            while(true) {
                std::cout << "Trying to find clique of size: " << currentCliqueSize << std::endl;

                auto [resultClique, passedIterations] = amts(g, currentCliqueSize, L, maxIters);

                if(resultClique.size() == 0) {
                    std::cout << "Failed to find clique of size " << currentCliqueSize << std::endl;
                    break;
                }
                else {
                    std::cout << "Found clique of size " << currentCliqueSize << " in " << passedIterations << " iterations" << std::endl;
                    // std::cout << "Resulting clique { ";
                    // for(auto& val : resultClique) {
                    //     std::cout << val << " ";
                    // }
                    // std::cout << "}" << std::endl << std::endl;
                    std::cout << std::endl;

                    maxFoundCliqueSize = currentCliqueSize;
                    totalIterations += passedIterations;
                }

                ++currentCliqueSize;
            }

            auto end = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> diff = end - start;
            // std::cout << diff.count() << std::endl;

            times.emplace_back(diff.count());
            cliqueSizes.emplace_back(maxFoundCliqueSize);
            iterCounts.emplace_back(totalIterations);

            std::cout << std::endl;
            std::cout << "Exporting results......";

            // export u fajl za plotter.py
            std::ofstream plotDataFile("plotData.txt", std::ofstream::out);
            plotDataFile << "results/" << dirEntry.path().filename() << std::endl;
            for(size_t i = 0; i < times.size(); ++i) {
                plotDataFile << times[i] << " " << cliqueSizes[i] << " " << iterCounts[i] << std::endl;
            }

            system("python3 plotter.py");

            std::cout << "Done" << std::endl << std::endl;
        }    
    }

    return 0;
}