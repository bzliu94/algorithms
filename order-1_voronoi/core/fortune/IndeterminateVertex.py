from ..graph.Vertex import *

class IndeterminateVertex(Vertex):

  def __init__(self):
  
    Vertex.__init__(self, None, None)

  def isIndeterminate(self):

    return True

  def toString(self):

    result_string = "v_inf"

    return result_string

  # arbitrarily choose location to be None

  def getLocation(self):

    return None

