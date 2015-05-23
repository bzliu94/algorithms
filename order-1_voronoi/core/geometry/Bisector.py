from Line import *

from LineSegment import *

# a particular type of line

# has direction

# abstract class

# points ninety degrees CCW of line segment from point a to point b

class Bisector(Line):

  @staticmethod

  def construct(point_a, point_b):

    line_segment = LineSegment(point_a, point_b)

    line_segment_direction_vector = line_segment.getDirectionVector()

    offset_vector = line_segment.getMidpoint()

    direction_vector = Line.rotateVectorNinetyDegreesCCW(line_segment_direction_vector)

    bisector = Bisector(point_a, point_b, offset_vector, direction_vector)

    return bisector

  def __init__(self, point_a, point_b, offset_vector, direction_vector):

    Line.__init__(self, offset_vector, direction_vector)

    self.point_a = point_a

    self.point_b = point_b

  def getPointA(self):

    return self.point_a

  def getPointB(self):

    return self.point_b

"""

# vertical line with x = 5

bisector1 = Bisector.construct((0, 0), (10, 0))

print bisector1.getPointA(), bisector1.getPointB()

# horizontal line with y = 0

bisector2 = Bisector.construct((5, 10), (5, -10))

print bisector1.intersectWithLine(bisector2)

"""

"""

# a vertical line with x = 78

bisector1 = Bisector.construct((70, 100), (86, 100))

# a diagonal line pointing to upper left

bisector2 = Bisector.construct((86, 100), (79, 93))

location = bisector1.intersectWithLine(bisector2)

print location

"""

"""

bisector1 = Bisector.construct((298, 366), (299, 366))

bisector2 = Bisector.construct((299, 366), (307, 268))

location = bisector1.intersectWithLine(bisector2)

print location

"""


