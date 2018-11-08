# 2018-11-08

# prim-jarnik mst algorithm for undirected connected graph

class PJVertex:
  def __init__(self, curr_id):
    self.curr_id = curr_id
  def getID(self):
    return self.curr_id
class PJEdge:
  def __init__(self, v_o, v_d, weight):
    self.v_o = v_o
    self.v_d = v_d
    self.weight = weight
  def getOriginVertex(self):
    return self.v_o
  def getDestinationVertex(self):
    return self.v_d
  def getWeight(self):
    return self.weight

from tree.DAryTree import *

from collections import defaultdict

from bundle_one.priority_queue.AdaptablePriorityQueue import AdaptablePriorityQueue

"""
binary heap with adjacency list OR fibonacci heap with adjacency list are two approaches that are used for prim's for mst that give good times but both are compatible with the idea that we don't have a clever approach for knowing how to handle adjacent vertices s.t. we can immediately skip those that are not in the priority queue anymore; further, in principle, either adjacency matrix or adjacency list could be better for different circumstances even with this lax stance towards adjacent vertex consideration
"""

# we assume V is non-empty

def doPrimJarnik(V, E):
  chosen_root_node = V[0]
  # handle adjacency "list"
  # possible sharing of list does not happen, so this is safe
  PJ_node_to_involved_PJ_edges = defaultdict(lambda: [])
  PJ_node_is_in_queue = defaultdict(lambda: False)
  for edge in E:
    v1 = edge.getOriginVertex()
    v2 = edge.getDestinationVertex()
    PJ_node_to_involved_PJ_edges[v1].append(edge)
    PJ_node_to_involved_PJ_edges[v2].append(edge)
  # deal with distances
  D = {}
  for curr_v in V:
    curr_d = None
    if curr_v == chosen_root_node:
      curr_d = 0
    else:
      curr_d = float("+inf")
    D[curr_v] = curr_d
  for curr_v in V:
    PJ_node_is_in_queue[curr_v] = True
  # deal with MST tree
  T = DAryTree()
  # deal with priority queue
  pq = AdaptablePriorityQueue()
  PJ_node_to_pq_entry_dict = {}
  for curr_v in V:
    curr_element = (curr_v, None)
    curr_key = D[curr_v]
    curr_pq_entry = pq.insert(curr_key, curr_element)
    PJ_node_to_pq_entry_dict[curr_v] = curr_pq_entry
  PJ_node_to_tree_node_dict = {}
  while pq.isEmpty() == False:
    curr_pq_entry = pq.removeMin()
    # print "entry key:", curr_pq_entry.getKey()
    curr_entry = curr_pq_entry.getValue()
    # print curr_entry
    # raise Exception()
    curr_v, curr_e = curr_entry
    # if edge is null, we don't add an edge to tree
    curr_tree_node = DAryTreeNode(DAryTreeEntry(curr_v, 1), None, [])
    # print "curr. v:", curr_v
    # print pq.toString()
    # print pq.size()
    # handle first vertex popped
    if curr_v == chosen_root_node:
      # print "curr. weight:", 0
      T._setRoot(curr_tree_node)
      PJ_node_to_tree_node_dict[curr_v] = curr_tree_node
    else:
      # print "curr. weight:", curr_e.getWeight()
      # add a node to tree
      PJ_node1 = curr_e.getOriginVertex()
      PJ_node2 = curr_e.getDestinationVertex()
      earlier_PJ_node = None
      if curr_v == PJ_node1:
        earlier_PJ_node = PJ_node2
      elif curr_v == PJ_node2:
        earlier_PJ_node = PJ_node1
      # curr. node comes at the advice of an earlier node
      curr_tree_node_parent = PJ_node_to_tree_node_dict[earlier_PJ_node]
      PJ_node_to_tree_node_dict[curr_v] = curr_tree_node
      curr_tree_node_parent.addChild(curr_tree_node)
    PJ_node_is_in_queue[curr_v] = False
    for edge in PJ_node_to_involved_PJ_edges[curr_v]:
      PJ_node1 = edge.getOriginVertex()
      PJ_node2 = edge.getDestinationVertex()
      partner_PJ_node = None
      if curr_v == PJ_node1:
        partner_PJ_node = PJ_node2
      elif curr_v == PJ_node2:
        partner_PJ_node = PJ_node1
      if PJ_node_is_in_queue[partner_PJ_node] == True and edge.getWeight() < D[partner_PJ_node]:
        # we see a better distance
        D[partner_PJ_node] = edge.getWeight()
        # print "update occurs with weight:", edge.getWeight()
        # change entry s.t. better edge is recorded in Q
        # change entry s.t. better priority is recorded in Q
        partner_pq_entry = PJ_node_to_pq_entry_dict[partner_PJ_node]
        pq.removeEntry(partner_pq_entry)
        next_key = D[partner_PJ_node]
        next_element = (partner_PJ_node, edge)
        next_partner_pq_entry = pq.insert(next_key, next_element)
        PJ_node_to_pq_entry_dict[partner_PJ_node] = next_partner_pq_entry
    # prepare tree node for input graph nodes
    # prepare to add a tree node as a child of the tree node for curr. PJ node's partner
    # if edge is non-existant, don't fret about partner
  return T

