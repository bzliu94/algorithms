# 2016-03-30

# brute-force student id censorer

# it helps to, e.g., cut off first two digits of a six-digit identifier to speed up censoring

# problem is not np-hard
# have isolated cliques
# slot conflicts, subset conflicts, unambiguity goal
# lexicographical ordering
# n is number of student id strings, m is number of digits per student id string

# n + n * (2 ^ m) + n * (2 ^ m) + n * (2 ^ m) + n + n * (2 ^ m) + n
# = O(n * 2 ^ m) time

from collections import defaultdict
import sys
import string
class UndirectedGraph:
  # assume that at most one edge exists for each two-node combination
  # also, we assume no self-edges
  def __init__(self, nodes, edges):
    self.id_str_to_node_list_dict = defaultdict(lambda: [])
    self.slot_id_to_node_list_dict = defaultdict(lambda: [])
    for node in nodes:
      self.addNode(node)
    self.node_pair_to_edge_dict = {}
    self.node_to_edge_list_dict = defaultdict(lambda: [])
    for edge in edges:
      self.addEdge(edge)
    self.num_nodes = 0
    self.num_edges = 0
  # takes O(n) time
  def getNodes(self):
    id_str_to_node_list_dict = self.id_str_to_node_list_dict
    values = id_str_to_node_list_dict.values()
    result = reduce(lambda x, y: x + y, values)
    return result
  def _getIDStrToNodeListDict(self):
    return self.id_str_to_node_list_dict
  def _getSlotIDToNodeListDict(self):
    return self.slot_id_to_node_list_dict
  def _getNodePairToEdgeDict(self):
    return self.node_pair_to_edge_dict
  def _getNodeToEdgeListDict(self):
    return self.node_to_edge_list_dict
  def getNumNodes(self):
    return self.num_nodes
  def getNumEdges(self):
    return self.num_edges
  def addNode(self, node):
    id_str_to_node_list_dict = self._getIDStrToNodeListDict()
    slot_id_to_node_list_dict = self._getSlotIDToNodeListDict()
    sack_item = node.getSackItem()
    id_str_to_node_list_dict[sack_item.getIDStr()].append(node)
    slot_id_to_node_list_dict[sack_item.getSlotID()].append(node)
    self.num_nodes += 1
  def removeNode(self, node):
    id_str_to_node_list_dict = self._getIDStrToNodeListDict()
    slot_id_to_node_list_dict = self._getSlotIDToNodeListDict()
    sack_item = node.getSackItem()
    id_str_to_node_list_dict[sack_item.getIDStr()].remove(node)
    slot_id_to_node_list_dict[sack_item.getSlotID()].remove(node)
    self.num_nodes -= 1
  def addEdge(self, edge):
    node_pair_to_edge_dict = self._getNodePairToEdgeDict()
    node_to_edge_list_dict = self._getNodeToEdgeListDict()
    node1 = edge.getNode1()
    node2 = edge.getNode2()
    node_pair1 = (node1, node2)
    node_pair2 = (node2, node1)
    node_pair_to_edge_dict[node_pair1] = edge
    node_pair_to_edge_dict[node_pair2] = edge
    node_to_edge_list_dict[node1].append(edge)
    node_to_edge_list_dict[node2].append(edge)
    self.num_edges += 1
  def removeEdge(self, edge):
    node_pair_to_edge_dict = self._getNodePairToEdgeDict()
    node_to_edge_list_dict = self._getNodeToEdgeListDict()
    node1 = edge.getNode1()
    node2 = edge.getNode2()
    node_pair1 = (node1, node2)
    node_pair2 = (node2, node1)
    node_pair_to_edge_dict.pop(node_pair1)
    node_pair_to_edge_dict.pop(node_pair2)
    node_to_edge_list_dict[node1].remove(edge)
    node_to_edge_list_dict[node2].remove(edge)
    self.num_edges -= 1
  def getEdge(self, node1, node2):
    node_pair = (node1, node2)
    node_pair_to_edge_dict = self._getNodePairToEdgeDict()
    if not (node_pair in node_pair_to_edge_dict):
      return None
    else:
      edge = node_pair_to_edge_dict[node_pair]
      return edge
  # takes O(1) time
  def getNumConflicts(self, node):
    node_to_edge_list_dict = self._getNodeToEdgeListDict()
    edges = node_to_edge_list_dict[node]
    num_edges = len(edges)
    num_conflicts = num_edges
    return num_conflicts
  def getEdgeExists(self, node1, node2):
    edge = self.getEdge(node1, node2)
    edge_exists = edge != None
    return edge_exists
  def getEdgeListForNode(self, node):
    node_to_edge_list_dict = self._getNodeToEdgeListDict()
    edge_list = node_to_edge_list_dict[node]
    return edge_list[ : ]
  def getNodeListForIDStr(self, id_str):
    id_str_to_node_list_dict = self._getIDStrToNodeListDict()
    node_list = id_str_to_node_list_dict[id_str]
    return node_list[ : ]
  def getNodeListForSlotID(self, slot_id):
    slot_id_to_node_list_dict = self._getSlotIDToNodeListDict()
    node_list = slot_id_to_node_list_dict[slot_id]
    return node_list[ : ]
