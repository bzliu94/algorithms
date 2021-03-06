# effective key is a three-tuple

from BalancedImplicitMaxIntervalTree import *

from ..SweepLine import *

from ...list.order_maintenance.OrderMaintainedDoublyLinkedList import *

from Arc import *

from ArcInterval import *

# import ArcInterval.ArcInterval as ArcInterval

from ArcPayload import *

from ...Util import *

class ArcTree(BalancedImplicitMaxIntervalTree):

  def __init__(self, precision, sweep_line):

    # key_transform = lambda x: (x.getLeftEndpoint(), x.getSweeplineAngle())

    # comparator = ArcTree._comparator
    
    key_transform = self._key_transform

    comparator = self._comparator

    BalancedImplicitMaxIntervalTree.__init__(self, key_transform, comparator)

    self.sweep_line = sweep_line

    # have order-maintained arc list as companion structure

    self.om_arc_list = OrderMaintainedDoublyLinkedList()
    
    self.arc_to_arc_interval_dict = {}
    
    self.arc_to_list_node_dict = {}

    self.precision = precision
    
    # self.precision = 3
    
    # attempt to avoid 
    # unexpected behavior 
    # that may result from use 
    # of floating-point values

    # note that tolerance may affect 
    # behavior relating to interval endpoints 
    # that are minus or positive infinity
    
    self.tolerance = 0.0001
    
  def _getOrderMaintainedArcList(self):
  
    return self.om_arc_list
  
  def _key_transform(self, arc_interval):
  
    # temporarily use exact arithmetic 
    # so that we may arrive 
    # at a truncated value 
    # and for purpose of comparison

    # print arc_interval.toString()

    arc = arc_interval._getArc()

    list_node = self._getListNodeForArc(arc)

    # return list_node1.compare(list_node2)

    key = list_node

    return key

    """
  
    left_endpoint = arc_interval.getTruncatedLeftEndpoint(self.getPrecision())

    # take into account fact that initial insertions of arcs 
    #   lead to degenerate parabolas that then tie 
    #   due to having comparisons partially on basis of left endpoints

    is_size_zero = arc_interval._getArc().isSizeZero(self)

    # print "is size zero:", is_size_zero
    
    sweepline_angle = arc_interval.getSweeplineAngle()
    
    key = (left_endpoint, is_size_zero, sweepline_angle)

    # print key
    
    return key

    """

  def _comparator(self, x, y):

    list_node1 = x

    list_node2 = y

    # print result

    result = self._getOrderMaintainedArcList().order(list_node1, list_node2)

    """

    arc1 = list_node1.getNode().getElement()

    arc2 = list_node2.getNode().getElement()

    focus1 = arc1.getFocus()

    focus2 = arc2.getFocus()

    if focus1 == focus2 and result != 0:

      raise Exception()

    """

    # print "comparison:", result

    return result

    """
  
    left_endpoint1, is_size_zero1, sweepline_angle1 = x
    
    left_endpoint2, is_size_zero2, sweepline_angle2 = y

    # note that an interesting situation arises 
    #   when attempting to subtract infinity from infinity
    
    # if (left_endpoint1 - self._getTolerance()) < left_endpoint2:

    # print left_endpoint1, left_endpoint2

    if left_endpoint1 < (left_endpoint2 - self._getTolerance()):

      # print "case 1"

      # print left_endpoint1 - self._getTolerance(), left_endpoint2

      # print left_endpoint1, self._getTolerance(), left_endpoint2
    
      return -1
    
    # elif (left_endpoint1 + self._getTolerance()) > left_endpoint2:

    elif left_endpoint1 > (left_endpoint2 + self._getTolerance()):

      # print "case 2"

      # print "case two with:", left_endpoint1, left_endpoint2
    
      return 1
    
    # elif abs(left_endpoint2 - left_endpoint1) <= self._getTolerance():

    elif (left_endpoint1 <= (left_endpoint2 + self._getTolerance())) and \
      (left_endpoint1 >= (left_endpoint2 - self._getTolerance())):

      # print "case 3"

      if self._degenerate_arc_comp(is_size_zero1, is_size_zero2) == -1:

        return -1

      elif self._degenerate_arc_comp(is_size_zero1, is_size_zero2) == 1:

        return 1

      elif self._degenerate_arc_comp(is_size_zero1, is_size_zero2) == 0:

        # print "using third item in tuple that serves as effective key"

        result = sweepline_angle1.compare(sweepline_angle2)

        if result == None:

          return 0

        else:

          return result

    """

  def _degenerate_arc_comp(self, is_size_zero1, is_size_zero2):

    if is_size_zero1 == True and is_size_zero2 == True:

      # return "tie"

      # print "case 2a"

      return 0

    elif is_size_zero1 == False and is_size_zero2 == False:

      # return "tie"

      # print "case 2b"

      return 0

    elif is_size_zero1 == False and is_size_zero2 == True:

      # prefer having size zero arc to left

      # print "case 2c"

      return 1

    elif is_size_zero1 == True and is_size_zero2 == False:

      # prefer having size zero arc to left

      # print "case 2d"

      return -1

  def _getTolerance(self):
  
    return self.tolerance

  def _addArcToArcIntervalRelationship(self, arc, arc_interval):
  
    (self.arc_to_arc_interval_dict)[arc] = arc_interval
    
  def _removeArcToArcIntervalRelationship(self, arc):
  
    (self.arc_to_arc_interval_dict).pop(arc)
    
  def _getArcIntervalForArc(self, arc):

    return (self.arc_to_arc_interval_dict)[arc]
    
  def _addArcToListNodeRelationship(self, arc, list_node):
  
    (self.arc_to_list_node_dict)[arc] = list_node
    
  def _removeArcToListNodeRelationship(self, arc):
  
    (self.arc_to_list_node_dict).pop(arc)
    
  def _getListNodeForArc(self, arc):
  
    # print self.arc_to_list_node_dict
    
    # print arc.getFocus()
  
    return (self.arc_to_list_node_dict)[arc]

  # entries are (interval, value) pairs

  @staticmethod

  def construct(arcs):

    tree = ArcTree()

    for entry in entries:

      key, value = entry

      tree.insertArc(key, value)

    return tree

  def getSweepLine(self):

    return self.sweep_line

  """

  # assume that arc tree is currently empty 
  #   and that arc list is ordered

  def insertLeadingArcs(self, arc_list):

    pass

  """

  # insert a leading arc, which is an arc 
  #   that we may insert without splitting 
  #   and insert even if the arc tree 
  #   is not empty

  def _insertLeadingArc(self, arc):

    # set neighbors correctly for guide structure# 

    # insert interval and prepare auxiliary structures

    # remember to prepare payload

    focus = arc.getFocus()

    x = focus[0]

    arc_pair = self.matchlessQuery(x)

    left_arc, right_arc = arc_pair

    has_left_arc = left_arc != None

    has_right_arc = right_arc != None

    if has_left_arc == False and has_right_arc == False:

      self._addArcAsFirstHelper(arc)

    elif has_left_arc == True and has_right_arc == False:

      self._addArcAfterHelper(arc, left_arc)

    elif has_left_arc == False and has_right_arc == True:

      self._addArcAsFirstHelper(arc)

    elif has_left_arc == True and has_right_arc == True:

      self._addArcAfterHelper(arc, left_arc)

    arc_interval = self._getArcIntervalForArc(arc)

    BalancedIntervalTree.intervalInsert(self, arc_interval, ArcPayload())

  # this method is for inserting an arc 
  #   with focus that has y-value that matches 
  #   that of current sweep-line location

  # assume that arc initially has no payload

  # may have to deal with a "leading arc"

  # def insertArc(self, arc):

  def insertArc(self, arc, sweep_line_initial_y_value):

    """

    print self.toString()

    print "interval string list:", self.toIntervalStringList()

    print "focus list:", self.toFocusList()

    """

    # print self.toIntervalStringList()

    # print self.toFocusList()
  
    # print "inserting an arc:", arc.getFocus()
  
    focus = arc.getFocus()

    focus_y = focus[1]

    if focus_y == sweep_line_initial_y_value:

      # arc is a leading arc

      self._insertLeadingArc(arc)

    elif self.hasNoArcs() == True:

      # print "insert arc case #1"
    
      # update auxiliary/companion structures
      
      self._addArcAsFirstHelper(arc)
      
      # update tree
      
      arc_interval = self._getArcIntervalForArc(arc)

      BalancedIntervalTree.intervalInsert(self, arc_interval, ArcPayload())

      # print "sole interval:", arc_interval.toString()
      
    else:

      # print "insert arc case #2"
    
      x_value = (arc.getFocus())[0]
      
      result = self.query(x_value)

      arc_above, arc_above_payload = result
      
      arc_above_focus = arc_above.getFocus()

      """

      print "arc tree - splitting arc:", arc_above.getFocus()

      print "arc tree - interval strings:", self.toIntervalStringList()

      print "arc tree - focuses:", self.toFocusList()

      print "arc tree - x value:", x_value

      """

      """

      # if we are at one of the endpoints of the arc above us, 
      #   we insert at said endpoint without splitting

      """

      """

      # not splitting

      """

      arc_above_arc_interval = self._getArcIntervalForArc(arc_above)

      left_endpoint = arc_above_arc_interval.getLeftEndpoint()

      right_endpoint = arc_above_arc_interval.getRightEndpoint()

      """

      if CircleEvent.axisAlignedComp(x_value, left_endpoint) == 0:

        # not splitting

        # insert to left

        self._addArcBeforeHelper(arc, arc_above)

        arc_interval = self._getArcIntervalForArc(arc)

        BalancedIntervalTree.intervalInsert(self, arc_interval, ArcPayload())

      elif CircleEvent.axisAlignedComp(x_value, right_endpoint) == 0:

        # not splitting

        # insert to right

        self._addArcAfterHelper(arc, arc_above)

        arc_interval = self._getArcIntervalForArc(arc)

        BalancedIntervalTree.intervalInsert(self, arc_interval, ArcPayload())

      else:

      """

      sweep_line = self.getSweepLine()

      l_y = sweep_line.getY()

      # splitting

      # print arc_above_focus

      left_arc_is_size_zero = False

      right_arc_is_size_zero = False

      if CircleEvent.axisAlignedComp(x_value, left_endpoint) == 0:

        left_arc_is_size_zero = True

      elif CircleEvent.axisAlignedComp(x_value, right_endpoint) == 0:

        right_arc_is_size_zero = True
      
      left_arc = Arc(arc_above_focus, left_arc_is_size_zero)

      right_arc = Arc(arc_above_focus, right_arc_is_size_zero)

      # arc_above is arc to remove
      
      # left_arc, arc, right_arc are replacement arcs
      
      # update auxiliary/companion structures

      """
      
      self._addArcAfterHelper(arc_above, left_arc)
      
      self._addArcAfterHelper(left_arc, arc)
      
      self._addArcAfterHelper(arc, right_arc)

      """

      """
      
      # update tree

      self.removeArc(arc_above)

      """
      
      """
      
      # update auxiliary/companion structures
      
      self._removeArcHelper(arc_above)
      
      """

      """
      
      # update tree

      # introduce center, remove original, introduce left and right

      # print "adding center arc"

      anchor_arc_focus_x_value = arc_above.getTruncatedLeftEndpoint(self.getPrecision())

      anchor_arc_focus_y_value = self.getSweepLine().getY()

      focus = (anchor_arc_focus_x_value, anchor_arc_focus_y_value)

      anchor_arc = Arc(focus)

      """

      arc_above_is_leftmost_arc = None

      anchor_arc = None

      # find an anchor

      if self.hasArcLeftNeighbor(arc_above) == True:

        arc_above_is_leftmost_arc = False

        anchor_arc = self.getArcLeftNeighbor(arc_above)

      else:

        arc_above_is_leftmost_arc = True

      # print arc_above_is_leftmost_arc

      self.removeArc(arc_above)

      if arc_above_is_leftmost_arc == False:

        # print "insert split case 1"

        # print "anchor arc focus:", anchor_arc.getFocus()

        """

        self._addArcAfterHelper(arc, anchor_arc)

        self._addArcBeforeHelper(left_arc, arc)

        self._addArcAfterHelper(right_arc, arc)

        """

        self._addArcAfterHelper(left_arc, anchor_arc)

        self._addArcAfterHelper(arc, left_arc)

        self._addArcAfterHelper(right_arc, arc)

        # print self._getOverlyingTree().toElementList()

        node_inorder_list = self._getOrderMaintainedArcList().overlying_tree.toInorderInternalNodeList()

        # arc_focus_list = [x.getElement().getValue().getNode().getElement().getFocus() for x in node_inorder_list]

        node_label_value_list = [(PathLabel.toBaseThreeString(x.getPathLabel().getNumericPath()), x.getPathLabel().getPathLength())  for x in node_inorder_list]

        # print "arc focus list:", arc_focus_list

        # print "label list:", node_label_value_list

      elif arc_above_is_leftmost_arc == True:

        # print "insert split case 2"

        self._addArcAsFirstHelper(arc)

        self._addArcBeforeHelper(left_arc, arc)

        self._addArcAfterHelper(right_arc, arc)

        # print "order-maintenance focus list:", [x.getFocus() for x in self._getOrderMaintainedArcList().toElementList()]

      """

      # above_arc_interval = self._getArcIntervalForArc(arc_above)

      BalancedIntervalTree.intervalDelete(self, above_arc_interval, None)

      self._addArcAfterHelper(left_arc, arc_above)

      self._addArcAfterHelper(arc, left_arc)

      self._addArcAfterHelper(right_arc, arc)

      self._removeArcHelper(arc_above)

      # self.removeArc(arc_above)

      """

      """

      # self._addArcBeforeHelper(anchor_arc, arc_above)

      anchor_arc_interval = self._getArcIntervalForArc(anchor_arc)

      BalancedIntervalTree.intervalInsert(self, arc_interval, ArcPayload())

      """

      # print "adding left arc:", left_arc.getFocus()

      left_arc_interval = self._getArcIntervalForArc(left_arc)
      
      BalancedIntervalTree.intervalInsert(self, left_arc_interval, ArcPayload())

      # print "intervals #1:", self.toIntervalStringList()

      # self._addArcAfterHelper(left_arc, anchor_arc)

      # print "order comparison:", self._getOrderMaintainedArcList().order(self._getListNodeForArc(arc), self._getListNodeForArc(left_arc))

      # print self._getListNodeForArc(arc), self._getListNodeForArc(left_arc)

      # print "adding middle arc:", arc.getFocus()

      arc_interval = self._getArcIntervalForArc(arc)
      
      BalancedIntervalTree.intervalInsert(self, arc_interval, ArcPayload())

      # print "intervals #2:", self.toIntervalStringList()

      # print "removing original arc"

      # self.removeArc(arc_above)

      # print "adding right arc:", right_arc.getFocus()

      right_arc_interval = self._getArcIntervalForArc(right_arc)
      
      BalancedIntervalTree.intervalInsert(self, right_arc_interval, ArcPayload())

      # print "intervals #3:", self.toIntervalStringList()

      # print "interval:", arc_interval.toString()

  def removeArc(self, arc):
  
    # update tree

    # print "removing an arc:", arc.getFocus()

    keys = self.arc_to_arc_interval_dict.values()

    """

    interval_strings = [x.toString() for x in keys]

    arc_focuses = [x._getArc().getFocus() for x in keys]

    print interval_strings

    print arc_focuses

    """
    
    arc_interval = self._getArcIntervalForArc(arc)
    
    # BalancedIntervalTree.remove(self, IntervalEntry(arc_interval, None))

    """

    print "interval corresponding to arc to be removed:", arc_interval.toString()

    print "focus:", arc.getFocus()

    """

    # print arc_interval._getArc().getFocus()

    # print self.toIntervalStringList()

    # print self.toFocusList()

    # print "order-maintenance focus list:", [x.getFocus() for x in self._getOrderMaintainedArcList().toElementList()]

    BalancedIntervalTree.intervalDelete(self, arc_interval, None)
    
    # update auxiliary/companion structures
    
    self._removeArcHelper(arc)

    # print "interval:", arc_interval.toString()

  # assume that no interval corresponding to an arc 
  #   currently covers given x value

  # could have zero, one, or two neighbors

  # return a (left neighbor arc, right neighbor arc) pair

  # either arc returned could be None

  def matchlessQuery(self, x_value):

    interval = Interval(x_value, x_value)

    # result = self._treeSearch(interval, self.getRoot())

    # expect that our result node is an external node

    # key_transform = lambda x: x.getLeftEndpoint()

    key_transform = lambda x: x

    comparator = lambda x, y: comp(x.getLeftEndpoint(), y.getLeftEndpoint())

    result_node = self._treeSearchWithTransformedKey(interval, self.getRoot(), key_transform, comparator)

    entry = result_node.getElement()

    # result = self.intervalSearch(interval)

    # entry, node = result

    node = result_node

    # entry = node.getElement()

    # found a leaf

    has_predecessor_internal_node = self.hasPredecessorInternalNode(node)

    has_successor_internal_node = self.hasSuccessorInternalNode(node)

    predecessor_arc_interval = None

    successor_arc_interval = None

    # print self.toString()

    """

    if node.getParent() != None:

      print node.getParent().getElement().getKey().toString()

      print node.getPrev()

      print node.getNext()

      print has_predecessor_internal_node

      print has_successor_internal_node

    """

    if has_predecessor_internal_node == True:

      predecessor_internal_node = self.getPredecessorInternalNode(node)

      predecessor_arc_interval = predecessor_internal_node.getElement().getKey()

    if has_successor_internal_node == True:

      successor_internal_node = self.getSuccessorInternalNode(node)

      successor_arc_interval = successor_internal_node.getElement().getKey()

    predecessor_arc = predecessor_arc_interval._getArc() if predecessor_arc_interval != None else None

    successor_arc = successor_arc_interval._getArc() if successor_arc_interval != None else None

    arc_pair = (predecessor_arc, successor_arc)

    # print arc_pair

    return arc_pair

  # retrieve arc above a location on sweep-line 
  #   given an x value and location of sweep-line

  # returns an (arc, payload) tuple

  # raises an exception if there is nothing above the query location

  def query(self, x_value):

    # print x_value

    interval = Interval(x_value, x_value)

    result = BalancedIntervalTree.intervalSearch(self, interval)

    if result == None:

      raise Exception("no arc above query location")

    result_interval, result_node = result

    entry = result_node.getElement()

    arc_interval = entry.getKey()

    arc = arc_interval._getArc()

    payload = entry.getValue()

    """

    print "x_value, arc_interval:", x_value, arc_interval.toString()

    tree = self

    print "tree:", tree.toString()

    print "interval:", arc_interval.toString()

    internal_node_list = tree.toInorderInternalNodeList()

    interval_list = [x.getElement().getKey() for x in internal_node_list]

    interval_string_list = [x.toString() for x in interval_list]

    focus_list = [x.getElement().getKey()._getArc().getFocus() for x in internal_node_list]

    print "interval string list:", interval_string_list

    print "focus list:", focus_list

    """

    return (arc, payload)

  def hasArcLeftNeighbor(self, arc):

    left_neighbor = self.getArcLeftNeighbor(arc)

    has_left_neighbor = left_neighbor != None
    
    return has_left_neighbor

  def hasArcRightNeighbor(self, arc):
  
    right_neighbor = self.getArcRightNeighbor(arc)

    has_right_neighbor = right_neighbor != None
    
    return has_right_neighbor
    
  # may return None

  # we assume that if a particular arc neighbor exists, 
  #   a corresponding arc interval also exists

  def getArcLeftNeighbor(self, arc):

    arc_tree = self

    om_arc_list = arc_tree._getOrderMaintainedArcList()

    list_node = arc_tree._getListNodeForArc(arc)

    if om_arc_list.hasPredecessor(list_node) == False:

      return None

    else:

      predecessor_list_node = list_node.prev

      predecessor_arc = predecessor_list_node.getElement()

      return predecessor_arc

    """

    left_neighbor = self.getPredecessorInternalNode()
    
    return left_neighbor

    """

  # may return None

  # we assume that if a particular arc neighbor exists, 
  #   a corresponding arc interval also exists

  def getArcRightNeighbor(self, arc):

    arc_tree = self

    om_arc_list = arc_tree._getOrderMaintainedArcList()

    list_node = arc_tree._getListNodeForArc(arc)

    if om_arc_list.hasSuccessor(list_node) == False:

      return None

    else:

      successor_list_node = list_node.next

      successor_arc = successor_list_node.getElement()

      return successor_arc

    """

    right_neighbor = self.getSuccessorInternalNode()
    
    return right_neighbor

    """

  def getArcPayload(self, arc):

    arc_interval = self._getArcIntervalForArc(arc)

    """

    sweep_line = self.getSweepLine()

    # print "sweep-line y-value:", sweep_line.getY()

    tree = self

    # print "tree:", tree.toString()

    # print "interval:", arc_interval.toString()

    internal_node_list = tree.toInorderInternalNodeList()

    interval_list = [x.getElement().getKey() for x in internal_node_list]

    interval_string_list = [x.toString() for x in interval_list]

    focus_list = [x.getElement().getKey()._getArc().getFocus() for x in internal_node_list]

    # print "interval string list:", interval_string_list

    # print "focus list:", focus_list

    om_arc_list_element_list = self._getOrderMaintainedArcList().toElementList()

    om_arc_list_arc_list = om_arc_list_element_list

    om_arc_list_arc_focus_list = [x.getFocus() for x in om_arc_list_arc_list]

    # print om_arc_list_arc_focus_list

    """

    result = self.find(arc_interval)

    """

    if result != None:

      raise Exception("found a match")

    """
    
    entry, node = result

    # print "found entry:", entry.toString()
    
    value = entry.getValue()
    
    return value

  # remove arc
  
  # modify only auxiliary/companion structures
  
  # assume that arc1 does not have certain associated objects (i.e. list node, arc interval)
  
  # assume that arc2 does have certain associated objects (i.e. list node, arc interval)

  def _removeArcHelper(self, arc):
  
    list_node = self._getListNodeForArc(arc)
    
    arc_interval = self._getArcIntervalForArc(arc)
    
    # update companion structure
    
    (self.om_arc_list).remove(list_node)
    
    # update auxiliary structures
    
    self._removeArcToArcIntervalRelationship(arc)
    
    self._removeArcToListNodeRelationship(arc)
    
  # add arc1 after arc2
  
  # modify only auxiliary/companion structures
  
  # assume that arc1 does not have certain associated objects (i.e. list node, arc interval)
  
  # assume that arc2 does have certain associated objects (i.e. list node, arc interval)
    
  def _addArcAfterHelper(self, arc1, arc2):

    arc_interval1 = self._createArcInterval(arc1)

    arc_interval2 = self._getArcIntervalForArc(arc2)

    # list_node1 = OrderMaintainedDoublyLinkedListNode(arc1, None, None)

    list_node1 = DoublyLinkedListNode(arc1, None, None)
  
    list_node2 = self._getListNodeForArc(arc2)
    
    # update companion structure
    
    # print list_node2, list_node1

    (self.om_arc_list).addAfter(list_node1, list_node2)

    # update auxiliary structures

    self._addArcToArcIntervalRelationship(arc1, arc_interval1)

    self._addArcToListNodeRelationship(arc1, list_node1)
    
  # add arc1 before arc2
  
  # modify only auxiliary/companion structures

  # assume that arc1 does not have certain associated objects (i.e. list node, arc interval)
  
  # assume that arc2 does have certain associated objects (i.e. list node, arc interval)

  def _addArcBeforeHelper(self, arc1, arc2):
  
    # list_node1 = OrderMaintainedDoublyLinkedListNode(arc1, None, None)

    list_node1 = DoublyLinkedListNode(arc1, None, None)

    list_node2 = self._getListNodeForArc(arc2)
    
    arc_interval1 = self._createArcInterval(arc1)

    arc_interval2 = self._getArcIntervalForArc(arc2)

    # update companion structure

    (self.om_arc_list).addBefore(list_node1, list_node2)

    """

    print "adding arc before an existing arc for auxiliary/companion structures and order comparison is:", (self.om_arc_list).order(list_node1, list_node2)

    print list_node1, list_node2

    print "label values:", list_node1.getLabel().getValue(), list_node2.getLabel().getValue()

    print "label values:", list_node1.getLabel(), list_node2.getLabel()

    """

    # print (self.om_arc_list).overlying_tree.toString()

    node_inorder_list = (self.om_arc_list).overlying_tree.toInorderInternalNodeList()

    # node_label_value_list = [(PathLabel.toBaseThreeString(x.getPathLabel().getNumericPath()), x.getPathLabel().getPathLength())  for x in node_inorder_list]

    # print node_label_value_list

    # focus_list = [x.getElement().getValue().getNode().getElement().getFocus() for x in node_inorder_list]

    # print focus_list

    node_inorder_list = (self.om_arc_list)._toNodeList()

    # node_label_value_list = [(PathLabel.toBaseThreeString(x.getLabel().getNumericPath()), x.getLabel().getPathLength())  for x in node_inorder_list]

    focus_list = [x.getFocus() for x in (self.om_arc_list).toElementList()]

    # print focus_list

    # print node_label_value_list

    # update auxiliary structures

    self._addArcToArcIntervalRelationship(arc1, arc_interval1)

    self._addArcToListNodeRelationship(arc1, list_node1)

  def _addArcAsFirstHelper(self, arc):
  
    # list_node = OrderMaintainedDoublyLinkedListNode(arc, None, None)

    list_node = DoublyLinkedListNode(arc, None, None)
    
    arc_interval = self._createArcInterval(arc)
    
    # update companion structure
    
    (self.om_arc_list).addFirst(list_node)
    
    # update auxiliary structures
    
    self._addArcToArcIntervalRelationship(arc, arc_interval)

    self._addArcToListNodeRelationship(arc, list_node)
    
  def _createArcInterval(self, arc):
  
    return ArcInterval(arc, self, self.getSweepLine())

