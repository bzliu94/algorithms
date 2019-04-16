# 2019-04-15

# algorithm AD version one from fraczak et al. 2013

# input: V, A, s

# the implementation is not efficient; the aim is to have correctness to begin with

# for this pseudocode, we do not have explicit subroutine transform, 
# but we do have explicit contraction

# reverse RPO is required (as opposed to standard reverse pre-order)

# we don't use doubly-linked lists yet and use lists with expensive non-destructive concatenation

# assume input graph is acyclic and directed; 
# all nodes are reachable from node s

from fgib_tarjan import Vertex, Edge, Tree, TreeVertex, TreeEdge, Graph
# from bundle_one.list.DoublyLinkedList import DoublyLinkedList
# from bundle_one.list.DoublyLinkedListNode import DoublyLinkedListNode
# from dsuf import NamedUnionFind
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

def AD(V, A, g_start_node):

  g = Graph()
  g.addVertices(V)
  g.addEdges(A)

  visited = {}
  pre = {}
  post = {}
  AD.clock = 1
  p = {}
  total = {}
  arcs = defaultdict(lambda: [])

  same = {}
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
    pre[v] = AD.clock
    AD.clock += 1

  def postvisit(v):
    post[v] = AD.clock
    AD.clock += 1

  dfs()

  for edge in A:
    origin = edge.getOrigin()
    destination = edge.getDestination()
    o_pre = pre[origin]
    o_post = post[origin]
    d_pre = pre[destination]
    d_post = post[destination]
    if origin == p[destination]:
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
  # t._setPreorderNumbers()
  t._setRPOPreorderNumbers()
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
      elif u_to_v_star == False and v_to_u_star == False and oipn_u < oipn_v:
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
    same[u] = [u]

  t_num_to_g_node = {}
  for tree_vertex in tree_vertices:
    g_node = g.getVertexByName(tree_vertex.getName())
    t_num = tree_vertex.getPreorderNumber()
    t_num_to_g_node[t_num] = g_node

  # since we have transitory tree edges, we make a copy 
  # so that we still have access to original tree edges
  next_A = A[ : ]

  marked = defaultdict(lambda: False)
  old_marked = defaultdict(lambda: False)

  for u_num in reversed(xrange(1, num_nodes + 1)):
    u = t_num_to_g_node[u_num]
    candidate_arcs = [x for x in next_A if (x.isTreeEdge() == True or x.isForwardEdge() == True) and x.getOrigin() == u and marked[x] == False]
    while len(candidate_arcs) != 0:
      arc = candidate_arcs.pop()
      if marked[arc] == True:
        continue
      v = arc.getDestination()
      marked[arc] = True
      if len([x for x in next_A if x.getDestination() == v and marked[x] == False]) == 0:
        if u == p[v]:
          for w in same[v]:
            d[w] = u
        else:
          same[p[v]] = same[p[v]] + same[v]
        # contract v into p(v)
        # updating parent function is possibly optional for the way we implement AD one
        for curr_child, curr_parent in p.items():
          if curr_parent == v:
            p[curr_child] = p[v]
        arcs_with_v_as_origin = [x for x in next_A if x.getOrigin() == v and x.getOrigin() != x.getDestination()]
        arcs_with_v_as_destination = [x for x in next_A if x.getDestination() == v and x.getOrigin() != x.getDestination()]
        for arc_to_remove in arcs_with_v_as_origin + arcs_with_v_as_destination:
          # there is interaction between marking logic here and when we create new edges below
          old_marked[arc_to_remove] = marked[arc_to_remove]
          marked[arc_to_remove] = True
          # if a node is removed, so are edges associated with it
          if arc_to_remove in next_A:
            next_A.remove(arc_to_remove)
        modified_arcs1 = []
        modified_arcs2 = []
        for curr_arc in arcs_with_v_as_origin:
          next_arc = Edge(p[v], curr_arc.getDestination())
          if next_arc.getOrigin() != next_arc.getDestination():
            # technically, we are allowed to be sloppy and not distinguish between tree and forward edge
            if p[v] == p[curr_arc.getDestination()]:
              next_arc.setIsTreeEdge()
            else:
              next_arc.setIsForwardEdge()
            if old_marked[curr_arc] == True:
              marked[next_arc] = True
            modified_arcs1.append(next_arc)
        for curr_arc in arcs_with_v_as_destination:
          next_arc = Edge(curr_arc.getOrigin(), p[v])
          if next_arc.getOrigin() != next_arc.getDestination():
            # technically, we are allowed to be sloppy and not distinguish between tree and forward edge
            if curr_arc.getOrigin() == p[p[v]]:
              next_arc.setIsTreeEdge()
            else:
              next_arc.setIsForwardEdge()
            if old_marked[curr_arc] == True:
              marked[next_arc] = True
            modified_arcs2.append(next_arc)
        candidate_arcs.extend([x for x in modified_arcs1 if x.getOrigin() == u and marked[x] == False])
        candidate_arcs.extend([x for x in modified_arcs2 if x.getOrigin() == u and marked[x] == False])
        # may not be necessary
        next_A.extend(modified_arcs1)
        next_A.extend(modified_arcs2)

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


