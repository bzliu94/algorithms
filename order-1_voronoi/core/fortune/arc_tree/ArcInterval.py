# left endpoint can be minus infinity

# right endpoint can be positive infinity

# from OrderedInterval import *

from Interval import *

from ..Breakpoint import *

"""

# avoid circular import

# from ArcTree import *

# import ArcTree.ArcTree as ArcTree

"""

from ...Util import *

# from CohortPinchlessAngle import *

from ..events.CircleEvent import *

# class ArcInterval(OrderedInterval):

class ArcInterval(Interval):

  # node is an ordered interval tree node

  def __init__(self, arc, arc_tree, sweep_line):
  
    # OrderedInterval.__init__(self, None, None)

    Interval.__init__(self, None, None)
    
    self.sweep_line = sweep_line
    
    self.arc = arc
    
    self.arc_tree = arc_tree

  def _getArcTree(self):
  
    return self.arc_tree
    
  def _getSweepLine(self):
  
    return self.sweep_line
    
  def _getArc(self):
  
    return self.arc

  """
    
  def _setNode(self, node):
  
    self.node = node

  """

  def _hasLeftNeighborArcInterval(self):

    left_neighbor_arc_interval = self._getLeftNeighborArcInterval()

    result = left_neighbor_arc_interval != None

    # print "result:", result

    return result

  # assume that if we have a right neighbor arc, we also have a right neighbor arc interval

  def _hasRightNeighborArcInterval(self):

    right_neighbor_arc_interval = self._getRightNeighborArcInterval()

    result = right_neighbor_arc_interval != None

    # print "result:", result

    return result

  # if left neighbor arc interval does not exist, 
  #   we return None

  def _getLeftNeighborArcInterval(self):

    arc_tree = self._getArcTree()

    arc = self._getArc()

    if arc_tree.hasArcLeftNeighbor(arc) == False:

      return None

    predecessor_arc = arc_tree.getArcLeftNeighbor(arc)

    predecessor_arc_interval = arc_tree._getArcIntervalForArc(predecessor_arc)

    return predecessor_arc_interval

    """

    arc_tree = self._getArcTree()

    om_arc_list = arc_tree._getOrderMaintainedArcList()

    arc = self._getArc()

    list_node = arc_tree._getListNodeForArc(arc)

    if om_arc_list.hasPredecessor(list_node) == False:

      return None

    else:

      predecessor_list_node = list_node.prev

      predecessor_arc = predecessor_list_node.getElement()

      predecessor_arc_interval = arc_tree._getArcIntervalForArc(predecessor_arc)

      return predecessor_arc_interval

    """

  # if right neighbor arc interval does not exist, 
  #   we return None

  def _getRightNeighborArcInterval(self):

    arc_tree = self._getArcTree()

    arc = self._getArc()

    if arc_tree.hasArcRightNeighbor(arc) == False:

      return None

    successor_arc = arc_tree.getArcRightNeighbor(arc)

    successor_arc_interval = arc_tree._getArcIntervalForArc(successor_arc)

    return successor_arc_interval

    """
  
    arc_tree = self._getArcTree()

    om_arc_list = arc_tree._getOrderMaintainedArcList()

    arc = self._getArc()

    list_node = arc_tree._getListNodeForArc(arc)

    if om_arc_list.hasSuccessor(list_node) == False:

      return None

    else:

      successor_list_node = list_node.next

      successor_arc = successor_list_node.getElement()

      successor_arc_interval = arc_tree._getArcIntervalForArc(successor_arc)

      return successor_arc_interval

    """

  # find left extent from perspective of current arc

  # may return floating-point version of minus infinity

  def getLeftEndpoint(self):

    # print "getting left endpoint"
  
    sweep_line = self._getSweepLine()
    
    l_y = sweep_line.getY()

    curr_arc_interval = self

    curr_arc = curr_arc_interval._getArc()

    arc_tree = self._getArcTree()

    # current arc extends left-ward to minus infinity

    if self._hasLeftNeighborArcInterval() == False and curr_arc.isDegenerate(l_y) == False:

      return float("-inf")
    
    left_arc_interval = self._getLeftNeighborArcInterval()

    arc_has_left_neighbor = arc_tree.hasArcLeftNeighbor(curr_arc)

    # current arc has no left neighbor and is degenerate

    have_no_left_neighbor_and_arc_is_degenerate = (self._hasLeftNeighborArcInterval() == False) and (curr_arc.isDegenerate(l_y) == True)

    # current arc has a left neighbor that is degenerate 
    #   and the current arc is degenerate

    have_left_degenerate_neighbor_and_arc_is_degenerate = (arc_has_left_neighbor == True and curr_arc.isDegenerate(l_y) == True) and (arc_tree.getArcLeftNeighbor(curr_arc).isDegenerate(l_y) == True)

    if (have_no_left_neighbor_and_arc_is_degenerate == True) or (have_left_degenerate_neighbor_and_arc_is_degenerate == True):

      # left neighbor arc does not intersect current arc

      focus = curr_arc.getFocus()

      x_location = focus[0]

      return x_location

    else:

      # have breakpoint to speak of

      left_arc = arc_tree.getArcLeftNeighbor(curr_arc)

      # print have_no_left_neighbor_and_arc_is_degenerate, have_left_degenerate_neighbor_and_arc_is_degenerate, curr_arc, left_arc

      breakpoint = Breakpoint(left_arc, curr_arc)

      x_location = breakpoint.getXComponent(l_y)

      # print "x location", x_location

      return x_location

  # find right extent from perspective of current arc

  # may return floating-point version of positive infinity

  def getRightEndpoint(self):

    # print "getting right endpoint"
  
    sweep_line = self._getSweepLine()
    
    l_y = sweep_line.getY()

    curr_arc_interval = self

    curr_arc = curr_arc_interval._getArc()

    arc_tree = self._getArcTree()

    # current arc extends right-ward to infinity

    if self._hasRightNeighborArcInterval() == False and curr_arc.isDegenerate(l_y) == False:
    
      return float("inf")
    
    right_arc_interval = self._getRightNeighborArcInterval()

    """
    
    curr_arc_node = curr_arc_interval._getNode()
    
    right_arc_node = right_arc_interval._getNode()

    curr_arc = curr_arc_node._getArc()
    
    right_arc = right_arc_node._getArc()

    """

    # right_arc = right_arc_interval._getArc()

    arc_has_right_neighbor = arc_tree.hasArcRightNeighbor(curr_arc)

    # print curr_arc.getFocus()

    # print right_arc.getFocus()

    # current arc has no right neighbor and is degenerate

    have_no_right_neighbor_and_arc_is_degenerate = (self._hasRightNeighborArcInterval() == False) and (curr_arc.isDegenerate(l_y) == True)

    # current arc has a right neighbor that is degenerate 
    #   and the current arc is degenerate

    have_right_degenerate_neighbor_and_arc_is_degenerate = (arc_has_right_neighbor == True and curr_arc.isDegenerate(l_y) == True) and (arc_tree.getArcRightNeighbor(curr_arc).isDegenerate(l_y) == True)

    if (have_no_right_neighbor_and_arc_is_degenerate == True) or (have_right_degenerate_neighbor_and_arc_is_degenerate == True):

      # right neighbor arc does not intersect current arc

      focus = curr_arc.getFocus()

      x_location = focus[0]

      return x_location

    else:

      # have breakpoint to speak of

      right_arc = arc_tree.getArcRightNeighbor(curr_arc)

      # print have_no_right_neighbor_and_arc_is_degenerate, have_right_degenerate_neighbor_and_arc_is_degenerate, curr_arc, right_arc

      breakpoint = Breakpoint(curr_arc, right_arc)
    
      x_location = breakpoint.getXComponent(l_y)

      # print "x location", x_location

      return x_location

  """

  # return a value that uniquely identifies 
  #   this ordered interval and is by default hashable

  def getOrderDistinguisher(self):

    return (self.arc).getFocus()

  """

  def toString(self):
  
    # left_endpoint = self.getLeftEndpoint()
        
    # right_endpoint = self.getRightEndpoint()

    arc_tree = self._getArcTree()

    left_endpoint = self.getTruncatedLeftEndpoint(arc_tree.getPrecision())

    right_endpoint = self.getTruncatedRightEndpoint(arc_tree.getPrecision())

    if not (left_endpoint <= right_endpoint):

      """

      print "focus list:", arc_tree.toFocusList()

      print "order-maintenance focus list:", [x.getFocus() for x in arc_tree._getOrderMaintainedArcList().toElementList()]

      print left_endpoint, right_endpoint, self._getSweepLine().getY()

      # arc_list = arc_tree._getOrderMaintainedArcList().toElementList()

      # arc_focus_list = [x.getFocus() for x in arc_list]

      # print arc_focus_list

      print self._getLeftNeighborArcInterval()._getArc().getFocus()

      print self._getArc().getFocus()

      print self._getRightNeighborArcInterval()._getArc().getFocus()

      arc1 = arc_tree.getArcLeftNeighbor(self._getArc())

      arc2 = self._getArc()

      arc3 = arc_tree.getArcRightNeighbor(self._getArc())

      sweep_line = arc_tree.getSweepLine()

      l_y = sweep_line.getY()

      """

      """

      location = CircleEvent.getLargestEmptyCircleLowestExtent(l_y, arc1, arc2, arc3)

      x, y = location

      truncated_x = arc_tree._truncate(x, arc_tree.getPrecision())

      truncated_y = arc_tree._truncate(y, arc_tree.getPrecision())

      location_with_truncated_components = (truncated_x, truncated_y)

      print location_with_truncated_components

      """

      raise Exception("left endpoint value not less than or equal to right endpoint value")

    result_str = "[" + str(left_endpoint) + ", " + str(right_endpoint) + "]"
    
    return result_str

  """

  def getSweeplineAngle(self):

    arc_tree = self._getArcTree()

    om_arc_list = arc_tree._getOrderMaintainedArcList()

    arc = self._getArc()

    arc_interval = arc_tree._getArcIntervalForArc(arc)

    return CohortPinchlessAngle(arc, arc_interval, arc_tree, om_arc_list)

  """

  def getTruncatedLeftEndpoint(self, precision):
  
    # return ArcTree._truncate(self.getLeftEndpoint(), precision)

    left_endpoint = self.getLeftEndpoint()

    if left_endpoint == float("-inf"):

      return left_endpoint

    else:

      # return truncate(left_endpoint, precision)

      return round_with_precision(left_endpoint, precision)
    
  def getTruncatedRightEndpoint(self, precision):
  
    # return ArcTree._truncate(self.getRightEndpoint(), precision)

    right_endpoint = self.getRightEndpoint()

    if right_endpoint == float("inf"):

      return right_endpoint

    else:

      # return truncate(self.getRightEndpoint(), precision)

      return round_with_precision(self.getRightEndpoint(), precision)

  def isSizeZero(self):

    arc_tree = self._getArcTree()

    left_endpoint = self.getTruncatedLeftEndpoint(arc_tree.getPrecision())

    right_endpoint = self.getTruncatedRightEndpoint(arc_tree.getPrecision())

    # print left_endpoint, right_endpoint

    tolerance = arc_tree._getTolerance()

    endpoints_match = (left_endpoint <= (right_endpoint + tolerance)) and \
      (left_endpoint >= (right_endpoint - tolerance))

    return endpoints_match

  """

  # care about x values

  # note that for a given positive change 
  #   in the quantity (focus y - sweep-line y), 
  #   change in x tends to be more

  def isDegenerate(self, l_y):

    # measuring axis-aligned quantities

    left_endpoint = self.getTruncatedLeftEndpoint(arc_tree.getPrecision())

    right_endpoint = self.getTruncatedRightEndpoint(arc_tree.getPrecision())

    return left_endpoint == right_endpoint

  """


