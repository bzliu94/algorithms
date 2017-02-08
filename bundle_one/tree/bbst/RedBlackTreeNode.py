from ..OrderedBinarySearchTreeNode import *
class RedBlackTreeNode(OrderedBinarySearchTreeNode):
  def __init__(self, element, parent, left_child, right_child, is_red = False):
    OrderedBinarySearchTreeNode.__init__(self, element, parent, left_child, right_child)
    self.is_red = is_red
  def isRed(self):
    return self.is_red
  def setRed(self):
    self.is_red = True
  def setBlack(self):
    self.is_red = False
  def setColor(self, color):
    self.is_red = color
  def parentIsRed(self):
    parent = self.getParent()
    return parent.isRed()
  def redChild(self):
    child1 = self.getLeftChild()
    child2 = self.getRightChild()
    if child1.isRed():
      return child1
    elif child2.isRed():
      return child2
    else:
      return None
  def hasRedChild(self):
    return self.getLeftChild().isRed() or self.getRightChild().isRed()


