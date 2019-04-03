# 2019-03-29

# standard DSU structure is ready to be swapped out 
# for gabow-tarjan 1985 off-line DSU; we have ready 
# link-style union operations; however, the way we handle 
# link-style unions is we assume root of set in DFS tree 
# is automatically made the name of the set as is the case 
# with gabow-tarjan approach; we do this explicitly 
# with standard-style union operations; this means 
# using the former style with standard DSU structure 
# may lead to incorrect behavior unless we use 
# explicit renaming of sets

# 2019-03-28

# BRIDGES requires RPO, which is special case of pre-order

# RPO is used to guarantee that for cross edges (v, w), we always have v < w

# RPO is not required (i.e. as long as we use regular pre-order) 
# for INTERVALS, but it is for BRIDGES (for non-tree edge step)

# because we want to in principle always consider cross edges 
# if they end at correct node, we choose a numbering scheme 
# where it's easy to measure goodness of a cross edge

# 2019-03-22

# we implement tarjan 1976 INTERVALS and BRIDGES algorithms for flow-graphs

# time for each of the two algorithms is O(|E| * alpha(|V|, |E|))

# input is directed graph via classes Graph, Vertex, Edge

# Graph, Vertex, Edge, addDummyNode, prepareGraph, doIntervals, doBridges are public

# classes Tree, TreeVertex, TreeEdge are internal and for DFS tree 
# (except in sense that when we prepare graph, 
# we get a tree and adjacency matrix generated 
# that we then pass to intervals and bridges algorithms)

# class Clock is internal, as well

# transform graph to have a new start vertex for flow-graph

# we assume graph is strongly connected before choosing an arbitrary node as start vertex for flow-graph

# get DFS tree for flow-graph for purpose of determining pre-order numbers

# we do not need reverse post-order for DFS tree, 
# despite what tarjan says about cross edges (v, w) and 
# needing to have for that case v < w 
# (assuming node values are pre-order numbers)

from collections import defaultdict

from dsuf import NamedUnionFind

from lca_bfc import LCA_BFC

class Graph:
  def __init__(self):
    self.name_to_vertex = {}
    self.origin_to_edges = defaultdict(lambda: [])
    self.destination_to_edges = defaultdict(lambda: [])
    self.vertices = []
    self.edges = []
  def addEdge(self, edge):
    self.edges.append(edge)
    origin = edge.getOrigin()
    destination = edge.getDestination()
    self.origin_to_edges[origin].append(edge)
    self.destination_to_edges[destination].append(edge)
  def addVertex(self, vertex):
    self.vertices.append(vertex)
    name = vertex.getName()
    self.name_to_vertex[name] = vertex
  def addEdges(self, edges):
    for edge in edges:
      self.addEdge(edge)
  def addVertices(self, vertices):
    for vertex in vertices:
      self.addVertex(vertex)
  def getVertices(self):
    return self.vertices
  def getEdges(self):
    return self.edges
  def getEdgesOriginatingAt(self, node):
    return self.origin_to_edges[node]
  def getEdgesEndingAt(self, node):
    return self.destination_to_edges[node]
  # sort according to alphabetical order
  def _sortOriginToEdgesLists(self, do_reverse = False):
    keys = self.origin_to_edges.keys()
    for key in keys:
      self.origin_to_edges[key].sort(reverse = do_reverse)
  # we assume each node has a unique name
  def getVertexByName(self, name):
    return self.name_to_vertex[name]

TREE_EDGE = 0
CYCLE_EDGE = 1
CROSS_EDGE = 2
FORWARD_EDGE = 3

