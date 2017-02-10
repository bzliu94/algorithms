class RectangleSegment:
  def __init__(self, x_interval, y_interval):
    self.x_interval = x_interval
    self.y_interval = y_interval
  def getXInterval(self):
    return self.x_interval
  def getYInterval(self):
    return self.y_interval
  def toString(self):
    x_interval = self.getXInterval()
    y_interval = self.getYInterval()
    result_str = str(x_interval) + " " + str(y_interval)
    return result_str
# rectangle_segment = RectangleSegment((0, 5), (6, 11))
# print rectangle_segment.toString()
