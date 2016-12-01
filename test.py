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

def solve(in_num=None, script_path=None):
  if not input_num:
    for file in os.listdir("cs170_final_inputs"):
      if file.endswith(".in"):
          print("Running on {0}: ".format(file))
          instance = parse_instance("cs170_final_inputs/{0}".format(str(file)))
          print("\tFinished parsing..")
          solution = solve_instance(instance)
          print("\tFound approximation:")
          write_solution(solution)
          print ("\t{0}".format(solution))
  else:
    for file in os.listdir("cs170_final_inputs"):
      if str(file) == "{0}.in".format(input_num):
          print("Running on {0}.in".format(input_num))
          instance = parse_instance("cs170_final_inputs/{0}".format(str(file)))
          print("\tFinished parsing..")
          solution = solve_instance(instance)
          write_solution(solution)
          print ("\tFound approximation: {0}".format(solution))

if __name__ == '__main__':
  solve()
