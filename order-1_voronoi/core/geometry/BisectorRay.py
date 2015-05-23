# constrained version of a particular type of line

# has direction

from Bisector import *

from Ray import *

# class BisectorRay(Ray, Bisector):

class BisectorRay(Ray):

  # create a bisector ray 
  #   without explicitly specifying a base; 
  #   use midpoint of line segment 
  #   from point a to point b as base

  @staticmethod

  def construct(point_a, point_b):

    base = LineSegment.getLineSegmentMidpoint(point_a, point_b)

    bisector_ray = BisectorRay(point_a, point_b, base)

    return bisector_ray

  # valid parameter values are those greater than or equal to zero

  # bisector ray points in direction 
  #   ninety degrees CCW of line segment 
  #   from point a to point b

  # assume that base is on line to a certain amount of precision

  def __init__(self, point_a, point_b, base):

    bisector = Bisector.construct(point_a, point_b)

    # print bisector.isOnLine(base)

    if bisector.isOnLine(base) == False:

      # print point_a, point_b, base

      raise Exception("base is not on line corresponding to bisector ray")

    direction_vector = bisector.getDirectionVector()

    Ray.__init__(self, base, direction_vector)

    self.bisector = bisector

  """

  def doesIntersectWithRay(self, ray):

    pass

  def intersectWithRay(self, ray):

    pass

  """

"""

bisector_ray = BisectorRay((0, 0), (1, 0), (0.5, 0))

print bisector_ray.getBase()

print bisector_ray.getDirectionVector()

"""

"""

bisector_ray1 = BisectorRay((0, 0), (1, 0), (0.5, 0))

bisector_ray2 = BisectorRay((1, 0), (2, 1), LineSegment.getLineSegmentMidpoint((1, 0), (2, 1)))

bisector_ray3 = BisectorRay((2, 1), (1, 0), LineSegment.getLineSegmentMidpoint((1, 0), (2, 1)))

print bisector_ray1.doesIntersectWithRay(bisector_ray2)

print bisector_ray1.intersectWithRay(bisector_ray2)

print bisector_ray1.doesIntersectWithRay(bisector_ray3)

"""

"""

bisector_ray1 = BisectorRay((0, 0), (1, 0), (0.5, 0))

bisector_ray2 = BisectorRay.construct((1, 0), (2, 1))

print bisector_ray1.intersectWithRay(bisector_ray2)

"""


