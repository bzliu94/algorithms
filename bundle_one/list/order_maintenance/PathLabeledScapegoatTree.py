from ...tree.bbst.ScapegoatTree import *
from PathLabeledScapegoatTreeNode import *
# modify insert and rebuild operations 
#   for scapegoat tree
class PathLabeledScapegoatTree(ScapegoatTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    ScapegoatTree.__init__(self, key_transform, comparator)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, PathLabeledScapegoatTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, PathLabeledScapegoatTreeNode)
  @staticmethod
  def construct(entries):
    tree = PathLabeledScapegoatTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  """
  def find(self, key):
    pass
  def insert(self, key, value):
    pass
  def remove(self, entry):
    pass
  """
  # assume insert introduces a node 
  #   by expanding a placeholder external node
  def _rebuildlessInsert(self, key, value):
    # print key
    # result = ScapegoatTree.insert(self, key, value)
    result = ScapegoatTree._rebuildlessInsert(self, key, value)
    entry, node = result
    # print node.getElement().getKey(), node.getHeight()
    label = self.getPathLabel(node)
    # print label, entry.toString()
    node.setPathLabel(label)
    return result
  # takes O(1) time
  def retrieveLabel(self, node):
    return node.getPathLabel()
  # by having re-determination of path labels 
  #   be included as part of rebuilding, 
  #   we introduce an additional time cost 
  #   of O(log(n) + m)
  # return root of the rebuilt subtree
  # an issue: item may not have fully been inserted 
  #   by the time we call this method
  def localRebuild(self, u):
    # print "rebuilding"
    subtree_root = ScapegoatTree.localRebuild(self, u)
    # get root for rebuilt subtree
    # find partial path label for subtree of root
    # update path labels for rest of nodes in subtree
    label = self.getPathLabel(subtree_root)
    # print label
    subtree_root.setPathLabel(label)
    label_value = label.getValue()
    numeric_path, path_length = label_value
    # print subtree_root.getElement().getKey(), PathLabel.toBaseThreeString(numeric_path)
    # partial_label_value = (label_value - label_value % 3) / 3
    partial_numeric_path = (numeric_path - 1) / 3
    partial_path_length = path_length
    # partial_label = (partial_numeric_path, partial_path_length)
    # print "partial label:", partial_label, "entry:", u.getElement().toString()
    self._localRebuildLabelHelper(subtree_root, partial_numeric_path, partial_path_length)
    # self._localRebuildLabelHelper(subtree_root, partial_label_value)
    # def _localRebuildLabelHelper(self, node, partial_numeric_path, partial_path_length):
    return subtree_root
  def _localRebuildLabelHelper(self, node, partial_numeric_path, partial_path_length):
    if node.isExternal() == True:
      # do not update path label
      return
    # print "key:", node.getElement().getKey()
    # partial_label = (partial_numeric_path, partial_path_length)
    # print "partial label:", partial_label, "entry:", node.getElement().toString()
    # update current node's label based on partial label
    curr_numeric_path = partial_numeric_path * 3 + 1
    curr_path_length = partial_path_length
    # print self.toString()
    # print node.getHeight(), node.getElement().getKey(), node.isExternal()
    # curr_label_value = partial_label_value * 3 + 1
    # curr_label_value = partial_label_value * 3 + 1
    # print PathLabel.toBaseThreeString(curr_label_value), node.getHeight()
    curr_label = PathLabel(curr_numeric_path, curr_path_length)
    # curr_label = PathLabel(curr_label_value)
    node.setPathLabel(curr_label)
    # self._localRebuildLabelHelper(node.getLeftChild(), partial_numeric_path * 3, partial_path_length + 1)
    # self._localRebuildLabelHelper(node.getRightChild(), partial_numeric_path * 3 + 2, partial_path_length + 1)
    self._localRebuildLabelHelper(node.getLeftChild(), partial_numeric_path * 3, partial_path_length + 1)
    self._localRebuildLabelHelper(node.getRightChild(), partial_numeric_path * 3 + 2, partial_path_length + 1)
  # get value corresponding to a path 
  #   from root to a node
  # we assume that path always contains >= 1 nodes, 
  #   and node at beginning is always root
  # node may be an internal node or an external node
  # return a PathLabel object
  # takes O(log(n)) time
  def getPathLabel(self, node):
    path_from_root = self.getPathFromRoot(node)
    # print path_from_root
    # label_value = self.getPathLabelHelper(path_from_root[1 : ], 0, 0)
    label = self.getPathLabelHelper(path_from_root[1 : ], 0, 0)
    """
    value = label.getValue()
    final_value = value * (3 ** node.getHeight())
    label.setValue(final_value)
    """
    # print label
    numeric_path = label.getNumericPath()
    path_length = label.getPathLength()
    # numeric_path, path_length = label
    next_numeric_path = numeric_path * 3 + 1
    next_path_length = path_length
    """
    label_value = label.getValue()
    # print node.getHeight(), node.getElement().getKey(), node.isExternal()
    # next_label_value = label_value + 1
    # next_label_value = label_value + 1
    next_label = PathLabel(next_numeric_path, next_path_length)
    # next_label = PathLabel(next_label_value)
    # print "label:", label, "entry:", node.getElement().toString()
    # print label
    return next_label
    """
    return label
  """
  # use base three
  # 0 for left child, 1 for current node, 
  #   2 for right child
  """
  # return a PathLabel object
  def getPathLabelHelper(self, path_nodes, partial_numeric_path, partial_path_length):
  # def getPathLabelHelper(self, path_nodes, partial_label_value, start_node):
    # path_size = len(path_from_root)
    path_size = len(path_nodes)
    if path_size == 0:
      # print partial_numeric_path
      # return PathLabel(partial_numeric_path, partial_path_length)
      return PathLabel(partial_numeric_path * 3 + 1, partial_path_length)
      """
    elif path_size == 1:
      return partial_label * 3 + 1
      """
    else:
      # curr_node = path_size[0]
      curr_node = path_nodes[0]
      if curr_node.isLeftChild() == True:
        # return self.getPathLabelHelper(path_nodes[1 : ], partial_numeric_path * 3, partial_path_length + 1)
        return self.getPathLabelHelper(path_nodes[1 : ], partial_numeric_path * 3, partial_path_length + 1)
      elif curr_node.isRightChild() == True:
        # return self.getPathLabelHelper(path_nodes[1 : ], partial_numeric_path * 3 + 2, partial_path_length + 1)
        return self.getPathLabelHelper(path_nodes[1 : ], partial_numeric_path * 3 + 2, partial_path_length + 1)
      # print curr_node, curr_node.isLeftChild(), curr_node.isRightChild()
  # get a list of nodes corresponding 
  #   to a path from root to a node
  # node may be an internal node or an external node
  # takes O(log(n)) time
  def getPathFromRoot(self, node):
    path_nodes = self.getPathFromRootHelper(node)
    result = path_nodes[ : ]
    result.reverse()
    # print len(result)
    return result
  # get a list of nodes corresponding 
  #   to a path from a node to root
  # takes O(log(n)) time
  def getPathFromRootHelper(self, node):
    if node == self.getRoot():
      return [node]
    else:
      return [node] + self.getPathFromRootHelper(node.getParent())
  def buildBalanced(self, nodes):
    # print "rebuilding subtree with subroot that has key:", nodes[0].getElement().getKey()
    return self._buildBalancedHelper(nodes, PathLabeledScapegoatTreeNode)
