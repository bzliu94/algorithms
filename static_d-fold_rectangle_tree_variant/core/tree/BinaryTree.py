from Node import *
from Entry import *
from collections import defaultdict
class BinaryTree:
  def __init__(self):
    self.root = None
  def _addRootHelper(self, element, node_class):
    self.root = node_class(element, None, None, None)
  def addRoot(self, element):
    self._addRootHelper(element, Node)
  def _setRoot(self, node):
    self.root = node
  def getRoot(self):
    return self.root
  def toInorderList(self):
    root = self.getRoot()
    return self._toInorderListHelper(root)
  def _toInorderListHelper(self, node):
    if node.isExternal():
      return []
    else:
      left_child = node.getLeftChild()
      right_child = node.getRightChild()
      entry_list_left = []
      entry_list_right = []
      if node.hasLeftChild():
        entry_list_left = self._toInorderListHelper(left_child)
      curr_entry = node.getElement()
      curr_entry_list = [curr_entry.toString()]
      if node.hasRightChild():
        entry_list_right = self._toInorderListHelper(right_child)
      entry_list = entry_list_left + curr_entry_list + entry_list_right
      return entry_list
  def toString(self):
    return self._toString(self.getRoot())
  def _toString(self, node):
    if node == None:
      return "None"
    else:
      left_child_str = self._toString(node.getLeftChild())
      curr_element = node.getElement()
      if curr_element != None:
        curr_entry_str = curr_element.toKeyString()
      else:
        curr_entry_str = "None"
      right_child_str = self._toString(node.getRightChild())
      partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"
      return partial_str
  def replace(self, v, o):
    v.setElement(o)
  def getAncestors(self, v):
    return self._getAncestorsHelper(v.getParent(), [])
  def _getAncestorsHelper(self, v, ordered_ancestors):
    if v == None:
      return ordered_ancestors
    else:
      return self._getAncestorsHelper(v.getParent(), ordered_ancestors + [v])
  def getLenientAncestors(self, v):
    return [v] + self.getAncestors(v)
  def getLCA(self, u, v):
    ancestors1 = self.getLenientAncestors(u)
    ancestors2 = self.getLenientAncestors(v)
    node_counts = defaultdict(lambda: 0)
    for ancestor in ancestors1:
      node_counts[ancestor] += 1
    lca = None
    for ancestor in ancestors2:
      if node_counts[ancestor] == 1:
        lca = ancestor
        break
    return lca
"""
t5 = BinaryTree()
n1 = Node(Entry(29, 1), None, None, None)
n2 = Node(Entry(28, 1), n1, None, None)
n3 = Node(Entry(17, 1), n2, None, None)
t5._setRoot(n1)
n1.setLeftChild(n2)
n2.setLeftChild(n3)
print t5.toString()
print t5.getAncestors(n3)
print t5.getAncestors(n2)
print t5.getAncestors(n1)
print t5.getLCA(n3, n2)
print t5.getLCA(n1, n1)
"""
