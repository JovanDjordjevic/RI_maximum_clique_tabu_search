from GraphClass import *
import numpy as np
from matplotlib import pyplot as plt
from amts import *
from bruteforce import *
import timeit
import os

import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import AsyncResult
from multiprocessing.pool import ThreadPool

if __name__ == "__main__":
    # TODO: ubaciti da se bira opcija da li se pokrece bruteforce ili amts,
    #  za neki ili za sve, da nadje k ili za zadato k


    # kljuc: ime grafa, vrednost: max clique koji je pronadjen u literaturi
    # TODO: naci bolji nacin za ovo
    maxCliquesInLiterature = {
        'brock200-1.mtx' : 21,
        'brock200-2.mtx' : 12,
        'brock200-3.mtx' : 15,

        'johnson8-2-4.mtx' : 4,
        
        'hamming10-2.mtx' : 512,
        'C500-9.mtx' : 57,
        'c-fat200-5.mtx' : 58,
        'hamming6-2.mtx' : 32,
        'hamming6-4.mtx' : 4,
    }
    
    alreadyTested = {
        'brock200-1.mtx', 
        'brock200-3.mtx',
        
        'johnson8-2-4.mtx',
        'c-fat200-5.mtx',
        'hamming6-2.mtx',
        'hamming6-4.mtx',
    }

    # oni gde se desavalo da jedna traje vise od pola minuta
    ignoreForNow = {
        #'C500-9.mtx',
        'hamming10-2.mtx',
    }

    for root, dirs, files in os.walk('data'):
        for file in files:
            if str(file).endswith('.mtx') and str(file) not in alreadyTested and str(file) not in ignoreForNow:
                fileName = os.path.join(root, file)
                # print(fileName)
                g = Graph(fileName)
                # print(f'Graph name: {fileName} Node count: {g.getNodeCount()}   Edgde count: {g.getEdgeCount()}    Graph density: {g.getDensity()}')

                times = []
                iterCounts = []
                cliqueSizes = []
                
                k = maxCliquesInLiterature[str(file)]

                maxIters = 100000                     # u radu korsiceno 10 ** 8 sto je za nas presporo
                L = g.getNodeCount()                  # u radu korisceno   L = g.getNodeCount() * k   osim za neke 
    
                # recimo da hocemo informacije za 100 iteracija
                for i in range(100):
                    print(f"{file}, current iteration: {i}")
                    
                    timerStart = timeit.default_timer()

                    resultClique, totalIterations = amts(g, k=k, L=L, maxIters=maxIters)
                    # threadPool = ThreadPool(processes=8)
                    # result1 = threadPool.apply_async(amts, [g, k, L, maxIters/2])
                    # ans1 = result1.get()
                    # result2 = threadPool.apply_async(amts, [g, k, L, maxIters/2])
                    # ans2 = result2.get()
                    # result3 = threadPool.apply_async(amts, [g, k, L, maxIters/2])
                    # ans3 = result3.get()
                    # print(ans1, ans2, ans3)
                    # exit()

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
                fig.set_size_inches(12, 6)
                
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
                plt.savefig(fileName + '.png')
                #plt.show()







    exit()

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
    fig.set_size_inches(12, 6)
    
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
    plt.savefig(fileName + '.png')
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

    # # maxCliqueTime = -1
    # # timerStart = timeit.default_timer()
    # # maxC = maxClique_bruteforce(g, 0, 1)
    # # timerEnd = timeit.default_timer()
    # # maxCliqueTime = timerEnd - timerStart
    # # print()
    # # print(f"Maximum found clique is of size {maxC} with bruteforce algorithm, found in {maxCliqueTime} seconds.")
