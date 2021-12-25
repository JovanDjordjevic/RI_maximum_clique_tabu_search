from GraphClass import *
import numpy as np
import random

def constructInitialSolution(S:set, notInS:set, g:Graph, frequencies, k):
    nodeToAdd = np.argmin(frequencies[1:]) + 1  # mora + 1 jer sa [1:] ignorisemo 0
    S.add(nodeToAdd)
    notInS.remove(nodeToAdd) 

    V = g.getNodeCount() + 1
    while len(S) < k:
        degreesTowardsS = [0 for _ in range(V)]
        maxDegree = 0
        for i in notInS:
            for j in S:
                if g.adjacencyMatrix[i][j] == 1:
                    degreesTowardsS[i] += 1
                    if degreesTowardsS[i] > maxDegree:
                        maxDegree = degreesTowardsS[i]
        
        # oni sa najvecim brojem grana koji vode ka S a nisu vec u S
        candidates = [i for i in range(1, V) if degreesTowardsS[i] == maxDegree]
        candidates = sorted(candidates, key = lambda i : frequencies[i])

        minFrequency = frequencies[candidates[0]]
        candidates = [i for i in candidates if frequencies[i] == minFrequency]
        
        nodeToAdd = random.choice(candidates)
        S.add(nodeToAdd)
        notInS.remove(nodeToAdd)

    return    

def generateConstrainedNeighborhood(tabuList:set, g:Graph, S:set, notInS:set, currentIteration:int):
    minInS = float('inf')
    maxOutS = float('-inf')

    V = g.getNodeCount() + 1
    degreesTowardsS = [0 for _ in range(V)]
    for i in S: 
        for j in range(1, V):
            if g.adjacencyMatrix[i][j] == 1:
                degreesTowardsS[j] += 1
    # print("S: ", S)
    # print("indexes: ", [i for i in range(V)])
    # print("degrees: ", degreesTowardsS)

    # da je neki cvor tabu tojest nedostupan gledamo takos to pitamod da li je tabuList[cvor] > currentIteration
    # zato sto je tabuList[cvor] = tenure_cvora + iteracija u kojoj je dodat u tabu listu
    for i in S:
        if tabuList[i] < currentIteration and degreesTowardsS[i] < minInS:   
            minInS = degreesTowardsS[i]

    for i in notInS:
        if tabuList[i] < currentIteration and degreesTowardsS[i] > maxOutS:   
            maxOutS = degreesTowardsS[i]
    # print("minInS: ", minInS)
    # print("maxOutS: ", maxOutS)

    A = [u for u in S if tabuList[u] < currentIteration and degreesTowardsS[u] == minInS]
    B = [v for v in notInS if tabuList[v] < currentIteration and degreesTowardsS[v] == maxOutS]
    # print("A: ", A)
    # print("B: ", B)

    constrainedNeighborhood = []
    for i in A:
        for j in B:
            delta = maxOutS - minInS
            if g.adjacencyMatrix[i][j] == 1:
                delta -= 1
            # ako zamenimo i sa j, dobijamo promenu delta
            constrainedNeighborhood.append([i, j, delta])
    
    #print(constrainedNeighborhood)
    desireableDelta = maxOutS - minInS

    return constrainedNeighborhood, A, B, desireableDelta, minInS, maxOutS, degreesTowardsS


