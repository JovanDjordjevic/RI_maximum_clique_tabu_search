from GraphClass import *

# koliko bi trebalo da bude max? 
MAX = 4000

subset = [0] * MAX

# funckcija koja proverava da li je trenutni podskup klik velicine k
def isClique(g, k):
    for i in range(1, k):
        for j in range(i+1, k):

            # ako bilo koja grana nedostaje znaci da nije klik i mozemo odmah da vratimo false
            if(g.adjacencyMatrix[subset[i]][subset[j]]) == 0:
                return False

    return True

def maxClique_bruteforce(g, i, l):
    max_clique= 0

    # proveravamo da li mozemo da dodamo bilo koji čvor tako da prosimo podskup i da on i dalje bude klik
    for j in range(i+1, g.nodeCount):
        subset[l] = j

        if(isClique(g, l+1)):
            max_clique = max(max_clique, l)
            max_clique = max(max_clique, maxClique_bruteforce(g, j, l+1))

    return max_clique