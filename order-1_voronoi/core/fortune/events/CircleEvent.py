# from ...geometry.Bisector import *

from ...Util import *

from ...graph.Vertex import *

from Event import *

from ...geometry.BisectorRay import *

from ..Breakpoint import *

class CircleEvent(Event):

  # def __init__(self, arc):

  def __init__(self, arc, causing_event_is_site_type):

    self.arc = arc

    self.causing_event_is_site_type = causing_event_is_site_type
    
  def getArc(self):

    return self.arc

  def getCausingEventIsSiteType(self):

    return self.causing_event_is_site_type

  def setCausingEventIsSiteType(self, causing_event_is_site_type):

    self.causing_event_is_site_type = causing_event_is_site_type

  """

  def centerArcIsSplitResidueArc(self):

    return (self.arc).getIsSplitResidueArc()

  """

  # retrieve focus of associated arc

  def _getAssociatedLocation(self):

    return self.getArc().getFocus()
    
  # append vertices to the vertex list

  def handle(self, tree, vertex_list, event_queue, truncated_bisector_edge_dict, sweep_line, initial_y_value):
  
    # print "handling a circle event"

    # three phases

    # 1. deal with arc tree and potentially 
    #      invalidate future circle events

    # 2. deal with features of diagram

    # 3. check for newly visible circle events
    
    # phase 1
    
    arc = self.getArc()
    
    left_arc = tree.getArcLeftNeighbor(arc)
    
    right_arc = tree.getArcRightNeighbor(arc)

    # print "left arc focus:", left_arc.getFocus()

    # print "arc focus:", arc.getFocus()

    # print "right arc focus:", right_arc.getFocus()

    # left_found_arc, left_found_payload = tree.getArcWithPayload(left_arc)

    l_y = sweep_line.getY()
    
    left_found_payload = tree.getArcPayload(left_arc)

    invalidated_left_arc_circle_event = False

    arc1 = tree.getArcLeftNeighbor(left_arc)

    arc2 = left_arc

    arc3 = arc
    
    if left_found_payload.hasCircleEvent() == True:

      result = CircleEvent.getLargestEmptyCircleLowestExtent(l_y, arc1, arc2, arc3)

      location = result

      y = location[1]

      curr_y = l_y

      # print "circle event y and sweep-line y:", y, curr_y

      # raise Exception()

      # if CircleEvent.axisAlignedComp(y, curr_y) == 0:

      if False:

        # do not remove circle event

        # raise Exception()

        pass

      else:

        # print "removed event's arcs:", arc1.getFocus(), arc2.getFocus(), arc3.getFocus()

        # remove circle event

        # print "invalidating a circle event for a left neighbor arc with focus:", left_arc.getFocus()
    
        left_circle_event = left_found_payload.getCircleEvent()
      
        # event_queue.remove(left_circle_event)

        event_queue.removeEvent(left_circle_event)
      
        left_found_payload.removeCircleEvent()

        invalidated_left_arc_circle_event = True

    # right_found_arc, right_found_payload = tree.getArcWithPayload(right_arc)

    right_found_payload = tree.getArcPayload(right_arc)

    invalidated_right_arc_circle_event = False
    
    arc1 = arc

    arc2 = right_arc

    arc3 = tree.getArcRightNeighbor(right_arc)

    if right_found_payload.hasCircleEvent() == True:

      result = CircleEvent.getLargestEmptyCircleLowestExtent(l_y, arc1, arc2, arc3)

      location = result

      y = location[1]

      curr_y = l_y

      # print "circle event y and sweep-line y:", y, curr_y

      # if CircleEvent.axisAlignedComp(y, curr_y) == 0:

      if False:

        # do not remove circle event

        # raise Exception()

        pass

      else:

        # print "removed event's arcs:", arc1.getFocus(), arc2.getFocus(), arc3.getFocus()

        # remove circle event

        # print "invalidating a circle event for a right neighbor arc with focus:", right_arc.getFocus()
    
        right_circle_event = right_found_payload.getCircleEvent()
      
        event_queue.removeEvent(right_circle_event)
      
        right_found_payload.removeCircleEvent()

        invalidated_right_arc_circle_event = True

    invalidated_values = [invalidated_left_arc_circle_event, invalidated_right_arc_circle_event]

    affirmative_invalidated_values = [x for x in invalidated_values if x == True]

    num_affirmative_invalidated_values = len(affirmative_invalidated_values)

    # print tree.toFocusList(), tree.toIntervalStringList()

    # print "circle event leads to # of circle events being invalidated:", num_affirmative_invalidated_values

    # phase 2
    
    # retrieve two edges
    
    # create an edge
    
    # create a vertex
    
    # set three endpoints
    
    left_site = left_arc.getFocus()
    
    center_site = arc.getFocus()
    
    right_site = right_arc.getFocus()

    left_edge = truncated_bisector_edge_dict.getTruncatedBisectorEdge(left_site, center_site)
    
    right_edge = truncated_bisector_edge_dict.getTruncatedBisectorEdge(center_site, right_site)
    
    outgoing_edge = truncated_bisector_edge_dict.addTruncatedBisectorEdge(left_site, right_site)
    
    might_occur, lowest_extent_location = CircleEvent.mightLeadToACircleEventOccurringInFuture(left_arc, arc, right_arc, sweep_line.getY())

    l_y = sweep_line.getY()

    # print "sweep-line y-value:", l_y

    # raise Exception()

    focus1 = left_arc.getFocus()

    focus2 = arc.getFocus()

    focus3 = right_arc.getFocus()

    # bisector1 = Bisector(focus1, focus2)

    bisectorRay1 = CircleEvent.getBisectorRay(l_y, left_arc, arc)

    """

    print "bisector ray one:", bisectorRay1.toString()

    print "focuses:", focus1, focus2, focus3

    """

    # bisector2 = Bisector(focus2, focus3)

    bisectorRay2 = CircleEvent.getBisectorRay(l_y, arc, right_arc)

    """

    print "bisector ray two:", bisectorRay2.toString()

    print tree.toIntervalStringList()

    print tree.toFocusList()

    """

    # raise Exception()

    # print bisectorRay1.doesIntersectWithRay(bisectorRay2)

    # print bisectorRay1.intersectWithRay(bisectorRay2)

    # print focus1, focus2, focus3

    # print bisector1.doesIntersectWithBisector(bisector2)

    # print CircleEvent.getLargestEmptyCircleLowestExtent(left_arc, arc, right_arc), sweep_line.getY()

    location = CircleEvent.getIntersectionHelper(l_y, left_arc, arc, right_arc)

    # truncate components of location 
    # so as to have outputted features 
    # with certain amount of precision

    x, y = location

    """

    truncated_x = tree._truncate(x, tree.getPrecision())

    truncated_y = tree._truncate(y, tree.getPrecision())

    """

    rounded_x = round_with_precision(x, tree.getPrecision())

    rounded_y = round_with_precision(y, tree.getPrecision())

    """

    location_with_truncated_components = (truncated_x, truncated_y)

    # vertex = Vertex(None, location)
    
    vertex = Vertex(None, location_with_truncated_components)
    
    """

    location_with_rounded_components = (rounded_x, rounded_y)

    vertex = Vertex(None, location)

    vertex_list.append(vertex)
    
    # print "about to modify existing edges"

    """
    
    left_edge.setIndeterminateEndpoint(location)
    
    right_edge.setIndeterminateEndpoint(location)

    outgoing_edge.setIndeterminateEndpoint(location)

    """

    truncated_bisector_edge_dict.setIndeterminateEndpoint(left_site, center_site, vertex)

    truncated_bisector_edge_dict.setIndeterminateEndpoint(center_site, right_site, vertex)

    truncated_bisector_edge_dict.setIndeterminateEndpoint(left_site, right_site, vertex)

    # phase 1 transplanted

    # remove an arc

    tree.removeArc(arc)

    # phase 3

    might_occur1 = None

    might_occur2 = None

    if tree.hasArcLeftNeighbor(left_arc):

      triple1_left = tree.getArcLeftNeighbor(left_arc)
    
      triple1_center = left_arc
    
      triple1_right = right_arc

      # print tree.toString()

      might_occur1, lowest_extent_location1 = CircleEvent.mightLeadToACircleEventOccurringInFuture(triple1_left, triple1_center, triple1_right, sweep_line.getY())

      # location1 = CircleEvent.getIntersectionHelper(triple1_left, triple1_center, triple1_right)

      if might_occur1 == True:

        # print "for a circle event, see that we have a possible additional circle event:", triple1_left.getFocus(), triple1_center.getFocus(), triple1_right.getFocus()

        event = CircleEvent(triple1_center, True)
      
        y = lowest_extent_location1[1]

        priority = -1 * y

        # priority = tree._truncate(-1 * y, tree.getPrecision())
      
        # priority = -1 * getLargestEmptyCircleLowestExtent(triple1_left, triple1_center, triple1_right)
      
        event_queue.insert((priority, triple1_center.getIsSplitResidueArc()), event)

        # print "prospective circle event involving arcs with focuses:", triple1_left.getFocus(), triple1_center.getFocus(), triple1_right.getFocus()

        # found_arc, found_payload = tree.getArcWithPayload(triple1_center)
      
        found_payload = tree.getArcPayload(triple1_center)
      
        found_payload.setCircleEvent(event)

        if event.isCircleEvent() == False:

          raise Exception("storing as a circle event a site event")

        # found_payload.setEventPriority(priority)

    if tree.hasArcRightNeighbor(right_arc):
    
      triple2_left = left_arc
    
      triple2_center = right_arc
    
      triple2_right = tree.getArcRightNeighbor(right_arc)
    
      might_occur2, lowest_extent_location2 = CircleEvent.mightLeadToACircleEventOccurringInFuture(triple2_left, triple2_center, triple2_right, sweep_line.getY())

      # location2 = CircleEvent.getIntersectionHelper(triple2_left, triple2_center, triple2_right)
    
      if might_occur2 == True:
    
        # print "for a circle event, see that we have a possible additional circle event:", triple2_left.getFocus(), triple2_center.getFocus(), triple2_right.getFocus()

        event = CircleEvent(triple2_center, True)
      
        y = lowest_extent_location2[1]

        priority = -1 * y

        # priority = tree._truncate(-1 * y, tree.getPrecision())

        # priority = -1 * getLargestEmptyCircleLowestExtent(triple2_left, triple2_center, triple2_right)
      
        event_queue.insert((priority, triple2_center.getIsSplitResidueArc()), event)

        # print "prospective circle event involving arcs with focuses:", triple2_left.getFocus(), triple2_center.getFocus(), triple2_right.getFocus()
      
        # found_arc, found_payload = tree.getArcWithPayload(triple2_center)

        # print "focus:", triple2_center.getFocus()

        found_payload = tree.getArcPayload(triple2_center)
      
        found_payload.setCircleEvent(event)

        if event.isCircleEvent() == False:

          raise Exception("storing as a circle event a site event")

        # found_payload.setEventPriority(priority)

    might_occur_values = [might_occur1, might_occur2]

    affirmative_might_occur_values = [x for x in might_occur_values if x == True]

    num_affirmative_might_occur_values = len(affirmative_might_occur_values)

    # print "circle event leads to # of possible circle events:", num_affirmative_might_occur_values

  # if a bisector intersection exists, return an (x, y) tuple

  # otherwise, return None

  @staticmethod
  
  # def getIntersectionHelper(arc1, arc2, arc3):
  
  def getIntersectionHelper(l_y, arc1, arc2, arc3):

    focus1 = arc1.getFocus()

    focus2 = arc2.getFocus()

    focus3 = arc3.getFocus()

    # print "focuses for arcs involved in an intersection:", focus1, focus2, focus3

    # print "sweep-line y-value for an intersection:", l_y

    # bisector1 = Bisector(focus1, focus2)

    bisectorRay1 = CircleEvent.getBisectorRay(l_y, arc1, arc2)

    # print focus1, focus2, focus3

    # bisector2 = Bisector(focus2, focus3)

    bisectorRay2 = CircleEvent.getBisectorRay(l_y, arc2, arc3)

    # print "bisector one for intersection:", bisectorRay1.toString()

    # print "bisector two for intersection:", bisectorRay2.toString()

    # print focus1, focus2, focus3

    # if not bisector1.doesIntersectWithBisector(bisector2):

    # if not bisectorRay1.intersectWithRay(bisectorRay2):

    # print "ray intersects:", bisectorRay1.doesIntersectWithRay(bisectorRay2)

    # using this test to disqualify intersections is flawed; 
    #   it ignores case where an arc is inserted that is at bottom 
    #   of largest empty circle for a circle event

    # middle_arc_is_growing = (arc1.isDegenerate(l_y) == False) and (arc2.isDegenerate(l_y) == True) and (arc3.isDegenerate(l_y) == False)

    """

    print "middle arc is growing:", middle_arc_is_growing

    print arc1.getFocus(), arc2.getFocus(), arc3.getFocus(), l_y

    print "bisector rays intersect:", bisectorRay1.doesIntersectWithRay(bisectorRay2)

    """

    # cover case where middle arc is growing but not degenerate

    # resulting pair of arc neighbors would share same focus

    """

    if bisectorRay1.doesIntersectWithRay(bisectorRay2) == False and not (arc1.isDegenerate(l_y) == False and arc2.isDegenerate(l_y) == True and arc3.isDegenerate(l_y) == False):

    """

    # if (bisectorRay1.doesIntersectWithRay(bisectorRay2) == False or middle_arc_is_growing == True):

    if (bisectorRay1.doesIntersectWithRay(bisectorRay2) == False):

      # print arc2.isDegenerate(l_y)

      # print "returning that we have no intersection"

      return None

    else:

      # location = bisector1.intersectWithBisector(bisector2)

      location = bisectorRay1.intersectWithRay(bisectorRay2)

      # print "intersection location:", location
  
      return location

  @staticmethod

  def intersectionExists(l_y, arc1, arc2, arc3):

    location = CircleEvent.getIntersectionHelper(l_y, arc1, arc2, arc3)

    # print "intersection location:", location

    result = location != None

    return result
  
  # assume a bisector intersection exists

  # return an (x, y) tuple

  @staticmethod
  
  def distanceFromBisectorIntersectionToContributingSite(l_y, arc1, arc2, arc3):

    # distance from center of a largest empty circle to a site on its boundary
  
    location = CircleEvent.getIntersectionHelper(l_y, arc1, arc2, arc3)

    site = arc1.getFocus()

    """

    site2 = arc2.getFocus()

    site3 = arc3.getFocus()

    """
  
    distance = getDistance(location, site)

    # print "largest empty circle arc focuses:", arc1.getFocus(), arc2.getFocus(), arc3.getFocus()

    # print "largest empty circle center, site, radius:", location, site, distance

    """

    distance2 = getDistance(location, site2)

    distance3 = getDistance(location, site3)

    print distance, distance2, distance3

    """
  
    return distance

  # assume a bisector intersection exists
  
  # return an (x, y) tuple

  @staticmethod

  def getLargestEmptyCircleLowestExtent(l_y, arc1, arc2, arc3):

    location = CircleEvent.getIntersectionHelper(l_y, arc1, arc2, arc3)
  
    distance = CircleEvent.distanceFromBisectorIntersectionToContributingSite(l_y, arc1, arc2, arc3)

    # print arc1.getFocus(), arc2.getFocus(), arc3.getFocus()
  
    lowest_extent_x = location[0]
  
    lowest_extent_y = location[1] - distance
  
    lowest_extent = (lowest_extent_x, lowest_extent_y)

    # print "values related to largest empty circle:", location, distance, lowest_extent

    return lowest_extent

  # might occur, given that circle event might be invalidated

  # by future, we mean at current sweep line location or lower, 
  # assuming that sweep line moves from top to bottom

  # return a (might_occur, location) tuple

  # might_occur is a boolean value

  # location is an (x, y) tuple 
  # if a corresponding circle event 
  # will occur in the "future", 
  # or None if a corresponding circle event 
  # will not occur in the "future"

  # location is lowest extent of corresponding largest empty circle

  @staticmethod

  # def mightLeadToACircleEventOccurringInFuture(arc1, arc2, arc3, l_y):

  def mightLeadToACircleEventOccurringInFuture(arc1, arc2, arc3, l_y, tolerance = 0.001):

    # result = getIntersectionHelper(arc1, arc2, arc3)

    intersection_exists = CircleEvent.intersectionExists(l_y, arc1, arc2, arc3)

    # print "intersection exists:", intersection_exists
  
    # if result == None:

    if intersection_exists == False:

      # no bisector intersection exists

      return (False, None)

    else:

      result = CircleEvent.getLargestEmptyCircleLowestExtent(l_y, arc1, arc2, arc3)

      location = result

      y = location[1]
    
      # print arc1.getFocus(), arc2.getFocus(), arc3.getFocus()
    
      # print "proposed circle event priority:", -1 * location[1]

      # print location, l_y

      # print "circle event prediction values:", y, l_y

      # if y <= l_y:

      # tolerance = tree._getTolerance()

      # print y, l_y

      y_is_satisfactory = (y <= (l_y + tolerance))

      # print y, l_y

      if y_is_satisfactory == True:

        # print "circle event might occur"

        return (True, location)
  
      else:

        return (False, None)

  def toString(self):

    return "circle event"

  def isCircleEvent(self):

    return True

  # x and y are location components, i.e. scalars

  # specifically, the location components 
  #   are assumed to be values that are 
  #   axis-aligned measurements

  @staticmethod

  # def _featureLocationComponentComparator(x, y, tolerance = 0.001):

  def axisAlignedComp(x, y, tolerance = 0.001):

    if x >= (y + tolerance):

      return 1

    elif x <= (y - tolerance):

      return -1

    elif (x <= (y + tolerance)) and (x >= (y - tolerance)):

      return 0

  # retrieve a bisector ray for a given left arc, right arc, and a sweep-line position

  # we do not attempt to get bisector rays for leading arcs

  @staticmethod

  def getBisectorRay(l_y, arc1, arc2):

    """

    arc_interval1 = arc_tree._getArcIntervalForArc(arc1)

    arc_interval2 = arc_tree._getArcIntervalForArc(arc2)

    """

    # generating breakpoints on-the-fly

    # breakpoint = Breakpoint(arc1, arc2)

    focus1 = arc1.getFocus()

    focus2 = arc2.getFocus()

    focus_y1 = focus1[1]

    focus_y2 = focus2[1]

    focus_x1 = focus1[0]

    focus_x2 = focus2[0]

    arcs = [arc1, arc2]

    min_focus_x = min(focus_x1, focus_x2)

    left_arc_candidates = [x for x in arcs if (x.getFocus())[0] == min_focus_x]

    left_arc = left_arc_candidates[0]

    right_arc_candidates = [x for x in arcs if x != left_arc]

    right_arc = right_arc_candidates[0]

    left_arc_focus = left_arc.getFocus()

    right_arc_focus = right_arc.getFocus()

    # sweep_line = arc_tree.getSweepLine()

    # l_y = sweep_line.getY()

    # if focus_y1 == focus_y2 and focus_y1 == l_y:

    """

    if CircleEvent.axisAlignedComp(focus_y1, focus_y2) == 0 and CircleEvent.axisAlignedComp(focus_y1, l_y) == 0:

      # both arcs are degenerate and are leading arcs

      # create a downward-facing vertical bisector ray 
      #   with base of midpoint of line segment 
      #   from arc one focus to arc two focus

      # such a bisector ray is clockwise ninety degrees 
      #   from line segment from arc one focus to arc two focus

      breakpoint = Breakpoint(arc1, arc2)

      breakpoint_location = breakpoint.getLocation(l_y)

      # bisectorRay = BisectorRay.construct(focus2, focus1)

      # bisectorRay = BisectorRay.construct(focus2, focus1, breakpoint_location)

      bisectorRay = BisectorRay.construct(right_arc_focus, left_arc_focus, breakpoint_location)

      return bisectorRay

    # elif focus_y1 == focus_y2 and focus_y1 != l_y:

    """

    if CircleEvent.axisAlignedComp(focus_y1, focus_y2) == 0 and CircleEvent.axisAlignedComp(focus_y1, l_y) != 0:

      # create a downward-facing vertical bisector 
      #   with a base of breakpoint corresponding to the two arcs 

      breakpoint = Breakpoint(arc1, arc2)

      breakpoint_location = breakpoint.getLocation(l_y)

      # bisectorRay = BisectorRay(focus2, focus1, breakpoint_location)

      bisectorRay = BisectorRay(right_arc_focus, left_arc_focus, breakpoint_location)

      return bisectorRay

    else:

      # create a bisector ray that has base of a breakpoint 
      #   corresponding to the two arcs

      # use concept of a "funnel" to tell 
      #   which of two possible directions 
      #   the bisector ray should point in

      # consider low arc

      low_focus_y = min(focus_y1, focus_y2)

      arcs = [arc1, arc2]

      low_arc_candidates = [x for x in arcs if (x.getFocus())[1] == low_focus_y]

      low_arc = low_arc_candidates[0]

      low_arc_focus = low_arc.getFocus()

      low_arc_focus_x = low_arc_focus[0]

      # print arc1, arc2

      # print focus1, focus2

      breakpoint = Breakpoint(arc1, arc2)

      breakpoint_location = breakpoint.getLocation(l_y)

      # print breakpoint.getXComponent(l_y)

      x, y = breakpoint_location

      # print focus1, focus2, breakpoint_location

      # have a degenerate case where low arc focus 
      #   shares x-component with breakpoint; 
      #   in this case, we consider high arc focus x

      # assume that the two arcs have corresponding focuses 
      #   that do not have x-component values that are the same, 
      #   as any situation possibly leading to this outcome 
      #   would have led arc with higher focus being removed 
      #   upon insertion of the arc with lower focus

      # if x < low_arc_focus_x:

      if CircleEvent.axisAlignedComp(x, low_arc_focus_x) == -1:

        if low_arc == arc1:

          # choose bisector ray with negative x component

          # bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(arc1, arc2, breakpoint_location)

          bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(left_arc, right_arc, breakpoint_location)

          return bisectorRay

        elif low_arc == arc2:

          # bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(arc1, arc2, breakpoint_location)

          bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(left_arc, right_arc, breakpoint_location)

          return bisectorRay

      # elif x > low_arc_focus_x:

      if CircleEvent.axisAlignedComp(x, low_arc_focus_x) == 1:

        if low_arc == arc1:

          # choose bisector ray with positive x component

          # bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(arc1, arc2, breakpoint_location)

          bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(left_arc, right_arc, breakpoint_location)

          return bisectorRay

        elif low_arc == arc2:

          # bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(arc1, arc2, breakpoint_location)

          bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(left_arc, right_arc, breakpoint_location)

          return bisectorRay

      # elif x == low_arc_focus_x:

      # low arc is degenerate

      elif CircleEvent.axisAlignedComp(x, low_arc_focus_x) == 0:

        # choose bisector ray with x component 
        #   pointing in direction of high arc focus x 
        #   relative to breakpoint x component

        # assume that high arc x is never equal to low arc x

        high_arc_candidates = [x for x in arcs if (x.getFocus())[1] != low_focus_y]

        high_arc = high_arc_candidates[0]

        high_arc_focus = high_arc.getFocus()

        high_arc_focus_x = high_arc_focus[0]

        # print "high arc focus:", high_arc_focus

        # if high_arc_focus_x < low_arc_focus_x:

        if CircleEvent.axisAlignedComp(high_arc_focus_x, low_arc_focus_x) == -1:

          if low_arc == arc1:

            bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(arc1, arc2, breakpoint_location)

            return bisectorRay

          elif low_arc == arc2:

            # choose bisector ray with negative x component

            bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(arc1, arc2, breakpoint_location)

            # print "bisector ray:", bisectorRay.toString()

            return bisectorRay

        # elif high_arc_focus_x > low_arc_focus_x:

        elif CircleEvent.axisAlignedComp(high_arc_focus_x, low_arc_focus_x) == 1:

          if low_arc == arc1:

            # choose bisector ray with positive x component

            bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(arc1, arc2, breakpoint_location)

            # print "bisector ray:", bisectorRay.toString()

            return bisectorRay

          elif low_arc == arc2:

            bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(arc1, arc2, breakpoint_location)

            return bisectorRay

        # elif high_arc_focus_x == low_arc_focus_x:

        elif CircleEvent.axisAlignedComp(high_arc_focus_x, low_arc_focus_x) == 0:

          if low_arc == arc1:

            bisectorRay = CircleEvent.getBisectorRayWithPositiveXComponent(arc1, arc2, breakpoint_location)

            return bisectorRay

          elif low_arc == arc2:

            bisectorRay = CircleEvent.getBisectorRayWithNegativeXComponent(arc1, arc2, breakpoint_location)

            return bisectorRay

    raise Exception("fell through")

  @staticmethod

  def getBisectorRayWithNegativeXComponent(arc1, arc2, offset_vector):

    bisector_ray_candidates = CircleEvent.getBisectorRayCandidates(arc1, arc2, offset_vector)

    satisfactory_bisector_rays = [x for x in bisector_ray_candidates if CircleEvent.bisectorRayHasNegativeXComponent(x) == True]

    satisfactory_bisector_ray = satisfactory_bisector_rays[0]

    return satisfactory_bisector_ray

  @staticmethod

  def getBisectorRayWithPositiveXComponent(arc1, arc2, offset_vector):

    bisector_ray_candidates = CircleEvent.getBisectorRayCandidates(arc1, arc2, offset_vector)

    satisfactory_bisector_rays = [x for x in bisector_ray_candidates if CircleEvent.bisectorRayHasPositiveXComponent(x) == True]

    satisfactory_bisector_ray = satisfactory_bisector_rays[0]

    return satisfactory_bisector_ray

  # retrieve two candidates in the form of a two-tuple

  @staticmethod

  def getBisectorRayCandidates(arc1, arc2, offset_vector):

    focus1 = arc1.getFocus()

    focus2 = arc2.getFocus()

    # create two bisector rays

    # points ninety degrees CCW of line segment from focus1 to focus2

    bisectorRay1 = BisectorRay(focus1, focus2, offset_vector)

    # points ninety degrees CW of line segment from focus1 to focus2

    bisectorRay2 = BisectorRay(focus2, focus1, offset_vector)

    result = (bisectorRay1, bisectorRay2)

    return result

  @staticmethod

  def bisectorRayHasPositiveXComponent(bisectorRay):

    direction_vector = bisectorRay.getDirectionVector()

    x_component = direction_vector[0]

    # print "x component:", x_component

    is_positive = x_component > 0

    return is_positive

  @staticmethod

  def bisectorRayHasNegativeXComponent(bisectorRay):

    direction_vector = bisectorRay.getDirectionVector()

    x_component = direction_vector[0]

    # print "x component:", x_component

    is_negative = x_component < 0

    return is_negative