# param L je za otkrivanje stagnacije
def ts_0 (g, S, notInS, k, L, iteration):
    i = 0   # broj uzastopnih iteracija koje se funkc f(S) nije poboljsala

    bestS = S

    #tabuList = set()
    V = g.getNodeCount() + 1
    tabuList = [0 for _ in range(V)]

    while (i < L):
        # move je (u, v) tj zamenimo u sa v
        # u stoji u tabu listi tabuTenureU iteracija, tj u sledecoj zameni, (u1, v1) ne moze da bude v1=u nerednih tabuTenureU iteracija   (tj u ne mzoe da se ubaci u naredna resenja)
        # V stoji u tabu listi tabuTenureV iteracija, tj u sledecoj zameni, (u1, v1) ne moze da bude u1=v nerednih tabuTenureV iteracija   (tj v ne moze da se izbaci iz trenutnog resenja)
        l = min(10, k * (k - 1) / 2 - f(g, S))    # bestS ili trenutno S?
        C = max(int( np.floor(k/40) ), 6)
        tabuTenureU = int( l + random.randint(1, C - 1) )
        tabuTenureV = int( np.floor( 0.6 * l + random.randint(1, 0.6 * (C - 1)) ) )  # ima mi smisla da bude floor jer samo ceo broj moze da bude broj iteracija
        # treba uvek da vazi da Tu > Tv
        # print("Tu: ", tabuTenureU)
        # print("Tv: ", tabuTenureV)
        # nije konkretno objasnjeno kako se tacno ovi tenurei koriste u implementaciji

        CN, A, B, desireableDelta, minInS, maxOutS, degreesTowardsS = generateConstrainedNeighborhood(tabuList, g, S, notInS, iteration)

        # u radu kaze da zelimod a napravimo potez koji ima desireableDelta
        # da li to znaci da treba da radimo onaj drugi probabilistic move ako je T prazno ?
        # tamo akze da se probabilsitis move radi ako ne postoji potez koji bvi poboljsao trenutno S
        # tojest kada za svako novo S, f(newS) <= f(S). Da li treba to da proverim? To deluje neefikasno
        # u 2.2.4 kaze da sa verovatnocom p radimo probabilistic a sa verovatnocom 1-p radimo normalan
        # sto deluje kontkradiktorno sa ovim iznad
        T = [move for move in CN if move[2] == desireableDelta]
        #print("T: ", T)

        bestMove = [-1, -1, -1]   # temp vrednost

        if 1==1:                    # TEMP,   ovo je obican move a u else grani je probabilistic
            if len(T) != 0:
                bestMove = random.choice(T)
            else: 
                delta = maxOutS - minInS
                u = random.choice(A)
                v = random.choice(B)
                if g.adjacencyMatrix[u][v] == 1:
                    delta -= 1
                bestMove = [u, v, delta]  #  Notice that  in this latter case, u and v must be two adjacent vertices.   (jel ovo treba da proverim?)
                #print("Best move: ", bestMove)
        else:
            l = min(10, k * (k - 1) / 2 - f(g, S))
            p = min(0.1, (l + 2) / g.getNodeCount() )

            u = random.choice(S)
            probV = [v for v in notInS if degreesTowardsS[v] < np.floor(k * g.getDensity())]
            v = random.choice(probV)
        
        u = bestMove[0]
        v = bestMove[1]
        S.remove(u)
        S.add(v)
        notInS.remove(v)
        notInS.add(u)

        tabuList[u] = tabuTenureU + iteration
        tabuList[v] = tabuTenureV + iteration
        
        if isValid(g, S, k):
            return S, iteration

        iteration += 1
        if f(g, S) > f(g, bestS):
            bestS = S
            i = 0
        else:
            i += 1

    return bestS, iteration

# parametri:
# g - graf,     k - velicina klike,     
# L - dubina pretrage,   maxIters - maksimalan dozvoljen broj iteracija
def amts (g:Graph, k:int, L:int, maxIters:int):
    frequencies = [0 for _ in range(g.getNodeCount() + 1)]    # svaki put kada se neki iskoristi za bilo sta, uveca mu se freq
                                                              # kada za svaki u nizu (osim 0) bude  broj >k onda se resetuje na 0
                                                              # da li su ovo proveravali svaki put ??
    S = set()
    notInS = g.getNodeSet()

    constructInitialSolution(S, notInS, g, frequencies, k)
    # print(S)
    # print(notInS)

    # iteracije morajud a se broje od jedan u suprotnom ce A i B biti praznis kupovi u nultoj iteraciji
    iters = 1
    
    while (iters <= maxIters):
        newS, iters = ts_0(g, S, notInS, k, L, iters)
        #print(f"Next found S: {newS}   fitness: {f(g, newS)}")
        if isValid(g, newS, k):
            #print("Returning newS: ", newS)
            return newS
        else: 
            #print(f"Restarting on iteration {iters}")
            S = set()
            notInS = g.getNodeSet()
            constructInitialSolution(S, notInS, g, frequencies, k)
    
    # ako za sve ove iteracije nije nasao veci clique od onga sto smo vec nasli u okviru funkcije koja ce da poziva amts
    # za svako k=3...|V| onda to signaliziramo pozivajucoj funkciji kao prazan set
    return set()


def isValid(g, S, k):
    if f(g, S) == k * (k - 1) / 2:
        return True
    else:
        return False

def f(g:Graph, S):
    f = 0
    for i in S:
        for j in S:
            if g.adjacencyMatrix[i][j] == 1:
                f += 1
    # u definiciji f u radu, kaze za svako u,v iz S se dodaje +1 ako postoji grana
    # dakle racunaju se duplikati, ali ako tako ubacim u kod, tabu tenure budu negativni sto nije logicno
    f /= 2
    return f
