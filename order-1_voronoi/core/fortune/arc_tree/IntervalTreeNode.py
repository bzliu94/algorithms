# have attributed max values

# from ...tree.Node import *

from ...tree.OrderedBinarySearchTreeNode import *

class BalancedIntervalTreeNode(OrderedBinarySearchTreeNode):

  def __init__(self, element, parent, left_child, right_child, max = None):

    OrderedBinarySearchTreeNode.__init__(self, element, parent, left_child, right_child)
    
    self.max = max

  def getMax(self):
  
    return self.max

  def setMax(self, max):
  
    self.max = max


