from ..LazyRemoveOrderedBinarySearchTreeNode import *

class ScapegoatTreeNode(LazyRemoveOrderedBinarySearchTreeNode):

  def __init__(self, element, parent, left_child, right_child, marked = False):

    LazyRemoveOrderedBinarySearchTreeNode.__init__(self, element, parent, left_child, right_child, marked)