class UndirectedEdge:
  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
  def getNode1(self):
    return self.node1
  def getNode2(self):
    return self.node2
  def toString(self):
    node1 = self.getNode1()
    node2 = self.getNode2()
    sack_item1 = node1.getSackItem()
    sack_item2 = node2.getSackItem()
    sack_item_str1 = sack_item1.toString()
    sack_item_str2 = sack_item2.toString()
    result_str = "(" + sack_item_str1 + ", " + sack_item_str2 + ")"
    return result_str
class SackItem:
  def __init__(self, id_str, slot_id, profit, weight, node, conflict_graph):
    self.id_str = id_str
    self.slot_id = slot_id
    self.profit = profit
    self.weight = weight
    self.node = node
    self.conflict_graph = conflict_graph
  def _getNode(self):
    return self.node
  def _setNode(self, node):
    self.node = node
  def _getConflictGraph(self):
    return self.conflict_graph
  def getProfit(self):
    return self.profit
  def getWeight(self):
    return self.weight
  def getRatio(self):
    profit = self.getProfit()
    weight = self.getWeight()
    ratio = profit / (1.0 * weight)
    return ratio
  def getRatioTuple(self):
    profit = self.getProfit()
    weight = self.getWeight()
    ratio = profit / (1.0 * weight)
    node = self._getNode()
    conflict_graph = self._getConflictGraph()
    num_conflicts = conflict_graph.getNumConflicts(node)
    # prefer nodes with fewer conflicts
    curr_tuple = (ratio, -1 * num_conflicts)
    return curr_tuple
  def getIDStr(self):
    return self.id_str
  def getSlotID(self):
    return self.slot_id
  def toString(self):
    id_str = self.getIDStr()
    slot_id = str(self.getSlotID())
    result_str = "(" + id_str + ", " + slot_id + ")"
    return result_str
def getNumAsterisks(curr_str):
    chars = list(curr_str)
    matching_chars = [x for x in chars if x == "*"]
    num_asterisks = len(matching_chars)
    return num_asterisks
class Node:
  def __init__(self, sack_item):
    self.sack_item = sack_item
    self.cc_num = None
  def getSackItem(self):
    return self.sack_item
  def toString(self, undirected_graph):
    sack_item = self.getSackItem()
    id_str = sack_item.getIDStr()
    edges = undirected_graph.getEdgeListForNode(self)
    edge_str_list = [x.toString() for x in edges]
    result_str = "(" + id_str + ", (" + ", ".join(edge_str_list) + "))"
    return result_str
