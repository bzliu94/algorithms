# 2019-08-04

# now is linear-time via gabow-tarjan DSU

# 2019-07-29

# we remember that we are assuming nodes that do not appear explicitly 
# in a block for output are effectively in their own output block; 
# this presumably happens either because of keeping the core algorithm 
# simple or efficient

# for reverse layer, need to use a specific start node

# 2019-06-27

# had typo s.t. we had curr_cobv, but it should be curr_C3_node; fix shortcut case a because of typo s.t. we had curr_aux_graph and we need curr_aux_G; we should remove self-edges via shortcut case b extended; we need to extend from forward direction to reverse direction; simplevrb needs to use names instead of node objects; removed pass statements; fixed simplevrb-like third layer check to be more relaxed for node status

# 2019-06-26

# most recent action is to base aux. graph construction 
# for reverse direction based on forward direction via copy and paste

# we implement fastvrb from georgiadis et al. 2015

# running time is O((m + n) * alpha), assuming use of standard DSU structure

from fgib_tarjan import Graph, Vertex, Edge, Tree, TreeVertex, TreeEdge, doStar
from sap_italiano import doStrongArticulationPoints
from scc_ks import SCC_KS
from sb_italiano import ReversedEdge
from collections import defaultdict
# from dt_fraczak_GD2_faster import GD
from dt_fraczak_GD2_fastest import GD

# from simplevrb_georgiadis import doSimpleVRB

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

OVERALL_ORDINARY_VERTEX = 0
OVERALL_AUXILIARY_VERTEX = 1

LOCAL_ORDINARY_VERTEX = 0
LOCAL_AUXILIARY_VERTEX = 1

LOCAL_ORDINARY_EDGE = 0
LOCAL_AUXILIARY_EDGE = 1

class DTree(Tree):
  def __init__(self):
    Tree.__init__(self)
  def determineLowValues(self):
    root = self.getRoot()
    root._determineLowValues(True)
  @staticmethod
  # dt_curr_aux_G_root is current auxiliary graph's r node s.t. it is a dominator tree node; 
  # r_node is that node, but for curr. auxiliary graph
  def collectShortcutCaseBEdges(dt, C3, candidate_edges, dt_curr_aux_G_root, r_node, curr_aux_G):
    edges = []
    for w in C3:
      next_w = curr_aux_G.getVertexByName(w.getName())
      # check that low(w) is < pre(r); i.e. low(w) is < pre(dt_curr_aux_G_root)
      if w.getLow() < dt_curr_aux_G_root.getPreorderNumber():
        curr_edge = AOEdge(next_w, r_node)
        curr_edge.setIsLocalAuxiliary()
        edges.append(curr_edge)
    return edges

class DTreeVertex(TreeVertex):
  def __init__(self, name):
    TreeVertex.__init__(self, name)
    self.overall_kind = None
    self.local_kind = None
    # for shortcut edge case b
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
  def setLabel(self, label):
    self.label = label
  def setLow(self, low):
    self.low = low
  def _determineLowValues(self, skip_curr_node = False):
    children = self.getChildren()
    for child in children:
      child._determineLowValues(False)
    candidate_low_values = [x.getLow() for x in children]
    if skip_curr_node == False:
      candidate_low_values.append(self.getLabel())
      curr_low_value = min(candidate_low_values)
      self.setLow(curr_low_value)

# if we do not have four non-proper ancestors, return less than four nodes
def getDTNodeFourNonproperAncestors(node):
  result = [node]
  if node.haveParent() == True:
    parent = node.getParent()
    result.append(parent)
    if parent.haveParent() == True:
      grandparent = parent.getParent()
      result.append(grandparent)
      if grandparent.haveParent() == True:
        grandgrandparent = grandparent.getParent()
        result.append(grandgrandparent)
  return result

"""

v1 = DTreeVertex(1)
v2 = DTreeVertex(2)
v3 = DTreeVertex(3)
v4 = DTreeVertex(4)
v5 = DTreeVertex(5)
v1.addChild(v2)
v2.addChild(v3)
v3.addChild(v4)
v4.addChild(v5)
v2.setParent(v1)
v3.setParent(v2)
v4.setParent(v3)
v5.setParent(v4)
print getDTNodeFourNonproperAncestors(v1)
print getDTNodeFourNonproperAncestors(v3)
print getDTNodeFourNonproperAncestors(v4)
print getDTNodeFourNonproperAncestors(v5)
raise Exception()

"""

class DTreeEdge(TreeEdge):
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
  # this is different w.r.t. fast2ecb
  def toString(self):
    return "(" + str(self.getOrigin().getName()) + ", " + str(self.getDestination().getName()) + ")"

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
    # for shortcut edge case b
    self.tag = None
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_EDGE
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_EDGE
  def getTag(self):
    return self.tag
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_EDGE
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_EDGE
  def setTag(self, tag):
    self.tag = tag
  # this is different w.r.t. fast2ecb
  def toString(self):
    return "(" + str(self.getOrigin().getName()) + ", " + str(self.getDestination().getName()) + ")"

class AOReversedEdge(ReversedEdge):
  def __init__(self, origin, destination, reference_edge):
    ReversedEdge.__init__(self, origin, destination, reference_edge)
    self.local_kind = None
    # for shortcut edge case b
    self.tag = None
  def isLocalOrdinary(self):
    return self.local_kind == LOCAL_ORDINARY_EDGE
  def isLocalAuxiliary(self):
    return self.local_kind == LOCAL_AUXILIARY_EDGE
  def getTag(self):
    return self.tag
  def setIsLocalOrdinary(self):
    self.local_kind = LOCAL_ORDINARY_EDGE
  def setIsLocalAuxiliary(self):
    self.local_kind = LOCAL_AUXILIARY_EDGE
  def setTag(self, tag):
    self.tag = tag
  # this is different w.r.t. fast2ecb
  def toString(self):
    return "(" + str(self.getOrigin().getName()) + ", " + str(self.getDestination().getName()) + ")"

def collectFourLayersUsingDTree(root_node):
  layer0 = []
  layer1 = []
  layer2 = []
  layer3 = []
  collectFourLayersUsingDTreeHelper(root_node, 0, layer0, layer1, layer2, layer3)
  result = [layer0, layer1, layer2, layer3]
  return result

# layer numbers are in [0, 3]
def collectFourLayersUsingDTreeHelper(curr_node, curr_layer_num, layer0, layer1, layer2, layer3):
  if curr_layer_num >= 0 and curr_layer_num <= 3:
    next_layer_num = curr_layer_num + 1
    curr_layer = None
    if curr_layer_num == 0:
      curr_layer = layer0
    elif curr_layer_num == 1:
      curr_layer = layer1
    elif curr_layer_num == 2:
      curr_layer = layer2
    elif curr_layer_num == 3:
      curr_layer = layer3
    curr_layer.append(curr_node)
    children = curr_node.getChildren()
    for child in children:
      collectFourLayersUsingDTreeHelper(child, next_layer_num, layer0, layer1, layer2, layer3)
  elif curr_layer_num > 3:
    return

"""

t1 = DTree()
v1 = DTreeVertex(1)
v2 = DTreeVertex(2)
v3 = DTreeVertex(3)
v4 = DTreeVertex(4)
v5 = DTreeVertex(5)
v6 = DTreeVertex(6)
v7 = DTreeVertex(7)
v8 = DTreeVertex(8)
v9 = DTreeVertex(9)
v10 = DTreeVertex(10)
v11 = DTreeVertex(11)
v12 = DTreeVertex(12)
t1.setRoot(v1)
v1.addChild(v2)
v1.addChild(v3)
v2.addChild(v4)
v3.addChild(v5)
v4.addChild(v6)
v4.addChild(v7)
v5.addChild(v8)
v6.addChild(v9)
v6.addChild(v10)
v8.addChild(v11)
v9.addChild(v12)

# expect result of [[2], [4], [6, 7], [9, 10]]
result = collectFourLayersUsingDTree(v2)

print [[x.getName() for x in y] for y in result]
raise Exception()

"""

"""

t1 = DTree()
v1 = DTreeVertex(1)
v2 = DTreeVertex(2)
v3 = DTreeVertex(3)
v4 = DTreeVertex(4)
v5 = DTreeVertex(5)
v6 = DTreeVertex(6)
v7 = DTreeVertex(7)
v8 = DTreeVertex(8)
v9 = DTreeVertex(9)
v10 = DTreeVertex(10)
v11 = DTreeVertex(11)
t1.setRoot(v1)
v1.addChild(v2)
v1.addChild(v3)
v2.addChild(v4)
v3.addChild(v5)
v4.addChild(v6)
v4.addChild(v7)
v5.addChild(v8)
v8.addChild(v10)
v9.addChild(v11)

# expect result of [[2], [4], [6, 7], []]
result = collectFourLayersUsingDTree(v2)

print [[x.getName() for x in y] for y in result]
raise Exception()

"""

