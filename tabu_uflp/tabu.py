import random

def readInput(filename):
    with open(filename, 'r') as f:
        numUsers, numResources = [int(x) for x in f.readline().split()]
        cost = [[int(j) for j in f.readline().split()] for i in range(numUsers)]
        fixedCost = [int(x) for x in f.readline().split()]
        
        return numUsers, numResources, cost, fixedCost

def isFeasible(solution):
    for resource in solution:
        if resource:
            return True
    return False

def initialize(numResources, p):
    solution = []
    for i in range(numResources):
        solution.append(random.random() < p)
    if not isFeasible(solution):
        solution[random.randrange(numResources)] = True
    
    return solution

def calcSolutionValue(solution, cost, fixedCost):
    numUsers = len(cost)
    numResources = len(fixedCost)
    value = 0.0
    used = [False for _ in range(numResources)]
    
    for i in range(numUsers):
        minCost = float('inf')
        resourceUsed = -1
        for j in range(numResources):
            if solution[j] and cost[i][j] < minCost:
                minCost = cost[i][j]
                resourceUsed = j
                
        value += minCost
        used[resourceUsed] = True
        
    for j in range(numResources):
        if used[j]:
            value += fixedCost[j]
            
    solution = used
    return value

def copyList(list):
    newList = []
    for el in list:
        newList.append(el)

    return newList

def myInvert(solution):
    solutions = []
    oldSolution = copyList(solution)
    newSolution = copyList(solution)
    for i in range(len(solution)):
        newSolution = copyList(oldSolution)
        solution = copyList(oldSolution)
        newSolution[i] = not solution[i]
        if isFeasible(newSolution):
            solutions.append(newSolution)

    return solutions

def choseRandomSolution(solutions):
    chosen = random.randrange(len(solutions))
    return solutions[chosen]

def restore(solution, j):
    solution[j] = not solution[j]

def getFirstSolutionOut(tabuList):
    newTabu = []
    for i in range(1, len(tabuList)):
        newTabu.append(tabuList[i])

    return newTabu

def TabuSearch(cost, fixedCost, maxIters, maxLenTabuList):
    currSolution = initialize(len(fixedCost), p=0.25)
    currValue = calcSolutionValue(currSolution, cost, fixedCost)
    bestSolution = currSolution
    bestValue = currValue

    tabu_list = [currSolution]

    for i in range(maxIters):
        environment = myInvert(currSolution)
        changedEnvironment = []
        for i in range(len(environment)):
            if environment[i] not in tabu_list:
                changedEnvironment.append(environment[i])

        if(len(changedEnvironment) == 0):
            break

        newSolution = choseRandomSolution(changedEnvironment)
        newValue = calcSolutionValue(newSolution, cost, fixedCost)
        tabu_list.append(newSolution)

        if newValue < currValue:
            currValue = newValue
            currSolution = newSolution
        
        if currValue < bestValue:
            bestValue = currValue
            bestSolution = currSolution
        
        if len(tabu_list) > maxLenTabuList:
            tabu_list = getFirstSolutionOut(tabu_list)

    return bestValue, bestSolution

numUsers, numResources, cost, fixedCost = readInput('/home/tamara/Tamara/MATF/RI/uflp.txt')
print(TabuSearch(cost, fixedCost, maxIters=10000, maxLenTabuList=10))
