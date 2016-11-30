import os

def parse(file_path):
  scores = []
  adj = {}
  with open(file_path, 'rb') as f:
    lines = f.readlines()
    for i in range(len(lines)-1):
      line = lines[i+1].split()
      if len(line):
        adj[i] = []
        scores.append(line[i])
        for j in range(len(line)):
            if j != i:
              adj[i].append(line[j])
            else:
              adj[i].append(-1)
  return adj, scores

def write_solution(solution, file_name):
  with open('{0}.sol'.format(file_name), 'wb') as f:
    for path in solution:
      for horse in path[:-1]:
        f.write("{0} ".format(horse))
      f.write("{0}; ".format(path[-1]))

#TODO
def solve_instance(instance):
  adj = instance[0]
  scores = instance[1]
  solution = []

def solve():
  for file in os.listdir("cs170_final_inputs"):
    if file.endswith(".in"):
        instance = parse("cs170_final_inputs/{0}".format(str(file)))
        solution = solve_instance(instance)