class Edge:
  def __init__(self, origin, destination):
    self.origin = origin
    self.destination = destination
    self.type = None
    self.is_active = None
  def getOrigin(self):
    return self.origin
  def getDestination(self):
    return self.destination
  def isTreeEdge(self):
    return self.type == TREE_EDGE
  def isCycleEdge(self):
    return self.type == CYCLE_EDGE
  def isCrossEdge(self):
    return self.type == CROSS_EDGE
  def isForwardEdge(self):
    return self.type == FORWARD_EDGE
  def setIsTreeEdge(self):
    self.type = TREE_EDGE
  def setIsCycleEdge(self):
    self.type = CYCLE_EDGE
  def setIsCrossEdge(self):
    self.type = CROSS_EDGE
  def setIsForwardEdge(self):
    self.type = FORWARD_EDGE
  def isActive(self):
    return self.is_active
  def setIsActive(self):
    self.is_active = True
  def setIsInactive(self):
    self.is_active = False
  def getEdgeTypeString(self):
    if self.isTreeEdge() == True:
      return "tree"
    elif self.isCycleEdge() == True:
      return "cycle"
    elif self.isCrossEdge() == True:
      return "cross"
    elif self.isForwardEdge() == True:
      return "forward"
  def toString(self):
    return "(" + self.getOrigin().toString() + ", " + self.getDestination().toString() + ")"
  def toOIPNString(self, t):
    g_origin = self.getOrigin()
    g_destination = self.getDestination()
    t_origin = t.getVertexByName(g_origin.getName())
    t_destination = t.getVertexByName(g_destination.getName())
    o_oipn = t_origin.getPreorderNumber()
    d_oipn = t_destination.getPreorderNumber()
    result_str = "(" + str(o_oipn) + ", " + str(d_oipn) + ")"
    return result_str

class Vertex:
  def __init__(self, name):
    self.name = name
    self.pre = None
    self.post = None
    self.is_active = None
  def getName(self):
    return self.name
  def setPreorderNumber(self, value):
    self.pre = value
  def setPostorderNumber(self, value):
    self.post = value
  def getPreorderNumber(self):
    return self.pre
  def getPostorderNumber(self):
    return self.post
  def toString(self):
    return str(self.getName())

class Clock:
  def __init__(self, value = 1):
    self.value = value
  def getValue(self):
    return self.value
  def increment(self):
    self.value += 1

def explore(graph, node, visited_dict, clock, prev_edge = None, is_recursive_call = False):
  if is_recursive_call == True:
    prev_edge.setIsTreeEdge()
  visited_dict[node] = True
  previsit(node, clock)
  curr_edges = graph.getEdgesOriginatingAt(node)
  for curr_edge in curr_edges:
    destination = curr_edge.getDestination()
    if visited_dict[destination] == False:
      explore(graph, destination, visited_dict, clock, curr_edge, True)
  postvisit(node, clock)

def previsit(node, clock):
  node.setPreorderNumber(clock.getValue())
  clock.increment()

def postvisit(node, clock):
  node.setPostorderNumber(clock.getValue())
  clock.increment()

def dfs(graph, root):
  vertices = graph.getVertices()
  visited_dict = defaultdict(lambda: False)
  clock = Clock()
  rest_vertices = [x for x in vertices if x != root]
  next_vertices = [root] + rest_vertices
  for vertex in next_vertices:
    if visited_dict[vertex] == False:
      explore(graph, vertex, visited_dict, clock)

class Tree:
  def __init__(self):
    self.root = None
    self.vertices = []
    self.edges = []
    self.name_to_vertex = {}
    self.oipn_to_vertex_dict = {}
  def getRoot(self):
    return self.root
  def setRoot(self, node):
    self.root = node
  def _setPreorderNumbers(self):
    root = self.getRoot()
    clock = Clock(1)
    root._setPreorderNumbers(clock, self)
  def _setPreorderNumbersHelper(self, vertex):
    oipn = vertex.getPreorderNumber()
    self.oipn_to_vertex_dict[oipn] = vertex
  def _setRPOPreorderNumbersHelper(self, vertex):
    oipn = vertex.getPreorderNumber()
    self.oipn_to_vertex_dict[oipn] = vertex
  def _setRPOPreorderNumbers(self):
    root = self.getRoot()
    po_nodes_out = []
    root._setRPOPreorderNumbers(po_nodes_out)
    rpo_nodes = reversed(po_nodes_out)
    clock = 1
    for node in rpo_nodes:
      node.setPreorderNumber(clock)
      clock += 1
    # reversed uses an iterator that when used up must be reset
    next_rpo_nodes = reversed(po_nodes_out)
    for node in next_rpo_nodes:
      self._setRPOPreorderNumbersHelper(node)
  # we care about non-proper descendants
  def _setNumberOfDescendants(self):
    root = self.getRoot()
    root._setNumberOfDescendants()
  def addVertex(self, tree_vertex):
    self.vertices.append(tree_vertex)
    name = tree_vertex.getName()
    self.name_to_vertex[name] = tree_vertex
  def getVertices(self):
    return self.vertices
  def addEdge(self, tree_edge):
    self.edges.append(tree_edge)
  def getEdges(self):
    return self.edges
  # we assume each node has a unique name
  def getVertexByName(self, name):
    return self.name_to_vertex[name]
  # we deal with one-indexed pre-order numbers
  def getVertexByOIPN(self, oipn):
    return self.oipn_to_vertex_dict[oipn]
  def toString(self):
    root = self.getRoot()
    return root.toString()
  def toPreorderNumberString(self):
    root = self.getRoot()
    return root.toString(lambda x: x.getPreorderNumber())
  def toNDString(self):
    root = self.getRoot()
    return root.toString(lambda x: x.getNumberOfDescendants())

