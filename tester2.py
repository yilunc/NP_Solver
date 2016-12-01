# void printPathsRecur(Node node, int path[], int pathLen) 
#     {
#         if (node == null)
#             return;
  
#         /* append this node to the path array */
#         path[pathLen] = node.data;
#         pathLen++;
  
#         /* it's a leaf, so print the path that led to here  */
#         if (node.left == null && node.right == null)
#             printArray(path, pathLen);
#         else
#         {
#             /* otherwise try both subtrees */
#             printPathsRecur(node.left, path, pathLen);
#             printPathsRecur(node.right, path, pathLen);
#         }
#     }

# def path_creator(current, vertices, edges, path):
#     path.append(current)
#     children = [e[1] if e[0]==current else '' for e in edges]
#     if(len(children) == 0 ):
#         temp_paths.append(path)
#         return path
#     else:
#         for child in children:
#             path_creator(child, vertices, edges, path)

# def construct_all_possible_paths(start, vertices, edges):
#     """
#     A function that constructs ALL possible paths and returns them.
#     INPUT   start - the start vertice for out path building
#             vertices - a set of all the vertices in the graph
#             edges -  a set of all the valid edges in the graph
#     OUTPUT A set of all possible paths
#     >>> v = set([1,2,3,4])
#     >>> e = set([(1,2),(1,3),(2,4)])
#     >>> s = 1
#     >>> construct_all_possible_paths(s, v, e)

#     """
#     # raiseNotDefined()
#     global temp_paths
#     temp_paths = list()
#     print path_creator(start,vertices,edges,[])
#     print temp_paths
    
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


#### Don't modify below this line ####
# v = set([1,2,3,4])
# e = set([(1,2),(1,3),(2,4)])
# s = 1
# construct_all_possible_paths(s, v, e)


if __name__ == "__main__":
    import doctest
    doctest.testmod()