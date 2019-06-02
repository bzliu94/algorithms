# 2019-06-01

# we implement simplevrb from georgiadis et al. 2015

# running time is O(m * n * alpha), assuming use of standard DSU structure

from fgib_tarjan import Vertex, Edge
from sap_italiano import doStrongArticulationPoints
from scc_ks import SCC_KS
from collections import defaultdict

def doSimpleVRB(V, E):
  # step one
  s = V[0]
  saps = doStrongArticulationPoints(V, E, s)
  # step two
  curr_blocks = [V[ : ]]
  # step three
  n = len(V)
  g_vertex_to_number_dict = {}
  number_to_g_vertex_dict = {}
  for i in xrange(len(V)):
    g_vertex = V[i]
    g_vertex_to_number_dict[g_vertex] = i
    number_to_g_vertex_dict[i] = g_vertex
  # step 3.1
  for curr_sap in saps:
    adj = defaultdict(lambda: [])
    for g_edge in E:
      origin = g_edge.getOrigin()
      destination = g_edge.getDestination()
      if origin == curr_sap or destination == curr_sap:
        continue
      origin_num = g_vertex_to_number_dict[origin]
      destination_num = g_vertex_to_number_dict[destination]
      adj[origin_num].append(destination_num)
    scc_ks = SCC_KS(n, adj)
    components = scc_ks.scc()
    next_components = []
    for component in components:
      next_component = [number_to_g_vertex_dict[x] for x in component]
      next_components.append(next_component)
    # step 3.2
    next_blocks = []
    label_num_to_component_dict = defaultdict(lambda: [])
    vertex_to_label_num_dict = {}
    for i in xrange(len(next_components)):
      label_num = i
      curr_next_component = next_components[i]
      label_num_to_component_dict[label_num] = curr_next_component
      curr_vertices = curr_next_component
      for curr_vertex in curr_vertices:
        vertex_to_label_num_dict[curr_vertex] = label_num
    for curr_block in curr_blocks:
      label_num_to_vertices_dict = defaultdict(lambda: [])
      for curr_vertex in curr_block:
        curr_label_num = vertex_to_label_num_dict[curr_vertex]
        label_num_to_vertices_dict[curr_label_num].append(curr_vertex)
      # have modified refine
      do_include_sap = curr_sap in curr_block
      for curr_group in label_num_to_vertices_dict.values():
        next_curr_group = curr_group[ : ]
        if do_include_sap == True:
          if curr_sap not in next_curr_group:
            next_curr_group.append(curr_sap)
        if len(next_curr_group) >= 2:
          next_blocks.append(next_curr_group)
    curr_blocks = next_blocks
  return curr_blocks

if __name__ == '__main__':

  """

  v1 = Vertex(1)
  v2 = Vertex(2)

  vertices = [v1, v2]

  e1 = Edge(v1, v2)
  e2 = Edge(v2, v1)

  edges = [e1, e2]

  result = doSimpleVRB(vertices, edges)
  print result

  """

  # example from figures one and two in georgiadis et al. 2015

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

  # (expect blocks of [A, B, C], [C, D, E, F], [F, H], [H, I, J, L])

  blocks = doSimpleVRB(vertices, edges)

  for i in xrange(len(blocks)):
    block = blocks[i]
    print "block", i, ":", [x.toString() for x in block]


