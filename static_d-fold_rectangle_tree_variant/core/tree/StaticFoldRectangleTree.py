from bbst.SubtreeEntryMemoizingSplayTree import SubtreeEntryMemoizingSplayTree
from ..Util import comp
import random
def quickSelect(S, k):
  if len(S) == 0:
    return None
  if len(S) == 1:
    return S[0]
  pivot_index = random.randint(0, len(S) - 1)
  pivot = S[pivot_index]
  L = [x for x in S if x < pivot]
  E = [x for x in S if x == pivot]
  G = [x for x in S if x > pivot]
  if k <= len(L):
    return quickSelect(L, k)
  elif k <= len(L) + len(E):
    return pivot
  else:
    return quickSelect(G, k - len(L) - len(E))
def getMedian(items):
  S = items
  num_items = len(items)
  k = None
  if num_items % 2 == 0:
    k = num_items / 2
  elif num_items % 2 == 1:
    k = (num_items - 1) / 2 + 1
  return quickSelect(S, k)
def getMedianModified(items):
  sorted_items = sorted(items)
  num_items = len(items)
  next_num_items = num_items / 2
  item1 = sorted_items[next_num_items - 1]
  item2 = sorted_items[next_num_items]
  value = (item1 + item2) / (1.0 * 2)
  return value
"""
result = getMedian([1, 2, 3])
print result
i1 = (0, 3)
i2 = (1, 5)
i3 = (2, 8)
i4 = (4, 6)
i5 = (7, 9)
endpoints = []
intervals = [i1, i2, i3, i4, i5]
for interval in intervals:
  start, end = interval
  endpoints.append(start)
  endpoints.append(end)
print getMedian(endpoints)
"""
class SplayTreeWithSplaylessFind(SubtreeEntryMemoizingSplayTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    SubtreeEntryMemoizingSplayTree.__init__(self, key_transform, comparator)
  @staticmethod
  def construct(entries, key_transform = lambda x: x, comparator = comp):
    tree = SplayTreeWithSplaylessFind(key_transform, comparator)
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def _findWithoutSplay(self, key, bst_find):
    result = bst_find(key)
    return result
  def find(self, key):
    bst_find = lambda x: OrderedBinarySearchTree.find(self, x)
    return self._findWithoutSplay(key, bst_find)
class SFRT:
  def __init__(self, d):
    self.root = None
    self.d = d
  def setRoot(self, sfrt_node):
    self.root = sfrt_node
  def getRoot(self):
    return self.root
  def getDimension(self):
    return self.d
  def toString(self):
    result_str = self.getRoot().toString()
    return result_str
  def __repr__(self):
    return self.toString()
  def do1DRangeSearch(self, left, right):
    d = self.getDimension()
    return self.getRoot().do1DRangeSearch(left, right)
  def doDRangeSearch(self, d_interval, start_d, end_d):
    d_to_lr_value_pair_dict = d_interval.toDToValuePairDict()
    return self.getRoot().doDRangeSearch(d_to_lr_value_pair_dict, start_d, end_d)
  def doDRangeSearchHelper(self, d_to_lr_value_pair_dict, start_d, end_d, have_ancestor_contained_by_q):
    if self.getRoot() == None:
      return []
    else:
      return self.getRoot().doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, have_ancestor_contained_by_q)
