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

def scores_to_int(scores):
	""" Converts the scores (which are currently strings) to int"""
	for k in scores.keys():
		scores[k] = int(scores[k])
	return scores

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

def _children(currentNode,edges):
    children = set()
    for e in edges:
        if(e[0] == currentNode):
            children.add(e[1])
    return children

def AllPathsUtil(currentNode, path, edges):
    if(currentNode in path):
        _path_collection.add(path)
        return
    path = path + (currentNode, )
    children = _children(currentNode,edges)
    # print "Current Node: ", currentNode
    # print "Children: ", children
    if(len(children) == 0): #no child
            # print "Path: ", path
            _path_collection.add(path)
            # return path
            return
    # case where there are children left
    for child in children:
        AllPathsUtil(child, path, edges)



def construct_all_possible_paths(start, vertices, edges):
    """
    A function that constructs ALL possible paths and returns them.
    INPUT   start - the start vertice for out path building
            vertices - a set of all the vertices in the graph
            edges -  a set of all the valid edges in the graph
    OUTPUT A set of all possible paths

    Trivial

    >>> v = set([1,2,3,4])
    >>> e = set([(1,2),(1,3),(2,4)])
    >>> s = 1
    >>> construct_all_possible_paths(s, v, e)
    set([(1, 3), (1, 2, 4)])

    Case with cycles and backtracking
    >>> v = set([1,2,3,4])
    >>> e = set([(1,2),(1,3),(2,1),(2,4),(2,4)])
    >>> s = 1
    >>> r = construct_all_possible_paths(s, v, e)
    >>> r == set([(1, 3), (1, 2, 4), (1,2)])
    True

    """
    # raiseNotDefined()
    global _path_collection
    _path_collection = set()
    AllPathsUtil(start,(),edges)
    # print "Path Collection: ", _path_collection
    return _path_collection

#Tested
def choose_path_with_max_score(paths, scores):
	"""
	A function that takes in the set of all paths, assigns scores to the paths
	and then chooses the path with the maximum score.
	INPUT A set of all the possible paths
	OUTPUT The path with the maximum score

	Doctests
	>>> paths = [(1,2),(3,)]
	>>> scores = {1 : 10, 2: 10, 3: 10}
	>>> choose_path_with_max_score(paths, scores)
	(1, 2)

	"""
	# raise NotImplementedError()
	paths_to_scores = dict() #ensure paths are tuples
	for path in paths:
		path_score = 0
		for h in path:
			path_score += scores[h]

		paths_to_scores[path] = path_score * len(path) #tom sugg

	max_path = None
	max_score = 0
	for el in paths_to_scores.keys():
		if(paths_to_scores[el] > max_score):
			max_score = paths_to_scores[el]
			max_path = el

	return max_path, max_score

#Tested
def mark_as_visited(path,visited):
	"""
	A function to take in the elements of a path and add them to the visited set
	INPUT A path
	OUTPUT Updated visited set

	>>> path = (1, 2)
	>>> visited = set()
	>>> mark_as_visited(path,visited)
	set([1, 2])

	"""
	# raiseNotDefined()
	for x in path:
		visited.add(x)

	return visited

#Tested
def update_graph(vertices,edges,visited):
	"""
	A function to update the graph by removing all the vertices (and associated edges) from it which occur
	in the set 'visited'.
	INPUT 	vertices, edges representation of the graph
			visited - set of vertices which need to be removed
	OUTPUT  vertices, edges - updated versions
	NOTE 	make sure to remove everything correctly from both vertices and edges

	>>> vertices = set([1,2,3])
	>>> edges = set([(1,2),(2,1),(1,3),(2,3)])
	>>> visited = set([1])
	>>> update_graph(vertices,edges,visited)
	(set([2, 3]), set([(2, 3)]))
	"""
	# raiseNotDefined()
	for v in visited:
		if(v in vertices):
			vertices.remove(v)
		#remove outgoing edges & incoming edges
		edges_to_remove = list()
		for edge in edges:
			if(v in edge):
				edges_to_remove.append(edge)

		for edge in edges_to_remove:
			edges.remove(edge)

	return vertices,edges


def best_team(sets_of_teams):
	"""
	Function to choose the best team from all the teams.
	This is the function which is messing up
	"""
	maxTeamScore = 0
	maxTeam = None

	for team in sets_of_teams.keys():
		teamScore = sets_of_teams[team]
		if (teamScore > maxTeamScore):
			maxTeamScore = teamScore
			maxTeam = team
	return maxTeam, maxTeamScore


#Main
def solve(instance):

	adj, scores = instance
	vertices, edges, scores = makeGraph(adj, scores)
	scores = scores_to_int(scores)
	# visited = set()
	teams = set()
	#Graph is ready
	teams_score = 0
	sets_of_teams = dict()
  	o_vertices = vertices.copy()
  	o_edges = edges.copy()
	for start in o_vertices:
		# print "Start Vertice: ", start
		visited = set()
		# teams = set()
		edges = o_edges.copy()
		vertices = o_vertices.copy()
		# teams_score = 0
		while(len(vertices)>0):
	  		#Step I: Choose a random starting vertex
	  		# start  = random.sample(vertices,1)[0]
	  		if(start in visited):
	  			start = None
	  			for v in vertices:
	  				if (v not in visited):
	  					v = start
	  			if(start == None):
	  				break
	  		paths = construct_all_possible_paths(start, vertices, edges)
	  		best_path, best_score = choose_path_with_max_score(paths,scores)
	  		flag = True
	  		for x in best_path:
	  			for y in teams:
	  				# print "X: ", x, " Y: ", y, " X in Y: ", x in y
	  				if(x in y):
	  					flag = False
	  		if(flag == True):	
	  			teams.add(best_path)
	  			teams_score += best_score
	  		visited = mark_as_visited(best_path,visited) # add all elements of best path
	  		vertices, edges = update_graph(vertices,edges,visited)
	  		# print "Path added: ", best_path
	  		# # print "Score added: ", best_score
	  		# print "Length of vertices: ", len(vertices)
	  		# print "Visited: ", visited
	  		# print "Does 0 exist in visited:", 0 in visited
	  		# print "Updated vertices: ", vertices
	  		# print "TEAM: ",teams ,"TEAM SCORE: ", teams_score
	  		if(tuple(teams) not in sets_of_teams.keys() or teams_score > sets_of_teams[tuple(teams)]):
	  			sets_of_teams[tuple(teams)] = teams_score 	#Contains the best team of each instance. 
	  										#Two instances are different if they have a different start vertex.
	  										#We need to choose the team with the instance with the highest score here
	# print "ALL TEAMS: ", sets_of_teams  								
	# print "BEST TEAM: ", best_team(sets_of_teams)[0], " SCORE: ", best_team(sets_of_teams)[1]			
	return best_team(sets_of_teams)[0]