# vertices must be dominator tree vertices for WBC to handle C1 aspect correctly
class WrappedBlock:
  counter = 0
  def __init__(self, vertices):
    self.vertices = vertices
    # self.oo_vertex_name_set = set([x.getName() for x in vertices if x.isOverallOrdinary() == True])
    self.id_num = WrappedBlock.counter
    WrappedBlock.counter += 1
  def _getID(self):
    return self.id_num
  def getVertices(self):
    return self.vertices
  # def getOOVertexNameSet(self):
  #   return self.oo_vertex_name_set

class WrappedBlockContainer:
  def __init__(self, forward_dominator_tree):
    self.forward_dominator_tree = forward_dominator_tree
    self.wrapped_blocks_set = set([])
    self.node_name_to_C1_wrapped_blocks_set_dict = defaultdict(lambda: set([]))
    self.node_name_C1_wrapped_block_tuple_commitment_count_dict = defaultdict(lambda: 0)
    self.node_name_to_wrapped_blocks_set_dict = defaultdict(lambda: set([]))
  def _getForwardDominatorTree(self):
    return self.forward_dominator_tree
  # takes time linear in number of wrapped_blocks
  def getWrappedBlocks(self):
    return list(self.wrapped_blocks_set)
  # takes constant time
  def getWrappedBlocksForC1WithVertexRootName(self, name):
    return list(self.node_name_to_C1_wrapped_blocks_set_dict[name])
  # takes constant time
  def getWrappedBlocksWithVertexName(self, name):
    return list(self.node_name_to_wrapped_blocks_set_dict[name])
  # takes time linear in size of wrapped block
  def removeWrappedBlock(self, wrapped_block):
    self.wrapped_blocks_set.remove(wrapped_block)
    for curr_node in wrapped_block.getVertices():
      curr_node_name = curr_node.getName()
      curr_dt_node = self._getForwardDominatorTree().getVertexByName(curr_node_name)
      if curr_dt_node.haveParent() == True:
        curr_node_parent = curr_dt_node.getParent()
        key = (curr_node_parent.getName(), wrapped_block)
        self.node_name_C1_wrapped_block_tuple_commitment_count_dict[key] -= 1
        if self.node_name_C1_wrapped_block_tuple_commitment_count_dict[key] <= 0:
          self.node_name_C1_wrapped_block_tuple_commitment_count_dict.pop(key)
          self.node_name_to_C1_wrapped_blocks_set_dict[curr_node_parent.getName()].remove(wrapped_block)
      self.node_name_to_wrapped_blocks_set_dict[curr_node_name].remove(wrapped_block)
  # takes time linear in size of wrapped block
  def addWrappedBlock(self, wrapped_block):
    self.wrapped_blocks_set.add(wrapped_block)
    for curr_node in wrapped_block.getVertices():
      curr_node_name = curr_node.getName()
      curr_dt_node = self._getForwardDominatorTree().getVertexByName(curr_node_name)
      if curr_dt_node.haveParent() == True:
        curr_node_parent = curr_dt_node.getParent()
        key = (curr_node_parent.getName(), wrapped_block)
        self.node_name_C1_wrapped_block_tuple_commitment_count_dict[key] += 1
        self.node_name_to_C1_wrapped_blocks_set_dict[curr_node_parent.getName()].add(wrapped_block)
      self.node_name_to_wrapped_blocks_set_dict[curr_node_name].add(wrapped_block)

def doFastVRB(V, E):
  wbc = doFastVRBForward(V, E)
  # we're not filtering
  result = []
  for wrapped_block in wbc.getWrappedBlocks():
    curr_vertices = wrapped_block.getVertices()
    result.append(curr_vertices)
  return result

