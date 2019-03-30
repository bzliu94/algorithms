# 2019-03-29

# we implement simple2ecb from georgiadis et al. 2014

# we consider two-edge-connected blocks

# we show that the two-edge-connected blocks partition the input vertex collection: 
# (i) all sets are disjoint -- if two vertices are not two-edge-connected, 
# then a third vertex cannot be two-edge-connected to both; 
# (ii) each node is in a sense two-edge-connected to itself 
# and so we give each node a chance by introducing it 
# at least via a singleton set

# running time is O(|V| ^ 3 * alpha(|V|, |E|)) assuming use of standard DSU structure

from fgib_tarjan import Vertex, Edge

from sb_italiano import doStrongBridges

from scc_ks import SCC_KS

from collections import defaultdict

def doSimple2ECB(V, E):
  # step one
  s = V[0]
  strong_bridges = doStrongBridges(V, E, s)
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
  for curr_sb in strong_bridges:
    # step 3.1
    active_edges = [x for x in E if x != curr_sb]
    adj = defaultdict(lambda: [])
    for g_edge in active_edges:
      origin = g_edge.getOrigin()
      destination = g_edge.getDestination()
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
    for curr_2ecb in curr_blocks:
      for curr_scc in next_components:
        # do intersection
        intersection_vertex_list = list(set(curr_2ecb) & set(curr_scc))
        if len(intersection_vertex_list) != 0:
          next_blocks.append(intersection_vertex_list)
    curr_blocks = next_blocks
  return curr_blocks

if __name__ == '__main__':

  # for lax boolean MM

  L0 = Vertex(1)
  L1 = Vertex(2)
  L2 = Vertex(3)
  M0 = Vertex(4)
  M1 = Vertex(5)
  M2 = Vertex(6)
  R0 = Vertex(7)
  R1 = Vertex(8)
  R2 = Vertex(9)
  v_MC = Vertex(10)
  v_MS = Vertex(11)
  v_B = Vertex(12)
  v_SC = Vertex(13)
  v_SS = Vertex(14)
  v_UT = Vertex(15)
  v_LT = Vertex(16)

  vertices = [L0, L1, L2, M0, M1, M2, R0, R1, R2, v_MC, v_MS, v_B, v_SC, v_SS, v_UT, v_LT]

  e1 = Edge(L0, v_MS)
  e2 = Edge(L1, v_MS)
  e3 = Edge(L2, v_MS)
  e4 = Edge(M0, L0)
  e5 = Edge(M0, L1)
  e6 = Edge(M1, L0)
  e7 = Edge(M1, L1)
  e8 = Edge(M1, L2)
  e9 = Edge(R0, M1)
  e10 = Edge(R1, M0)
  e11 = Edge(R1, M1)
  e12 = Edge(R1, M2)
  e13 = Edge(v_MC, R0)
  e14 = Edge(v_MC, R1)
  e15 = Edge(v_MC, R2)
  e16 = Edge(v_MS, v_B)
  e17 = Edge(v_B, v_MC)
  e18 = Edge(L0, v_SS)
  e19 = Edge(L1, v_SS)
  e20 = Edge(L2, v_SS)
  e21 = Edge(v_LT, L0)
  e22 = Edge(v_LT, L1)
  e23 = Edge(v_LT, L2)
  e24 = Edge(M0, v_LT)
  e25 = Edge(M1, v_LT)
  e26 = Edge(M2, v_LT)
  e27 = Edge(v_UT, M0)
  e28 = Edge(v_UT, M1)
  e29 = Edge(v_UT, M2)
  e30 = Edge(R0, v_UT)
  e31 = Edge(R1, v_UT)
  e32 = Edge(R2, v_UT)
  e33 = Edge(v_SC, R0)
  e34 = Edge(v_SC, R1)
  e35 = Edge(v_SC, R2)
  e36 = Edge(v_SS, v_B)
  e37 = Edge(v_B, v_SC)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29, e30, e31, e32, e33, e34, e35, e36, e37]

  blocks = doSimple2ECB(vertices, edges)

  for i in xrange(len(blocks)):
    block = blocks[i]
    print "block", i, ":", [x.toString() for x in block]


