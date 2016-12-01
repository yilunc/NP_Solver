import random
import heapq


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
    for i in range(0,len(horses)):
        pq.push(i, priority=int(horses[i]))
    while not pq.empty():
        current_best = pq.pop()
        value = horses[current_best]
        current_friend = None
        friend_score = -1
        temp = adj[current_best]
        for i in range(0,500):
            if temp[i] == '1' and horses[i] > friend_score and i not in used:
                current_friend = i
        if current_friend != None:
            used.add(current_friend)
        found = False
        if lst == []:
            lst += [[current_best,current_friend]]
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
    for i in range(0,len(lst)):
        for j in range(0,len(lst)):
            if i == j:
                continue
            elif lst[i][0] == lst[j][len(lst[j])-1] and i not in used2 and j not in used2:
                temp = lst[j] + lst[i][1:]
                final += [temp]
                used2.add(i)
                used2.add(j)
            elif lst[j][0] == lst[i][len(lst[i])-1] and i not in used2 and j not in used2:
                temp = lst[i] + lst[j][1:]
                final += [temp]
                used2.add(i)
                used2.add(j)
    finalscore = 0
    len_sum = 0
    for path in final:
        len_sum += len(path)
        score = 0
        for i in range(len(path)):
            if path[i] != None:
                score += int(horses[path[i]])
        finalscore += score * len(path)

    print "\tBEFORE COMPRESS: " + str(len(lst))
    print "\tAFTER COMPRESS: " + str(len(final))
    return final