# takes O(2 ^ m) time, where m is number of characters in given string
# assume asterisks can exist in the given string
# assume full-asterisked string is disallowed
def getAsteriskedStrings(source_str, M):
  n = len(source_str)
  first_char = source_str[0]
  remaining_chars = source_str[1 : ]
  if n == 0:
    return []
  elif n == 1:
    if first_char != "*":
      return [source_str, "*"]
    else:
      return [source_str]
  else:
    next_asterisked_str_list = getAsteriskedStrings(remaining_chars, M)
    str_list1 = []
    if first_char != "*":
      str_list1 = [first_char + x for x in next_asterisked_str_list]
    str_list2 = ["*" + x for x in next_asterisked_str_list]
    result = str_list1 + str_list2
    all_asterisk_str = "*" * M
    result = [x for x in result if x != all_asterisk_str]
    return result
def addCliqueEdges(nodes, undirected_graph):
  # for three digits, we have 7 + 6 + 5 + 4 + 3 + 2 + 1 + 0 = 28 edges
  edges = []
  num_nodes = len(nodes)
  for i in xrange(num_nodes):
    node1 = nodes[i]
    for j in xrange(i + 1, num_nodes):
      node2 = nodes[j]
      edge = UndirectedEdge(node1, node2)
      undirected_graph.addEdge(edge)
      edges.append(edge)
  return edges
def removeNodesAndTheirEdges(id_str, graph):
  node_list = graph.getNodeListForIDStr(id_str)
  # print [x.getSackItem().toString() for x in node_list]
  for node in node_list:
    edge_list = graph.getEdgeListForNode(node)
    for edge in edge_list:
      graph.removeEdge(edge)
    graph.removeNode(node)
def main():
  # stream = open("tests/input10.txt")
  stream = sys.stdin
  line = stream.readline()
  line = line.rstrip("\n")
  args = line.split()
  args = [string.atol(x) for x in args]
  M = int(args[0])
  N = int(args[1])
  # print N
  if N == 1:
    print "*" * M
    return
  student_id_str_list = []
  for i in xrange(N):
    line = stream.readline()
    line = line.rstrip("\n")
    args = line.split()
    student_id_str = args[0]
    student_id_str_list.append(student_id_str)
  id_str_list = student_id_str_list
  nodes = []
  num_id_values = len(id_str_list)
  graph = UndirectedGraph([], [])
  for i in xrange(num_id_values):
    id_str = id_str_list[i]
    curr_nodes = []
    asterisked_str_list = getAsteriskedStrings(id_str, M)
    for asterisked_str in asterisked_str_list:
      sack_item = SackItem(asterisked_str, i, getNumAsterisks(asterisked_str), 1, None, graph)
      node = Node(sack_item)
      sack_item._setNode(node)
      curr_nodes.append(node)
      graph.addNode(node)
    # handle slot clique
    addCliqueEdges(curr_nodes, graph)
    nodes = nodes + curr_nodes
  # have modified conflict graph (e.g., no "****")
  num_asterisks_to_count_dict = defaultdict(lambda: 0)
  for node in nodes:
    sack_item = node.getSackItem()
    num_asterisks = getNumAsterisks(sack_item.getIDStr())
    num_asterisks_to_count_dict[num_asterisks] += 1
  id_str_to_source_str_list_dict = defaultdict(lambda: [])
  for id_str in id_str_list:
    asterisked_str_list = getAsteriskedStrings(id_str, M)
    for curr_id_str in asterisked_str_list:
      id_str_to_source_str_list_dict[curr_id_str].append(id_str)
  for id_str in id_str_to_source_str_list_dict.keys():
    if len(id_str_to_source_str_list_dict[id_str]) >= 2:
      removeNodesAndTheirEdges(id_str, graph)
  id_str_list = []
  for i in xrange(N):
    node_list = graph.getNodeListForSlotID(i)
    tagged_node_list = [((-1 * x.getSackItem().getProfit(), x.getSackItem().getIDStr()), x) for x in node_list]
    # sorted_tagged_node_list = sorted(tagged_node_list, key = lambda x: x[0], reverse = False)
    # chosen_node = sorted_tagged_node_list[0][1]
    chosen_tagged_node = min(tagged_node_list, key = lambda x: x[0])
    chosen_node = chosen_tagged_node[1]
    id_str = chosen_node.getSackItem().getIDStr()
    id_str_list.append(id_str)
  for id_str in id_str_list:
    print id_str
if __name__ == "__main__":
  main()
