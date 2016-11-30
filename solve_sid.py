import os
import horse_template as template
import numpy as np
import random


def toMatrix(dictionary):
	l = list()
	for k in dictionary.keys():
		valueList = dictionary[k]
		l.append(valueList)
	matrix = np.matrix(l)
	return matrix

def makeGraph(adj, scores):
	""" Converts the adj and scores into a graph like structure"""
	#VERTICES
	vertices = set() # A set of vertices
	#Initialize the vertices. AKA the number of horses
	for h in range(0, len(adj.keys())):
		vertices.add(h)

	#EDGES
	edges = set()
	for h1 in adj.keys():
		h2 = 0
		for h2_val in adj[h1]:
			if(int(h2_val) == 1):
				if (h1 == h2):
					pass
				else:
					edge = (h1,h2)
					edges.add(edge)
			h2 += 1
	
	#SCORE_DICTIONARY
	scoreDict = dict()
	for v in vertices:
		scoreDict[v] = scores[v]

	return vertices, edges, scoreDict

#deprecated
def recurseThroughGraph(parent_vertice, vertices,edges,scores, visited):
	print "ParentVertice: ", parent_vertice
	if(parent_vertice in visited):
		return
	visited.add(parent_vertice)
	children = list()
	for el in edges:
		if(el[0] == parent_vertice):
			# Is child
			child = el[1]
			print "\t",child
			recurseThroughGraph(child,vertices,edges,scores,visited)
			# children.append(el[1])
	return visited
	
	# print "Children: ",children

def construct_all_possible_paths(start, vertices, edges):
	"""
	A function that constructs ALL possible paths and returns them.
	INPUT  	start - the start vertice for out path building
			vertices - a set of all the vertices in the graph
			edges -  a set of all the valid edges in the graph
	OUTPUT A set of all possible paths
	"""
	raise NotImplementedError()

def choose_path_with_max_score(paths, scores):
	"""
	A function that takes in the set of all paths, assigns scores to the paths 
	and then chooses the path with the maximum score.
	INPUT A set of all the possible paths
	OUTPUT The path with the maximum score
	"""
	raise NotImplementedError()

def mark_as_visited(path):
	"""
	A fucntion to take in the elements of a path and add them to the visited set
	INPUT A path
	OUTPUT Updated visited set
	"""
	raise NotImplementedError()

def update_graph(vertices,edges,visited):
	"""
	A function to update the graph by removing all the vertices (and associated edges) from it which occur
	in the set 'visited'.
	INPUT 	vertices, edges representation of the graph
			visited - set of vertices which need to be removed
	OUTPUT  vertices, edges - updated versions
	NOTE 	make sure to remove everything correctly from both vertices and edges
	"""
	raise NotImplementedError()


adj, scores = template.parse("sample1.in")
vertices, edges, scores = makeGraph(adj, scores)
visited = set()
teams = set()
#Graph is ready

while(len(vertices)>0):
	#Step I: Choose a random starting vertex
	start  = random.sample(vertices,1)[0]
	paths = construct_all_possible_paths(start, vertices, edges)
	best_path = choose_path_with_max_score(paths)
	teams.add(best_path)
	visited = mark_as_visited(best_path) # add all elements of best path
	vertices, edges, scores = update_graph(vertices,edges,scores,visited)

print "The best possible combination of teams is: ", teams