def doFastVRBReverse(V, E, wbc, start_name):
  # reverse the graph
  # this is for debugging
  # s = [x for x in V if x.getName() == "r"][0]
  next_V = []
  for old_vertex in V:
    curr_vertex = AOVertex(old_vertex.getName())
    if old_vertex.isOverallOrdinary() == True:
      curr_vertex.setIsOverallOrdinary()
    elif old_vertex.isOverallAuxiliary() == True:
      curr_vertex.setIsOverallAuxiliary()
    curr_vertex.setIsLocalOrdinary()
    next_V.append(curr_vertex)
  name_to_next_vertex_dict = {}
  for vertex in next_V:
    name = vertex.getName()
    name_to_next_vertex_dict[name] = vertex
  s = name_to_next_vertex_dict[start_name]
  next_E = []
  for edge in E:
    curr_origin = edge.getOrigin()
    curr_destination = edge.getDestination()
    next_origin = name_to_next_vertex_dict[curr_origin.getName()]
    next_destination = name_to_next_vertex_dict[curr_destination.getName()]
    reversed_edge = AOReversedEdge(next_destination, next_origin, edge)
    reversed_edge.setIsLocalOrdinary()
    next_E.append(reversed_edge)
  next_s = name_to_next_vertex_dict[s.getName()]
  # step 3.1 - get reverse dominator tree
  name_to_old_vertex_dict = {}
  for vertex in V:
    name = vertex.getName()
    name_to_old_vertex_dict[name] = vertex
  dt_pairs2 = GD(next_V, next_E, next_s)
  dt2 = DTree()
  name_to_dt_vertex_dict = {}
  for curr_vertex in next_V:
    dt_vertex = DTreeVertex(curr_vertex.getName())
    dt_vertex.setIsOverallOrdinary()
    dt_vertex.setIsLocalOrdinary()
    name_to_dt_vertex_dict[curr_vertex.getName()] = dt_vertex
  s2 = name_to_dt_vertex_dict[next_s.getName()]
  dt2.setRoot(s2)
  dt_vertices2 = name_to_dt_vertex_dict.values()
  dt_edges2 = []
  for curr_child, curr_parent in dt_pairs2.items():
    next_child = name_to_dt_vertex_dict[curr_child.getName()]
    next_parent = name_to_dt_vertex_dict[curr_parent.getName()]
    next_parent.addChild(next_child)
    next_child.setParent(next_parent)
    dt_edge = DTreeEdge(next_child, next_parent)
    dt_edge.setIsLocalOrdinary()
    dt_edges2.append(dt_edge)
  dt2.addVertices(dt_vertices2)
  dt2.addEdges(dt_edges2)
  dt2._setPreorderNumbers()
  dt2._setNumberOfDescendants()
  # step 3.2
  all_wrapped_blocks = wbc.getWrappedBlocks()
  next_cursive_B = list(wbc.getWrappedBlocksForC1WithVertexRootName(s2.getName()))
  # step 3.3
  for wrapped_block in next_cursive_B:
    # this modifies without copying
    wbc.removeWrappedBlock(wrapped_block)
  # we only add pairs or labels if the node is part of some block; 
  # also, we consider each block separately so as to not erroneously pass threshold of output group size of at least two
  # pairs are of form (split_label_num, node name)
  for wrapped_block in next_cursive_B:
    all_pairs = []
    curr_non_dt_vertices = wrapped_block.getVertices()
    curr_vertices = []
    for curr_vertex in curr_non_dt_vertices:
      if dt2.haveVertexWithName(curr_vertex.getName()) == True:
        curr_vertices.append(dt2.getVertexByName(curr_vertex.getName()))
    for curr_vertex in curr_vertices:
      if curr_vertex.getName() == s2.getName():
        # only have one label instead of two
        label1 = curr_vertex.getPreorderNumber()
        pair1 = (label1, curr_vertex.getName())
        all_pairs.append(pair1)
      else:
        label1 = curr_vertex.getPreorderNumber()
        pair1 = (label1, curr_vertex.getName())
        node2 = curr_vertex.getParent()
        label2 = node2.getPreorderNumber()
        pair2 = (label2, curr_vertex.getName())
        all_pairs.append(pair1)
        all_pairs.append(pair2)
    replacement_wrapped_blocks = []
    label_to_node_names_dict = defaultdict(lambda: [])
    for curr_pair in all_pairs:
      curr_label, curr_node_name = curr_pair
      label_to_node_names_dict[curr_label].append(curr_node_name)
    for curr_item in label_to_node_names_dict.items():
      curr_label, curr_node_names = curr_item
      next_node_names = list(set(curr_node_names))
      if len(next_node_names) >= 2:
        curr_wrapped_block = WrappedBlock([dt2.getVertexByName(x) for x in next_node_names])
        replacement_wrapped_blocks.append(curr_wrapped_block)
    for curr_replacement_wrapped_block in replacement_wrapped_blocks:
      wbc.addWrappedBlock(curr_replacement_wrapped_block)
  # step 3.4
  # make auxiliary graphs
  # use groups based on reverse dominator tree
  auxiliary_graph_root_name_pair_list = []
  # this is for efficiently-determined base edges
  aux_graphs = []
  aux_graph_to_base_edge_sources_dict = defaultdict(lambda: [])
  # tuple is (C0, C1, C2, C3)
  aux_graph_to_C0_C1_C2_C3_tuple_dict = {}
  # tuple is (LO_node_names, LA_node_names)
  aux_graph_to_LO_node_names_LA_node_names_tuple_dict = {}
  aux_graph_to_root_dt_vertex_dict = {}
  # this is for efficiently-determined shortcut case a edges
  root_node_name_to_aux_graph_dict = {}
  aux_graph_to_source_edge_dest_names_dict = defaultdict(lambda: [])
  aux_graph_to_source_edges_dict = defaultdict(lambda: [])
  for ag_root_dt_vertex in dt_vertices2:
    curr_aux_G = AOGraph()
    is_G_s = None
    if ag_root_dt_vertex.getName() == next_s.getName():
      # C0 is local ordinary instead of local auxiliary
      is_G_s = True
    else:
      is_G_s = False
    C0, C1, C2, C3 = collectFourLayersUsingDTree(ag_root_dt_vertex)
    local_ordinary_nodes = None
    local_auxiliary_nodes = None
    if is_G_s == True:
      local_ordinary_nodes = C0 + C1 + C2
      local_auxiliary_nodes = C3
    else:
      local_ordinary_nodes = C1 + C2
      local_auxiliary_nodes = C0 + C3
    next_subtree_node_group = []
    for curr_node in local_ordinary_nodes:
      next_node = AOVertex(curr_node.getName())
      # propagate kind
      if curr_node.isOverallOrdinary() == True:
        next_node.setIsOverallOrdinary()
      elif curr_node.isOverallAuxiliary() == True:
        next_node.setisOverallAuxiliary()
      next_node.setIsLocalOrdinary()
      next_subtree_node_group.append(next_node)
    for curr_node in local_auxiliary_nodes:
      next_node = AOVertex(curr_node.getName())
      # propagate kind
      next_node.setIsOverallAuxiliary()
      next_node.setIsLocalAuxiliary()
      next_subtree_node_group.append(next_node)
    curr_aux_G.addVertices(next_subtree_node_group)
    LO_node_name_set = set([x.getName() for x in local_ordinary_nodes])
    LA_node_name_set = set([x.getName() for x in local_auxiliary_nodes])
    # V_r is union of local ordinary and local auxiliary nodes for an output auxiliary graph
    aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G] = (C0, C1, C2, C3)
    aux_graph_to_LO_node_names_LA_node_names_tuple_dict[curr_aux_G] = (LO_node_name_set, LA_node_name_set)
    aux_graph_to_root_dt_vertex_dict[curr_aux_G] = ag_root_dt_vertex
    aux_graphs.append(curr_aux_G)
    root_node_name_to_aux_graph_dict[ag_root_dt_vertex.getName()] = curr_aux_G
  # this is for efficiently-determined base edges
  node_name_to_aux_graphs_dict = defaultdict(lambda: [])
  for aux_graph in aux_graphs:
    curr_vertices = aux_graph.getVertices()
    for curr_vertex in curr_vertices:
      curr_name = curr_vertex.getName()
      node_name_to_aux_graphs_dict[curr_name].append(aux_graph)
  for edge in next_E:
    origin = edge.getOrigin()
    dest = edge.getDestination()
    origin_name = origin.getName()
    dest_name = dest.getName()
    origin_aux_graph_set = set(node_name_to_aux_graphs_dict[origin_name])
    dest_aux_graph_set = set(node_name_to_aux_graphs_dict[dest_name])
    target_aux_graphs = list(origin_aux_graph_set & dest_aux_graph_set)
    for target_aux_graph in target_aux_graphs:
      aux_graph_to_base_edge_sources_dict[target_aux_graph].append(edge)
  # this is for efficiently-determined shortcut case a edges; 
  # if each node belongs to at most one output auxiliary graph, 
  # visiting edges in chunks based on an endpoint takes time linear in number of edges; 
  # if each node belongs to at most four output auxiliary graphs, 
  # visiting nodes in chunks based on endpoint takes time linear in number of edges times four, which is linear again
  for node in next_V:
    next_node = dt2.getVertexByName(node.getName())
    non_proper_ancestors = getDTNodeFourNonproperAncestors(next_node)
    curr_aux_graphs = [root_node_name_to_aux_graph_dict[x.getName()] for x in non_proper_ancestors]
    # need to determine source edges for each output auxiliary graph by checking three conditions for each edge
    for curr_aux_graph in curr_aux_graphs:
      aux_graph_to_source_edge_dest_names_dict[curr_aux_graph].append(node.getName())
  dest_name_to_edges_dict = defaultdict(lambda: [])
  for edge in next_E:
    dest = edge.getDestination()
    dest_name = dest.getName()
    dest_name_to_edges_dict[dest_name].append(edge)
  # if dest. name groups are disjoint, we take linear time overall for visiting edges for shortcut case a
  for curr_aux_graph in aux_graphs:
    source_edge_dest_names = aux_graph_to_source_edge_dest_names_dict[curr_aux_graph]
    # we have already satisfied condition one (i.e. edge (u, v) has v in V_r); 
    # now, we need to satisfy conditions u is not in V_r and u is non-proper descendant of r for G_r
    for source_edge_dest_name in source_edge_dest_names:
      curr_source_edge_candidates = dest_name_to_edges_dict[source_edge_dest_name]
      for curr_source_edge_candidate in curr_source_edge_candidates:
        origin = curr_source_edge_candidate.getOrigin()
        curr_root_name = aux_graph_to_root_dt_vertex_dict[curr_aux_graph].getName()
        if curr_aux_graph.haveVertexWithName(origin.getName()) == True:
          continue
        if doStar(dt2.getVertexByName(curr_root_name), dt2.getVertexByName(origin.getName())) == False:
          continue
        aux_graph_to_source_edges_dict[curr_aux_graph].append(curr_source_edge_candidate)
  # these five dictionaries below are for shortcut case a
  aux_G_to_shiny_edges_dict = {}
  aux_G_to_input_sec_list_dict = {}
  aux_G_to_input_C3_node_list_dict = {}
  # output is expected to be sorted
  aux_G_to_output_sec_list_dict = defaultdict(lambda: [])
  # output is expected to be sorted
  aux_G_to_output_C3_node_list_dict = defaultdict(lambda: [])
  for curr_aux_G in aux_graphs:
    C0, C1, C2, C3 = aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G]
    LO_node_name_set, LA_node_name_set = aux_graph_to_LO_node_names_LA_node_names_tuple_dict[curr_aux_G]
    V_r_name_set = LO_node_name_set | LA_node_name_set
    ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
    # determine "base" edges that are local ordinary or local auxiliary depending on if both endpoints are local ordinary or not, resp.
    LO_edges = []
    base_LA_edges = []
    # this is used s.t. we later remove duplicate edges
    shiny_edges = []
    for edge in aux_graph_to_base_edge_sources_dict[curr_aux_G]:
      old_origin = edge.getOrigin()
      old_dest = edge.getDestination()
      if old_origin.getName() not in V_r_name_set or old_dest.getName() not in V_r_name_set:
        continue
      next_origin = curr_aux_G.getVertexByName(old_origin.getName())
      next_dest = curr_aux_G.getVertexByName(old_dest.getName())
      next_edge = AOEdge(next_origin, next_dest)
      if old_origin.getName() in LO_node_name_set and old_dest.getName() in LO_node_name_set:
        LO_edges.append(next_edge)
        next_edge.setIsLocalOrdinary()
      elif old_origin.getName() in V_r_name_set and old_dest.getName() in V_r_name_set:
        base_LA_edges.append(next_edge)
        next_edge.setIsLocalAuxiliary()
    shiny_edges.extend(LO_edges)
    shiny_edges.extend(base_LA_edges)
    # determine local auxiliary edges -- i.e. two types of shortcut edge
    # handle shortcut edge type a
    # create list B_r and create list (B_r)'
    # we must set pre-order numbers and number of descendants for forward dominator tree
    source_edge_candidates = []
    for curr_edge in aux_graph_to_source_edges_dict[curr_aux_G]:
      old_origin = curr_edge.getOrigin()
      old_dest = curr_edge.getDestination()
      dt2_next_origin = dt2.getVertexByName(old_origin.getName())
      # source edges for shortcut edge type a are: 
      # origin is not in our four layers, 
      # destination is in our four layers, 
      # origin is a non-proper descendant of root for current auxiliary graph
      if (old_origin.getName() not in V_r_name_set) and (old_dest.getName() in V_r_name_set) and (doStar(ag_root_dt_vertex, dt2_next_origin) == True):
        source_edge_candidates.append(curr_edge)
    aux_G_to_shiny_edges_dict[curr_aux_G] = shiny_edges
    aux_G_to_input_sec_list_dict[curr_aux_G] = source_edge_candidates
    aux_G_to_input_C3_node_list_dict[curr_aux_G] = C3
  # handle shortcut case a all at once via merge, bucket sort, unmerge
  combined_sec_list = []
  combined_C3_node_list = []
  sec_to_aux_graphs_dict = defaultdict(lambda: [])
  C3_node_to_aux_graphs_dict = defaultdict(lambda: [])
  for curr_aux_graph in aux_graphs:
    curr_sec_list = aux_G_to_input_sec_list_dict[curr_aux_graph]
    curr_C3_node_list = aux_G_to_input_C3_node_list_dict[curr_aux_graph]
    # we assume extend for operand with length k takes time O(k)
    combined_sec_list.extend(curr_sec_list)
    combined_C3_node_list.extend(curr_C3_node_list)
    for curr_sec in curr_sec_list:
      sec_to_aux_graphs_dict[curr_sec].append(curr_aux_graph)
    for curr_C3_node in curr_C3_node_list:
      C3_node_to_aux_graphs_dict[curr_C3_node].append(curr_aux_graph)
  sec_list_sorted = bucketSort(combined_sec_list, 1, len(next_V), lambda x: dt2.getVertexByName(x.getOrigin().getName()).getPreorderNumber())
  C3_node_list_sorted = bucketSort(combined_C3_node_list, 1, len(next_V), lambda x: dt2.getVertexByName(x.getName()).getPreorderNumber())
  for curr_sec in sec_list_sorted:
    curr_aux_graphs = sec_to_aux_graphs_dict[curr_sec]
    for curr_aux_G in curr_aux_graphs:
      aux_G_to_output_sec_list_dict[curr_aux_G].append(curr_sec)
  for curr_C3_node in C3_node_list_sorted:
    curr_aux_graphs = C3_node_to_aux_graphs_dict[curr_C3_node]
    for curr_aux_G in curr_aux_graphs:
      aux_G_to_output_C3_node_list_dict[curr_aux_G].append(curr_C3_node)
  aux_G_to_shiny_edges_again_dict = {}
  for curr_aux_G in aux_graphs:
    C0, C1, C2, C3 = aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G]
    ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
    source_edge_candidates_sorted = aux_G_to_output_sec_list_dict[curr_aux_G]
    # for (B_r)', have vertices in C^3
    second_list_sorted = aux_G_to_output_C3_node_list_dict[curr_aux_G]
    shiny_edges = aux_G_to_shiny_edges_dict[curr_aux_G]
    augmented_secs = [(x, dt2.getVertexByName(x.getOrigin().getName()).getPreorderNumber()) for x in source_edge_candidates_sorted]
    augmented_sls = [(x, dt2.getVertexByName(x.getName()).getPreorderNumber()) for x in second_list_sorted]
    cs1_result = doShortcutEdgeCaseBSelectZ(augmented_secs, augmented_sls)
    cs1_edges = []
    for i in xrange(len(source_edge_candidates_sorted)):
      source_edge = source_edge_candidates_sorted[i]
      z_vertex = cs1_result[i]
      # have invalid z vertex
      if z_vertex == None:
        continue
      # we must remember whether origin replacement is in curr. auxiliary graph
      source_origin = source_edge.getOrigin()
      source_dest = source_edge.getDestination()
      next_origin = curr_aux_G.getVertexByName(z_vertex.getName())
      next_dest = curr_aux_G.getVertexByName(source_dest.getName())
      curr_edge = AOEdge(next_origin, next_dest)
      curr_edge.setIsLocalAuxiliary()
      cs1_edges.append(curr_edge)
    shiny_edges.extend(cs1_edges)
    aux_G_to_shiny_edges_again_dict[curr_aux_G] = shiny_edges
  # handle shortcut edge type b
  # for each edge (u, v), u needs to be descendant of a C^3 vertex, 
  # v needs to be descendant of curr. aux. graph root r, 
  # use LCA of endpoint for an edge by having three O(1)-time checks for determining tag values t
  # details in fastvrb s.t. they do not exist in fast2ecb:
  # - have extra initial step of using tag values t
  # - don't use compressed dominator tree
  # - label l for a node is based on min. tag for edges (w, v) s.t. origin is that node
  # details in fastvrb s.t. they are also in fast2ecb:
  # - low values are determined for every node except root of dominator tree
  # - low is same
  # - deciding whether to add an edge is based on comparison between low number and pre-order number
  # this used to be inefficient
  for edge in next_E:
    # for edge (u, v): 
    # t(u, v) = pre(u) if u is ancestor of v in D(s)
    # t(u, v) = pre(v) if v is ancestor of u in D(s)
    # t(u, v) = pre(d(v)) otherwise
    t_value = None
    origin = edge.getOrigin()
    dest = edge.getDestination()
    node_u = dt2.getVertexByName(origin.getName())
    node_v = dt2.getVertexByName(dest.getName())
    if doStar(node_u, node_v) == True:
      t_value = node_u.getPreorderNumber()
    elif doStar(node_v, node_u) == True:
      t_value = node_v.getPreorderNumber()
    else:
      t_value = node_v.getParent().getPreorderNumber()
    edge.setTag(t_value)
  origin_name_to_edges_dict = defaultdict(lambda: [])
  for edge in next_E:
    origin = edge.getOrigin()
    origin_name = origin.getName()
    origin_name_to_edges_dict[origin_name].append(edge)
  for dt2_vertex in dt2.getVertices():
    if dt2_vertex.getName() == next_s.getName():
      continue
    tag_values = []
    # this used to be inefficient; we need to consider only edges with origin that is the current node
    for edge in origin_name_to_edges_dict[dt2_vertex.getName()]:
      origin = edge.getOrigin()
      dest = edge.getDestination()
      if origin.getName() == dt2_vertex.getName():
        tag_values.append(edge.getTag())
    min_tag_value = min(tag_values)
    # note that we are guaranteed to have at least one tag value
    dt2_vertex.setLabel(min_tag_value)
  node_name_to_aux_graph_dict = defaultdict(lambda: [])
  for curr_aux_G in aux_graphs:
    curr_vertices = curr_aux_G.getVertices()
    for curr_vertex in curr_vertices:
      curr_vertex_name = curr_vertex.getName()
      node_name_to_aux_graph_dict[curr_vertex_name].append(curr_aux_G)
  aux_graph_to_cs2b_edges_dict = defaultdict(lambda: [])
  # iterate over edges, take origin and iterate over output aux. graphs
  for edge in next_E:
    origin = edge.getOrigin()
    dest = edge.getDestination()
    # there was a bug here; we care about C0, C1, C2, C3, not just C1 and C2
    for curr_aux_G in node_name_to_aux_graph_dict[origin.getName()]:
      curr_ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
      r_node = curr_aux_G.getVertexByName(curr_ag_root_dt_vertex.getName())
      if doStar(curr_ag_root_dt_vertex, dt2.getVertexByName(dest.getName())) == False:
        # if edge is self-edge, ignore it
        next_origin = curr_aux_G.getVertexByName(origin.getName())
        if next_origin.getName() == r_node.getName():
          continue
        next_edge = AOEdge(next_origin, r_node)
        next_edge.setIsLocalAuxiliary()
        aux_graph_to_cs2b_edges_dict[curr_aux_G].append(next_edge)
  # found a bug here
  dt2.determineLowValues()
  for curr_aux_G in aux_graphs:
    C0, C1, C2, C3 = aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G]
    ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
    shiny_edges = aux_G_to_shiny_edges_again_dict[curr_aux_G]
    r_node = curr_aux_G.getVertexByName(ag_root_dt_vertex.getName())
    # found a bug here
    cs2_edges = DTree.collectShortcutCaseBEdges(dt2, C3, next_E, ag_root_dt_vertex, r_node, curr_aux_G)
    # by definition, G_s has no type-b shortcut edges; this was source of a bug
    if ag_root_dt_vertex.getName() != next_s.getName():
      shiny_edges.extend(cs2_edges)
    cs2b_edges = aux_graph_to_cs2b_edges_dict[curr_aux_G]
    # by definition, G_s has no type-b shortcut edges; this was source of a bug
    if ag_root_dt_vertex.getName() != next_s.getName():
      shiny_edges.extend(cs2b_edges)
    auxiliary_graph_root_name_pair_list.append((curr_aux_G, ag_root_dt_vertex.getName()))
    seen_edge_str_set = set([])
    next_shiny_edges = []
    for edge in shiny_edges:
      if edge.toString() not in seen_edge_str_set:
        next_shiny_edges.append(edge)
        seen_edge_str_set |= set([edge.toString()])
    curr_aux_G.addEdges(next_shiny_edges)
  # step 3.5 - process nodes in dominator tree (in any order)
  nodes = dt2.getPreorderNodes()
  root_name_to_aux_graph_dict = {}
  for aux_graph, root_name in auxiliary_graph_root_name_pair_list:
    root_name_to_aux_graph_dict[root_name] = aux_graph
  for curr_dt_node in nodes:
    aux_graph = root_name_to_aux_graph_dict[curr_dt_node.getName()]
    if curr_dt_node.haveChildren() == False:
      continue
    # this is mostly safe because name is what matters most; 
    # overall-ordinary status matters as well, which the replacement items excel at
    curr_result = doSimpleVRBModified(aux_graph.getVertices(), aux_graph.getEdges(), wbc, aux_graph.getVertexByName(curr_dt_node.getName()))
  return wbc

