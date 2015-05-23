# undirected edge

class Edge:

  def __init__(self, vertex1, vertex2):

    self.vertex1 = vertex1

    self.vertex2 = vertex2

  def getFirstVertex(self):

    return self.vertex1

  def getSecondVertex(self):

    return self.vertex2

  def setFirstVertex(self, vertex):

    self.vertex1 = vertex

  def setSecondVertex(self, vertex):

    self.vertex2 = vertex

  def toString(self):

    vertex1_string = self.getFirstVertex().toString()

    vertex2_string = self.getSecondVertex().toString()

    result_string = "(" + vertex1_string + ", " + vertex2_string + ")"

    return result_string

