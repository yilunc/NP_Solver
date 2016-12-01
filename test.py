import sys, os
import solve_yil
import solve_tom
import gurik

ALGORITHMS = {
              "yilun":  solve_yil.solve_instance,
              "tommy":  solve_tom.solve_instance_BFS_Greedy,
              "gurik":  gurik.solver,
              "sidd" :  None,
              }

def score_solution(solution, instance):
  score = 0
  for path in solution:
    path_score = 0
    for vertex_num in path:
      path_score += instance[1][vertex_num]
    score += path_score*len(path)
  return score

def write_solution(solution):
  with open('output', 'wb') as f:
    for path in solution:
      for horse in path[:-1]:
        f.write("{0} ".format(horse))
      f.write("{0}; ".format(path[-1]))
    f.write("\n")

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
  algorithms = ALGORITHMS

  if alg_name:
    algorithms = [alg_name]

  if in_num:
    for file in os.listdir("cs170_final_inputs"):
      if str(file) == "{0}.in".format(in_num):
        print("Parsing {0}.in ...".format(in_num))
        instances[in_num] = (parse_instance("cs170_final_inputs/{0}".format(str(file))))
  else:
    for file in os.listdir("cs170_final_inputs"):
      if file.endswith(".in"):
        print("Parsing {0} ... ".format(file))
        instances[int(file.split('.')[0])] = parse_instance("cs170_final_inputs/{0}".format(str(file)))

  for instance in range(1, len(instances)+1):
    for alg in algorithms:
      print("Solving on {0}.in on {1}'s algorithm...".format(instance, alg))
      solution = ALGORITHMS[alg](instances[instance])
      write_solution(solution)
      print ("\tFound approximation: {0} with score {1}".format(solution, score_solution(solution, instance)))

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