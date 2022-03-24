#ifndef __GRAPH_CLASS__
#define __GRAPH_CLASS__

#include <filesystem>
#include <unordered_set>
#include <vector>

class Graph {
    public:
        Graph(std::filesystem::path filePath);

        int getNodeCount();
        int getEdgeCount();
        double getDensity();
        std::unordered_set<int> getNodeSet();
        std::vector<std::vector<int>> getAdjacencyMatrix();
        void addEdge(int node, int neighbor);

        friend std::ostream& operator<<(std::ostream& out, const Graph& g);

    private:
        double calcDensity();

    private:
        int nodeCount;   // da li treba long long mozda
        int edgeCount;   //isto
        std::vector<std::vector<int>> adjacencyMatrix; // mozda unsigned long ili slicno
        std::unordered_set<int> nodeSet;    // isto
        double density;     // isto da li trba veci tip
};

#endif