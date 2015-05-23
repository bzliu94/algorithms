from ...tree.bbst.SplayTree import *

from ...tree.Entry import *

from BalancedIntervalTreeNode import *

from Interval import *

from IntervalEntry import *

# maintain for each node a max field 
# for storing max value of a right endpoint 
# of an interval in the subtree 
# rooted at the node

# use as key the interval

# internally, use left endpoint as key

class BalancedIntervalTree(SplayTree):

  def __init__(self, key_transform = lambda x: x.getLeftEndpoint(), comparator = comp):

    # key internal representation is an interval object

    # transformed key is interval left endpoint

    # key_transform = lambda x: x.getLeftEndpoint()

    SplayTree.__init__(self, key_transform, comparator)

  # entries are (interval, value) pairs

  @staticmethod

  def construct(entries):

    tree = BalancedIntervalTree()

    for entry in entries:

      key, value = entry

      tree.intervalInsert(key, value)

    return tree

  def _expandExternal(self, external_node, left_entry, right_entry):
  
    self._expandExternalHelper(external_node, left_entry, right_entry, BalancedIntervalTreeNode)
    
  def addRoot(self, entry):

    self._addRootHelper(entry, BalancedIntervalTreeNode)

  # return an entry
  
  def _insertIntroduceEntry(self, key, value, ins_node):
  
    return self._insertAtExternal(ins_node, IntervalEntry(key, value))

  # return an (entry, node) pair
    
  def _insertWithUntransformedKeyForTree(self, untransformed_key, value):

    # return self._insertHelper(untransformed_key, value, self._treeSearchWithUntransformedKey)

    return self.insert(untransformed_key, value)

  # remove an entry with matching (transformed) key

  # note: entry provided should involve untransformed key

  # return an (entry, node) pair

  def _removeForTree(self, entry):

    # return self._removeHelper(entry, self._treeSearch)
    
    return self.remove(entry)

  """

  # return an (entry, node) pair

  def _removeForTree(self, entry_with_transformed_key):

    # return self._removeHelper(entry_with_transformed_key, self._treeSearch)
    
    return self.remove(entry_with_transformed_key)

  """

  """
    
  # return an (entry, node) pair
  
  def _removeWithUntransformedKeyForTree(self, entry_with_untransformed_key):

    # return self._removeHelper(entry_with_untransformed_key, self._treeSearchWithUntransformedKey)
    
    return self.removeWithUntransformedKey(entry_with_untransformed_key)

  """
    
  """

  # return an entry
    
  def insert(self, transformed_key, value):
  
    return (self._insertForTree(transformed_key, value))[0]

  # return an entry

  def remove(self, entry_with_transformed_key):
  
    return (self._removeForTree(entry_with_transformed_key))[0]

  """

  """

  # do not assume node is an internal node

  def _updateMaxValuesForParents(self, node):

    if node.isExternal() == True:

      return

  """

  # update max values for node and its parents

  # do not assume node is an internal node

  def _updateMaxValuesForParents(self, node):
  
    if node == self.getRoot():
    
      return

    elif node.isExternal() == True:

      self._updateMaxValuesForParents(node.getParent())

    elif node.isExternal() == False:
    
      # candidate_values = []

      tagged_candidate_node_options = []
      
      if node.hasLeftChild() == True:
      
        # candidate_values.append(node.getLeftChild().getMax())
        
        tagged_candidate_node_options.append((node.getLeftChild(), True))

      if node.hasRightChild() == True:
      
        # candidate_values.append(node.getRightChild().getMax())
        
        tagged_candidate_node_options.append((node.getRightChild(), True))

      # curr_right_endpoint = node.getElement().getKey().getRightEndpoint()

      tagged_candidate_node_options.append((node, False))

      # candidate_values.append(curr_right_endpoint)
      
      # next_max_value = max(candidate_values)

      tagged_interval = self.chooseFromCandidates(BalancedIntervalTree._toTaggedIntervals(tagged_candidate_node_options))

      # entry, is_from_max_bearing_node = tagged_entry

      # self._setMaxValue(node, tagged_entry)

      self._setMaxValue(node, tagged_interval)

      # node.setMax(next_max_value)

      self._updateMaxValuesForParents(node.getParent())

  # i is an interval and has form of an Interval object
  
  # return an (entry, node) pair

  def intervalInsert(self, i, value):

    """

    if i.getLeftEndpoint() > i.getRightEndpoint():

      print i.getLeftEndpoint(), i.getRightEndpoint()

      raise Exception("unexpected endpoints with insertion of an interval")

    """
  
    # actually insert

    entry, node = self._insertWithUntransformedKeyForTree(i, value)
    
    # take care of inserted node's max value
    
    right_endpoint = i.getRightEndpoint()
    
    # print "introduced interval's right_endpoint:", right_endpoint

    # entry = node.getElement()

    # node.setMax(right_endpoint)

    tagged_entry = (entry, False)

    # responsible_interval = BalancedIntervalTree.toResponsibleInterval(tagged_entry)

    responsible_interval = BalancedIntervalTree._toTaggedResponsibleInterval(tagged_entry)

    # print entry.getKey()

    self._setMaxValue(node, responsible_interval)

    """
    
    # take care of max values

    tree_search = self._treeSearchWithUntransformedKey
    
    ins_node = self._insertRetrieveNode(i, value, tree_search)
  
    self._updateMaxValuesForParents(ins_node)
    
    """
    
    # take care of max values
    
    self._updateMaxValuesForParents(node)

    return (entry, node)

  # i is an interval and has form of an Interval object
  
  # return an (entry, node) pair

  def intervalDelete(self, i, value):

    # entry, node = self.find(i)

    # print entry.toString()

    # raise Exception("attempting to remove an interval")

    """

    interval_entries = self.findAll(i.getLeftEndpoint())

    matching_interval_entries = [x for x in interval_entries if x[0].isEqualTo(i)]

    chosen_interval_entry = matching_intervals[0]

    self.remove(IntervalEntry((chosen_interval_entry[0]).getLeftEndpoint(), value))

    """
    
    # for taking care of max values
    
    # tree_search = self._treeSearchWithUntransformedKey

    # print "interval to be removed:", i.toString(), value
    
    # w = self.removeRetrieveNode(IntervalEntry(i, value), tree_search)
    
    w = self._removeRetrieveNode(IntervalEntry(i, value))

    """

    print w.isExternal()

    print self.toString()

    """
    
    rem_node = self._removeRetrieveReplacementNode(w)
    
    rem_node_sibling = rem_node.getSibling()
    
    """

    # actually remove

    self.removeWithUntransformedKey(IntervalEntry(i, value))
    
    """
    
    # actually remove
    
    # entry, node = self._removeWithUntransformedKeyForTree(IntervalEntry(i, value))

    entry, node = self._removeForTree(IntervalEntry(i, value))
    
    # take care of max values
    
    self._updateMaxValuesForParents(rem_node_sibling)
    
    return (entry, node)

    """
    
    # actually remove
    
    entry, node = self._removeForTree(i, value)
    
    # take care of max values
    
    self._updateMaxValuesForParents(node)

    """

  @staticmethod

  def _toTaggedResponsibleInterval(tagged_entry):

    entry, is_max_bearing = tagged_entry

    # print entry.getKey().toString()

    responsible_interval = None

    if is_max_bearing == True:

      responsible_interval = entry.getLocation().getMaxRightEndpoint().getResponsibleInterval()

    elif is_max_bearing == False:

      responsible_interval = entry.getKey()

    # print tagged_entry, is_max_bearing

    return (responsible_interval, is_max_bearing)

  @staticmethod

  def _toTaggedIntervals(tagged_node_options):

    # print "tagged node options:", tagged_node_options

    tagged_nodes = [x for x in tagged_node_options if x[0] != None]

    tagged_entry_options = [((x[0]).getElement(), x[1]) for x in tagged_nodes]

    tagged_entries = [x for x in tagged_entry_options if x[0] != None]

    # print "tagged entries:", tagged_entries

    # return tagged_entries

    tagged_intervals = [BalancedIntervalTree._toTaggedResponsibleInterval(x) for x in tagged_entries]

    # print [(x[0]).toString() for x in tagged_intervals]

    # print "tagged intervals:", tagged_intervals

    return tagged_intervals

  """

  @staticmethod

  def toResponsibleInterval(tagged_entry):

    entry, is_max_bearing = tagged_entry

    node = entry.getLocation()

    # responsible_interval = node.getResponsibleInterval()

    responsible_interval = node.getMaxRightEndpoint().getResponsibleInterval()

    # print "found responsible interval:", responsible_interval

    return responsible_interval

  """

  def _getTaggedCandidateIntervalsWithMaxMaxValue(self, tagged_intervals):

    candidate_values = [self._getCandidateValue(x) for x in tagged_intervals]

    max_candidate_value = max(candidate_values)

    tagged_interval_candidate_value_pairs = [(x, self._getCandidateValue(x)) for x in tagged_intervals]

    matching_tagged_interval_candidate_value_pairs = [x for x in tagged_interval_candidate_value_pairs if x[1] == max_candidate_value]

    matching_tagged_intervals = [x[0] for x in matching_tagged_interval_candidate_value_pairs]

    return matching_tagged_intervals

  def _chooseTaggedResponsibleInterval(self, tagged_intervals):

    matching_tagged_intervals = self._getTaggedCandidateIntervalsWithMaxMaxValue(tagged_intervals)

    matching_tagged_interval = matching_tagged_intervals[0]

    """

    matching_tagged_interval_candidate_value_pair = matching_tagged_interval_candidate_value_pairs[0]

    matching_tagged_interval = matching_tagged_interval_candidate_value_pair[0]

    """

    return matching_tagged_interval

  # choose from tagged candidate nodes

  def chooseFromCandidates(self, tagged_candidate_intervals):

    # print "choosing from candidates:", tagged_candidate_intervals

    tagged_responsible_interval = self._chooseTaggedResponsibleInterval(tagged_candidate_intervals)

    return tagged_responsible_interval

    """

    tagged_max_bearing_intervals = [x for x in tagged_candidate_intervals if x[1] == True]

    tagged_specific_intervals = [x for x in tagged_candidate_intervals if x[1] == False]

    """

    """

    # print tagged_max_bearing_entries, tagged_specific_entries

    # max_bearing_entries = [x[0] for x in tagged_max_bearing_entries]

    max_bearing_candidate_values = [self._getCandidateValue(x) for x in tagged_max_bearing_intervals]

    # specific_entries = [x[0] for x in tagged_specific_entries]

    specific_candidate_values = [self._getCandidateValue(x) for x in tagged_specific_intervals]

    candidate_values = max_bearing_candidate_values + specific_candidate_values

    max_value = max(candidate_values)

    """

    """

    if max_value in max_bearing_candidate_values:

      # matching_max_bearing_entries = [x for x in max_bearing_entries if self._getCandidateValues(x) == max_value]

      # chosen_max_bearing_entry = matching_max_bearing_entries[0]

      # return (chosen_max_bearing_entry, True)

      matching_tagged_max_bearing_intervals = [x for x in tagged_max_bearing_intervals if self._getCandidateValue(x) == max_value]

      chosen_tagged_max_bearing_interval = matching_tagged_max_bearing_intervals[0]

      # responsible_interval = BalancedIntervalTree.toResponsibleInterval(chosen_max_bearing_interval)

      # return (chosen_max_bearing_entry, responsible_interval)

      return chosen_tagged_max_bearing_interval

    elif max_value in specific_candidate_values:

      # matching_specific_entries = [x for x in specific_entries if self._getCandidateValues(x) == max_value]

      # chosen_specific_entry = matching_specific_entries[0]

      # return (chosen_specific_entry, False)

      matching_tagged_specific_intervals = [x for x in tagged_specific_intervals if self._getCandidateValue(x) == max_value]

      chosen_tagged_specific_interval = matching_tagged_specific_intervals[0]

      # responsible_interval = BalancedIntervalTree.toResponsibleInterval(chosen_specific_entry)

      # return (chosen_specific_entry, responsible_interval)

      return chosen_tagged_specific_interval

    """

  # retrieve a scalar

  def _getCandidateValue(self, tagged_interval):

    interval, is_max_bearing = tagged_interval

    """

    if interval == 1:

      raise Exception()

    """

    if interval == None:

      return None

    # entry, is_max_bearing = tagged_entry

    # print tagged_entry

    # return node.getMaxValue()

    # node = entry.getLocation()

    # return node.getMaxValue()

    candidate_value = None

    if is_max_bearing == True:

      # candidate_value = node.getMaxRightEndpoint().getValue()

      candidate_value = interval.getRightEndpoint()

    else:

      # candidate_value = node.getElement().getKey().getRightEndpoint()

      candidate_value = interval.getRightEndpoint()

    # print max_value

    return candidate_value

  # set a max value based on a tagged mediating entry

  def _setMaxValue(self, node, tagged_responsible_interval):

    responsible_interval, is_max_bearing = tagged_responsible_interval

    """

    source_entry, is_max_bearing = tagged_source_entry

    source_node = source_entry.getLocation()

    max_value = source_node.getMaxRightEndpoint().getValue()

    node.getMaxRightEndpoint().setValue(max_value)

    """

    # print node.getElement().getKey().toString(), responsible_interval.toString()

    if responsible_interval == None:

      # may be dealing with external nodes

      pass

    else:

      max_value = responsible_interval.getRightEndpoint()

      max_right_endpoint = node.getMaxRightEndpoint()

      max_right_endpoint.setValue(max_value)

      max_right_endpoint.setResponsibleInterval(responsible_interval)

      """

      print node.getElement().getKey().toString(), max_value

      if node.getElement().getKey().getRightEndpoint() < max_value:

        raise Exception()

      """

    # print max_right_endpoint.getResponsibleInterval()

  def _zig_zig(self, x):

    # take care of max values

    y = x.getParent()

    z = y.getParent()

    if x.isLeftChild() == True:

      # left, left

      # print "splay substep: LL"

      t1 = x.getLeftChild()

      t2 = x.getRightChild()

      t3 = y.getRightChild()

      t4 = z.getRightChild()
      
      """
      
      print x, y, z
      
      print t1, t2, t3, t4
      
      """

      z_tagged_candidate_node_options = [(t3, True), (t4, True), (z, False)]

      z_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(z_tagged_candidate_node_options)

      z_tagged_interval = self.chooseFromCandidates(z_tagged_candidate_intervals)

      y_tagged_candidate_node_options = [(t2, True), (y, False)]

      y_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(y_tagged_candidate_node_options)

      y_tagged_candidate_intervals = y_tagged_candidate_intervals + [z_tagged_interval]

      y_tagged_interval = self.chooseFromCandidates(y_tagged_candidate_intervals)

      x_tagged_candidate_node_options = [(t1, True), (x, False)]

      x_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(x_tagged_candidate_node_options)

      x_tagged_candidate_intervals = x_tagged_candidate_intervals + [y_tagged_interval]

      x_tagged_interval = self.chooseFromCandidates(x_tagged_candidate_intervals)

      self._setMaxValue(x, x_tagged_interval)

      self._setMaxValue(y, y_tagged_interval)

      self._setMaxValue(z, z_tagged_interval)

    else:

      # right, right

      # print "splay substep: RR"

      t1 = z.getLeftChild()

      t2 = y.getLeftChild()

      t3 = x.getLeftChild()

      t4 = x.getRightChild()

      z_tagged_candidate_node_options = [(t1, True), (t2, True), (z, False)]

      z_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(z_tagged_candidate_node_options)

      z_tagged_interval = self.chooseFromCandidates(z_tagged_candidate_intervals)

      y_tagged_candidate_node_options = [(t3, True), (y, False)]

      y_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(y_tagged_candidate_node_options)

      y_tagged_candidate_intervals = y_tagged_candidate_intervals + [z_tagged_interval]

      y_tagged_interval = self.chooseFromCandidates(y_tagged_candidate_intervals)

      x_tagged_candidate_node_options = [(t4, True), (x, False)]

      x_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(x_tagged_candidate_node_options)

      x_tagged_candidate_intervals = x_tagged_candidate_intervals + [y_tagged_interval]

      x_tagged_interval = self.chooseFromCandidates(x_tagged_candidate_intervals)

      self._setMaxValue(x, x_tagged_interval)

      self._setMaxValue(y, y_tagged_interval)

      self._setMaxValue(z, z_tagged_interval)

    SplayTree._zig_zig(self, x)

  def _zig_zag(self, x):

    # take care of max values

    y = x.getParent()

    z = y.getParent()

    if x.isRightChild() == True:

      # left, right

      # print "splay substep: LR"

      t1 = y.getLeftChild()

      t2 = x.getLeftChild()

      t3 = x.getRightChild()

      t4 = z.getRightChild()

      y_tagged_candidate_node_options = [(t1, True), (t2, True), (y, False)]

      y_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(y_tagged_candidate_node_options)

      y_tagged_interval = self.chooseFromCandidates(y_tagged_candidate_intervals)

      z_tagged_candidate_node_options = [(t3, True), (t4, True), (z, False)]

      z_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(z_tagged_candidate_node_options)

      z_tagged_interval = self.chooseFromCandidates(z_tagged_candidate_intervals)

      x_tagged_candidate_node_options = [(x, False)]

      x_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(x_tagged_candidate_node_options)

      x_tagged_candidate_intervals = x_tagged_candidate_intervals + [y_tagged_interval, z_tagged_interval]

      x_tagged_interval = self.chooseFromCandidates(x_tagged_candidate_intervals)

      self._setMaxValue(x, x_tagged_interval)

      self._setMaxValue(y, y_tagged_interval)

      self._setMaxValue(z, z_tagged_interval)

    else:

      # right, left

      # print "splay substep: RL"

      t1 = z.getLeftChild()

      t2 = x.getLeftChild()

      t3 = x.getRightChild()

      t4 = y.getRightChild()

      z_tagged_candidate_node_options = [(t1, True), (t2, True), (z, False)]

      z_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(z_tagged_candidate_node_options)

      z_tagged_interval = self.chooseFromCandidates(z_tagged_candidate_intervals)

      y_tagged_candidate_node_options = [(t3, True), (t4, True), (y, False)]

      """

      t3_responsible_interval = t3.getMaxRightEndpoint().getResponsibleInterval()

      t4_responsible_interval = t4.getMaxRightEndpoint().getResponsibleInterval()

      y_interval = y.getElement().getKey()

      print "y candidate node options:"

      print t3_responsible_interval.toString() if t3_responsible_interval != None else None

      print t4_responsible_interval.toString() if t4_responsible_interval != None else None

      print y_interval.toString() if y_interval != None else None

      """

      y_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(y_tagged_candidate_node_options)

      y_tagged_interval = self.chooseFromCandidates(y_tagged_candidate_intervals)

      x_tagged_candidate_node_options = [(x, False)]

      x_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(x_tagged_candidate_node_options)

      x_tagged_candidate_intervals = x_tagged_candidate_intervals + [y_tagged_interval, z_tagged_interval]

      x_tagged_interval = self.chooseFromCandidates(x_tagged_candidate_intervals)

      """

      print "y tagged responsible interval:", y_tagged_interval

      print "y responsible interval:", (y_tagged_interval[0]).toString()

      """

      self._setMaxValue(x, x_tagged_interval)

      self._setMaxValue(y, y_tagged_interval)

      self._setMaxValue(z, z_tagged_interval)

    SplayTree._zig_zag(self, x)

  def _zig(self, x):

    # take care of max values

    y = x.getParent()

    w1 = x.getLeftChild()

    w2 = x.getRightChild()

    if x.isLeftChild() == True:

      # left

      # print "splay substep: L"

      t3 = x.getRightChild()

      t4 = y.getRightChild()

      y_tagged_candidate_node_options = [(t3, True), (t4, True), (y, False)]

      y_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(y_tagged_candidate_node_options)

      y_tagged_interval = self.chooseFromCandidates(y_tagged_candidate_intervals)

      x_tagged_candidate_node_options = [(w1, True), (x, False)]

      x_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(x_tagged_candidate_node_options)

      x_tagged_candidate_intervals = x_tagged_candidate_intervals + [y_tagged_interval]

      x_tagged_interval = self.chooseFromCandidates(x_tagged_candidate_intervals)

      self._setMaxValue(x, x_tagged_interval)

      self._setMaxValue(y, y_tagged_interval)

    else:

      # right

      # print "splay substep: LL"

      t1 = y.getLeftChild()

      t2 = x.getLeftChild()

      y_tagged_candidate_node_options = [(t1, True), (t2, True), (y, False)]

      y_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(y_tagged_candidate_node_options)

      # print "y tagged candidate node options:", y_tagged_candidate_node_options

      # print "y tagged candidate intervals:", y_tagged_candidate_intervals

      y_tagged_interval = self.chooseFromCandidates(y_tagged_candidate_intervals)

      x_tagged_candidate_node_options = [(w2, True), (x, False)]

      x_tagged_candidate_intervals = BalancedIntervalTree._toTaggedIntervals(x_tagged_candidate_node_options)

      x_tagged_candidate_intervals = x_tagged_candidate_intervals + [y_tagged_interval]

      x_tagged_interval = self.chooseFromCandidates(x_tagged_candidate_intervals)

      # print x_tagged_interval, x_responsible_interval

      self._setMaxValue(x, x_tagged_interval)

      self._setMaxValue(y, y_tagged_interval)

    SplayTree._zig(self, x)

  # retrieve a node corresponding to one overlapped interval, 
  #   with ties between intervals resolved arbitrarily
  
  # interval is an interval object
  
  # return an (entry, node) pair

  # takes O(log(n)) time

  def intervalSearch(self, interval):

    node = self._intervalSearchHelper(interval, None, self.getRoot())

    entry = node.getElement()

    return (entry, node)

  # assume the tree is not empty

  # returns an internal node 
  #   or an external node 
  #   where interval should go

  def _intervalSearchHelper(self, interval, prev_node, curr_node):

    # print "interval search - interval:", interval.toString()

    if curr_node.isExternal() == True:

      return prev_node

    else:

      curr_interval = curr_node.getElement().getKey()

      # print "interval search - current interval:", curr_interval.toString()

      if curr_interval.overlapsInterval(interval):

        # print "interval search - interval overlap:", curr_interval.toString(), interval.toString()

        return curr_node

      # travel in a safe direction

      have_left_child = curr_node.hasLeftChild()

      left_endpoint = interval.getLeftEndpoint()

      """

      if have_left_child == True:

        print "max value:", curr_node.getLeftChild().getMax()

      """

      # look_at_left = have_left_child and curr_node.getLeftChild().getMax() >= left_endpoint

      look_at_left = have_left_child and curr_node.getLeftChild().getMaxValue() >= left_endpoint

      look_at_right = not look_at_left

      if look_at_left == True:

        return self._intervalSearchHelper(interval, curr_node, curr_node.getLeftChild())

      elif look_at_right == True:

        return self._intervalSearchHelper(interval, curr_node, curr_node.getRightChild())

  """

  # retrieve a node corresponding to one overlapped interval, 
  #   with ties between intervals resolved arbitrarily
  
  # i is an interval object
  
  # return an (entry, node) pair

  # if no overlapped interval, return None

  def intervalSearch(self, i):

    node = self._intervalSearch(i)

    print node == None

    if node == None:

      return None

    interval = node.getElement().getKey()

    entry = node.getElement()

    if interval.overlapsInterval(i):

      return (entry, node)

    else:

      return None

  # assume the tree is not empty

  # returns a node

  def _intervalSearch(self, i):

    x = self.getRoot()

    if self.isEmpty() == True:

      raise Exception("tree is empty")
    
    curr_interval = x.getElement().getKey()

    # print x.getElement().toString()

    # print curr_interval

    # print x.getMax()
    
    while x != None and not curr_interval.overlapsInterval(i):

      if x.hasLeftChild() == True \
        and x.getLeftChild().getMax() >= i.getLeftEndpoint():

        x = x.getLeftChild()
      
      else:
      
        x = x.getRightChild()
        
    return x

  """

  """

  def _toString(self, node):

    if node == None:

      # non-existent node

      return "None"

    else:

      left_child_str = self._toString(node.getLeftChild())

      curr_element = node.getElement()

      if curr_element != None:

        curr_entry_str = str(self.getKeyString(node))

      else:

        # non-existent key (possibly because entry does not exist)

        curr_entry_str = "None"

      right_child_str = self._toString(node.getRightChild())

      partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"

      return partial_str

  def getKeyString(self, node):

    entry = node.getElement()

    interval = entry.getKey()

    left_endpoint = interval.getLeftEndpoint()

    right_endpoint = interval.getRightEndpoint()

    result_str = "[" + str(left_endpoint) + ", " + str(right_endpoint) + "]"

    return result_str

  """

  def toIntervalList(self):

    internal_node_list = self.toInorderInternalNodeList()

    interval_list = [x.getElement().getKey() for x in internal_node_list]

    return interval_list

  def toIntervalStringList(self):

    interval_list = self.toIntervalList()

    interval_string_list = [x.toString() for x in interval_list]

    return interval_string_list

