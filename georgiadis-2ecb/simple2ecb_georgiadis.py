# 2019-05-20

# we have a bug s.t. we have unexpected behavior with SCC 
# if we use defaultdict collection with adjacency list input; 
# if we have a key associated an empty list that is non-explicit, 
# we may get different answer

# may erroneously give an answer if input graph is not strongly connected

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

  """

  # for lax boolean MM (old)

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

  """

  # for lax boolean MM

  v_S = Vertex("S")
  v_A = Vertex("A")
  v_B = Vertex("B")
  v_C = Vertex("C")
  v_D = Vertex("D")
  v_E = Vertex("E")
  v_F = Vertex("F")
  v_G = Vertex("G")
  v_H = Vertex("H")
  v_I = Vertex("I")
  v_J = Vertex("J")
  v_K = Vertex("K")
  v_L = Vertex("L")
  v_M = Vertex("M")
  v_N = Vertex("N")

  vertices = [v_S, v_A, v_B, v_C, v_D, v_E, v_F, v_G, v_H, v_I, v_J, v_K, v_L, v_M, v_N]

  e1 = Edge(v_S, v_A)
  e2 = Edge(v_S, v_B)
  e3 = Edge(v_A, v_S)
  e4 = Edge(v_A, v_C)
  e5 = Edge(v_A, v_D)
  e6 = Edge(v_B, v_A)
  e7 = Edge(v_C, v_D)
  e8 = Edge(v_D, v_E)
  e9 = Edge(v_E, v_F)
  e10 = Edge(v_E, v_H)
  e11 = Edge(v_F, v_G)
  e12 = Edge(v_F, v_I)
  e13 = Edge(v_G, v_E)
  e14 = Edge(v_G, v_J)
  e15 = Edge(v_G, v_K)
  e16 = Edge(v_H, v_G)
  e17 = Edge(v_I, v_G)
  e18 = Edge(v_J, v_K)
  e19 = Edge(v_K, v_H)
  e20 = Edge(v_K, v_J)
  e21 = Edge(v_K, v_L)
  e22 = Edge(v_L, v_M)
  e23 = Edge(v_L, v_N)
  e24 = Edge(v_M, v_F)
  e25 = Edge(v_M, v_N)
  e26 = Edge(v_N, v_B)
  e27 = Edge(v_N, v_M)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27]

  """

  # example from figure one in georgiadis et al. 2014

  v_A = Vertex("A")
  v_B = Vertex("B")
  v_C = Vertex("C")
  v_D = Vertex("D")
  v_E = Vertex("E")
  v_F = Vertex("F")
  v_H = Vertex("H")
  v_I = Vertex("I")
  v_J = Vertex("J")

  vertices = [v_A, v_B, v_C, v_D, v_E, v_F, v_H, v_I, v_J]

  e1 = Edge(v_A, v_B)
  e2 = Edge(v_B, v_A)
  e3 = Edge(v_B, v_E) # try removing this edge and see if J is still separated from all other nodes in a 2-edge-connected block
  e4 = Edge(v_C, v_A)
  e5 = Edge(v_C, v_B)
  e6 = Edge(v_C, v_D)
  e7 = Edge(v_C, v_E)
  e8 = Edge(v_D, v_C)
  e9 = Edge(v_D, v_E)
  e10 = Edge(v_E, v_C)
  e11 = Edge(v_E, v_D)
  e12 = Edge(v_E, v_J)
  e13 = Edge(v_E, v_I)
  e14 = Edge(v_F, v_D)
  e15 = Edge(v_F, v_J)
  e16 = Edge(v_H, v_F)
  e17 = Edge(v_H, v_I)
  e18 = Edge(v_I, v_E)
  e19 = Edge(v_I, v_H)
  e20 = Edge(v_I, v_J)
  e21 = Edge(v_J, v_E)
  e22 = Edge(v_J, v_F)
  e23 = Edge(v_J, v_I)

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23]

  """

  """

  # example from figure two in georgiadis et al. 2014

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

  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]

  """

  blocks = doSimple2ECB(vertices, edges)

  for i in xrange(len(blocks)):
    block = blocks[i]
    print "block", i, ":", [x.toString() for x in block]


