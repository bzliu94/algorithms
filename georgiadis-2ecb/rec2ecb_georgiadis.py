# 2019-05-25

# addressing difference between overall and local ordinary vertex/edge

# 2019-05-20

# dominator tree root can be a boundary node for a subtree

# base edges are induced by pairs of ordinary nodes

# 2019-05-19

# start vertex has to be ordinary, low is not set for compressed dominator tree root

# 2019-05-18

# time is O(m * n * alpha)

# we assume names are short and hashable

# we set ordinary/auxiliary status for nodes and edges 
# for dominator tree and subtrees, but override them effectively 
# when we switch to using auxiliary subgraphs

# input nodes and edges must be set to be ordinary manually

# 2019-04-18

# we implement rec2ecb from georgiadis et al. 2014

from fgib_tarjan import Graph, Vertex, Edge, addDummyNode, prepareGraph, doIntervals, doBridges, Tree, TreeVertex, TreeEdge
from sb_italiano import doStrongBridges, ReversedEdge
from scc_ks import SCC_KS
from collections import defaultdict
from dt_fraczak_GD2_faster import GD

from bundle_one.list.DoublyLinkedList import DoublyLinkedList
from bundle_one.list.DoublyLinkedListNode import DoublyLinkedListNode

# takes time linear in number of items and size of range; 
# assume buckets are in range [k_l, k_l + 1, k_l + 2, ..., k_r]
def bucketSort(items, k_l, k_r, key = lambda x: x):
  key_to_bucket_dict = defaultdict(lambda: [])
  for item in items:
    curr_key = key(item)
    key_to_bucket_dict[curr_key].append(item)
  result = []
  for i in xrange(k_l, k_r + 1):
    for j in xrange(len(key_to_bucket_dict[i])):
      curr_item = key_to_bucket_dict[i][j]
      result.append(curr_item)
  return result

"""
print bucketSort([1, 0, 3, 4, 2, 4], 0, 4, lambda x: x)
raise Exception()
"""

from collections import deque

def doMatch(items1, items2, fn1 = lambda x: x, fn2 = lambda x: x):
  result = []
  next_items1 = deque(items1)
  next_items2 = deque(items2)
  doMatchHelper(next_items1, next_items2, None, result, fn1, fn2)
  return result
def doMatchHelper(items1, items2, prev_item2, result, fn1, fn2):
  if len(items1) == 0:
    return
  elif len(items2) == 0:
    result.append(prev_item2)
    items1.popleft()
    doMatchHelper(items1, items2, prev_item2, result, fn1, fn2)
  else:
    curr_item1 = items1[0]
    curr_item2 = items2[0]
    curr_transformed_item1 = fn1(curr_item1)
    curr_transformed_item2 = fn2(curr_item2)
    if curr_transformed_item2 > curr_transformed_item1:
      result.append(prev_item2)
      items1.popleft()
      doMatchHelper(items1, items2, prev_item2, result, fn1, fn2)
    else:
      items2.popleft()
      doMatchHelper(items1, items2, curr_item2, result, fn1, fn2)

"""
# expected result is [None, 5, 5, 6, 8, 8]
print doMatch([4, 5, 5, 6, 9, 11], [5, 6, 8, 10])
# expected result is []
print doMatch([], [1, 2, 3])
# expected result is [None, None, None]
print doMatch([1, 2, 3], [])
# expected result is [0, 2, 2]
print doMatch([1, 2, 3], [0, 2, 4, 5, 6, 7])
# expected result is []
print doMatch([], [])
# expected result is [None, None, None, None]
print doMatch([10, 11, 12, 13], [14, 15, 16])
# expected result is [2, 2, 2]
print doMatch([10, 11, 12], [1, 2])
raise Exception()
"""

# takes time linear in size of source edge list and size of origin candidate list
def doShortcutEdgeCaseBSelectZ(augmented_secs, augmented_cobvs):
  result = doMatch(augmented_secs, augmented_cobvs, lambda x: x[1], lambda x: x[1])
  next_result = []
  for item in result:
    if item == None:
      next_result.append(None)
    else:
      next_result.append(item[0])
  return next_result
def doStar(t_v, t_w):
  nd_v = t_v.getNumberOfDescendants()
  oipn_v = t_v.getPreorderNumber()
  oipn_w = t_w.getPreorderNumber()
  result = oipn_v <= oipn_w and oipn_w < oipn_v + nd_v
  return result

OVERALL_ORDINARY_VERTEX = 0
OVERALL_AUXILIARY_VERTEX = 1

LOCAL_ORDINARY_VERTEX = 0
LOCAL_AUXILIARY_VERTEX = 1

LOCAL_ORDINARY_EDGE = 0
LOCAL_AUXILIARY_EDGE = 1

# dominator-subtree tree
class DSTree(Tree):
  def __init__(self):
    Tree.__init__(self)
    self.origin_dest_tuple_to_edge_dict = {}
  # this is to do with special status
  def doMarkNonProperAncestorsOfOverallOrdinaryNodes(self):
    root = self.getRoot()
    root.doMarkNonProperAncestorsOfOverallOrdinaryNodes()
  # we assume nodes have been marked; 
  # output is a list of tuples s.t. each tuple is of form (root, node_group)
  def getAugmentedSubtreeNodeGroups(self):
    actual_root = self.getRoot()
    secondary_roots = [x for x in self.getPreorderNodes() if x.isMarked() == True]
    result = []
    actual_root_group = actual_root.getProperDescendantsStoppingAtMarkedNodes()
    result.append((actual_root, actual_root_group))
    for secondary_root in secondary_roots:
      curr_group = secondary_root.getProperDescendantsStoppingAtMarkedNodes()
      result.append((secondary_root, curr_group))
    return result
  def doMarkBoundaryNodes(self):
    root = self.getRoot()
    root.doMarkBoundaryNodes()
  def addEdge(self, edge):
    Tree.addEdge(self, edge)
    origin = edge.getOrigin()
    dest = edge.getDestination()
    key = (origin, dest)
    self.origin_dest_tuple_to_edge_dict[key] = edge
  def getEdge(self, origin, dest):
    key = (origin, dest)
    return self.origin_dest_tuple_to_edge_dict[key]
  def getNodesThatAreProperDescendantOfBoundaryNode(self):
    root = self.getRoot()
    return root.getNodesThatAreProperDescendantOfBoundaryNode()
  @staticmethod
  def getChildrenOfBoundaryVertices(subtree_vertices):
    boundary_vertices = [x for x in subtree_vertices if x.isBoundary() == True]
    result = []
    for boundary_vertex in boundary_vertices:
      children = boundary_vertex.getChildren()
      result.extend(children)
    return result
  def getCompressedTree(self):
    root = self.getRoot()
    next_tree = DSTree()
    next_root = DSTreeVertex(root.getName())
    next_tree.setRoot(next_root)
    root._getCompressedTree(next_tree, next_root, True)
    return next_tree
  def determineLabelValues(self, source_edges, root_name_to_subtree_graph_dict, uncompressed_dominator_tree, node_name_to_subtree_root_dict):
    # we take advantage of fact that source edges have endpoints that are not newly added -- they come from nodes and edges already present in source dominator tree from which we have cut into subtrees that we have auxiliary graphs (i.e. we do not have endpoints or edges that are bridge-related or shortcut-related that we have just added for current auxiliary graph)
    root = self.getRoot()
    root._determineLabelValues(source_edges, root_name_to_subtree_graph_dict, uncompressed_dominator_tree, node_name_to_subtree_root_dict, True)
  def determineLowValues(self):
    root = self.getRoot()
    root._determineLowValues(True)
  @staticmethod
  # for current subtree graph with associated subtree with root r, we consider children of boundary vertices in the subtree and if low(z) < pre(r), we add edge to subtree graph of (z, d(r)); 
  # cdt is compressed dominator tree, dt is dominator tree
  def collectShortcutCaseCEdges(cdt, dt, subtree_nodes, curr_subtree_G, subtree_root):
    result = []
    curr_boundary_nodes = [x for x in subtree_nodes if dt.getVertexByName(x.getName()).isBoundary() == True]
    curr_child_of_boundary_node_list = []
    for curr_boundary_node in curr_boundary_nodes:
      curr_children = curr_boundary_node.getChildren()
      # we may need to check that the node (i.e. a child) is marked
      for curr_child in curr_children:
        if curr_child.isMarked() == False:
          continue
        curr_child_of_boundary_node_list.append(curr_child)
    # here is a synonym
    curr_marked_nodes = curr_child_of_boundary_node_list
    # subtree_root is from dominator tree we cut up
    r = subtree_root
    pre_r = r.getPreorderNumber()
    for curr_marked_node in curr_marked_nodes:
      z = cdt.getVertexByName(curr_marked_node.getName())
      low_z = z.getLow()
      if low_z < pre_r:
        # make edge (z, d(r)) using partially made auxiliary graph (i.e. one with all nodes that we need to add added)
        edge = AOEdge(curr_subtree_G.getVertexByName(z.getName()), curr_subtree_G.getVertexByName(r.getParent().getName()))
        edge.setIsLocalAuxiliary()
        result.append(edge)
    return result

