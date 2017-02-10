from RectangleSegment import *
# import pdb
from RedBlackTreeNode import *
# primary canonical subset and spanning interval are for describing a group of three
# secondary canonical subset and spanning interval are for describing a node for a point elem. interval
class TwoDSegmentTreeNode(RedBlackTreeNode):
  def __init__(self, element, parent, left_child, right_child):
    RedBlackTreeNode.__init__(self, element, parent, left_child, right_child)
    self.canonical_subset = []
    self.secondary_canonical_subset = []
    self.lower_d_segment_tree = None
    self.secondary_lower_d_segment_tree = None
  def getCanonicalSubset(self):
    return self.canonical_subset
  def getSecondaryCanonicalSubset(self):
    return self.secondary_canonical_subset
  # spanning intervals include both endpoints
  def getSpanningInterval(self):
    return self.spanning_interval
  def getSecondarySpanningInterval(self):
    return self.secondary_spanning_interval
  def setCanonicalSubset(self, canonical_subset):
    self.canonical_subset = canonical_subset
  def setSecondaryCanonicalSubset(self, secondary_canonical_subset):
    self.secondary_canonical_subset = secondary_canonical_subset
  def setSpanningInterval(self, spanning_interval):
    self.spanning_interval = spanning_interval
  def setSecondarySpanningInterval(self, secondary_spanning_interval):
    self.secondary_spanning_interval = secondary_spanning_interval
  def addToCanonicalSubset(self, item):
    self.canonical_subset.append(item)
  def addToSecondaryCanonicalSubset(self, item):
    self.secondary_canonical_subset.append(item)
  # return True if we have only children (if we have any at all) that are external
  def hasNoNonExternalChildren(self):
    have_no_non_external_children = True
    if self.hasLeftChild() == True:
      if self.getLeftChild().isInternal() == True:
        have_no_non_external_children = False
    if self.hasRightChild() == True:
      if self.getRightChild().isInternal() == True:
        have_no_non_external_children = False
    return have_no_non_external_children
  # bottom-to-top
  def memoizeSpanningIntervals(self):
    if self.isExternal() == True:
      # do nothing
      return
    elif self.isInternal() == True:
      # use key, which is elementary interval
      entry = self.getElement()
      key = entry.getKey()
      elementary_interval = key
      spanning_interval = elementary_interval
      left_child = self.getLeftChild()
      right_child = self.getRightChild()
      if self.hasLeftChild() == True and left_child.isExternal() == False:
        left_child.memoizeSpanningIntervals()
        left_spanning_interval = left_child.getSpanningInterval()
        l_a, r_a = left_spanning_interval
        l_b, r_b = spanning_interval
        spanning_interval = (l_a, r_b)
      if self.hasRightChild() == True and right_child.isExternal() == False:
        right_child.memoizeSpanningIntervals()
        right_spanning_interval = right_child.getSpanningInterval()
        l_a, r_a = right_spanning_interval
        l_b, r_b = spanning_interval
        spanning_interval = (l_b, r_a)
      self.setSpanningInterval(spanning_interval)
      if self.hasPointElementaryInterval() == True:
        secondary_spanning_interval = elementary_interval
        self.setSecondarySpanningInterval(secondary_spanning_interval)
      return
  def hasPointElementaryInterval(self):
    if self.isExternal() == True:
      raise Exception()
    elif self.isInternal() == True:
      entry = self.getElement()
      key = entry.getKey()
      elementary_interval = key
      (l, r) = elementary_interval
      has_point_elementary_interval = l == r
      return has_point_elementary_interval
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
  def partiallyMemoizeCanonicalSubsets(self, interval):
    spanning_interval = self.getSpanningInterval()
    secondary_spanning_interval = None
    have_secondary_spanning_interval = False
    if self.hasPointElementaryInterval() == True:
      secondary_spanning_interval = self.getSecondarySpanningInterval()
      have_secondary_spanning_interval = True
    if TwoDSegmentTreeNode._endpointInclusiveIsContainedBy(spanning_interval, interval) == True:
      self.addToCanonicalSubset(interval)
    elif have_secondary_spanning_interval == True and \
      TwoDSegmentTreeNode._intervalsAreIdentical(interval, secondary_spanning_interval) == True:
      # better would be to state that the two intervals are identical
      self.addToSecondaryCanonicalSubset(interval)
    else:
      left_child = self.getLeftChild()
      right_child = self.getRightChild()
      have_left_child = self.hasLeftChild()
      have_right_child = self.hasRightChild()
      if have_left_child == True:
        left_child_is_internal = left_child.isInternal()
        if left_child_is_internal == True:
          child_interval = left_child.getSpanningInterval()
          if TwoDSegmentTreeNode._endpointInclusiveIntersect(interval, child_interval) == True:
            left_child.partiallyMemoizeCanonicalSubsets(interval)
      if have_right_child == True:
        right_child_is_internal = right_child.isInternal()
        if right_child_is_internal == True:
          child_interval = right_child.getSpanningInterval()
          if TwoDSegmentTreeNode._endpointInclusiveIntersect(interval, child_interval) == True:
            right_child.partiallyMemoizeCanonicalSubsets(interval)
  def hasPointCanonicalSubset(self):
    return self.hasPointElementaryInterval()
  """
  def rangeQuery(self, query_interval):
    result = []
    self.rangeQueryHelper(query_interval, result)
    return result
  def rangeQueryHelper(self, query_interval, partial_result):
    # print "*"
    canonical_subset = self.getCanonicalSubset()
    partial_result.extend(canonical_subset)
    have_secondary_spanning_interval = self.hasPointElementaryInterval() == True
    if have_secondary_spanning_interval == True:
      secondary_spanning_interval = self.getSecondarySpanningInterval()
      if TwoDSegmentTreeNode._endpointInclusiveIntersect(query_interval, secondary_spanning_interval) == True:
        secondary_canonical_subset = self.getSecondaryCanonicalSubset()
        partial_result.extend(secondary_canonical_subset)
    if self.isExternal() == False:
      left_child = self.getLeftChild()
      right_child = self.getRightChild()
      if left_child.isExternal() == False:
        left_child_spanning_interval = left_child.getSpanningInterval()
        if TwoDSegmentTreeNode._endpointInclusiveIntersect(query_interval, left_child_spanning_interval) == True:
          left_child.rangeQueryHelper(query_interval, partial_result)
      if right_child.isExternal() == False:
        right_child_spanning_interval = right_child.getSpanningInterval()
        if TwoDSegmentTreeNode._endpointInclusiveIntersect(query_interval, right_child_spanning_interval) == True:
          right_child.rangeQueryHelper(query_interval, partial_result)
  """
  # stabbing query; never to be run on an external node
  def pointQuery(self, query_x, query_y, tree, for_x = True):
    result = []
    query_x_interval = (query_x, query_x)
    query_y_interval = (query_y, query_y)
    # in case we are root with no children
    if self.isExternal() == True:
      return []
    self.pointQueryHelper(query_x_interval, query_y_interval, result, tree, for_x)
    """
    if (0, 7) in [x.getXInterval() for x in result]:
      # pdb.set_trace()
      pass
    """
    # result is a list of rectangle segments
    next_result = list(set(result))
    return next_result
  def pointQueryHelper(self, query_x_interval, query_y_interval, partial_result, tree, for_x):
    query_interval = None
    if for_x == True:
      query_interval = query_x_interval
    else:
      query_interval = query_y_interval
    # if self.isExternal() == True:
    #   return
    # pdb.set_trace()
    lower_d_segment_tree = self.getLowerDSegmentTree()
    """
    if lower_d_segment_tree == None:
      pdb.set_trace()
    """
    secondary_lower_d_segment_tree = self.getSecondaryLowerDSegmentTree()
    canonical_subset = self.getCanonicalSubset()
    # print canonical_subset
    # partial_result.extend(canonical_subset)
    if for_x == True and self.haveLowerDSegmentTree() == True:
      # is a primary segment tree
      additions = []
      lower_d_segment_tree.getRoot().pointQueryHelper(query_x_interval, query_y_interval, additions, lower_d_segment_tree, False)
      partial_result.extend(additions)
      """
      if (0, 7) in [x.getXInterval() for x in additions]:
        pdb.set_trace()
        pass
      """
    else:
      # is a secondary segment tree
      y_dict = tree.getXDict()
      additions = reduce(lambda x, y: x + y, [y_dict[x] for x in list(set(canonical_subset))],
 [])
      partial_result.extend(additions)
      """
      if (0, 7) in [x.getXInterval() for x in additions]:
        # pdb.set_trace()
        pass
      """
    have_secondary_spanning_interval = self.hasPointElementaryInterval() == True
    if have_secondary_spanning_interval == True:
      secondary_spanning_interval = self.getSecondarySpanningInterval()
      if TwoDSegmentTreeNode._endpointInclusiveIsContainedBy(query_interval, secondary_spanning_interval) == True:
        secondary_canonical_subset = self.getSecondaryCanonicalSubset()
        if for_x == True and self.haveSecondaryLowerDSegmentTree() == True:
          # is a primary segment tree
          additions = []
          secondary_lower_d_segment_tree.getRoot().pointQueryHelper(query_x_interval, query_y_interval, additions, secondary_lower_d_segment_tree, False)
          partial_result.extend(additions)
          """
          if (0, 7) in [x.getXInterval() for x in partial_result]:
            # pdb.set_trace()
            pass
          """
        else:
          # is a secondary segment tree
          y_dict = tree.getXDict()
          additions = reduce(lambda x, y: x + y, [y_dict[x] for x in list(set(secondary_canonical_subset))], [])
          partial_result.extend(additions)
    if self.isExternal() == False:
      left_child = self.getLeftChild()
      right_child = self.getRightChild()
      if left_child.isExternal() == False:
        left_child_spanning_interval = left_child.getSpanningInterval()
        if TwoDSegmentTreeNode._endpointInclusiveIsContainedBy(query_interval, left_child_spanning_interval) == True:
          left_child.pointQueryHelper(query_x_interval, query_y_interval, partial_result, tree, for_x)
      if right_child.isExternal() == False:
        right_child_spanning_interval = right_child.getSpanningInterval()
        if TwoDSegmentTreeNode._endpointInclusiveIsContainedBy(query_interval, right_child_spanning_interval) == True:
          right_child.pointQueryHelper(query_x_interval, query_y_interval, partial_result, tree, for_x)
  def haveLowerDSegmentTree(self):
    return self.lower_d_segment_tree != None
  def haveSecondaryLowerDSegmentTree(self):
    return self.secondary_lower_d_segment_tree != None
  def getLowerDSegmentTree(self):
    return self.lower_d_segment_tree
  def getSecondaryLowerDSegmentTree(self):
    return self.secondary_lower_d_segment_tree
  def setLowerDSegmentTree(self, lower_d_segment_tree):
    self.lower_d_segment_tree = lower_d_segment_tree
  def setSecondaryLowerDSegmentTree(self, secondary_lower_d_segment_tree):
    self.secondary_lower_d_segment_tree = secondary_lower_d_segment_tree


