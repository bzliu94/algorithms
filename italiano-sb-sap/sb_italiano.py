# 2019-03-28

# find strong bridges for strongly connected digraph via italiano et al. 2012

# only tree edges for a flow-graph can be bridges via tarjan 1976; 
# this means that if we have more than n - 1 edges, only n - 1 of them can be 
# bridges without considering reversal graph

# running time is O(|E| * alpha(|V|, |E|)) assuming use of standard DSU structure

from fgib_tarjan import Graph, Vertex, Edge, addDummyNode, prepareGraph, doIntervals, doBridges

class ReversedEdge(Edge):
  def __init__(self, origin, destination, reference_edge):
    Edge.__init__(self, origin, destination)
    self.reference_edge = reference_edge
  def getReferenceEdge(self):
    return self.reference_edge

# graph has to be strongly connected

def doStrongBridges(V, E, s):

  # s is different from a dummy node; flow-graph bridges must be filtered to remove dummy-related edges

  # forward direction	

  g1 = Graph()
  g1.addVertices(V)
  g1.addEdges(E)

  v_dummy1 = addDummyNode(g1, s)
  g1, t1, adj1 = prepareGraph(g1, v_dummy1)

  result1 = doIntervals(g1, t1, adj1, v_dummy1)
  curr_h1, curr_I1 = result1
  next_result1 = doBridges(g1, t1, adj1, curr_h1, curr_I1, v_dummy1)
  bridges1, x_result1, y_result1, l1, v_star1, w_star1 = next_result1

  dummy_name1 = v_dummy1.getName()

  next_bridges1 = []

  for bridge in bridges1:
    origin = bridge.getOrigin()
    dest = bridge.getDestination()
    o_name = origin.getName()
    d_name = dest.getName()
    if o_name != dummy_name1 and d_name != dummy_name1:
      next_bridges1.append(bridge)

  # reverse direction

  next_V = [Vertex(x.getName()) for x in V]
  name_to_next_vertex = {}
  for vertex in next_V:
    name = vertex.getName()
    name_to_next_vertex[name] = vertex
  next_E = []
  for edge in E:
    curr_origin = edge.getOrigin()
    curr_destination = edge.getDestination()
    next_origin = name_to_next_vertex[curr_origin.getName()]
    next_destination = name_to_next_vertex[curr_destination.getName()]
    reversed_edge = ReversedEdge(next_destination, next_origin, edge)
    next_E.append(reversed_edge)
  next_s = name_to_next_vertex[s.getName()]

  g2 = Graph()
  g2.addVertices(next_V)
  g2.addEdges(next_E)

  v_dummy2 = addDummyNode(g2, next_s)
  g2, t2, adj2 = prepareGraph(g2, v_dummy2)

  result2 = doIntervals(g2, t2, adj2, v_dummy2)
  curr_h2, curr_I2 = result2
  next_result2 = doBridges(g2, t2, adj2, curr_h2, curr_I2, v_dummy2)
  bridges2, x_result2, y_result2, l2, v_star2, w_star2 = next_result2

  dummy_name2 = v_dummy2.getName()

  next_bridges2 = []

  for bridge in bridges2:
    origin = bridge.getOrigin()
    dest = bridge.getDestination()
    o_name = origin.getName()
    d_name = dest.getName()
    if o_name != dummy_name2 and d_name != dummy_name2:
      next_bridges2.append(bridge)

  next_bridges2_original = [x.getReferenceEdge() for x in next_bridges2]

  # we take union

  result_strong_bridges = list(set(next_bridges1 + next_bridges2_original))

  return result_strong_bridges

