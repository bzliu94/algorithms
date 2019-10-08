from RectangleSegment import *
from RedBlackTreeNode import *

class TwoDRangeTreeNode(RedBlackTreeNode):
  def __init__(self, element, parent, left_child, right_child):
    RedBlackTreeNode.__init__(self, element, parent, left_child, right_child)
    self.canonical_subset = None
    self.associated_tree = None
  def setCanonicalSubset(self, cs):
    self.canonical_subset = cs
  def getCanonicalSubset(self):
    return self.canonical_subset
  def setAssociatedTree(self, tree):
    self.associated_tree = tree
  def getAssociatedTree(self):
    return self.associated_tree