class DSTreeVertex(TreeVertex):
  def __init__(self, name):
    TreeVertex.__init__(self, name)
    self.overall_kind = None
    self.local_kind = None
    # for step two of rec2ecb
    self.is_special = False
    # is for dominator tree node marking s.t. we use bridges
    self.marked = False
    # is for auxiliary edges
    self.is_boundary = False
    # for case c
    self.label = None
    self.low = None
  def isOverallOrdinary(self):
    return self.overall_kind == OVERALL_ORDINARY_VERTEX
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_VERTEX
  def isOverallAuxiliary(self):
    return self.overall_kind == OVERALL_AUXILIARY_VERTEX
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_VERTEX
  def isSpecial(self):
    return self.is_special
  def isBoundary(self):
    return self.is_boundary
  def getLabel(self):
    return self.label
  def getLow(self):
    return self.low
  def setIsOverallOrdinary(self):
    self.overall_kind = OVERALL_ORDINARY_VERTEX
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_VERTEX
  def setIsOverallAuxiliary(self):
    self.overall_kind = OVERALL_AUXILIARY_VERTEX
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_VERTEX
  def setIsSpecial(self):
    self.is_special = True
  def setIsBoundary(self):
    self.is_boundary = True
  def setLabel(self, label):
    self.label = label
  def setLow(self, low):
    self.low = low
  def doMarkNonProperAncestorsOfOverallOrdinaryNodes(self):
    if self.haveChildren() == False:
      # we are leaf
      if self.isOverallOrdinary() == True:
        self.setIsSpecial()
        return True
      else:
        return False
    else:
      # we are internal node
      results = []
      # don't forget to include current node
      results.append(self.isOverallOrdinary())
      for child in self.getChildren():
        curr_result = child.doMarkNonProperAncestorsOfOverallOrdinaryNodes()
        results.append(curr_result)
      if True in results:
        self.setIsSpecial()
        return True
      else:
        return False
  def mark(self):
    self.marked = True
  def isMarked(self):
    return self.marked
  def getProperDescendantsStoppingAtMarkedNodes(self):
    result = []
    self._getProperDescendantsStoppingAtMarkedNodesHelper(result, True)
    return result
  def _getProperDescendantsStoppingAtMarkedNodesHelper(self, result, skip_curr_node = False):
    children = self.getChildren()
    if self.isMarked() == True and skip_curr_node == False:
      return
    else:
      result.append(self)
      for child in children:
        child._getProperDescendantsStoppingAtMarkedNodesHelper(result, False)
  def doMarkBoundaryNodes(self):
    self._doMarkBoundaryNodesHelper()
    # root can be boundary node
    """
    children = self.getChildren()
    for child in children:
      child._doMarkBoundaryNodesHelper()
    """
  # we forgot to recurse
  def _doMarkBoundaryNodesHelper(self):
    children = self.getChildren()
    for child in children:
      if child.isMarked() == True:
        self.setIsBoundary()
      child._doMarkBoundaryNodesHelper()
  def getNodesThatAreProperDescendantOfBoundaryNode(self):
    result = []
    self._getNodesThatAreProperDescendantOfBoundaryNodeHelper(result, False)
    return result
  def _getNodesThatAreProperDescendantOfBoundaryNodeHelper(self, result, seen_boundary_node):
    children = self.getChildren()
    if seen_boundary_node == True:
      result.append(self)
    curr_seen_boundary_node = None
    if self.isBoundary() == True or seen_boundary_node == True:
      curr_seen_boundary_node = True
    else:
      curr_seen_boundary_node = False
    for child in children:
      child._getNodesThatAreProperDescendantOfBoundaryNodeHelper(result, curr_seen_boundary_node)
  def _getCompressedTree(self, next_tree, ancestor, skip_curr_node = False):
    # overall/local ordinary/auxiliary statuses do not matter for compressed dominator tree
    next_ancestor = ancestor
    if skip_curr_node == False:
      # check curr. node
      if self.isMarked() == True:
        # include current node
        curr_node = DSTreeVertex(self.getName())
        next_ancestor = curr_node
        curr_node.setParent(ancestor)
        ancestor.addChild(curr_node)
        curr_edge = DSTreeEdge(ancestor, curr_node)
        next_tree.addVertex(curr_node)
        next_tree.addEdge(curr_edge)
      else:
        # exclude current node
        pass
    children = self.getChildren()
    for child in children:
      child._getCompressedTree(next_tree, next_ancestor, False)
  def _determineLabelValues(self, source_edges, root_name_to_subtree_graph_dict, uncompressed_dominator_tree, node_name_to_subtree_root_dict, skip_curr_node = False):
    children = self.getChildren()
    if skip_curr_node == False:
      # we are assuming this tree is compressed dominator tree
      pre_values = []
      for edge in source_edges:
        # find min. pre of a subtree root s.t. that subtree contains destination of a source edge s.t. origin is in subtree for current compressed dominator tree node; 
        # in other words, this node is w and we set label(w) to be min. pre(r_v) for source edge (u, v) s.t. u is in T(w); if no source edge exists, set label(w) to be pre(w)
        curr_origin = edge.getOrigin()
        curr_dest = edge.getDestination()
        T_w = root_name_to_subtree_graph_dict[self.getName()]
        if T_w.haveVertexWithName(curr_origin.getName()) == True:
          # we make use of getting a list of auxiliary graphs that contain a certain node
          T_v_root_name_list = [x.getName() for x in node_name_to_subtree_root_dict[curr_dest.getName()]]
          curr_pre_value_list = [uncompressed_dominator_tree.getVertexByName(x).getPreorderNumber() for x in T_v_root_name_list]
          # we are assuming this takes time linear in size of second list
          pre_values.extend(curr_pre_value_list)
      if len(pre_values) == 0:
        self.setLabel(uncompressed_dominator_tree.getVertexByName(self.getName()).getPreorderNumber())
      else:
        self.setLabel(min(pre_values))
    for child in children:
      child._determineLabelValues(source_edges, root_name_to_subtree_graph_dict, uncompressed_dominator_tree, node_name_to_subtree_root_dict, False)
  def _determineLowValues(self, skip_curr_node = False):
    children = self.getChildren()
    for child in children:
      child._determineLowValues(False)
    candidate_low_values = [x.getLow() for x in children]
    if skip_curr_node == False:
      candidate_low_values.append(self.getLabel())
      curr_low_value = min(candidate_low_values)
      self.setLow(curr_low_value)

