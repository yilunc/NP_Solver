import os, random, Queue
import heapq

def parse_instance(file_path):
  horses = []
  adj = {}
  already_ran = set()
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

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self.counter = 0

    # insert priority to -priority can change to max priority queue
    def push(self, item, priority):
        self.counter +=1
        heapq.heappush(self._queue, (-priority, item))

    def pop(self):
        self.counter -=1
        return heapq.heappop(self._queue)[1]

    def empty(self):
        return self.counter <= 0

    def __str__(self):
        return str(self._queue)


def solver(instance):
    adj, horses = instance
    used = set()
    used2 = set()
    lst = []
    final = []
    pq = PriorityQueue()
    cant = {}
    for i in range(0,len(horses)):
        pq.push(i, priority=int(horses[i]))
    while not pq.empty():
        current_best = pq.pop()
        value = horses[current_best]
        current_friend = None
        friend_score = -1
        temp = adj[current_best]
        for i in range(0,len(horses)):
            if temp[i] == '1' and horses[i] > friend_score and i not in used:
                    if current_best in cant and cant[current_best] == i:
                        continue
                    else:
                        current_friend = i
        if current_friend != None:
            used.add(current_friend)
            cant[current_friend] = current_best

        found = False
        if lst == []:
            lst += [[current_best,current_friend]]
            found = True
        else:
            for i in range(0, len(lst)):
                if lst[i][0] == current_friend and not found:
                    lst[i] = [current_best] + lst[i]
                    found = True
                elif lst[i][len(lst[i])-1] == current_best and not found:
                    lst[i] = lst[i] + [current_friend]
                    found = True
        if not found:
            lst += [[current_best,current_friend]]
    double_check = [True]*len(lst)

    for i in range(0,len(lst)):
        for j in range(0,len(lst)):
            if i == j:
                continue
            elif lst[i][0] == lst[j][len(lst[j])-1] and i not in used2 and j not in used2:
                temp = lst[j] + lst[i][1:]
                final += [temp]
                used2.add(i)
                used2.add(j)
                double_check[i]=False
                double_check[j]=False
            elif lst[j][0] == lst[i][len(lst[i])-1] and i not in used2 and j not in used2:
                temp = lst[i] + lst[j][1:]
                final += [temp]
                used2.add(i)
                used2.add(j)
                double_check[i]=False
                double_check[j]=False
    for i in range(0,len(lst)):
        if double_check[i]:
            final += [lst[i]]
    finalscore = 0
    len_sum = 0
    for element in final:
        len_sum += len(element)
        score = 0
        for i in range(0,len(element)):
            if element[i] != None:
                score += int(horses[element[i]])
        finalscore += score * len(element)
    print "\tBEFORE COMPRESS: " + str(len(lst))
    print "\tAFTER COMPRESS: " + str(len(final))
    print final
    return final