class TreeVertex():
  def __init__(self, name):
    self.name = name
    self.parent = None
    self.children = []
    self.pre = None
  def getName(self):
    return self.name
  def setParent(self, node):
    self.parent = node
  def getParent(self):
    return self.parent
  def addChild(self, node):
    self.children.append(node)
  def getChildren(self):
    return self.children
  def haveChildren(self):
    return len(self.children) != 0
  def haveParent(self):
    return self.parent != None
  def setPreorderNumber(self, value):
    self.pre = value
  def getPreorderNumber(self):
    return self.pre
  def _setPreorderNumbers(self, clock, tree):
    self.setPreorderNumber(clock.getValue())
    tree._setPreorderNumbersHelper(self)
    clock.increment()
    children = self.getChildren()
    for child in children:
      child._setPreorderNumbers(clock, tree)
  def _setRPOPreorderNumbers(self, po_nodes_out):
    children = self.getChildren()
    for child in children:
      child._setRPOPreorderNumbers(po_nodes_out)
    po_nodes_out.append(self)
  # assumes pre-order number is one-indexed
  def getZeroIndexedPreorderNumber(self):
    return self.getPreorderNumber() - 1
    self.nd = None
  def getNumberOfDescendants(self):
    return self.nd
  # we care about non-proper descendants
  def _setNumberOfDescendants(self):
    children = self.getChildren()
    num_children = len(children)
    if num_children == 0:
      count = 1
      self.nd = count
      return count
    count = sum([x._setNumberOfDescendants() for x in children]) + 1
    self.nd = count
    return count
  def toString(self, value_fn = lambda x: x.getName()):
    children = self.getChildren()
    curr_str = None
    if self.haveChildren() == False:
      curr_str = str(value_fn(self))
    else:
      curr_str = "(" + str(value_fn(self)) + " " + reduce(lambda x, y: x + " " + y, [x.toString(value_fn) for x in children]) + ")"
    return curr_str

class TreeEdge(Edge):
  def __init__(self, origin, destination):
    Edge.__init__(self, origin, destination)

# for graph nodes and edges
class AugmentingEdgeContainer:
  def __init__(self):
    self.edges = []
    self.destination_to_edges = defaultdict(lambda: [])
  def addEdge(self, edge):
    self.edges.append(edge)
    destination = edge.getDestination()
    self.destination_to_edges[destination].append(edge)
  def getEdgesEndingAt(self, node):
    return self.destination_to_edges[node]

# is cross or forward
class AugmentingEdge(Edge):
  def __init__(self, origin, destination):
    Edge.__init__(self, origin, destination)
  def isTreeEdge(self):
    return False
  def isCycleEdge(self):
    return False
  def isCrossEdge(self):
    raise Exception()
  def isForwardEdge(self):
    raise Exception()
  def isActive(self):
    raise Exception()
  def setIsTreeEdge(self):
    raise Exception()
  def setIsCycleEdge(self):
    raise Exception()
  def setIsCrossEdge(self):
    raise Exception()
  def setIsForwardEdge(self):
    raise Exception()
  def isActive(self):
    return True
  def setIsActive(self):
    raise Exception()
  def setIsInactive(self):
    raise Exception()
  def getEdgeTypeString(self):
    return "cross-or-forward"

