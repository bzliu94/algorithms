from ..arc_tree.Arc import *

from ..arc_tree.ArcPayload import *

from Event import *

from CircleEvent import *

class SiteEvent(Event):

  # p_i is an (x, y) tuple

  def __init__(self, p_i):

    self.p_i = p_i
    
  def getLocation(self):
  
    return self.p_i

  # retrieve location of site

  def _getAssociatedLocation(self):

    return self.getLocation()
    
  # append vertices to the vertex list

  def handle(self, tree, vertex_list, event_queue, truncated_bisector_edge_dict, sweep_line, initial_y_value):

    l_y = sweep_line.getY()

    # print "handling a site event"

    # raise Exception("handling a site event")

    # three phases

    # 1. deal with arc tree and potentially 
    #      invalidate future circle events

    # 2. deal with features of diagram

    # 3. check for newly visible circle events
    
    site = self.getLocation()

    # if tree.isEmpty() == True:

    if sweep_line.getY() == initial_y_value or tree.hasNoArcs() == True:
    
      # case 1

      # phase 1
      
      arc = Arc(site, tree)

      payload = ArcPayload()

      # print type(arc), type(payloade)

      # print arc, payload
      
      # tree.insertArcAsFirst(arc, payload)

      # tree.insertArc(arc, payload)

      tree.insertArc(arc, initial_y_value)

      # return

      # phase 2

      # (nothing)

      # phase 3

      # (nothing)

      # prepare truncated bisector edges for sites corresponding to leading arcs

      """

      print "sweep-line y-value:", sweep_line.getY()

      print "initial y-value:", initial_y_value

      # raise Exception("outputted sweep-line y-value and initial y-value")

      if sweep_line.getY() == initial_y_value:

        print "considering whether to include a truncated bisector edge"

        # raise Exception("considering whether to include a truncated bisector edge")

        has_left_arc_neighbor = tree.hasArcLeftNeighbor(arc)

        has_right_arc_neighbor = tree.hasArcRightNeighbor(arc)

        arc_focus = arc.getFocus()

        if has_left_arc_neighbor == True:

          # add truncated bisector edge for left arc and current arc

          print "adding a truncated bisector edge for left arc and current arc"

          left_arc = tree.getArcLeftNeighbor(arc)

          left_arc_focus = left_arc.getFocus()

          truncated_bisector_edge_dict.addTruncatedBisectorEdge(left_arc_focus, arc_focus)

        if has_right_arc_neighbor == True:

          # add truncated bisector edge for current arc and right arc

          print "adding a truncated bisector edge for current arc and right arc"

          right_arc = tree.getArcRightNeighbor(arc)

          right_arc_focus = right_arc.getFocus()

          truncated_bisector_edge_dict.addTruncatedBisectorEdge(arc_focus, right_arc_focus)

      """

      # print "site event leads to # of circle events being invalidated:", 0

      # print "site event leads to # of possible circle events:", 0

      return

    else:
    
      # case 2

      # phase 1
    
      x = site[0]

      # print "match:", tree.query(x)

      # print tree.toFocusList()

      # print tree.toIntervalStringList()

      alpha_arc, alpha_payload = tree.query(x)
      
      alpha_site = alpha_arc.getFocus()

      invalidated_a_circle_event = False

      alpha_payload_has_circle_event = alpha_payload.hasCircleEvent()
      
      arc1 = tree.getArcLeftNeighbor(alpha_arc)

      arc2 = alpha_arc

      arc3 = tree.getArcRightNeighbor(alpha_arc)
      
      if alpha_payload_has_circle_event == True:

        circle_event = alpha_payload.getCircleEvent()

        result = CircleEvent.getLargestEmptyCircleLowestExtent(l_y, arc1, arc2, arc3)

        location = result

        y = location[1]

        curr_y = l_y

        # print "circle event y and sweep-line y:", y, curr_y

        # if CircleEvent.axisAlignedComp(y, curr_y) == 0:

        if False:

          # do not remove

          pass

        else:
        
          # print "removed event's arcs:", arc1.getFocus(), arc2.getFocus(), arc3.getFocus()

          event_queue.removeEvent(circle_event)
        
          # circle_event.removeCircleEvent()

          alpha_payload.removeCircleEvent()

          invalidated_a_circle_event = True

      num_circle_events_invalidated = 1 if invalidated_a_circle_event == True else 0

      # print "site event leads to # of circle events being invalidated:", num_circle_events_invalidated

      # replace an arc with three

      """
      
      arc1 = alpha_arc
      
      arc2 = Arc(site)
      
      arc3 = Arc(alpha_site)
      
      payload1 = alpha_payload
      
      payload2 = ArcPayload()
      
      payload3 = ArcPayload()

      # print arc1.getFocus(), arc2.getFocus(), arc3.getFocus()
      
      tree.insertArcAfter(alpha_arc, arc2, payload2)

      tree.insertArcAfter(arc2, arc3, payload3)

      """

      # arc = Arc(site)

      arc = Arc(site)

      payload = ArcPayload()

      # tree.insertArc(arc, payload)

      tree.insertArc(arc, initial_y_value)

      # print tree.toFocusList()

      # print tree.toIntervalStringList()

      """

      tree.insertArcAfter(alpha_arc, arc1, payload1)

      tree.insertArcAfter(arc1, arc2, payload2)
      
      tree.insertArcAfter(arc2, arc3, payload3)
      
      tree.removeArc(alpha_arc)

      """
      
      # phase 2
    
      # retrieve edge if one exists

      # both endpoints are indeterminate
    
      truncated_bisector_edge = truncated_bisector_edge_dict.addTruncatedBisectorEdge(alpha_site, site)
    
      # phase 3

      arc1 = tree.getArcLeftNeighbor(arc)

      arc2 = arc

      arc3 = tree.getArcRightNeighbor(arc)

      might_occur1 = None

      might_occur2 = None

      if tree.hasArcLeftNeighbor(arc1):
      
        # print "left triple being considered"
    
        triple1_left = tree.getArcLeftNeighbor(arc1)
    
        triple1_center = arc1
    
        triple1_right = arc2

        """

        print "considering left triple and arc two focus is:", arc2.getFocus()

        print "left arc:", arc1.getFocus()

        print "right arc:", arc3.getFocus()

        print tree.toIntervalStringList()

        print "focus list:", tree.toFocusList()

        print "order-maintenance focus list:", [x.getFocus() for x in tree._getOrderMaintainedArcList().toElementList()]

        """

        # print tree.toFocusList()

        # print tree.toInorderList()

        might_occur1, lowest_extent_location1 = CircleEvent.mightLeadToACircleEventOccurringInFuture(triple1_left, triple1_center, triple1_right, sweep_line.getY())

        if might_occur1 == True:

          # print "introducing a circle event"

          event = CircleEvent(triple1_center, False)
      
          y = lowest_extent_location1[1]

          priority = -1 * y

          # priority = tree._truncate(-1 * y, tree.getPrecision())
      
          # priority = -1 * getLargestEmptyCircleLowestExtent(triple1_left, triple1_center, triple2_right)
      
          event_queue.insert((priority, triple1_center.getIsSplitResidueArc()), event)
      
          # print "inserting a circle event with focus and priority:", triple1_center.getFocus(), priority

          # found_arc, found_payload = tree.getArcWithPayload(triple1_center)

          # entry, node = tree.find(tree._getArcIntervalForArc(triple1_center))

          # print node.getElement().getKey().toString()

          found_payload = tree.getArcPayload(triple1_center)
      
          found_payload.setCircleEvent(event)

          if event.isCircleEvent() == False:

            raise Exception("storing as a circle event a site event")

      if tree.hasArcRightNeighbor(arc3):
      
        # print "right triple being considered"
    
        triple2_left = arc2
    
        triple2_center = arc3
    
        triple2_right = tree.getArcRightNeighbor(arc3)

        """

        print "considering right triple and arc two focus is:", arc2.getFocus()

        print "left arc:", arc1.getFocus()

        print "right arc:", arc3.getFocus()

        print tree.toIntervalStringList()

        print "focus list:", tree.toFocusList()

        print "order-maintenance focus list:", [x.getFocus() for x in tree._getOrderMaintainedArcList().toElementList()]

        """
    
        might_occur2, lowest_extent_location2 = CircleEvent.mightLeadToACircleEventOccurringInFuture(triple2_left, triple2_center, triple2_right, sweep_line.getY())

        # print might_occur2, location2
      
        if might_occur2 == True:

          # print "introducing a circle event"
    
          event = CircleEvent(triple2_center, False)
      
          y = lowest_extent_location2[1]

          priority = -1 * y

          # priority = tree._truncate(-1 * y, tree.getPrecision())
      
          # priority = -1 * getLargestEmptyCircleLowestExtent(triple2_left, triple2_center, triple2_right)

          # print "priority:", priority

          event_queue.insert((priority, triple2_center.getIsSplitResidueArc()), event)

          # print "inserting a circle event with focus and priority:", triple2_center.getFocus(), priority

          """
      
          found_arc, found_payload = tree.getArcWithPayload(triple2_center)
      
          found_payload.setCircleEvent(event)

          """

          found_payload = tree.getArcPayload(triple2_center)
      
          found_payload.setCircleEvent(event)

          if event.isCircleEvent() == False:

            raise Exception("storing as a circle event a site event")

      might_occur_values = [might_occur1, might_occur2]

      affirmative_might_occur_values = [x for x in might_occur_values if x == True]

      num_affirmative_might_occur_values = len(affirmative_might_occur_values)

      # print "site event leads to # of possible circle events:", num_affirmative_might_occur_values

  def toString(self):

    return "site event"

  def isSiteEvent(self):

    return True

