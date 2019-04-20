# 2019-04-16

# algorithm GD version two from fraczak et al. 2013

# input: V, A, s

# values: 
# visited(u) -- boolean
# p(v) -- node
# total(v) -- integer
# added(v) -- integer
# arcs(v) -- arc standard list
# same(u) -- node doubly-linked list (i.e. technically a set)
# uf -- standard DSU
# in(u) -- node doubly-linked list
# out(u) -- node doubly-linked list
# d(w) -- node

# this implementation is slightly optimized

# time is O(|E| * alpha(|V|, |E|))

# for this pseudocode, we do not have explicit subroutines transform, 
# but we do have explicit contraction

# reverse RPO is not required (as opposed to standard reverse pre-order)

# we do use doubly-linked lists and use lists with destructive concatenation

# assume input graph is not acyclic and that is directed; 
# all nodes are reachable from node s

from fgib_tarjan import Vertex, Edge, Tree, TreeVertex, TreeEdge, Graph
from bundle_one.list.DoublyLinkedList import DoublyLinkedList
from bundle_one.list.DoublyLinkedListNode import DoublyLinkedListNode
from dsuf import NamedUnionFind
from collections import defaultdict
from lca_bfc import LCA_BFC

def doStar(t_v, t_w):
  nd_v = t_v.getNumberOfDescendants()
  oipn_v = t_v.getPreorderNumber()
  oipn_w = t_w.getPreorderNumber()
  result = oipn_v <= oipn_w and oipn_w < oipn_v + nd_v
  return result

TREE_EDGE = 0
CYCLE_EDGE = 1
CROSS_EDGE = 2
FORWARD_EDGE = 3

