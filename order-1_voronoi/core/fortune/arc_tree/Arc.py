# from BeachLineItem import *

import math

# class Arc(BeachLineItem):

class Arc:

  # focus is a (x, y) pair

  # def __init__(self, focus, arc_tree):

  """

  def __init__(self, focus, insert_l_y):

    self.focus = focus

    # self.arc_tree = arc_tree

    self.insert_l_y = insert_l_y

  """

  # def __init__(self, focus, arc_tree, is_split_residue_arc = False):

  def __init__(self, focus, is_split_residue_arc = False):

    self.focus = focus

    # self.arc_tree = arc_tree

    self.is_split_residue_arc = is_split_residue_arc

  """

  def getInsertSweepLineY(self):

    return self.insert_l_y

  def setInsertSweepLineY(self, insert_l_y):

    self.insert_l_y = insert_l_y

  """

  def getIsSplitResidueArc(self):

    return self.is_split_residue_arc

  def setIsSplitResidueArc(self, is_split_residue_arc):

    self.is_split_residue_arc = is_split_residue_arc

  def getFocus(self):

    return self.focus

  """

  def _getArcTree(self):

    return self.arc_tree

  """

  """

  # assume two parabolas are not degenerate

  # assume two roots exist

  """

  # have two parabolas s.t. zero or one are degenerate

  def getLeftIntersectionXValue(self, arc, l_y):

    values = self.getIntersectionXValues(arc, l_y)

    left_x_value = values[0]

    # print left_x_value

    return left_x_value

  # have two parabolas s.t. zero or one are degenerate

  def getRightIntersectionXValue(self, arc, l_y):

    values = self.getIntersectionXValues(arc, l_y)

    right_x_value = values[1]

    # print right_x_value

    return right_x_value

  """

  # note: could be a good idea 
  #   to make sure that method 
  #   supports having either 
  #   (i.e. lower or higher) 
  #   parabola or both 
  #   being degenerate

  # handle one case involving a degenerate parabola

  # in particular, we deal with a case 
  #   where we have a degenerate lower parabola

  """

  # handle case where we have one degenerate parabola

  # do not handle case where we have two degenerate parabolas
  
  # we consider scenarios that tend to involve 
  #   two parabolas that have 
  #   exactly two intersection points 
  #   (as opposed to zero, one, or infinite) 
  #   except in case of degenerate parabolas 
  #   (where we have one/two or infinite)
  
  # assume two arcs involved 
  #   have corresponding focuses 
  #   that do not have:
  #   x values that are identical 
  #     and y values that are identical

  # return list with left x value and right x value

  # have case where two parabolas have focuses at same y, 
  #   but they are not necessarily degenerate

  def getIntersectionXValues(self, arc, l_y):

    # consider case where lower arc 
    #   is a portion of a degenerate parabola

    # arc_tree = self._getArcTree()
    
    arcs = [self, arc]
    
    arc_focus_pairs = [(x, x.getFocus()) for x in arcs]
    
    y_values = [x[1][1] for x in arc_focus_pairs]
    
    min_y = min(y_values)
    
    candidate_low_arcs = [x[0] for x in arc_focus_pairs if x[1][1] == min_y]
    
    low_arc = candidate_low_arcs[0]
    
    low_arc_focus = low_arc.getFocus()
    
    low_arc_focus_x = low_arc_focus[0]
    
    low_arc_focus_y = low_arc_focus[1]

    # may have floating-point-related error for this comparison

    # low_arc_is_degenerate = low_arc_focus_y == l_y

    low_arc_is_degenerate = low_arc.isDegenerate(l_y)

    """

    print "values for determining whether low arc is degenerate:", low_arc_focus_y, l_y
    
    print abs(low_arc_focus_y - l_y)

    print low_arc_is_degenerate

    """

    # print low_arc_focus_y, l_y

    candidate_high_arcs = [x for x in arcs if x != low_arc]

    high_arc = candidate_high_arcs[0]
    
    high_arc_focus = high_arc.getFocus()
    
    high_arc_focus_x = high_arc_focus[0]
    
    high_arc_focus_y = high_arc_focus[1]

    # may have floating-point-related error for this comparison

    # high_arc_is_degenerate = high_arc_focus_y == l_y

    high_arc_is_degenerate = high_arc.isDegenerate(l_y)

    focus_i = self.getFocus()

    focus_j = arc.getFocus()

    """

    unadjusted_focus_i = self.getFocus()

    unadjusted_focus_j = arc.getFocus()

    # consider sweep-line y for purpose of addressing a floating-point-related issue

    focus_i = (unadjusted_focus_i[0], min(unadjusted_focus_i[1], l_y))

    focus_j = (unadjusted_focus_j[0], min(unadjusted_focus_j[1], l_y))

    """

    x_values = [x[1][0] for x in arc_focus_pairs]

    min_x_value = min(x_values)

    candidate_left_arcs = [x[0] for x in arc_focus_pairs if x[1][0] == min_x_value]

    left_arc = candidate_left_arcs[0]

    candidate_right_arcs = [x for x in arcs if x != left_arc]

    right_arc = candidate_right_arcs[0]

    left_arc_is_degenerate = left_arc.isDegenerate(l_y)

    right_arc_is_degenerate = right_arc.isDegenerate(l_y)

    """

    print "low arc is degenerate:", low_arc_is_degenerate

    print "high arc is degenerate:", high_arc_is_degenerate

    print "low arc focus:", low_arc.getFocus()

    print "high arc focus:", high_arc.getFocus()

    """

    if left_arc_is_degenerate == True and right_arc_is_degenerate == True:

      raise Exception("handling two arcs with same focus y-value that are currently degenerate")
    
    if low_arc_is_degenerate == True and high_arc_is_degenerate == False:
    
      x_value = low_arc_focus_x
      
      return [x_value, x_value]

    # if the two parabolas have focuses with same y, 
    #   either the parabolas are degenerate or 
    #   we have one intersection point

    # assume that case where parabolas are degenerate 
    #   has already been handled

    if (low_arc_is_degenerate == False and high_arc_is_degenerate == False) and \
      (low_arc_focus_y == high_arc_focus_y):

      # raise Exception("handling two arcs with same focus y-value but that are not degenerate")

      alpha_i = 1.0 / (2.0 * (focus_i[1] - l_y))

      b_i = (-2.0 * focus_i[0]) * alpha_i

      c_i = (focus_i[0] ** 2.0 + focus_i[1] ** 2.0 - l_y ** 2.0) * alpha_i

      alpha_j = 1.0 / (2.0 * (focus_j[1] - l_y))

      b_j = (-2.0 * focus_j[0]) * alpha_j

      c_j = (focus_j[0] ** 2.0 + focus_j[1] ** 2.0 - l_y ** 2.0) * alpha_j

      b_r = b_j - b_i

      c_r = c_j - c_i

      x_value = -1 * c_r / b_r

      # we are aware that only one intersection point exists

      result = [x_value]

      return result

    # print low_arc_focus, l_y

    """

    print "focus 1:", focus_i

    print "focus 2:", focus_j

    print self == arc

    """

    # print l_y

    alpha_i = 1.0 / (2.0 * (focus_i[1] - l_y))

    # print alpha_i

    a_i = alpha_i

    b_i = (-2.0 * focus_i[0]) * alpha_i

    c_i = (focus_i[0] ** 2.0 + focus_i[1] ** 2.0 - l_y ** 2.0) * alpha_i

    # print alpha_j

    alpha_j = 1.0 / (2.0 * (focus_j[1] - l_y))

    a_j = alpha_j

    b_j = (-2.0 * focus_j[0]) * alpha_j

    c_j = (focus_j[0] ** 2.0 + focus_j[1] ** 2.0 - l_y ** 2.0) * alpha_j

    a_r = a_j - a_i

    # print a_r, a_j, a_i

    # print a_r

    b_r = b_j - b_i

    c_r = c_j - c_i

    # print self.getFocus(), arc.getFocus(), l_y

    """

    print self.getFocus(), arc.getFocus(), l_y

    print a_r, a_j, a_i

    print b_r, b_j, b_i

    print c_r, c_j, c_i

    """

    # making sure that determinant is at least zero, 
    #   because we assume that we have 
    #   at least one intersection 
    #   and to deal with floating-point issues

    determinant = max(b_r ** 2.0 - 4.0 * a_r * c_r, 0)

    # print "determinant:", determinant

    """

    # deal with floating-point-related issue 
    #   where we may have value for determinant 
    #   that is very small yet negative

    epsilon = 0.00000001

    if determinant < 0 and abs(determinant) >= epsilon:

      raise Exception()

    else:

      determinant = abs(determinant)

    """

    x1 = (-1.0 * b_r - math.sqrt(determinant)) / (2.0 * a_r)

    x2 = (-1.0 * b_r + math.sqrt(determinant)) / (2.0 * a_r)

    # print [x1, x2]

    # print b_r, determinant, a_r

    # return [x1, x2]

    lower_x_value = min(x1, x2)

    higher_x_value = max(x1, x2)

    x_values = [lower_x_value, higher_x_value]

    return x_values

  """

  def getRightIntersectionX(self, arc, l_y):

    pass

  """

  def isSizeZero(self, arc_tree):

    # arc_tree = self._getArcTree()

    arc = self

    arc_interval = arc_tree._getArcIntervalForArc(arc)

    result = arc_interval.isSizeZero()

    return result

  """

  # somewhat circular definition for whether an arc is degenerate

  def isDegenerate(self, l_y):

    arc_tree = self._getArcTree()

    arc_interval = arc_tree._getArcIntervalForArc(self)

    arc_interval_is_size_zero = arc_interval.isSizeZero()

    return arc_interval_is_size_zero

  """

  # care about x values

  # note that for a given positive change 
  #   in the quantity (focus y - sweep-line y), 
  #   change in x tends to be more

  # def isDegenerate(self, l_y):

  def isDegenerate(self, l_y, tolerance = 0.001):

    # test whether difference between sweep-line y-value 
    #   and y-component of focus for given arc 
    #   is within given tolerance value

    # measuring axis-aligned quantities

    # sweep_line = arc_tree.getSweepLine()

    # l_y = sweep_line.getY()

    focus = self.getFocus()

    focus_y_component = focus[1]

    if l_y > focus_y_component + tolerance:

      print l_y, focus_y_component

      raise Exception("arc will be concave down")

    # is_degenerate = focus_y_component == l_y

    # print l_y

    # asymmetric tolerance

    is_degenerate = (l_y <= (focus_y_component + tolerance)) \
                      and (l_y >= focus_y_component)

    """

    is_degenerate = (focus_y_component <= (l_y + tolerance)) \
                      and (focus_y_component >= (l_y - tolerance))

    """

    return is_degenerate

  def isArc(self):

    return True

  # should not use this method for an arc that is degenerate

  """

  # we note that an arc inserted 
  # when there are no arcs 
  # that already exist in arc tree 
  # technically ought to be degenerate, 
  # but we say that its left and right extents 
  # are minus infinity and positive infinity

  # assume that if we are degenerate, we have neighbors

  """

  # assume that focus y is greater than or equal to l_y

  def getYValueForXValue(self, x_value, l_y):

    focus = self.getFocus()

    focus_x, focus_y = focus

    if not (focus_y >= l_y):

      raise Exception("considering y for a curve corresponding to a site with y not at or above sweep-line")

    alpha = 1.0 / (2.0 * (focus_y - l_y))

    a = alpha

    b = (-2.0 * focus_x) * alpha

    c = (focus_x ** 2 + focus_y ** 2 - l_y ** 2) * alpha

    y = a * x_value ** 2 + b * x_value + c

    return y

  """

  # is size-zero at time of insert 
  #   and at that time is not degenerate

  def isSplitResidueArc(self, tolerance = 0.001):

    focus = self.getFocus()

    focus_y = focus[1]

    insert_l_y = self.getInsertSweepLineY()

    created_as_split_residue_arc = (focus_y <= (insert_l_y + tolerance)) \
                                     and (focus_y >= (insert_l_y - tolerance))

    return created_as_split_residue_arc

  """

  """

  # retrieve an (x, y) tuple

  def getBreakpointLocation(self, arc, l_y):

    pass

  """

"""

arc1 = Arc((10, 20))

arc2 = Arc((20, 15))

l_y = 12.5

print arc1.getLeftIntersectionXValue(arc2, l_y)

print arc1.getRightIntersectionXValue(arc2, l_y)

"""

"""

arc1 = Arc((10, 20))

print arc1.isArc()

print arc1.isSweepLineTouchingSlab()

"""

"""

print abs(-1.80143985095e+16)

print abs(-1.80143985095e+16) > 0.00000001

"""