class DSTreeEdge(TreeEdge):
  def __init__(self, origin, destination):
    TreeEdge.__init__(self, origin, destination)
    self.local_kind = None
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_EDGE
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_EDGE
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_EDGE
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_EDGE

"""
dst = DSTree()
root = DSTreeVertex("root")
v_a = DSTreeVertex("a")
e1 = DSTreeEdge(root, v_a)
root.addChild(v_a)
dst.setRoot(root)
dst.addVertices([root, v_a])
dst.addEdge(e1)
print "dominator-subtree tree:", dst.toString()
raise Exception()
"""

"""
compressing tree to only have marked vertices and root
root*
|	\
v1	v2
|	|
v3*	v4*
	|	\
	v5	v6*
=>
root
|	\
v3	v4
	|
	v6
root
|	\
v1	v2
|	|
v3*	v4*
	|	\
	v5	v6*
=>
root
|	\
v3	v4
	|
	v6
"""

"""
t1 = DSTree()
root = DSTreeVertex("root")
v1 = DSTreeVertex(1)
v2 = DSTreeVertex(2)
v3 = DSTreeVertex(3)
v4 = DSTreeVertex(4)
v5 = DSTreeVertex(5)
v6 = DSTreeVertex(6)
vertices = [root, v1, v2, v3, v4, v5, v6]
t1.addVertices(vertices)
t1.setRoot(root)
root.addChild(v1)
root.addChild(v2)
v1.setParent(root)
v1.addChild(v3)
v2.setParent(v1)
v2.addChild(v4)
v3.setParent(v1)
v4.setParent(v2)
v4.addChild(v5)
v4.addChild(v6)
v5.setParent(v4)
v6.setParent(v4)
# root.mark()
v3.mark()
v4.mark()
v6.mark()
e1 = DSTreeEdge(root, v1)
e2 = DSTreeEdge(root, v2)
e3 = DSTreeEdge(v1, v3)
e4 = DSTreeEdge(v2, v4)
e5 = DSTreeEdge(v4, v5)
e6 = DSTreeEdge(v4, v6)
edges = [e1, e2, e3, e4, e5, e6]
t1.addEdges(edges)
print t1.toString()
t1_c = t1.getCompressedTree()
print t1_c.toString()
raise Exception()
"""

# auxiliary-original graph
class AOGraph(Graph):
  def __init__(self):
    Graph.__init__(self)

class AOVertex(Vertex):
  def __init__(self, name):
    Vertex.__init__(self, name)
    self.overall_kind = None
    self.local_kind = None
  def isOverallOrdinary(self):
    return self.overall_kind == OVERALL_ORDINARY_VERTEX
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_VERTEX
  def isOverallAuxiliary(self):
    return self.overall_kind == OVERALL_AUXILIARY_VERTEX
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_VERTEX
  def setIsOverallOrdinary(self):
    self.overall_kind = OVERALL_ORDINARY_VERTEX
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_VERTEX
  def setIsOverallAuxiliary(self):
    self.overall_kind = OVERALL_AUXILIARY_VERTEX
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_VERTEX

class AOEdge(Edge):
  def __init__(self, origin, destination):
    Edge.__init__(self, origin, destination)
    self.local_kind = None
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_EDGE
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_EDGE
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_EDGE
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_EDGE

class AOReversedEdge(ReversedEdge):
  def __init__(self, origin, destination, reference_edge):
    ReversedEdge.__init__(self, origin, destination, reference_edge)
    self.local_kind = None
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_EDGE
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_EDGE
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_EDGE
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_EDGE

"""
aog = AOGraph()
root = AOVertex("root")
v_a = AOVertex("a")
e1 = AOEdge(root, v_a)
aog.addVertices([root, v_a])
aog.addEdge(e1)
print len(aog.getVertices()), len(aog.getEdges())
print "auxiliary-original graph:", aog
raise Exception()
"""

# takes O(m * n * alpha) time
def doRec2ECB(V, E):
  result = doRec2ECBHelper(V, E)
  return result.toElementList()
