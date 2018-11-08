# 2018-11-04
# tree that can have more than two children

import string

from DAryTreeNode import *
from DAryTreeEntry import *

class DAryTree:
  def __init__(self):
    # self.size = 0
    self.root = None
  def _addRootHelper(self, element, node_class):
    self.root = node_class(element, None, None, None)
  def addRoot(self, element):
    self._addRootHelper(element, Node)
  def _setRoot(self, node):
    self.root = node
  def getRoot(self):
    return self.root
  """
  def size(self):
    return self.size
  def isEmpty(self):
    return self.size() == 0
  """
  # added

  # get flattened list of entries for nodes visited using pre-order traversal

  def toPreorderList(self, include_external_nodes = False):
    root = self.getRoot()
    return self._toPreorderListHelper(root, include_external_nodes)
  def _toPreorderListHelper(self, node, include_external_nodes = False):
    if node.isExternal() and include_external_nodes == True:
      return []
    else:
      curr_entry = node.getElement()
      curr_entry_list = [curr_entry]
      entry_list_children = reduce(lambda x, y: x + y, [self._toPreorderListHelper(x) for x in node.getChildren()], [])
      entry_list = curr_entry_list + entry_list_children
      return entry_list
  # assume that we have entries, and keys cannot be None
  def toString(self):
    return self._toString(self.getRoot())
  def _toString(self, node):
    if node == None:
      # non-existent node
      return "None"
    else:
      # left_child_str = self._toString(node.getLeftChild())
      curr_element = node.getElement()
      if curr_element != None:
        curr_entry_str = curr_element.toKeyString()
        # curr_entry_str = node.toKeyString()
      else:
        # non-existent key (possibly because entry does not exist)
        curr_entry_str = "None"
      # right_child_str = self._toString(node.getRightChild())
      children_str = string.join([self._toString(x) for x in node.getChildren()], " ")
      # partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"
      partial_str = "(" + curr_entry_str + " " + children_str + ")"
      return partial_str
  def replace(self, v, o):
    v.setElement(o)

"""
t5 = DAryTree()
n1 = DAryTreeNode(DAryTreeEntry(29, 1), None, [])
n2 = DAryTreeNode(DAryTreeEntry(28, 1), n1, [])
n3 = DAryTreeNode(DAryTreeEntry(17, 1), n2, [])
t5._setRoot(n1)
n1.addChild(n2)
n2.addChild(n3)
print t5.toString()
"""


