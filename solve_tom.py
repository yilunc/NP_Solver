import os, random, math, copy, heapq
from random import randint

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Path:
    def __init__(self):
        self.path = []
        self.weight = 0.0

    def appendToPath(self, val, horses):
        self.path.append(val)
        self.weight = self.weight + int(horses[val]) + 0.001

    def spawnNewPath(self):
        result = Path()
        result.path = list(self.path)
        result.weight = self.weight
        return result

    def currHorse(self):
        return self.path[-1]

    def relayScore(self):
        numHorses = int(math.ceil((self.weight % 1)*1000))
        weight = int(self.weight)
        return weight * numHorses

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def size(self):
        return len(self._queue)


# GLOBAL VARIABLES
topHowManyHorses = 20
tryHowManyTimes = 20

# Gets the top topHowManyHorses horses.
def getTopHorses(outgoing_edges):
    q = PriorityQueue()
    for horse in outgoing_edges:
        q.push(horse, len(outgoing_edges[horse]))
    pledgeHorses = []
    for i in range(0,topHowManyHorses):
        if q.size() != 0:
            pledgeHorses.append(q.pop())
    return pledgeHorses


# Naive way to choose a horse to start with.
# Chooses the horse with the most outgoing edges.
def chooseHorse(outgoing_edges):
    maxHorse = 0
    maxOutgoing = -1
    for e in outgoing_edges:
        if (len(outgoing_edges[e]) > maxOutgoing):
            maxOutgoing = len(outgoing_edges[e])
            maxHorse = e
    return maxHorse

# Randomly chooses a horse out of the top topHowManyHorses horses.
def chooseHorseDFS(pledgeHorses):
    randomHorseIndex = randint(0, len(pledgeHorses) - 1)
    horse = pledgeHorses[randomHorseIndex]
    return horse


# Once a path is found, it deletes those horses so they can't be used again.
def updateOutgoingEdges(outgoing_edges, best_solution):
    for e in best_solution:
        del outgoing_edges[e]
        for horse in outgoing_edges:
            if e in outgoing_edges[horse]:
                outgoing_edges[horse].remove(e)
    return outgoing_edges


def solve_instance_DFS_Greedy(instance):
    adj = instance[0]
    horses = instance[1]
    best_solution = []
    edges = []
    # a dictionary with a horse as key, and an array of horses who have and edge pointing to that horse
    incoming_edges = {}
    # a dictionary with a horse as key, and an array of horses who this horse points to
    outgoing_edges = {}
    for h in adj:
        incoming_edges[h] = []
        outgoing_edges[h] = []
    for h in adj:
        for i in range(len(adj[h])):
            if int(adj[h][i]) and h != i:
                edges.append((h,i))
                incoming_edges[i].append(h)
                outgoing_edges[h].append(i)

    finalRelayTeams = []
    outgoing_edges_base = copy.deepcopy(outgoing_edges)
    while (len(outgoing_edges) > 0):
        possibleSolutions = []
        pledgeHorses = getTopHorses(outgoing_edges)
        for x in range(0, tryHowManyTimes):
            # Mess around with this line to change the way you choose a horse.
            #horse = chooseHorse(outgoing_edges)
            horse = chooseHorseDFS(pledgeHorses)
            #print("Starting on horse " + str(horse))
            initialPath = Path()
            initialPath.appendToPath(horse, horses)
            condition = True
            while condition:
                currHorse = initialPath.currHorse()
                maxHorse = -1
                maxWeight = -1
                for e in outgoing_edges[currHorse]:
                    print(type(horses[e]))
                    if horses[e] > maxWeight and e not in initialPath.path:
                        maxWeight, maxHorse = horses[e], e
                if maxHorse != -1 and maxHorse not in initialPath.path:
                    initialPath.appendToPath(maxHorse,horses)
                else:
                    #print(initialPath.path)
                    possibleSolutions.append(initialPath)
                    condition = False

        # Get the best overall path.
        best_solution = []
        bestWeight = -1
        for path in possibleSolutions:
            if path.relayScore() > bestWeight:
                bestWeight = path.relayScore()
                best_solution = path.path

        # Append that to the final relay teams.
        finalRelayTeams.append(tuple(best_solution))
        # Delete those from the outgoin_edges
        outgoing_edges_base = updateOutgoingEdges(outgoing_edges_base, best_solution)
        outgoing_edges = copy.deepcopy(outgoing_edges_base)
    return finalRelayTeams





# Deprecated
def solve_instance_BFS_Greedy(instance):
    adj = instance[0]
    horses = instance[1]
    best_solution = []

    edges = []

    # a dictionary with a horse as key, and an array of horses who have and edge pointing to that horse
    incoming_edges = {}
    # a dictionary with a horse as key, and an array of horses who this horse points to
    outgoing_edges = {}
    for h in adj:
        incoming_edges[h] = []
        outgoing_edges[h] = []
    for h in adj:
        for i in range(len(adj[h])):
            if int(adj[h][i]) and h != i:
                edges.append((h,i))
                incoming_edges[i].append(h)
                outgoing_edges[h].append(i)

    solution = []
    outgoing_edges_base = copy.deepcopy(outgoing_edges)
    while (len(outgoing_edges) > 0):
        # Find the best path
        horse = chooseHorse(incoming_edges, outgoing_edges)
        initialPath = Path()
        initialPath.appendToPath(horse,horses)
        queue = Queue()
        queue.enqueue(initialPath)
        #print(initialPath.path)
        solutions = []
        print("\toutgoing edges is of size " + str(len(outgoing_edges)))
        while (not queue.isEmpty()):
            #print("Queue size is " + str(queue.size()))

            currPath = queue.dequeue()
            currHorse = currPath.currHorse()
            # print("New Curr Horse is: " + str(currHorse))
            # print(outgoing_edges[currHorse])
            if len(outgoing_edges[currHorse]) == 0: # sketch
                solutions.append(currPath)
            else:
                #if currHorse in outgoing_edges:
                for horseFriend in outgoing_edges[currHorse]:
                    #path = currPath.spawnNewPath()
                    if horseFriend not in currPath.path and horseFriend in outgoing_edges:
                        path = currPath.spawnNewPath()
                        path.appendToPath(horseFriend, horses)
                        queue.enqueue(path)
                        for horse in outgoing_edges:
                            if horseFriend in outgoing_edges[horse]:
                                outgoing_edges[horse].remove(horseFriend)
                    else:
                        if currPath not in solutions:
                            solutions.append(currPath)

        best_solution = []
        bestWeight = -1
        for path in solutions:
            if path.relayScore() > bestWeight:
                bestWeight = path.relayScore()
                best_solution = path.path
        print("\tBest Solution is: ")
        print("\t{0}".format(best_solution))
        solution.append(tuple(best_solution))
        outgoing_edges_base = updateOutgoingEdges(outgoing_edges_base, best_solution)
        outgoing_edges = copy.deepcopy(outgoing_edges_base)
    print("\t{0}".format(solution))
    return solution

# Deprecated #
def solve():
    # for file in os.listdir("inputs"):
    #     if file.endswith(".in"):
    #         instance = parse_instance("inputs/{0}".format(str(file)))
    #         #instance = parse_instance("inputs/trivial.in")
    #         solution = solve_instance_BFS_Greedy(instance)
    #         write_solution(solution)
    instance = parse_instance("inputs/3.in")
    solution = solve_instance_BFS_Greedy(instance)
