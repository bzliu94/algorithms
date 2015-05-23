class SweepLine:

  def __init__(self, y = None):

    self.y = y

  def getY(self):

    # print "retrieving sweep-line y:", self.y

    return self.y

  def setY(self, y):

    self.y = y

    # print "setting sweep-line y:", y