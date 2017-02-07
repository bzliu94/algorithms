from ...tree.bbst.ScapegoatTree import *
from HeightAwareScapegoatTreeNode import *
class HeightAwareScapegoatTree(ScapegoatTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    ScapegoatTree.__init__(self, key_transform, comparator)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, HeightAwareScapegoatTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, HeightAwareScapegoatTreeNode)
  @staticmethod
  def construct(entries):
    tree = HeightAwareScapegoatTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def _rebuildlessFind(self, key):
    result = ScapegoatTree._rebuildlessFind(self, key)
    entry, node = result
    return result
  """
  def find(self, key):
    pass
  def insert(self, key, value):
    pass
  def remove(self, entry):
    pass
  """
  def _rebuildlessInsert(self, key, value):
    # result = ScapegoatTree.insert(self, key, value)
    result = ScapegoatTree._rebuildlessInsert(self, key, value)
    entry, node = result
    # action node after an insert is different from inserted node
    target_node = self.action_node
    # print node.getElement().getKey()
    # print "key:", key
    # print "target node key:", target_node.getElement().getKey()
    # update heights starting at inserted node
    self._updateHeightValuesForParents(target_node)
    """
    # print target_node == node
    # target_node.getHeight() == None
    ScapegoatTree._rebuildForInsert(self, key, value)
    """
    return result
  def _rebuildlessRemove(self, entry):
    # result = ScapegoatTree.remove(self, entry)
    result = ScapegoatTree._rebuildlessRemove(self, entry)
    entry, node = result
    # action node after a remove is likely sibling of replacement for removed node
    target_node = self.action_node
    # update heights starting at sibling of replacement for removed node
    self._updateHeightValuesForParents(target_node)
    """
    ScapegoatTree._rebuildForRemove(self, entry)
    """
    return result
  def localRebuild(self, u):
    subtree_root = ScapegoatTree.localRebuild(self, u)
    self._updateHeightValuesForSubtree(subtree_root)
    self._updateHeightValuesForParents(subtree_root)
    return subtree_root
  # assume that node is internal
  def _updateHeightValuesForSubtree(self, node):
    self._updateHeightValuesForSubtreeHelper(node)
  def _updateHeightValuesForSubtreeHelper(self, node):
    if node.isExternal() == True:
      return 0
    else:
      left_child_height = self._updateHeightValuesForSubtreeHelper(node.getLeftChild())
      right_child_height = self._updateHeightValuesForSubtreeHelper(node.getRightChild())
      height = max(left_child_height, right_child_height) + 1
      node.setHeight(height)
      return height
  """
  def _rebuildForInsert(self, key, value):
    result = ScapegoatTree._rebuildForInsert(self, key, value)
    return result
  def _rebuildForRemove(self, entry):
    result = ScapegoatTree._rebuildForRemove(self, entry)
    return result
  """
  def buildBalanced(self, nodes):
    return self._buildBalancedHelper(nodes, HeightAwareScapegoatTreeNode)
  # assume that children have valid height values
  # assume that node is internal
  def getHeightUsingChildren(self, node):
    return self._getHeightUsingChildrenHelper(node)
  def _getHeightUsingChildrenHelper(self, node):
    if node.isExternal() == True:
      return 0
    else:
      left_child = node.getLeftChild()
      right_child = node.getRightChild()
      left_child_height = None
      right_child_height = None
      if left_child.isExternal() == False:
        left_child_height = left_child.getHeight()
      else:
        left_child_height = 0
      if right_child.isExternal() == False:
        right_child_height = right_child.getHeight()
      else:
        right_child_height = 0
      max_height = max(left_child_height, right_child_height) + 1
      return max_height
  """
  def _getHeightHelper(self, node):
    if self.getRoot() == node:
      return 0
    else:
      return self._getDepthHelper(node.getParent()) + 1
  """
  def _updateHeightValuesForParentsHelper(self, node, curr_height):
    # print node.getElement().getKey()
    # print curr_height
    node.setHeight(curr_height)
    if self.getRoot() == node:
      return
    else:
      self._updateHeightValuesForParentsHelper(node.getParent(), curr_height + 1)
  # update height values for node and its parents
  def _updateHeightValuesForParents(self, node):
    # print node.getElement().getKey()
    curr_height = self.getHeightUsingChildren(node)
    self._updateHeightValuesForParentsHelper(node, curr_height)
"""
# note: 17 expected twice
t2 = HeightAwareScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)])
# t2 = HeightAwareScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1)])
print t2.toString()
print t2.toInorderList()
t2.remove(Entry(32, 1))
print t2.toString()
print t2.toInorderList()
t2.remove(Entry(65, 1))
print t2.toString()
print t2.toInorderList()
inorder_internal_node_list = t2.toInorderInternalNodeList()
inorder_height_list = [x.getHeight() for x in inorder_internal_node_list]
print inorder_height_list
"""
