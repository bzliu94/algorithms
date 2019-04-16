# 2019-04-15

# algorithm GD version three from fraczak et al. 2013

# input: V, A, s

# the implementation is not efficient; the aim is to have correctness to begin with

# for this pseudocode, we do not have explicit subroutines transform, 
# but we do have explicit contraction

# reverse RPO is not required (as opposed to standard reverse pre-order)

# we don't use doubly-linked lists yet and use lists with expensive non-destructive concatenation

# assume input graph is not acyclic and that is directed; 
# all nodes are reachable from node s

from fgib_tarjan import Vertex, Edge, Tree, TreeVertex, TreeEdge, Graph
# from bundle_one.list.DoublyLinkedList import DoublyLinkedList
# from bundle_one.list.DoublyLinkedListNode import DoublyLinkedListNode
from dsuf import NamedUnionFind
from collections import defaultdict
# from lca_bfc import LCA_BFC

def GD(V, A, g_start_node):

  visited = {}
  p = {}

  total = {}
  added = {}
  arcs = defaultdict(lambda: [])
  same = {}
  uf = NamedUnionFind()
  uf_nca = NamedUnionFind()
  in_bag = {}
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

  for u in V:
    visited[u] = False
    # number of arcs into node u
    total[u] = len(destination_to_arc_dict[u])

  # we assume all nodes are reachable from node s
  def dfs(u):
    previsit(u)
    for edge in origin_to_arc_dict[u]:
      v = edge.getDestination()
      if visited[v] == False:
        dfs(v)
        p[v] = u
        uf_nca.union(p[v], v)
      arcs[uf_nca.find(v)].append(edge)
    postvisit(u)

  def previsit(u):
    visited[u] = True
    arcs[u] = []
    uf_nca.insert_objects([u])

  def postvisit(u):
    out_bag[u] = []
    in_bag[u] = []
    uf.insert_objects([u])
    added[u] = 0
    same[u] = [u]
    for edge in arcs[u]:
      x = edge.getOrigin()
      y = edge.getDestination()
      out_bag[uf.find(x)].append(y)
      in_bag[uf.find(y)].append(x)
      added[uf.find(y)] += 1
    while len(out_bag[u]) != 0:
      y = out_bag[u].pop()
      v = uf.find(y)
      if v != u:
        total[v] -= 1
        added[v] -= 1
        if total[v] == 0:
          x = uf.find(p[v])
          if u == x:
            for w in same[v]:
              d[w] = u
          else:
            same[x] = same[x] + same[v]
          uf.union(p[v], v)
          out_bag[x] = out_bag[x] + out_bag[v]
    while len(in_bag[u]) != 0:
      z = in_bag[u].pop()
      v = uf.find(z)
      while v != u:
        same[u] = same[u] + same[v]
        x = uf.find(p[v])
        uf.union(p[v], v)
        in_bag[x] = in_bag[x] + in_bag[v]
        out_bag[x] = out_bag[x] + out_bag[v]
        total[x] += total[v]
        added[x] += added[v]
        v = x
    total[u] -= added[u]
    added[u] = 0

  dfs(g_start_node)

  return d

if __name__ == '__main__':

  """

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

  """

  # example is from page two from fraczak et al. 2013

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
  e3 = Edge(v8, v4)
  e4 = Edge(v1, v5)
  e5 = Edge(v2, v3)
  e6 = Edge(v2, v6)
  e7 = Edge(v3, v1)
  e8 = Edge(v3, v4)
  e9 = Edge(v4, v2)
  e10 = Edge(v5, v7)
  e11 = Edge(v6, v3)
  e12 = Edge(v6, v4)
  e13 = Edge(v6, v7)
  e14 = Edge(v7, v1)
  e15 = Edge(v7, v4)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]

  # answer is:
  # (f, b), (c, b), (e, a), (b, s), (d, s), (g, s), (a, s)

  result = GD(vertices, edges, v8)

  d = result

  for d_item in d.items():
    curr_node, curr_parent = d_item
    print curr_node.getName(), curr_parent.getName()