# update companion structure

# update auxiliary structures

# add to tree

  def getArcList(self):

    return self.toInorderList()

  def getBreakpointList(self):

    arc_list = self.getArcList()
    
    num_arcs = len(arc_list)
    
    num_pairs = max(0, num_arcs - 1)
    
    adjacent_arc_pairs = []
    
    for i in range(0, num_pairs):
    
      left_arc = arc_list[i]
      
      right_arc = arc_list[i + 1]
      
      arc_pair = (left_arc, right_arc)
      
      adjacent_arc_pairs.append(arc_pair)
      
    breakpoint_list = [Breakpoint(x[0], x[1]) for x in adjacent_arc_pairs]
    
    return breakpoint_list

  def toString(self):

    return BalancedIntervalTree.toString(self)

  def getPrecision(self):

    return self.precision

  def setPrecision(self, precision):

    self.precision = precision

  """

  # truncate a value

  # precision is # of places to right of decimal point to keep

  @staticmethod

  def _truncate(value, precision):

    return truncate(value, precision)

  """

  def getNumArcs(self):
  
    return self.getNumEntries()
    
  def hasNoArcs(self):
  
    return self.getNumArcs() == 0

  def getLevelValue(self):
  
    return self.level

  def _chooseTaggedResponsibleInterval(self, tagged_intervals):

    # get intervals with max. candidate value

    matching_tagged_intervals = self._getTaggedCandidateIntervalsWithMaxMaxValue(tagged_intervals)

    # get interval that is most to the right

    # tagged_arc_intervals = tagged_intervals

    tied_tagged_intervals = matching_tagged_intervals

    tied_tagged_arc_intervals = tied_tagged_intervals

    # arcs = [x._getArc() for x in arc_intervals]

    key_transform = lambda x: self._key_transform(x[0])

    comparator = self._comparator

    sorted_tied_tagged_arc_intervals = sorted(tied_tagged_arc_intervals, key = key_transform, cmp = comparator, reverse = True)

    chosen_tied_tagged_arc_interval = sorted_tied_tagged_arc_intervals[0]

    return chosen_tied_tagged_arc_interval

  """

  def toIntervalString(self):

    pass

  """

  def toFocusList(self):

    internal_node_list = self.toInorderInternalNodeList()

    focus_list = [x.getElement().getKey()._getArc().getFocus() for x in internal_node_list]

    return focus_list

  """

  def toInternalNodeList(self):

    pass

  """

  """

  # takes O(n ^ 2) time

  def checkForAgreement(self):

    node_list = self.toInorderInternalNodeList()

    return self._checkForAgreement(node_list)

  def _checkForAgreement(self, node_list):

    if len(node_list) == 0:

      return True

    else:

      curr_node = node_list[0]

      curr_arc = curr_node.getElement().getKey()._getArc()

      curr_list_node = self._getListNodeForArc(curr_arc)

      candidate_list_nodes = [x for x in self._getOrderMaintainedArcList()._toNodeList() if x.getElement() == curr_arc]

      matching_list_node = candidate_list_nodes[0]

      # print "list nodes:", curr_list_node, matching_list_node

      if not (curr_list_node == matching_list_node):

        return False

      else:

        next_node_list = node_list[1 : ]

        return self._checkForAgreement(next_node_list)

  """

