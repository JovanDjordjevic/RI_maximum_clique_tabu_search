from GraphClass import *
import numpy as np
from matplotlib import pyplot as plt
from amts import *
from bruteforce import *
import timeit

if __name__ == "__main__":

    fileName = "data/johnson8-2-4.mtx"
    #fileName = "data/brock200-1.mtx"
    #fileName = "data/brock200-3.mtx"
    #fileName = "data/hamming10-2.mtx"
    #fileName = "data/C500-9.mtx"
    #fileName = "data/c-fat200-5.mtx"
    g = Graph(fileName)

    # print(g)
    print(f'Node count: {g.getNodeCount()}   Edgde count: {g.getEdgeCount()}    Graph density: {g.getDensity()}')
    # print(g.getNodeSet())

    times = []
    iterCounts = []
    cliqueSizes = []

    # recimo da hocemo informacije za 100 iteracija
    for i in range(100):
        print(f"current iteration: {i}")
        # za konkretno k
        k = 4
        #k = 21
        #k = 15
        #k = 512
        #k = 57
        #k = 58
        maxIters = 100000                     # u radu korsiceno 10 ** 8
        L = g.getNodeCount()                  # u radu korisceno   L = g.getNodeCount() * k   osim za neke 

        timerStart = timeit.default_timer()

        resultClique, totalIterations = amts(g, k=k, L=L, maxIters=maxIters)

        timerEnd = timeit.default_timer()
        totalTime = timerEnd - timerStart

        print(f"Maximum found clique is of size {len(resultClique)}, found in {totalIterations} iterations:\n\n{resultClique}\n\n Elapsed time: {totalTime}")

        times.append(totalTime)
        cliqueSizes.append(len(resultClique))
        iterCounts.append(totalIterations)

    avgTime = np.average(times)
    avgIterations = np.average(iterCounts)
    avgCliqueSize = np.average(cliqueSizes)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.suptitle("Results for graph " + fileName)
    
    _, bins, _ = ax1.hist(times)
    ax1.set_title("Average time: " + str(avgTime))
    ax1.set(xlabel="t", xticks=bins)
    ax1.grid(True)

    _, bins, _ = ax2.hist(cliqueSizes)
    ax2.set_title( "Average size of found cliques: " + str(avgCliqueSize))
    ax2.set(xlabel="clique size", xticks=bins)
    ax2.grid(True)

    _, bins, _ = ax3.hist(iterCounts)
    ax3.set_title("Average needed iterations: " + str(avgIterations))
    ax3.set(xlabel="iterations", xticks=bins)
    ax3.grid(True)

    plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.setp(ax2.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.setp(ax3.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.tight_layout()
    plt.show()
    

    ## da nadje k
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

    # maxCliqueTime = -1
    # timerStart = timeit.default_timer()
    # maxC = maxClique_bruteforce(g, 0, 1)
    # timerEnd = timeit.default_timer()
    # maxCliqueTime = timerEnd - timerStart
    # print()
    # print(f"Maximum found clique is of size {maxC} with bruteforce algorithm, found in {maxCliqueTime} seconds.")
