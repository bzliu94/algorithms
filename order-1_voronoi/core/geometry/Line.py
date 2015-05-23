"""

getOffsetVector(self)

getDirectionVector(self)

setOffsetVector(self, vector)

setDirectionVector(self, vector)

normalize(vec)

intersectWithLine(self, line)
  
doesIntersectWithLine(self, line)

_getLinePointIntersectionMatrix(line, point)

_getLineLineIntersectionMatrix(line1, line2)

isOnLine(self, point, tolerance = 0.001)

rotateVectorNinetyDegreesCCW(vector)

getClosestPointOnLine(self, point)

getParameterValue(self, point)

"""

# a line

# abstract class

import math

from ..matrix_math.Matrix2x2 import *

from Line import *

from core.Util import *

class Line:

  # t = 0 corresponds to provided offset vector

  """

  def __init__(self, offset_vector, direction_vector):
  
    self.offset_vector = offset_vector

    normalized_direction_vector = Line.normalize(direction_vector)
    
    self.direction_vector = normalized_direction_vector

  """

  def __init__(self, offset_vector, direction_vector):

    self.offset_vector = offset_vector

    # print direction_vector, normalized_direction_vector
    
    self.direction_vector = direction_vector

  # t = 0 corresponds to vector associated with point a

  # direction vector is by default normalized

  @staticmethod

  def construct(point_a, point_b):

    # print point_a, point_b

    offset_vector = point_a

    x_a, y_a = point_a

    x_b, y_b = point_b

    delta_y = y_b - y_a

    delta_x = x_b - x_a

    direction_vector = (delta_x, delta_y)

    normalized_direction_vector = Line.normalize(direction_vector)

    # print "normalized direction vector:", normalized_direction_vector

    return Line(offset_vector, normalized_direction_vector)

  """

  def getPointA(self):

    return self.point_a

  def getPointB(self):

    return self.point_b

  def setPointA(self, point_a):

    self.point_a = point_a

  def setPointB(self, point_b):

    self.point_b = point_b

  """

  def getOffsetVector(self):

    return self.offset_vector

  def getDirectionVector(self):

    return self.direction_vector

  def setOffsetVector(self, vector):

    self.offset_vector = vector

  def setDirectionVector(self, vector):

    self.direction_vector = vector

  # assume that vec is a (x, y) tuple

  @staticmethod

  def normalize(vec):

    # print vec

    (vec_x, vec_y) = vec

    magnitude = math.sqrt(vec_x ** 2.0 + vec_y ** 2.0)

    result_vec = ((1.0 * vec_x) / magnitude, (1.0 * vec_y) / magnitude)

    return result_vec
    
  # assume that an intersection exists
  
  # we assume the lines are not identical
    
  def intersectWithLine(self, line):
  
    offset_vec1 = self.getOffsetVector()

    direction_vec1 = self.getDirectionVector()

    offset_vec2 = line.getOffsetVector()

    direction_vec2 = line.getDirectionVector()
  
    m = Line._getLineLineIntersectionMatrix(self, line)

    # invert a (2 x 2) matrix

    m_inv = m.getInverse()

    # print m_inv.getA(), m_inv.getB(), m_inv.getC(), m_inv.getD()

    b_x = offset_vec2[0] - offset_vec1[0]

    b_y = offset_vec2[1] - offset_vec1[1]

    t1 = m_inv.getA() * b_x + m_inv.getB() * b_y

    t2 = m_inv.getC() * b_x + m_inv.getD() * b_y

    intersection_x = direction_vec1[0] * t1 + offset_vec1[0]

    intersection_y = direction_vec1[1] * t1 + offset_vec1[1]

    # print t1, intersection_x, intersection_y

    return (intersection_x, intersection_y)
  
  def doesIntersectWithLine(self, line):
  
    m = Line._getLineLineIntersectionMatrix(self, line)

    det = m.getDeterminant()

    unique_solution_exists = det != 0

    return unique_solution_exists

  @staticmethod

  def _getLinePointIntersectionMatrix(line, point):

    # find implicit formula for line

    # a * x + b * y + c = 0

    offset_vec1 = line.getOffsetVector()

    direction_vec1 = line.getDirectionVector()

    offset_vec2 = point

    direction_vec2 = (0, 0)

    a = direction_vec1[0]

    b = -1.0 * direction_vec2[0]

    c = direction_vec1[1]

    d = -1.0 * direction_vec2[1]

    m = Matrix2x2(a, b, c, d)

    return m

  # retrieve a 2 x 2 matrix

  # in particular, retrieving M in M * t = b

  # free variable for column 0 is t1, the parameter for the first line

  # free variable for column 1 is t2, the parameter for the second line
  
  @staticmethod

  def _getLineLineIntersectionMatrix(line1, line2):

    # find implicit formula for line

    # a * x + b * y + c = 0

    offset_vec1 = line1.getOffsetVector()

    direction_vec1 = line1.getDirectionVector()

    offset_vec2 = line2.getOffsetVector()

    direction_vec2 = line2.getDirectionVector()

    # s1 = m1 * t1 + b1

    # s2 = m2 * t2 + b2

    # m1 * t1 + b1 = m2 * t2 + b2

    # => m1 * t1 + (-1 * m2) * t2 = b2 - b1

    # => M * t = b

    # => t = (M ^ -1) * b

    # a = m1.x, b = -m2.x, c = m1.y, d = -m2.y

    # b.x = b2.x - b1.x

    # b.y = b2.y - b1.y

    a = direction_vec1[0]

    b = -1.0 * direction_vec2[0]

    c = direction_vec1[1]

    d = -1.0 * direction_vec2[1]

    m = Matrix2x2(a, b, c, d)

    # print m.getA(), m.getB(), m.getC(), m.getD()

    return m

  # tolerance value corresponding 
  #   to three places to right of decimal point 
  #   for purpose of aiming for 
  #   (axis-aligned) component values 
  #   that are precise 
  #   to three places to right of decimal point

  # deal with point closest to line, 
  #   assuming it is within a distance 
  #   equal to value of tolerance

  # deal with tolerance of .01 for parameter

  def isOnLine(self, point, tolerance = 0.01):

    # find closest point on line 
    #   and see if we are within tolerance

    """

    x_value = point[0]

    y_value = point[1]

    parameter_value = self._getParameterValueForYValue(y_value)

    found_x_value = self._getXValueForParameterValue(parameter_value)

    x_values_match = (found_x_value <= (x_value + tolerance)) and \
                       (found_x_value >= (x_value - tolerance))

    return x_values_match

    """

    closest_point = self.getClosestPointOnLine(point)

    distance = getDistance(point, closest_point)

    # print "distance:", distance

    is_on_line = distance <= tolerance

    return is_on_line

  @staticmethod

  def rotateVectorNinetyDegreesCCW(vector):

    # rotate vector ninety degrees in counter-clockwise direction

    y_component = vector[1]

    x_component = vector[0]

    rotated_vector = (-1 * y_component, x_component)

    return rotated_vector

  def getClosestPointOnLine(self, point):

    offset_vector = self.getOffsetVector()

    direction_vector = self.getDirectionVector()

    curr_offset_vector = point

    curr_direction_vector = Line.rotateVectorNinetyDegreesCCW(direction_vector)

    line = self

    curr_line = Line(curr_offset_vector, curr_direction_vector)

    intersection_point = line.intersectWithLine(curr_line)

    # print offset_vector, direction_vector

    # print curr_offset_vector, curr_direction_vector

    # print intersection_point

    return intersection_point

  # get parameter value for a point on the line

  # assume we are "exactly" on the line

  def getParameterValue(self, point):

    """

    is_on_line == self.isOnLine(point)

    if is_on_line == False:

      raise Exception("is not on line")

    else:

      y_value = point[1]

      parameter_value = self._getParameterValueForYValue(y_value)

      return parameter_value

    """

    # s1 = m1 * t1 + b1

    # s2 = m2 * t2 + b2, s.t. m2 = 0

    # m1 * t1 + b1 = m2 * t2 + b2

    # => m1 * t1 + (-1 * m2) * t2 = b2 - b1

    # => M * t = b

    # => t = (M ^ -1) * b

    # a = m1.x, b = -m2.x, c = m1.y, d = -m2.y

    # b.x = b2.x - b1.x

    # b.y = b2.y - b1.y

    # determinant is zero 
    #   does not mean we cannot invert

    offset_vec1 = self.getOffsetVector()

    direction_vec1 = self.getDirectionVector()

    offset_vec2 = point

    direction_vec2 = (0, 0)

    line = self

    v_o_x, v_o_y = offset_vec1

    v_d_x, v_d_y = direction_vec1

    x, y = point

    t = None

    # print offset_vec1

    # print direction_vec1

    # solve for t using x if line is not vertical

    # x = v_d.x * t + v_o.x

    # t = (x - v_o.x) / v_d.x

    if v_d_x != 0:

      # print "case 1"

      t = (x - 1.0 * v_o_x) / (1.0 * v_d_x)

      # print t, x, v_o_x, v_d_x

    # solve for t using y if line is vertical

    # y = v_d.y * t + v_o.y

    # t = (y - v_o.y) / v_d.y

    if v_d_x == 0:

      # print "case 2"

      t = (y - 1.0 * v_o_y) / (1.0 * v_d_y)

    return t

    """

    m = Line._getLinePointIntersectionMatrix(line, point)

    # invert a (2 x 2) matrix

    m_inv = m.getInverse()

    # print m_inv.getA(), m_inv.getB(), m_inv.getC(), m_inv.getD()

    b_x = offset_vec2[0] - offset_vec1[0]

    b_y = offset_vec2[1] - offset_vec1[1]

    t1 = m_inv.getA() * b_x + m_inv.getB() * b_y

    t2 = m_inv.getC() * b_x + m_inv.getD() * b_y

    intersection_x = direction_vec1[0] * t1 + offset_vec1[0]

    intersection_y = direction_vec1[1] * t1 + offset_vec1[1]

    # print t1, intersection_x, intersection_y

    """

  """

  # assume we are "exactly" on the line

  def _getParameterValueForYValue(self, y_value):

    y = 1.0 * point[1]

    # y = v_d.y * t + v_o.y

    # => t = (y - v_o.y) / v_d.y

    offset_vector = self.getOffsetVector()

    direction_vector = self.getDirectionVector()

    offset_vector_y = offset_vector[1]

    direction_vector_y = direction_vector[1]

    t = (y - offset_vector_y) / (1.0 * direction_offset_vector_y)

    return t

  # assume we are "exactly" on the line

  def _getXValueForParameterValue(self, parameter_value):

    # x = v_d.x * t + v_o.x

    offset_vector = self.getOffsetVector()

    direction_vector = self.getDirectionVector()

    offset_vector_x = offset_vector[0]

    direction_vector_x = direction_vector[0]

    x = direction_vector * parameter_value + offset_vector_x

    return x

  """