def doFastVRBForward(V, E):
  # important detail - across layers, we for each node (identified via name) maintain a collection of blocks that contain it
  # step 1 - choose start vertex, compute forward dominator tree, get initial blocks C-hat of v for each node v in dominator tree, make note of node elements for each block and make note of block collection for each node
  s = V[0]
  # this is for debugging
  # s = [x for x in V if x.getName() == "s"][0]
  dt_pairs1 = GD(V, E, s)
  dt1 = DTree()
  name_to_dt_vertex_dict = {}
  for curr_vertex in V:
    dt_vertex = DTreeVertex(curr_vertex.getName())
    dt_vertex.setIsOverallOrdinary()
    dt_vertex.setIsLocalOrdinary()
    name_to_dt_vertex_dict[curr_vertex.getName()] = dt_vertex
  s1 = name_to_dt_vertex_dict[s.getName()]
  dt1.setRoot(s1)
  dt_vertices1 = name_to_dt_vertex_dict.values()
  dt_edges1 = []
  for curr_child, curr_parent in dt_pairs1.items():
    next_child = name_to_dt_vertex_dict[curr_child.getName()]
    next_parent = name_to_dt_vertex_dict[curr_parent.getName()]
    next_parent.addChild(next_child)
    next_child.setParent(next_parent)
    dt_edge = DTreeEdge(next_child, next_parent)
    dt_edge.setIsLocalOrdinary()
    dt_edges1.append(dt_edge)
  dt1.addVertices(dt_vertices1)
  dt1.addEdges(dt_edges1)
  dt1._setPreorderNumbers()
  dt1._setNumberOfDescendants()
  root_node_name_to_C_hat_dict = {}
  for curr_node in dt_vertices1:
    # this is important; for forward layer, requiring that a C-hat's root node be not a leaf means it has at least two overall ordinary nodes for each initial block, which is important because a block may survive until end and not encounter simplevrb modified (i.e. layer three) call
    if curr_node.haveChildren() == False:
      continue
    children = curr_node.getChildren()
    curr_block = [curr_node]
    for child in children:
      curr_block.append(child)
    root_node_name_to_C_hat_dict[curr_node.getName()] = curr_block
  wbc = WrappedBlockContainer(dt1)
  for curr_C_hat in root_node_name_to_C_hat_dict.values():
    curr_wrapped_block = WrappedBlock(curr_C_hat)
    wbc.addWrappedBlock(curr_wrapped_block)
  # step 2 - create auxiliary graph G_r for each node r in forward dominator tree
  # (we note that initial blocks and auxiliary graphs are determined differently; 
  # the former has two layers and the latter has four layers 
  # s.t. middle two are ordinary and outer two are auxiliary)
  auxiliary_graph_root_name_pair_list = []
  # this is for efficiently-determined base edges
  aux_graphs = []
  aux_graph_to_base_edge_sources_dict = defaultdict(lambda: [])
  # tuple is (C0, C1, C2, C3)
  aux_graph_to_C0_C1_C2_C3_tuple_dict = {}
  # tuple is (LO_node_names, LA_node_names)
  aux_graph_to_LO_node_names_LA_node_names_tuple_dict = {}
  aux_graph_to_root_dt_vertex_dict = {}
  # this is for efficiently-determined shortcut case a edges
  root_node_name_to_aux_graph_dict = {}
  aux_graph_to_source_edge_dest_names_dict = defaultdict(lambda: [])
  aux_graph_to_source_edges_dict = defaultdict(lambda: [])
  for ag_root_dt_vertex in dt_vertices1:
    curr_aux_G = AOGraph()
    is_G_s = None
    if ag_root_dt_vertex.getName() == s.getName():
      # C0 is local ordinary instead of local auxiliary
      is_G_s = True
    else:
      is_G_s = False
    C0, C1, C2, C3 = collectFourLayersUsingDTree(ag_root_dt_vertex)
    local_ordinary_nodes = None
    local_auxiliary_nodes = None
    if is_G_s == True:
      local_ordinary_nodes = C0 + C1 + C2
      local_auxiliary_nodes = C3
    else:
      local_ordinary_nodes = C1 + C2
      local_auxiliary_nodes = C0 + C3
    next_subtree_node_group = []
    for curr_node in local_ordinary_nodes:
      next_node = AOVertex(curr_node.getName())
      # propagate kind
      if curr_node.isOverallOrdinary() == True:
        next_node.setIsOverallOrdinary()
      elif curr_node.isOverallAuxiliary() == True:
        next_node.setisOverallAuxiliary()
      next_node.setIsLocalOrdinary()
      next_subtree_node_group.append(next_node)
    for curr_node in local_auxiliary_nodes:
      next_node = AOVertex(curr_node.getName())
      # propagate kind
      next_node.setIsOverallAuxiliary()
      next_node.setIsLocalAuxiliary()
      next_subtree_node_group.append(next_node)
    curr_aux_G.addVertices(next_subtree_node_group)
    LO_node_name_set = set([x.getName() for x in local_ordinary_nodes])
    LA_node_name_set = set([x.getName() for x in local_auxiliary_nodes])
    # V_r is union of local ordinary and local auxiliary nodes for an output auxiliary graph
    aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G] = (C0, C1, C2, C3)
    aux_graph_to_LO_node_names_LA_node_names_tuple_dict[curr_aux_G] = (LO_node_name_set, LA_node_name_set)
    aux_graph_to_root_dt_vertex_dict[curr_aux_G] = ag_root_dt_vertex
    aux_graphs.append(curr_aux_G)
    root_node_name_to_aux_graph_dict[ag_root_dt_vertex.getName()] = curr_aux_G
  # this is for efficiently-determined base edges
  node_name_to_aux_graphs_dict = defaultdict(lambda: [])
  for aux_graph in aux_graphs:
    curr_vertices = aux_graph.getVertices()
    for curr_vertex in curr_vertices:
      curr_name = curr_vertex.getName()
      node_name_to_aux_graphs_dict[curr_name].append(aux_graph)
  for edge in E:
    origin = edge.getOrigin()
    dest = edge.getDestination()
    origin_name = origin.getName()
    dest_name = dest.getName()
    origin_aux_graph_set = set(node_name_to_aux_graphs_dict[origin_name])
    dest_aux_graph_set = set(node_name_to_aux_graphs_dict[dest_name])
    target_aux_graphs = list(origin_aux_graph_set & dest_aux_graph_set)
    for target_aux_graph in target_aux_graphs:
      aux_graph_to_base_edge_sources_dict[target_aux_graph].append(edge)
  # this is for efficiently-determined shortcut case a edges; 
  # if each node belongs to at most one output auxiliary graph, 
  # visiting edges in chunks based on an endpoint takes time linear in number of edges; 
  # if each node belongs to at most four output auxiliary graphs, 
  # visiting nodes in chunks based on endpoint takes time linear in number of edges times four, which is linear again
  for node in V:
    next_node = dt1.getVertexByName(node.getName())
    non_proper_ancestors = getDTNodeFourNonproperAncestors(next_node)
    curr_aux_graphs = [root_node_name_to_aux_graph_dict[x.getName()] for x in non_proper_ancestors]
    # need to determine source edges for each output auxiliary graph by checking three conditions for each edge
    for curr_aux_graph in curr_aux_graphs:
      aux_graph_to_source_edge_dest_names_dict[curr_aux_graph].append(node.getName())
  dest_name_to_edges_dict = defaultdict(lambda: [])
  for edge in E:
    dest = edge.getDestination()
    dest_name = dest.getName()
    dest_name_to_edges_dict[dest_name].append(edge)
  # if dest. name groups are disjoint, we take linear time overall for visiting edges for shortcut case a
  for curr_aux_graph in aux_graphs:
    source_edge_dest_names = aux_graph_to_source_edge_dest_names_dict[curr_aux_graph]
    # we have already satisfied condition one (i.e. edge (u, v) has v in V_r); 
    # now, we need to satisfy conditions u is not in V_r and u is non-proper descendant of r for G_r
    for source_edge_dest_name in source_edge_dest_names:
      curr_source_edge_candidates = dest_name_to_edges_dict[source_edge_dest_name]
      for curr_source_edge_candidate in curr_source_edge_candidates:
        origin = curr_source_edge_candidate.getOrigin()
        curr_root_name = aux_graph_to_root_dt_vertex_dict[curr_aux_graph].getName()
        if curr_aux_graph.haveVertexWithName(origin.getName()) == True:
          continue
        if doStar(dt1.getVertexByName(curr_root_name), dt1.getVertexByName(origin.getName())) == False:
          continue
        aux_graph_to_source_edges_dict[curr_aux_graph].append(curr_source_edge_candidate)
  # these five dictionaries below are for shortcut case a
  aux_G_to_shiny_edges_dict = {}
  aux_G_to_input_sec_list_dict = {}
  aux_G_to_input_C3_node_list_dict = {}
  # output is expected to be sorted
  aux_G_to_output_sec_list_dict = defaultdict(lambda: [])
  # output is expected to be sorted
  aux_G_to_output_C3_node_list_dict = defaultdict(lambda: [])
  for curr_aux_G in aux_graphs:
    C0, C1, C2, C3 = aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G]
    LO_node_name_set, LA_node_name_set = aux_graph_to_LO_node_names_LA_node_names_tuple_dict[curr_aux_G]
    V_r_name_set = LO_node_name_set | LA_node_name_set
    ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
    # determine "base" edges that are local ordinary or local auxiliary depending on if both endpoints are local ordinary or not, resp.
    LO_edges = []
    base_LA_edges = []
    # this is used s.t. we later remove duplicate edges
    shiny_edges = []
    for edge in aux_graph_to_base_edge_sources_dict[curr_aux_G]:
      old_origin = edge.getOrigin()
      old_dest = edge.getDestination()
      if old_origin.getName() not in V_r_name_set or old_dest.getName() not in V_r_name_set:
        continue
      next_origin = curr_aux_G.getVertexByName(old_origin.getName())
      next_dest = curr_aux_G.getVertexByName(old_dest.getName())
      next_edge = AOEdge(next_origin, next_dest)
      if old_origin.getName() in LO_node_name_set and old_dest.getName() in LO_node_name_set:
        LO_edges.append(next_edge)
        next_edge.setIsLocalOrdinary()
      elif old_origin.getName() in V_r_name_set and old_dest.getName() in V_r_name_set:
        base_LA_edges.append(next_edge)
        next_edge.setIsLocalAuxiliary()
    shiny_edges.extend(LO_edges)
    shiny_edges.extend(base_LA_edges)
    # determine local auxiliary edges -- i.e. two types of shortcut edge
    # handle shortcut edge type a
    # create list B_r and create list (B_r)'
    # we must set pre-order numbers and number of descendants for forward dominator tree
    source_edge_candidates = []
    # there was a bug here s.t. we need to use curr_aux_G and not curr_aux_graph
    for curr_edge in aux_graph_to_source_edges_dict[curr_aux_G]:
      old_origin = curr_edge.getOrigin()
      old_dest = curr_edge.getDestination()
      dt1_next_origin = dt1.getVertexByName(old_origin.getName())
      # source edges for shortcut edge type a are: 
      # origin is not in our four layers, 
      # destination is in our four layers, 
      # origin is a non-proper descendant of root for current auxiliary graph
      if (old_origin.getName() not in V_r_name_set) and (old_dest.getName() in V_r_name_set) and (doStar(ag_root_dt_vertex, dt1_next_origin) == True):
        source_edge_candidates.append(curr_edge)
    aux_G_to_shiny_edges_dict[curr_aux_G] = shiny_edges
    aux_G_to_input_sec_list_dict[curr_aux_G] = source_edge_candidates
    aux_G_to_input_C3_node_list_dict[curr_aux_G] = C3
  # handle shortcut case a all at once via merge, bucket sort, unmerge
  combined_sec_list = []
  combined_C3_node_list = []
  sec_to_aux_graphs_dict = defaultdict(lambda: [])
  C3_node_to_aux_graphs_dict = defaultdict(lambda: [])
  for curr_aux_graph in aux_graphs:
    curr_sec_list = aux_G_to_input_sec_list_dict[curr_aux_graph]
    curr_C3_node_list = aux_G_to_input_C3_node_list_dict[curr_aux_graph]
    # we assume extend for operand with length k takes time O(k)
    combined_sec_list.extend(curr_sec_list)
    combined_C3_node_list.extend(curr_C3_node_list)
    for curr_sec in curr_sec_list:
      sec_to_aux_graphs_dict[curr_sec].append(curr_aux_graph)
    for curr_C3_node in curr_C3_node_list:
      C3_node_to_aux_graphs_dict[curr_C3_node].append(curr_aux_graph)
  sec_list_sorted = bucketSort(combined_sec_list, 1, len(V), lambda x: dt1.getVertexByName(x.getOrigin().getName()).getPreorderNumber())
  C3_node_list_sorted = bucketSort(combined_C3_node_list, 1, len(V), lambda x: dt1.getVertexByName(x.getName()).getPreorderNumber())
  for curr_sec in sec_list_sorted:
    curr_aux_graphs = sec_to_aux_graphs_dict[curr_sec]
    for curr_aux_G in curr_aux_graphs:
      aux_G_to_output_sec_list_dict[curr_aux_G].append(curr_sec)
  for curr_C3_node in C3_node_list_sorted:
    curr_aux_graphs = C3_node_to_aux_graphs_dict[curr_C3_node]
    for curr_aux_G in curr_aux_graphs:
      aux_G_to_output_C3_node_list_dict[curr_aux_G].append(curr_C3_node)
  aux_G_to_shiny_edges_again_dict = {}
  for curr_aux_G in aux_graphs:
    C0, C1, C2, C3 = aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G]
    ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
    source_edge_candidates_sorted = aux_G_to_output_sec_list_dict[curr_aux_G]
    # for (B_r)', have vertices in C^3
    second_list_sorted = aux_G_to_output_C3_node_list_dict[curr_aux_G]
    shiny_edges = aux_G_to_shiny_edges_dict[curr_aux_G]
    augmented_secs = [(x, dt1.getVertexByName(x.getOrigin().getName()).getPreorderNumber()) for x in source_edge_candidates_sorted]
    augmented_sls = [(x, dt1.getVertexByName(x.getName()).getPreorderNumber()) for x in second_list_sorted]
    cs1_result = doShortcutEdgeCaseBSelectZ(augmented_secs, augmented_sls)
    cs1_edges = []
    for i in xrange(len(source_edge_candidates_sorted)):
      source_edge = source_edge_candidates_sorted[i]
      z_vertex = cs1_result[i]
      # have invalid z vertex
      if z_vertex == None:
        continue
      # we must remember whether origin replacement is in curr. auxiliary graph
      source_origin = source_edge.getOrigin()
      source_dest = source_edge.getDestination()
      next_origin = curr_aux_G.getVertexByName(z_vertex.getName())
      next_dest = curr_aux_G.getVertexByName(source_dest.getName())
      curr_edge = AOEdge(next_origin, next_dest)
      curr_edge.setIsLocalAuxiliary()
      cs1_edges.append(curr_edge)
    shiny_edges.extend(cs1_edges)
    aux_G_to_shiny_edges_again_dict[curr_aux_G] = shiny_edges
  # handle shortcut edge type b
  # for each edge (u, v), u needs to be descendant of a C^3 vertex, 
  # v needs to be descendant of curr. aux. graph root r, 
  # use LCA of endpoint for an edge by having three O(1)-time checks for determining tag values t
  # details in fastvrb s.t. they do not exist in fast2ecb:
  # - have extra initial step of using tag values t
  # - don't use compressed dominator tree
  # - label l for a node is based on min. tag for edges (w, v) s.t. origin is that node
  # details in fastvrb s.t. they are also in fast2ecb:
  # - low values are determined for every node except root of dominator tree
  # - low is same
  # - deciding whether to add an edge is based on comparison between low number and pre-order number
  # this used to be inefficient
  for edge in E:
    # for edge (u, v): 
    # t(u, v) = pre(u) if u is ancestor of v in D(s)
    # t(u, v) = pre(v) if v is ancestor of u in D(s)
    # t(u, v) = pre(d(v)) otherwise
    t_value = None
    origin = edge.getOrigin()
    dest = edge.getDestination()
    node_u = dt1.getVertexByName(origin.getName())
    node_v = dt1.getVertexByName(dest.getName())
    if doStar(node_u, node_v) == True:
      t_value = node_u.getPreorderNumber()
    elif doStar(node_v, node_u) == True:
      t_value = node_v.getPreorderNumber()
    else:
      # we cannot be related via cross edge if destination is start vertex, so this is safe
      t_value = node_v.getParent().getPreorderNumber()
    edge.setTag(t_value)
  origin_name_to_edges_dict = defaultdict(lambda: [])
  for edge in E:
    origin = edge.getOrigin()
    origin_name = origin.getName()
    origin_name_to_edges_dict[origin_name].append(edge)
  for dt1_vertex in dt1.getVertices():
    if dt1_vertex.getName() == s.getName():
      continue
    tag_values = []
    # this used to be inefficient; we need to consider only edges with origin that is the current node
    for edge in origin_name_to_edges_dict[dt1_vertex.getName()]:
      origin = edge.getOrigin()
      dest = edge.getDestination()
      if origin.getName() == dt1_vertex.getName():
        tag_values.append(edge.getTag())
    min_tag_value = min(tag_values)
    # note that we are guaranteed to have at least one tag value
    dt1_vertex.setLabel(min_tag_value)
  node_name_to_aux_graph_dict = defaultdict(lambda: [])
  for curr_aux_G in aux_graphs:
    curr_vertices = curr_aux_G.getVertices()
    for curr_vertex in curr_vertices:
      curr_vertex_name = curr_vertex.getName()
      node_name_to_aux_graph_dict[curr_vertex_name].append(curr_aux_G)
  aux_graph_to_cs2b_edges_dict = defaultdict(lambda: [])
  # iterate over edges, take origin and iterate over output aux. graphs
  for edge in E:
    origin = edge.getOrigin()
    dest = edge.getDestination()
    # there was a bug here; we care about C0, C1, C2, C3, not just C1 and C2
    for curr_aux_G in node_name_to_aux_graph_dict[origin.getName()]:
      curr_ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
      r_node = curr_aux_G.getVertexByName(curr_ag_root_dt_vertex.getName())
      if doStar(curr_ag_root_dt_vertex, dt1.getVertexByName(dest.getName())) == False:
        # if edge is self-edge, ignore it
        next_origin = curr_aux_G.getVertexByName(origin.getName())
        if next_origin.getName() == r_node.getName():
          continue
        next_edge = AOEdge(next_origin, r_node)
        next_edge.setIsLocalAuxiliary()
        aux_graph_to_cs2b_edges_dict[curr_aux_G].append(next_edge)
  dt1.determineLowValues()
  for curr_aux_G in aux_graphs:
    C0, C1, C2, C3 = aux_graph_to_C0_C1_C2_C3_tuple_dict[curr_aux_G]
    ag_root_dt_vertex = aux_graph_to_root_dt_vertex_dict[curr_aux_G]
    shiny_edges = aux_G_to_shiny_edges_again_dict[curr_aux_G]
    r_node = curr_aux_G.getVertexByName(ag_root_dt_vertex.getName())
    cs2_edges = DTree.collectShortcutCaseBEdges(dt1, C3, E, ag_root_dt_vertex, r_node, curr_aux_G)
    # by definition, G_s has no type-b shortcut edges; this was source of a bug
    if ag_root_dt_vertex.getName() != s.getName():
      shiny_edges.extend(cs2_edges)
    cs2b_edges = aux_graph_to_cs2b_edges_dict[curr_aux_G]
    # by definition, G_s has no type-b shortcut edges; this was source of a bug
    if ag_root_dt_vertex.getName() != s.getName():
      shiny_edges.extend(cs2b_edges)
    auxiliary_graph_root_name_pair_list.append((curr_aux_G, ag_root_dt_vertex.getName()))
    seen_edge_str_set = set([])
    next_shiny_edges = []
    for edge in shiny_edges:
      if edge.toString() not in seen_edge_str_set:
        next_shiny_edges.append(edge)
        seen_edge_str_set |= set([edge.toString()])
    curr_aux_G.addEdges(next_shiny_edges)
  # step 3 - process nodes in dominator tree in bottom-up order (e.g. via descending pre-order)
  preorder_nodes = dt1.getPreorderNodes()
  bottom_up_nodes = list(reversed(preorder_nodes))
  root_name_to_aux_graph_dict = {}
  for aux_graph, root_name in auxiliary_graph_root_name_pair_list:
    root_name_to_aux_graph_dict[root_name] = aux_graph
  for curr_dt_node in bottom_up_nodes:
    aux_graph = root_name_to_aux_graph_dict[curr_dt_node.getName()]
    if curr_dt_node.haveChildren() == False:
      continue
    curr_result = doFastVRBReverse(aux_graph.getVertices(), aux_graph.getEdges(), wbc, curr_dt_node.getName())
  return wbc

