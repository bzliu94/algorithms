# from Node import *
from OrderedBinarySearchTreeNode import *
# class LazyRemoveOrderedBinarySearchTreeNode(Node):
class LazyRemoveOrderedBinarySearchTreeNode(OrderedBinarySearchTreeNode):
  def __init__(self, element, parent, left_child, right_child, marked = False):
    # Node.__init__(self, element, parent, left_child, right_child)
    OrderedBinarySearchTreeNode.__init__(self, element, parent, left_child, right_child)
    self.marked = marked
  def setMarked(self, marked):
    self.marked = marked
  def getMarked(self):
    return self.marked
