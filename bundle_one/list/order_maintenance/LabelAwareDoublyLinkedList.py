# for use with LabelAwareDoublyLinkedListNode objects
from LabelAwareDoublyLinkedListNode import *
from ..DoublyLinkedList import *
from PathLabel import *
class LabelAwareDoublyLinkedList(DoublyLinkedList):
  def __init__(self):
    DoublyLinkedList.__init__(self)
    # self.label_tree = label_tree
  """
  def _getLabelTree(self):
    return self.label_tree
  def _setLabelTree(self, label_tree):
    self.label_tree = label_tree
  """
  def _createNode(self, item, prev, next):
    node = LabelAwareDoublyLinkedListNode(item, prev, next, self)
    return node
"""
list = LabelAwareDoublyLinkedList()
list.addFirst(LabelAwareDoublyLinkedListNode(1, None, None, PathLabel(244, 5)))
node = list.getFirst()
label = node.getLabel()
label_value = label.getValue()
print label_value
"""
