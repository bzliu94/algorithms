class Interval:

  # interval is [left, right]

  # note that endpoints are included

  def __init__(self, left, right):

    self.left = left

    self.right = right

  def getLeftEndpoint(self):

    return self.left

  def getRightEndpoint(self):

    return self.right

  def isEqualTo(self, i):

    left_endpoints_match = self.getLeftEndpoint() == i.getLeftEndpoint()

    right_endpoints_match = self.getRightEndpoint() == i.getRightEndpoint()

    return left_endpoints_match and right_endpoints_match
    
  def overlapsInterval(self, i):

    left_is_satisfactory = i.getLeftEndpoint() <= self.getRightEndpoint()

    right_is_satisfactory = i.getRightEndpoint() >= self.getLeftEndpoint()
    
    return left_is_satisfactory and right_is_satisfactory

  def toString(self):

    left_endpoint = self.getLeftEndpoint()

    right_endpoint = self.getRightEndpoint()

    result_str = "[" + str(left_endpoint) + ", " + str(right_endpoint) + "]"

    return result_str

