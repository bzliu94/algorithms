# augmented vertex

class Vertex:

  def __init__(self, element, location):

    self.element = element

    self.location = location

  def getElement(self):

    return self.element

  def setElement(self, element):

    self.element = element

  def getLocation(self):

    return self.location

  def setLocation(self, location):

    self.location = location

  def isIndeterminate(self):

    return False

  def toString(self):

    return str(self.location)

