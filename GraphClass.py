import numpy as np
from tabulate import tabulate

class Graph:
    def __init__(self, fileName):
        with open(fileName) as f:
            # prva linija je nebitna
            f.readline()

            # koliko sam shvatio i prvi i drugi broj u ovoj liniji su uvek isti, ne razumem koja je poenta
            # treci broj je broj linija koji se citaju
            nodeCount, _, lineCount = map(int, f.readline().split(' '))

            self.__nodeCount = nodeCount
            # u podacima umeracija pocinje od 1
            self.__adjacencyMatrix = np.zeros((self.__nodeCount + 1, self.__nodeCount + 1))
            self.__nodeSet = set(i for i in range(1, self.__nodeCount + 1))
            
            for i in range(lineCount):
                node, neighbor = map(int, f.readline().split(' '))
                self.addEdgde(node, neighbor)

            self.__edgeCount = self.calcEdgeCount()
            self.__density = self.calcDensity()
           
    def __str__(self):
        indicesTop = [str(i) for i in range(self.__nodeCount + 1)]
        indicesLeft = [str(i) for i in range(self.__nodeCount + 1)]
        return tabulate(self.__adjacencyMatrix, headers=indicesTop, showindex=indicesLeft, tablefmt="github")

    def addEdgde(self, node, neighbor):
        self.__adjacencyMatrix[node][neighbor] = 1
        self.__adjacencyMatrix[neighbor][node] = 1
        
    def getNodeCount(self):
        return self.__nodeCount

    def getNodeSet(self):
        return self.__nodeSet
    
    def getEdgeCount(self):
        return self.__edgeCount

    def getDensity(self):
        return self.__density
    
    def getAdjacencyMatrix(self):
        return self.__adjacencyMatrix

    def calcDensity(self):
        return (2 * self.__edgeCount) / (self.__nodeCount * (self.__nodeCount - 1))

    def calcEdgeCount(self):
        count = 0
        for i in range(1, self.__nodeCount + 1):
            for j in range(1, self.__nodeCount + 1):
                if self.__adjacencyMatrix[i][j] == 1:
                    count += 1
        return count