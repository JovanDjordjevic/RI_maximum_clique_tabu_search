from GraphClass import *
import numpy as np
from amts import *
from bruteforce import *
import timeit

if __name__ == "__main__":

    fileName = "data/johnson8-2-4.mtx"
    g = Graph(fileName)

    # print(g)
    print(f'Node count: {g.getNodeCount()}   Edgde count: {g.getEdgeCount()}    Graph density: {g.getDensity()}')
    # print(g.getNodeSet())

    # # za konkretno k
    # timerStart = timeit.default_timer()
    # k = 4
    # maxIters = 100000 #10 ** 8
    # L = g.getNodeCount() * k
    # print(f"Maximum found clique is of size {k}:\n{amts(g, k=k, L=L, maxIters=maxIters)}\n")
    # timerEnd = timeit.default_timer()
    # print(f"Elapsed time: {timerEnd - timerStart}")

    # da nadje k
    # maxK = -1
    # maxCliqueTime = -1
    # for k in range(3, g.getNodeCount() + 1):  # nema smisla traziti clique manji od 3
    #     maxIters = 10000                    # maxIters = 10 ** 8  u onom radu
    #     L = g.getNodeCount() * k

    #     timerStart = timeit.default_timer()
    #     kClique = amts(g, k=k, L=L, maxIters=maxIters)
    #     timerEnd = timeit.default_timer()

    #     if len(kClique) == 0:
    #         print(f"Maximum found clique is of size {maxK}, found in {maxCliqueTime} seconds: ")
    #         print(maxClique)

    #         break
    #     else:
    #        maxK = k
    #        maxClique = kClique
    #        maxCliqueTime = timerEnd - timerStart

    maxCliqueTime = -1
    timerStart = timeit.default_timer()
    maxC = maxClique_bruteforce(g, 0, 1)
    timerEnd = timeit.default_timer()
    maxCliqueTime = timerEnd - timerStart
    print()
    print(f"Maximum found clique is of size {maxC} with bruteforce algorithm, found in {maxCliqueTime} seconds.")
