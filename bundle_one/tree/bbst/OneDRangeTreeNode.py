from RedBlackTreeNode import *

class OneDRangeTreeNode(RedBlackTreeNode):
  def __init__(self, element, parent, left_child, right_child):
    RedBlackTreeNode.__init__(self, element, parent, left_child, right_child)
  @staticmethod
  def _endpointInclusiveIsContainedBy(interval1, interval2):
    l1, r1 = interval1
    l2, r2 = interval2
    result = l2 <= l1 and r2 >= r1
    return result
  @staticmethod
  def _endpointInclusiveIntersect(interval1, interval2):
    l1, r1 = interval1
    l2, r2 = interval2
    result = not ((r1 < l2) or (r2 < l1))
    return result
  @staticmethod
  def _intervalsAreIdentical(interval1, interval2):
    return interval1 == interval2