if __name__ == '__main__':

  """

  # self-created

  v1 = Vertex(1)
  v2 = Vertex(2)

  vertices = [v1, v2]

  e1 = Edge(v1, v2)

  edges = [e1]

  """

  """

  # self-created

  v1 = Vertex(1)
  v2 = Vertex(2)
  v3 = Vertex(3)
  v4 = Vertex(4)
  v5 = Vertex(5)

  vertices = [v1, v2, v3, v4, v5]

  e1 = Edge(v1, v2)
  e2 = Edge(v2, v3)
  e3 = Edge(v1, v4)
  e4 = Edge(v4, v5)
  e5 = Edge(v5, v3)
  e6 = Edge(v3, v5)

  edges = [e1, e2, e3, e4, e5, e6]

  """

  """

  # self-created

  v1 = Vertex("A")
  v2 = Vertex("B")
  v3 = Vertex("C")
  v4 = Vertex("D")
  v5 = Vertex("E")
  v6 = Vertex("F")
  v7 = Vertex("G")

  vertices = [v1, v2, v3, v4, v5, v6, v7]

  e1 = Edge(v1, v2)
  e2 = Edge(v1, v6)
  e3 = Edge(v2, v3)
  e4 = Edge(v3, v4)
  e5 = Edge(v4, v5)
  e6 = Edge(v6, v7)
  e7 = Edge(v1, v3)
  e8 = Edge(v2, v1)
  e9 = Edge(v5, v2)
  e10 = Edge(v6, v4)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]

  # this can reveal problem with INTERVALS if we ignore updating destination for waking cross edges (though, not forward edges)

  """

  v1 = Vertex(1)
  v2 = Vertex(2)
  v3 = Vertex(3)
  v4 = Vertex(4)
  v5 = Vertex(5)
  v6 = Vertex(6)
  v7 = Vertex(7)

  # from italiano 2012 -- is best example

  """

  v1 = Vertex("A")
  v2 = Vertex("B")
  v3 = Vertex("C")
  v4 = Vertex("D")
  v5 = Vertex("E")
  v6 = Vertex("F")
  v7 = Vertex("G")

  """

  vertices = [v1, v2, v3, v4, v5, v6, v7]

  e1 = Edge(v1, v2)
  e2 = Edge(v1, v3)
  e3 = Edge(v2, v3)
  e4 = Edge(v3, v1)
  e5 = Edge(v3, v4)
  e6 = Edge(v3, v6)
  e7 = Edge(v3, v7)
  e8 = Edge(v4, v5)
  e9 = Edge(v5, v1)
  e10 = Edge(v5, v2)
  e11 = Edge(v5, v4)
  e12 = Edge(v5, v7)
  e13 = Edge(v6, v5)
  e14 = Edge(v6, v7)
  e15 = Edge(v7, v5)
  e16 = Edge(v7, v6)

  """

  e1 = Edge(v2, v1)
  e2 = Edge(v3, v1)
  e3 = Edge(v3, v2)
  e4 = Edge(v1, v3)
  e5 = Edge(v4, v3)
  e6 = Edge(v6, v3)
  e7 = Edge(v7, v3)
  e8 = Edge(v5, v4)
  e9 = Edge(v1, v5)
  e10 = Edge(v2, v5)
  e11 = Edge(v4, v5)
  e12 = Edge(v7, v5)
  e13 = Edge(v5, v6)
  e14 = Edge(v7, v6)
  e15 = Edge(v5, v7)
  e16 = Edge(v6, v7)

  """

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16]

  # (expect bridges of (B, C), (D, E))

  """

  # self-created

  v1 = Vertex(1)
  v2 = Vertex(2)
  v3 = Vertex(3)
  v4 = Vertex(4)

  vertices = [v1, v2, v3, v4]

  e1 = Edge(v1, v3)
  e2 = Edge(v1, v2)
  e3 = Edge(v2, v3)
  e4 = Edge(v3, v4)
  e5 = Edge(v4, v1)

  e1 = Edge(v3, v1)
  e2 = Edge(v2, v1)
  e3 = Edge(v3, v2)
  e4 = Edge(v4, v3)
  e5 = Edge(v1, v4)

  edges = [e1, e2, e3, e4, e5]

  # useful to determine if cross edges (v, w) have v < w (as it should) or if does not (signifying a bug w.r.t. RPO assumption)

  """

  """

  # from italiano 2012 and is one big cycle

  v1 = Vertex(1)
  v2 = Vertex(2)
  v3 = Vertex(3)
  v4 = Vertex(4)
  v5 = Vertex(5)
  v6 = Vertex(6)

  vertices = [v1, v2, v3, v4, v5, v6]

  e1 = Edge(v1, v2)
  e2 = Edge(v2, v3)
  e3 = Edge(v3, v4)
  e4 = Edge(v4, v5)
  e5 = Edge(v5, v6)
  e6 = Edge(v6, v1)

  e1 = Edge(v2, v1)
  e2 = Edge(v3, v2)
  e3 = Edge(v4, v3)
  e4 = Edge(v5, v4)
  e5 = Edge(v6, v5)
  e6 = Edge(v1, v6)

  edges = [e1, e2, e3, e4, e5, e6]

  """

  """

  # from georgiadis 2014 article

  v1 = Vertex(1)
  v2 = Vertex(2)
  v3 = Vertex(3)
  v4 = Vertex(4)
  v5 = Vertex(5)
  v6 = Vertex(6)
  v7 = Vertex(7)
  v8 = Vertex(8)

  vertices = [v1, v2, v3, v4, v5, v6, v7, v8]

  e1 = Edge(v1, v2)
  e2 = Edge(v1, v3)
  e3 = Edge(v2, v5)
  e4 = Edge(v3, v5)
  e5 = Edge(v4, v1)
  e6 = Edge(v5, v1)
  e7 = Edge(v5, v4)
  e8 = Edge(v5, v6)
  e9 = Edge(v5, v7)
  e10 = Edge(v5, v8)
  e11 = Edge(v6, v5)
  e12 = Edge(v6, v7)
  e13 = Edge(v7, v5)
  e14 = Edge(v7, v8)
  e15 = Edge(v8, v5)

  e1 = Edge(v2, v1)
  e2 = Edge(v3, v1)
  e3 = Edge(v5, v2)
  e4 = Edge(v5, v3)
  e5 = Edge(v1, v4)
  e6 = Edge(v1, v5)
  e7 = Edge(v4, v5)
  e8 = Edge(v6, v5)
  e9 = Edge(v7, v5)
  e10 = Edge(v8, v5)
  e11 = Edge(v5, v6)
  e12 = Edge(v7, v6)
  e13 = Edge(v5, v7)
  e14 = Edge(v8, v7)
  e15 = Edge(v5, v8)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]

  """

  """

  g = Graph()
  g.addVertices(vertices)
  g.addEdges(edges)
  # g._sortOriginToEdgesLists()

  v_dummy = addDummyNode(g, v1)
  g, t, adj = prepareGraph(g, v_dummy)

  next_vertices = g.getVertices()
  next_edges = g.getEdges()
  num_nodes = len(next_vertices)

  """

  """

  for edge in next_edges:
    print edge.toString(), edge.getEdgeTypeString()

  for vertex in next_vertices:
    curr_t_vertex = t.getVertexByName(vertex.getName())
    print "vertex:", curr_t_vertex.getName(), curr_t_vertex.getPreorderNumber()

  """

  """

  result = doIntervals(g, t, adj, v_dummy)
  curr_h, curr_I = result
  # print "I:", curr_I
  next_result = doBridges(g, t, adj, curr_h, curr_I, v_dummy)
  bridges, x_result, y_result, l, v_star, w_star = next_result

  dummy_name = v_dummy.getName()

  next_bridges = []

  for bridge in bridges:
    origin = bridge.getOrigin()
    dest = bridge.getDestination()
    o_name = origin.getName()
    d_name = dest.getName()
    if o_name != dummy_name and d_name != dummy_name:
      next_bridges.append(bridge)

  print [(x.getOrigin().getName(), x.getDestination().getName()) for x in next_bridges]

  """

  """

  # print curr_h

  # print x_result, y_result

  # print "v*:", [(x[0].toString(), x[1]) for x in v_star.items()]

  # print "w*:", [(x[0].toString(), x[1]) for x in w_star.items()]

  # print "l:", [(x[0].toString(), x[1]) for x in l.items()]

  """

  strong_bridges = doStrongBridges(vertices, edges, v1)

  print [x.toString() for x in strong_bridges]


