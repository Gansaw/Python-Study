import random
import math

NumEval = 0    # Total number of evaluations


def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline())
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        locations.append(eval(line)) # Make a tuple and append
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)
    return numCities, locations, table


def calcDistanceTable(numCities, locations): ###    
    table = []
    for i in range (numCities):
        row = []
        for j in range(numCities):
            distancex = locations[j][0] - locations[i][0]
            distancey = locations[j][1] - locations[i][1]
            distance = round(math.sqrt(distancex ** 2 + distancey ** 2),2)
            row.append(distance)
        table.append(row)   

    return table # A symmetric matrix of pairwise distances


def randomInit(p):   # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init


def evaluate(current, p): ###
    ## Calculate the tour cost of 'current'    
        ## 'p' is a Problem instance
    ## 'current' is a list of city ids

    global NumEval
    NumEval += 1

    n = p[0]
    table = p[2]

    cost = 0
    for i in range(n-1):
        city1 = current[i]
        city2 = current[i + 1]
        cost += table[city1][city2]
    # 원위치로 돌아오는 거리    
    cost += table[current[n-1]][current[0]]

    return cost


def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors

def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
        i += 1
        j -= 1
    return curCopy

def bestOf(neighbors, p): ###    
    best = neighbors[0]
    bestValue = evaluate(best,p)    
    for i in range(1,len(neighbors)):
        value = evaluate(neighbors[i],p)
        if value < bestValue:
            best = neighbors[i]
            bestValue = value        
        
    return best, bestValue

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()


def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()