"""

# invalid intersection

focus1 = (90.0, 100.0)

focus2 = (86.0, 98.0)

focus3 = (90.0, 100.0)

bisector1 = Bisector(focus1, focus2)

# print focus1, focus2, focus3

bisector2 = Bisector(focus2, focus3)

# print focus1, focus2, focus3

print bisector1.doesIntersectWithBisector(bisector2)

location = bisector1.intersectWithBisector(bisector2)
  
print location

"""

"""

from ..SweepLine import *

# from ..arc_tree.ArcTree import *

sweep_line = SweepLine()

"""

"""

arc_tree = ArcTree(3, sweep_line)

sweep_line.setY(364)

arc_tree.insertArc(arc1)

sweep_line.setY(328)

arc_tree.insertArc(arc2)

sweep_line.setY(243)

arc_tree.insertArc(arc3)

sweep_line.setY(155)

print arc_tree.toIntervalStringList()

"""

from ..arc_tree.Arc import *

"""

l_y = 155

arc1 = Arc((141, 364))

arc2 = Arc((255, 328))

arc3 = Arc((128, 243))

"""

"""

l_y = 268

arc1 = Arc((298, 366))

arc2 = Arc((299, 366))

arc3 = Arc((307, 268))

"""

"""

l_y = 203

arc1 = Arc((298, 366))

arc2 = Arc((299, 366))

arc3 = Arc((370, 203))

"""