def doSimpleVRBModified(V, E, wbc, sap):
  # step 3.5.1 -- retrieve blocks from active block set s.t. intersection with V is s.t. number of overall ordinary nodes in it is >= 2
  # (note -- we do not use single block to start off with -- we use block collection that we retrieve from active block set)
  name_to_vertex_dict = {}
  for v in V:
    name = v.getName()
    name_to_vertex_dict[name] = v
  curr_wrapped_blocks = []
  wrapped_block_to_special_node_count_dict = defaultdict(lambda: 0)
  for curr_vertex in V:
    curr_wrapped_blocks_again = wbc.getWrappedBlocksWithVertexName(curr_vertex.getName())
    # there was a bug here s.t. we do not care about just overall ordinary -- we just care that we are from V and a block
    if True:
      for curr_wrapped_block in curr_wrapped_blocks_again:
        wrapped_block_to_special_node_count_dict[curr_wrapped_block] += 1
  for curr_wrapped_block, curr_special_node_count in wrapped_block_to_special_node_count_dict.items():
    if curr_special_node_count >= 2:
      curr_wrapped_blocks.append(curr_wrapped_block)
  # step "one"
  saps = [sap]
  # step "two"
  curr_blocks = []
  for curr_wrapped_block in curr_wrapped_blocks:
    curr_block = curr_wrapped_block.getVertices()
    curr_blocks.append(curr_block)
  # step "three"
  n = len(V)
  g_vertex_name_to_number_dict = {}
  number_to_g_vertex_dict = {}
  for i in xrange(len(V)):
    g_vertex = V[i]
    g_vertex_name_to_number_dict[g_vertex.getName()] = i
    number_to_g_vertex_dict[i] = g_vertex
  for curr_sap in saps:
    # step 3.5.2 -- get SCC's s.t. we have removed single sap
    adj = defaultdict(lambda: [])
    for g_edge in E:
      origin = g_edge.getOrigin()
      destination = g_edge.getDestination()
      if origin.getName() == curr_sap.getName() or destination.getName() == curr_sap.getName():
        continue
      origin_num = g_vertex_name_to_number_dict[origin.getName()]
      destination_num = g_vertex_name_to_number_dict[destination.getName()]
      adj[origin_num].append(destination_num)
    scc_ks = SCC_KS(n, adj)
    components = scc_ks.scc()
    next_components = []
    for component in components:
      next_component = [number_to_g_vertex_dict[x] for x in component]
      next_components.append(next_component)
    # step 3.5.3 -- note that it takes time linear in O(N + K), 
    # where N is sum of sizes of active blocks and K is |V|;
    # we perform an "overlay"
    next_blocks = []
    label_num_to_component_dict = defaultdict(lambda: [])
    vertex_name_to_label_num_dict = defaultdict(lambda: 0)
    for i in xrange(1, len(next_components) + 1):
      label_num = i
      curr_next_component = next_components[i - 1]
      label_num_to_component_dict[label_num] = curr_next_component
      curr_vertices = curr_next_component
      for curr_vertex in curr_vertices:
        vertex_name_to_label_num_dict[curr_vertex.getName()] = label_num
    for curr_block in curr_blocks:
      label_num_to_vertices_dict = defaultdict(lambda: [])
      for curr_vertex in curr_block:
        curr_label_num = vertex_name_to_label_num_dict[curr_vertex.getName()]
        if curr_label_num == 0:
          continue
        label_num_to_vertices_dict[curr_label_num].append(curr_vertex)
      # have modified refine
      do_include_sap = curr_sap.getName() in [x.getName() for x in curr_block]
      for curr_group in label_num_to_vertices_dict.values():
        next_curr_group = curr_group[ : ]
        if do_include_sap == True:
          if curr_sap.getName() not in [x.getName() for x in next_curr_group]:
            next_curr_group.append(curr_sap)
        if len(next_curr_group) >= 2:
          next_blocks.append(next_curr_group)
    curr_blocks = next_blocks
  # we now have replacement wrapped blocks; 
  # remove the source wrapped blocks 
  # and add the replacement wrapped blocks 
  # to all_wrapped_blocks_set
  for curr_wrapped_block in curr_wrapped_blocks:
    wbc.removeWrappedBlock(curr_wrapped_block)
  for curr_block in curr_blocks:
    curr_wrapped_block = WrappedBlock(curr_block)
    wbc.addWrappedBlock(curr_wrapped_block)
  return wbc

