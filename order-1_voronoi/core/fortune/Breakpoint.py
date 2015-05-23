class Breakpoint:

  def __init__(self, arc_a, arc_b):

    self.arc_a = arc_a

    self.arc_b = arc_b

  def getArcA(self):

    return self.arc_a

  def getArcB(self):

    return self.arc_b

  # assume the two corresponding parabolas are non-degenerate

  # in particular, we assume two intersection points

  def getXComponent(self, l_y):
  
    # we have for the two involved arcs
    #   corresponding focuses that have either:
    #   1. x values that are distinct 
    #        and y values that are distinct
    #   2. x values that are identical
    #   3. y values that are identical
    
    # we note that the two involved arcs 
    #   have corresponding focuses 
    #   that do not have:
    #   x values that are identical 
    #     and y values that are identical
    
    # we have six cases

    # print "retrieving an x component"

    arc_a = self.getArcA()
    
    arc_b = self.getArcB()
    
    focus_a = arc_a.getFocus()
    
    focus_b = arc_b.getFocus()
    
    arcs = [arc_a, arc_b]

    arc_focus_pairs = [(x, x.getFocus()) for x in arcs]
    
    y_values = [x[1][1] for x in arc_focus_pairs]
    
    x_values = [x[1][0] for x in arc_focus_pairs]
    
    max_y = max(y_values)
    
    min_y = min(y_values)
    
    max_x = max(x_values)
    
    min_x = min(x_values)

    # print min_x, max_x, min_y, max_y
    
    candidate_high_arcs = [x[0] for x in arc_focus_pairs if x[1][1] == max_y]
    
    candidate_low_arcs = [x[0] for x in arc_focus_pairs if x[1][1] == min_y]
    
    candidate_left_arcs = [x[0] for x in arc_focus_pairs if x[1][0] == min_x]
    
    candidate_right_arcs = [x[0] for x in arc_focus_pairs if x[1][0] == max_x]
    
    high_arc = candidate_high_arcs[0]
    
    low_arc = candidate_low_arcs[0]
    
    left_arc = candidate_left_arcs[0]
    
    right_arc = candidate_right_arcs[0]
    
    x_values_are_identical = focus_a[0] == focus_b[0]
    
    y_values_are_identical = focus_a[1] == focus_b[1]
    
    x_value = None

    # print focus_a, focus_b

    # print x_values_are_identical, y_values_are_identical

    if not x_values_are_identical and not y_values_are_identical:

      # print "case 1"
    
      # case 1: distinguish by y
    
      # if focus_a == high_arc:

      if arc_a == high_arc:
      
        x_value = high_arc.getLeftIntersectionXValue(low_arc, l_y)
        
      else:
      
        x_value = high_arc.getRightIntersectionXValue(low_arc, l_y)

        # print "case 1b:", x_value
        
    elif x_values_are_identical and not y_values_are_identical:

      # print "case 2"
    
      # case 2: distinguish by y
    
      # if focus_a == high_arc:

      if arc_a == high_arc:
      
        x_value = high_arc.getLeftIntersectionXValue(low_arc, l_y)
        
      else:
      
        x_value = high_arc.getRightIntersectionXValue(low_arc, l_y)
        
    elif not x_values_are_identical and y_values_are_identical:

      # print "case 3"
    
      # case 3: distinguish by x
    
      # if focus_a == left_arc:

      if arc_a == left_arc:
      
        # x_value = left_arc.getLeftIntersectionXValue(low_arc, l_y)

        # technically, there is only one intersection point to choose from

        x_value = left_arc.getLeftIntersectionXValue(right_arc, l_y)
        
      else:
      
        # x_value = left_arc.getRightIntersectionXValue(low_arc, l_y)

        # technically, there is only one intersection point to choose from

        # x_value = left_arc.getRightIntersectionXValue(right_arc, l_y)

        x_value = left_arc.getLeftIntersectionXValue(right_arc, l_y)

      # print "case three x value:", x_value

    # print "x value:", x_value
    
    """

    focus_a = self.getArcA().getFocus()

    focus_b = self.getArcB().getFocus()

    # print focus_a, focus_b

    x_a, y_a = focus_a

    x_b, y_b = focus_b

    x_value = None

    if right_focus_y > left_focus_y or right_focus_y == left_focus_y:

      x_value = left_arc.getLeftIntersectionXValue(right_arc, l_y)

    else:

      x_value = left_arc.getLeftIntersectionXValue(right_arc, l_y)
    
    """

    # print focus_a, focus_b, x_value

    return x_value

  # retrieve location

  # return an (x, y) tuple

  def getLocation(self, l_y):

    # handle case where one arc is degenerate, 
    #   but do not handle case 
    #   where two arcs are degenerate

    x_value = self.getXComponent(l_y)

    # print x_value

    # choose an arbitrary non-degenerate arc 
    #   associated with the breakpoint

    arcs = [self.getArcA(), self.getArcB()]

    focuses = [x.getFocus() for x in arcs]

    focus_y_values = [x[1] for x in focuses]

    max_focus_y = max(focus_y_values)

    candidate_arcs = [x for x in arcs if (x.getFocus())[1] == max_focus_y]

    high_arc = candidate_arcs[0]

    # arc = high_arc

    # y_value = arc.getYValueForXValue(x_value, l_y)

    y_value = high_arc.getYValueForXValue(x_value, l_y)

    location = (x_value, y_value)

    return location

"""

from arc_tree.Arc import *

arc_a = Arc([0, 4])

arc_b = Arc([1, 1])

l_y = 0.837

breakpoint = Breakpoint(arc_a, arc_b)

x_value = breakpoint.getXComponent(l_y)

print x_value

# print arc_a.getLeftIntersectionXValue(arc_b, l_y)

# print arc_a.getRightIntersectionXValue(arc_b, l_y)

# expect ~0.297

arc_a = Arc([1, 1])

arc_b = Arc([2, 3])

l_y = 0.837

breakpoint = Breakpoint(arc_a, arc_b)

x_value = breakpoint.getXComponent(l_y)

print x_value

# print arc_a.getLeftIntersectionXValue(arc_b, l_y)

# print arc_a.getRightIntersectionXValue(arc_b, l_y)

# expect ~1.58

"""

"""

# this is not a valid test; 
# describes invalid collection of arcs 
# for given sweep-line location

from arc_tree.Arc import *

arc_a = Arc([0, 4])

arc_b = Arc([2, 3])

l_y = 0.763

breakpoint = Breakpoint(arc_a, arc_b)

x_value = breakpoint.getXComponent(l_y)

print x_value

print arc_a.getLeftIntersectionXValue(arc_b, l_y)

print arc_a.getRightIntersectionXValue(arc_b, l_y)

# expect ~0.457

arc_a = Arc([2, 3])

arc_b = Arc([1, 1])

l_y = 0.763

breakpoint = Breakpoint(arc_a, arc_b)

x_value = breakpoint.getXComponent(l_y)

print x_value

print arc_a.getLeftIntersectionXValue(arc_b, l_y)

print arc_a.getRightIntersectionXValue(arc_b, l_y)

# expect ~0.069

"""


