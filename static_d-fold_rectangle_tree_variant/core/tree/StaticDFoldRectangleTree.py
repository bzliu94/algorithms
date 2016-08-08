# 2016-07-06

# key insight - possibly not faster than brute force if we just have one query after construction
# faster for when we have multiple queries, say when we have all-intersecting-pairs reporting

# turning off re-distributing between left and right for center leads to a tie for n = 1000 and pypy vs. brute force with pypy

import random
from StaticOneFoldRectangleTree import SOFRT
from StaticFoldRectangleTree import SFRT, SFRTNode, getMedian, getMedianModified, DInterval, SplayTreeWithSplaylessFind, ThrowawayEndpoint
# import numpy as np
class SDFRT(SFRT):
  def __init__(self, d):
    SFRT.__init__(self, d)
  @staticmethod
  def construct(d_intervals, d, first_node_flag = True):
    if d == 1:
      return SOFRT.construct(d_intervals)
    root_node = SDFRTNode.construct(d_intervals, d, first_node_flag)
    tree = SDFRT(d)
    tree.setRoot(root_node)
    return tree
class SDFRTNode(SFRTNode):
  def __init__(self, split_value, d, set_p, primary_type_i_tree, secondary_node_to_set_p_dict, middle_is_dead_end, parent = None, left_child = None, middle_child = None, right_child = None):
    SFRTNode.__init__(self, split_value, d, set_p, secondary_node_to_set_p_dict, parent, left_child, middle_child, right_child)
    self.secondary_node_to_type_one_lower_tree_dict = {}
    self.secondary_node_to_type_two_lower_tree_dict = {}
    self.primary_type_i_tree = primary_type_i_tree
    self.middle_is_dead_end = middle_is_dead_end
    self.addressed_left_deficit = False
    self.addressed_right_deficit = False
  def getAddressedLeftDeficit(self):
    return self.addressed_left_deficit
  def getAddressedRightDeficit(self):
    return self.addressed_right_deficit
  def setAddressedLeftDeficit(self, value):
    self.addressed_left_deficit = value
  def setAddressedRightDeficit(self, value):
    self.addressed_right_deficit = value
  def getMiddleIsDeadEnd(self):
    return self.middle_is_dead_end
  def setMiddleIsDeadEnd(self, middle_is_dead_end):
    self.middle_is_dead_end = middle_is_dead_end
  def getPrimaryTypeOneLowerTree(self):
    return self.primary_type_i_tree
  def setPrimaryTypeOneLowerTree(self, type_i_tree):
    self.primary_type_i_tree = type_i_tree
  def getTypeOneLowerTree(self, secondary_node):
    return self.secondary_node_to_type_one_lower_tree_dict[secondary_node]
  def getTypeTwoLowerTree(self, secondary_node):
    return self.secondary_node_to_type_two_lower_tree_dict[secondary_node]
  def setTypeOneLowerTree(self, secondary_node, lower_tree):
    self.secondary_node_to_type_one_lower_tree_dict[secondary_node] = lower_tree
  def setTypeTwoLowerTree(self, secondary_node, lower_tree):
    self.secondary_node_to_type_two_lower_tree_dict[secondary_node] = lower_tree
  @staticmethod
  def getCrawledNodeToIntervalCollectionDict(secondary_tree):
    node_to_interval_collection_dict = {}
    secondary_tree.crawlNodeToEntryCollectionDict()
    node_to_entry_collection_dict = secondary_tree.getNodeToEntryCollectionDict()
    for k_v_pair in node_to_entry_collection_dict.items():
      node, entry_collection = k_v_pair
      interval_collection = [x.getKey().getDInterval() for x in entry_collection]
      next_interval_collection = list(set(interval_collection))
      node_to_interval_collection_dict[node] = next_interval_collection
    return node_to_interval_collection_dict
  @staticmethod
  def construct(d_intervals, d, first_node_flag = True, parent = None):
    result = SDFRTNode.constructHelper(d_intervals, d, first_node_flag, parent)
    return result
  @staticmethod
  def constructHelper(d_intervals, d, first_node_flag, parent = None):
    if d == 0 or d == 1:
      raise Exception()
    endpoint_values = []
    for d_interval in d_intervals:
      start = d_interval.getStartEndpoint(d).getValue()
      end = d_interval.getEndEndpoint(d).getValue()
      endpoint_values.append(start)
      endpoint_values.append(end)
    split_value = getMedian(endpoint_values)
    left_d_intervals = []
    middle_d_intervals = []
    right_d_intervals = []
    for d_interval in d_intervals:
      d_interval_tuple = d_interval.toTuple(d)
      if SFRTNode.intersectInterval(split_value, d_interval_tuple) == True:
        middle_d_intervals.append(d_interval)
      elif SFRTNode.isToRightOfInterval(split_value, d_interval_tuple) == True:
        left_d_intervals.append(d_interval)
      elif SFRTNode.isToLeftOfInterval(split_value, d_interval_tuple) == True:
        right_d_intervals.append(d_interval)
    average_size = len(d_intervals) / (1.0 * 3)
    middle_surplus = len(middle_d_intervals) - average_size
    addressed_left_deficit = False
    addressed_right_deficit = False
    if len(middle_d_intervals) == 1:
      pass
    else:
      middle_d_interval_set = set(middle_d_intervals)
      for d_interval in middle_d_intervals:
        # change here
        break
        left_deficit = average_size - len(left_d_intervals)
        right_deficit = average_size - len(right_d_intervals)
        if len(middle_d_interval_set) == 1:
          break
        if len(left_d_intervals) <= len(right_d_intervals):
          if left_deficit > 0:
            middle_d_interval_set.remove(d_interval)
            left_d_intervals.append(d_interval)
            addressed_left_deficit = True
          elif right_deficit > 0:
            middle_d_interval_set.remove(d_interval)
            right_d_intervals.append(d_interval)
            addressed_right_deficit = True
        elif len(right_d_intervals) < len(left_d_intervals):
          if right_deficit > 0:
            middle_d_interval_set.remove(d_interval)
            right_d_intervals.append(d_interval)
            addressed_right_deficit = True
          elif left_deficit > 0:
            middle_d_interval_set.remove(d_interval)
            left_d_intervals.append(d_interval)
            addressed_left_deficit = True
      middle_d_intervals = list(middle_d_interval_set)
    result = None
    left_child = None
    endpoints = SFRTNode.fromIntervalsToEndpoints(middle_d_intervals, d)
    entries = [(x, 1) for x in endpoints]
    middle_child = SplayTreeWithSplaylessFind.construct(entries, key_transform = lambda x: x.getValue())
    set_p_dict = SDFRTNode.getCrawledNodeToIntervalCollectionDict(middle_child)
    primary_type_i_tree = None
    if first_node_flag != True:
      if random.randint(0, 1) == 1 and d <= d_intervals[0].getDimension() - 2:
        # if np.random.randint(0, 1) == 1 and d <= d_intervals[0].getDimension() - 2:
        primary_type_i_tree = SDFRT.construct(d_intervals, d - 1, False)
      pass
    node = SDFRTNode(split_value, d, d_intervals, primary_type_i_tree, set_p_dict, False, parent, None, None, None)
    if addressed_left_deficit == True:
      node.setAddressedLeftDeficit(True)
    if addressed_right_deficit == True:
      node.setAddressedRightDeficit(True)
    if len(set_p_dict) == 2:
      node.setMiddleIsDeadEnd(True)
      curr_type_i_tree = primary_type_i_tree
      curr_type_ii_tree = primary_type_i_tree
      k_v_pairs = set_p_dict.items()
      k_v_pair1 = k_v_pairs[0]
      curr_node1, curr_type_i_interval_list1 = k_v_pair1
      node.setTypeOneLowerTree(curr_node1, curr_type_i_tree)
      node.setTypeTwoLowerTree(curr_node1, curr_type_ii_tree)
      k_v_pair2 = k_v_pairs[1]
      curr_node2, curr_type_i_interval_list2 = k_v_pair2
      node.setTypeOneLowerTree(curr_node2, curr_type_i_tree)
      node.setTypeTwoLowerTree(curr_node2, curr_type_ii_tree)
    else:
      node.setMiddleIsDeadEnd(True)
      endpoint_node_to_interval_list_pair_list = set_p_dict.keys()
      endpoint_to_endpoint_node_dict = {}
      for endpoint_node in endpoint_node_to_interval_list_pair_list:
        endpoint = endpoint_node.getElement().getKey()
        endpoint_to_endpoint_node_dict[endpoint] = endpoint_node
      curr_endpoints = [x.getElement().getKey() for x in endpoint_node_to_interval_list_pair_list]
      curr_intervals = [x.getDInterval() for x in curr_endpoints]
      curr_unique_intervals = list(set(curr_intervals))
      for interval in curr_unique_intervals:
        start_endpoint = interval.getStartEndpoint(d)
        end_endpoint = interval.getEndEndpoint(d)
        start_endpoint_node = endpoint_to_endpoint_node_dict[start_endpoint]
        end_endpoint_node = endpoint_to_endpoint_node_dict[end_endpoint]
        curr_type_i_interval_list1 = set_p_dict[start_endpoint_node]
        curr_type_i_interval_list2 = set_p_dict[end_endpoint_node]
        have_same_items = True
        if len(curr_type_i_interval_list1) != len(curr_type_i_interval_list2):
          have_same_items = False
        else:
          curr_interval_set = set(curr_type_i_interval_list1)
          for curr_interval in curr_type_i_interval_list1:
            if curr_interval not in curr_interval_set:
              have_same_items = False
              break
        curr_type_ii_interval = interval
        curr_type_ii_interval_list = [curr_type_ii_interval]
        curr_type_i_tree1 = SDFRT.construct(curr_type_i_interval_list1, d - 1, False)
        curr_type_i_tree2 = None
        curr_type_ii_tree = SDFRT.construct(curr_type_ii_interval_list, d - 1, False)
        if have_same_items == True:
          curr_type_i_tree2 = curr_type_i_tree1
        else:
          curr_type_i_tree2 = SDFRT.construct(curr_type_i_interval_list2, d - 1, False)
        node.setTypeOneLowerTree(start_endpoint_node, curr_type_i_tree1)
        node.setTypeOneLowerTree(end_endpoint_node, curr_type_i_tree2)
        node.setTypeTwoLowerTree(start_endpoint_node, curr_type_ii_tree)
        node.setTypeTwoLowerTree(end_endpoint_node, curr_type_ii_tree)
    right_child = None
    if len(left_d_intervals) != 0:
      left_child = SDFRTNode.constructHelper(left_d_intervals, d, False, node)
    if len(right_d_intervals) != 0:
      right_child = SDFRTNode.constructHelper(right_d_intervals, d, False, node)
    node.setLeftChild(left_child)
    node.setMiddleChild(middle_child)
    node.setRightChild(right_child)
    return node
  def reportAllForNonMiddle(self, subtree_root, d, start_d, query_di, d_to_lr_value_pair_dict, have_ancestor_contained_by_q):
    if d == start_d:
      return SFRTNode.reportAllForNonMiddle(self, subtree_root, d, start_d, query_di)
    next_intervals = []
    primary_trees = []
    primary_type_i_tree = self.getPrimaryTypeOneLowerTree()
    if primary_type_i_tree != None:
      primary_trees.append(primary_type_i_tree)
    else:
      intervals = self.getSetP()
      next_intervals = [x for x in intervals if DInterval.intersectCompletelyBruteForce(query_di, x) == True]
    return (next_intervals, primary_trees)
  def reportAllForMiddle(self, primary_node, middle_tree, d, start_d, query_di):
    if d == start_d:
      return SFRTNode.reportAllForMiddle(self, primary_node, middle_tree, d, start_d, query_di)
    primary_trees = []
    intervals = []
    if primary_node.getMiddleIsDeadEnd() == True:
      curr_intervals = [x.getElement().getKey().getDInterval() for x in middle_tree.toInorderInternalNodeList()]
      next_curr_intervals = list(set(curr_intervals))
      for curr_interval in next_curr_intervals:
        if DInterval.intersectCompletelyBruteForce(query_di, curr_interval):
          intervals.append(curr_interval)
    return (intervals, primary_trees)
  def leftToRightSequentialReportForMiddle(self, primary_node, middle_tree, right_endpoint_value, d, start_d, query_di):
    if d == start_d:
      return SFRTNode.leftToRightSequentialReportForMiddle(self, primary_node, middle_tree, right_endpoint_value, d, start_d, query_di)
    leftmost_key = middle_tree.getMinimalKeyValue()
    if leftmost_key == None:
      return ([], [])
    left_boundary_key = leftmost_key
    right_boundary_key = ThrowawayEndpoint(right_endpoint_value)
    tagged_secondary_nodes = middle_tree.getDisjointSubtreeRootsForRange(left_boundary_key, right_boundary_key)
    primary_trees = []
    intervals = []
    if True:
      for tagged_secondary_node in tagged_secondary_nodes:
        type_tag, secondary_node = tagged_secondary_node
        if type_tag == 1:
          tree = self.getTypeOneLowerTree(secondary_node)
          if tree != None:
            primary_trees.append(tree)
        elif type_tag == 2:
          tree = self.getTypeTwoLowerTree(secondary_node)
          if tree != None:
            primary_trees.append(tree)
    return (intervals, primary_trees)
  def rightToLeftSequentialReportForMiddle(self, primary_node, middle_tree, left_endpoint_value, d, start_d, query_di):
    if d == start_d:
      return SFRTNode.rightToLeftSequentialReportForMiddle(self, primary_node, middle_tree, left_endpoint_value, d, start_d, query_di)
    left_boundary_key = ThrowawayEndpoint(left_endpoint_value)
    rightmost_key = middle_tree.getMaximalKeyValue()
    if rightmost_key == None:
      return ([], [])
    right_boundary_key = rightmost_key
    tagged_secondary_nodes = middle_tree.getDisjointSubtreeRootsForRange(left_boundary_key, right_boundary_key)
    primary_trees = []
    intervals = []
    if True:
      for tagged_secondary_node in tagged_secondary_nodes:
        type_tag, secondary_node = tagged_secondary_node
        if type_tag == 1:
          tree = self.getTypeOneLowerTree(secondary_node)
          if tree != None:
            primary_trees.append(tree)
        elif type_tag == 2:
          tree = self.getTypeTwoLowerTree(secondary_node)
          if tree != None:
            primary_trees.append(tree)
    return (intervals, primary_trees)
