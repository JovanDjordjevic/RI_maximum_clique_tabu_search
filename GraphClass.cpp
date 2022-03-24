#include "GraphClass.hpp"
#include <iostream>
#include <fstream>

std::ostream& operator<<(std::ostream& out, const Graph& g) {
    for(auto& row : g.adjacencyMatrix) {
        for(auto& val : row) {
            out << val << " ";
        }
        out << std::endl;
    }
    return out;
}

Graph::Graph(std::filesystem::path filePath) {
    std::ifstream file(filePath);

    // prva linija je nesto nebitno
    std::string line;
    getline(file, line);
    //std::cout << line;

    // koliko sam shvatio prvi i drugi broj u ovoj liniji su uvek isti, ne razumem koja je poenta
    // treci broj je broj linija koji se cita
    int numNodes;
    int lineCount;
    file >> numNodes >> numNodes >> lineCount;
    // std::cout << nodeCount << " " << lineCount << std::endl;

    this->nodeCount = numNodes;
    this->edgeCount = 0;
    this->adjacencyMatrix = std::vector<std::vector<int>>(this->nodeCount + 1, std::vector<int>(this->nodeCount + 1, 0));
    // std::cout << this->adjacencyMatrix.size();

    for(int i = 1; i < this->nodeCount + 1; ++i) {
        this->nodeSet.emplace(i);
    }
    // for(auto& val : this->nodeSet) {
    //     std::cout << val << " ";
    // }

    int node;
    int neighbor;
    
    while(lineCount) {    
        file >> node >> neighbor;
        this->addEdge(node, neighbor);
        --lineCount;
    }

    this->density = this->calcDensity();
}

int Graph::getNodeCount() {
    return this->nodeCount;
}

int Graph::getEdgeCount() {
    return this->edgeCount;
}

double Graph::getDensity() {
    return this->density;
}

std::unordered_set<int> Graph::getNodeSet() {
    return this->nodeSet;
}

std::vector<std::vector<int>> Graph::getAdjacencyMatrix() {
    return this->adjacencyMatrix;
}
        
void Graph::addEdge(int node, int neighbor) {
    this->adjacencyMatrix[node][neighbor] = 1;
    this->adjacencyMatrix[neighbor][node] = 1;
    ++this->edgeCount;
}

double Graph::calcDensity() {
    return (2.0 * this->edgeCount) / (this->nodeCount * (this->nodeCount - 1));
}