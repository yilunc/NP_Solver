import random

class Node():
  def __init__(self, num, score, incoming, outgoing):
    self.num = num
    self.score = score
    self.incoming = set(incoming)
    self.outgoing = set(outgoing)
    self.all_edges = set(incoming + outgoing)

  def __str__(self):
    return "Node({})".format(str(self.num))

  def __repr__(self):
    return "Node({})".format(str(self.num))

  def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.num == other.num
        else:
            return False

  def __hash__(self):
        return hash(self.num)

  def remove_from_adj(self, node):
    if node.num in self.incoming:
      self.incoming.remove(node.num)
    if node.num in self.outgoing:
      self.outgoing.remove(node.num)

  def add_to_incoming(self, node):
    self.incoming.add(node.num)

  def add_to_outgoing(self, node):
    self.outgoing.add(node.num)

class CompressedNode(Node):
  def __init__(self, node1, node2):
    self.num = (node1.num, node2.num)
    self.score = node1.score + node2.score
    self.node1 = node1
    self.node2 = node2
    self.incoming = (node1.incoming | node2.incoming) - set([node1.num, node2.num])
    self.outgoing = (node1.outgoing | node2.outgoing) - set([node1.num, node2.num])
    self.internal = []
    if node2.num in node1.incoming:
      self.internal.append((node2.num, node1.num))
    if node2.num in node1.outgoing:
      self.internal.append((node1.num, node2.num))

  def __str__(self):
   return "CNode({})".format(str((str(self.node1.num), str(self.node2.num))))

  def __repr__(self):
   return "CNode({})".format(str((str(self.node1.num), str(self.node2.num))))

class Graph():
  def __init__(self, nodes):
    self.nodes = nodes
    self.get_node_dict = self._parse_nodes(nodes)
    self.edges = self._get_edges(nodes)
    self.num_compressed_nodes = 0

  def __str__(self):
    s = "Graph("
    for node in self.nodes[:-1]:
      s += "{0}, ".format(str(node))
    if self.nodes:
      s += "{0}".format(str(self.nodes[-1]))
    s += ")"
    return s

  def __repr__(self):
    s = "Graph(("
    for node in self.nodes[:-1]:
      s += "{0}, ".format(str(node))
    if self.nodes:
      s += "{0}) ~~~ (".format(str(self.nodes[-1]))
    for edge in self.edges[:-1]:
      s += "{0}, ".format(str(edge))
    if self.edges:
      s += "{0})".format(str(self.edges[-1]))
    s += ")"
    return s

  def __len__(self):
    return len(self.nodes)

  def _get_edges(self, nodes):
    edges = []
    for node in nodes:
      for other_node_num in node.incoming:
        edges.append((self.get_node_dict[other_node_num], node))
      for other_node_num in node.outgoing:
        edges.append((node, self.get_node_dict[other_node_num]))
    return edges

  def _parse_nodes(self, nodes):
    node_dict = {}
    for node in nodes:
      node_dict[node.num] = node
    return node_dict

  def _remove_node(self, node):
    self.nodes.remove(node)
    del self.get_node_dict[node.num]
    for edge in self.edges:
      if node in edge:
        other_node = [o_node for o_node in edge if o_node != node][0]
        other_node.remove_from_adj(node)
    self.edges = [edge for edge in self.edges if node not in edge]

  def _add_node(self, node):
    self.nodes.append(node)
    self.get_node_dict[node.num] = node
    for incoming in node.incoming:
      self.edges.append((self.get_node_dict[incoming], node))
      self.get_node_dict[incoming].add_to_outgoing(node)
    for outgoing in node.outgoing:
      self.edges.append((self.get_node_dict[outgoing], node))
      self.get_node_dict[outgoing].add_to_incoming(node)

  def compress(self, node1, node2):
    self._remove_node(node1)
    self._remove_node(node2)
    self._add_node(CompressedNode(node1, node2))
    self.num_compressed_nodes += 1

  def has_compressed_node(self):
    return self.num_compressed_nodes > 0

def get_edge_data(instance):
  adj = instance[0]
  horses = instance[1]
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
  return {
          "edges":          edges,
          "incoming_edges": incoming_edges,
          "outgoing_edges": outgoing_edges
          }

def solve_instance(instance):
  adj = instance[0]
  horses = instance[1]
  best_solution = []

  #Parse edges and get incoming, outgoing edges
  print "\t\t Finding Edges.."
  edge_data = get_edge_data(instance)

  print "\t\t Creating Nodes.."
  nodes = [Node(i, horses[i], edge_data["incoming_edges"][i], edge_data["outgoing_edges"][i]) for i in range(len(horses))]
  node_dict = {i: Node(i, horses[i], edge_data["incoming_edges"][i], edge_data["outgoing_edges"][i]) for i in range(len(horses))}

  #Find connected subgraphs
  print "\t\t Finding Subgraphs.."
  connected_subgraphs = []
  while nodes:
    curr_subgraph = set([nodes[0]])
    seen_set = set([nodes[0]])
    curr_nums = set([nodes[0].num])
    for adj in nodes[0].all_edges:
        curr_subgraph.add(node_dict[adj])
        curr_nums.add(node_dict[adj].num)
    while curr_subgraph-seen_set:
      node = (curr_subgraph-seen_set).pop()
      seen_set.add(node)
      for adj in node.all_edges-curr_subgraph:
        curr_subgraph.add(node_dict[adj])
        curr_nums.add(node_dict[adj].num)
    nodes = [node for node in nodes if node not in curr_subgraph]
    connected_subgraphs.append(Graph(list(set(curr_subgraph))))

  #Solve the instance
  print "\t\t Solving.."
  solution = []
  for subgraph in connected_subgraphs:
    print "\t\t Compressing Subgraph.."
    while len(subgraph) > 2:
      edge = subgraph.edges[int(random.random()*len(subgraph.edges))]
      subgraph.compress(edge[0], edge[1])
    print "\t\t Expanding Compressed Nodes"
    while subgraph.has_compressed_node:
      subgraph.compress(edge[0], edge[1])
  return best_solution
