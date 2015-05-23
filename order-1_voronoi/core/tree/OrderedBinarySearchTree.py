"""

# maintain prev, next, prev_external, next_external 
#   pointers for internal nodes

"""

"""

# maintain prev and next pointers for internal nodes

"""

# maintain prev, next pointers for internal and external nodes

from LocationAwareBinarySearchTree import *

from OrderedBinarySearchTreeNode import *

class OrderedBinarySearchTree(LocationAwareBinarySearchTree):

  def __init__(self, key_transform = lambda x: x, comparator = comp):

    BinarySearchTree.__init__(self, key_transform, comparator)

  def _expandExternal(self, external_node, left_entry, right_entry):
  
    self._expandExternalHelper(external_node, left_entry, right_entry, OrderedBinarySearchTreeNode)
    
  def addRoot(self, entry):

    self._addRootHelper(entry, OrderedBinarySearchTreeNode)

  @staticmethod

  def construct(entries):

    tree = OrderedBinarySearchTree()

    for entry in entries:

      key, value = entry

      tree.insert(key, value)

    return tree

  # takes O(h) time

  def insert(self, key, value):

    # raise Exception()

    result = BinarySearchTree.insert(self, key, value)

    entry, node = result

    prev = self._getPredecessorInternalNode(node)

    next = self._getSuccessorInternalNode(node)

    if prev != None:

      prev.setNext(node)

    node.setPrev(prev)

    node.setNext(next)

    if next != None:

      next.setPrev(node)

    # modify external node children

    node.getLeftChild().setNext(node)

    node.getRightChild().setPrev(node)

    """

    print node.getLeftChild().getNext()

    print node.getRightChild().getPrev()

    """

    """

    prev_external = self._getPredecessorExternalNode(node)

    next_external = self._getSuccessorExternalNode(node)

    node.setPrevExternal(prev_external)

    node.setNextExternal(next_external)

    """

    return result

  # takes O(h) time

  def remove(self, entry):

    key = entry.getKey()

    value = entry.getValue()

    result = BinarySearchTree.find(self, key)

    entry, node = result

    prev = node.getPrev()

    next = node.getNext()

    # modify external node children

    if node.getLeftChild().isExternal() == True:

      node.getLeftChild().setNext(next)

    if node.getRightChild().isExternal() == True:

      node.getRightChild().setPrev(prev)

    result = BinarySearchTree._removeHelper(self, node)

    # result = BinarySearchTree.remove(self, entry)

    entry, node = result

    """

    prev = node.getPrev()

    next = node.getNext()

    """

    if prev != None:

      prev.setNext(next)

    if next != None:

      next.setPrev(prev)

    """

    # modify external node children

    if node.getLeftChild().isExternal() == True:

      node.getLeftChild().setNext(next)

    if node.getRightChild().isExternal() == True:

      node.getRightChild().setPrev(prev)

    """

    return result

  # takes O(1) time

  def getPredecessorInternalNode(self, node):

    return node.getPrev()

  # takes O(1) time

  def getSuccessorInternalNode(self, node):

    return node.getNext()

  # takes O(log(n)) time

  def getPredecessorExternalNode(self, node):

    return self._getPredecessorExternalNode(node)

  # takes O(log(n)) time

  def getSuccessorExternalNode(self, node):

    return self._getSuccessorExternalNode(node)

  def _getMinimumInternalNode(self, node):

    found_node = self._getMinimumInternalNodeHelper(node)

    if found_node == self.getRoot():

      return None

    # expect an external node

    return found_node.getParent()

  def _getMinimumInternalNodeHelper(self, node):

    if node.isExternal() == True:

      return node

    else:

      return self._getMinimumInternalNodeHelper(node.getLeftChild())

  def _getMaximumInternalNode(self, node):

    found_node = self._getMaximumInternalNodeHelper(node)

    if found_node == self.getRoot():

      return None

    # expect an external node

    return found_node.getParent()

  def _getMaximumInternalNodeHelper(self, node):

    if node.isExternal() == True:

      return node

    else:

      return self._getMaximumInternalNodeHelper(node.getRightChild())

  def _getClosestAncestorWithLeftChild(self, node):

    if self.getRoot() == node:

      return None

    else:

      return self._getClosestAncestorWithLeftChildHelper(node, node.getParent())

  def _getClosestAncestorWithLeftChildHelper(self, node, next_node):

    if self.getRoot() == node:

      return None

    elif next_node.hasLeftChild() == True and next_node.getLeftChild() == node:

      return next_node

    else:

      return self._getClosestAncestorWithLeftChildHelper(next_node, next_node.getParent())

  def _getClosestAncestorWithRightChild(self, node):

    if self.getRoot() == node:

      return None

    else:

      return self._getClosestAncestorWithRightChildHelper(node, node.getParent())

  def _getClosestAncestorWithRightChildHelper(self, node, next_node):

    if self.getRoot() == node:

      return None

    elif next_node.hasRightChild() == True and next_node.getRightChild() == node:

      return next_node

    else:

      return self._getClosestAncestorWithRightChildHelper(next_node, next_node.getParent())

  # retrieves a predecessor internal node

  # takes as input a node that is an internal node or an external node

  # returns a node

  # takes O(log(n)) time

  # may return None

  def _getPredecessorInternalNode(self, node):

    if node.isExternal() == True:

      if self.getRoot() == node:

        return None

      else:

        match = self._getClosestAncestorWithRightChild(node)

        return match

    else:

      if node.getLeftChild().isExternal() == False:

        return self._getMaximumInternalNode(node.getLeftChild())

      else:

        match = self._getClosestAncestorWithRightChild(node)

        return match

  # takes O(log(n)) time

  def _getSuccessorInternalNode(self, node):

    if node.isExternal() == True:

      if self.getRoot() == node:

        return None

      else:

        match = self._getClosestAncestorWithLeftChild(node)

        return match

    else:

      if node.getRightChild().isExternal() == False:

        return self._getMinimumInternalNode(node.getRightChild())

      else:

        match = self._getClosestAncestorWithLeftChild(node)

        # print "node", str(node.getElement().getKey()) + ":", match

        return match

  # takes as input a node that is an internal node or an external node

  def _getPredecessorExternalNode(self, node):

    return self._getMaximumExternalNode(node.getLeftChild())

  # takes as input a node that is an internal node or an external node

  def _getSuccessorExternalNode(self, node):

    return self._getMinimumExternalNode(node.getRightChild())

  # takes as input a node that is an internal node or an external node

  # takes O(log(n)) time

  def _getMaximumExternalNode(self, node):

    return self._getMaximumExternalNodeHelper(node)

  def _getMaximumExternalNodeHelper(self, node):

    if node.isExternal() == True:

      return node

    else:

      return self._getMaximumExternalNodeHelper(node.getRightChild())

  # takes as input a node that is an internal node or an external node

  # takes O(log(n)) time

  def _getMinimumExternalNode(self, node):

    return self._getMinimumExternalNodeHelper(node)

  def _getMinimumExternalNodeHelper(self, node):

    if node.isExternal() == True:

      return node

    else:

      return self._getMinimumExternalNodeHelper(node.getLeftChild())

  # takes O(1) time

  def hasPredecessorInternalNode(self, node):

    result = self.getPredecessorInternalNode(node) != None

    return result

  # takes O(1) time

  def hasSuccessorInternalNode(self, node):

    result = self.getSuccessorInternalNode(node) != None

    return result

