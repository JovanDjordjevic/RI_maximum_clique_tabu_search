import numpy as np
from tabulate import tabulate

class Graph:
    def __init__(self, nodeCount):
        # u podacima umeracija pocinje od 1
        self.nodeCount = nodeCount + 1
        self.adjacencyMatrix = np.zeros((self.nodeCount, self.nodeCount))

    def __str__(self):
        indicesTop = [str(i) for i in range(self.nodeCount)]
        indicesLeft = [str(i) for i in range(self.nodeCount)]
        return tabulate(self.adjacencyMatrix, headers=indicesTop, showindex=indicesLeft, tablefmt="github")

    def addEdgde(self, node, neighbor):
        self.adjacencyMatrix[node][neighbor] = 1
        self.adjacencyMatrix[neighbor][node] = 1
        
    def getNodeCount(self):
        return self.nodeCount - 1

    def getEdgeCount(self):
        count = 0
        for i in range(self.nodeCount):
            for j in range(self.nodeCount):
                if self.adjacencyMatrix[i][j] == 1:
                    count += 1
        return count