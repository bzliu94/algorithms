from ..OrderedBinarySearchTree import *
from ..Entry import *
class SplayTree(OrderedBinarySearchTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    OrderedBinarySearchTree.__init__(self, key_transform, comparator)
  @staticmethod
  def construct(entries, key_transform = lambda x: x, comparator = comp):
    tree = SplayTree(key_transform, comparator)
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def _oughtToSplay(self, action_node):
    return not (action_node.isExternal() and action_node == self.getRoot())
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
    parent = x.getParent()
    if parent == None:
      return
    grandparent = parent.getParent()
    if grandparent == None:
      self._zig(x)
    elif (x.isLeftChild() and parent.isLeftChild())      or (x.isRightChild() and parent.isRightChild()):
      self._zig_zig(x)
    elif (x.isLeftChild() and parent.isRightChild())      or (x.isRightChild() and parent.isLeftChild()):
      self._zig_zag(x)
    self._splay(x)
  def _zig_zig(self, x):
    y = x.getParent()
    z = y.getParent()
    z_parent = z.getParent()
    z_has_parent = z.hasParent()
    if x.isLeftChild() == True:
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
    y = x.getParent()
    z = y.getParent()
    z_parent = z.getParent()
    z_has_parent = z.hasParent()
    if x.isRightChild() == True:
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
  def _zig(self, x):
    y = x.getParent()
    w1 = x.getLeftChild()
    w2 = x.getRightChild()
    y_parent = y.getParent()
    y_has_parent = y.hasParent()
    if x.isLeftChild() == True:
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
      t1 = y.getLeftChild()
      t2 = x.getLeftChild()
      self._upperSituate(x, y)
      self._lowerSituate(t1, y)
      self._lowerSituate(t2, y)
      y.setLeftChild(t1)
      y.setRightChild(t2)
      y.setParent(x)
      x.setLeftChild(y)
      x.setRightChild(w2)
      x.setParent(y_parent)
  def _findWithSplay(self, key, bst_find):
    #--
    result = bst_find(key)
    target_node = self.action_node
    self._splayGivenActionNode(target_node)
    return result
  def find(self, key):
    bst_find = lambda x: OrderedBinarySearchTree.find(self, x)
    return self._findWithSplay(key, bst_find)
  def _insertWithSplay(self, key, value, bst_insert):
    result = bst_insert(key, value)
    target_node = self.action_node
    self._splayGivenActionNode(target_node)
    return result
  def insert(self, untransformed_key, value):
    bst_insert = lambda key, value: OrderedBinarySearchTree.insert(self, key, value)
    return self._insertWithSplay(untransformed_key, value, bst_insert)
  def _removeWithSplay(self, entry, bst_remove):
    #--
    result = bst_remove(entry)
    target_node = self.action_node
    self._splayGivenActionNode(target_node)
    return result
  def remove(self, entry):
    bst_remove = lambda entry: OrderedBinarySearchTree.remove(self, entry)
    return self._removeWithSplay(entry, bst_remove)
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
