#include "GraphClass.hpp"
#include <chrono>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <tuple>
#include <utility>
#include <math.h>

class Graph;
std::pair<std::unordered_set<int>, int> amts(Graph&g, int k, int L, int maxIters);

int main() {
    std::filesystem::path dataPath("./data");
    for(const auto& dirEntry : std::filesystem::directory_iterator(dataPath)) {
        if(dirEntry.path().extension() == ".mtx") {
            std::cout << "Loading graph " << dirEntry.path().stem() << " from file  ...... " << std::flush;
            Graph g(dirEntry.path());
            // std::cout << g << std::endl;
            std::cout << "Done" << std::endl;
            
            std::vector<double> times{};
            std::vector<int> iterCounts{};
            std::vector<int> cliqueSizes{};

            // ponavljamo za jedan graf 5 puta
            for(int i = 1; i <= 5; ++i) {
                int maxIters = 100'000;             // isprobano i 100'000'000
                int L = g.getNodeCount();

                auto start = std::chrono::high_resolution_clock::now();

                int currentCliqueSize = 3;
                int maxFoundCliqueSize = 0;
                int totalIterations = 0;

                
                std::cout << "--------------------------------------------------------------------------" << std::endl;
                std::cout << "Finding maximum clique in graph: " << dirEntry.path().stem() << " attempt " << i << "/5"  << std::endl;
                std::cout << "--------------------------------------------------------------------------" << std::endl;

                while(true) {
                    std::cout << "Trying to find clique of size: " << currentCliqueSize << " ..... " << std::flush;
                    
                    auto [resultClique, passedIterations] = amts(g, currentCliqueSize, L, maxIters);
                    
                    totalIterations += passedIterations;

                    if(resultClique.size() == 0) {
                        std::cout << "Failed to find clique of size " << currentCliqueSize << " in " << passedIterations << std::endl;
                        break;
                    }
                    else {
                        std::cout << "Found clique of size " << currentCliqueSize << " in " << passedIterations << " iterations" << std::endl;
                        // std::cout << "Resulting clique { ";
                        // for(auto& val : resultClique) {
                        //     std::cout << val << " ";
                        // }
                        // std::cout << "}" << std::endl << std::endl;

                        maxFoundCliqueSize = currentCliqueSize;
                    }

                    ++currentCliqueSize;
                }

                auto end = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> diff = end - start;
                // std::cout << diff.count() << std::endl;

                times.emplace_back(diff.count());
                cliqueSizes.emplace_back(maxFoundCliqueSize);
                iterCounts.emplace_back(totalIterations);
            }

            std::cout << std::endl;
            std::cout << "Exporting results  ......  " << std::flush;

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