def doIntervalsHelper(g, t, h, I, uf, v, i, augmenting_g_edge_container):
  if v <= i:
    # this is custom-added
    return
  h[v] = i
  I[i].append(v)
  uf.union(i, v)
  # ready for swap-out with gabow-tarjan off-line DSU
  # parent_oipn = t.getVertexByOIPN(v).getParent().getPreorderNumber()
  # uf.union(v, parent_oipn)
  # uf.renameSet(v, i)
  candidate_g_edges = g.getEdgesEndingAt(g.getVertexByName(t.getVertexByOIPN(v).getName()))
  candidate_a_g_edges = augmenting_g_edge_container.getEdgesEndingAt(g.getVertexByName(t.getVertexByOIPN(v).getName()))
  for curr_g_edge in candidate_g_edges + candidate_a_g_edges:
    g_w = curr_g_edge.getOrigin()
    t_w = t.getVertexByName(g_w.getName())
    t_oipn = t_w.getPreorderNumber()
    curr_value = uf.find(t_oipn)
    next_value = h[curr_value]
    # we must remember not to visit root
    if curr_value != i and next_value == 1 and curr_g_edge.isActive() == True:
      doIntervalsHelper(g, t, h, I, uf, curr_value, i, augmenting_g_edge_container)

def doIntervals(g, t, adj, g_start_node):
  # we need to group edges by kind -- i.e. into tree, cycle, cross, forward
  g_edges = g.getEdges()
  t_nodes = t.getVertices()
  t_edges = t.getEdges()
  g_tree_edges, g_cycle_edges, g_cross_edges, g_forward_edges = [], [], [], []
  for g_edge in g_edges:
    if g_edge.isTreeEdge() == True:
      g_tree_edges.append(g_edge)
    elif g_edge.isCycleEdge() == True:
      g_cycle_edges.append(g_edge)
    elif g_edge.isCrossEdge() == True:
      g_cross_edges.append(g_edge)
    elif g_edge.isForwardEdge() == True:
      g_forward_edges.append(g_edge)
  g_nodes = g.getVertices()
  num_nodes = len(g_nodes)
  
  augmenting_g_edge_container = AugmentingEdgeContainer()
  # phase one
  uf = NamedUnionFind()
  h = {}
  I = defaultdict(lambda: [])
  for i in xrange(1, num_nodes + 1):
    uf.insert_objects([i])
    h[i] = 1
    I[i] = [i]
  # phase two
  # LCA is based on tree edge zero-indexed pre-order numbers
  lca_bfc = LCA_BFC(num_nodes, adj)
  t_start_node = t.getVertexByName(g_start_node.getName())
  root_zipn = t_start_node.getZeroIndexedPreorderNumber()
  lca_bfc.precompute_lca(root_zipn)
  for g_edge in g_edges:
    if g_edge.isCrossEdge() == True or g_edge.isForwardEdge() == True:
      g_edge.setIsInactive()
    else:
      g_edge.setIsActive()
  # partition graph edges based on one-indexed LCA
  lca_to_g_edges_dict = defaultdict(lambda: [])
  for g_edge in g_edges:
    g_origin, g_destination = g_edge.getOrigin(), g_edge.getDestination()
    origin_name, destination_name = g_origin.getName(), g_destination.getName()
    t_origin = t.getVertexByName(origin_name)
    t_destination = t.getVertexByName(destination_name)
    origin_zipn = t_origin.getZeroIndexedPreorderNumber()
    destination_zipn = t_destination.getZeroIndexedPreorderNumber()
    curr_lca = lca_bfc.lca(origin_zipn, destination_zipn)
    curr_lca_oipn = curr_lca + 1
    lca_to_g_edges_dict[curr_lca_oipn].append(g_edge)
  for i in xrange(num_nodes, 2 - 1, -1):
    curr_g_edges_for_reintroduction = lca_to_g_edges_dict[i]
    for curr_g_edge in curr_g_edges_for_reintroduction:
      # we reintroduce cross or forward edges in form of augmenting edge of type cross-or-forward
      if curr_g_edge.isCrossEdge() == False and curr_g_edge.isForwardEdge() == False:
        continue
      g_v = curr_g_edge.getOrigin()
      g_w = curr_g_edge.getDestination()
      t_w = t.getVertexByName(g_w.getName())
      t_w_oipn = t_w.getPreorderNumber()
      augmenting_g_edge = AugmentingEdge(g_v, g.getVertexByName(t.getVertexByOIPN(uf.find(t_w_oipn)).getName()))
      augmenting_g_edge_container.addEdge(augmenting_g_edge)
    curr_candidate_g_edges = g.getEdgesEndingAt(g.getVertexByName(t.getVertexByOIPN(i).getName()))
    curr_g_cycle_edges = [x for x in curr_candidate_g_edges if x.isCycleEdge() == True]
    # we remember that only cycle edges can morph into cycle edges after a contraction
    for curr_g_cycle_edge in curr_g_cycle_edges:
      g_v = curr_g_cycle_edge.getOrigin()
      t_v = t.getVertexByName(g_v.getName())
      t_oipn = t_v.getPreorderNumber()
      curr_value = h[uf.find(t_oipn)]
      if curr_value == 1 and curr_g_cycle_edge.isActive() == True:
        doIntervalsHelper(g, t, h, I, uf, uf.find(t_oipn), i, augmenting_g_edge_container)
  # phase three
  for i in xrange(2, num_nodes + 1):
    if h[i] == 1:
      I[1].append(i)
  return h, I

