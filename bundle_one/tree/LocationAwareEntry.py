from Entry import *
class LocationAwareEntry(Entry):
  def __init__(self, key, value, location = None):
    Entry.__init__(self, key, value)
    self.location = location
  def setLocation(self, location):
    self.location = location
  def getLocation(self):
    return self.location
