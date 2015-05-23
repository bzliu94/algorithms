from BalancedIntervalTree import *

from BalancedImplicitMaxIntervalTreeNode import *

class BalancedImplicitMaxIntervalTree(BalancedIntervalTree):

  def __init__(self, key_transform = lambda x: x.getLeftEndpoint(), comparator = comp):

    BalancedIntervalTree.__init__(self, key_transform, comparator)

  # entries are (interval, value) pairs

  @staticmethod

  def construct(entries):

    tree = BalancedImplicitMaxIntervalTree()

    for entry in entries:

      key, value = entry

      tree.intervalInsert(key, value)

    return tree

  def _expandExternal(self, external_node, left_entry, right_entry):
  
    self._expandExternalHelper(external_node, left_entry, right_entry, BalancedImplicitMaxIntervalTreeNode)
    
  def addRoot(self, entry):

    self._addRootHelper(entry, BalancedImplicitMaxIntervalTreeNode)

  """

  # retrieve a scalar

  def _getCandidateValue(self, tagged_entry):

    entry, is_max_bearing = tagged_entry

    node = entry.getLocation()

    max_value = node.getMaxRightEndpoint().getValue()

    return max_value

  """

  """

  # set a max value based on a tagged mediating entry

  def _setMaxValue(self, node, tagged_source_entry):

    source_entry, is_max_bearing = tagged_source_entry

    responsible_interval = source_entry.getKey()

    source_node = source_entry.getLocation()

    max_value = source_node.getMaxRightEndpoint().getValue()

    print "setting a responsible interval"

    node.getMaxRightEndpoint().setResponsibleInterval(responsible_interval)

  """

"""

tree = BalancedImplicitMaxIntervalTree()

interval1 = Interval(1, 2)

interval2 = Interval(2, 3)

interval3 = Interval(3, 4)

interval4 = Interval(4, 5)

tree.intervalInsert(interval1, 1)

tree.intervalInsert(interval2, 2)

tree.intervalInsert(interval3, 2)

tree.intervalInsert(interval4, 2)

print tree.toString()

print tree.toInorderList()

entry1, node1 = tree.find(interval1)

print tree.toString()

print tree.toInorderList()

# print [x.getElement().toString() for x in tree.toInorderInternalNodeList()]

entry2, node2 = tree.find(interval2)

print tree.toString()

print tree.toInorderList()

print tree.toIntervalStringList()

print entry1.getKey().toString()

print node1.getMaxValue()

print entry2.getKey().toString()

print node2.getMaxValue()

print node1.getMaxRightEndpoint().getResponsibleInterval().toString()

"""


