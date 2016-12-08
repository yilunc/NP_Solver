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
        self.elements = set()
        self.weight = 0.0

    def appendToPath(self, val, horses):
        self.path.append(val)
        self.elements.add(val)
        self.weight = self.weight + int(horses[val]) + 0.001

    def spawnNewPath(self):
        result = Path()
        result.path = list(self.path)
        result.weight = self.weight
        result.elements = set(self.elements)
        return result

    def currHorse(self):
        return self.path[-1]

    def relayScore(self):
        numHorses = int(math.ceil((self.weight % 1)*1000))
        weight = int(self.weight)
        return weight * numHorses

    def __len__(self):
      return len(self.path)

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
topHowManyHorses = 30
tryHowManyTimes = 300

# Gets the top topHowManyHorses horses.
def getTopHorses_Limit(outgoing_edges, topHowManyHorses):
    q = PriorityQueue()
    for horse in outgoing_edges:
        q.push(horse, len(outgoing_edges[horse]))
    pledgeHorses = []
    for i in range(0,topHowManyHorses):
        if q.size() != 0:
            pledgeHorses.append(q.pop())
    return pledgeHorses

def getTopHorses(outgoing_edges):
    q = PriorityQueue()
    for horse in outgoing_edges:
        q.push(horse, len(outgoing_edges[horse]))
    pledgeHorses = []
    for i in range(0,q.size()):
      pledgeHorses.append(q.pop())
    return pledgeHorses

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
        EXIT=False
        possibleSolutions = []
        pledgeHorses = getTopHorses(outgoing_edges)
        for x in range(0, tryHowManyTimes):
            if EXIT:
              break
            # Mess around with this line to change the way you choose a horse
            horse = chooseHorseDFS(pledgeHorses)
            initialPath = Path()
            initialPath.appendToPath(horse, horses)
            condition = True
            while condition:
                currHorse = initialPath.currHorse()
                maxHorse, maxWeight = -1, -1
                edge_horses = []
                for e in outgoing_edges[currHorse]:
                  if horses[e] > maxWeight and e not in initialPath.elements:
                    maxWeight, maxHorse = horses[e], e
                if maxHorse != -1:
                      initialPath.appendToPath(maxHorse, horses)
                else:
                  possibleSolutions.append(initialPath)
                  if len(initialPath) == len(horses):
                    EXIT=True
                  condition = False
        if not EXIT:
          for x in range(0, 200):
              if EXIT:
                break
              # Mess around with this line to change the way you choose a horse.
              horse = chooseHorseDFS(pledgeHorses)
              initialPath = Path()
              initialPath.appendToPath(horse, horses)
              condition = True
              while condition:
                  currHorse = initialPath.currHorse()
                  maxHorse, maxWeight = -1, -1
                  edge_horses = []
                  for e in outgoing_edges[currHorse]:
                    if horses[e] > maxWeight and e not in initialPath.elements:
                      maxWeight, maxHorse = horses[e], e
                      edge_horses.append((horses[e], e))
                  edge_horses = sorted(edge_horses, key=lambda x: int(x[0]), reverse=False)
                  if maxHorse != -1 & maxWeight != -1:
                    for weight, horse in edge_horses:
                      if horse not in initialPath.path:
                        initialPath.appendToPath(horse,horses)
                        break
                  else:
                    if len(initialPath) == len(horses):
                      EXIT=True
                    possibleSolutions.append(initialPath)
                    condition = False
        if not EXIT:
          for x in range(0, 200):
              if EXIT:
                break
              # Mess around with this line to change the way you choose a horse.
              horse = chooseHorseDFS(pledgeHorses)
              initialPath = Path()
              initialPath.appendToPath(horse, horses)
              condition = True
              while condition:
                  currHorse = initialPath.currHorse()
                  maxHorse, maxWeight = -1, -1
                  edge_horses = []
                  for e in outgoing_edges[currHorse]:
                    if horses[e] > maxWeight and e not in initialPath.elements:
                      maxWeight, maxHorse = horses[e], e
                      edge_horses.append((horses[e], e))
                  edge_horses = sorted(edge_horses, key=lambda x: int(x[0]), reverse=True)
                  if maxHorse != -1 & maxWeight != -1:
                    for weight, horse in edge_horses:
                      if horse not in initialPath.path:
                        initialPath.appendToPath(horse,horses)
                        break
                  else:
                    if len(initialPath) == len(horses):
                      EXIT=True
                    possibleSolutions.append(initialPath)
                    condition = False
        if not EXIT:
          pledgeHorses = getTopHorses_Limit(outgoing_edges, topHowManyHorses)
          for x in range(0, tryHowManyTimes):
              if EXIT:
                break
              # Mess around with this line to change the way you choose a horse.
              #horse = chooseHorse(outgoing_edges)
              horse = chooseHorseDFS(pledgeHorses)
              initialPath = Path()
              initialPath.appendToPath(horse, horses)
              condition = True
              while condition:
                  currHorse = initialPath.currHorse()
                  maxHorse = -1
                  maxWeight = -1
                  for e in outgoing_edges[currHorse]:
                      #print(type(horses[e]))
                      if horses[e] > maxWeight and e not in initialPath.path:
                          maxWeight, maxHorse = horses[e], e
                  if maxHorse != -1 and maxHorse not in initialPath.path:
                      initialPath.appendToPath(maxHorse,horses)
                  else:
                      possibleSolutions.append(initialPath)
                      if len(initialPath) == len(horses):
                        EXIT=True
                      condition = False
        if not EXIT:
          pledgeHorses = getTopHorses(outgoing_edges)
          print "\t Doing random, fuck"
          for x in range(0, 500000):
              if EXIT:
                break
              # Mess around with this line to change the way you choose a horse.
              horse = chooseHorseDFS(pledgeHorses)
              initialPath = Path()
              initialPath.appendToPath(horse, horses)
              condition = True
              while condition:
                  currHorse = initialPath.currHorse()
                  maxHorse, maxWeight = -1, -1
                  edge_horses = []
                  available_horses = set(outgoing_edges[currHorse]) - initialPath.elements
                  if available_horses:
                    next_horse = random.sample(available_horses, 1)[0]
                    initialPath.appendToPath(next_horse,horses)
                  else:
                    if len(initialPath) == len(horses):
                      EXIT=True
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
    print finalRelayTeams
    return finalRelayTeams