def main():
  import cProfile, pstats, StringIO
  """
  next_d = 2
  next_i1 = DInterval.constructDInterval({1: (0, 3), 2: (1, 4)}, next_d)
  next_i2 = DInterval.constructDInterval({1: (1, 5), 2: (2, 6)}, next_d)
  next_i3 = DInterval.constructDInterval({1: (2, 8), 2: (3, 9)}, next_d)
  next_i4 = DInterval.constructDInterval({1: (4, 6), 2: (5, 7)}, next_d)
  next_i5 = DInterval.constructDInterval({1: (7, 9), 2: (8, 10)}, next_d)
  next_i6 = DInterval.constructDInterval({1: (10, 11), 2: (11, 12)}, next_d)
  next_d_intervals = [next_i1, next_i2, next_i3, next_i4, next_i5]
  next_tree = SDFRT.construct(next_d_intervals, next_d)
  print next_tree
  query_i1 = DInterval.constructDInterval({1: (0, 9), 2: (1, 10)}, next_d)
  print next_tree.doDRangeSearch(query_i1, 1, 1)
  query_i2 = DInterval.constructDInterval({1: (0, 1), 2: (1, 10)}, next_d)
  print next_tree.doDRangeSearch(query_i2, 1, 2)
  query_i3 = DInterval.constructDInterval({1: (0, 9), 2: (1, 10)}, next_d)
  print next_tree.doDRangeSearch(query_i3, 1, 2)
  query_i4 = DInterval.constructDInterval({1: (-2, -1), 2: (1, 10)}, next_d)
  print next_tree.doDRangeSearch(query_i4, 1, 2)
  query_i5 = DInterval.constructDInterval({1: (0, 9), 2: (1, 4)}, next_d)
  print next_tree.doDRangeSearch(query_i5, 2, 2)
  """
  """
  pr = cProfile.Profile()
  pr.enable()
  """
  intervals = []
  # num_intervals = 100
  num_intervals = 1000
  # num_intervals = 1500
  # num_intervals = 2000
  # num_intervals = 3000
  # num_intervals = 750
  # num_intervals = 375
  # num_intervals = 100
  # d = 10
  d = 35
  for i in xrange(num_intervals):
    d_to_end_value_pair_dict = {}
    for j in xrange(1, d + 1):
      start = random.randint(0, 100)
      # start = random.random() * 100
      end = start + 0.5
      end_value_pair = (start, end)
      d_to_end_value_pair_dict[j] = end_value_pair
    curr_interval = DInterval.constructDInterval(d_to_end_value_pair_dict, d)
    intervals.append(curr_interval)
  import time
  time1 = time.time()
  tree = SDFRT.construct(intervals, d)
  query_d_to_end_value_pair_dict = {}
  for i in xrange(1, d + 1):
    start = 0
    end = 50
    end_value_pair = (start, end)
    query_d_to_end_value_pair_dict[i] = end_value_pair
  query_interval = DInterval.constructDInterval(query_d_to_end_value_pair_dict, d)
  """																																																																																																																																							
  brute_force_result = []
  for interval in intervals:
    does_intersect = DInterval.intersectCompletelyBruteForce(query_interval, interval)
    if does_intersect == True:
      brute_force_result.append(interval)
  brute_force_result_set = set(brute_force_result)
  result_set = set(result)
  import pdb
  if brute_force_result_set != result_set:
    print len(brute_force_result_set), len(result_set)
    pdb.set_trace()
    next_result = tree.doDRangeSearch(query_interval, 1, d)
    # raise Exception()
  """
  """
  for i in xrange(2000):
    result = tree.doDRangeSearch(query_interval, 1, d)
  """
  for i in xrange(1):
    for curr_interval in intervals:
      intersected_intervals = []
      result = tree.doDRangeSearch(curr_interval, 1, d)
      intersected_intervals = result
  time2 = time.time()
  print time2 - time1, "seconds"
  """
  pr.disable()
  s = StringIO.StringIO()
  sortby = 'cumulative'
  ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
  ps.print_stats()
  # print s.getvalue()
  """
if __name__ == "__main__":
  main()
