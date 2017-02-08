from SplayTree import *

from ..OrderedBinarySearchTree import *
from ..Entry import *
from RedBlackTreeNode import *

class RedBlackTree(OrderedBinarySearchTree):

  def __init__(self, key_transform = lambda x: x, comparator = comp):
    OrderedBinarySearchTree.__init__(self, key_transform, comparator)

  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, RedBlackTreeNode)

  def addRoot(self, entry):
    self._addRootHelper(entry, RedBlackTreeNode)

  @staticmethod
  def construct(entries):
    tree = RedBlackTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree

  def find(self, key):
    bst_find = lambda x: OrderedBinarySearchTree.find(self, x)
    result = bst_find(key)
    return result

  def insert(self, untransformed_key, value):
    bst_insert = lambda key, value: OrderedBinarySearchTree.insert(self, key, value)
    result = bst_insert(untransformed_key, value)
    z = self.action_node
    z.setRed()
    if self.getRoot() == z:
      z.setBlack()
    else:
      self.remedyDoubleRed(z)
    return result

  def remove(self, entry):
    bst_remove = lambda entry: OrderedBinarySearchTree.remove(self, entry)
    result = bst_remove(entry)
    r = self.action_node
    if result != None:
      if self.getRoot() == r or r.getParent().isRed() == True or r.isRed() == True:
        r.setBlack()
      else:
        self.remedyDoubleBlack(r)
    return result

  def restructure(self, x):
    y = x.getParent()
    z = y.getParent()
    x_is_left_child = x.isLeftChild()
    y_is_left_child = y.isLeftChild()
    in_order_nodes = None
    sub_trees = None
    # step #1 - determine in-order nodes and sub-trees
    if y_is_left_child == True:
      if x_is_left_child == True:
        in_order_nodes = [x, y, z]
        sub_trees = [x.getLeftChild(), x.getRightChild(), y.getRightChild(), z.getRightChild()]
      else:
        in_order_nodes = [y, x, z]
        sub_trees = [y.getLeftChild(), x.getLeftChild(), x.getRightChild(), z.getRightChild()]
    else:
      if x_is_left_child == True:
        in_order_nodes = [z, x, y]
        sub_trees = [z.getLeftChild(), x.getLeftChild(), x.getRightChild(), y.getRightChild()]
      else:
        in_order_nodes = [z, y, x]
        sub_trees = [z.getLeftChild(), y.getLeftChild(), x.getLeftChild(), x.getRightChild()]
    a, b, c = in_order_nodes
    t0, t1, t2, t3 = sub_trees
    # step #2 - replace grandparent z with b using upper-situate
    # step #3 - deal with b and a using pointers and t_0 and t_1 using lower-situate
    # step #4 - deal with b and c using pointers and t_2 and t_3 using lower-situate
    z_parent = z.getParent()
    self._upperSituate(b, z)
    self._lowerSituate(t0, a)
    self._lowerSituate(t1, a)
    self._lowerSituate(t2, c)
    self._lowerSituate(t3, c)
    b.setLeftChild(a)
    b.setRightChild(c)
    b.setParent(z_parent)
    a.setLeftChild(t0)
    a.setRightChild(t1)
    a.setParent(b)
    c.setLeftChild(t2)
    c.setRightChild(t3)
    c.setParent(b)
    return b

  def remedyDoubleRed(self, z):
    v = z.getParent()
    if self.getRoot() == v:
      return
    if not v.isRed():
      return
    if v.getSibling().isRed() == False:
      # case #1 - trinode restructuring
      v = self.restructure(z)
      v.setBlack()
      v.getLeftChild().setRed()
      v.getRightChild().setRed()
    else:
      # case #2 - recoloring
      v.setBlack()
      v.getSibling().setBlack()
      u = v.getParent()
      if self.getRoot() == u:
        return
      u.setRed()
      self.remedyDoubleRed(u)

  def remedyDoubleBlack(self, r):
    z = None
    x = r.getParent()
    y = r.getSibling()
    if y.isRed() == False:
      z = y.redChild()
      if y.hasRedChild() == True:
        # case #1 - trinode restructuring
        old_color = x.isRed()
        z = self.restructure(z)
        z.setColor(old_color)
        r.setBlack()
        z.getLeftChild().setBlack()
        z.getRightChild().setBlack()
        return
      r.setBlack()
      y.setRed()
      if x.isRed() == False:
        # case #2 - recoloring
        if self.getRoot() != x:
          self.remedyDoubleBlack(x)
        return
      # case #3 - adjustment
      if x.getRightChild() == y:
        z = y.getRightChild()
      else:
        z = y.getLeftChild()
      self.restructure(z)
      y.setBlack()
      x.setRed()
      self.remedyDoubleBlack(r)

"""

tree = RedBlackTree()

tree.insert(1, 1)
tree.insert(2, 1)
tree.insert(3, 1)

print tree.toString()

"""

"""

k_v_pairs = [(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)]

t2 = RedBlackTree.construct(k_v_pairs)
t2.remove(LocationAwareEntry(32, 1))
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(65, 1))
result2 = t2.toInorderList()

t3 = SplayTree.construct(k_v_pairs)
t3.remove(LocationAwareEntry(32, 1))
print t3.toString()
print t3.toInorderList()
t3.remove(LocationAwareEntry(65, 1))
result3 = t3.toInorderList()

print set(result2) == set(result3)

"""