def doRec2ECBHelper(V, E):
  num_overall_ordinary_nodes = len([x for x in V if x.isOverallOrdinary() == True])
  if num_overall_ordinary_nodes < 2:
    result = [x for x in V if x.isOverallOrdinary() == True]
    next_result = DoublyLinkedList()
    if len(result) != 0:
      dll_node = DoublyLinkedListNode(result, None, None)
      next_result.addLast(dll_node)
    return next_result
  # step 1.1 -- choose start vertex
  # (note -- we assume the start vertex must be ordinary in an overall sense)
  s = [x for x in V if x.isOverallOrdinary() == True][0]
  # (we assume we are allowed to modify input item properties without affecting other problems)
  for old_vertex in V:
    old_vertex.setIsLocalOrdinary()
  for old_edge in E:
    old_edge.setIsLocalOrdinary()
  # step 1.2 -- find forward dominator tree
  dt1 = GD(V, E, s)
  # (note that the size is off because we omit dominator for root)
  # step 1.3 -- find forward bridges
  g1 = Graph()
  g1.addVertices(V)
  g1.addEdges(E)
  v_dummy1 = addDummyNode(g1, s)
  g1, t1, adj1 = prepareGraph(g1, v_dummy1)
  result1 = doIntervals(g1, t1, adj1, v_dummy1)
  curr_h1, curr_I1 = result1
  next_result1 = doBridges(g1, t1, adj1, curr_h1, curr_I1, v_dummy1)
  bridges1, x_result1, y_result1, l1, v_star1, w_star1 = next_result1
  dummy_name1 = v_dummy1.getName()
  next_bridges1 = []
  for bridge in bridges1:
    origin = bridge.getOrigin()
    dest = bridge.getDestination()
    o_name = origin.getName()
    d_name = dest.getName()
    if o_name != dummy_name1 and d_name != dummy_name1:
      next_bridges1.append(bridge)
  # step 1.4 -- find reverse graph
  next_V = []
  for old_vertex in V:
    curr_vertex = AOVertex(old_vertex.getName())
    if old_vertex.isOverallOrdinary() == True:
      curr_vertex.setIsOverallOrdinary()
    elif old_vertex.isOverallAuxiliary() == True:
      curr_vertex.setIsOverallAuxiliary()
    curr_vertex.setIsLocalOrdinary()
    next_V.append(curr_vertex)
  name_to_next_vertex = {}
  for vertex in next_V:
    name = vertex.getName()
    name_to_next_vertex[name] = vertex
  next_E = []
  for edge in E:
    curr_origin = edge.getOrigin()
    curr_destination = edge.getDestination()
    next_origin = name_to_next_vertex[curr_origin.getName()]
    next_destination = name_to_next_vertex[curr_destination.getName()]
    reversed_edge = AOReversedEdge(next_destination, next_origin, edge)
    reversed_edge.setIsLocalOrdinary()
    next_E.append(reversed_edge)
  next_s = name_to_next_vertex[s.getName()]
  # step 1.5 -- find reverse dominator tree
  name_to_old_vertex = {}
  for vertex in V:
    name = vertex.getName()
    name_to_old_vertex[name] = vertex
  dt2 = GD(next_V, next_E, next_s)
  # deal with original nodes
  dt2_original = {}
  for child, parent in dt2.items():
    old_child = name_to_old_vertex[child.getName()]
    old_parent = name_to_old_vertex[parent.getName()]
    dt2_original[old_child] = old_parent
  # (note that the size is off because we omit dominator for root)
  # step 1.6 -- find reverse bridges
  g2 = Graph()
  g2.addVertices(next_V)
  g2.addEdges(next_E)
  v_dummy2 = addDummyNode(g2, next_s)
  g2, t2, adj2 = prepareGraph(g2, v_dummy2)
  result2 = doIntervals(g2, t2, adj2, v_dummy2)
  curr_h2, curr_I2 = result2
  next_result2 = doBridges(g2, t2, adj2, curr_h2, curr_I2, v_dummy2)
  bridges2, x_result2, y_result2, l2, v_star2, w_star2 = next_result2
  dummy_name2 = v_dummy2.getName()
  next_bridges2 = []
  for bridge in bridges2:
    origin = bridge.getOrigin()
    dest = bridge.getDestination()
    o_name = origin.getName()
    d_name = dest.getName()
    if o_name != dummy_name2 and d_name != dummy_name2:
      next_bridges2.append(bridge)
  next_bridges2_original = [x.getReferenceEdge() for x in next_bridges2]
  # step two
  # (we make explicit tree for forward dominator tree to compute number of special forward bridges)
  # (we assume names are hashable)
  name_tuple_to_edge_dict1 = {}
  for curr_edge in E:
    origin = curr_edge.getOrigin()
    dest = curr_edge.getDestination()
    origin_name = origin.getName()
    dest_name = dest.getName()
    name_pair = (origin_name, dest_name)
    name_tuple_to_edge_dict1[name_pair] = curr_edge
  t1 = DSTree()
  t_nodes1 = []
  t_edges1 = []
  name_to_t_node_dict1 = {}
  for node in V:
    name = node.getName()
    t_node = DSTreeVertex(name)
    if node.isOverallOrdinary() == True:
      t_node.setIsOverallOrdinary()
    elif node.isOverallAuxiliary() == True:
      t_node.setIsOverallAuxiliary()
    t_node.setIsLocalOrdinary()
    t_nodes1.append(t_node)
    name_to_t_node_dict1[name] = t_node
  start_t_node1 = name_to_t_node_dict1[s.getName()]
  for curr_child, curr_parent in dt1.items():
    curr_child_t_node = name_to_t_node_dict1[curr_child.getName()]
    curr_parent_t_node = name_to_t_node_dict1[curr_parent.getName()]
    curr_child_t_node.setParent(curr_parent_t_node)
    curr_parent_t_node.addChild(curr_child_t_node)
    curr_t_edge = DSTreeEdge(curr_parent_t_node, curr_child_t_node)
    origin_name = curr_parent_t_node.getName()
    dest_name = curr_child_t_node.getName()
    name_pair = (origin_name, dest_name)
    if name_pair in name_tuple_to_edge_dict1:
      old_edge = name_tuple_to_edge_dict1[name_pair]
      if old_edge.isLocalOrdinary() == True:
        curr_t_edge.setIsLocalOrdinary()
      elif old_edge.isLocalAuxiliary() == True:
        curr_t_edge.setIsLocalAuxiliary()
    else:
        curr_t_edge.setIsLocalAuxiliary()
    t_edges1.append(curr_t_edge)
  t1.setRoot(start_t_node1)
  t1.addVertices(t_nodes1)
  t1.addEdges(t_edges1)
  t1.doMarkNonProperAncestorsOfOverallOrdinaryNodes()
  # count the bridges that end at special nodes
  b_count1 = 0
  for g_edge in next_bridges1:
    g_destination = g_edge.getDestination()
    t_destination = t1.getVertexByName(g_destination.getName())
    if t_destination.isSpecial() == True:
      b_count1 += 1
  # (we make explicit tree for reverse dominator tree)
  # (we assume names are hashable)
  name_tuple_to_edge_dict2 = {}
  for curr_edge in next_E:
    origin = curr_edge.getOrigin()
    dest = curr_edge.getDestination()
    origin_name = origin.getName()
    dest_name = dest.getName()
    name_pair = (origin_name, dest_name)
    name_tuple_to_edge_dict2[name_pair] = curr_edge
  t2 = DSTree()
  t_nodes2 = []
  t_edges2 = []
  name_to_t_node_dict2 = {}
  for node in next_V:
    name = node.getName()
    t_node = DSTreeVertex(name)
    if node.isOverallOrdinary() == True:
      t_node.setIsOverallOrdinary()
    elif node.isOverallAuxiliary() == True:
      t_node.setIsOverallAuxiliary()
    t_node.setIsLocalOrdinary()
    t_nodes2.append(t_node)
    name_to_t_node_dict2[name] = t_node
  start_t_node2 = name_to_t_node_dict2[s.getName()]
  for curr_child, curr_parent in dt2_original.items():
    curr_child_t_node = name_to_t_node_dict2[curr_child.getName()]
    curr_parent_t_node = name_to_t_node_dict2[curr_parent.getName()]
    curr_child_t_node.setParent(curr_parent_t_node)
    curr_parent_t_node.addChild(curr_child_t_node)
    curr_t_edge = DSTreeEdge(curr_parent_t_node, curr_child_t_node)
    origin_name = curr_parent_t_node.getName()
    dest_name = curr_child_t_node.getName()
    name_pair = (origin_name, dest_name)
    if name_pair in name_tuple_to_edge_dict2:
      old_edge = name_tuple_to_edge_dict2[name_pair]
      if old_edge.isLocalOrdinary() == True:
        curr_t_edge.setIsLocalOrdinary()
      elif old_edge.isLocalAuxiliary() == True:
        curr_t_edge.setIsLocalAuxiliary()
    else:
        curr_t_edge.setIsLocalAuxiliary()
    t_edges2.append(curr_t_edge)
  t2.setRoot(start_t_node2)
  t2.addVertices(t_nodes2)
  t2.addEdges(t_edges2)
  t2.doMarkNonProperAncestorsOfOverallOrdinaryNodes()
  # count the bridges that end at special nodes
  b_count2 = 0
  for g_edge in next_bridges2:
    g_destination = g_edge.getDestination()
    t_destination = t2.getVertexByName(g_destination.getName())
    if t_destination.isSpecial() == True:
      b_count2 += 1
  # step 3 -- exit early, possibly
  if b_count1 == b_count2 and b_count1 == 0:
    result = [x for x in V if x.isOverallOrdinary() == True]
    next_result = DoublyLinkedList()
    if len(result) != 0:
      dll_node = DoublyLinkedListNode(result, None, None)
      next_result.addLast(dll_node)
    return next_result
  # step 4 -- possibly swap, partition dominator tree into subtrees, compute auxiliary graph for each subtree, count ordinary vertices in each auxiliary graph, possibly recurse on each created auxiliary graph; 
  # choose graph with more special bridges left; 
  # partition chosen graph's dominator tree; 
  # count number of ordinary nodes for each subtree and ignore if number is lower than two; 
  # create auxiliary graphs for each subtree, 
  # add ordinary nodes and edges, 
  # add two kinds of bridge-related local auxiliary nodes and local auxiliary edges, 
  # add three kinds of shortcut-related local auxiliary edges; 
  # recurse for auxiliary graphs that we do not throw away; 
  # mark the dominator tree nodes s.t. bridge destination has dominator that is bridge origin and we mark bridge destination
  t1._setPreorderNumbers()
  t1._setNumberOfDescendants()
  t2._setPreorderNumbers()
  t2._setNumberOfDescendants()
  use_forward = None
  if b_count1 >= b_count2:
    use_forward = True
  elif b_count2 > b_count1:
    use_forward = False
  source_subtree = None
  source_comp_subtree = None
  source_V = None
  source_E = None
  source_bridges = None
  source_G = None
  if use_forward == True:
    # forward direction
    source_subtree = t1
    source_V = V
    source_E = E
    source_bridges = next_bridges1
    source_G = g1
  elif use_forward == False:
    # reverse direction
    source_subtree = t2
    source_V = next_V
    source_E = next_E
    source_bridges = next_bridges2
    source_G = g2
  if True:
    for bridge in source_bridges:
      curr_g_dest = bridge.getDestination()
      curr_t_dest = source_subtree.getVertexByName(curr_g_dest.getName())
      curr_t_dest.mark()
    augmented_subtree_node_groups = source_subtree.getAugmentedSubtreeNodeGroups()
    # we never actually explicitly create trees for the subtrees created after cutting up dominator tree; 
    # place all old features in graphs without considering how to add more nodes and edges 
    # and we note that old does not mean all ordinary necessarily; 
    # in preparation for shortcut-related cases a and b, we relate ordinary node to subtree and then relate subtree to edge (i.e. via origin for case a or via destination for case b)
    subtree_root_name_to_case_a_edges_dict = defaultdict(lambda: [])
    subtree_root_name_to_case_b_edges_dict = defaultdict(lambda: [])
    ord_node_name_to_subtree_root_name_dict = {}
    for subtree_root, subtree_node_group in augmented_subtree_node_groups:
      for curr_node in subtree_node_group:
        # this is a little redundant because we haven't added local local auxiliary nodes yet
        if curr_node.isLocalOrdinary() == False:
          continue
        curr_name = curr_node.getName()
        ord_node_name_to_subtree_root_name_dict[curr_name] = subtree_root.getName()
    for edge in source_E:
      origin = edge.getOrigin()
      dest = edge.getDestination()
      origin_name = origin.getName()
      dest_name = dest.getName()
      if origin_name in ord_node_name_to_subtree_root_name_dict:
        subtree_root_name1 = ord_node_name_to_subtree_root_name_dict[origin_name]
        subtree_root_name_to_case_a_edges_dict[subtree_root_name1].append(edge)
      if dest_name in ord_node_name_to_subtree_root_name_dict:
        subtree_root_name2 = ord_node_name_to_subtree_root_name_dict[dest_name]
        subtree_root_name_to_case_b_edges_dict[subtree_root_name2].append(edge)
    # we start to handle auxiliary graphs; 
    # WE START TO HANDLE BASE NODES
    augmented_subtree_graphs = []
    for subtree_root, subtree_node_group in augmented_subtree_node_groups:
      curr_subtree_G = AOGraph()
      # handle base nodes -- i.e. we clone
      next_subtree_node_group = []
      for curr_node in subtree_node_group:
        next_node = AOVertex(curr_node.getName())
        # propagate kind
        if curr_node.isOverallOrdinary() == True:
          next_node.setIsOverallOrdinary()
        elif curr_node.isOverallAuxiliary() == True:
          next_node.setIsOverallAuxiliary()
        next_node.setIsLocalOrdinary()
        next_subtree_node_group.append(next_node)
      curr_subtree_G.addVertices(next_subtree_node_group)
      augmented_subtree_graphs.append((subtree_root, curr_subtree_G, subtree_node_group))
    # accumulate base edges s.t. we assign each to at most one output auxiliary graph
    subtree_graph_to_base_edges_dict = defaultdict(lambda: [])
    local_ordinary_node_name_to_auxiliary_graph_dict = {}
    for subtree_root, curr_subtree_G, subtree_node_group in augmented_subtree_graphs:
      for node in subtree_node_group:
        # this is possibly redundant
        if node.isLocalOrdinary() == True:
          local_ordinary_node_name_to_auxiliary_graph_dict[node.getName()] = curr_subtree_G
    for edge in source_E:
      origin = edge.getOrigin()
      dest = edge.getDestination()
      origin_name = origin.getName()
      dest_name = dest.getName()
      target_subtree_G1 = local_ordinary_node_name_to_auxiliary_graph_dict[origin_name]
      target_subtree_G2 = local_ordinary_node_name_to_auxiliary_graph_dict[dest_name]
      if target_subtree_G1 == target_subtree_G2:
        subtree_graph_to_base_edges_dict[target_subtree_G1].append(edge)
    # WE START TO HANDLE BASE EDGES
    for subtree_root, curr_subtree_G, subtree_node_group in augmented_subtree_graphs:
      # make sure to use names
      curr_edges = []
      node_name_is_present_dict = defaultdict(lambda: False)
      for node in subtree_node_group:
        node_name_is_present_dict[node.getName()] = True
      # handle base edges -- i.e. we clone
      for edge in subtree_graph_to_base_edges_dict[curr_subtree_G]:
        origin = edge.getOrigin()
        dest = edge.getDestination()
        if node_name_is_present_dict[origin.getName()] == True and node_name_is_present_dict[dest.getName()] == True:
          old_origin = edge.getOrigin()
          old_dest = edge.getDestination()
          next_origin = curr_subtree_G.getVertexByName(old_origin.getName())
          next_dest = curr_subtree_G.getVertexByName(old_dest.getName())
          # base edges are induced by pairs of ordinary nodes
          if next_origin.isLocalAuxiliary() == True or next_dest.isLocalAuxiliary() == True:
            continue
          curr_edge = AOEdge(next_origin, next_dest)
          # propagate kind
          curr_edge.setIsLocalOrdinary()
          curr_edges.append(curr_edge)
      curr_subtree_G.addEdges(curr_edges)
    # this is for shortcut local auxiliary edge cases
    source_subtree.doMarkBoundaryNodes()
    # this is in preparation for shortcut case b; 
    # check for each input edge before adding non-base nodes and edges 
    # that origin and destination are not in same subtree 
    # and that origin goes up to destination spatially; 
    # then, edge belongs to subtree containing destination
    auxiliary_subgraph_to_cs2_source_edges_dict = defaultdict(lambda: [])
    ord_node_name_to_subtree_root_name_dict = {}
    ord_node_name_to_auxiliary_subgraph_dict = {}
    for sr, csG, sng in augmented_subtree_graphs:
      for curr_node in sng:
        if curr_node.isLocalOrdinary() == True:
          curr_node_name = curr_node.getName()
          ord_node_name_to_auxiliary_subgraph_dict[curr_node_name] = csG
          ord_node_name_to_subtree_root_name_dict[curr_node_name] = sr.getName()
    for edge in source_E:
      origin = edge.getOrigin()
      dest = edge.getDestination()
      if dest.isLocalOrdinary() == False:
        continue
      dest_subgraph = ord_node_name_to_auxiliary_subgraph_dict[dest.getName()]
      if dest_subgraph.haveVertexWithName(origin.getName()) == True:
        continue
      dest_subtree_root_name = ord_node_name_to_subtree_root_name_dict[dest.getName()]
      sr_is_oriented = doStar(source_subtree.getVertexByName(dest_subtree_root_name), source_subtree.getVertexByName(origin.getName()))
      if sr_is_oriented == False:
        continue
      if dest.getName() == origin.getName():
        continue
      auxiliary_subgraph_to_cs2_source_edges_dict[dest_subgraph].append(edge)
    for subtree_root, curr_subtree_G, subtree_node_group in augmented_subtree_graphs:
      base_edges = curr_subtree_G.getEdges()[ : ]
      shiny_edges = []
      # (handle bridge-related local auxiliary nodes and edges)
      # bridge-related nodes and edges case one
      # (any cloning we do except for base nodes and edges we automatically consider arbitrarily to be local auxiliary)
      cb1_nodes = []
      cb1_edges = []
      # we need nodes that are children of boundary nodes, not just children of any node; this makes a difference
      for curr_node in [x for x in subtree_node_group if x.isBoundary() == True]:
        children = curr_node.getChildren()
        for child in children:
          if child.isMarked() == True:
            next_child = AOVertex(child.getName())
            next_child.setIsOverallAuxiliary()
            next_child.setIsLocalAuxiliary()
            next_curr_node = curr_subtree_G.getVertexByName(curr_node.getName())
            cb1_nodes.append(next_child)
            curr_edge = AOEdge(next_curr_node, next_child)
            curr_edge.setIsLocalAuxiliary()
            cb1_edges.append(curr_edge)
      curr_subtree_G.addVertices(cb1_nodes)
      shiny_edges.extend(cb1_edges)
      # bridge-related nodes and edges case two
      cb2_nodes = []
      cb2_edges = []
      curr_root = curr_subtree_G.getVertexByName(subtree_root.getName())
      if subtree_root.isMarked() == True and subtree_root != source_subtree.getRoot():
        dominator_t_node = subtree_root.getParent()
        next_dominator_t_node = AOVertex(dominator_t_node.getName())
        next_dominator_t_node.setIsOverallAuxiliary()
        next_dominator_t_node.setIsLocalAuxiliary()
        cb2_nodes.append(next_dominator_t_node)
        curr_edge = AOEdge(next_dominator_t_node, curr_root)
        curr_edge.setIsLocalAuxiliary()
        cb2_edges.append(curr_edge)
      curr_subtree_G.addVertices(cb2_nodes)
      shiny_edges.extend(cb2_edges)
      # shortcut-related nodes and edges case a
      cs1_edges = []
      # implicit detail
      if subtree_root != source_subtree.getRoot():
        curr_root = curr_subtree_G.getVertexByName(subtree_root.getName())
        for edge in subtree_root_name_to_case_a_edges_dict[subtree_root.getName()]:
          old_origin = edge.getOrigin()
          old_dest = edge.getDestination()
          # remember that u must be in same subtree, 
          # which is important if edge collection we are iterating over 
          # is not totally properly winnowed down
          old_dominator = subtree_root.getParent()
          next_origin = curr_subtree_G.getVertexByName(old_origin.getName())
          next_dominator = curr_subtree_G.getVertexByName(old_dominator.getName())
          dt_subtree_root = source_subtree.getVertexByName(subtree_root.getName())
          dt_dest = source_subtree.getVertexByName(old_dest.getName())
          if curr_subtree_G.getVertexByName(old_origin.getName()).isLocalOrdinary() == True:
            # check if dest. is not reachable as a non-proper descendant of curr. root
            if doStar(dt_subtree_root, dt_dest) == False:
              curr_edge = AOEdge(next_origin, next_dominator)
              curr_edge.setIsLocalAuxiliary()
              cs1_edges.append(curr_edge)
        shiny_edges.extend(cs1_edges)
      # shortcut-related nodes and edges case b
      boundary_nodes_in_subtree = [x for x in subtree_node_group if x.isBoundary() == True]
      # first find all edges with origin that is proper descendant of a boundary vertex in dominator tree s.t. destination is ordinary and in current subtree
      source_edge_candidates = []
      for edge in auxiliary_subgraph_to_cs2_source_edges_dict[curr_subtree_G]:
        old_origin = edge.getOrigin()
        old_dest = edge.getDestination()
        next_origin = source_subtree.getVertexByName(old_origin.getName())
        if True:
          if curr_subtree_G.haveVertexWithName(old_dest.getName()) == True:
            if curr_subtree_G.getVertexByName(old_dest.getName()).isLocalOrdinary() == True:
              source_edge_candidates.append(edge)
      # source_edge_candidates is our B_r; 
      # we are prepared to determine shortcut-related case b edge
      source_edge_candidates_sorted = bucketSort(source_edge_candidates, 1, len(source_V), lambda x: source_subtree.getVertexByName(x.getOrigin().getName()).getPreorderNumber())
      # this is for (B_r)'; this has to be for us to collect nodes from current subtree
      children_of_boundary_vertices = DSTree.getChildrenOfBoundaryVertices(subtree_node_group)
      children_of_boundary_vertices_sorted = bucketSort(children_of_boundary_vertices, 1, len(source_V), lambda x: source_subtree.getVertexByName(x.getName()).getPreorderNumber())
      # s.e.c.'s is source edge candidates
      augmented_secs = [(x, source_subtree.getVertexByName(x.getOrigin().getName()).getPreorderNumber()) for x in source_edge_candidates_sorted]
      # c.o.b.v.'s is children of boundary vertices
      augmented_cobvs = [(x, source_subtree.getVertexByName(x.getName()).getPreorderNumber()) for x in children_of_boundary_vertices_sorted]
      cs2_result = doShortcutEdgeCaseBSelectZ(augmented_secs, augmented_cobvs)
      cs2_edges = []
      for i in xrange(len(source_edge_candidates_sorted)):
        source_edge = source_edge_candidates_sorted[i]
        z_vertex = cs2_result[i]
        # have invalid z vertex
        if z_vertex == None:
          continue
        # we must remember whether origin replacement is in curr. auxiliary graph
        source_origin = source_edge.getOrigin()
        source_dest = source_edge.getDestination()
        next_origin = curr_subtree_G.getVertexByName(z_vertex.getName())
        next_dest = curr_subtree_G.getVertexByName(source_dest.getName())
        curr_edge = AOEdge(next_origin, next_dest)
        curr_edge.setIsLocalAuxiliary()
        cs2_edges.append(curr_edge)
      shiny_edges.extend(cs2_edges)
      seen_edge_str_set = set([x.toString() for x in base_edges])
      next_shiny_edges = []
      for edge in shiny_edges:
        if edge.toString() not in seen_edge_str_set:
          next_shiny_edges.append(edge)
          seen_edge_str_set |= set([edge.toString()])
      curr_subtree_G.addEdges(next_shiny_edges)
    # shortcut-related nodes and edges case c
    # (we indeed have many clones of case c edges across auxiliary graphs for same layer, possibly; 
    # the restriction is how destination interacts with subtree root)
    # (we assume r is not dominator tree root)
    # (we assume no self-edges)
    # (we construct a compressed dominator tree)
    # this name is shared by forward and reverse directions
    source_comp_subtree = source_subtree.getCompressedTree()
    curr_edges = []
    for edge in source_E:
      old_origin = edge.getOrigin()
      old_dest = edge.getDestination()
      dt_origin = source_subtree.getVertexByName(old_origin.getName())
      dt_dest = source_subtree.getVertexByName(old_dest.getName())
      dt_subtree_root = source_subtree.getVertexByName(subtree_root.getName())
      if True:
        if doStar(dt_subtree_root, dt_dest) == False:
          curr_edges.append(edge)
    # this is for shortcut case c step 1/3
    node_name_to_subtree_root_dict = defaultdict(lambda: [])
    for sr, csG, sng in augmented_subtree_graphs:
      for curr_node in sng:
        curr_node_name = curr_node.getName()
        node_name_to_subtree_root_dict[curr_node_name].append(sr)
    # this is also for shortcut case c step 1/3
    root_name_to_subtree_graph_dict = {}
    # this introduced an error because we need to avoid overwriting curr_subtree_G
    for sr, csG, sng in augmented_subtree_graphs:
      # we distinguish between subtree and currently-being-constructed auxiliary graph
      root_name_to_subtree_graph_dict[sr.getName()] = csG
    source_comp_subtree.determineLabelValues(curr_edges, root_name_to_subtree_graph_dict, source_subtree, node_name_to_subtree_root_dict)
    source_comp_subtree.determineLowValues()
    for subtree_root, curr_subtree_G, subtree_node_group in augmented_subtree_graphs:
      shiny_edges = []
      cs3_edges = DSTree.collectShortcutCaseCEdges(source_comp_subtree, source_subtree, subtree_node_group, curr_subtree_G, subtree_root)
      shiny_edges.extend(cs3_edges)
      # we have to remember to look up label and low values using compressed dominator tree
      seen_edge_str_set = set([x.toString() for x in curr_subtree_G.getEdges()])
      next_shiny_edges = []
      for edge in shiny_edges:
        if edge.toString() not in seen_edge_str_set:
          next_shiny_edges.append(edge)
          seen_edge_str_set |= set([edge.toString()])
      curr_subtree_G.addEdges(next_shiny_edges)
  subtree_graphs = [x[1] for x in augmented_subtree_graphs]
  results = [doRec2ECBHelper(x.getVertices(), x.getEdges()) for x in subtree_graphs]
  if len(results) == 0:
    raise Exception()
  else:
    curr_result = DoublyLinkedList()
    for result in results:
      curr_result = DoublyLinkedList.concatenate(curr_result, result)
    return curr_result
  return result

