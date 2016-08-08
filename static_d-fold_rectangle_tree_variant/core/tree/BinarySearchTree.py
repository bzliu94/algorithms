from BinaryTree import *
from Entry import *
from ..Util import *
class BinarySearchTree(BinaryTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    BinaryTree.__init__(self)
    self.num_entries = 0
    self.addRoot(None)
    self.key_transform = key_transform
    self.comparator = comparator
  def getKeyTransform(self):
    return self.key_transform
  def getComparator(self):
    return self.comparator
  def setComparator(self, comparator):
    self.comparator = comparator
  def getNumEntries(self):
    return self.num_entries
  def hasNoEntries(self):
    return self.getNumEntries() == 0
  @staticmethod
  def construct(entries):
    tree = BinarySearchTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def _treeSearch(self, key, node):
    if node.isExternal() == True:
      return node
    else:
      curr_key = node.getElement().getKey()
      comparator = self.getComparator()
      key_transform = self.getKeyTransform()
      transformed_key = key_transform(key)
      curr_transformed_key = key_transform(curr_key)
      if comparator(transformed_key, curr_transformed_key) == 0:
        return node
      elif comparator(transformed_key, curr_transformed_key) < 0:
        return self._treeSearch(key, node.getLeftChild())
      elif comparator(transformed_key, curr_transformed_key) > 0:
        return self._treeSearch(key, node.getRightChild())
  def find(self, key):
    node = self._treeSearch(key, self.getRoot())
    self.action_node = node
    if node.isInternal() == True:
      entry = node.getElement()
      return (entry, node)
    else:
      return None
  def _expandExternalHelper(self, external_node, left_entry, right_entry, node_class):
    node = external_node
    left_child = node_class(left_entry, node, None, None)
    right_child = node_class(right_entry, node, None, None)
    node.setLeftChild(left_child)
    node.setRightChild(right_child)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, Node)
  def _insertAtExternal(self, external_node, entry):
    self._expandExternal(external_node, None, None)
    node = external_node
    self._replaceEntry(node, entry)
    self.num_entries = self.num_entries + 1
    return entry
  def _insertRetrieveNode(self, key, value):
    ins_node = self._treeSearch(key, self.getRoot())
    while not ins_node.isExternal():
      ins_node = self._treeSearch(key, ins_node.getLeftChild())
    return ins_node
  def _insertIntroduceEntry(self, key, value, ins_node):
    return self._insertIntroduceEntryHelper(key, value, ins_node, Entry)
  def _insertIntroduceEntryHelper(self, key, value, ins_node, entry_class):
    return self._insertAtExternal(ins_node, entry_class(key, value))
  def insert(self, key, value):
    ins_node = self._insertRetrieveNode(key, value)
    self.action_node = ins_node
    entry = self._insertIntroduceEntry(key, value, ins_node)
    return (entry, ins_node)
  def _removeRetrieveNode(self, entry):
    key = entry.getKey()
    value = entry.getValue()
    curr_node = self._treeSearch(key, self.getRoot())
    return curr_node
  def _removeRetrieveReplacementNode(self, found_node):
    curr_node = found_node
    rem_node = None
    if curr_node.getLeftChild().isExternal() == True:
      rem_node = curr_node.getLeftChild()
    elif curr_node.getRightChild().isExternal() == True:
      rem_node = curr_node.getRightChild()
    else:
      w = curr_node
      x = curr_node
      x = x.getRightChild()
      while x.isInternal() == True:
        x = x.getLeftChild()
      rem_node = x
    return rem_node
  def remove(self, entry):
    w = self._removeRetrieveNode(entry)
    rem_node = self._removeRetrieveReplacementNode(w)
    to_return = w.getElement()
    if w.isInternal() == True:
      x = rem_node
      y_entry = x.getParent().getElement()
      self._replaceEntry(w, y_entry)
    self.action_node = rem_node.getSibling()
    self._removeExternal(rem_node)
    return (to_return, rem_node)
  def _replaceEntry(self, node, entry):
    node.setElement(entry)
  def _removeExternal(self, node):
    self._removeAboveExternal(node)
    self.num_entries = self.num_entries - 1
  def _upperSituate(self, u, v):
    v_parent = v.getParent()
    if v_parent != None:
      if v.isLeftChild():
        v_parent.setLeftChild(u)
      else:
        v_parent.setRightChild(u)
    if v == self.getRoot():
      self._setRoot(u)
  def _lowerSituate(self, u, v):
    if u == None:
      return
    else:
      u.setParent(v)
  def _removeAboveExternal(self, external_node):
    z = external_node
    w = z.getParent()
    z_sibling = z.getSibling()
    w_parent = w.getParent()
    self._upperSituate(z_sibling, w)
    z_sibling.setParent(w_parent)
  def _addAll(self, L, node, key):
    if node.isExternal() == True:
      return
    node = self._treeSearch(key, node)
    if node.isExternal() == False:
      self._addAll(L, node.getLeftChild(), key)
      entry = node.getElement()
      L.append(entry)
      self._addAll(L, node.getRightChild(), key)
  def findAll(self, key):
    L = []
    self._addAll(L, self.getRoot(), key)
    return L
  def toInorderInternalNodeList(self):
    return self._toInorderInternalNodeListHelper(self.getRoot())
  def _toInorderInternalNodeListHelper(self, node):
    if node.isExternal():
      return []
    left_nodes = self._toInorderInternalNodeListHelper(node.getLeftChild())
    current_nodes = [node]
    right_nodes = self._toInorderInternalNodeListHelper(node.getRightChild())
    result_nodes = left_nodes + current_nodes + right_nodes
    return result_nodes
"""
# t1 = BinarySearchTree.construct([(1, 1), (2, 1), (3, 1), (4, 1)])
t1 = BinarySearchTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1)])
print t1.toString()
t1.remove(Entry(32, 1))
t1.remove(Entry(65, 1))
print t1.toInorderList()
t1.insert(17, 1)
print t1.find(17)
print t1.findAll(17)
"""
"""
t3 = BinarySearchTree.construct([(17, 1), (28, 1), (29, 1)])
print t3.toInorderList()
t3.remove(Entry(28, 1))
print t3.toInorderList()
"""
"""
t4 = BinarySearchTree.construct([(17, 1)])
print t4.toString()
t4.remove(Entry(17, 1))
print t4.toString()
"""