"""

line = Line((1, 2), (2, 3))

print line.getDirectionVector()

print line.getOffsetVector()

"""

"""

line1 = Line((0, -5), (0, 5))

line2 = Line((-5, 0), (5, 0))

print line1.intersectWithLine(line2)

"""

"""

line1 = Line.construct((0, 0), (5, 5))

line2 = Line.construct((5, 0), (1.25, 3.75))

print line1.getOffsetVector()

print line2.getOffsetVector()

direction_vector1 = line1.getDirectionVector()

direction_vector2 = line2.getDirectionVector()

x, y = direction_vector1

inverted_direction_vector1 = (-x, -y)

line1.setDirectionVector(inverted_direction_vector1)

print line1.getDirectionVector()

line1.setDirectionVector(direction_vector1)

line2.setOffsetVector((3.75, 1.25))

print line2.getOffsetVector()

print Line.normalize((5, 5))

print line1.intersectWithLine(line2)

print line1.doesIntersectWithLine(line2)

line3 = Line.construct((0, -1), (5, 4))

print line1.doesIntersectWithLine(line3)

# _getLinePointIntersectionMatrix(line, point)

# _getLineLineIntersectionMatrix(line1, line2)

point1 = (1.25, 1.25)

point2 = (1.25001, 1.25)

print line1.isOnLine(point1, 0.001)

print line2.isOnLine(point1, 0.001)

print line1.isOnLine(point2, 0.001)

print Line.rotateVectorNinetyDegreesCCW((3, 0))

point3 = (5, 0)

print line1.getOffsetVector(), line1.getDirectionVector()

# print "closest point:", line1.getClosestPointOnLine(point3)

print line1.getClosestPointOnLine(point3)

print line1.getParameterValue((0, 0))

print line1.getParameterValue((5, 5))

print line1.getParameterValue((2.5, 2.5))

line4 = Line.construct((0, 0), (0, 1))

print line4.getParameterValue((0, 2))

"""


