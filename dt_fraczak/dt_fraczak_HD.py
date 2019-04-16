# 2019-04-15

# algorithm HD from fraczak et al. 2013

# input: V, A, s

# values: 
# visited(u) -- boolean
# p(v) -- node
# total(v) -- integer
# out(u) -- node doubly-linked list
# in-arcs(u) -- arc doubly-linked list
# same(u) -- node doubly-linked list (i.e. technically a set)
# d(w) -- node
# revpre -- node doubly-linked list
# H -- graph that cares about edge groups based on origin and destination
# exit_arc(v) -- arc

# for this pseudocode, we do not have explicit subroutines transform or contraction

# this is using lists with expensive non-destructive concatenation

# we can in the future use link-style unions

# loop nesting forest is unique to DFS tree, but not to input graph

# assume input graph is directed; 
# all nodes are reachable from node s

from fgib_tarjan import Graph, Vertex, Edge
# from bundle_one.list.DoublyLinkedList import DoublyLinkedList
# from bundle_one.list.DoublyLinkedListNode import DoublyLinkedListNode
from dsuf import NamedUnionFind
from collections import defaultdict

def HD(V, A, s):

  visited = {}
  p = {}
  total = {}
  out_bag = {}
  in_arcs = {}
  same = {}
  d = {}
  uf = NamedUnionFind()
  revpre = []
  H = Graph()
  exit_arc = {}

  origin_to_arc_dict = defaultdict(lambda: [])
  destination_to_arc_dict = defaultdict(lambda: [])
  for edge in A:
    origin = edge.getOrigin()
    destination = edge.getDestination()
    origin_to_arc_dict[origin].append(edge)
    destination_to_arc_dict[destination].append(edge)

  # we know root is node s
  for u in V:
    visited[u] = False
    total[u] = len(destination_to_arc_dict[u])

  def dfs(u):
    previsit(u)
    for edge in origin_to_arc_dict[u]:
      u = edge.getOrigin()
      v = edge.getDestination()
      if visited[v] == False:
        dfs(v)
        p[v] = u
      in_arcs[uf.find(v)].append(edge)
    postvisit(u)

  def previsit(u):
    visited[u] = True
    in_arcs[u] = []
    uf.insert_objects([u])
    revpre.insert(0, u)

  def postvisit(u):
    while len(in_arcs[u]) != 0:
      curr_arc = in_arcs[u].pop(0)
      z = curr_arc.getOrigin()
      y = curr_arc.getDestination()
      total[u] -= 1
      v = uf.find(z)
      while v != u:
        next_arc = Edge(u, v)
        H.addEdge(next_arc)
        exit_arc[v] = curr_arc
        x = uf.find(p[v])
        uf.union(p[v], v)
        in_arcs[x] = in_arcs[x] + in_arcs[v]
        total[u] += total[v]
        v = x

  dfs(s)

  """

  # this is to show that we can recreate a specific loop nesting forest if we fix the tree edges created via DFS

  print [x.toString() for x in V]
  print [x.toString() for x in A]
  v_a, v_b, v_c, v_d, v_e, v_f, v_g, v_s = V
  ordered_nodes = [v_b, v_c, v_f, v_d, v_a, v_e, v_g]

  p[v_b] = v_s
  p[v_c] = v_b
  p[v_f] = v_b
  p[v_d] = v_c
  p[v_a] = v_c
  p[v_e] = v_a
  p[v_g] = v_e

  e_sa, e_sb, e_sd, e_ae, e_bc, e_bf, e_ca, e_cd, e_db, e_eg, e_fc, e_fd, e_fg, e_ga, e_gd = A

  # visit s
  previsit(v_s)
  # visit b
  previsit(v_b)
  # visit c
  previsit(v_c)
  # visit d
  previsit(v_d)
  in_arcs[uf.find(v_b)].append(e_db)
  postvisit(v_d)
  in_arcs[uf.find(v_d)].append(e_cd)
  # visit a
  previsit(v_a)
  # visit e
  previsit(v_e)
  # visit g
  previsit(v_g)
  in_arcs[uf.find(v_a)].append(e_ga)
  in_arcs[uf.find(v_d)].append(e_gd)
  postvisit(v_g)
  in_arcs[uf.find(v_g)].append(e_eg)
  postvisit(v_e)
  in_arcs[uf.find(v_e)].append(e_ae)
  postvisit(v_a)
  in_arcs[uf.find(v_a)].append(e_ca)
  postvisit(v_c)
  in_arcs[uf.find(v_c)].append(e_bc)
  # visit f
  previsit(v_f)
  in_arcs[uf.find(v_c)].append(e_fc)
  in_arcs[uf.find(v_d)].append(e_fd)
  in_arcs[uf.find(v_g)].append(e_fg)
  postvisit(v_f)
  in_arcs[uf.find(v_f)].append(e_bf)
  postvisit(v_b)
  in_arcs[uf.find(v_a)].append(e_sa)
  in_arcs[uf.find(v_b)].append(e_sb)
  in_arcs[uf.find(v_d)].append(e_sd)
  postvisit(v_s)

  """

  # it is important to re-initialize disjoint set
  uf = NamedUnionFind()
  for u in V:
    uf.insert_objects([u])
    # we pull out bag and same set out; 
    # there is precedent as with DSU re-initialization; 
    # this is in contrast to e.g. GD version three
    out_bag[u] = []
    # this can either be pulled out (as it is) 
    # or technically can go inside revpre loop 
    # for some reason
    same[u] = [u]
  for u in revpre:
    curr_A_edges = destination_to_arc_dict[u]
    for edge in curr_A_edges:
      x = edge.getOrigin()
      out_bag[uf.find(x)].append(u)
    while len(out_bag[u]) != 0:
      y = out_bag[u].pop()
      v = uf.find(y)
      if v != u:
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
    curr_H_edges = H.getEdgesOriginatingAt(u)
    for edge in curr_H_edges:
      z = edge.getDestination()
      v = uf.find(z)
      if v != u:
        same[u] = same[u] + same[v]
        x = uf.find(p[v])
        uf.union(p[v], v)
        out_bag[x] = out_bag[x] + out_bag[v]

  return d, H, exit_arc

if __name__ == '__main__':

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

  result = HD(vertices, edges, v8)

  d, H, exit_arc = result

  for d_item in d.items():
    curr_node, curr_parent = d_item
    print curr_node.getName(), curr_parent.getName()

  for edge in H.getEdges():
    print edge.toString()

  # we assume exits are correct
  for node, edge in exit_arc.items():
    print "exit for node", node.getName(), "is edge", edge.toString()


