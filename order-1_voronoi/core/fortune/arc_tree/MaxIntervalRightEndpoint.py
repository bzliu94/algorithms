class MaxIntervalRightEndpoint:

  """

  def __init__(self, entry):

    self.entry = entry

  def _getEntry(self):

    return self.entry

  def _setEntry(self, entry):

    self.entry = entry

  def getValue(self):

    entry = self._getEntry()

    interval = entry.getKey()

    right_endpoint = interval.getRightEndpoint()

    return right_endpoint

  """

  def __init__(self, value):

    self.value = value

    self.responsible_interval = None

  def getValue(self):

    return self.value

  def setValue(self, value):

    self.value = value

  def setResponsibleInterval(self, responsible_interval):

    # print "responsible interval being set:", responsible_interval

    self.responsible_interval = responsible_interval

  # may return None

  def getResponsibleInterval(self):

    # print "responsible interval being retrieved:", self.responsible_interval

    return self.responsible_interval


