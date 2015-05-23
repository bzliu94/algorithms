class ArcPayload:

  # a circle event may not yet exist 
  # that is associated with a particular arc

  # def __init__(self, circle_event = None, event_priority = None):

  def __init__(self, circle_event = None):
  
    self.circle_event = circle_event

    # self.event_priority = event_priority
    
  # if no associated circle event, 
  #   can return None
    
  def getCircleEvent(self):
  
    return self.circle_event
    
  # if no associated circle event, 
  #   can accept None as an argument
    
  def setCircleEvent(self, circle_event):
  
    self.circle_event = circle_event
    
  def removeCircleEvent(self):
  
    self.setCircleEvent(None)

  def hasCircleEvent(self):
  
    return self.getCircleEvent() != None

  """

  def getEventPriority(self):

    return self.event_priority

  def setEventPriority(self, event_priority):

    self.event_priority = event_priority

  """

