import os, random

class Node():
  def __init__(self, num, score, incoming, outgoing):
    self.num = num
    self.score = score
    self.incoming = incoming
    self.outgoing = outgoing

  def __str__(self):
    return str(self.num)

  def __repr__(self):
    return str(self.num)

class CompressedNode():
  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.score = node1.score + node2.score

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

def score_solution(solution):
  score = 0
  for path in solution
    score += sum(path)*len(path)
  return score

def solve_instance(instance):
  adj = instance[0]
  horses = instance[1]
  best_solution = []

  edges = []
  incoming_edges = {}
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

  nodes = [Node(i, horses[i], incoming_edges[i], outgoing_edges[i]) for i in range(len(horses))]

  connected_subgraphs = []
  while nodes:
    curr_subgraph = [nodes[0]]
    for node in nodes[1:]:
      for node_sub in curr_subgraph:
        if node not in curr_subgraph and node_sub.num in node.incoming or node_sub in node.outgoing:
          curr_subgraph.append(node)
    nodes = [node for node in nodes if node not in curr_subgraph]
    connected_subgraphs.append(curr_subgraph)

  solution = []
  for sg in connected_subgraphs:
    edge_to_compress = edges[int(random.random()*len(edges))]

  return best_solution

def solve(input_num=None):
  if not input_num:
    for file in os.listdir("cs170_final_inputs"):
      if file.endswith(".in"):
          instance = parse_instance("cs170_final_inputs/{0}".format(str(file)))
          solution = solve_instance(instance)
          write_solution(solution)
  else:
    for file in os.listdir("cs170_final_inputs"):
      if str(file) == "{0}.in".format(input_num):
          instance = parse_instance("cs170_final_inputs/{0}".format(str(file)))
          solution = solve_instance(instance)
          write_solution(solution)

