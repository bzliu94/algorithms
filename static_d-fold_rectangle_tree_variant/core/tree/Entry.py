class Entry:
  def __init__(self, key, value):
    self.key = key
    self.value = value
  def setKey(self, key):
    self.key = key
  def setValue(self, value):
    self.value = value
  def getKey(self):
    return self.key
  def getValue(self):
    return self.value
  def toString(self):
    return "(" + str(self.getKey()) + ", " + str(self.getValue()) + ")"
  def toKeyString(self):
    return str(self.getKey())
