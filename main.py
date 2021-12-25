from GraphClass import *
import numpy as np
from amts import *
import timeit

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

        print(f'Node count: {g.getNodeCount()}   Edgde count: {g.getEdgeCount()}    Graph density: {g.getDensity()}')
        #print(g)

        # # za konkretno k
        # timerStart = timeit.default_timer()
        # k = 2
        # maxIters = 100000 #10 ** 8 
        # L = g.getNodeCount() * k
        # print(f"Maximum found clique is of size {k}:\n{amts(g, k=k, L=L, maxIters=maxIters)}\n")
        # timerEnd = timeit.default_timer()
        # print(f"Elapsed time: {timerEnd - timerStart}")

        # da nadje k
        maxK = -1
        maxCliqueTime = -1
        for k in range(3, g.getNodeCount() + 1):  # nema smisla traziti clique manji od 3
            maxIters = 10000                    # maxIters = 10 ** 8  u onom radu
            L = g.getNodeCount() * k   

            timerStart = timeit.default_timer()         
            kClique = amts(g, k=k, L=L, maxIters=maxIters)
            timerEnd = timeit.default_timer()

            if len(kClique) == 0:
                print(f"Maximum found clique is of size {maxK}, found in {maxCliqueTime} seconds: ")
                print(maxClique)
                
                break
            else:
               maxK = k
               maxClique = kClique
               maxCliqueTime = timerEnd - timerStart

        
        