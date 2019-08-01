# 2019-07-24

# we create block forest for vertex resilience

# it's worth noting that for vrb algorithms, 
# if a node does not explicitly appear 
# in any output block is taken to be 
# in its own size-one block

from bf import BlockGraph, Block, BlockNode, StandardNode, VRBBFOracle

from fastvrb_georgiadis import doFastVRB

from fastvrb_georgiadis import AOEdge as FastVRBAOEdge
from fastvrb_georgiadis import AOVertex as FastVRBAOVertex

from fast2ecb_georgiadis import doFast2ECB

from fast2ecb_georgiadis import AOEdge as Fast2ECBAOEdge
from fast2ecb_georgiadis import AOVertex as Fast2ECBAOVertex

from fgib_tarjan import Graph, Vertex, Edge, Tree, TreeVertex, TreeEdge
from collections import defaultdict

# have nodes and edges that come in two flavors: graph, tree

# throughout, we assume nodes have unique names; 
# this even includes blocks for vertex-resilience; 
# we assume "B#" is untaken

class TwoECBOracle:
  # we assume a node is in exactly one two-edge-connected block
  def __init__(self, ao_vertices, ao_edges):
    blocks = doFast2ECB(ao_vertices, ao_edges)
    self.blocks = blocks
    name_to_node_dict = {}
    self.name_to_node_dict = name_to_node_dict
    node_to_block_dict = {}
    self.node_to_block_dict = node_to_block_dict
    for block in blocks:
      for item in block:
        # item is an AOVertex
        node_to_block_dict[item] = block
        name_to_node_dict[item.getName()] = item
    self.node_names_set = set(name_to_node_dict.keys())
  def _getNodeNamesSet(self):
    return self.node_names_set
  def _getBlocks(self):
    return self.blocks
  def _getNameToNodeDict(self):
    return self.name_to_node_dict
  def _getNodeToBlockDict(self):
    return self.node_to_block_dict
  # if names are not present for vertex collection, we fail
  def areTwoEdgeConnected(self, name1, name2):
    node_names_set = self._getNodeNamesSet()
    if name1 not in node_names_set or name2 not in node_names_set:
      raise Exception()
    name_to_node_dict = self._getNameToNodeDict()
    node_to_block_dict = self._getNodeToBlockDict()
    node1 = name_to_node_dict[name1]
    node2 = name_to_node_dict[name2]
    block1 = node_to_block_dict[node1]
    block2 = node_to_block_dict[node2]
    return block1 == block2

class VRBOracle:
  def __init__(self, ao_vertices, ao_edges):
    standard_names = [x.getName() for x in ao_vertices]
    blocks = doFastVRB(ao_vertices, ao_edges)
    # we note that un-post-processed vrb algorithms may provide 
    # only blocks that have at least two items in them
    next_blocks = []
    for i in xrange(len(blocks)):
      next_name = "B" + str(i)
      next_block = Block(next_name, [x.getName() for x in blocks[i]])
      next_blocks.append(next_block)
    node_name_is_seen_dict = defaultdict(lambda: False)
    for block in blocks:
      for item in block:
        curr_name = item.getName()
        node_name_is_seen_dict[curr_name] = True
    leftover_names = []
    for ao_vertex in ao_vertices:
      curr_name = ao_vertex.getName()
      if node_name_is_seen_dict[curr_name] == False:
        leftover_names.append(curr_name)
    # print leftover_names
    additional_blocks = []
    for i in xrange(len(leftover_names)):
      block_name = "B" + str(i + len(blocks))
      curr_leftover_name = leftover_names[i]
      curr_block = Block(block_name, [curr_leftover_name])
      additional_blocks.append(curr_block)
    next_next_blocks = next_blocks + additional_blocks
    vrb_bf_oracle = VRBBFOracle.construct(standard_names, next_next_blocks)
    self.vrb_bf_oracle = vrb_bf_oracle
  def _getVRBBFOracle(self):
    return self.vrb_bf_oracle
  # if names are not present for vertex collection, we fail
  def areVertexResilient(self, name1, name2):
    vrb_bf_oracle = self._getVRBBFOracle()
    return vrb_bf_oracle.areVertexResilient(name1, name2)

class TwoVCBOracle:
  def __init__(self, twoecb_oracle, vrb_oracle):
    self.twoecb_oracle = twoecb_oracle
    self.vrb_oracle = vrb_oracle
  def _getTwoECBOracle(self):
    return self.twoecb_oracle
  def _getVRBOracle(self):
    return self.vrb_oracle
  def areTwoVertexConnected(self, name1, name2):
    twoecb_oracle = self._getTwoECBOracle()
    vrb_oracle = self._getVRBOracle()
    result1 = twoecb_oracle.areTwoEdgeConnected(name1, name2)
    result2 = vrb_oracle.areVertexResilient(name1, name2)
    result = result1 == True and result2 == True
    return result