def doBridges(g, t, adj, h, I, g_start_node):
  # we assume graph edges are grouped by kind -- i.e. into tree, cycle, cross, forward
  g_edges = g.getEdges()
  t_nodes = t.getVertices()
  t_edges = t.getEdges()
  g_nodes = g.getVertices()
  num_nodes = len(g_nodes)
  # phase one
  uf = NamedUnionFind()
  x_result = {}
  y_result = {}
  wake_list = defaultdict(lambda: [])
  bridges = []
  l = {}
  v_star = {}
  w_star = {}
  dest_t_oipn_to_candidate_bridge_dict = {}
  g_tree_edges = [x for x in g_edges if x.isTreeEdge() == True]
  for curr_g_edge in g_tree_edges:
    g_dest = curr_g_edge.getDestination()
    t_dest = t.getVertexByName(g_dest.getName())
    t_dest_oipn = t_dest.getPreorderNumber()
    dest_t_oipn_to_candidate_bridge_dict[t_dest_oipn] = curr_g_edge
  for i in xrange(1, num_nodes + 1):
    uf.insert_objects([i])
    x_result[i] = i
    y_result[i] = None
    wake_list[i] = []
  for curr_edge in g_edges:
    l[curr_edge] = None
    v_star[curr_edge] = None
    w_star[curr_edge] = None
  lca_bfc = LCA_BFC(num_nodes, adj)
  t_start_node = t.getVertexByName(g_start_node.getName())
  root_zipn = t_start_node.getZeroIndexedPreorderNumber()
  lca_bfc.precompute_lca(root_zipn)
  # partition graph edges based on one-indexed LCA
  lca_to_g_edges_dict = defaultdict(lambda: [])
  for g_edge in g_edges:
    g_origin, g_destination = g_edge.getOrigin(), g_edge.getDestination()
    origin_name, destination_name = g_origin.getName(), g_destination.getName()
    t_origin = t.getVertexByName(origin_name)
    t_destination = t.getVertexByName(destination_name)
    origin_zipn = t_origin.getZeroIndexedPreorderNumber()
    destination_zipn = t_destination.getZeroIndexedPreorderNumber()
    curr_lca = lca_bfc.lca(origin_zipn, destination_zipn)
    curr_lca_oipn = curr_lca + 1
    lca_to_g_edges_dict[curr_lca_oipn].append(g_edge)
  # phase two
  for i in xrange(num_nodes, 1 - 1, -1):
    curr_g_edges = lca_to_g_edges_dict[i]
    for curr_g_edge in curr_g_edges:
      g_w = curr_g_edge.getDestination()
      t_w = t.getVertexByName(g_w.getName())
      t_oipn = t_w.getPreorderNumber()
      curr_value = uf.find(t_oipn)
      wake_list[curr_value].append(curr_g_edge)
    curr_candidate_g_edges = g.getEdgesEndingAt(g.getVertexByName(t.getVertexByOIPN(i).getName()))
    curr_g_non_tree_edges = [x for x in curr_candidate_g_edges if x.isTreeEdge() == False]
    for curr_g_non_tree_edge in curr_g_non_tree_edges:
      g_v = curr_g_non_tree_edge.getOrigin()
      t_v = t.getVertexByName(g_v.getName())
      t_oipn = t_v.getPreorderNumber()
      if t_oipn < x_result[i]:
        x_result[i] = t_oipn
        y_result[i] = i
    if True:
      for u in I[i]:
        if u == i:
          pass
        for curr_g_edge in wake_list[u]:
          g_v, g_w = curr_g_edge.getOrigin(), curr_g_edge.getDestination()
          t_v, t_w = t.getVertexByName(g_v.getName()), t.getVertexByName(g_w.getName())
          t_v_oipn, t_w_oipn = t_v.getPreorderNumber(), t_w.getPreorderNumber()
          if uf.find(t_v_oipn) != uf.find(t_w_oipn):
            v_star[curr_g_edge] = uf.find(t_v_oipn)
            w_star[curr_g_edge] = uf.find(t_w_oipn)
            l[curr_g_edge] = i
        if x_result[u] < x_result[i]:
          x_result[i] = x_result[u]
          y_result[i] = y_result[u]
    if i != 1:
      for u in I[i]:
        if u == i:
          continue
        uf.union(i, u)
        # ready for swap-out with gabow-tarjan off-line DSU
        # parent_oipn = t.getVertexByOIPN(u).getParent().getPreorderNumber()
        # uf.union(u, parent_oipn)
        # uf.renameSet(u, i)
    if i == 1:
      x_result[i] = None
      y_result[i] = None
    elif x_result[i] == i:
      candidate_bridge = dest_t_oipn_to_candidate_bridge_dict[i]
      bridges.append(candidate_bridge)
      g_origin = candidate_bridge.getOrigin()
      t_origin = t.getVertexByName(g_origin.getName())
      t_origin_oipn = t_origin.getPreorderNumber()
      x_result[i] = t_origin_oipn
      y_result[i] = i
  # deal with edges (v, w) whose endpoints v and w 
  # are never both merged into some other node u s.t. u != v and u != w
  for curr_g_edge in g_edges:
    if l[curr_g_edge] == None:
      l[curr_g_edge] = 1
  for curr_g_edge in g_edges:
    if l[curr_g_edge] == 1:
      g_v, g_w = curr_g_edge.getOrigin(), curr_g_edge.getDestination()
      t_v, t_w = t.getVertexByName(g_v.getName()), t.getVertexByName(g_w.getName())
      t_v_oipn, t_w_oipn = t_v.getPreorderNumber(), t_w.getPreorderNumber()
      v_star[curr_g_edge] = uf.find(t_v_oipn)
      w_star[curr_g_edge] = uf.find(t_w_oipn)
  return bridges, x_result, y_result, l, v_star, w_star

