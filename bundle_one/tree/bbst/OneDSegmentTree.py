# import pdb
"""
easier to implement without bit-wise parallelization, and then introduce it later
"""
from RedBlackTree import *
from OneDSegmentTreeNode import *
"""
tree = SplayTree()
print tree
t2 = SplayTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)])
t2.remove(LocationAwareEntry(32, 1))
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(65, 1))
print t2.toInorderList()
"""
# intervals are always unique and they are disjoint except for endpoints
def intervalComp(interval_a, interval_b):
  l_a, r_a = interval_a
  l_b, r_b = interval_b
  # print interval_a, interval_b
  if r_a < l_b:
    return -1
  elif l_a > r_b:
    return 1
  elif r_a == l_b:
    if l_a < r_b:
      return -1
    elif r_a > l_b:
      return 1
    elif l_a == r_b:
      return 0
  elif r_a > l_b:
    return 1
class OneDSegmentTree(RedBlackTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    RedBlackTree.__init__(self, key_transform, comparator)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, OneDSegmentTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, OneDSegmentTreeNode)
  def memoizeSpanningIntervals(self):
    root = self.getRoot()
    root.memoizeSpanningIntervals()
  # assume that we have entries, and keys cannot be None
  def toSpanningIntervalString(self):
    return self._toSpanningIntervalString(self.getRoot())
  def _toSpanningIntervalString(self, node):
    if node == None:
      # non-existent node
      return "None"
    else:
      left_child_str = self._toSpanningIntervalString(node.getLeftChild())
      curr_element = node.getElement()
      if curr_element != None:
        curr_entry_str = curr_element.toKeyString() + " " + str(node.getSpanningInterval())
        if node.hasPointElementaryInterval() == True:
          # leave a mark noting that the node has secondary values
          curr_entry_str += " " + "*"
        # curr_entry_str = node.toKeyString()
      else:
        # non-existent key (possibly because entry does not exist)
        curr_entry_str = "None"
      right_child_str = self._toSpanningIntervalString(node.getRightChild())
      partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"
      return partial_str
  # assume that we have entries, and keys cannot be None
  def toCanonicalSubsetString(self):
    return self._toCanonicalSubsetString(self.getRoot())
  def _toCanonicalSubsetString(self, node):
    if node == None:
      # non-existent node
      return "None"
    else:
      left_child_str = self._toCanonicalSubsetString(node.getLeftChild())
      curr_element = node.getElement()
      if curr_element != None:
        curr_entry_str = curr_element.toKeyString() + " " + str(node.getCanonicalSubset())
        if node.hasPointCanonicalSubset() == True:
          # leave a mark noting that the node has secondary values
          curr_entry_str += " " + "*" + " " + str(node.getSecondaryCanonicalSubset())
        # curr_entry_str = node.toKeyString()
      else:
        # non-existent key (possibly because entry does not exist)
        curr_entry_str = "None"
      right_child_str = self._toCanonicalSubsetString(node.getRightChild())
      partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"
      return partial_str
  def memoizeCanonicalSubsets(self, intervals):
    root = self.getRoot()
    for interval in intervals:
      root.partiallyMemoizeCanonicalSubsets(interval)
  """
  def rangeQuery(self, query_interval):
    root = self.getRoot()
    result = root.rangeQuery(query_interval)
    return result
  """
  def pointQuery(self, query_x):
    root = self.getRoot()
    result = root.pointQuery(query_x)
    return result
  @staticmethod
  def construct(points):
    # print points
    endpoints = list(set(reduce(lambda x, y: x + y, [list(x) for x in points])))
    ordered_endpoints = sorted(endpoints)
    # print ordered_endpoints
    ordered_unique_x_points = [(float("-inf"), float("-inf"))] + [(x, x) for x in ordered_endpoints] + [(float("inf"), float("inf"))]
    elementary_intervals = []
    for i in xrange(len(ordered_unique_x_points) - 1):
      curr_point = ordered_unique_x_points[i]
      next_point = ordered_unique_x_points[i + 1]
      curr_interval = (curr_point[1], next_point[0])
      elementary_intervals.append(curr_interval)
      elementary_intervals.append(next_point)
    elementary_intervals.pop()
    # print elementary_intervals
    tree = OneDSegmentTree(comparator = intervalComp)
    entries = [(x, 1) for x in elementary_intervals]
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    """
    print tree.toString()
    print tree.toInorderList()
    tree.memoizeSpanningIntervals()
    nodes = tree.toInorderInternalNodeList()
    print [x.getSpanningInterval() for x in nodes]
    print tree.toSpanningIntervalString()
    intervals = points
    tree.memoizeCanonicalSubsets(intervals)
    print
    print tree.toCanonicalSubsetString()
    # pdb.set_trace()
    result = tree.pointQuery(0)
    print result
    """
"""
tree = OneDSegmentTree()
# curr_str = tree.toString()
# print curr_str
"""
# have elementary intervals
# store only points and not, for example, bounding boxes
# have static structure
# build off of a red-black tree
# have spanning interval for each node, endpoints inclusive
# have canonical subset for each node
"""
one_d_points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (0, 7), (-2, 0)]
# print one_d_points
OneDSegmentTree.construct(one_d_points)
"""


