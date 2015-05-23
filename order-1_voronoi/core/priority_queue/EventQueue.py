from AdaptablePriorityQueue import *

# keys are internally (priority, is_for_split_residue_arc) pairs

# assume unique values for our key-value pairs

class EventQueue(AdaptablePriorityQueue):

  def __init__(self):

    AdaptablePriorityQueue.__init__(self)

    self.value_to_entry_dict = {}

  def _comparator(x, y):

    priority1, is_for_split_residue_arc1 = x

    priority2, is_for_split_residue_arc2 = y

    if priority1 > priority2:

      return 1

    elif priority1 < priority2:

      return -1

    elif priority1 == priority2:

      if is_for_split_residue_arc1 == False and is_for_split_residue_arc2 == True:

        return 1

      elif is_for_split_residue_arc1 == True and is_for_split_residue_arc2 == False:

        return -1

      elif is_for_split_residue_arc1 == is_for_split_residue_arc2:

        return 0

  def insert(self, k, x):

    # print "event queue key:", k

    """

    if type(k) != type((0, 0)):

      raise Exception("key is not a two-tuple")

    if x.isCircleEvent() == True:

      print "encountered a circle event with focus:", x.getArc().getFocus()

    """

    entry = AdaptablePriorityQueue.insert(self, k, x)

    (self.value_to_entry_dict)[x] = entry

    return entry

  def _removeHelper(self, v):

    entry = AdaptablePriorityQueue._removeHelper(self, v)

    value = entry.getValue()

    (self.value_to_entry_dict).pop(value)

    """

    if not (entry.getLocation() == v):

      raise Exception("locations do not match")

    """

    return entry

  # takes O(log(n)) time

  def removeEvent(self, event):

    """

    if event.isCircleEvent() == True:

      print "aiming to remove a circle event with focus:", event.getArc().getFocus()

    """

    entry = (self.value_to_entry_dict)[event]

    node = entry.getLocation()

    nodes = (self.T)[1 : ]

    # print nodes

    candidate_nodes = [x for x in nodes if x.getElement().getValue() == event]

    matching_node = candidate_nodes[0]

    # print matching_node.getElement().getValue()

    if not (node == matching_node):

      raise Exception("location-aware entry location mis-set")

    result_entry = self._removeHelper(node)

    # print self.toString()

    """

    print result_entry.getValue(), event

    if not (result_entry.getValue() == event):

      raise Exception("values do not match")

    """

    return result_entry

  def removeMin(self):

    return LocationAwareHeap.removeMin(self)

"""

event_queue = EventQueue()

"""

# possible issue relating to getting min. value if tree is empty