"""

l_y = 150

arc1 = Arc((100, 200))

arc2 = Arc((200, 400))

arc3 = Arc((300, 200))

"""

"""

l_y = 79.289

arc1 = Arc((400, 100))

arc2 = Arc((400, 200))

arc3 = Arc((500, 200))

"""

"""

l_y = 79.289

arc1 = Arc((300, 200))

arc2 = Arc((400, 100))

arc3 = Arc((400, 200))

"""

"""

l_y = 79.289

arc1 = Arc((300, 200))

arc2 = Arc((400, 200))

arc3 = Arc((400, 100))

"""

"""

l_y = 200

arc1 = Arc((200, 400), 400)

arc2 = Arc((400, 400), 400)

arc3 = Arc((300, 200), 200)

"""

l_y = 228

"""

arc1 = Arc((170, 314))

arc2 = Arc((230, 271))

arc3 = Arc((170, 314))

"""

"""

arc1 = Arc((230, 271))

arc2 = Arc((170, 314))

arc3 = Arc((359, 228))

bisector_ray1 = CircleEvent.getBisectorRay(l_y, arc1, arc2)

bisector_ray2 = CircleEvent.getBisectorRay(l_y, arc2, arc3)

breakpoint1 = Breakpoint(arc1, arc2)

breakpoint_location1 = breakpoint1.getLocation(l_y)

breakpoint2 = Breakpoint(arc2, arc3)

breakpoint_location2 = breakpoint2.getLocation(l_y)

"""

"""

print "breakpoint one location:", breakpoint_location1

print "breakpoint two location:", breakpoint_location2

print "bisector ray one:", bisector_ray1.toString()

print "bisector ray two:", bisector_ray2.toString()

"""

"""

does_intersect = bisector_ray1.doesIntersectWithRay(bisector_ray2)

intersection = bisector_ray1.intersectWithRay(bisector_ray2)

"""

"""

print does_intersect

"""

"""

# raise Exception()

# print intersection

result = CircleEvent.mightLeadToACircleEventOccurringInFuture(arc1, arc2, arc3, l_y)

# print result

"""


