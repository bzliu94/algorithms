# 2019-06-01

# find strong articulation points for strongly connected digraph via italiano et al. 2012

# running time is O(|E| * alpha(|V|, |E|) assuming use of standard DSU structure

from fgib_tarjan import Vertex, Edge
from dt_fraczak_GD2_faster import GD
from scc_ks import SCC_KS
from collections import defaultdict

class ReversedEdge(Edge):
  def __init__(self, origin, destination, reference_edge):
    Edge.__init__(self, origin, destination)
    self.reference_edge = reference_edge
  def getReferenceEdge(self):
    return self.reference_edge

# graph has to be strongly connected

def doStrongArticulationPoints(V, E, s):

  # we test whether start node is a strong articulation point 
  # by removing it temporarily and telling whether SCC's change

  # count SCC's

  n1 = len(V)
  g_vertex_to_number_dict1 = {}
  number_to_g_vertex_dict1 = {}
  for i in xrange(n1):
    g_vertex = V[i]
    g_vertex_to_number_dict1[g_vertex] = i
    number_to_g_vertex_dict1[i] = g_vertex
  adj1 = defaultdict(lambda: [])
  for g_edge in E:
    origin = g_edge.getOrigin()
    destination = g_edge.getDestination()
    origin_num = g_vertex_to_number_dict1[origin]
    destination_num = g_vertex_to_number_dict1[destination]
    adj1[origin_num].append(destination_num)

  name_to_original_vertex_dict = {}
  for vertex in V:
    name_to_original_vertex_dict[vertex.getName()] = vertex

  next_V = [x for x in V if x != s]
  n2 = len(next_V)
  g_vertex_to_number_dict2 = {}
  number_to_g_vertex_dict2 = {}
  for i in xrange(n2):
    g_vertex = next_V[i]
    g_vertex_to_number_dict2[g_vertex] = i
    number_to_g_vertex_dict2[i] = g_vertex
  adj2 = defaultdict(lambda: [])
  for g_edge in E:
    origin = g_edge.getOrigin()
    destination = g_edge.getDestination()
    if origin == s or destination == s:
      continue
    origin_num = g_vertex_to_number_dict2[origin]
    destination_num = g_vertex_to_number_dict2[destination]
    adj2[origin_num].append(destination_num)

  scc_ks1 = SCC_KS(n1, adj1)
  components1 = scc_ks1.scc()

  scc_ks2 = SCC_KS(n2, adj2)
  components2 = scc_ks2.scc()

  s_is_sap = None
  if len(components2) > len(components1):
    s_is_sap = True
  else:
    s_is_sap = False

  # start vertex s and target node v are trivial dominators for node v

  # forward direction

  dt1 = GD(V, E, s)

  forward_sap_set = set([])
  for curr_child, curr_parent in dt1.items():
    if curr_parent.getName() != s.getName():
      forward_sap_set |= set([curr_parent])

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

  dt2 = GD(next_V, next_E, next_s)

  reverse_sap_set = set([])

  for curr_child, curr_parent in dt2.items():
    if curr_parent.getName() != next_s.getName():
      reverse_sap_set |= set([curr_parent])

  next_reverse_sap_set = set([name_to_original_vertex_dict[x.getName()] for x in list(reverse_sap_set)])

  # combine results

  group1 = None
  if s_is_sap == True:
    group1 = [s]
  else:
    group1 = []

  result = list(set(group1) | forward_sap_set | next_reverse_sap_set)

  return result

if __name__ == '__main__':

  v1 = Vertex(1)
  v2 = Vertex(2)
  v3 = Vertex(3)
  v4 = Vertex(4)
  v5 = Vertex(5)
  v6 = Vertex(6)
  v7 = Vertex(7)

  # from italiano 2012 -- is best example

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

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16]

  # (expect sap's of nodes 3, 5)

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

  # (expect sap's of nodes 1, 2, 3, 4, 5, 6)

  """

  """

  # example from figure one in georgiadis et al. 2015

  v_A = Vertex("A")
  v_B = Vertex("B")
  v_C = Vertex("C")
  v_D = Vertex("D")
  v_E = Vertex("E")
  v_F = Vertex("F")
  v_H = Vertex("H")
  v_I = Vertex("I")
  v_J = Vertex("J")
  v_L = Vertex("L")

  vertices = [v_A, v_B, v_C, v_D, v_E, v_F, v_H, v_I, v_J, v_L]

  e1 = Edge(v_A, v_B)
  e2 = Edge(v_A, v_C)
  e3 = Edge(v_B, v_A)
  e4 = Edge(v_B, v_C)
  e5 = Edge(v_C, v_A)
  e6 = Edge(v_C, v_B)
  e7 = Edge(v_C, v_D)
  e8 = Edge(v_C, v_E)
  e9 = Edge(v_C, v_H)
  e10 = Edge(v_D, v_B)
  e11 = Edge(v_D, v_C)
  e12 = Edge(v_D, v_E)
  e13 = Edge(v_E, v_C)
  e14 = Edge(v_E, v_D)
  e15 = Edge(v_E, v_F)
  e16 = Edge(v_E, v_H)
  e17 = Edge(v_F, v_D)
  e18 = Edge(v_F, v_E)
  e19 = Edge(v_F, v_I)
  e20 = Edge(v_H, v_F)
  e21 = Edge(v_H, v_J)
  e22 = Edge(v_H, v_L)
  e23 = Edge(v_I, v_H)
  e24 = Edge(v_I, v_L)
  e25 = Edge(v_J, v_H)
  e26 = Edge(v_J, v_L)
  e27 = Edge(v_L, v_H)
  e28 = Edge(v_L, v_I)
  e29 = Edge(v_L, v_J)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29]

  # (expect sap's of nodes C, F, H)

  """

  sap_list = doStrongArticulationPoints(vertices, edges, v1)

  print [x.getName() for x in sap_list]


