import os, random, math

def parse_instance(file_path):
  horses = []
  adj = {}
  with open(file_path, 'rb') as f:
    lines = f.readlines()
    for i in range(len(lines)-1):
      line = lines[i+1].split()
      if len(line):
        adj[i] = []
        horses.append(line[i])
        for j in range(len(line)):
            if j != i:
              adj[i].append(line[j])
            else:
              adj[i].append(-1)
  return adj, horses

def write_solution(solution):
  with open('output', 'wb') as f:
    for path in solution:
      for horse in path[:-1]:
        f.write("{0} ".format(horse))
      f.write("{0}; ".format(path[-1]))
    f.write("\n")

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


# Change this to be random
def chooseHorse(incoming_edges, outgoing_edges):
    maxHorse = 0
    maxOutgoing = -1
    for e in outgoing_edges:
        if (len(outgoing_edges[e]) > maxOutgoing):
            maxOutgoing = len(outgoing_edges[e])
            maxHorse = e
    return maxHorse

def updateOutgoingEdges(outgoing_edges, best_solution):
    for e in best_solution:
        print("horse " + str(e) + " was deleted.")
        del outgoing_edges[e]
        for horse in outgoing_edges:
            if e in outgoing_edges[horse]:
                outgoing_edges[horse].remove(e)
    return outgoing_edges


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
    while (len(outgoing_edges) > 0):
        # Find the best path
        horse = chooseHorse(incoming_edges, outgoing_edges)
        initialPath = Path()
        initialPath.appendToPath(horse,horses)
        queue = Queue()
        queue.enqueue(initialPath)
        print(initialPath.path)
        solutions = []
        while (not queue.isEmpty()):
            print("Queue size is " + str(queue.size()))
            currPath = queue.dequeue()
            currHorse = currPath.currHorse()
            print("New Curr Horse is: " + str(currHorse))
            if len(outgoing_edges[currHorse]) == 0:
                solutions.append(currPath)
            else:
                if currHorse in outgoing_edges:
                    for horseFriend in outgoing_edges[currHorse]:
                        #path = currPath.spawnNewPath()
                        if horseFriend not in currPath.path and horseFriend in outgoing_edges:
                            path = currPath.spawnNewPath()
                            path.appendToPath(horseFriend, horses)
                            queue.enqueue(path)
                        else:
                            if currPath not in solutions:
                                solutions.append(currPath)

        best_solution = []
        bestWeight = -1
        for path in solutions:
            if path.relayScore() > bestWeight:
                bestWeight = path.relayScore()
                best_solution = path.path
        print("Best Solution is: ")
        print(best_solution)
        solution.append(tuple(best_solution))
        outgoing_edges = updateOutgoingEdges(outgoing_edges, best_solution)
    print(solution)
    return solution

def solve():
    # for file in os.listdir("inputs"):
    #     if file.endswith(".in"):
    #         instance = parse_instance("inputs/{0}".format(str(file)))
    #         #instance = parse_instance("inputs/trivial.in")
    #         solution = solve_instance_BFS_Greedy(instance)
    #         write_solution(solution)
    instance = parse_instance("inputs/1.in")
    solution = solve_instance_BFS_Greedy(instance)


solve()
