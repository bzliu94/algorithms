"""

class ArcTreeNode:

  def __init__(self):

    arc_farthest_to_left_with_coinciding_circle_event = None

    offset_from_arc_farthest_to_left_with_coinciding_circle_event = 0

  def _expandExternal(self, external_node, left_entry, right_entry):
  
    self._expandExternalHelper(external_node, left_entry, right_entry, ArcTreeNode)
    
  def addRoot(self, entry):

    self._addRootHelper(entry, ArcTreeNode)

"""

from BalancedShiftingEndpointIntervalTreeNode import *

class ArcTreeNode(BalancedShiftingEndpointIntervalTreeNode):

  def __init__(self):

    self.sweep_line = sweep_line

  def _getSweepLine(self):

    return self.sweep_line

  def getMax(self, retrieve_fn):

    max_source_node = self._getMaxSourceNode()

    sweep_line = self._getSweepLine()

    l_y = sweep_line.getY()

    entry = max_source_node.getElement()

    interval = entry.getKey()