class SFRTNode:
  def __init__(self, split_value, d, set_p, secondary_node_to_set_p_dict, parent = None, left_child = None, middle_child = None, right_child = None):
    self.split_value = split_value
    self.d = d
    self.set_p = set_p
    self.secondary_node_to_set_p_dict = secondary_node_to_set_p_dict
    self.parent = parent
    self.left_child = left_child
    self.middle_child = middle_child
    self.right_child = right_child
  def getAddressedRightDeficit(self):
    return False
  def getAddressedLeftDeficit(self):
    return False
  def getSetP(self):
    return self.set_p
  def getSecondaryNodeToSetPDict(self):
    return self.secondary_node_to_set_p_dict
  def haveAsLeftChild(self, sfrt_node):
    return self.getLeftChild() == sfrt_node
  def haveAsRightChild(self, sfrt_node):
    return self.getRightChild() == sfrt_node
  def getDimension(self):
    return self.d
  def getParent(self):
    return self.parent
  def setParent(self, sfrt_node):
    self.parent = sfrt_node
  def setLeftChild(self, sfrt_node):
    self.left_child = sfrt_node
  def setMiddleChild(self, splay_tree):
    self.middle_child = splay_tree
  def setRightChild(self, sfrt_node):
    self.right_child = sfrt_node
  def getLeftChild(self):
    return self.left_child
  def getMiddleChild(self):
    return self.middle_child
  def getRightChild(self):
    return self.right_child
  def getSplitValue(self):
    return self.split_value
  @staticmethod
  def intersectInterval(val, interval_tuple):
    start, end = interval_tuple
    does_intersect = val >= start and val <= end
    return does_intersect
  @staticmethod
  def isToLeftOfInterval(val, interval_tuple):
    start, end = interval_tuple
    is_to_left = val <= start and val <= end
    return is_to_left
  @staticmethod
  def isToRightOfInterval(val, interval_tuple):
    start, end = interval_tuple
    is_to_right = val >= start and val >= end
    return is_to_right
  @staticmethod
  def fromIntervalsToEndpoints(intervals, d, do_sort = False):
    endpoints = []
    for interval in intervals:
      start_endpoint, end_endpoint = interval.getStartEndpoint(d), interval.getEndEndpoint(d)
      endpoints.append(start_endpoint)
      endpoints.append(end_endpoint)
    if do_sort == True:
      endpoints = sorted(endpoints, key = lambda x: x.getValue())
    return endpoints
  def haveLeftChild(self):
    return self.getLeftChild() != None
  def haveMiddleChild(self):
    return self.getMiddleChild() != None
  def haveRightChild(self):
    return self.getRightChild() != None
  def toString(self):
    left_child = self.getLeftChild()
    middle_child = self.getMiddleChild()
    right_child = self.getRightChild()
    have_left_child = self.haveLeftChild()
    have_middle_child = self.haveMiddleChild()
    have_right_child = self.haveRightChild()
    result_str = "("
    result_str += left_child.toString() if have_left_child == True else "None"
    result_str += ", "
    middle_str = None
    if have_middle_child == True:
      nodes = middle_child.toInorderInternalNodeList()
      endpoint_list = [x.getElement().getKey() for x in nodes]
      endpoint_value_list = [x.getValue() for x in endpoint_list]
      endpoint_value_str_list = [str(x) for x in endpoint_value_list]
      middle_str = "[" + ", ".join(endpoint_value_str_list) + "]"
    result_str += middle_str if have_middle_child == True else "None"
    result_str += ", "
    result_str += right_child.toString() if have_right_child == True else "None"
    result_str += ")"
    return result_str
  def __repr__(self):
    return self.toString()
  def reportAllForNonMiddle(self, subtree_root, d, start_d, query_di, d_to_lr_value_pair_dict, have_ancestor_contained_by_q):
    left, right = d_to_lr_value_pair_dict[d]
    split_value = self.getSplitValue()
    split_value_is_inside = self.intersectInterval(split_value, (left, right))
    next_have_ancestor_contained_by_q = have_ancestor_contained_by_q or split_value_is_inside
    left_child = subtree_root.getLeftChild()
    middle_child = subtree_root.getMiddleChild()
    right_child = subtree_root.getRightChild()
    have_left_child = subtree_root.haveLeftChild()
    have_middle_child = subtree_root.haveMiddleChild()
    have_right_child = subtree_root.haveRightChild()
    result = []
    if have_left_child == True:
      result.extend(self.reportAllForNonMiddle(subtree_root, left_child, d, start_d, query_di, d_to_lr_value_pair_dict, next_have_ancestor_contained_by_q)[0])
    if have_middle_child == True:
      result.extend(self.reportAllForMiddle(subtree_root, middle_child, d, start_d, query_di)[0])
    if have_right_child == True:
      result.extend(self.reportAllForNonMiddle(subtree_root, right_child, d, start_d, query_di, d_to_lr_value_pair_dict, next_have_ancestor_contained_by_q)[0])
    return (result, [])
  def reportAllForMiddle(self, primary_node, middle_tree, d, start_d, query_di):
    nodes = middle_tree.toInorderInternalNodeList()
    endpoint_list = [x.getElement().getKey() for x in nodes]
    interval_list = [x.getDInterval() for x in endpoint_list]
    unique_interval_list = list(set(interval_list))
    return (unique_interval_list, [])
  def leftToRightSequentialReportForMiddle(self, primary_node, middle_tree, right_endpoint_value, d, start_d, query_di):
    leftmost_internal_node = middle_tree._getMinimumInternalNode(middle_tree.getRoot())
    internal_nodes = self.leftToRightSequentialReportForMiddleHelper(middle_tree, leftmost_internal_node, right_endpoint_value, d, start_d, query_di, [])
    endpoint_list = [x.getElement().getKey() for x in internal_nodes]
    interval_list = [x.getDInterval() for x in endpoint_list]
    unique_interval_list = list(set(interval_list))
    return (unique_interval_list, [])
  def leftToRightSequentialReportForMiddleHelper(self, tree, node, right_endpoint_value, d, start_d, query_di, partial_result):
    if node == None:
      return partial_result
    elif node.getElement().getKey().getValue() > right_endpoint_value:
      return partial_result
    else:
      next_node = tree.getSuccessorInternalNode(node)
      partial_result.append(node)
      self.leftToRightSequentialReportForMiddleHelper(tree, next_node, right_endpoint_value, d, start_d, query_di, partial_result)
  def rightToLeftSequentialReportForMiddle(self, primary_node, middle_tree, left_endpoint_value, d, start_d, query_di):
    rightmost_internal_node = middle_tree._getMaximumInternalNode(middle_tree.getRoot())
    internal_nodes = self.rightToLeftSequentialReportForMiddleHelper(middle_tree, rightmost_internal_node, left_endpoint_value, d, start_d, query_di, [])
    endpoint_list = [x.getElement().getKey() for x in internal_nodes]
    interval_list = [x.getDInterval() for x in endpoint_list]
    unique_interval_list = list(set(interval_list))
    return (unique_interval_list, [])
  def rightToLeftSequentialReportForMiddleHelper(self, tree, node, left_endpoint_value, d, start_d, query_di, partial_result):
    if node == None:
      return partial_result
    elif node.getElement().getKey().getValue() < left_endpoint_value:
      return partial_result
    else:
      next_node = tree.getPredecessorInternalNode(node)
      partial_result.append(node)
      self.rightToLeftSequentialReportForMiddleHelper(tree, next_node, left_endpoint_value, d, start_d, query_di, partial_result)
  @staticmethod
  def getClosestAncestorInIntervalAndPosition(node, left, right):
    parent = node.getParent()
    if parent == None:
      return (None, None)
    else:
      split_value = parent.getSplitValue()
      is_valid_ancestor = node.intersectInterval(split_value, (left, right))
      came_from_right_subtree = parent.haveAsRightChild(node)
      if is_valid_ancestor == True:
        return (parent, came_from_right_subtree)
      else:
        return SFRTNode.getClosestAncestorInIntervalAndPosition(parent, left, right)
  def do1DRangeSearch(self, left, right):
    d = self.getDimension()
    if d != 1:
      raise Exception()
    return self.doDRangeSearch({d: (left, right)}, d, d)
  def doDRangeSearch(self, d_to_lr_value_pair_dict, start_d, end_d):
    return self.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, False)
  def doDRangeSearchHelper(self, d_to_lr_value_pair_dict, start_d, end_d, have_ancestor_contained_by_q):
    d = end_d
    if d < start_d:
      return []
    left, right = d_to_lr_value_pair_dict[d]
    split_value = self.getSplitValue()
    split_value_is_inside = self.intersectInterval(split_value, (left, right))
    split_value_is_to_left = self.isToLeftOfInterval(split_value, (left, right))
    split_value_is_to_right = self.isToRightOfInterval(split_value, (left, right))
    left_child = self.getLeftChild()
    middle_child = self.getMiddleChild()
    right_child = self.getRightChild()
    have_left_child = self.haveLeftChild()
    have_middle_child = self.haveMiddleChild()
    have_right_child = self.haveRightChild()
    query_di = DInterval.fromDToValuePairDict(d_to_lr_value_pair_dict)
    result = []
    if have_ancestor_contained_by_q == False:
      if split_value_is_inside == False:
        if split_value_is_to_right == True:
          if have_middle_child == True:
            result.extend([] if (have_right_child == False or self.getAddressedRightDeficit() == False) else right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, False))
            intervals, lower_level_trees = self.leftToRightSequentialReportForMiddle(self, middle_child, right, d, start_d, query_di)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_left_child == True:
            result.extend(left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, False))
        elif split_value_is_to_left == True:
          if have_middle_child == True:
            result.extend([] if (have_left_child == False or self.getAddressedLeftDeficit() == False) else left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, False))
            intervals, lower_level_trees = self.rightToLeftSequentialReportForMiddle(self, middle_child, left, d, start_d, query_di)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_right_child == True:
            result.extend(right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, False))
      elif split_value_is_inside == True:
        if have_middle_child == True:
          intervals, lower_level_trees = self.reportAllForMiddle(self, middle_child, d, start_d, query_di)
          result.extend(intervals)
          for lower_level_tree in lower_level_trees:
            result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
        if have_left_child == True:
          result.extend(left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
        if have_right_child == True:
          result.extend(right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
    elif have_ancestor_contained_by_q == True:
      closest_ancestor, is_in_right_subtree = SFRTNode.getClosestAncestorInIntervalAndPosition(self, left, right)
      if split_value_is_inside == False:
        if is_in_right_subtree == True:
          if have_middle_child == True:
            result.extend([] if (have_right_child == False or self.getAddressedRightDeficit() == False) else right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
            intervals, lower_level_trees = self.leftToRightSequentialReportForMiddle(self, middle_child, right, d, start_d, query_di)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_left_child == True:
            result.extend(left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
        elif is_in_right_subtree == False:
          if have_middle_child == True:
            result.extend([] if (have_left_child == False or self.getAddressedLeftDeficit() == False) else left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
            intervals, lower_level_trees = self.rightToLeftSequentialReportForMiddle(self, middle_child, left, d, start_d, query_di)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_right_child == True:
            result.extend(right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
        pass
      elif split_value_is_inside == True:
        if is_in_right_subtree == True:
          if have_left_child == True:
            intervals, lower_level_trees = self.reportAllForNonMiddle(left_child, d, start_d, query_di, d_to_lr_value_pair_dict, True)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_middle_child == True:
            result.extend([] if (have_left_child == False or self.getAddressedLeftDeficit() == False) else left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
            intervals, lower_level_trees = self.reportAllForMiddle(self, middle_child, d, start_d, query_di)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_right_child == True:
            result.extend(right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
        elif is_in_right_subtree == False:
          if have_right_child == True:
            intervals, lower_level_trees = self.reportAllForNonMiddle(right_child, d, start_d, query_di, d_to_lr_value_pair_dict, True)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_middle_child == True:
            result.extend([] if (have_right_child == False or self.getAddressedRightDeficit() == False) else right_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
            intervals, lower_level_trees = self.reportAllForMiddle(self, middle_child, d, start_d, query_di)
            result.extend(intervals)
            for lower_level_tree in lower_level_trees:
              result.extend(lower_level_tree.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d - 1, False))
          if have_left_child == True:
            result.extend(left_child.doDRangeSearchHelper(d_to_lr_value_pair_dict, start_d, end_d, True))
    next_result = list(set(result))
    return next_result
class DInterval:
  def __init__(self, d_to_start_end_endpoint_pair_dict, d):
    self.dtseepd = d_to_start_end_endpoint_pair_dict
    self.d = d
    self.is_active = True
  @staticmethod
  def OneDIntervalIntersect(l1, r1, l2, r2):
    return r1 >= l2 and l1 <= r2
  @staticmethod
  def intersectCompletelyBruteForce(d_interval1, d_interval2):
    dimension = d_interval1.getDimension()
    dtvpd1 = d_interval1.toDToValuePairDict()
    dtvpd2 = d_interval2.toDToValuePairDict()
    do_intersect = True
    for i in xrange(1, dimension + 1):
      value_pair1 = dtvpd1[i]
      value_pair2 = dtvpd2[i]
      l1, r1 = value_pair1
      l2, r2 = value_pair2
      if DInterval.OneDIntervalIntersect(l1, r1, l2, r2) == False:
        do_intersect = False
        break
    return do_intersect
  @staticmethod
  def fromDToValuePairDict(d_to_lr_value_pair_dict):
    dtseepd = {}
    d_values = d_to_lr_value_pair_dict.keys()
    max_d_value = max(d_values)
    endpoint_list = []
    for k_v_pair in d_to_lr_value_pair_dict.items():
      d, lr_value_pair = k_v_pair
      l_value, r_value = lr_value_pair
      left_endpoint = Endpoint(l_value, None, d)
      right_endpoint = Endpoint(r_value, None, d)
      start_end_endpoint_pair = (left_endpoint, right_endpoint)
      dtseepd[d] = start_end_endpoint_pair
      endpoint_list.append(left_endpoint)
      endpoint_list.append(right_endpoint)
    d_interval = DInterval(dtseepd, max_d_value)
    for endpoint in endpoint_list:
      endpoint.setDInterval(d_interval)
    return d_interval
  def toDToValuePairDict(self):
    d_to_lr_value_pair_dict = {}
    d = self.getDimension()
    for i in xrange(1, d + 1):
      left = self.getStartEndpoint(i).getValue()
      right = self.getEndEndpoint(i).getValue()
      d_to_lr_value_pair_dict[i] = (left, right)
    return d_to_lr_value_pair_dict
  def isActive(self):
    return self.is_active
  def setIsActive(self, is_active):
    self.is_active = is_active
  def getDimension(self):
    return self.d
  def _getDToStartEndEndpointPairDict(self):
    return self.dtseepd
  def _setDToStartEndEndpointPairDict(self, dtseepd):
    self.dtseepd = dtseepd
  def getStartEndpoint(self, d):
    return self.dtseepd[d][0]
  def getEndEndpoint(self, d):
    return self.dtseepd[d][1]
  @staticmethod
  def constructDInterval(d_to_start_end_pair_dict, d):
    dtseepd = {}
    d_interval = DInterval(None, d)
    for i in xrange(1, d + 1):
      start_end_pair = d_to_start_end_pair_dict[i]
      start_value, end_value = start_end_pair
      start_endpoint = Endpoint(start_value, d_interval, i)
      end_endpoint = Endpoint(end_value, d_interval, i)
      endpoint_pair = (start_endpoint, end_endpoint)
      dtseepd[i] = endpoint_pair
    d_interval._setDToStartEndEndpointPairDict(dtseepd)
    return d_interval
  def toTuple(self, d):
    dtseepd = self._getDToStartEndEndpointPairDict()
    endpoint_pair = dtseepd[d]
    start_endpoint, end_endpoint = endpoint_pair
    start = start_endpoint.getValue()
    end = end_endpoint.getValue()
    pair = (start, end)
    return pair
  def toTupleCollection(self):
    d = self.getDimension()
    tuple_list = []
    for i in xrange(1, d + 1):
      pair = self.toTuple(i)
      tuple_list.append(pair)
    tuple_tuple = tuple(tuple_list)
    return tuple_tuple
  def toString(self):
    tuples = self.toTupleCollection()
    d = self.getDimension()
    result_str = "("
    for i in xrange(1, d + 1):
      curr_tuple = tuples[i - 1]
      start, end = curr_tuple
      curr_str = "(" + str(start) + ", " + str(end) + ")"
      if i != d:
        curr_str += ", "
      result_str += curr_str
    result_str += ")"
    return result_str
  def __repr__(self):
    return self.toString()
class Endpoint:
  def __init__(self, value, d_interval, d):
    self.value = value
    self.d_interval = d_interval
    self.d = d
  def setDInterval(self, d_interval):
    self.d_interval = d_interval
  def getValue(self):
    return self.value
  def getDInterval(self):
    return self.d_interval
  def getDimension(self):
    return self.d
  def toString(self):
    return str(self.getValue())
  def __repr__(self):
    return self.toString()
class ThrowawayEndpoint(Endpoint):
  def __init__(self, value):
    Endpoint.__init__(self, value, None, None)
  def toString(self):
    return "(" + " - ".join(["TA", str(self.getValue())]) + ")"
def main():
  print "hello"
if __name__ == "__main__":
  main()
