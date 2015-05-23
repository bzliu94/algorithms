# for inserts, we make sure that inserted node is unmarked

# for removals, we make sure that we retrieve an unmarked node and mark it

# for finds, we make sure that we return an unmarked node

from OrderedBinarySearchTree import *

from LazyRemoveOrderedBinarySearchTreeNode import *

# we are not concerned with how to remove marked nodes

class LazyRemoveOrderedBinarySearchTree(OrderedBinarySearchTree):

  def __init__(self, key_transform = lambda x: x, comparator = comp):

    OrderedBinarySearchTree.__init__(self, key_transform, comparator)

  def _expandExternal(self, external_node, left_entry, right_entry):
  
    self._expandExternalHelper(external_node, left_entry, right_entry, LazyRemoveOrderedBinarySearchTreeNode)
    
  def addRoot(self, entry):

    self._addRootHelper(entry, LazyRemoveOrderedBinarySearchTreeNode)

  @staticmethod

  def construct(entries):

    tree = LazyRemoveOrderedBinarySearchTree()

    for entry in entries:

      key, value = entry

      tree.insert(key, value)

    return tree

  def find(self, key):

    # return self._findWithRebuilding(key)

    # return BinarySearchTree.find(self, key)

    return OrderedBinarySearchTree.find(self, key)

  def insert(self, key, value):

    # print "key:", key

    # return BinarySearchTree.insert(self, key, value)

    # return self._insertWithRebuilding(key, value)

    # return BinarySearchTree.insert(self, key, value)

    return OrderedBinarySearchTree.insert(self, key, value)

  def remove(self, entry):

    # return BinarySearchTree.remove(self, entry)

    # return self._removeWithRebuilding(entry)

    key = entry.getKey()

    result = self.find(key)

    # print key

    entry, node = result

    node.setMarked(True)

    return result

  # override to deal with marked nodes discreetly; 
  #   returns only external nodes or unmarked nodes

  # takes O(log(n)) time

  def _treeSearch(self, key, node):

    return self._treeSearchForUnmarkedNodes(key, node)

  # return an unmarked node or an external node

  def _treeSearchForUnmarkedNodes(self, key, node):

    # start search off with result of a conventional search

    # node = BinarySearchTree._treeSearch(self, key, node)

    node = OrderedBinarySearchTree._treeSearch(self, key, node)

    if node.isExternal() == True:

      return node

    if node.getMarked() == False:

      return node

    left_match = self.closestUnmarkedPredecessorWithKey(key, node)

    if left_match != None:

      return left_match

    right_match = self.closestUnmarkedSuccessorWithKey(key, node)

    if right_match != None:

      return right_match

    external_node = self.closestPredecessorWithKeyMismatch(key, node)

    return external_node

  def closestUnmarkedPredecessorWithKey(self, key, node):

    if node.getPrev() == None:

      return None

    else:

      return self._closestUnmarkedPredecessorWithKeyHelper(key, node)

  def _closestUnmarkedPredecessorWithKeyHelper(self, key, node):

    if node == None:

      return None

    curr_key = node.getElement().getKey()

    comparator = self.getComparator()

    key_transform = self.getKeyTransform()

    transformed_key = key_transform(key)

    curr_transformed_key = key_transform(curr_key)

    if comparator(transformed_key, curr_transformed_key) == 0:

      if node.getMarked() == False:

        return node

      else:

        return self._closestUnmarkedPredecessorWithKeyHelper(key, node.getPrev())

    else:

      return None

  def closestUnmarkedSuccessorWithKeyHelper(self, key, node):

    if node.getNext() == None:

      return None

    else:

      return self._closestUnmarkedSuccessorWithKeyHelper(key, node.getNext())

  def _closestUnmarkedSuccessorWithKeyHelper(self, key, node):

    if node == None:

      return None

    curr_key = node.getElement().getKey()

    comparator = self.getComparator()

    key_transform = self.getKeyTransform()

    transformed_key = key_transform(key)

    curr_transformed_key = key_transform(curr_key)

    if comparator(transformed_key, curr_transformed_key) == 0:

      if node.getMarked() == False:

        return node

      else:

        return self._closestUnmarkedSuccessorWithKeyHelper(key, node.getNext())

    else:

      return None

  def closestPredecessorWithKeyMismatch(self, key, node):

    if node.getPrev() == None:

      return None

    else:

      return self._closestPredecessorWithKeyMismatch(key, node.getPrev())

  def _closestPredecessorWithKeyMismatch(self, key, node):

    if node == None:

      return None

    curr_key = node.getElement().getKey()

    comparator = self.getComparator()

    key_transform = self.getKeyTransform()

    transformed_key = key_transform(key)

    curr_transformed_key = key_transform(curr_key)

    if comparator(transformed_key, curr_transformed_key) == 0:

      return self._closestUnmarkedPredecessorWithKeyHelper(key, node.getPrev())

    else:

      return node

  # make note of whether items are marked or unmarked

  def toLazyRemoveInorderList(self):

    root = self.getRoot()

    return self._toLazyRemoveInorderListHelper(root)

  def _toLazyRemoveInorderListHelper(self, node):

    if node.isExternal():

      return []

    else:

      left_child = node.getLeftChild()

      right_child = node.getRightChild()

      entry_list_left = []

      entry_list_right = []

      if node.hasLeftChild():

        entry_list_left = self._toLazyRemoveInorderListHelper(left_child)

      curr_entry = node.getElement()

      marked_str = "marked: "

      if node.getMarked() == True:

        marked_str = marked_str + "true"

      else:

        marked_str = marked_str + "false"

      curr_entry_list = [(curr_entry.toString(), marked_str)]

      if node.hasRightChild():

        entry_list_right = self._toLazyRemoveInorderListHelper(right_child)

      entry_list = entry_list_left + curr_entry_list + entry_list_right

      return entry_list

  # get a string representation of entries

  # for nodes visited using in-order traversal

  def toInorderList(self):

    root = self.getRoot()

    return self._toInorderListHelper(root)

  def _toInorderListHelper(self, node):

    if node.isExternal():

      return []

    else:

      left_child = node.getLeftChild()

      right_child = node.getRightChild()

      # print left_child, right_child

      """

      print node.getElement().toString()

      left_child_entry = left_child.getElement()

      if left_child_entry != None:

        print left_child_entry.toString()

      """

      entry_list_left = []

      entry_list_right = []

      if node.hasLeftChild():

        entry_list_left = self._toInorderListHelper(left_child)

      curr_entry = node.getElement()

      """

      curr_entry_list = []

      if curr_entry != None:

        curr_entry_list = [curr_entry.toString()]

      """

      curr_entry_list = []

      if node.getMarked() == False:

        curr_entry_list = [curr_entry.toString()]

      if node.hasRightChild():

        entry_list_right = self._toInorderListHelper(right_child)

      entry_list = entry_list_left + curr_entry_list + entry_list_right

      return entry_list

  # takes O(n) time

  def _toLazyRemoveInorderInternalNodeList(self, node):

    # return self._toLazyRemoveInorderInternalNodeListHelper(self.getRoot())

    return self._toLazyRemoveInorderInternalNodeListHelper(node)

  def _toLazyRemoveInorderInternalNodeListHelper(self, node):

    if node.isExternal():

      return []

    # print node.getElement().toKeyString()

    left_nodes = self._toLazyRemoveInorderInternalNodeListHelper(node.getLeftChild())

    current_nodes = [node]

    right_nodes = self._toLazyRemoveInorderInternalNodeListHelper(node.getRightChild())

    result_nodes = left_nodes + current_nodes + right_nodes

    return result_nodes

  """

  def toInorderInternalNodeList(self):

    # return self._toInorderInternalNodeListHelper(self.getRoot())

    return self._toInorderInternalNodeListHelper(self.getRoot())

  """

  # retrieve internal nodes (that have not been marked)

  # takes O(n) time

  def _toInorderInternalNodeListHelper(self, node):

    if node.isExternal():

      return []

    # print node.getElement().toKeyString()

    left_nodes = self._toInorderInternalNodeListHelper(node.getLeftChild())

    current_nodes = []

    if node.getMarked() == False:

      current_nodes = [node]

    right_nodes = self._toInorderInternalNodeListHelper(node.getRightChild())

    result_nodes = left_nodes + current_nodes + right_nodes

    return result_nodes

"""

t1 = LazyRemoveOrderedBinarySearchTree.construct([(1, 1), (2, 1), (3, 1), (4, 1)])

print t1.toString()

node = t1._treeSearchForUnmarkedNodes(1, t1.getRoot())

print node.getElement().getKey()

print t1.toLazyRemoveInorderList()

print t1.toInorderList()

t1.remove(LocationAwareEntry(1, 1))

print t1.toLazyRemoveInorderList()

print t1.toInorderList()

"""