def doSimple2ECB(V, E):
  # step one
  s = V[0]
  strong_bridges = doStrongBridges(V, E, s)
  # step two
  curr_blocks = [V[ : ]]
  # step three
  n = len(V)
  g_vertex_to_number_dict = {}
  number_to_g_vertex_dict = {}
  for i in xrange(len(V)):
    g_vertex = V[i]
    g_vertex_to_number_dict[g_vertex] = i
    number_to_g_vertex_dict[i] = g_vertex
  for curr_sb in strong_bridges:
    # step 3.1
    active_edges = [x for x in E if x != curr_sb]
    adj = defaultdict(lambda: [])
    for g_edge in active_edges:
      origin = g_edge.getOrigin()
      destination = g_edge.getDestination()
      origin_num = g_vertex_to_number_dict[origin]
      destination_num = g_vertex_to_number_dict[destination]
      adj[origin_num].append(destination_num)
    scc_ks = SCC_KS(n, adj)
    components = scc_ks.scc()
    next_components = []
    for component in components:
      next_component = [number_to_g_vertex_dict[x] for x in component]
      next_components.append(next_component)
    # step 3.2
    next_blocks = []
    for curr_2ecb in curr_blocks:
      for curr_scc in next_components:
        # do intersection
        intersection_vertex_list = list(set(curr_2ecb) & set(curr_scc))
        if len(intersection_vertex_list) != 0:
          next_blocks.append(intersection_vertex_list)
    curr_blocks = next_blocks
  return curr_blocks

