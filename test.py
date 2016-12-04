import sys, os
import solve_sid
import solve_yil
import solve_tom
import gurik

ALGORITHMS = {
              "yilun":  solve_yil.solve_instance,
              "gurik":  gurik.solver,
              "tommy":  solve_tom.solve_instance_DFS_Greedy,
              "sid" :  solve_sid.solve,
              }

def score_solution(solution, instance):
  score = 0
  len_sum = 0
  for path in solution:
    path_score = 0
    for vertex_num in path:
      if vertex_num is not None:
        path_score += int(instance[1][vertex_num])
    score += path_score*len(path)
    len_sum += len(path)
  avg_len = float(len_sum)/float(len(solution))
  return score, avg_len

def write_solution(solution):
  with open('output.out', 'a') as f:
    for path in solution:
      for horse in path[:-1]:
        f.write("{0} ".format(horse))
      f.write("{0}; ".format(path[-1]))
    f.write("\n")

def write_score(name, in_num, score):
  with open('outputScore.out', 'a') as f:
    f.write("{0} {1}: {2}".format(name, in_num, score))
    f.write("\n")

def is_valid(solution, instance):
  seen = set()
  for team in solution:
    if team[0] in seen:
        return False, "Repeated Horse {0}".format(team[0])
    seen.add(team[0])
    for i in range(0,len(team)-1):
      if team[i+1] in seen:
        return False, "Repeated Horse {0}".format(team[i+1])
      if (instance[0][team[i]][team[i+1]]==0):
        return False, "Horse is not a friend"
      seen.add(team[i+1])
  return True, ""

def parse_instance(file_path):
  horses = []
  adj = {}
  with open(file_path, 'rb') as f:
    lines = f.readlines()
    for i in range(len(lines)-1):
      line = lines[i+1].split()
      if len(line):
        adj[i] = []
        horses.append(int(line[i]))
        for j in range(len(line)):
            if j != i:
              adj[i].append(int(line[j]))
            else:
              adj[i].append(-1)
  return adj, horses

def solve(alg_names=None, in_num=None):
  instances = {}
  instance_nums = []
  algorithms = ALGORITHMS

  if alg_names:
    algorithms = alg_names.split(",")

  if in_num:
    for file in os.listdir("cs170_final_inputs"):
      if str(file) == "{0}.in".format(in_num):
        print("Parsing {0}.in ...".format(in_num))
        instances[in_num] = (parse_instance("cs170_final_inputs/{0}".format(str(file))))
        instance_nums.append(in_num)
  else:
    for file in os.listdir("cs170_final_inputs"):
      if file.endswith(".in"):
        print("Parsing {0} ... ".format(file))
        instances[int(file.split('.')[0])] = parse_instance("cs170_final_inputs/{0}".format(str(file)))
        instance_nums.append(int(file.split('.')[0]))

  instance_nums.sort()

  runHowManyIterations = 5
  for instance in instance_nums:
    for alg in algorithms:
        print("\033[94mSolving on {0}.in on {1}'s algorithm... \033[1m \033[93m".format(instance, alg))
        bestSolution = None
        bestScore = -1
        bestAvgLen = -1
        for z in range(0,runHowManyIterations):
            solution = ALGORITHMS[alg](instances[instance])
            validity = is_valid(solution, instances[instance])
            if validity[0]:
                score, avg_len = score_solution(solution, instances[instance])
                if score > bestScore:
                    bestScore, bestSolution, bestAvgLen = score, solution, avg_len
            else:
                print "\033[91m INVALID SOLUTION, {0}: {1}".format(validity[1], solution)
                return
        write_solution(bestSolution)
        write_score(alg, instance, bestScore)
        print ("\033[92m\tApproximation: {0}".format(bestSolution)[:100] + "...")
        print ("\tInput Size: {0}".format(len(instances[instance][1])))
        print ("\tNumber of Teams: {0}".format(len(bestSolution)))
        print ("\tAverage Team Size: {0}".format(bestAvgLen))
        print ("\tBiggest Team Size: {0}".format(len(max(bestSolution, key=len))))
        print ("\tSmallest Team Size: {0}".format(len(min(bestSolution, key=len))))
        print ("\tScore: {0}".format(bestScore))


if (len(sys.argv) == 3) and sys.argv[2].isdigit():
  solve(alg_names=sys.argv[1], in_num=int(sys.argv[2]))
elif (len(sys.argv) == 2) and sys.argv[1].isdigit():
  solve(in_num=int(sys.argv[1]))
elif (len(sys.argv) == 2):
  solve(alg_names=sys.argv[1])
elif (len(sys.argv) == 1):
  solve()
else:
  print("ERROR: invalid argument(s).")