"""

sweep_line = SweepLine(2)

tree = ArcTree(3, sweep_line)

arc1 = Arc([0, 2])

arc2 = Arc([0, 1])

arc3 = Arc([0, 0])

tree.insertArc(arc1)

print tree.toIntervalStringList()

sweep_line.setY(1)

tree.insertArc(arc2)

sweep_line.setY(0)

tree.insertArc(arc3)

print tree.toString()

internal_node_list = tree.toInorderInternalNodeList()

interval_list = [x.getElement().getKey() for x in internal_node_list]

interval_string_list = [x.toString() for x in interval_list]

arc_list = [x._getArc() for x in interval_list]

arc_focus_list = [x.getFocus() for x in arc_list]

print internal_node_list

print interval_list

print interval_string_list

print arc_list

print arc_focus_list

"""

"""

arc1 = Arc([2, 3])

arc2 = Arc([1, 1])

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

print "tree:", tree.toString()

sweep_line.setY(3)

tree.insertArc(arc1)

print "tree:", tree.toString()

sweep_line.setY(1)

tree.insertArc(arc2)

print "tree:", tree.toString()

sweep_line.setY(0.7639)

# tree.removeArc(arc2)

# print "tree:", tree.toString()

"""

"""

# insert (45, 99), insert (58, 99), insert (38, 99)

arc1 = Arc((45, 99))

arc2 = Arc((58, 99))

arc3 = Arc((38, 99))

sweep_line = SweepLine()

sweep_line.setY(99)

tree = ArcTree(3, sweep_line)

tree.insertArc(arc1)

tree.insertArc(arc2)

arc, payload = tree.query(38)

print "focus:", arc.getFocus()

tree.insertArc(arc3)

print tree.toFocusList()

print tree.toIntervalStringList()

"""