if __name__ == '__main__':

  """

  # for lax boolean MM

  L0 = AOVertex(1)
  L1 = AOVertex(2)
  L2 = AOVertex(3)
  M0 = AOVertex(4)
  M1 = AOVertex(5)
  M2 = AOVertex(6)
  R0 = AOVertex(7)
  R1 = AOVertex(8)
  R2 = AOVertex(9)
  v_MC = AOVertex(10)
  v_MS = AOVertex(11)
  v_B = AOVertex(12)
  v_SC = AOVertex(13)
  v_SS = AOVertex(14)
  v_UT = AOVertex(15)
  v_LT = AOVertex(16)

  vertices = [L0, L1, L2, M0, M1, M2, R0, R1, R2, v_MC, v_MS, v_B, v_SC, v_SS, v_UT, v_LT]

  for vertex in vertices:
    vertex.setIsOrdinary()

  e1 = AOEdge(L0, v_MS)
  e2 = AOEdge(L1, v_MS)
  e3 = AOEdge(L2, v_MS)
  e4 = AOEdge(M0, L0)
  e5 = AOEdge(M0, L1)
  e6 = AOEdge(M1, L0)
  e7 = AOEdge(M1, L1)
  e8 = AOEdge(M1, L2)
  e9 = AOEdge(R0, M1)
  e10 = AOEdge(R1, M0)
  e11 = AOEdge(R1, M1)
  e12 = AOEdge(R1, M2)
  e13 = AOEdge(v_MC, R0)
  e14 = AOEdge(v_MC, R1)
  e15 = AOEdge(v_MC, R2)
  e16 = AOEdge(v_MS, v_B)
  e17 = AOEdge(v_B, v_MC)
  e18 = AOEdge(L0, v_SS)
  e19 = AOEdge(L1, v_SS)
  e20 = AOEdge(L2, v_SS)
  e21 = AOEdge(v_LT, L0)
  e22 = AOEdge(v_LT, L1)
  e23 = AOEdge(v_LT, L2)
  e24 = AOEdge(M0, v_LT)
  e25 = AOEdge(M1, v_LT)
  e26 = AOEdge(M2, v_LT)
  e27 = AOEdge(v_UT, M0)
  e28 = AOEdge(v_UT, M1)
  e29 = AOEdge(v_UT, M2)
  e30 = AOEdge(R0, v_UT)
  e31 = AOEdge(R1, v_UT)
  e32 = AOEdge(R2, v_UT)
  e33 = AOEdge(v_SC, R0)
  e34 = AOEdge(v_SC, R1)
  e35 = AOEdge(v_SC, R2)
  e36 = AOEdge(v_SS, v_B)
  e37 = AOEdge(v_B, v_SC)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29, e30, e31, e32, e33, e34, e35, e36, e37]

  """

  # for lax boolean MM

  v_S = AOVertex("S")
  v_A = AOVertex("A")
  v_B = AOVertex("B")
  v_C = AOVertex("C")
  v_D = AOVertex("D")
  v_E = AOVertex("E")
  v_F = AOVertex("F")
  v_G = AOVertex("G")
  v_H = AOVertex("H")
  v_I = AOVertex("I")
  v_J = AOVertex("J")
  v_K = AOVertex("K")
  v_L = AOVertex("L")
  v_M = AOVertex("M")
  v_N = AOVertex("N")

  vertices = [v_S, v_A, v_B, v_C, v_D, v_E, v_F, v_G, v_H, v_I, v_J, v_K, v_L, v_M, v_N]

  for vertex in vertices:
    vertex.setIsOverallOrdinary()
    vertex.setIsLocalOrdinary()

  e1 = AOEdge(v_S, v_A)
  e2 = AOEdge(v_S, v_B)
  e3 = AOEdge(v_A, v_S)
  e4 = AOEdge(v_A, v_C)
  e5 = AOEdge(v_A, v_D)
  e6 = AOEdge(v_B, v_A)
  e7 = AOEdge(v_C, v_D)
  e8 = AOEdge(v_D, v_E)
  e9 = AOEdge(v_E, v_F)
  e10 = AOEdge(v_E, v_H)
  e11 = AOEdge(v_F, v_G)
  e12 = AOEdge(v_F, v_I)
  e13 = AOEdge(v_G, v_E)
  e14 = AOEdge(v_G, v_J)
  e15 = AOEdge(v_G, v_K)
  e16 = AOEdge(v_H, v_G)
  e17 = AOEdge(v_I, v_G)
  e18 = AOEdge(v_J, v_K)
  e19 = AOEdge(v_K, v_H)
  e20 = AOEdge(v_K, v_J)
  e21 = AOEdge(v_K, v_L)
  e22 = AOEdge(v_L, v_M)
  e23 = AOEdge(v_L, v_N)
  e24 = AOEdge(v_M, v_F)
  e25 = AOEdge(v_M, v_N)
  e26 = AOEdge(v_N, v_B)
  e27 = AOEdge(v_N, v_M)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27]

  for edge in edges:
    edge.setIsLocalOrdinary()

  """

  # at one point, this input leads to infinite loop 
  # via an output auxiliary graph is identical to input graph

  v_L = AOVertex("L")
  v_N = AOVertex("N")
  v_M = AOVertex("M")
  v_K = AOVertex("K")

  vertices = [v_L, v_N, v_M, v_K]

  for vertex in vertices:
    vertex.setIsOrdinary()

  e1 = AOEdge(v_L, v_M)
  e2 = AOEdge(v_L, v_N)
  e3 = AOEdge(v_M, v_N)
  e4 = AOEdge(v_N, v_M)
  e5 = AOEdge(v_K, v_L)
  e6 = AOEdge(v_M, v_K)
  e7 = AOEdge(v_N, v_K)

  edges = [e1, e2, e3, e4, e5, e6, e7]

  for edge in edges:
    edge.setIsOrdinary()

  """

  """

  # we need to separate M and N; we could have error if we have too many edges; 
  # we have one bridge-related case two edge and two shortcut-related case a edges; 
  # these last two edges are inappropriate and it is a bug that we have them

  v_L = AOVertex("L")
  v_N = AOVertex("N")
  v_M = AOVertex("M")
  v_K = AOVertex("K") # auxiliary
  v_B = AOVertex("B") # auxiliary

  vertices = [v_L, v_N, v_M, v_K, v_B]

  for vertex in vertices:
    vertex.setIsOrdinary()

  v_K.setIsAuxiliary()
  v_B.setIsAuxiliary()

  e1 = AOEdge(v_L, v_M)
  e2 = AOEdge(v_L, v_N)
  e3 = AOEdge(v_M, v_N)
  e4 = AOEdge(v_N, v_M)
  e5 = AOEdge(v_K, v_L) # bridge-related case two
  e6 = AOEdge(v_N, v_B) # shortcut-related case a
  e7 = AOEdge(v_M, v_K) # shortcut-related case a
  e8 = AOEdge(v_B, v_K) # shortcut-related case a

  e1 = AOEdge(v_M, v_L)
  e2 = AOEdge(v_N, v_L)
  e3 = AOEdge(v_N, v_M)
  e4 = AOEdge(v_M, v_N)
  e5 = AOEdge(v_L, v_K) # bridge-related case two
  e6 = AOEdge(v_B, v_N) # shortcut-related case a
  e7 = AOEdge(v_K, v_M) # shortcut-related case a
  e8 = AOEdge(v_K, v_B) # shortcut-related case a

  edges = [e1, e2, e3, e4, e5, e6, e7, e8]

  for edge in edges:
    edge.setIsOrdinary()

  """

  """

  # example from figure one in georgiadis et al. 2014

  v_A = AOVertex("A")
  v_B = AOVertex("B")
  v_C = AOVertex("C")
  v_D = AOVertex("D")
  v_E = AOVertex("E")
  v_F = AOVertex("F")
  v_H = AOVertex("H")
  v_I = AOVertex("I")
  v_J = AOVertex("J")

  vertices = [v_A, v_B, v_C, v_D, v_E, v_F, v_H, v_I, v_J]

  for vertex in vertices:
    vertex.setIsOrdinary()

  e1 = AOEdge(v_A, v_B)
  e2 = AOEdge(v_B, v_A)
  e3 = AOEdge(v_B, v_E)
  e4 = AOEdge(v_C, v_A)
  e5 = AOEdge(v_C, v_B)
  e6 = AOEdge(v_C, v_D)
  e7 = AOEdge(v_C, v_E)
  e8 = AOEdge(v_D, v_C)
  e9 = AOEdge(v_D, v_E)
  e10 = AOEdge(v_E, v_C)
  e11 = AOEdge(v_E, v_D)
  e12 = AOEdge(v_E, v_J)
  e13 = AOEdge(v_E, v_I)
  e14 = AOEdge(v_F, v_D)
  e15 = AOEdge(v_F, v_J)
  e16 = AOEdge(v_H, v_F)
  e17 = AOEdge(v_H, v_I)
  e18 = AOEdge(v_I, v_E)
  e19 = AOEdge(v_I, v_H)
  e20 = AOEdge(v_I, v_J)
  e21 = AOEdge(v_J, v_E)
  e22 = AOEdge(v_J, v_F)
  e23 = AOEdge(v_J, v_I)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23]

  for edge in edges:
    edge.setIsOrdinary()

  """

  """

  # example from figure two in georgiadis et al. 2014

  v1 = AOVertex(1)
  v2 = AOVertex(2)
  v3 = AOVertex(3)
  v4 = AOVertex(4)
  v5 = AOVertex(5)
  v6 = AOVertex(6)
  v7 = AOVertex(7)
  v8 = AOVertex(8)

  vertices = [v1, v2, v3, v4, v5, v6, v7, v8]

  for vertex in vertices:
    vertex.setIsOrdinary()

  e1 = AOEdge(v1, v2)
  e2 = AOEdge(v1, v3)
  e3 = AOEdge(v2, v5)
  e4 = AOEdge(v3, v5)
  e5 = AOEdge(v4, v1)
  e6 = AOEdge(v5, v1)
  e7 = AOEdge(v5, v4)
  e8 = AOEdge(v5, v6)
  e9 = AOEdge(v5, v7)
  e10 = AOEdge(v5, v8)
  e11 = AOEdge(v6, v5)
  e12 = AOEdge(v6, v7)
  e13 = AOEdge(v7, v5)
  e14 = AOEdge(v7, v8)
  e15 = AOEdge(v8, v5)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]

  for edge in edges:
    edge.setIsOrdinary()

  """

  blocks = doRec2ECB(vertices, edges)

  for i in xrange(len(blocks)):
    block = blocks[i]
    print "block", i, ":", [x.toString() for x in block]


