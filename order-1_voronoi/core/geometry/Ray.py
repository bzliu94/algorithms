# constrained version of a line

# has direction

from Line import *

class Ray:

  def __init__(self, base, direction_vector):

    self.base = base

    self.direction_vector = direction_vector

    self.line = Line(base, direction_vector)

  def getBase(self):

    return self.base

  def setBase(self, base):

    self.base = base

  def getDirectionVector(self):

    return self.direction_vector

  def setDirectionVector(self, direction_vector):

    self.direction_vector = direction_vector

  def _getLine(self):

    return self.line

  def doesIntersectWithRay(self, ray, parameter_tolerance = 0.01):

    line = self._getLine()

    curr_line = ray._getLine()

    lines_intersect = line.doesIntersectWithLine(curr_line)

    if lines_intersect == False:

      return False

    else:

      intersection_point = line.intersectWithLine(curr_line)

      t = line.getParameterValue(intersection_point)

      curr_t = curr_line.getParameterValue(intersection_point)

      # print "t and current t:", t, curr_t

      rays_intersect = t >= (-1 * parameter_tolerance) and curr_t >= (-1 * parameter_tolerance)

      return rays_intersect

  def intersectWithRay(self, ray):

    """

    if self.doesIntersectWithRay(ray) == False:

      raise Exception("rays do not intersect")

    """

    line = self._getLine()

    curr_line = ray._getLine()

    intersection_point = line.intersectWithLine(curr_line)

    return intersection_point

  def toString(self):

    base = self.getBase()

    direction_vector = self.getDirectionVector()

    result = str(base) + " " + str(direction_vector)

    return result

"""

ray1 = Ray((0, 0), (0, 1))

print ray1.getBase()

print ray1.getDirectionVector()

ray2 = Ray((1, 1), (-1, 0))

print ray1.doesIntersectWithRay(ray2)

print ray1.intersectWithRay(ray2)

"""