"""

# insert (75, 100), insert (64, 99), insert (36, 99)

# insert (51, 100), insert (67, 98)

sweep_line = SweepLine()

# sweep_line.setY(99)

tree = ArcTree(3, sweep_line)

arc1 = Arc((71, 99))

arc2 = Arc((70, 99))

arc3 = Arc((37, 99))

arc4 = Arc((94, 97))

arc5 = Arc((21, 94))

arc6 = Arc((75, 94))

arc7 = Arc((50, 93))

arc8 = Arc((92, 93))

arc9 = Arc((6, 91))

arc10 = Arc((12, 90))

sweep_line.setY(99)

tree.insertArc(arc1)

tree.insertArc(arc2)

tree.insertArc(arc3)

sweep_line.setY(97)

tree.insertArc(arc4)

sweep_line.setY(94)

tree.insertArc(arc5)

tree.insertArc(arc6)

sweep_line.setY(93)

tree.insertArc(arc7)

tree.insertArc(arc8)

print tree.toIntervalStringList()

# rest is unnecessary

arc, payload = tree.query(93)

print "focus:", arc.getFocus()

# tree.insertArc(arc3)

# sweep_line.setY(96.9977477934)

print tree.toIntervalStringList()

tree_arc_focus_list = tree.toFocusList()

print tree_arc_focus_list

om_list_node_inorder_list = tree._getOrderMaintainedArcList()._toNodeList()

om_list_arc_focus_list = [x.getElement().getFocus() for x in om_list_node_inorder_list]

# om_list_label_value_list = [x.getLabel().getValue() for x in om_list_node_inorder_list]

print "order-maintained list arc focus list:", om_list_arc_focus_list

# print "order-maintained list label value list:", om_list_label_value_list

label_tree_node_inorder_list = tree._getOrderMaintainedArcList().overlying_tree.toInorderInternalNodeList()

# label_tree_arc_focus_list = [x.getElement().getValue().getNode().getElement().getFocus() for x in label_tree_node_inorder_list]

label_tree_node_label_value_list = [(PathLabel.toBaseThreeString(x.getPathLabel().getNumericPath()), x.getPathLabel().getPathLength())  for x in label_tree_node_inorder_list]

# print "label tree arc focus list:", label_tree_arc_focus_list

print "label tree label list:", label_tree_node_label_value_list

# print tree._getOrderMaintainedArcList().overlying_tree.checkForAgreement()

# print tree._getOrderMaintainedArcList().checkForAgreement()

# print tree.checkForAgreement()

"""