# introduces a node with name "dummy"
def addDummyNode(g, base_vertex):
  v_dummy = Vertex("dummy")
  curr_edge = Edge(v_dummy, base_vertex)
  g.addVertex(v_dummy)
  g.addEdge(curr_edge)
  return v_dummy

def doStar(t_v, t_w):
  nd_v = t_v.getNumberOfDescendants()
  oipn_v = t_v.getPreorderNumber()
  oipn_w = t_w.getPreorderNumber()
  result = oipn_v <= oipn_w and oipn_w < oipn_v + nd_v
  return result

# remember that graph g will be modified, as well; 
# we also remember that we assume start vertex has no in-edges
def prepareGraph(g, start_vertex):
  # tree edges can be interpreted in two ways -- 
  # edges from graph that are edges in associated DFS tree 
  # or edges from tree
  next_vertices = g.getVertices()
  next_edges = g.getEdges()
  # this will set type for graph edges that are of type tree
  dfs(g, start_vertex)
  # we have two types of pre-order -- one for graph and one for tree
  t = Tree()
  tree_vertices = [TreeVertex(x.getName()) for x in next_vertices]
  name_to_tree_vertex_dict = {}
  for tree_vertex in tree_vertices:
    name = tree_vertex.getName()
    name_to_tree_vertex_dict[name] = tree_vertex
    t.addVertex(tree_vertex)
  t.setRoot(name_to_tree_vertex_dict[start_vertex.getName()])
  for edge in next_edges:
    g_origin, g_destination = edge.getOrigin(), edge.getDestination()
    origin_name, destination_name = g_origin.getName(), g_destination.getName()
    t_origin, t_destination = name_to_tree_vertex_dict[origin_name], name_to_tree_vertex_dict[destination_name]
    t_destination.setParent(t_origin)
    tree_edge = TreeEdge(t_origin, t_destination)
    t.addEdge(tree_edge)
    if edge.isTreeEdge() == True:
      t_origin.addChild(t_destination)
  # t._setPreorderNumbers()
  t._setRPOPreorderNumbers()
  t._setNumberOfDescendants()

  # using graph pre-order/post-order is inappropriate for classifying of edges; 
  # using dfs tree pre-order and post-order is the correct way; 
  # note that we use graph edges as opposed to tree edges at this point
  for edge in next_edges:
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

  num_nodes = len(next_vertices)
  # for LCA structure based on DFS tree
  adj = defaultdict(lambda: [])
  for tree_vertex in tree_vertices:
    curr_zipn = tree_vertex.getZeroIndexedPreorderNumber()
    children = tree_vertex.getChildren()
    child_zipn_values = [x.getZeroIndexedPreorderNumber() for x in children]
    for child_zipn_value in child_zipn_values:
      adj[curr_zipn].append(child_zipn_value)
      adj[child_zipn_value].append(curr_zipn)
  return g, t, adj

