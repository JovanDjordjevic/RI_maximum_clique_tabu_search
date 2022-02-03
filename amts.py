from GraphClass import *
import numpy as np
import random
from copy import deepcopy
from collections import defaultdict
import timeit


def constructInitialSolution(S:set, notInS:set, g:Graph, frequencies, k):
    nodeToAdd = np.argmin(frequencies[1:]) + 1  # mora + 1 jer sa [1:] ignorisemo 0 (0 ce uvek da ima )

    S.add(nodeToAdd)
    notInS.remove(nodeToAdd) 

    adjMatrix = g.getAdjacencyMatrix()

    V = g.getNodeCount() + 1

    # mapa gde je kljuc stepen cvora ka S, a vrednost skup cvorova sa tim stepenom
    degreeSets = defaultdict(set)
    degreesTowardsS = [0 for _ in range(V)]
    maxDegree = 0

    for i in notInS:
        for j in S:
            if adjMatrix[i][j] == 1:
                degreesTowardsS[i] += 1
        degreeSets[degreesTowardsS[i]].add(i)
        if degreesTowardsS[i] > maxDegree:
            maxDegree = degreesTowardsS[i]

    while len(S) < k:
        candidates = []
        minFreq = float('inf')  
        for i in degreeSets[maxDegree]:          
            if frequencies[i] < minFreq:
                minFreq = frequencies[i]
                candidates = []
                candidates.append(i)
            elif frequencies[i] == minFreq:
                candidates.append(i)

        nodeToAdd = random.choice(candidates)

        S.add(nodeToAdd)
        notInS.remove(nodeToAdd)

        degreesTowardsS[nodeToAdd] = 0

        degreeSets[maxDegree].remove(nodeToAdd)
        while len(degreeSets[maxDegree]) == 0:
            maxDegree -= 1

        for i in notInS:
            if adjMatrix[i][nodeToAdd] == 1:
                degreeSets[degreesTowardsS[i]].remove(i)
                degreesTowardsS[i] += 1
                degreeSets[degreesTowardsS[i]].add(i)
                if degreesTowardsS[i] > maxDegree:
                    maxDegree = degreesTowardsS[i]
    return    



def generateConstrainedNeighborhood(tabuList:list, g:Graph, S:set, notInS:set, degreesTowardsS:list, currentIteration:int):
    minInS = float('inf')
    maxOutS = float('-inf')

    V = g.getNodeCount() + 1
    adjMatrix = g.getAdjacencyMatrix()

    for i in S:
        if tabuList[i] < currentIteration and degreesTowardsS[i] < minInS:   
            minInS = degreesTowardsS[i]

    for i in notInS:
        if tabuList[i] < currentIteration and degreesTowardsS[i] > maxOutS:   
            maxOutS = degreesTowardsS[i]

    A = [u for u in S if tabuList[u] < currentIteration and degreesTowardsS[u] == minInS]
    B = [v for v in notInS if tabuList[v] < currentIteration and degreesTowardsS[v] == maxOutS]

    # constrained neigborhood je lista svih mogucih zamenena cvora iz A sa cvorom iz B
    # delta je promena vrednosti funkcije f(S) ako se taj potez primeni, f(newS) = f(S) + delta
    constrainedNeighborhood = []
    for i in A:
        for j in B:
            delta = maxOutS - minInS
            if adjMatrix[i][j] == 1:
                delta -= 1
            constrainedNeighborhood.append([i, j, delta])
    #print(constrainedNeighborhood)
    return constrainedNeighborhood, A, B, minInS, maxOutS



def calcTenures(fS:int, k:int):
    l = min(10, k * (k - 1) / 2 - fS)
    C = max(int( np.floor(k/40) ), 6)
    tabuTenureU = int( l + random.randint(1, C - 1) )
    tabuTenureV = int( np.floor( 0.6 * l + random.randint(1, np.floor(0.6 * (C - 1)) ) ) )
    return tabuTenureU, tabuTenureV