if __name__ == '__main__':

  """

  # example from figures one and two in georgiadis et al. 2015

  v_A = AOVertex("A")
  v_B = AOVertex("B")
  v_C = AOVertex("C")
  v_D = AOVertex("D")
  v_E = AOVertex("E")
  v_F = AOVertex("F")
  v_H = AOVertex("H")
  v_I = AOVertex("I")
  v_J = AOVertex("J")
  v_L = AOVertex("L")

  vertices = [v_A, v_B, v_C, v_D, v_E, v_F, v_H, v_I, v_J, v_L]

  for vertex in vertices:
    vertex.setIsOverallOrdinary()
    vertex.setIsLocalOrdinary()

  e1 = AOEdge(v_A, v_B)
  e2 = AOEdge(v_A, v_C)
  e3 = AOEdge(v_B, v_A)
  e4 = AOEdge(v_B, v_C)
  e5 = AOEdge(v_C, v_A)
  e6 = AOEdge(v_C, v_B)
  e7 = AOEdge(v_C, v_D)
  e8 = AOEdge(v_C, v_E)
  e9 = AOEdge(v_C, v_H)
  e10 = AOEdge(v_D, v_B)
  e11 = AOEdge(v_D, v_C)
  e12 = AOEdge(v_D, v_E)
  e13 = AOEdge(v_E, v_C)
  e14 = AOEdge(v_E, v_D)
  e15 = AOEdge(v_E, v_F)
  e16 = AOEdge(v_E, v_H)
  e17 = AOEdge(v_F, v_D)
  e18 = AOEdge(v_F, v_E)
  e19 = AOEdge(v_F, v_I)
  e20 = AOEdge(v_H, v_F)
  e21 = AOEdge(v_H, v_J)
  e22 = AOEdge(v_H, v_L)
  e23 = AOEdge(v_I, v_H)
  e24 = AOEdge(v_I, v_L)
  e25 = AOEdge(v_J, v_H)
  e26 = AOEdge(v_J, v_L)
  e27 = AOEdge(v_L, v_H)
  e28 = AOEdge(v_L, v_I)
  e29 = AOEdge(v_L, v_J)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29]

  for edge in edges:
    edge.setIsLocalOrdinary()

  # (expect blocks of [A, B, C], [C, D, E, F], [F, H], [H, I, J, L])

  """

  """

  # example from figure five in georgiadis et al. 2015

  v_a = AOVertex("a")
  v_b = AOVertex("b")
  v_c = AOVertex("c")
  v_d = AOVertex("d")
  v_e = AOVertex("e")
  v_f = AOVertex("f")
  v_g = AOVertex("g")
  v_h = AOVertex("h")
  v_i = AOVertex("i")
  v_j = AOVertex("j")
  v_k = AOVertex("k")
  v_l = AOVertex("l")
  v_m = AOVertex("m")
  v_n = AOVertex("n")
  v_o = AOVertex("o")
  v_p = AOVertex("p")
  v_q = AOVertex("q")
  v_r = AOVertex("r")
  v_s = AOVertex("s")
  v_t = AOVertex("t")
  v_u = AOVertex("u")
  v_v = AOVertex("v")
  v_w = AOVertex("w")
  v_x = AOVertex("x")
  v_y = AOVertex("y")
  v_z = AOVertex("z")

  vertices = [v_a, v_b, v_c, v_d, v_e, v_f, v_g, v_h, v_i, v_j, v_k, v_l, v_m, v_n, v_o, v_p, v_q, v_r, v_s, v_t, v_u, v_v, v_w, v_x, v_y, v_z]

  for vertex in vertices:
    vertex.setIsOverallOrdinary()
    vertex.setIsLocalOrdinary()

  e1 = AOEdge(v_a, v_r)
  e2 = AOEdge(v_b, v_r)
  e3 = AOEdge(v_c, v_g)
  e4 = AOEdge(v_c, v_h)
  e5 = AOEdge(v_d, v_i)
  e6 = AOEdge(v_d, v_k)
  e7 = AOEdge(v_e, v_f)
  e8 = AOEdge(v_f, v_l)
  e9 = AOEdge(v_f, v_m)
  e10 = AOEdge(v_g, v_n)
  e11 = AOEdge(v_h, v_d)
  e12 = AOEdge(v_h, v_g)
  e13 = AOEdge(v_i, v_o)
  e14 = AOEdge(v_i, v_q)
  e15 = AOEdge(v_j, v_k)
  e16 = AOEdge(v_k, v_t)
  e17 = AOEdge(v_l, v_u)
  e18 = AOEdge(v_l, v_v)
  e19 = AOEdge(v_m, v_l)
  e20 = AOEdge(v_n, v_c)
  e21 = AOEdge(v_n, v_w)
  e22 = AOEdge(v_o, v_p)
  e23 = AOEdge(v_p, v_x)
  e24 = AOEdge(v_q, v_j)
  e25 = AOEdge(v_q, v_p)
  e26 = AOEdge(v_r, v_c)
  e27 = AOEdge(v_r, v_f)
  e28 = AOEdge(v_r, v_s)
  e29 = AOEdge(v_s, v_a)
  e30 = AOEdge(v_s, v_b)
  e31 = AOEdge(v_t, v_y)
  e32 = AOEdge(v_u, v_e)
  e33 = AOEdge(v_u, v_v)
  e34 = AOEdge(v_v, v_u)
  e35 = AOEdge(v_v, v_z)
  e36 = AOEdge(v_w, v_h)
  e37 = AOEdge(v_x, v_q)
  e38 = AOEdge(v_y, v_e)
  e39 = AOEdge(v_y, v_j)
  e40 = AOEdge(v_z, v_b)
  e41 = AOEdge(v_z, v_d)
  e42 = AOEdge(v_z, v_m)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29, e30, e31, e32, e33, e34, e35, e36, e37, e38, e39, e40, e41, e42]

  for edge in edges:
    edge.setIsLocalOrdinary()

  # (expect blocks of [b, r], [f, l], [m, l], [c, h], [u, l, v], [g, n])

  """

  """

  # example from figure three of georgiadis et al. 2015

  v_a = AOVertex("a")
  v_b = AOVertex("b")
  v_c = AOVertex("c")
  v_d = AOVertex("d")
  v_e = AOVertex("e")
  v_f = AOVertex("f")
  v_g = AOVertex("g")
  v_h = AOVertex("h")
  v_i = AOVertex("i")

  vertices = [v_a, v_b, v_c, v_d, v_e, v_f, v_g, v_h, v_i]

  for vertex in vertices:
    vertex.setIsOverallOrdinary()
    vertex.setIsLocalOrdinary()

  e1 = AOEdge(v_a, v_b)
  e2 = AOEdge(v_a, v_c)
  e3 = AOEdge(v_b, v_f)
  e4 = AOEdge(v_b, v_g)
  e5 = AOEdge(v_c, v_d)
  e6 = AOEdge(v_c, v_f)
  e7 = AOEdge(v_c, v_g)
  e8 = AOEdge(v_d, v_a)
  e9 = AOEdge(v_d, v_e)
  e10 = AOEdge(v_d, v_h)
  e11 = AOEdge(v_e, v_a)
  e12 = AOEdge(v_e, v_h)
  e13 = AOEdge(v_f, v_i)
  e14 = AOEdge(v_g, v_d)
  e15 = AOEdge(v_g, v_e)
  e16 = AOEdge(v_h, v_g)
  e17 = AOEdge(v_i, v_a)
  e18 = AOEdge(v_i, v_f)
  e19 = AOEdge(v_i, v_g)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19]

  for edge in edges:
    edge.setIsLocalOrdinary()

  # (expect blocks of [a, b], [a, c], [a, d, g, e], [g, h], [f, i])

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

  # blocks = doSimpleVRB(vertices, edges)
  blocks = doFastVRB(vertices, edges)

  for i in xrange(len(blocks)):
    block = blocks[i]
    # print "block", i, ":", [x.toString() for x in block]
    print "block", i, ":", [x.getName() for x in block]
    # print "block", i, ":", [x.toString() for x in block if x.isOverallOrdinary() == True]


