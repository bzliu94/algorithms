# 2019-07-24

# we create block forest for vertex resilience

# have nodes and edges that come in two flavors: graph, tree

from fgib_tarjan import Graph, Vertex, Edge, Tree, TreeVertex, TreeEdge
from collections import defaultdict

class BlockGraph(Graph):
  def __init__(self):
    Graph.__init__(self)
    self.visited = None
  def generateBlockForest(self):
    roots = self._dfs()
    block_trees = []
    for curr_root in roots:
      curr_tree = BlockTree()
      curr_tree.setRoot(curr_root)
      block_trees.append(curr_tree)
    return block_trees
  def _dfs(self):
    nodes = self.getVertices()
    self.visited = defaultdict(lambda: False)
    roots = []
    for curr_g_node in nodes:
      if self.visited[curr_g_node] == False:
        # start a new tree for our forest
        curr_root = self._explore(curr_g_node, None)
        roots.append(curr_root)
    return roots
  # if ref. parent is None, we are root of a tree
  def _explore(self, g_node, t_ref_parent):
    self.visited[g_node] = True
    curr_t_node = self._previsit(g_node, t_ref_parent)
    for edge in self.getEdgesOriginatingAt(g_node):
      curr_dest = edge.getDestination()
      if self.visited[curr_dest] == False:
        self._explore(curr_dest, curr_t_node)
    self._postvisit(g_node)
    return curr_t_node
  def _previsit(self, g_node, t_ref_parent):
    # add a child for our current tree
    curr_t_node = TreeVertex(g_node.getName())
    if t_ref_parent != None:
      t_ref_parent.addChild(curr_t_node)
      curr_t_node.setParent(t_ref_parent)
    return curr_t_node
  def _postvisit(self, node):
    pass

class BlockTree(Tree):
  def __init__(self):
    Tree.__init__(self)

class Block:
  def __init__(self, name, items):
    self.name = name
    self.items = items
  def getName(self):
    return self.name
  def getItems(self):
    return self.items
  def toString(self):
    curr_str = str(self.getName()) + " " + str(self.getItems())
    return curr_str

class BlockGraphNode(Vertex):
  def __init__(self, name):
    Vertex.__init__(self, name)

class StandardNode(BlockGraphNode):
  def __init__(self, name):
    BlockGraphNode.__init__(self, name)

class BlockNode(BlockGraphNode):
  def __init__(self, name):
    BlockGraphNode.__init__(self, name)