"""

tree.removeArc(arc3)

tree.removeArc(arc7)

print tree._getOrderMaintainedArcList().toElementList(), arc1

print tree.toFocusList()

print tree.toIntervalStringList()

tree.removeArc(arc1)

tree.removeArc(arc6)

sweep_line.setY(91)

tree.insertArc(arc9)

sweep_line.setY(90)

tree.insertArc(arc10)

tree.removeArc(arc5)

tree.removeArc(arc9)

tree.removeArc(arc10)

"""

"""

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

arc1 = Arc((97, 96))

arc2 = Arc((47, 93))

arc3 = Arc((67, 93))

arc4 = Arc((34, 91))

arc5 = Arc((76, 88))

sweep_line.setY(96)

tree.insertArc(arc1)

sweep_line.setY(93)

tree.insertArc(arc2)

tree.insertArc(arc3)

sweep_line.setY(92.801271358)

# print tree.toIntervalStringList()

print tree.toFocusList()

# cannot remove an arc that ends up being split after it has been split

# tree.removeArc(arc1)

# tree.removeArc(arc2)

sweep_line.setY(91)

tree.insertArc(arc4)

sweep_line.setY(88)

tree.insertArc(arc5)

"""

"""

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

arc1 = Arc((143, 382))

arc2 = Arc((382, 374))

arc3 = Arc((291, 363))

sweep_line.setY(382)

tree.insertArc(arc1, 382)

sweep_line.setY(374)

tree.insertArc(arc2, 382)

"""

