# constrained version of a line

from Line import *

class LineSegment:

  # valid parameter values are those in interval [t.a, t.b]

  # note that the endpoints are included

  def __init__(self, point_a, point_b):

    self.point_a = point_a

    self.point_b = point_b

    line = Line.construct(point_a, point_b)

    self.line = line

  def getPointA(self):

    return self.point_a

  def getPointB(self):

    return self.point_b

  def _getLine(self):

    return self.line

  def getMidpoint(self):

    point_a = self.getPointA()

    point_b = self.getPointB()

    return LineSegment.getLineSegmentMidpoint(point_a, point_b)

  @staticmethod

  def getLineSegmentMidpoint(point_a, point_b):

    """

    point_a = self.getPointA()

    point_b = self.getPointB()

    """

    x = (point_a[0] + point_b[0]) / 2.0

    y = (point_a[1] + point_b[1]) / 2.0

    midpoint = (x, y)

    return midpoint

  def getDirectionVector(self):

    line = self._getLine()

    direction_vector = line.getDirectionVector()

    return direction_vector

"""

line_segment = LineSegment((0, 0), (1, 0))

print line_segment.getPointA()

print line_segment.getPointB()

"""


