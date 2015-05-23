# from ...tree.Entry import *

from ...tree.LocationAwareEntry import *

class IntervalEntry(LocationAwareEntry):

  def __init__(self, key, value, location = None):

    LocationAwareEntry.__init__(self, key, value, location)

  def toString(self):

    location = self.getLocation()

    max_value = location.getMaxRightEndpoint().getValue()

    return "(" + self.toKeyString() + ", " + str(self.getValue()) + ", " + str(max_value) + ")"

  def toKeyString(self):

    return self.getKey().toString()

