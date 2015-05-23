# for rebuilds, we make sure that only unmarked nodes survive

import math

from ..LazyRemoveOrderedBinarySearchTree import *

# structure that revolves around rebuilding

# make certain space, height, running-time guarantees

# allows one to minimize how many paths 
#   get changed for a re-balancing operation

class ScapegoatTree(LazyRemoveOrderedBinarySearchTree):

  def __init__(self, key_transform = lambda x: x, comparator = comp):

    LazyRemoveOrderedBinarySearchTree.__init__(self, key_transform, comparator)

    self.num_unmarked_nodes = 0

    self.num_marked_and_unmarked_nodes = 0

    self.alpha = 2.0 / 3.0

    # print self.alpha

  # takes O(n * log(n)) time

  @staticmethod

  def construct(entries):

    # repeatedly insert items

    tree = ScapegoatTree()

    for entry in entries:

      key, value = entry

      tree.insert(key, value)

    return tree

  # assume number of unmarked nodes is at least one

  def _getDepthBasedOnAlpha(self):

    # depth = math.floor(math.log(max(self.num_unmarked_nodes, 1)) / math.log(1.0 / self.alpha))

    depth = math.floor(math.log(self.num_unmarked_nodes) / math.log(1.0 / self.alpha))

    # print depth

    # depth = math.ceil(math.log(max(self.num_unmarked_nodes, 1)) / math.log(1.0 / self.alpha))

    return depth

  def _rebuildlessFind(self, key):

    result = LazyRemoveOrderedBinarySearchTree.find(self, key)

    # return self._findWithRebuilding(key)

    return result

  def _rebuildlessInsert(self, key, value):

    """

    # print "key:", key

    # return BinarySearchTree.insert(self, key, value)

    """

    result = LazyRemoveOrderedBinarySearchTree.insert(self, key, value)

    # result.setMarked(False)

    # update counts

    self.num_unmarked_nodes = self.num_unmarked_nodes + 1

    self.num_marked_and_unmarked_nodes = self.num_marked_and_unmarked_nodes + 1

    # self._rebuildForInsert(key, value)

    return result

  def _rebuildlessRemove(self, entry):

    # return BinarySearchTree.remove(self, entry)

    result = LazyRemoveOrderedBinarySearchTree.remove(self, entry)

    # update counts

    self.num_unmarked_nodes = self.num_unmarked_nodes - 1

    # self._rebuildForRemove(entry)

    return result

  """  

  def _treeSearchForUnmarkedNodesResultIsSatisfactory(self, node):

    return node.isExternal() == True or node.getMarked() == True

  def _treeSearchForUnmarkedNodesHelper(self, key, node):

    # repeatedly perform a conventional search, 
    #   but in an organized way

    if self._treeSearchForUnmarkedNodesResultIsSatisfactory(node):

      return node

    else:

      left_branch_result = self._treeSearch(key, node.getLeftChild())

      tentative_result = self._treeSearchForUnmarkedNodesHelper(key, left_branch_result)

      if tentative_result.isExternal() == False:

        return tentative_result

      right_branch_result = self._treeSearch(key, node.getRightChild())

      tentative_result = self._treeSearchForUnmarkedNodesHelper(key, right_branch_result)

      # if tentative_result.isExternal() == False:

      return tentative_result

  """

  """

  # return an (entry, node) pair

  def _findUnmarked(self, key):

  def findUnmarked

    node = self._treeSearch(key, self.getRoot())

    if node.isExternal() == True:

      

    self.action_node = node

    if node.isInternal() == True:

      entry = node.getElement()

      return (entry, node)

    else:

      return None

  """

  def find(self, key):

    result = self._rebuildlessFind(key)

    self._rebuildForFind(key)

    return result

  def insert(self, key, value):

    result = self._rebuildlessInsert(key, value)

    self._rebuildForInsert(key, value)

    return result

  def remove(self, entry):

    result = self._rebuildlessRemove(entry)

    self._rebuildForRemove(entry)

    return result

  def _rebuildForFind(self, key):

    # target_node = self.action_node

    pass

  # makes use of a technique called local rebuilding

  # takes O(log(n)) amortized time

  def _rebuildForInsert(self, key, value):

    target_node = self.action_node

    # possibly locally rebuild

    # check depth of subtree rooted at inserted node

    subtree_depth = self._getDepth(target_node)

    # check whether there will be a scapegoat along path 
    #   from node to root

    node_is_deep = subtree_depth > self._getDepthBasedOnAlpha()

    # print subtree_depth, self._getDepthBasedOnAlpha(), is_unbalanced

    # print is_unbalanced

    # find a scapegoat

    # rebuild subtree rooted at scapegoat

    # further maintain counts

    if node_is_deep == True:

      scapegoat_node = self._getScapegoatNodeGivenActionNode(target_node)

      # print "overall tree:", self.toString()

      self.localRebuild(scapegoat_node)

  # makes use of a technique called global rebuilding

  # takes O(log(n)) amortized time

  def _rebuildForRemove(self, entry):

    target_node = self.action_node

    # possibly globally rebuild

    # check how many marked and unmarked nodes there are

    # rebuild entire tree if have enough marked nodes

    # further maintain counts

    # print self.num_unmarked_nodes, self.alpha * self.num_marked_and_unmarked_nodes

    if self.num_unmarked_nodes < self.alpha * self.num_marked_and_unmarked_nodes:

      self.globalRebuild()

      self.num_marked_and_unmarked_nodes = self.num_unmarked_nodes

  # assume u is an internal node

  def _nodeIsBalanced(self, u):

    left_child = u.getLeftChild()

    right_child = u.getRightChild()

    left_child_size = ScapegoatTree._getSize(left_child)

    right_child_size = ScapegoatTree._getSize(right_child)

    curr_size = ScapegoatTree._getSize(u)

    left_child_is_balanced = left_child_size <= self.alpha * curr_size

    right_child_is_balanced = right_child_size <= self.alpha * curr_size

    is_balanced = left_child_is_balanced and right_child_is_balanced

    return is_balanced

  # may return None, if no node along path from 
  #   node to root qualifies as scapegoat

  def _getScapegoatNodeGivenActionNode(self, action_node):

    if action_node == self.getRoot():

      return None

    else:

      # print action_node

      return self._getScapegoatNodeGivenActionNodeHelper(action_node.getParent())

  def _getScapegoatNodeGivenActionNodeHelper(self, node):

    if node.isExternal() == True:

      if node == self.getRoot():

        return None

      else:

        return self._getScapegoatNodeGivenActionNodeHelper(node.getParent())

    else:      

      curr_node_is_balanced = self._nodeIsBalanced(node)

      if curr_node_is_balanced == False:

        return node

      elif node == self.getRoot():

        return None

      else:

        return self._getScapegoatNodeGivenActionNodeHelper(node.getParent())

  # def _insertWithRebuilding(self, u):

  # def _removeHelper(self, x):

  # takes O(n) time

  # return root of the rebuilt subtree

  def localRebuild(self, u):

    # print "key of u:", u.getElement().toString()

    # print "locally rebuilding"

    """

    parent = u.getParent()

    if parent == None:

      r = buildBalanced(n, u)

      r.parent = None

    elif u.isRightChild() == True:

      next_subtree_root = buildBalanced(n, u)

      parent.right = next_subtree_root

      next_subtree_root.parent = parent

    elif u.isLeftChild() == True:

      next_subtree_root = buildBalanced(n, u)

      parent.left = next_subtree_root

      next_subtree_root.parent = parent

    """

    # care about retrieving parent before rebuilding, 
    #   since we re-use existing nodes when re-arranging

    parent = u.getParent()

    # care about retrieving information about whether a node 
    #   is a left child or a right child before rebuilding, 
    #   since we re-use existing nodes when re-arranging

    is_left_child = u.isLeftChild()

    is_right_child = u.isRightChild()

    # print "parent key:", parent.getElement().toString()

    nodes = self.flatten(u)

    # make sure to only include unmarked nodes for the rebuilt subtree

    unmarked_nodes = [x for x in nodes if x.getMarked() == False]

    # print "before:", [x.getElement().toString() for x in nodes]

    # subtree_root = self.buildBalanced(nodes)

    subtree_root = self.buildBalanced(unmarked_nodes)

    # print "subtree:", self._toString(subtree_root)

    # print "overall tree:", self.toString()

    # print u, self.getRoot()

    # print u.getElement().toString(), self.getRoot().getElement().toString()

    if u == self.getRoot():

      # print "subtree root:", subtree_root

      # print self._getSize(subtree_root)

      self._setRoot(subtree_root)

      # print "subtree for a node that is root:", self._toString(subtree_root)

    elif is_left_child == True:

      # in case of local rebuilding, u is scapegoat node

      # after rebuilding, u may be within subtree

      # in this case, u's parent may no longer be appropriate parent 

      # for next root of subtree

      # parent = u.getParent()

      # print subtree_root.getElement().toString()

      parent.setLeftChild(subtree_root)

      subtree_root.setParent(parent)

      # print "subtree for a node that is left child:", self._toString(subtree_root)

    elif is_right_child == True:

      # parent = u.getParent()

      parent.setRightChild(subtree_root)

      subtree_root.setParent(parent)

      # print "subtree for a node that is right child:", self._toString(subtree_root)

    return subtree_root

  # takes O(n) time

  def globalRebuild(self):

    # print "globally rebuilding"

    return self.localRebuild(self.getRoot())

  # always retrieve a list with at least one node 
  # (i.e. when subtree has size zero, retrieve a placeholder node)

  # takes O(n) time

  def flatten(self, node):

    # print "flattening"

    return self._toInorderInternalNodeListHelper(node)

  # view as partitioning for an in-place sort, 
  # without the effort expended for sorting, 
  # as it has been done ahead of time

  # rebuild a subtree

  # account for fact that node provided may be root

  # takes O(n) time

  def buildBalanced(self, nodes):

    return self._buildBalancedHelper(nodes, LazyRemoveOrderedBinarySearchTreeNode)

  def _buildBalancedHelper(self, nodes, node_class):

    # print [x.getElement().toString() for x in nodes]

    num_nodes = len(nodes)

    if num_nodes == 0:

      # return a placeholder

      node = node_class(None, None, None, None)

      return node

      """

    elif num_nodes == 1:

      # return a node with two placeholders

      left_child = node_class(None, None, None, None)

      right_child = node_class(None, None, None, None)

      node = nodes[0]

      left_child.setParent(node)

      right_child.setParent(node)

      node.setLeftChild(left_child)

      node.setRightChild(right_child)

      return node

      """

      """

    else:

      """

    elif num_nodes >= 1:

      # have at least one child

      num_left_nodes = int(math.ceil((num_nodes - 1) / 2.0))

      num_right_nodes = num_nodes - 1 - num_left_nodes

      # choose a node that may be described as acting as a "pivot"

      node = nodes[num_left_nodes]

      # print num_left_nodes, num_right_nodes

      # build subtree corresponding to left child

      left_nodes = nodes[0 : num_left_nodes]

      # print "left nodes:", [x.getElement().toString() for x in left_nodes]

      left_node = self._buildBalancedHelper(left_nodes, node_class)

      # print "left subtree:", self._toString(left_node)

      # print "left subtree size:", self._getSize(left_node)

      node.setLeftChild(left_node)

      left_node.setParent(node)

      # build subtree corresponding to right child

      right_nodes = nodes[num_left_nodes + 1 : ]

      # print "right nodes:", [x.getElement().toString() for x in right_nodes]

      right_node = self._buildBalancedHelper(right_nodes, node_class)

      # print "right subtree:", self._toString(right_node)

      # print "right subtree size:", self._getSize(right_node)

      node.setRightChild(right_node)

      right_node.setParent(node)

      return node

  def toInorderList(self):

    return BinarySearchTree.toInorderList(self)

  # takes O(log(n)) time

  def _getDepth(self, node):

    return self._getDepthHelper(node)

  def _getDepthHelper(self, node):

    if node == self.getRoot():

      return 0

    else:

      return self._getDepthHelper(node.getParent()) + 1

  # takes O(n) time

  # get size in terms of non-placeholder nodes

  @staticmethod

  def _getSize(node):

    if node.isExternal() == True:

      return 0

    else:

      left_count = 0

      right_count = 0

      if node.hasLeftChild() == True:

        left_count = ScapegoatTree._getSize(node.getLeftChild())

      if node.hasRightChild() == True:

        right_count = ScapegoatTree._getSize(node.getRightChild())

      return left_count + 1 + right_count

"""

# note: 17 expected twice

t2 = ScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)])

# t2 = ScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1)])

print t2.toString()

print t2.toInorderList()

t2.remove(LocationAwareEntry(32, 1))

print t2.toString()

print t2.toInorderList()

t2.remove(LocationAwareEntry(65, 1))

print t2.toInorderList()

"""

"""

t4 = ScapegoatTree.construct([(17, 1), (28, 1), (29, 1)])

print t4.toInorderList()

print t4.toString()

t4.remove(LocationAwareEntry(28, 1))

t4.remove(LocationAwareEntry(17, 1))

# t4.remove(LocationAwareEntry(32, 1))

print t4.toInorderList()

print t4.toString()

"""

"""

t5 = ScapegoatTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1)])

print t5.toString()

print t5.toInorderList()

t5.remove(LocationAwareEntry(17, 1))

t5.remove(LocationAwareEntry(28, 1))

t5.remove(LocationAwareEntry(29, 1))

t5.remove(LocationAwareEntry(32, 1))

print t5.toString()

print t5.toInorderList()

"""

