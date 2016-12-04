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
		# print "The path: ", type(path)
		path_score = 0
		for h in path:
			path_score += scores[h]
		paths_to_scores[path] = path_score

	max_path = None
	max_score = 0
	for el in paths_to_scores.keys():
		if(paths_to_scores[el] > max_score):
			max_score = paths_to_scores[el]
			max_path = el

	return max_path


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

#### Don't modify below this line ####

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# paths = [(1,2),(3,)]
# scores = {1 : 10, 2: 10, 3: 10}
# print choose_path_with_max_score(paths, scores)