if __name__ == '__main__':

  """

  # from example on wikipedia article about depth-first search

  v_A = Vertex("A")
  v_B = Vertex("B")
  v_C = Vertex("C")
  v_D = Vertex("D")

  vertices = [v_A, v_B, v_C, v_D]

  e1 = Edge(v_A, v_B)
  e2 = Edge(v_A, v_C)
  e3 = Edge(v_B, v_D)
  e4 = Edge(v_C, v_D)

  edges = [e1, e2, e3, e4]

  """

  # self-created

  v_A = Vertex("A")
  v_B = Vertex("B")
  v_C = Vertex("C")
  v_D = Vertex("D")
  v_E = Vertex("E")
  v_F = Vertex("F")
  v_G = Vertex("G")
  v_H = Vertex("H")
  v_I = Vertex("I")

  vertices = [v_A, v_B, v_C, v_D, v_E, v_F, v_G, v_H, v_I]

  e1 = Edge(v_A, v_B)
  e2 = Edge(v_B, v_C)
  e3 = Edge(v_C, v_D)
  e4 = Edge(v_D, v_E)
  e5 = Edge(v_E, v_B)
  e6 = Edge(v_A, v_F)
  e7 = Edge(v_F, v_G)
  e8 = Edge(v_G, v_H)
  e9 = Edge(v_H, v_I)
  e10 = Edge(v_I, v_F)
  e11 = Edge(v_A, v_B)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11]

  g = Graph()
  g.addVertices(vertices)
  g.addEdges(edges)
  # g._sortOriginToEdgesLists()

  v_dummy = addDummyNode(g, v_A)
  g, t, adj = prepareGraph(g, v_dummy)

  next_vertices = g.getVertices()
  next_edges = g.getEdges()
  num_nodes = len(next_vertices)

  result = doIntervals(g, t, adj, v_dummy)
  curr_h, curr_I = result
  next_result = doBridges(g, t, adj, curr_h, curr_I, v_dummy)
  bridges, x_result, y_result, l, v_star, w_star = next_result

  print [(x.getOrigin().getName(), x.getDestination().getName()) for x in bridges]

  """

  for i in xrange(1, num_nodes + 1):
    print "i, (x(i), y(i)):", i, x_result[i], y_result[i]

  """

  """

  for curr_g_edge in next_edges:
    curr_v = t.getVertexByName(curr_g_edge.getOrigin().getName())
    curr_w = t.getVertexByName(curr_g_edge.getDestination().getName())
    curr_v_oipn = curr_v.getPreorderNumber()
    curr_w_oipn = curr_w.getPreorderNumber()
    print "(v, w):", curr_v_oipn, curr_w_oipn
    print "l value:", l[curr_g_edge]
    print "(v*, w*):", v_star[curr_g_edge], w_star[curr_g_edge]
    print

  """