"""

V = []
vertex_names = ["SFO", "LAX", "DFW", "ORD", "BOS", "PVD", "JFK", "BWI", "MIA"]
vertex_name_to_vertex_dict = {}
for vertex_name in vertex_names:
  vertex = PJVertex(vertex_name)
  vertex_name_to_vertex_dict[vertex_name] = vertex
  V.append(vertex)
# print V

E = []
SFO_partner_weight_tuples = [("LAX", 337), ("DFW", 1464), ("ORD", 1846), ("BOS", 2704)]
LAX_partner_weight_tuples = [("SFO", 337), ("DFW", 1235), ("MIA", 2342)]
DFW_partner_weight_tuples = [("SFO", 1464), ("LAX", 1235), ("ORD", 802), ("JFK", 1391), ("MIA", 1121)]
ORD_partner_weight_tuples = [("SFO", 1846), ("DFW", 802), ("BWI", 621), ("JFK", 740), ("PVD", 849), ("BOS", 867)]
BOS_partner_weight_tuples = [("SFO", 2704), ("ORD", 867), ("JFK", 187), ("MIA", 1258)]
PVD_partner_weight_tuples = [("ORD", 849), ("JFK", 144)]
JFK_partner_weight_tuples = [("BOS", 187), ("ORD", 740), ("DFW", 1391), ("BWI", 184), ("MIA", 1090), ("PVD", 144)]
BWI_partner_weight_tuples = [("JFK", 184), ("ORD", 621), ("MIA", 946)]
MIA_partner_weight_tuples = [("LAX", 2342), ("DFW", 1121), ("BWI", 946), ("JFK", 1090), ("BOS", 1258)]
node_node_weight_tuples = []
node_node_weight_tuples.extend([("SFO", x[0], x[1]) for x in SFO_partner_weight_tuples])
node_node_weight_tuples.extend([("LAX", x[0], x[1]) for x in LAX_partner_weight_tuples])
node_node_weight_tuples.extend([("DFW", x[0], x[1]) for x in DFW_partner_weight_tuples])
node_node_weight_tuples.extend([("ORD", x[0], x[1]) for x in ORD_partner_weight_tuples])
node_node_weight_tuples.extend([("BOS", x[0], x[1]) for x in BOS_partner_weight_tuples])
node_node_weight_tuples.extend([("PVD", x[0], x[1]) for x in PVD_partner_weight_tuples])
node_node_weight_tuples.extend([("JFK", x[0], x[1]) for x in JFK_partner_weight_tuples])
node_node_weight_tuples.extend([("BWI", x[0], x[1]) for x in BWI_partner_weight_tuples])
node_node_weight_tuples.extend([("MIA", x[0], x[1]) for x in MIA_partner_weight_tuples])

node_str_pair_seen_dict = {}
for node_node_weight_tuple in node_node_weight_tuples:
  v1_str, v2_str, weight = node_node_weight_tuple
  seen_before = False
  node_str_pair1 = (v1_str, v2_str)
  node_str_pair2 = (v2_str, v1_str)
  if node_str_pair1 in node_str_pair_seen_dict:
    seen_before = True
  elif node_str_pair2 in node_str_pair_seen_dict:
    seen_before = True
  else:
    seen_before = False
    node_str_pair_seen_dict[node_str_pair1] = True
  if seen_before == False:
    vertex1 = vertex_name_to_vertex_dict[v1_str]
    vertex2 = vertex_name_to_vertex_dict[v2_str]
    edge = PJEdge(vertex1, vertex2, weight)
    E.append(edge)

# print "edges:", E
# print "number of edges:", len(E)

# 337, 1464, 1235, 1846, 2704, 2342, 802, 1121, 867, 946, 1391, 621, 740, 849, 1090, 184, 187, 144, 1258
# (4 + 3 + 5 + 6 + 4 + 2 + 6 + 3 + 5) / 2 = 38 / 2 = 19

tree = doPrimJarnik(V, E)
entries = tree.toPreorderList()

# print "result:", entries

print "vertex ID's:", [x.getKey().getID() for x in entries]

"""


