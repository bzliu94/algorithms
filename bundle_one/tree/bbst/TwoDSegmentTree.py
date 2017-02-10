# a 2-d segment tree is similar to a 1-d segment tree; 
# have a primary segment tree that orders based on x, 
# and have for each canonical subset for a node in primary segment tree, 
# have a secondary segment tree based on y; 
# having rectangle entities obeys requirement 
# that "segments" have disjoint interiors

# 2-d segment tree takes O(n * log(n) ^ 2) space 
# and answers queries in O(log(n) ^ 2) time 
# without fractional cascading

# for a query, we get to a node's canonical subset for x 
# and we query associated 1-d segment tree for y

# import pdb
from collections import defaultdict
"""
easier to implement without bit-wise parallelization, and then introduce it later
"""
from RedBlackTree import *
from TwoDSegmentTreeNode import *
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
class TwoDSegmentTree(RedBlackTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    RedBlackTree.__init__(self, key_transform, comparator)
    self.x_dict = None
    self.x_y_dict = None
  def getXDict(self):
    return self.x_dict
  """
  def getXYDict(self):
    return self.x_y_dict
  """
  def setXDict(self, x_interval_to_rectangle_segment_dict):
    self.x_dict = x_interval_to_rectangle_segment_dict
  """
  def setXYDict(self, x_interval_y_interval_tuple_to_rectangle_segment_dict):
    self.y_dict = x_interval_y_interval_tuple_to_rectangle_segment_dict
  """
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, TwoDSegmentTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, TwoDSegmentTreeNode)
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
  def pointQuery(self, query_x, query_y, for_x = True):
    root = self.getRoot()
    segment_dict = self.getXDict()
    result = root.pointQuery(query_x, query_y, self, for_x)
    return result
  @staticmethod
  def constructForX(rectangle_segments):
    x_intervals = [x.getXInterval() for x in rectangle_segments]
    # print x_intervals
    x_endpoints = list(set(reduce(lambda x, y: x + y, [list(x) for x in x_intervals], [])))
    x_ordered_endpoints = sorted(x_endpoints)
    # print ordered_endpoints
    ordered_unique_x_points = [(float("-inf"), float("-inf"))] + [(x, x) for x in x_ordered_endpoints] + [(float("inf"), float("inf"))]
    x_elementary_intervals = []
    for i in xrange(len(ordered_unique_x_points) - 1):
      curr_x_interval = ordered_unique_x_points[i]
      next_x_interval = ordered_unique_x_points[i + 1]
      interval = (curr_x_interval[1], next_x_interval[0])
      x_elementary_intervals.append(interval)
      x_elementary_intervals.append(next_x_interval)
    x_elementary_intervals.pop()
    # print elementary_intervals
    tree = TwoDSegmentTree(comparator = intervalComp)
    entries = [(x, 1) for x in x_elementary_intervals]
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  @staticmethod
  def constructForY(rectangle_segments):
    y_intervals = [x.getYInterval() for x in rectangle_segments]
    # print y_intervals
    y_endpoints = list(set(reduce(lambda x, y: x + y, [list(x) for x in y_intervals], [])))
    y_ordered_endpoints = sorted(y_endpoints)
    # print ordered_endpoints
    ordered_unique_y_points = [(float("-inf"), float("-inf"))] + [(x, x) for x in y_ordered_endpoints] + [(float("inf"), float("inf"))]
    y_elementary_intervals = []
    for i in xrange(len(ordered_unique_y_points) - 1):
      curr_y_interval = ordered_unique_y_points[i]
      next_y_interval = ordered_unique_y_points[i + 1]
      interval = (curr_y_interval[1], next_y_interval[0])
      y_elementary_intervals.append(interval)
      y_elementary_intervals.append(next_y_interval)
    y_elementary_intervals.pop()
    # print elementary_intervals
    tree = TwoDSegmentTree(comparator = intervalComp)
    entries = [(x, 1) for x in y_elementary_intervals]
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  @staticmethod
  def construct(rectangle_segments):
    x_interval_to_rectangle_segment_dict = defaultdict(lambda: [])
    for rectangle_segment in rectangle_segments:
      x_interval = rectangle_segment.getXInterval()
      x_interval_to_rectangle_segment_dict[x_interval].append(rectangle_segment)
    tree = TwoDSegmentTree.constructForX(rectangle_segments)
    nodes = tree.toInorderInternalNodeList()
    """
    x_interval_y_interval_tuple_to_rectangle_segment_dict = defaultdict(lambda: [])
    for rectangle_segment in rectangle_segments:
      x_interval = rectangle_segment.getXInterval()
      y_interval = rectangle_segment.getYInterval()
      key = (x_interval, y_interval)
      x_interval_y_interval_tuple_to_rectangle_segment_dict[key].append(rectangle_segment)
    """
    x_intervals = [x.getXInterval() for x in rectangle_segments]
    tree.memoizeSpanningIntervals()
    tree.memoizeCanonicalSubsets(x_intervals)
    for node in nodes:
      # print node.toString()
      canonical_subset = node.getCanonicalSubset()
      secondary_canonical_subset = node.getSecondaryCanonicalSubset()
      distinct_canonical_subset = list(set(canonical_subset))
      distinct_secondary_canonical_subset = list(set(secondary_canonical_subset))
      curr_rectangle_segments = reduce(lambda x, y: x + y, [x_interval_to_rectangle_segment_dict[x] for x in distinct_canonical_subset], [])
      curr_secondary_rectangle_segments = reduce(lambda x, y: x + y, [x_interval_to_rectangle_segment_dict[x] for x in distinct_secondary_canonical_subset], [])
      """
      if len(set(distinct_canonical_subset).intersection(set(distinct_secondary_canonical_subset))) != 0:
        raise Exception()
      """
      next_tree1 = TwoDSegmentTree.constructForY(curr_rectangle_segments)
      next_tree2 = TwoDSegmentTree.constructForY(curr_secondary_rectangle_segments)
      next_tree1.memoizeSpanningIntervals()
      next_tree1.memoizeCanonicalSubsets([x.getYInterval() for x in curr_rectangle_segments])
      next_tree2.memoizeSpanningIntervals()
      next_tree2.memoizeCanonicalSubsets([x.getYInterval() for x in curr_secondary_rectangle_segments])
      node.setLowerDSegmentTree(next_tree1)
      node.setSecondaryLowerDSegmentTree(next_tree2)
      # print next_tree1.toString()
      # print next_tree2.toString()
      y_interval_to_rectangle_segment_dict1 = defaultdict(lambda: [])
      for rectangle_segment in curr_rectangle_segments:
        y_interval1 = rectangle_segment.getYInterval()
        y_interval_to_rectangle_segment_dict1[y_interval1].append(rectangle_segment)
      next_tree1.setXDict(y_interval_to_rectangle_segment_dict1)
      y_interval_to_rectangle_segment_dict2 = defaultdict(lambda: [])
      for rectangle_segment in curr_secondary_rectangle_segments:
        y_interval2 = rectangle_segment.getYInterval()
        y_interval_to_rectangle_segment_dict2[y_interval2].append(rectangle_segment)
      next_tree2.setXDict(y_interval_to_rectangle_segment_dict2)
    tree.setXDict(x_interval_to_rectangle_segment_dict)
    # tree.setXYDict(x_interval_y_interval_tuple_to_rectangle_segment_dict)
    return tree
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
tree = TwoDSegmentTree()
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
from RectangleSegment import *
s1 = RectangleSegment((0, 0), (0, 10))
s2 = RectangleSegment((1, 1), (0, 10))
s3 = RectangleSegment((2, 2), (0, 10))
s4 = RectangleSegment((3, 3), (0, 10))
s5 = RectangleSegment((4, 4), (10, 11))
s6 = RectangleSegment((5, 5), (10, 11))
s7 = RectangleSegment((6, 6), (10, 11))
s8 = RectangleSegment((0, 7), (10, 12))
s9 = RectangleSegment((-2, 0), (10, 12))
rectangle_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
tree = TwoDSegmentTree.construct(rectangle_segments)
d1 = tree.getXDict()
# d2 = tree.getXYDict()
# print rectangle_segments
# print tree.toString()
"""
"""
nodes = tree.toInorderInternalNodeList()
for node in nodes:
  next_tree1 = node.getLowerDSegmentTree()
  next_tree2 = node.getSecondaryLowerDSegmentTree()
  print next_tree1.toString()
  print next_tree2.toString()
"""
"""
nodes = tree.toInorderInternalNodeList()
node_str_list = [x.toString() for x in nodes]
print node_str_list
"""
"""
for node in nodes:
  next_tree1 = node.getLowerDSegmentTree()
  next_tree2 = node.getSecondaryLowerDSegmentTree()
  print "primary node:", node.toString()
  print "primary spanning interval:", node.getSpanningInterval()
  if node.hasPointElementaryInterval() == True:
    print "secondary spanning interval:", node.getSecondarySpanningInterval()
  else:
    print "secondary spanning interval:", "N/A"
  print "primary canonical subset:", node.getCanonicalSubset()
  print "secondary canonical subset:", node.getSecondaryCanonicalSubset()
  print "primary lower tree:", [x.toString() for x in next_tree1.toInorderInternalNodeList()]
  print "secondary lower tree:", [x.toString() for x in next_tree2.toInorderInternalNodeList()]
  print
"""
"""
result = tree.pointQuery(4, 10)
print [x.toString() for x in result]
"""


