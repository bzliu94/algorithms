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
  def construct(entries, key_transform = lambda x: x, comparator = comp):
    tree = OrderedBinarySearchTree(key_transform, comparator)
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def insert(self, key, value):
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
    return result
  def remove(self, entry):
    result = BinarySearchTree.remove(self, entry)
    entry, node = result
    prev = node.getPrev()
    next = node.getNext()
    if prev != None:
      prev.setNext(next)
    if next != None:
      next.setPrev(prev)
    return result
  def getPredecessorInternalNode(self, node):
    return node.getPrev()
  def getSuccessorInternalNode(self, node):
    return node.getNext()
  def getPredecessorExternalNode(self, node):
    return self._getPredecessorExternalNode(node)
  def getSuccessorExternalNode(self, node):
    return self._getSuccessorExternalNode(node)
  def _getMinimumInternalNode(self, node):
    found_node = self._getMinimumInternalNodeHelper(node)
    if found_node == self.getRoot():
      return None
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
        return match
  def _getPredecessorExternalNode(self, node):
    return self._getMaximumExternalNode(node.getLeftChild())
  def _getSuccessorExternalNode(self, node):
    return self._getMinimumExternalNode(node.getRightChild())
  def _getMaximumExternalNode(self, node):
    return self._getMaximumExternalNodeHelper(node)
  def _getMaximumExternalNodeHelper(self, node):
    if node.isExternal() == True:
      return node
    else:
      return self._getMaximumExternalNodeHelper(node.getRightChild())
  def _getMinimumExternalNode(self, node):
    return self._getMinimumExternalNodeHelper(node)
  def _getMinimumExternalNodeHelper(self, node):
    if node.isExternal() == True:
      return node
    else:
      return self._getMinimumExternalNodeHelper(node.getLeftChild())
  def hasPredecessorInternalNode(self, node):
    result = self.getPredecessorInternalNode(node) != None
    return result
  def hasSuccessorInternalNode(self, node):
    result = self.getSuccessorInternalNode(node) != None
    return result
  def doLeftBoundaryQuery(self, left_boundary_key):
    node = self._treeSearch(left_boundary_key, self.getRoot())
    base_node = None
    if node.isExternal() == True:
      base_node = node.getParent()
    elif node.isInternal() == True:
      base_node = node
    return self.doLeftBoundaryQueryHelper(base_node, base_node, left_boundary_key)
  def doLeftBoundaryQueryHelper(self, curr_internal_node, best_internal_node, left_boundary_key):
    if curr_internal_node == None:
      return best_internal_node
    else:
      curr_key = curr_internal_node.getElement().getKey()
      comparator = self.getComparator()
      key_transform = self.getKeyTransform()
      transformed_key = key_transform(left_boundary_key)
      curr_transformed_key = key_transform(curr_key)
      if comparator(curr_transformed_key, transformed_key) <= 0:
        return best_internal_node
      else:
        predecessor = self.getPredecessorInternalNode(curr_internal_node)
        return self.doLeftBoundaryQueryHelper(predecessor, curr_internal_node, left_boundary_key)
  def doRightBoundaryQuery(self, right_boundary_key):
    node = self._treeSearch(right_boundary_key, self.getRoot())
    base_node = None
    if node.isExternal() == True:
      base_node = node.getParent()
    elif node.isInternal() == True:
      base_node = node
    return self.doRightBoundaryQueryHelper(base_node, base_node, right_boundary_key)
  def doRightBoundaryQueryHelper(self, curr_internal_node, best_internal_node, right_boundary_key):
    if curr_internal_node == None:
      return best_internal_node
    else:
      curr_key = curr_internal_node.getElement().getKey()
      comparator = self.getComparator()
      key_transform = self.getKeyTransform()
      transformed_key = key_transform(right_boundary_key)
      curr_transformed_key = key_transform(curr_key)
      if comparator(curr_transformed_key, transformed_key) >= 0:
        return best_internal_node
      else:
        successor = self.getSuccessorInternalNode(curr_internal_node)
        return self.doRightBoundaryQueryHelper(successor, curr_internal_node, right_boundary_key)
  def getDisjointSubtreeRootsForRange(self, left_boundary_key, right_boundary_key):
    left_internal_node = self.doLeftBoundaryQuery(left_boundary_key)
    right_internal_node = self.doRightBoundaryQuery(right_boundary_key)
    if left_internal_node == right_internal_node == None:
      return []
    if left_internal_node == right_internal_node:
      node = left_internal_node
      result = [(2, node)]
      return result
    ancestors1 = self.getLenientAncestors(left_internal_node)
    ancestors2 = self.getLenientAncestors(right_internal_node)
    lca = self.getLCA(left_internal_node, right_internal_node)
    lca_index1 = ancestors1.index(lca)
    culled_ancestors1 = ancestors1[ : lca_index1]
    lca_index2 = ancestors2.index(lca)
    culled_ancestors2 = ancestors2[ : lca_index2]
    subtree_roots = []
    left_tagged_nodes = self.GDSRFRLeftHelper(left_internal_node, left_boundary_key, culled_ancestors1)
    right_tagged_nodes = self.GDSRFRRightHelper(right_internal_node, right_boundary_key, culled_ancestors2)
    result = left_tagged_nodes + [(2, lca)] + right_tagged_nodes
    return result
  def GDSRFRLeftHelper(self, internal_node, left_boundary_key, left_non_lca_lenient_ancestors):
    result = []
    prev_ancestor = None
    for ancestor in left_non_lca_lenient_ancestors:
      curr_key = ancestor.getElement().getKey()
      comparator = self.getComparator()
      key_transform = self.getKeyTransform()
      transformed_key = key_transform(left_boundary_key)
      curr_transformed_key = key_transform(curr_key)
      if comparator(transformed_key, curr_transformed_key) <= 0:
        result.append((2, ancestor))
      right_child = ancestor.getRightChild()
      if ancestor.hasRightChild() == True and prev_ancestor != right_child and right_child.isInternal() == True:
        result.append((1, right_child))
      prev_ancestor = ancestor
    return result
  def GDSRFRRightHelper(self, internal_node, right_boundary_key, right_non_lca_lenient_ancestors):
    result = []
    prev_ancestor = None
    for ancestor in right_non_lca_lenient_ancestors:
      curr_key = ancestor.getElement().getKey()
      comparator = self.getComparator()
      key_transform = self.getKeyTransform()
      transformed_key = key_transform(right_boundary_key)
      curr_transformed_key = key_transform(curr_key)
      if comparator(transformed_key, curr_transformed_key) >= 0:
        result.append((2, ancestor))
      left_child = ancestor.getLeftChild()
      if ancestor.hasLeftChild() == True and prev_ancestor != left_child and left_child.isInternal() == True:
        result.append((1, left_child))
      prev_ancestor = ancestor
    next_result = list(reversed(result))
    return next_result
  def getMinimalKeyValue(self):
    leftmost_internal_node = self._getMinimumInternalNode(self.getRoot())
    if leftmost_internal_node == None or leftmost_internal_node.isExternal() == True:
      return None
    else:
      key = leftmost_internal_node.getElement().getKey()
      return key
  def getMaximalKeyValue(self):
    rightmost_internal_node = self._getMaximumInternalNode(self.getRoot())
    if rightmost_internal_node == None or rightmost_internal_node.isExternal() == True:
      return None
    else:
      key = rightmost_internal_node.getElement().getKey()
      return key
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
print "left boundary:", t2.doLeftBoundaryQuery(1.5).toString()
print "right boundary:", t2.doRightBoundaryQuery(3.5).toString()
# if we don't see type-i, this means we don't have internal nodes where we care about whole left subtree, whole right subtree, and current node
result = t2.getDisjointSubtreeRootsForRange(4, 4)
print [(x[0], x[1].toString()) for x in result]
"""
"""
class Container:
  def __init__(self, value):
    self.value = value
  def getValue(self):
    return self.value
"""
"""
t2b = OrderedBinarySearchTree.construct([(1, 1), (2, 1), (3, 1), (3, 1), (4, 1), (5, 1), (1, 1)])
print t2b.toString()
result = t2b.getDisjointSubtreeRootsForRange(1, 3)
print [(x[0], x[1].toString()) for x in result]
"""
"""
t2c = OrderedBinarySearchTree.construct([(Container(1), 1), (Container(2), 1), (Container(3), 1)], lambda x: x.getValue())
print t2c.toString()
result = t2c.getDisjointSubtreeRootsForRange(Container(2), Container(3))
print [(x[0], x[1].toString()) for x in result]
"""
