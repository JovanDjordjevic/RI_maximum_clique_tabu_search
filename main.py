from GraphClass import *
import numpy as np
from amts import *
from bruteforce import *
import timeit
import os

if __name__ == "__main__":
    # TODO: ubaciti da se bira opcija da li se pokrece bruteforce ili amts,
    #  za neki ili za sve, da nadje k ili za zadato k


    # kljuc: ime grafa, vrednost: max clique koji je pronadjen u literaturi
    # TODO: naci bolji nacin za ovo
    maxCliquesInLiterature = {
        'brock200-1.mtx' : 21,
        # 'brock200-2.mtx' : 12,
        # 'brock200-3.mtx' : 15,

        # 'johnson8-2-4.mtx' : 4,
        
        # 'hamming10-2.mtx' : 512,
        # 'C500-9.mtx' : 57,
        # 'c-fat200-5.mtx' : 58,
        # 'hamming6-2.mtx' : 32,
        # 'hamming6-4.mtx' : 4,
    }
    
    alreadyTested = {
        # 'brock200-1.mtx', 
        # 'brock200-3.mtx',
        
        # 'johnson8-2-4.mtx',
        # 'c-fat200-5.mtx',
        # 'hamming6-2.mtx',
        # 'hamming6-4.mtx',
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
                print(fileName)
                g = Graph(fileName)
                # print(f'Graph name: {fileName} Node count: {g.getNodeCount()}   Edgde count: {g.getEdgeCount()}    Graph density: {g.getDensity()}')

                times = []
                iterCounts = []
                cliqueSizes = []

                maxIters = 100000                     # u radu korsiceno 10 ** 8 sto je za nas presporo
                L = g.getNodeCount()                  # u radu korisceno   L = g.getNodeCount() * k   osim za neke 

                timerStart = timeit.default_timer()
                #lastTimeBeforeFailure = 0

                currentCliqueSize = 3
                maxFoundClique = 0
                totalIterations = 0
                while(True):
                    print(f"{file}, trying to find clique of size: {currentCliqueSize}")
                    
                    resultClique, passedIterations = amts(g, k=currentCliqueSize, L=L, maxIters=maxIters)

                    if len(resultClique) == 0:
                        print(f"Failed to find clique of size {currentCliqueSize}")
                        break
                    else:
                        print(f"Found clique of size {currentCliqueSize} in {passedIterations} iterations")
                        print(f"clique: {resultClique}\n")
                        maxFoundClique = currentCliqueSize
                        totalIterations += passedIterations
                        # lastTimeBeforeFailure = timeit.default_timer()
                        # print(f"time untill now: {lastTimeBeforeFailure - timerStart}")

                    currentCliqueSize += 1

                timerEnd = timeit.default_timer()
                totalTime = timerEnd - timerStart
                # totalTime = lastTimeBeforeFailure - timerStart

                times.append(totalTime)
                cliqueSizes.append(maxFoundClique)
                iterCounts.append(totalIterations)

                with open("plotData.txt", "w+") as plotDataFile:
                    plotDataFile.write(file + "\n")
                    for i in range(len(times)):
                        plotDataFile.write(f"{times[i]} {cliqueSizes[i]} {iterCounts[i]}\n")
                
                print("done")
                os.system("python3 plotter.py")