# we note that un-post-processed vrb algorithms may provide 
# only blocks that have at least two items in them
class VRBBFOracle:
  def __init__(self, standard_names, blocks):
    self.standard_names = standard_names
    self.blocks = blocks
    self.name_to_bf_node_dict = None
    self.standard_names_set = set(standard_names)
  def _getStandardNames(self):
    return self.standard_names
  def _getBlocks(self):
    return self.blocks
  def _getNameToBFNodeDict(self):
    return self.name_to_bf_node_dict
  def _setNameToBFNodeDict(self, name_to_bf_node_dict):
    self.name_to_bf_node_dict = name_to_bf_node_dict
  def _getStandardNamesSet(self):
    return self.standard_names_set
  @staticmethod
  def construct(standard_names, blocks):
    oracle = VRBBFOracle(standard_names, blocks)
    # make block graph, from which we make block forest; 
    # block graph is undirected and bipartite; 
    # make standard nodes and block nodes that we later connect
    standard_nodes = []
    block_nodes = []
    name_to_block_node_dict = {}
    for curr_block in blocks:
      curr_block_name = curr_block.getName()
      curr_block_node = BlockNode(curr_block_name)
      block_nodes.append(curr_block_node)
      name_to_block_node_dict[curr_block_name] = curr_block_node
    name_to_standard_node_dict = {}
    for curr_standard_name in standard_names:
      curr_standard_node = StandardNode(curr_standard_name)
      standard_nodes.append(curr_standard_node)
      name_to_standard_node_dict[curr_standard_name] = curr_standard_node
    # determine undirected edges
    base_edges = []
    for curr_block in blocks:
      curr_items = curr_block.getItems()
      for curr_item in curr_items:
        # each item is a name
        curr_name = curr_item
        curr_origin = name_to_standard_node_dict[curr_name]
        curr_dest = name_to_block_node_dict[curr_block.getName()]
        curr_undirected_edge = Edge(curr_origin, curr_dest)
        base_edges.append(curr_undirected_edge)
    directed_edges = []
    for curr_base_edge in base_edges:
      curr_origin = curr_base_edge.getOrigin()
      curr_dest = curr_base_edge.getDestination()
      edge1 = Edge(curr_origin, curr_dest)
      edge2 = Edge(curr_dest, curr_origin)
      directed_edges.append(edge1)
      directed_edges.append(edge2)
    g = BlockGraph()
    g.addVertices(standard_nodes + block_nodes)
    g.addEdges(directed_edges)
    block_trees = g.generateBlockForest()
    name_to_bf_node_dict = {}
    for curr_block_tree in block_trees:
      nodes = curr_block_tree.getPreorderNodes()
      for curr_node in nodes:
        curr_name = curr_node.getName()
        name_to_bf_node_dict[curr_name] = curr_node
    oracle._setNameToBFNodeDict(name_to_bf_node_dict)
    return oracle
  # takes constant time, in principle; 
  # we assume each name appears once; 
  # also, we would prefer to make sure 
  # that the two names given are different; 
  # if names are not present for vertex collection, we fail
  def areVertexResilient(self, name1, name2):
    # this check is necessary because we might not 
    # have a parent to share, let alone have a grandparent; 
    # we assume the name is present in the input
    standard_names_set = self._getStandardNamesSet()
    if name1 not in standard_names_set or name2 not in standard_names_set:
      raise Exception()
    if name1 == name2:
      return True
    name_to_bf_node_dict = self._getNameToBFNodeDict()
    v1 = name_to_bf_node_dict[name1]
    v2 = name_to_bf_node_dict[name2]
    have_parent1 = v1.haveParent()
    have_parent2 = v2.haveParent()
    result = False
    if have_parent1 == True and have_parent2 == True:
      # check whether we are siblings for same node
      parent1 = v1.getParent()
      parent2 = v2.getParent()
      if parent1 == parent2:
        result = True
    # check whether one node is grandparent of the other
    if have_parent1 == True:
      parent1 = v1.getParent()
      have_gp1 = parent1.haveParent()
      if have_gp1 == True:
        if v2 == v1.getParent().getParent():
          result = True
    if have_parent2 == True:
      parent2 = v2.getParent()
      have_gp2 = parent2.haveParent()
      if have_gp2 == True:
        if v1 == v2.getParent().getParent():
          result = True
    return result

if __name__ == '__main__':

  # all nodes (i.e. standard and block) must have distinct names

  """

  standard_names = [1, 2, 3, 4, 5, 6]
  blocks = [Block("B1", [1, 2, 3]), Block("B2", [3, 4, 5]), Block("B3", [3, 4, 5, 6])]

  """

  standard_names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
  blocks = [Block("B1", ["a", "b"]), Block("B2", ["a", "c"]), Block("B3", ["a", "d", "g", "e"]), Block("B4", ["g", "h"]), Block("B5", ["f", "i"])]

  oracle = VRBBFOracle.construct(standard_names, blocks)

  # expect True
  print oracle.areVertexResilient("g", "h")
  # expect True
  print oracle.areVertexResilient("d", "g")
  # expect False
  print oracle.areVertexResilient("b", "c")
  # expect False
  print oracle.areVertexResilient("b", "i")
  # expect True
  print oracle.areVertexResilient("f", "i")
  # expect True
  print oracle.areVertexResilient("i", "i")
  # expect False
  print oracle.areVertexResilient("j", "i")
  # expect True
  print oracle.areVertexResilient("j", "j")
  # expect failure
  # print oracle.areVertexResilient("a", "z")


