import random

class Node():
  def __init__(self, num, score):
    self.num = num
    self.score = score
    self.incoming = set()
    self.outgoing = set()
    self.all_edges = set()

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

  def init_incoming(self, incoming):
    self.incoming = set(incoming)
    self.all_edges = self.incoming | self.outgoing

  def init_outgoing(self, outgoing):
    self.outgoing = set(outgoing)
    self.all_edges = self.incoming | self.outgoing

  def remove_from_adj(self, node):
    if node in self.incoming:
      self.incoming.remove(node)
    if node in self.outgoing:
      self.outgoing.remove(node)

  def add_to_incoming(self, node):
    self.incoming.add(node)

  def add_to_outgoing(self, node):
    self.outgoing.add(node)

class CompressedNode(Node):
  def __init__(self, node1, node2):
    self.num = (node1.num, node2.num)
    self.score = node1.score + node2.score
    self.node1 = node1
    self.node2 = node2
    self.incoming = (node1.incoming | node2.incoming) - set([node1, node2])
    self.incoming1 = node1.incoming - set([node1, node2])
    self.incoming2 = node2.incoming - set([node1, node2])
    self.outgoing = (node1.outgoing | node2.outgoing) - set([node1, node2])
    self.outgoing1 = node1.outgoing - set([node1, node2])
    self.outgoing2 = node2.outgoing - set([node1, node2])
    self.internal = []
    if node2 in node1.incoming:
      self.internal.append((node2, node1))
    if node2 in node1.outgoing:
      self.internal.append((node1, node2))

  def __str__(self):
   return "CNode({})".format(str((str(self.node1.num), str(self.node2.num))))

  def __repr__(self):
   return "CNode({})".format(str((str(self.node1.num), str(self.node2.num))))

class Graph():
  def __init__(self, nodes):
    self.nodes = nodes
    self.edges, self.edge_map = self._get_edges(nodes)
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
    edge_map = {}
    for node in nodes:
      for other_node in node.incoming:
        edge_map[(other_node.num, node.num)] = (other_node, node)
        edges.append((other_node, node))
      for other_node in node.outgoing:
        edge_map[((node.num, other_node.num))] = (node, other_node)
        edges.append((node, other_node))
    return edges, edge_map

  def _parse_nodes(self, nodes):
    node_dict = {}
    for node in nodes:
      node_dict[node.num] = node
    return node_dict

  def _remove_node(self, node):
    self.nodes.remove(node)
    for edge in self.edges:
      if node in edge:
        other_node = [o_node for o_node in edge if o_node != node][0]
        other_node.remove_from_adj(node)
    self.edges = [edge for edge in self.edges if node not in edge]


  def _add_node(self, node):#FIX THIS SHIT TOO
    self.nodes.append(node)

    for incoming in node.incoming1:
      self.edge_map[(incoming.num, node.num)] = (incoming, node.node1)
      self.edges.append((incoming, node))
      incoming.add_to_outgoing(node)

    for incoming in node.incoming2:
      self.edge_map[(incoming.num, node.num)] = (incoming, node.node2)
      self.edges.append((incoming, node))
      incoming.add_to_outgoing(node)

    for outgoing in node.outgoing1:
      self.edge_map[(node.num, outgoing.num)] = (node.node1, outgoing)
      self.edges.append((node, outgoing))
      outgoing.add_to_incoming(node)

    for outgoing in node.outgoing2:
      self.edge_map[(node.num, outgoing.num)] = (node.node2, outgoing)
      self.edges.append((node, outgoing))
      outgoing.add_to_incoming(node)

  def _add_nodes(self, node1, node2):
    self.nodes.append(node1)
    self.nodes.append(node2)

    for incoming in node1.incoming:
      self.edges.append((incoming, node1))
      incoming.add_to_outgoing(node1)
    for outgoing in node1.outgoing:
      self.edges.append((node1, outgoing))
      outgoing.add_to_incoming(node1)

    for incoming in node2.incoming:
      self.edges.append((incoming, node2))
      incoming.add_to_outgoing(node2)
    for outgoing in node2.outgoing:
      self.edges.append((node2, outgoing))
      outgoing.add_to_incoming(node2)

  def compress(self, node1, node2):
    self._remove_node(node1)
    self._remove_node(node2)
    cnode = CompressedNode(node1, node2)
    self._add_node(cnode)
    self.num_compressed_nodes += 1
    return cnode

  def decompress(self, node):
    self._remove_node(node)
    self._add_nodes(node.node1, node.node2)
    self.num_compressed_nodes -= 1

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
          "incoming_nodes": incoming_edges,
          "outgoing_nodes": outgoing_edges
          }

