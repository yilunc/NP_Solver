import sys
import random

def generate_instance(num_instances, V=500):
  if V > 500 or V <= 0:
    raise IndexError('To many vertices')

  for instance_num in range(1, num_instances + 1):
    vertices = []
    adjacency = {}

    for i in range(V):
      vertices.append((i, random.randint(0, 99)))

    for v, p in vertices:
      adjacency[v] = [u[0] for u in random.sample(vertices, random.randint(0, V)) if u != v]

    with open('{0}.in'.format(instance_num), 'wb') as f:
      f.write("{0}\n".format(V))
      for i in range(1, len(vertices) + 1):
        for j in range(1, i):
          if j in adjacency[i - 1]:
            f.write("1 ")
          else:
            f.write("0 ")
        f.write("{0} ".format(vertices[i - 1][1]))
        for j in range(i + 1, V + 1):
          if j in adjacency[i - 1]:
            f.write("1 ")
          else:
            f.write("0 ")
        f.write('\n')

if (len(sys.argv) == 3):
    generate_instance(int(sys.argv[1]), int(sys.argv[2]))
elif (len(sys.argv) == 2):
    generate_instance(int(sys.argv[1]))
else:
  print("ERROR: invalid argument(s).")
