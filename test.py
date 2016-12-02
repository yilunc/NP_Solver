import sys, os
import solve_yil
import solve_tom
import gurik

ALGORITHMS = {
              "yilun":  solve_yil.solve_instance,
              "gurik":  gurik.solver,
              "tommy":  solve_tom.solve_instance_DFS_Greedy,
              "sidd" :  None,
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
  with open('output', 'wb') as f:
    for path in solution:
      for horse in path[:-1]:
        f.write("{0} ".format(horse))
      f.write("{0}; ".format(path[-1]))
    f.write("\n")

def is_valid(solution, instance):
  seen = set()
  for team in solution:
    seen.add(team[0])
    for i in range(0,len(team)-2):
      if team[i+1] in seen:
        return False
      else:
        seen.add(team[i+1])
      if (instance[0][team[i]][team[i+1]]==0):
        return False
  return True

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

def solve(alg_name=None, in_num=None):
  instances = {}
  instance_nums = []
  algorithms = ALGORITHMS

  if alg_name:
    algorithms = [alg_name]

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

  for instance in instance_nums:
    for alg in algorithms:
      print("\033[94m Solving on {0}.in on {1}'s algorithm... \033[1m \033[93m".format(instance, alg))
      solution = ALGORITHMS[alg](instances[instance])
      if is_valid(solution, instances[instance]):
        score, avg_len = score_solution(solution, instances[instance])
        write_solution(solution)
        print ("\033[92m\tApproximation: {0}".format(solution)[:100] + "...")
        print ("\tAverage Team Size: {0}".format(avg_len))
        print ("\tBiggest Team Size: {0}".format(len(max(solution, key=len))))
        print ("\tScore: {0}".format(score))
      else:
        print "\033[91m INVALID SOLUTION"
        return

if (len(sys.argv) == 3) and sys.argv[2].isdigit():
  solve(alg_name=sys.argv[1], in_num=int(sys.argv[2]))
elif (len(sys.argv) == 2) and sys.argv[1].isdigit():
  solve(in_num=int(sys.argv[1]))
elif (len(sys.argv) == 2):
  solve(alg_name=sys.argv[1])
elif (len(sys.argv) == 1):
  solve()
else:
  print("ERROR: invalid argument(s).")