"""

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

arc1 = Arc((156, 380))

arc2 = Arc((155, 377))

arc3 = Arc((155, 380))

sweep_line.setY(380)

tree.insertArc(arc1, 380)

tree.insertArc(arc3, 380)

sweep_line.setY(377)

tree.insertArc(arc2, 380)

"""

"""

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

arc1 = Arc((383, 384))

arc2 = Arc((228, 384))

arc3 = Arc((146, 383))

arc4 = Arc((238, 379))

arc5 = Arc((301, 367))

sweep_line.setY(384)

tree.insertArc(arc1, 384)

tree.insertArc(arc2, 384)

sweep_line.setY(383)

tree.insertArc(arc3, 384)

sweep_line.setY(379)

tree.insertArc(arc4, 384)

sweep_line.setY(367)

tree.insertArc(arc5, 384)

sweep_line.setY(364)

nodes = tree.toInorderInternalNodeList()

responsible_intervals = [x.getMaxRightEndpoint().getResponsibleInterval() for x in nodes]

responsible_interval_strings = [x.toString() for x in responsible_intervals]

print tree.toString()

print tree.toFocusList()

print responsible_interval_strings

# sweep_line.setY(363)

# print tree.toInorderList()

# print tree.toString()

# raise Exception()

print tree.toIntervalStringList()

# tree.insertArc(arc3, 382)

"""

"""

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

arc1 = Arc((170, 314))

arc2 = Arc((230, 271))

arc3 = Arc((359, 228))

sweep_line.setY(314)

tree.insertArc(arc1, 314)

print tree.toIntervalStringList()

sweep_line.setY(271)

tree.insertArc(arc2, 314)

print tree.toIntervalStringList()

sweep_line.setY(228)

print tree.toIntervalStringList()

arc, payload = tree.query(359)

print tree.toString()

print "focus:", arc.getFocus()

# raise Exception()

tree.insertArc(arc3, 314)

print tree.toFocusList()

"""

"""

sweep_line.setY(228)

tree.insertArc(arc3, 314)

print tree.toIntervalStringList()

print tree.toFocusList()

"""

# cannot remove an arc that ends up being split after it has been split

# tree.removeArc(arc1)

# tree.removeArc(arc2)

# print tree.toIntervalStringList()


