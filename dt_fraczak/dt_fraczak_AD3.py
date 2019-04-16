# 2019-04-15

# algorithm AD version three from fraczak et al. 2013

# input: V, A, s

# the implementation is not efficient; the aim is to have correctness to begin with

# for this pseudocode, we do not have explicit subroutines transform, 
# but we do have explicit contraction

# reverse RPO is not required (as opposed to standard reverse pre-order)

# we don't use doubly-linked lists yet and use lists with expensive non-destructive concatenation

# assume input graph is acyclic and directed; 
# all nodes are reachable from node s

from fgib_tarjan import Vertex, Edge, Tree, TreeVertex, TreeEdge, Graph
# from bundle_one.list.DoublyLinkedList import DoublyLinkedList
# from bundle_one.list.DoublyLinkedListNode import DoublyLinkedListNode
from dsuf import NamedUnionFind
from collections import defaultdict
# from lca_bfc import LCA_BFC

def AD(V, A, g_start_node):

  visited = {}
  p = {}

  total = {}
  arcs = defaultdict(lambda: [])
  same = {}
  uf = NamedUnionFind()
  out_bag = {}
  d = {}

  num_nodes = len(V)

  origin_to_arc_dict = defaultdict(lambda: [])
  destination_to_arc_dict = defaultdict(lambda: [])
  for edge in A:
    origin = edge.getOrigin()
    destination = edge.getDestination()
    origin_to_arc_dict[origin].append(edge)
    destination_to_arc_dict[destination].append(edge)

  # note that we want numbering from bottom up; 
  # this is not what pre-order numbering does; 
  # as a result, we go from high pre-order 
  # to low pre-order for main loop

  for u in V:
    # number of arcs into node u
    uf.insert_objects([u])
    # this line must be here, but was not present here in even corrected version of algorithm AD version three
    out_bag[u] = []

  t_num_to_g_node = {}
  for tree_vertex in tree_vertices:
    g_node = g.getVertexByName(tree_vertex.getName())
    t_num = tree_vertex.getPreorderNumber()
    t_num_to_g_node[t_num] = g_node

  for u_num in reversed(xrange(1, num_nodes + 1)):
    u = t_num_to_g_node[u_num]
    total[u] = 0
    same[u] = [u]
    for edge in destination_to_arc_dict[u]:
      total[u] += 1
      x = edge.getOrigin()
      out_bag[uf.find(x)].append(u)
    while len(out_bag[u]) != 0:
      v = out_bag[u].pop()
      total[v] -= 1
      if total[v] == 0:
        x = uf.find(p[v])
        if u == x:
          for w in same[v]:
            d[w] = u
        else:
          same[x] = same[x] + same[v]
        uf.union(p[v], v)
        out_bag[x] = out_bag[x] + out_bag[v]

  return d

if __name__ == '__main__':

  # example is from page eight from fraczak et al. 2013

  v1 = Vertex("a")
  v2 = Vertex("b")
  v3 = Vertex("c")
  v4 = Vertex("d")
  v5 = Vertex("e")
  v6 = Vertex("f")
  v7 = Vertex("g")
  v8 = Vertex("s")

  vertices = [v1, v2, v3, v4, v5, v6, v7, v8]

  e1 = Edge(v8, v1)
  e2 = Edge(v8, v2)
  e3 = Edge(v1, v5)
  e4 = Edge(v2, v3)
  e5 = Edge(v2, v6)
  e6 = Edge(v3, v1)
  e7 = Edge(v3, v4)
  e8 = Edge(v3, v5)
  e9 = Edge(v5, v7)
  e10 = Edge(v6, v4)
  e11 = Edge(v6, v7)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11]

  # answer is:
  # (f, b), (c, b), (d, b), (g, s), (e, s), (a, s)

  result = AD(vertices, edges, v8)

  d = result

  for d_item in d.items():
    curr_node, curr_parent = d_item
    print curr_node.getName(), curr_parent.getName()