"""
# note: 17 expected twice
t2 = PathLabeledScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 2)])
# t2 = PathLabeledScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1)])
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(32, 1))
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(65, 1))
print t2.toInorderList()
"""
"""
# find returns an arbitrary match in terms of keys, 
#   not necessarily a particular entry that we are interested in
key_value_pairs = [(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1)]
keys = [x[0] for x in key_value_pairs]
t3 = PathLabeledScapegoatTree.construct(key_value_pairs)
entry_node_pairs = [t3.find(x) for x in keys]
nodes = [x[1] for x in entry_node_pairs]
path_labels = [(x.getElement().getKey(), x.getPathLabel().toString()) for x in nodes]
# make sure to only include unmarked nodes for the rebuilt subtree
unmarked_nodes = [x for x in nodes if x.getMarked() == False]
"""
"""
key_value_pairs = [(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 2)]
# key_value_pairs = [(17, 1), (28, 1), (29, 1), (32, 1), (44, 1)]
t3 = PathLabeledScapegoatTree.construct(key_value_pairs)
print t3.toInorderList()
print t3.toString()
nodes = t3.toInorderInternalNodeList()
# path_labels = [(x.getElement().getKey(), x.getPathLabel().toString()) for x in nodes]
# path_labels = [(x.getElement().getKey(), x.getPathLabel().getValue()) for x in nodes]
path_labels = [(x.getElement().getKey(), PathLabel.toBaseThreeString(x.getPathLabel().getNumericPath()), x.getPathLabel().getPathLength()) for x in nodes]
print path_labels
inorder_internal_node_list = t3.toInorderInternalNodeList()
# inorder_height_list = [x.getHeight() for x in inorder_internal_node_list]
# print inorder_height_list
"""
"""
# print PathLabel.toBaseThreeString(2)
"""
"""
# note: 17 expected twice
# t2 = PathLabeledScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)])
t2 = PathLabeledScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1)])
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(32, 1))
print t2.toString()
print t2.toInorderList()
# t2.remove(LocationAwareEntry(65, 1))
# print t2.toInorderList()
inorder_internal_node_list = t2.toInorderInternalNodeList()
# inorder_height_list = [x.getHeight() for x in inorder_internal_node_list]
# print inorder_height_list
# structure may be deceiving given that we are dealing with lazily-removed nodes
"""
