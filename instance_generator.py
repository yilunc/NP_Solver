import random

def generate_instance(V=500):
  if V > 500 or V <= 0:
    raise IndexError

  vertices = []
  adjacency = {}

  for i in range(V):
    vertices.append((i, random.randint(0, 99)))

  for v, p in vertices:
    adjacency[v] = [u[0] for u in random.sample(vertices, random.randint(0, V)) if u != v]

  for i in range(1, len(vertices) + 1):
    for j in range(1, i):
      if j in adjacency[i - 1]:
        print 1,
      else:
        print 0,
    print vertices[i - 1][1],
    for j in range(i + 1, V + 1):
      if j in adjacency[i - 1]:
        print 1,
      else:
        print 0,
    print ''