"""

t1 = OrderedBinarySearchTree.construct([(1, 1), (2, 1), (3, 1), (4, 1)])

print t1.toString()

keys = [1, 2, 3, 4]

entry_node_pairs = [t1.find(x) for x in keys]

nodes = [x[1] for x in entry_node_pairs]

predecessors = [t1.getPredecessorInternalNode(x) for x in nodes]

successors = [t1.getSuccessorInternalNode(x) for x in nodes]

predecessor_str_list = [x.getElement().toString() if x != None else x for x in predecessors]

successor_str_list = [x.getElement().toString() if x != None else x for x in successors]

for i in range(len(nodes)):

  predecessor = predecessor_str_list[i]

  successor = successor_str_list[i]

  print predecessor

  print successor

"""

"""

t2 = OrderedBinarySearchTree.construct([(1, 1), (2, 1), (3, 1), (4, 1)])

print t2.toString()

entry, node = t2.find(2)

predecessor_external_node = t2.getPredecessorExternalNode(node)

successor_external_node = t2.getSuccessorExternalNode(node)

print predecessor_external_node.isLeftChild()

print t2._getSuccessorInternalNode(predecessor_external_node).getElement().toString()

print successor_external_node.isRightChild()

print t2._getPredecessorInternalNode(successor_external_node).getElement().toString()

# print successor_external_node.getParent().getElement().toString()

"""