# param L je za otkrivanje stagnacije
def ts_0 (g, S, notInS, frequencies, k , L, iteration, maxIters):
    tabuIters = 0   # broj uzastopnih iteracija koje se funkc f(S) nije poboljsala

    bestS = S
    fS = f(g, S)
    fBestS = fS

    # za signaliziranje da treba ponovo da se racunaji tabuTenureU i tabuTenureV
    fBestChanged = False

    adjMatrix = g.getAdjacencyMatrix()

    V = g.getNodeCount() + 1

    tabuList = [0 for _ in range(V)]

    # move je (u, v) tj zamenimo u sa v
    # u stoji u tabu listi tabuTenureU iteracija, tj u sledecoj zameni, (u1, v1) ne moze da bude v1=u nerednih tabuTenureU iteracija   (tj u ne mzoe da se ubaci u naredna resenja)
    # V stoji u tabu listi tabuTenureV iteracija, tj u sledecoj zameni, (u1, v1) ne moze da bude u1=v nerednih tabuTenureV iteracija   (tj v ne moze da se izbaci iz trenutnog resenja)  
    tabuTenureU, tabuTenureV = calcTenures(fS, k)
    
    # racunacemo ovo inkrementalno umesto svaki put prilikom poziva generateConstrainedNeighborhood
    degreesTowardsS = [0 for _ in range(V)]
    for i in range(1, V): 
        for j in S:
            if adjMatrix[i][j] == 1:
                degreesTowardsS[i] += 1

    while (tabuIters < L and tabuIters < maxIters):
        #iterStart = timeit.default_timer()

        # posto l i C zavise od funkcije fS, ima smisla ne racunati ih stalno vec 
        # fS = fBestS samo kada se nadje novi najbolji
        if fBestChanged:
            fBestChanged = False
            tabuTenureU, tabuTenureV = calcTenures(fS, k)  

        CN, A, B, minInS, maxOutS = generateConstrainedNeighborhood(tabuList, g, S, notInS, degreesTowardsS, iteration)
 
        desireableDelta = maxOutS - minInS

        T = [move for move in CN if move[2] == desireableDelta]

        bestMove = [-1, -1, -1]   # temp vrednost

        # NOTE: deo u radu o biranju sledeceg poteza moze se protumaciti na 2 nacina 
        if len(T) != 0:
            bestMove = random.choice(T)
        else: 
            l = min(10, k * (k - 1) / 2 - fS)
            p = min(0.1, (l + 2) / g.getNodeCount() )
            
            u = -1
            v = -1

            if random.random() < p:
                u = random.choice(tuple(S))
                kDens = np.floor(k * g.getDensity())
                probV = [v for v in notInS if degreesTowardsS[v] < kDens]
                v = random.choice(probV)
            else:
                u = random.choice(A)
                v = random.choice(B)

            delta = maxOutS - minInS
            if adjMatrix[u][v] == 1:
                delta -= 1
            bestMove = [u, v, delta]

        u = bestMove[0]
        v = bestMove[1]

        S.remove(u)
        S.add(v)

        notInS.remove(v)
        notInS.add(u)

        fS += bestMove[2]

        tabuList[u] = tabuTenureU + iteration
        tabuList[v] = tabuTenureV + iteration
        
        frequencies[u] += 1
        frequencies[v] += 1

        for i in range(1, V): 
           if adjMatrix[i][v] == 1:
               degreesTowardsS[i] += 1

        for i in range(1, V): 
           if adjMatrix[i][u] == 1:
               degreesTowardsS[i] -= 1
        
        if isValid(fS, k):
            return S, iteration

        iteration += 1
        if fS > fBestS:
            fBestChanged = True
            bestS = S
            fBestS = fS
            tabuIters = 0
        else:
            tabuIters += 1

        #iterEnd = timeit.default_timer()
        #print(fBestS, tabuIters, iteration, iterEnd-iterStart)

    return bestS, iteration



def amts (g:Graph, k:int, L:int, maxIters:int):
    frequencies = [0 for _ in range(g.getNodeCount() + 1)]
     
    S = set()
    notInS = deepcopy(g.getNodeSet())

    constructInitialSolution(S, notInS, g, frequencies, k)

    iters = 1
    
    while (iters <= maxIters):
        newS, iters = ts_0(g, S, notInS, frequencies, k, L, iters, maxIters)
        if isValid(f(g, newS), k):
            #print("Returning newS: ", newS)
            return newS, iters
        else: 
            #print(f"Restarting on iteration {iters}")
            # ako su sve frekvencije vece od k, niz treba da se resetuje
            shouldResetFrequencies = True
            for i in range(1, g.getNodeCount() + 1):
                if frequencies[i] < k:
                    shouldResetFrequencies = False
                    break
            
            if shouldResetFrequencies:
                frequencies = [0 for _ in range(g.getNodeCount() + 1)]
            
            S = set()
            notInS = deepcopy(g.getNodeSet())
            constructInitialSolution(S, notInS, g, frequencies, k)
    
    # ako se desi da prodje maxIters, vracamo prazan set kako bi signalizirali neuspeh
    return set(), iters



def isValid(fS, k):
    return fS == k * (k - 1) / 2



def f(g:Graph, S):
    adjMatrix = g.getAdjacencyMatrix()
    f = 0
    for i in S:
        for j in S:
            if adjMatrix[i][j] == 1:
                f += 1
    f /= 2
    return f
