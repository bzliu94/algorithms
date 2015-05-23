from SweepLineAngle import *

class CohortPinchlessAngle(SweeplineAngle):

  def __init__(self, arc, arc_interval, arc_tree, om_arc_list):

    SweeplineAngle.__init__(self, arc)

    self.arc_interval = arc_interval

    self.arc_tree = arc_tree

    self.om_arc_list = om_arc_list

  def _getArcInterval(self):

    return self.arc_interval

  def _getArcTree(self):

    return self.arc_tree

  def _getOrderMaintainedArcList(self):

    return self.om_arc_list

  # if two sweep-line angles correspond to arcs 
  #   that are both degenerate and that share 
  #   left endpoints, then they are comparable

  # if two sweep-line angles are not comparable, 
  #   we return None

  def compare(self, sweepline_angle):

    curr_arc = self._getArc()

    arc = sweepline_angle._getArc()

    om_arc_list = self._getOrderMaintainedArcList()

    curr_arc_interval = self._getArcInterval()

    arc_interval = self._getArcInterval()

    arc_tree = self._getArcTree()

    precision = arc_tree.getPrecision()

    curr_left_endpoint = curr_arc_interval.getTruncatedLeftEndpoint(precision)

    left_endpoint = arc_interval.getTruncatedLeftEndpoint(precision)

    curr_arc_is_size_zero = curr_arc.isSizeZero(arc_tree)

    arc_is_size_zero = arc.isSizeZero(arc_tree)

    # figure out if two sweep-line angles are comparable

    # if abs(curr_left_endpoint == left_endpoint) <= arc_tree.getPrecision():

    left_endpoints_match = (curr_left_endpoint <= (left_endpoint + arc_tree._getTolerance())) and \
      (curr_left_endpoint >= (left_endpoint - arc_tree._getTolerance()))

    both_arcs_are_size_zero = curr_arc_is_size_zero == True and arc_is_size_zero == True

    if left_endpoints_match == True and both_arcs_are_size_zero == True:

      # two given sweep-line angles are comparable

      # determine relative positions of associated list nodes

      list_node1 = arc_tree._getListNodeForArc(self._getArc())

      list_node2 = arc_tree._getListNodeForArc(sweepline_angle._getArc())

      # return list_node1.compare(list_node2)

      result = om_arc_list.order(list_node1, list_node2)

      return result

    else:

      # two given sweep-line angles are not comparable

      return None