"""

# node can be non-existent, 
# in which case it would be None; 
# in this case, we return None

def getMax(node):

  if node == None:
  
    return None
    
  else:
  
    return node.getMax()

"""

# node can have no entry; 
# in this case, we return None

def getRightEndpointUsingNode(node):

  if node.getElement() == None:
  
    return None
    
  else:
  
    return node.getElement().getKey().getRightEndpoint()

t1 = BalancedIntervalTree.construct([(Interval(0, 1), 1), (Interval(1, 2), 1), (Interval(2, 3), 1)])

# print t1.toString()

# print t1.toInorderList()

"""

t1.intervalInsert(Interval(3, 4), 1)

# print t1.toString()

print t1.toInorderList()

t1.intervalDelete(Interval(1, 2), 1)

# print t1.toString()

print t1.toInorderList()

print t1.intervalSearch(Interval(2.5, 2.5))

t2 = BalancedIntervalTree.construct([(Interval(1, 11), 1), (Interval(2, 12), 1), (Interval(4, 14), 1), (Interval(3, 5), 1), (Interval(0, 10), 1)])

print t2.toString()

print t2.toInorderList()

"""

"""

from SweepLineTouchingSlab import *

from LeadingSweepLineTouchingSlab import *

from TrailingSweepLineTouchingSlab import *

from SweepLineTouchingSlabInterval import *

from ..SweepLine import *

t2 = BalancedIntervalTree.construct([(Interval(0, 1), 1), (Interval(1, 2), 1), (Interval(2, 3), 1)])

sweep_line = SweepLine()

sweep_line.setY(3)

slab1 = SweepLineTouchingSlab(3, 4, sweep_line)

slab_interval1 = SweepLineTouchingSlabInterval(slab1)

t2.intervalInsert(slab_interval1, 1)

slab2 = TrailingSweepLineTouchingSlab(4, sweep_line)

slab_interval2 = SweepLineTouchingSlabInterval(slab2)

t2.intervalInsert(slab_interval2, 1)

slab3 = LeadingSweepLineTouchingSlab(0, sweep_line)

slab_interval3 = SweepLineTouchingSlabInterval(slab3)

t2.intervalInsert(slab_interval3, 1)

print t2.toIntervalStringList()

"""


