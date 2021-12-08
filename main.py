from GraphClass import *
import numpy as np

if __name__ == "__main__":
    with open("data/johnson8-2-4.mtx") as f:
        # prva linija je nebitna
        f.readline()

        # koliko sam shvatio i prvi i drugi broj u ovoj liniji su uvek isti, ne razumem koja je poenta
        # treci broj je broj linija koji se citaju
        nodeCount, _, lineCount = map(int, f.readline().split(' '))

        g = Graph(nodeCount)

        for i in range(lineCount):
            node, neighbor = map(int, f.readline().split(' '))
            g.addEdgde(node, neighbor)

        print(f'Node count: {g.getNodeCount()}   Edgde count: {g.getEdgeCount()}')
        print(g)