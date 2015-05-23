from ..geometry.Bisector import *

from Util import *

class Site:

  # assume bisectors corresponding to three sites are non-degenerate

  # points is a list of three (x, y) tuples with x monotonically increasing

  @staticmethod

  def distanceFromLargestEmptyCircleCenterToSiteOnBoundary(points):

    point1 = points[0]

    point2 = points[1]

    point3 = points[2]

    bisector1 = Bisector(point1, point2)

    bisector2 = Bisector(point2, point3)

    intersection = bisector1.intersectWithBisector(bisector2)

    distance = getDistance(intersection, point1)

    return distance

