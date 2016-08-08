from StaticFoldRectangleTree import SFRT, SFRTNode, getMedian, DInterval, SplayTreeWithSplaylessFind
class SOFRT(SFRT):
  def __init__(self):
    SFRT.__init__(self, 1)
  @staticmethod
  def construct(d_intervals):
    root_node = SOFRTNode.construct(d_intervals)
    tree = SOFRT()
    tree.setRoot(root_node)
    return tree
class SOFRTNode(SFRTNode):
  def __init__(self, split_value, set_p, secondary_node_to_set_p_dict, parent = None, left_child = None, middle_child = None, right_child = None):
    SFRTNode.__init__(self, split_value, 1, set_p, secondary_node_to_set_p_dict, parent, left_child, middle_child, right_child)
  @staticmethod
  def construct(d_intervals, parent = None):
    endpoint_values = []
    for d_interval in d_intervals:
      start = d_interval.getStartEndpoint(1).getValue()
      end = d_interval.getEndEndpoint(1).getValue()
      endpoint_values.append(start)
      endpoint_values.append(end)
    split_value = getMedian(endpoint_values)
    left_d_intervals = []
    middle_d_intervals = []
    right_d_intervals = []
    for d_interval in d_intervals:
      d_interval_tuple = d_interval.toTuple(1)
      if SFRTNode.intersectInterval(split_value, d_interval_tuple) == True:
        middle_d_intervals.append(d_interval)
      elif SFRTNode.isToRightOfInterval(split_value, d_interval_tuple) == True:
        left_d_intervals.append(d_interval)
      elif SFRTNode.isToLeftOfInterval(split_value, d_interval_tuple) == True:
        right_d_intervals.append(d_interval)
    result = None
    left_child = None
    endpoints = SFRTNode.fromIntervalsToEndpoints(middle_d_intervals, 1)
    entries = [(x, 1) for x in endpoints]
    middle_child = SplayTreeWithSplaylessFind.construct(entries, key_transform = lambda x: x.getValue())
    right_child = None
    node = SOFRTNode(split_value, None, None, parent, None, None, None)
    if len(left_d_intervals) != 0:
      left_child = SOFRTNode.construct(left_d_intervals, node)
    if len(right_d_intervals) != 0:
      right_child = SOFRTNode.construct(right_d_intervals, node)
    node.setLeftChild(left_child)
    node.setMiddleChild(middle_child)
    node.setRightChild(right_child)
    return node
def main():
  d = 1
  i1 = DInterval.constructDInterval({1: (0, 3)}, d)
  i2 = DInterval.constructDInterval({1: (1, 5)}, d)
  i3 = DInterval.constructDInterval({1: (2, 8)}, d)
  i4 = DInterval.constructDInterval({1: (4, 6)}, d)
  i5 = DInterval.constructDInterval({1: (7, 9)}, d)
  i6 = DInterval.constructDInterval({1: (10, 11)}, d)
  endpoints = []
  d_intervals = [i1, i2, i3, i4, i5]
  tree = SOFRT.construct(d_intervals)
  print tree
  print tree.do1DRangeSearch(1, 2)
if __name__ == "__main__":
  main()
