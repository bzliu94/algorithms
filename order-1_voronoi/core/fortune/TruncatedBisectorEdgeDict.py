from IndeterminateVertex import *

from ..geometry.Bisector import *

from ..graph.Edge import *

# edges are related to pairs of sites

class TruncatedBisectorEdgeDict:

  def __init__(self):

    # for edge additions, 
    # introduce one edge 
    # using an arbitrary site ordering

    # for edge retrievals, 
    # check for edges 
    # using two possible site orderings

    self.truncated_bisector_edges = {}
    
  # by default, both endpoints are indeterminate

  def addTruncatedBisectorEdge(self, site1, site2):

    vertex1 = IndeterminateVertex()

    vertex2 = IndeterminateVertex()

    edge = Edge(vertex1, vertex2)

    key = (site1, site2)

    (self.truncated_bisector_edges)[key] = edge

  # takes O(1) time on average

  def getTruncatedBisectorEdge(self, site1, site2):

    key1 = (site1, site2)

    key2 = (site2, site1)

    if key1 in self.truncated_bisector_edges:

      return (self.truncated_bisector_edges)[key1]

    elif key2 in self.truncated_bisector_edges:

      return (self.truncated_bisector_edges)[key2]

    else:

      # print site1, site2

      raise Exception("did not encounter a matching truncated bisector edge")

    """

    edge = (self.truncated_bisector_edges)[key]

    # (self.truncated_bisector_edges)[key2] = edge

    return edge

    """
    
  def hasTruncatedBisectorEdge(self, site1, site2):
  
    key1 = (site1, site2)

    key2 = (site2, site1)

    if key1 in self.truncated_bisector_edges:

      return True

    elif key2 in self.truncated_bisector_edges:

      return True

    else:

      return False

  # assume that at least one endpoint for edge 
  #   corresponding to two given sites is indeterminate
    
  def setIndeterminateEndpoint(self, site1, site2, vertex):
  
    edge = self.getTruncatedBisectorEdge(site1, site2)

    vertex1 = edge.getFirstVertex()

    vertex2 = edge.getSecondVertex()

    # print vertex.toString()

    if vertex1.isIndeterminate() == True:

      edge.setFirstVertex(vertex)

    elif vertex2.isIndeterminate() == True:

      edge.setSecondVertex(vertex)

    else:

      # print vertex.toString(), vertex1.toString(), vertex2.toString()

      # raise Exception("attempted to add a fixed endpoint to an edge with two fixed endpoints")

      pass

  # returns a list of Edge objects

  def getAllEdges(self):

    return (self.truncated_bisector_edges).values()

  @staticmethod

  def _isEdgeWithAnIndeterminateEndpoint(edge):

    first_vertex = edge.getFirstVertex()

    second_vertex = edge.getSecondVertex()

    first_vertex_is_indeterminate = first_vertex.isIndeterminate()

    second_vertex_is_indeterminate = second_vertex.isIndeterminate()

    result = first_vertex_is_indeterminate or second_vertex_is_indeterminate

    return result

  def getAllEdgesWithEndpointsThatAreNotIndeterminate(self):

    edges = self.getAllEdges()

    isQualifyingEdge = lambda x: not TruncatedBisectorEdgeDict._isEdgeWithAnIndeterminateEndpoint(x)

    result_edges = [x for x in edges if isQualifyingEdge(x) == True]
    
    return result_edges

  def getAllEdgesWithAnEndpointThatIsIndeterminate(self):

    edges = self.getAllEdges()

    isQualifyingEdge = lambda x: TruncatedBisectorEdgeDict._isEdgeWithAnIndeterminateEndpoint(x)

    result_edges = [x for x in edges if isQualifyingEdge(x) == True]

    return result_edges