def GD(V, A, g_start_node):

  g = Graph()
  g.addVertices(V)
  g.addEdges(A)

  visited = {}
  pre = {}
  post = {}
  GD.clock = 1
  p = {}

  total = {}
  added = {}
  # sometimes an arc list is empty and this helps prepares for that
  arcs = defaultdict(lambda: [])
  same = {}
  uf = NamedUnionFind()
  in_bag = {}
  out_bag = {}
  d = {}

  origin_to_arc_dict = defaultdict(lambda: [])
  destination_to_arc_dict = defaultdict(lambda: [])
  for edge in A:
    origin = edge.getOrigin()
    destination = edge.getDestination()
    origin_to_arc_dict[origin].append(edge)
    destination_to_arc_dict[destination].append(edge)

  def explore(v):
    visited[v] = True
    previsit(v)
    for edge in origin_to_arc_dict[v]:
      u = edge.getDestination()
      if visited[u] == False:
        p[u] = v
        explore(u)
    postvisit(v)

  # we assume all nodes are reachable from node s
  def dfs():
    for v in V:
      visited[v] = False
    explore(g_start_node)

  def previsit(v):
    pre[v] = GD.clock
    GD.clock += 1

  def postvisit(v):
    post[v] = GD.clock
    GD.clock += 1

  dfs()

  for edge in A:
    origin = edge.getOrigin()
    destination = edge.getDestination()
    o_pre = pre[origin]
    o_post = post[origin]
    d_pre = pre[destination]
    d_post = post[destination]
    if destination == g_start_node:
      continue
    elif origin == p[destination]:
      edge.setIsTreeEdge()

  t = Tree()
  tree_vertices = [TreeVertex(x.getName()) for x in V]
  name_to_tree_vertex_dict = {}
  for tree_vertex in tree_vertices:
    name = tree_vertex.getName()
    name_to_tree_vertex_dict[name] = tree_vertex
    t.addVertex(tree_vertex)
  t.setRoot(name_to_tree_vertex_dict[g_start_node.getName()])
  for edge in A:
    g_origin, g_destination = edge.getOrigin(), edge.getDestination()
    origin_name, destination_name = g_origin.getName(), g_destination.getName()
    t_origin, t_destination = name_to_tree_vertex_dict[origin_name], name_to_tree_vertex_dict[destination_name]
    if edge.isTreeEdge() == True:
      t_destination.setParent(t_origin)
      tree_edge = TreeEdge(t_origin, t_destination)
      t.addEdge(tree_edge)
      t_origin.addChild(t_destination)
  t._setPreorderNumbers()
  # t._setRPOPreorderNumbers()
  t._setNumberOfDescendants()

  # using graph pre-order/post-order is inappropriate for classifying of edges; 
  # using dfs tree pre-order and post-order is the correct way; 
  # note that we use graph edges as opposed to tree edges at this point
  for edge in A:
    if edge.isTreeEdge() == False:
      g_u, g_v = edge.getOrigin(), edge.getDestination()
      t_u = t.getVertexByName(g_u.getName())
      t_v = t.getVertexByName(g_v.getName())
      oipn_u = t_u.getPreorderNumber()
      oipn_v = t_v.getPreorderNumber()
      u_to_v_star = doStar(t_u, t_v)
      v_to_u_star = doStar(t_v, t_u)
      if v_to_u_star == True:
        # edge is a cycle edge
        edge.setIsCycleEdge()
      elif u_to_v_star == True:
        # edge is a forward edge
        edge.setIsForwardEdge()
      elif u_to_v_star == False and v_to_u_star == False:
        # edge is a cross edge
        edge.setIsCrossEdge()
      else:
        raise Exception()

  num_nodes = len(V)
  # for LCA structure based on DFS tree
  adj = defaultdict(lambda: [])
  for tree_vertex in tree_vertices:
    curr_zipn = tree_vertex.getZeroIndexedPreorderNumber()
    children = tree_vertex.getChildren()
    child_zipn_values = [x.getZeroIndexedPreorderNumber() for x in children]
    for child_zipn_value in child_zipn_values:
      adj[curr_zipn].append(child_zipn_value)
      adj[child_zipn_value].append(curr_zipn)

  # LCA is based on tree edge zero-indexed pre-order numbers
  lca_bfc = LCA_BFC(num_nodes, adj)
  t_start_node = t.getVertexByName(g_start_node.getName())
  root_zipn = t_start_node.getZeroIndexedPreorderNumber()
  lca_bfc.precompute_lca(root_zipn)

  # partition graph edges based on one-indexed LCA
  lca_to_g_edges_dict = defaultdict(lambda: [])
  for g_edge in A:
    g_origin, g_destination = g_edge.getOrigin(), g_edge.getDestination()
    origin_name, destination_name = g_origin.getName(), g_destination.getName()
    t_origin = t.getVertexByName(origin_name)
    t_destination = t.getVertexByName(destination_name)
    origin_zipn = t_origin.getZeroIndexedPreorderNumber()
    destination_zipn = t_destination.getZeroIndexedPreorderNumber()
    curr_lca = lca_bfc.lca(origin_zipn, destination_zipn)
    curr_lca_oipn = curr_lca + 1
    lca_to_g_edges_dict[curr_lca_oipn].append(g_edge)

  oipn_to_g_node_dict = {}

  for tree_vertex in tree_vertices:
    oipn = tree_vertex.getPreorderNumber()
    g_node = g.getVertexByName(tree_vertex.getName())
    oipn_to_g_node_dict[oipn] = g_node

  for curr_oipn, curr_arcs in lca_to_g_edges_dict.items():
    curr_g_node = oipn_to_g_node_dict[curr_oipn]
    arcs[curr_g_node] = curr_arcs

  # note that we want numbering from bottom up; 
  # this is not what pre-order numbering does; 
  # as a result, we go from high pre-order 
  # to low pre-order for main loop

  for u in V:
    # number of arcs into node u
    total[u] = len(destination_to_arc_dict[u])

  t_num_to_g_node = {}
  for tree_vertex in tree_vertices:
    g_node = g.getVertexByName(tree_vertex.getName())
    t_num = tree_vertex.getPreorderNumber()
    t_num_to_g_node[t_num] = g_node

  for u_num in reversed(xrange(1, num_nodes + 1)):
    u = t_num_to_g_node[u_num]
    out_bag[u] = DoublyLinkedList()
    in_bag[u] = DoublyLinkedList()
    uf.insert_objects([u])
    added[u] = 0
    curr_dll = DoublyLinkedList()
    curr_dll_node = DoublyLinkedListNode(u, None, None)
    curr_dll.addLast(curr_dll_node)
    same[u] = curr_dll
    for edge in arcs[u]:
      x = edge.getOrigin()
      y = edge.getDestination()
      y_dll_node = DoublyLinkedListNode(y, None, None)
      x_dll_node = DoublyLinkedListNode(x, None, None)
      out_bag[uf.find(x)].addLast(y_dll_node)
      in_bag[uf.find(y)].addLast(x_dll_node)
      added[uf.find(y)] += 1
    while out_bag[u].isEmpty() == False:
      y_dll_node = out_bag[u].getFirst()
      out_bag[u].remove(y_dll_node)
      y = y_dll_node.getElement()
      v = uf.find(y)
      if v != u:
        total[v] -= 1
        added[v] -= 1
        if total[v] == 0:
          x = uf.find(p[v])
          if u == x:
            for w in same[v].toElementList():
              d[w] = u
          else:
            same[x] = DoublyLinkedList.concatenate(same[x], same[v])
          uf.union(p[v], v)
          out_bag[x] = DoublyLinkedList.concatenate(out_bag[x], out_bag[v])
    while in_bag[u].isEmpty() == False:
      z_dll_node = in_bag[u].getFirst()
      in_bag[u].remove(z_dll_node)
      z = z_dll_node.getElement()
      v = uf.find(z)
      while v != u:
        same[u] = DoublyLinkedList.concatenate(same[u], same[v])
        x = uf.find(p[v])
        uf.union(p[v], v)
        in_bag[x] = DoublyLinkedList.concatenate(in_bag[x], in_bag[v])
        out_bag[x] = DoublyLinkedList.concatenate(out_bag[x], out_bag[v])
        total[x] += total[v]
        added[x] += added[v]
        v = x
    total[u] -= added[u]
    added[u] = 0

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


