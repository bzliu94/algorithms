# splay ought to not be called on a placeholder node, 
# lest it become root
from ..OrderedBinarySearchTree import *
from ..Entry import *
class SplayTree(OrderedBinarySearchTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    # BinarySearchTree.__init__(self, key_transform, comparator)
    OrderedBinarySearchTree.__init__(self, key_transform, comparator)
  @staticmethod
  def construct(entries):
    tree = SplayTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  # return whether we have a non-placeholder node to splay
  def _oughtToSplay(self, action_node):
    return not (action_node.isExternal() and action_node == self.getRoot())
  # candidates include current node and ancestors; 
  #   we are interested in the closest such node
  # if there is no non-placeholder node among these candidates, 
  #   return None
  def _getNodeToSplayGivenActionNode(self, action_node):
    return self._getNodeToSplayGivenActionNodeHelper(action_node)
  def _getNodeToSplayGivenActionNodeHelper(self, node):
    if not node.isExternal():
      return node
    else:
      if node == self.getRoot():
        return None
      else:
        return self._getNodeToSplayGivenActionNodeHelper(node.getParent())
  def _splayGivenActionNode(self, node):
    if self._oughtToSplay(node) == True:
      node_to_splay = self._getNodeToSplayGivenActionNode(node)
      self._splay(node_to_splay)
  def _splay(self, x):
    # if is left child of a left child, or right child of a right child
    # if is left child of a right child, or right child of a left child
    # if does not have a grandparent
    # print "splaying"
    parent = x.getParent()
    if parent == None:
      return
    grandparent = parent.getParent()
    if grandparent == None:
      self._zig(x)
    elif (x.isLeftChild() and parent.isLeftChild()) \
      or (x.isRightChild() and parent.isRightChild()):
      self._zig_zig(x)
    elif (x.isLeftChild() and parent.isRightChild()) \
      or (x.isRightChild() and parent.isLeftChild()):
      self._zig_zag(x)
    self._splay(x)
  def _zig_zig(self, x):
    # print "zig-zig"
    # x, y, z
    # replace z by x
    # make x have y as a child
    # make y have z as a child
    y = x.getParent()
    z = y.getParent()
    z_parent = z.getParent()
    z_has_parent = z.hasParent()
    if x.isLeftChild() == True:
      # print "left, left"
      # left, left
      t1 = x.getLeftChild()
      t2 = x.getRightChild()
      t3 = y.getRightChild()
      t4 = z.getRightChild()
      self._upperSituate(x, z)
      self._lowerSituate(t1, x)
      self._lowerSituate(t2, y)
      self._lowerSituate(t3, z)
      self._lowerSituate(t4, z)
      x.setLeftChild(t1)
      x.setRightChild(y)
      x.setParent(z_parent)
      y.setLeftChild(t2)
      y.setRightChild(z)
      y.setParent(x)
      z.setLeftChild(t3)
      z.setRightChild(t4)
      z.setParent(y)
    else:
      # print "right, right"
      # right, right
      t1 = z.getLeftChild()
      t2 = y.getLeftChild()
      t3 = x.getLeftChild()
      t4 = x.getRightChild()
      self._upperSituate(x, z)
      self._lowerSituate(t1, z)
      self._lowerSituate(t2, z)
      self._lowerSituate(t3, y)
      self._lowerSituate(t4, x)
      z.setLeftChild(t1)
      z.setRightChild(t2)
      z.setParent(y)
      y.setLeftChild(z)
      y.setRightChild(t3)
      y.setParent(x)
      x.setLeftChild(y)
      x.setRightChild(t4)
      x.setParent(z_parent)
  def _zig_zag(self, x):
    # print "zig-zag"
    # x, y, z
    # replace z by x
    # make x have y and z as children
    y = x.getParent()
    z = y.getParent()
    z_parent = z.getParent()
    z_has_parent = z.hasParent()
    if x.isRightChild() == True:
      # left, right
      t1 = y.getLeftChild()
      t2 = x.getLeftChild()
      t3 = x.getRightChild()
      t4 = z.getRightChild()
      self._upperSituate(x, z)
      self._lowerSituate(t1, y)
      self._lowerSituate(t2, y)
      self._lowerSituate(t3, z)
      self._lowerSituate(t4, z)
      y.setLeftChild(t1)
      y.setRightChild(t2)
      y.setParent(x)
      x.setLeftChild(y)
      x.setRightChild(z)
      x.setParent(z_parent)
      z.setLeftChild(t3)
      z.setRightChild(t4)
      z.setParent(x)
    else:
      # right, left
      t1 = z.getLeftChild()
      t2 = x.getLeftChild()
      t3 = x.getRightChild()
      t4 = y.getRightChild()
      self._upperSituate(x, z)
      self._lowerSituate(t1, z)
      self._lowerSituate(t2, z)
      self._lowerSituate(t3, y)
      self._lowerSituate(t4, y)
      z.setLeftChild(t1)
      z.setRightChild(t2)
      z.setParent(x)
      x.setLeftChild(z)
      x.setRightChild(y)
      x.setParent(z_parent)
      y.setLeftChild(t3)
      y.setRightChild(t4)
      y.setParent(x)
  # x might be an external node
  def _zig(self, x):
    # print "zig"
    # print x.getElement().toString()
    # x, y, w
    # make x have y and w as children
    y = x.getParent()
    w1 = x.getLeftChild()
    w2 = x.getRightChild()
    y_parent = y.getParent()
    y_has_parent = y.hasParent()
    # print x.getElement().toString()
    if x.isLeftChild() == True:
      # print "left"
      # left
      t3 = x.getRightChild()
      t4 = y.getRightChild()
      self._upperSituate(x, y)
      self._lowerSituate(t3, y)
      self._lowerSituate(t4, y)
      x.setLeftChild(w1)
      x.setRightChild(y)
      x.setParent(y_parent)
      y.setLeftChild(t3)
      y.setRightChild(t4)
      y.setParent(x)
    else:
      # print "right"
      # right
      t1 = y.getLeftChild()
      t2 = x.getLeftChild()
      self._upperSituate(x, y)
      self._lowerSituate(t1, y)
      self._lowerSituate(t2, y)
      y.setLeftChild(t1)
      y.setRightChild(t2)
      y.setParent(x)
      # print y.getElement().getKey()
      x.setLeftChild(y)
      x.setRightChild(w2)
      x.setParent(y_parent)
      # print x.getLeftChild() == x
      # print x.getLeftChild().getElement().getKey()
      # print self.getRoot().getElement().getKey()
  # return an (entry, node) pair
  def _findWithSplay(self, key, bst_find):
    """
    entry = bst_find(key)
    # perform splaying on lowest accessed node
    target_node = self.action_node
    self._splay(target_node)
    """
    result = bst_find(key)
    # perform splaying on lowest accessed node
    target_node = self.action_node
    self._splayGivenActionNode(target_node)
    return result
  # return an (entry, node) pair
  def find(self, key):
    # bst_find = lambda x: BinarySearchTree.find(self, x)
    bst_find = lambda x: BinarySearchTree.find(self, x)
    return self._findWithSplay(key, bst_find)
    """
    tree_search = BinarySearchTree._treeSearch
    return (self._findWithSplay(key, tree_search))[0]
    return self._findWithSplay(key)
    """
  # return an (entry, node) pair
  def _insertWithSplay(self, key, value, bst_insert):
    result = bst_insert(key, value)
    # perform splaying on lowest accessed node
    target_node = self.action_node
    # self._splay(target_node)
    self._splayGivenActionNode(target_node)
    return result
  # return an (entry, node) pair
  def insert(self, untransformed_key, value):
    # bst_insert = lambda key, value: BinarySearchTree.insert(self, key, value)
    bst_insert = lambda key, value: OrderedBinarySearchTree.insert(self, key, value)
    return self._insertWithSplay(untransformed_key, value, bst_insert)
  """
  def insertWithUntransformedKey(self, key, value):
    bst_insert = lambda x: BinarySearchTree.insertWithUntransformedKey(self, x)
    return self._insertWithSplay(key, value, bst_insert)
  """
  # return an (entry, node) pair
  def _removeWithSplay(self, entry, bst_remove):
    """
    bst_remove(entry)
    # perform splaying on lowest accessed node
    target_node = self.action_node
    self._splay(target_node)
    """
    result = bst_remove(entry)
    # perform splaying on lowest accessed node
    target_node = self.action_node
    self._splayGivenActionNode(target_node)
    return result
  # remove an entry with matching (transformed) key
  # note: entry provided should involve untransformed key
  # return an (entry, node) pair
  def remove(self, entry):
    # bst_remove = lambda x: BinarySearchTree.remove(self, x)
    # bst_remove = lambda entry: BinarySearchTree.remove(self, entry)
    bst_remove = lambda entry: OrderedBinarySearchTree.remove(self, entry)
    return self._removeWithSplay(entry, bst_remove)
    """
    tree_search = BinarySearchTree._treeSearch
    return (self._removeWithSplay(entry, tree_search))[0]
    """
  """
  def remove(self, entry_with_transformed_key):
    # bst_remove = lambda x: BinarySearchTree.remove(self, x)
    bst_remove = lambda entry: BinarySearchTree.remove(self, entry)
    return self._removeWithSplay(entry_with_transformed_key, bst_remove)
    # tree_search = BinarySearchTree._treeSearch
    # return (self._removeWithSplay(entry_with_untransformed_key, tree_search))[0]
  """
  """
  # remove an entry with matching untransformed key
  # return an (entry, node) pair
  def removeWithUntransformedKey(self, entry_with_untransformed_key):
    transform = self.getKeyTransform()
    key = entry_with_untransformed_key.getKey()
    value = entry_with_untransformed_key.getValue()
    # key, value = entry_with_untransformed_key
    transformed_key = transform(key)
    # arbitrarily create an entry object
    # entry_with_transformed_key = transformed_key, value
    entry_with_transformed_key = LocationAwareEntry(transformed_key, value)
    return self.remove(entry_with_transformed_key)
  """
  """
    # bst_remove = lambda x: BinarySearchTree.removeWithUntransformedKey(self, x)
    # return self._removeWithSplay(entry_with_untransformed_key, bst_remove)
  """
  """
    # tree_search = BinarySearchTree._treeSearchWithoutTransformedKey
    # return (self._removeWithSplay(entry_with_untransformed_key, tree_search))[0]
  """
  """
  def _treeSearchWithBalancingWithSplay(self, key, node, tree_search):
    result_node = tree_search(key, node)
    self.action_node = result_node
    # perform splaying on lowest accessed node
    target_node = self.action_node
    self._splayGivenActionNode(target_node)
    return result_node
  # this method is to be considered protected, not private
  def _treeSearchWithBalancing(self, key, node):
    tree_search = lambda x, y: self._treeSearch(self, x, y)
    return self._treeSearchWithBalancingWithSplay(key, node, tree_search)
  """
  """
  def _treeSearchWithBalancingWithUntransformedKey(self, key, node):
    tree_search = lambda x, y: self._treeSearchWithUntransformedKey(self, x, y)
    return self._treeSearchWithBalancingWithSplay(key, node, tree_search)
  """
"""
t2 = SplayTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)])
t2.remove(LocationAwareEntry(32, 1))
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(65, 1))
print t2.toInorderList()
"""
"""
t4 = SplayTree.construct([(17, 1), (28, 1), (29, 1)])
print t4.toInorderList()
print t4.toString()
t4.remove(LocationAwareEntry(28, 1))
t4.remove(LocationAwareEntry(17, 1))
# t4.remove(LocationAwareEntry(32, 1))
print t4.toInorderList()
print t4.toString()
"""