def can_add(edge, path):
  return len(path) == 0 or (edge[1].num not in path and path[-1] == edge[0].num)

def add_edge_to_path(edge, path):
  if not can_add(edge, path):
    print("\tERROR: CANNOT ADD {0} TO PATH".format(edge))
  path.append(edge[1].num)
  return True

def get_o_edge(edge, subgraph):
  o_edge = subgraph.edge_map[(edge[0].num, edge[1].num)]
  while not (isinstance(o_edge[0].num, int) and isinstance(o_edge[1].num, int)):
    o_edge = subgraph.edge_map[(o_edge[0].num, o_edge[1].num)]
  return o_edge

def solve_instance(instance):
  adj = instance[0]
  horses = instance[1]
  best_solution = []

  #Parse edges and get incoming, outgoing edges
  print "\tFinding Edges.."
  edge_data = get_edge_data(instance)

  print "\tCreating Nodes.."
  node_dict = {}
  nodes = []
  for i in range(len(horses)):
    node = Node(i, horses[i])
    nodes.append(node)
    node_dict[i] = node

  for i in range(len(horses)):
    incoming = [node_dict[x] for x in edge_data["incoming_nodes"][i]]
    outgoing = [node_dict[x] for x in edge_data["outgoing_nodes"][i]]
    node_dict[i].init_incoming(incoming)
    node_dict[i].init_outgoing(outgoing)

  #Find connected subgraphs
  print "\tFinding Subgraphs.."
  connected_subgraphs = []
  while nodes:
    curr_subgraph = set([nodes[0]])
    seen_set = set([nodes[0]])
    curr_nums = set([nodes[0].num])
    for adj in nodes[0].all_edges:
        curr_subgraph.add(adj)
        curr_nums.add(adj.num)
    while curr_subgraph-seen_set:
      node = (curr_subgraph-seen_set).pop()
      seen_set.add(node)
      for adj in node.all_edges-curr_subgraph:
        curr_subgraph.add(adj)
        curr_nums.add(adj.num)
    nodes = [node for node in nodes if node not in curr_subgraph]
    connected_subgraphs.append(Graph(list(set(curr_subgraph))))

  #Solve the instance
  print "\tSolving.."
  solutions = []
  for subgraph in connected_subgraphs:
    compression_order = []

    print "\tCompressing Subgraph.."
    while len(subgraph) > 2:
      edge = subgraph.edges[int(random.random()*len(subgraph.edges))]
      cnode = subgraph.compress(edge[0], edge[1])
      compression_order.append(cnode)

    print "\t{}".format(subgraph)

    print "\tExpanding Compressed Nodes.."
    #Find starting points for possible paths
    seen = set()
    for edge in subgraph.edges:
      o_edge = get_o_edge(edge, subgraph)
      if o_edge[0].num not in seen:
        solutions.append([[o_edge[0].num]])
        seen.add(o_edge[0].num)

    print solutions
    #Decompress the compressed nodes, and pick an edge
    while subgraph.has_compressed_node():
      for cnode in compression_order[::-1]:
        for inner_edge in cnode.internal:
          edge = get_o_edge(inner_edge, subgraph)
          for solution in solutions:
            added_edge = False
            for path in solution:
              if can_add(edge, path):
                added_edge = add_edge_to_path(edge, path)
                break
            if not added_edge:
              solution.append([edge[0].num])

        subgraph.decompress(cnode)
  print solutions
  return solution
