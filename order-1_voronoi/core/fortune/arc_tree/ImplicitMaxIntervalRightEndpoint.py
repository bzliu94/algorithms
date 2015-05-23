from MaxIntervalRightEndpoint import *

class ImplicitMaxIntervalRightEndpoint(MaxIntervalRightEndpoint):

  def __init__(self):

    MaxIntervalRightEndpoint.__init__(self, None)

  # overriding a method

  def getValue(self):

    # retrieve right endpoint of responsible interval

    interval = self.getResponsibleInterval()

    # print "responsible interval:", interval

    if interval == None:

      return None

    else:

      right_endpoint = interval.getRightEndpoint()

      return right_endpoint

  # overriding a method

  def setValue(self, value):

    pass

  """

  def setResponsibleInterval(self, responsible_interval):

    self.responsible_interval = responsible_interval

  # may return None

  def getResponsibleInterval(self):

    return self.responsible_interval

  """