if __name__ == '__main__':

  # all nodes (i.e. standard and block) must have distinct names

  """

  standard_names = [1, 2, 3, 4, 5, 6]
  blocks = [Block("B1", [1, 2, 3]), Block("B2", [3, 4, 5]), Block("B3", [3, 4, 5, 6])]

  """

  """

  standard_names = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
  blocks = [Block("B1", ["a", "b"]), Block("B2", ["a", "c"]), Block("B3", ["a", "d", "g", "e"]), Block("B4", ["g", "h"]), Block("B5", ["f", "i"])]

  oracle = VRBOracle.construct(standard_names, blocks)

  """

  # for lax boolean MM

  v_S = Fast2ECBAOVertex("S")
  v_A = Fast2ECBAOVertex("A")
  v_B = Fast2ECBAOVertex("B")
  v_C = Fast2ECBAOVertex("C")
  v_D = Fast2ECBAOVertex("D")
  v_E = Fast2ECBAOVertex("E")
  v_F = Fast2ECBAOVertex("F")
  v_G = Fast2ECBAOVertex("G")
  v_H = Fast2ECBAOVertex("H")
  v_I = Fast2ECBAOVertex("I")
  v_J = Fast2ECBAOVertex("J")
  v_K = Fast2ECBAOVertex("K")
  v_L = Fast2ECBAOVertex("L")
  v_M = Fast2ECBAOVertex("M")
  v_N = Fast2ECBAOVertex("N")

  vertices1 = [v_S, v_A, v_B, v_C, v_D, v_E, v_F, v_G, v_H, v_I, v_J, v_K, v_L, v_M, v_N]

  vertices2 = [FastVRBAOVertex(x.getName()) for x in vertices1]

  for vertex in vertices1 + vertices2:
    vertex.setIsOverallOrdinary()
    vertex.setIsLocalOrdinary()

  name_to_vrb_node = {}
  for vertex in vertices2:
    name_to_vrb_node[vertex.getName()] = vertex

  e1 = Fast2ECBAOEdge(v_S, v_A)
  e2 = Fast2ECBAOEdge(v_S, v_B)
  e3 = Fast2ECBAOEdge(v_A, v_S)
  e4 = Fast2ECBAOEdge(v_A, v_C)
  e5 = Fast2ECBAOEdge(v_A, v_D)
  e6 = Fast2ECBAOEdge(v_B, v_A)
  e7 = Fast2ECBAOEdge(v_C, v_D)
  e8 = Fast2ECBAOEdge(v_D, v_E)
  e9 = Fast2ECBAOEdge(v_E, v_F)
  e10 = Fast2ECBAOEdge(v_E, v_H)
  e11 = Fast2ECBAOEdge(v_F, v_G)
  e12 = Fast2ECBAOEdge(v_F, v_I)
  e13 = Fast2ECBAOEdge(v_G, v_E)
  e14 = Fast2ECBAOEdge(v_G, v_J)
  e15 = Fast2ECBAOEdge(v_G, v_K)
  e16 = Fast2ECBAOEdge(v_H, v_G)
  e17 = Fast2ECBAOEdge(v_I, v_G)
  e18 = Fast2ECBAOEdge(v_J, v_K)
  e19 = Fast2ECBAOEdge(v_K, v_H)
  e20 = Fast2ECBAOEdge(v_K, v_J)
  e21 = Fast2ECBAOEdge(v_K, v_L)
  e22 = Fast2ECBAOEdge(v_L, v_M)
  e23 = Fast2ECBAOEdge(v_L, v_N)
  e24 = Fast2ECBAOEdge(v_M, v_F)
  e25 = Fast2ECBAOEdge(v_M, v_N)
  e26 = Fast2ECBAOEdge(v_N, v_B)
  e27 = Fast2ECBAOEdge(v_N, v_M)

  edges1 = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27]

  edges2 = []
  for edge1 in edges1:
    next_origin = name_to_vrb_node[edge1.getOrigin().getName()]
    next_dest = name_to_vrb_node[edge1.getDestination().getName()]
    next_edge = FastVRBAOEdge(next_origin, next_dest)
    edges2.append(next_edge)

  for edge in edges1 + edges2:
    edge.setIsLocalOrdinary()

  twoecb_oracle = TwoECBOracle(vertices1, edges1)
  # expect False
  print twoecb_oracle.areTwoEdgeConnected("S", "A")
  # expect True
  print twoecb_oracle.areTwoEdgeConnected("E", "G")
  # expect False
  print twoecb_oracle.areTwoEdgeConnected("E", "H")
  vrb_oracle = VRBOracle(vertices2, edges2)
  # expect True
  print vrb_oracle.areVertexResilient("D", "D")
  # expect False
  print vrb_oracle.areVertexResilient("C", "D")
  # expect True
  print vrb_oracle.areVertexResilient("K", "G")
  # expect False
  print vrb_oracle.areVertexResilient("K", "L")
  # expect False
  print vrb_oracle.areVertexResilient("S", "B")
  # expect True
  print vrb_oracle.areVertexResilient("A", "B")
  twovcb_oracle = TwoVCBOracle(twoecb_oracle, vrb_oracle)
  # expect True
  print twovcb_oracle.areTwoVertexConnected("E", "G")
  # expect True
  print twovcb_oracle.areTwoVertexConnected("N", "M")
  # expect True
  print twovcb_oracle.areTwoVertexConnected("G", "G")
  # expect False
  print twovcb_oracle.areTwoVertexConnected("D", "E")
  # expect True
  print twovcb_oracle.areTwoVertexConnected("D", "D")

  # expect error
  # print twoecb_oracle.areTwoEdgeConnected("Z", "Z")
  # expect error
  # print vrb_oracle.areVertexResilient("Z", "Z")
  # expect error
  # print twovcb_oracle.areTwoVertexConnected("Z", "Z")

  # expect error
  # print twoecb_oracle.areTwoEdgeConnected("A", "Z")
  # expect error
  # print vrb_oracle.areVertexResilient("A", "Z")
  # expect error
  # print twovcb_oracle.areTwoVertexConnected("A", "Z")


