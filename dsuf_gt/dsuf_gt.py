# 2019-07-23

# important values are b_noneffective and num_chunk_bits; 
# num_chunk_bits >= log_2(b_noneffective); 
# b_noneffective * num_chunk_bits <= w

# the way we deal with skipping work for repeat parent signals is causing issues with correctness via mark status for gtm nodes

# we had a stale value for processing microset for curr. gtm tree

# NOTE -- word-related parameters are hard-coded here

# 2019-07-02

# we implement gabow-tarjan disjoint set union-find data structure

# for n items in union tree and m union/find operations, overall time is in O(n + m)

# assume b parameter is s.t. b * log_2(b) <= w (i.e. this latter number of bits fits in one word)

# we assume ram model (meaning that we do math with pointers)

# DETAILS

# smaller universe of macro level makes alpha lower 
# s.t. it is boundable by a constant for all n and not just certain n

# we have m + n / b macrofind calls 
# because we have m find/union operations at most and n / b macro nodes; 
# links are lazy and cost O(1) time each and there are m links at most; 
# we have m + n / b find calls at most; 
# we have m + n / b macrounite calls at most; 
# overall time is O((m + n / b) * alpha(m + n / b, n / b)

# if b = big-omega of log(log(n)), overall time becomes O(m + n)

# b does not have to be so large, but it is a good starting value

# b affects: (1) alpha bounding by a constant for all n 
# and not just some n; (2) time required to construct and use table; 
# (3) our ability to use word-packing

# how do we handle tables efficiently?
# we don't need b ^ b different configurations for each microset 
# (in the form of a table), because elements of a set must all exist 
# in one contiguous piece; apparently, this allows for 2 ^ (b * log(b)) time 
# for each candidate table s.t. overall time (via considering all candidates) 
# is around b * 2 ^ (b * log(b)) instead

# if b is in O(log(log(n))), time for constructing parent table 
# is around O(b * (2 ^ (b ^ 2))) = O(b * 2 ^ (log^2(log(n)) ^ 2)) 
# = O(b * log^2(n)) = O(log(log(n)) * log^2(n)) = O(log^3(n)); 
# the main idea is that log(log(n)) dominates alpha and log^3(n) 
# is dominated by n

# the time is due to having b different sets in a microset 
# and for each set we have elements included and excluded; 
# we have a power of log(b) because this becomes 2 ^ log(b) = O(b), 
# which exists because we provide a reference node 
# (and also provide environment as part of query)

# micro, number, parent, mark feed into answer

# node, root exist as well

# find and microfind are special

# we must remember that we initialize microsets 
# by determining their structure via parent table once 
# and re-use this parent table for each microset repeatedly later

# parent table values are not in {0, 1}, but are in [0, b - 1]

# we must remember that one of the b's that exists 
# as a coefficient because we choose a different reference logical set 
# and each of these combination possibilities are isolated 
# from each other (and so we avoid an extra power of b and 
# instead have an extra factor of b)

# microfind uses our answer table, macrofind uses alpha-algorithm

# we also need to construct microsets and macrosets correctly

# we allow m macrofinds because alpha is boundable by a constant 
# for all n given that we have a small universefrom fgib_tarjan import Tree, TreeVertex

from fgib_tarjan import Tree, TreeVertex
from dsuf import UnionFind, NamedUnionFind
from collections import defaultdict, deque
import random
import math

"""

from sys import maxint
print maxint

"""

# int type (as opposed to long) on our machine has 64 bits, 
# which means 63 bits that are usable (i.e. not for sign)

# for cpython 2.7, we likely have at least 32-bit int values (i.e. 31 bits that are usable)

# because one bit for a number is devoted to sign, 
# for simplicity we assume this bit is not useable

# w = 31
w = 63

# deal with chunks

# num_chunk_bits = 4
num_chunk_bits = 3
# num_chunk_bits = 2

full_word_without_sign_ones = int((1 << w) - 1)

"""

print bin(full_word_without_sign_ones)
print type(full_word_without_sign_ones)

"""

"""

chunk_size = math.ceil(math.log(100, 2))
print chunk_size

"""

# b_noneffective should fit in num_chunk_bits bits; 
# this value should be kept s.t. 2 ^ b_noneffective is low

# b_noneffective = 15
b_noneffective = 7
# b_noneffective = 3

# zero-th chunk is the one with LSB
def setIthChunk(word, value, chunk_bit_size, i):
  if chunk_bit_size > (w - 1):
    raise Exception()
  # clear the chunk
  # perform one's complement
  curr_value = (((1 << chunk_bit_size) - 1) << (chunk_bit_size * i)) ^ full_word_without_sign_ones
  curr_value = word & curr_value
  # set the chunk
  curr_value = curr_value | (value << (chunk_bit_size * i))
  return curr_value

"""

print bin(setIthChunk(0b101101, 5, 4, 1))

"""

# there could be an issue with if we are close to using bigints 
# instead of ints because we momentarily cross word boundary; 
# we assume chunk_bit_size << w
def getFirstChunk(word, chunk_bit_size):
  if chunk_bit_size > (w - 1):
    raise Exception()
  curr_value = word & ((1 << chunk_bit_size) - 1)
  return curr_value

"""

print bin(getFirstChunk(0b101101, 3))

"""

# there could be an issue with if we are close to using bigints 
# instead of ints because we momentarily cross word boundary; 
# we assume chunk_bit_size << w
def getIthChunk(word, chunk_bit_size, i):
  if chunk_bit_size > (w - 1):
    raise Exception()
  curr_value = word >> (chunk_bit_size * i)
  curr_value = getFirstChunk(curr_value, chunk_bit_size)
  return curr_value

"""

print bin(getIthChunk(0b100101, 3, 1))

"""

"""

curr_num = 0
curr_num = setIthChunk(curr_num, 0b101101, 6, 0)
curr_num = setIthChunk(curr_num, 0b101101, 6, 2)
print bin(curr_num)
print bin(getIthChunk(curr_num, 6, 2))

"""

# have unmarking of nodes for removal as a set name
class UnionTree(Tree):
  def __init__(self):
    Tree.__init__(self)
  def getPostorderNodes(self):
    root = self.getRoot()
    result = root._getPostorderNodes()
    return result
  # is destructive; takes O(n) time where n is number of nodes in union tree; 
  # ignoring last set, sizes still do not have to be uniform; 
  # return root-group tuples
  def prepareNodeGroups(self, b):
    post_order_nodes = self.getPostorderNodes()
    post_order_nodes_deque = deque(post_order_nodes)
    result_root_group_tuples = []
    go_to_step_two = False
    children = None
    children_deque = None
    while len(post_order_nodes_deque) != 0:
      if go_to_step_two == False:
        curr_node = post_order_nodes_deque.popleft()
        children = curr_node.getChildren()
        children_deque = deque(children)
        # step one
        curr_node.setD(1)
        w = None
        if curr_node.haveChildren() == True:
          w = children_deque.popleft()
      # step two
      while curr_node.getD() < (b + 1) / 2. and w != None:
        curr_node.setD(curr_node.getD() + w.getD())
        if len(children_deque) == 0:
          w = None
        else:
          w = children_deque.popleft()
      # step three
      if curr_node.getD() < (b + 1) / 2.:
        go_to_step_two = False
        continue
      else:
        curr_group = []
        # all children from left to right stopping at and excluding node w
        remaining_children = []
        for child in children:
          if child == w:
            break
          remaining_children.append(child)
        for remaining_child in remaining_children:
          # we're assuming extend is efficient
          curr_group.extend(remaining_child.getSubtreeTreeNodes())
        # we remove vertices assuming that vertices we remove are at left of children list for a parent
        curr_group_node_set = set(curr_group)
        parent_to_children_dict = defaultdict(lambda: [])
        for curr_group_node in curr_group:
          curr_parent = curr_group_node.getParent()
          parent_to_children_dict[curr_parent].append(curr_group_node)
        for curr_parent in parent_to_children_dict.keys():
          curr_children_deque = deque(curr_parent.getChildren())
          while len(curr_children_deque) != 0 and curr_children_deque[0] in curr_group_node_set:
            curr_parent.removeLeftmostChild()
            curr_children_deque.popleft()
        curr_node.setD(1)
        go_to_step_two = True
        result_root_group_tuples.append((curr_node, curr_group))
    # have one final group
    last_root_group_tuple = (None, self.getPreorderNodes())
    result_root_group_tuples.append(last_root_group_tuple)
    return result_root_group_tuples
  # names are preserved
  def clone(self):
    nodes = self.getPreorderNodes()
    next_nodes = [UnionTreeVertex(x.getName()) for x in nodes]
    name_to_next_node = {}
    for curr_next_node in next_nodes:
      curr_name = curr_next_node.getName()
      name_to_next_node[curr_name] = curr_next_node
    for curr_node in nodes:
      next_node = name_to_next_node[curr_node.getName()]
      if curr_node.haveParent() == True:
        parent = curr_node.getParent()
        next_node.setParent(name_to_next_node[parent.getName()])
      for child_node in curr_node.getChildren():
        next_node.addChild(name_to_next_node[child_node.getName()])
    next_root = name_to_next_node[self.getRoot().getName()]
    t = UnionTree()
    t.setRoot(next_root)
    return t
class UnionTreeVertex(TreeVertex):
  def __init__(self, name):
    TreeVertex.__init__(self, name)
    # for microset creation
    self.d = None
  def getD(self):
    return self.d
  def setD(self, d):
    self.d = d
  def _getPostorderNodes(self):
    result = []
    self._getPostorderNodesHelper(result)
    return result
  def _getPostorderNodesHelper(self, result):
    children = self.getChildren()
    for child in children:
      child._getPostorderNodesHelper(result)
    result.append(self)

# this is internal to gabow-tarjan
class GTNode:
  def __init__(self, name):
    self.name = name
    self.micro = None
    self.num = None
    self.microset = None
  def getName(self):
    return self.name
  def setMicro(self, micro):
    self.micro = micro
  def setNumber(self, num):
    self.num = num
  def getMicro(self):
    return self.micro
  def getNumber(self):
    return self.num
  def getMicroset(self):
    return self.microset
  def setMicroset(self, microset):
    self.microset = microset

"""

gt_node1 = GTNode(1)
gt_node1.setMicro(3)
gt_node1.setNumber(4)
print gt_node1.getName()
print gt_node1.getMicro()
print gt_node1.getNumber()

"""

class GTMicroset:
  def __init__(self, root, gt_nodes):
    self.root = root
    self.gt_nodes = gt_nodes[ : ]
    self.id_value = None
    self.parent_signal = None
    self.mark_signal = 0
  def getRoot(self):
    return self.root
  def setRoot(self, root):
    self.root = root
  def getGTNodes(self):
    return self.gt_nodes
  def setGTNodes(self, gt_nodes):
    self.gt_nodes = gt_nodes
  def toString(self):
    root_str = self.getRoot().getName() if self.getRoot() != None else str(None)
    gt_nodes_str = str([x.getName() for x in self.getGTNodes()])
    return str((root_str, gt_nodes_str))
  def setID(self, id_value):
    self.id_value = id_value
  def getID(self):
    return self.id_value
  # set micro and number values for nodes in this microset
  def _setConstituentNumbers(self):
    gt_nodes = self.getGTNodes()
    for i in xrange(len(gt_nodes)):
      gt_node = gt_nodes[i]
      gt_node.setMicro(self.getID())
      gt_node.setNumber(i + 1)
  def _setParentSignal(self, parent_signal):
    self.parent_signal = parent_signal
  def _getParentSignal(self):
    return self.parent_signal
  def _getMarkSignal(self):
    return self.mark_signal
  # we assume values we store are single 0/1 bits and that they all fit in a word; 
  # i is 1-indexed
  def unmark(self, i):
    self.mark_signal = setIthChunk(self.mark_signal, 1, 1, i - 1)
  def _resetMarkSignal(self):
    self.mark_signal = 0
class GTMicrosetTree(Tree):
  def __init__(self):
    Tree.__init__(self)
  def getNodeMarkTupleCombinations(self):
    nodes = self.getPreorderNodes()
    # takes time in O(2 ^ (|V| + c))
    node_include_tuples = GTMicrosetTree._getItemIncludeTupleCombinations(nodes)
    return node_include_tuples
  @staticmethod
  def _getItemIncludeTupleCombinations(items):
    result = GTMicrosetTree._getItemIncludeTupleCombinationsHelper(deque(items))
    return result
  @staticmethod
  def _getItemIncludeTupleCombinationsHelper(item_deque):
    if len(item_deque) == 0:
      return []
    else:
      curr_item = item_deque.popleft()
      if len(item_deque) == 0:
        return [[(curr_item, False)], [(curr_item, True)]]
      else:
        next_tuples = GTMicrosetTree._getItemIncludeTupleCombinationsHelper(item_deque)
        curr_tuples = [[(curr_item, False)] + x for x in next_tuples] + [[(curr_item, True)] + x for x in next_tuples]
      return curr_tuples
  # we assume mark status for each node is set correctly 
  # and that we are not just using mark signals; 
  # consider all possible start nodes and visit all nodes for each start node; 
  # time required is O(b * 2 ^ b) s.t. size of microset is O(b); 
  # coefficient of b comes from considering all reference nodes, which we do via a pre-order traversal (!)
  # we ignore root because we assume it is a dummy node
  def doPreorderClosestNonProperAncestorTraversal(self, node_mark_tuple_combination):
    for node_mark_tuple in node_mark_tuple_combination:
      gtm_node, is_marked = node_mark_tuple
      if is_marked == True:
        gtm_node.setIsMarked()
      elif is_marked == False:
        gtm_node.setIsNotMarked()
    root = self.getRoot()
    root.doPreorderClosestNonProperAncestorTraversalHelper(None, True)

class GTMicrosetTreeVertex(TreeVertex):
  def __init__(self, name):
    TreeVertex.__init__(self, name)
    self.mark = None
    self.closest_marked_non_proper_ancestor_gtm_node = None
  def isMarked(self):
    return self.mark
  def setIsMarked(self):
    self.mark = True
  def setIsNotMarked(self):
    self.mark = False
  def getCMNPA(self):
    return self.closest_marked_non_proper_ancestor_gtm_node
  def setCMNPA(self, gtm_node):
    self.closest_marked_non_proper_ancestor_gtm_node = gtm_node
  def haveCMNPA(self):
    return self.closest_marked_non_proper_ancestor_gtm_node != None
  def doPreorderClosestNonProperAncestorTraversalHelper(self, closest_marked_proper_ancestor, ignore_curr_node = False):
    children = self.getChildren()
    next_closest_marked_non_proper_ancestor = closest_marked_proper_ancestor
    if ignore_curr_node == False and self.isMarked() == True:
      next_closest_marked_non_proper_ancestor = self
    self.setCMNPA(next_closest_marked_non_proper_ancestor)
    for child in children:
      child.doPreorderClosestNonProperAncestorTraversalHelper(next_closest_marked_non_proper_ancestor, False)

class UnionTreeUnionFind:
  def __init__(self, union_tree):
    self.union_tree = union_tree
    self.name_to_ut_node_dict = None
    self.name_to_gt_node_dict = None
    self.name_to_gtm_node_dict = None
    self.macroset_uf = None
    self.microset_id_node_num_tuple_to_node_dict = None
    self.answer_three_tuple_to_num_dict = None
    self._prepare()
  def _getUnionTree(self):
    return self.union_tree
  def _setNameToUTNodeDict(self, name_to_ut_node_dict):
    self.name_to_ut_node_dict = name_to_ut_node_dict
  def _getNameToUTNodeDict(self):
    return self.name_to_ut_node_dict
  def _setNameToGTNodeDict(self, name_to_gt_node_dict):
    self.name_to_gt_node_dict = name_to_gt_node_dict
  def _getNameToGTNodeDict(self):
    return self.name_to_gt_node_dict
  def _setNameToGTMNodeDict(self, name_to_gtm_node_dict):
    self.name_to_gtm_node_dict = name_to_gtm_node_dict
  def _getNameToGTMNodeDict(self):
    return self.name_to_gtm_node_dict
  def _setMacrosetUF(self, macroset_uf):
    self.macroset_uf = macroset_uf
  def _getMacrosetUF(self):
    return self.macroset_uf
  def _setMicrosetIDNodeNumTupleToNodeDict(self, microset_id_node_num_tuple_to_node_dict):
    self.microset_id_node_num_tuple_to_node_dict = microset_id_node_num_tuple_to_node_dict
  def _getMicrosetIDNodeNumTupleToNodeDict(self):
    return self.microset_id_node_num_tuple_to_node_dict
  def _setAnswerThreeTupleToNumDict(self, answer_three_tuple_to_num_dict):
    self.answer_three_tuple_to_num_dict = answer_three_tuple_to_num_dict
  def _getAnswerThreeTupleToNumDict(self):
    return self.answer_three_tuple_to_num_dict
  # returns a gt node
  def _node(self, i, j):
    microset_id_node_num_tuple_to_node_dict = self._getMicrosetIDNodeNumTupleToNodeDict()
    return microset_id_node_num_tuple_to_node_dict[(i, j)]
  def _link(self, gt_node):
    name_to_ut_node_dict = self._getNameToUTNodeDict()
    if name_to_ut_node_dict[gt_node.getName()].haveParent() == False:
      raise Exception()
    curr_microset = gt_node.getMicroset()
    curr_num = gt_node.getNumber()
    curr_microset.unmark(curr_num)
  # returns a gtm node
  def _getRoot(self, microset):
    return microset.getRoot()
  def _microfind(self, node_name):
    name_to_gt_node_dict = self._getNameToGTNodeDict()
    name_to_gtm_node_dict = self._getNameToGTMNodeDict()
    microset_id_node_num_tuple_to_node_dict = self._getMicrosetIDNodeNumTupleToNodeDict()
    answer_three_tuple_to_num_dict = self._getAnswerThreeTupleToNumDict()
    gt_node = name_to_gt_node_dict[node_name]
    gtm_node = name_to_gtm_node_dict[node_name]
    i = gt_node.getMicro()
    j = gt_node.getNumber()
    curr_microset = gt_node.getMicroset()
    curr_parent_signal = curr_microset._getParentSignal()
    curr_mark_signal = curr_microset._getMarkSignal()
    curr_key = (curr_parent_signal, curr_mark_signal, j)
    k = answer_three_tuple_to_num_dict[curr_key]
    if k == 0:
      return self._getRoot(curr_microset)
    else:
      return self._node(i, k)
  def _micro(self, node_name):
    name_to_gt_node_dict = self._getNameToGTNodeDict()
    gt_node = name_to_gt_node_dict[node_name]
    return gt_node.getMicro()
  # returns a node name and not a node
  def _find(self, node_name):
    curr_macroset_uf = self._getMacrosetUF()
    v_name = node_name
    x_name = v_name
    # define find in terms of microfind and macrofind operations; 
    # determine whether we use solely intra-microset moves 
    # or 3+ moves consisting of inter-microset (i.e. macroset) moves 
    # wrapped by a pair of intra-microset moves
    """
    def find(v):
      local x
      x = v
      if micro(x) != micro(microfind(x)):
        x = macrofind(microfind(x))
      while micro(x) != micro(microfind(x)):
        macrounite(microfind(x), x)
        x = macrofind(x)
      return microfind(x)
    """
    # if predicate is true, we need to cross a microset boundary
    if self._micro(x_name) != self._micro(self._microfind(x_name).getName()):
      x_name = curr_macroset_uf.find(self._microfind(x_name).getName())
    # name of a macroset must be name of highest element in it; 
    # if predicate is true, we have >= 1 pending macro-unions to perform; 
    # at this point, x is guaranteed to be a microset root or macro universe element; 
    # if we do not need a macro-union, calling microfind on a node should lead us to remain in the same microset
    while self._micro(x_name) != self._micro(self._microfind(x_name).getName()):
      # we follow up on lazy approach by finally actually performing a macro-side union; 
      # there is a bug from pseudocode here for first argument
      curr_macroset_uf.union(self._microfind(x_name).getName(), x_name)
      x_name = curr_macroset_uf.find(x_name)
    # we end with a last-mile microfind
    return self._microfind(x_name).getName()
  # we need to construct microsets; all except last have non-trivial min. size and last has size in [1, b - 1]
  def _prepare(self):
    t1 = self._getUnionTree()
    t2 = t1.clone()
    t2._setPostorderNumbers()
    root_group_tuples = t2.prepareNodeGroups(b_noneffective)
    t1._setPostorderNumbers()
    # make microsets with size b >= 2 out of union tree
    nodes = t1.getPreorderNodes()
    name_to_ut_node_dict = {}
    for ut_node in nodes:
      name_to_ut_node_dict[ut_node.getName()] = ut_node
    gt_nodes = [GTNode(x.getName()) for x in nodes]
    name_to_gt_node_dict = {}
    for gt_node in gt_nodes:
      name_to_gt_node_dict[gt_node.getName()] = gt_node
    microsets = []
    for root_group_tuple in root_group_tuples:
      root, node_group = root_group_tuple
      gt_root = name_to_gt_node_dict[root.getName()] if root != None else None
      gt_node_group = [name_to_gt_node_dict[x.getName()] for x in node_group]
      curr_microset = GTMicroset(gt_root, gt_node_group)
      for gt_node in gt_node_group:
        gt_node.setMicroset(curr_microset)
      microsets.append(curr_microset)
    # finalize the microsets by giving each a number in [1, num. microsets] 
    # and giving each item in each microset a number in [1, |S|]
    for i in xrange(len(microsets)):
      curr_microset = microsets[i]
      curr_microset.setID(i + 1)
      curr_microset._setConstituentNumbers()
    microset_id_node_num_tuple_to_node_dict = {}
    for curr_microset in microsets:
      curr_microset_id = curr_microset.getID()
      for curr_node in curr_microset.getGTNodes():
        curr_node_num = curr_node.getNumber()
        curr_key = (curr_microset_id, curr_node_num)
        microset_id_node_num_tuple_to_node_dict[curr_key] = curr_node
    # now, we have micro, num, node; now, we need parent, mark, answer
    for curr_microset in microsets:
      curr_gt_nodes = curr_microset.getGTNodes()
      word_packed_parent_signal = 0
      for curr_gt_node in curr_gt_nodes:
        # num. of bits for a chunk needs to be verified as being desirable
        curr_ut_node = name_to_ut_node_dict[curr_gt_node.getName()]
        have_parent = curr_ut_node.haveParent()
        curr_chunk_value = 0
        if have_parent == True:
          curr_gt_parent = name_to_gt_node_dict[curr_ut_node.getParent().getName()]
          if curr_gt_parent.getMicro() == curr_microset.getID():
            curr_chunk_value = curr_gt_parent.getNumber()
        word_packed_parent_signal = setIthChunk(word_packed_parent_signal, curr_chunk_value, num_chunk_bits, curr_gt_node.getNumber() - 1)
        curr_microset._setParentSignal(word_packed_parent_signal)
    # handle answer 3-d hash table; 
    # microfind is defined in terms of answer; 
    # re-construct trees using microsets and perform pre-order traversal 
    # as part of filling out answer 3-d table; 
    # result values are integers in {0} U {1, ... b - 1}
    name_to_gtm_node_dict = {}
    gtm_nodes = [GTMicrosetTreeVertex(x.getName()) for x in nodes]
    for gtm_node in gtm_nodes:
      name_to_gtm_node_dict[gtm_node.getName()] = gtm_node
    gtm_trees = []
    gtm_tree_to_microset_dict = {}
    for curr_microset in microsets:
      curr_gt_nodes = curr_microset.getGTNodes()
      curr_ut_nodes = [name_to_ut_node_dict[x.getName()] for x in curr_gt_nodes]
      have_root = curr_microset.getRoot() != None
      curr_gt_root = name_to_ut_node_dict[curr_microset.getRoot().getName()] if have_root == True else None
      curr_gtm_tree = GTMicrosetTree()
      curr_gtm_nodes = [name_to_gtm_node_dict[x.getName()] for x in curr_gt_nodes]
      # instead of having a forest, we have a dummy root and a single tree
      dummy_root = GTMicrosetTreeVertex("dummy")
      curr_gtm_tree.setRoot(dummy_root)
      # set parent-child relationships for gtm nodes
      curr_ut_nodes_set = set(curr_ut_nodes)
      for curr_ut_node in curr_ut_nodes:
        curr_gtm_node = name_to_gtm_node_dict[curr_ut_node.getName()]
        parent = curr_ut_node.getParent()
        if parent in curr_ut_nodes_set:
          curr_gtm_parent = name_to_gtm_node_dict[parent.getName()]
          curr_gtm_parent.addChild(curr_gtm_node)
          curr_gtm_node.setParent(curr_gtm_parent)
        else:
          # parent is a microset root or if current node is overall root, there is no microset root
          curr_gtm_node.setParent(dummy_root)
          dummy_root.addChild(curr_gtm_node)
      gtm_trees.append(curr_gtm_tree)
      gtm_tree_to_microset_dict[curr_gtm_tree] = curr_microset
    # an answer four-tuple is of form (parent signal, mark signal, node number, result)
    answer_four_tuples = []
    # we don't want to repeat work for same parent signal
    seen_parent_signal_set = set([])
    for curr_gtm_tree in gtm_trees:
      # we don't want to repeat work for same parent signal; 
      # there was a bug here s.t. use of name curr_microset is stale
      curr_microset = gtm_tree_to_microset_dict[curr_gtm_tree]
      curr_parent_signal = curr_microset._getParentSignal()
      if curr_parent_signal in seen_parent_signal_set:
        continue
      else:
        seen_parent_signal_set |= set([curr_parent_signal])
      node_mark_tuple_combinations = curr_gtm_tree.getNodeMarkTupleCombinations()
      for node_mark_tuple_combination in node_mark_tuple_combinations:
        curr_gtm_tree.doPreorderClosestNonProperAncestorTraversal(node_mark_tuple_combination)
        curr_microset = gtm_tree_to_microset_dict[curr_gtm_tree]
        curr_microset._resetMarkSignal()
        for node_mark_tuple in node_mark_tuple_combination:
          curr_node, is_marked = node_mark_tuple
          if curr_node.getName() == "dummy":
            continue
          curr_num = name_to_gt_node_dict[curr_node.getName()].getNumber()
          if is_marked == False:
            curr_microset.unmark(curr_num)
        # generate mark signal
        curr_mark_signal = curr_microset._getMarkSignal()
        for curr_gtm_node in [x for x in curr_gtm_tree.getPreorderNodes() if x.getName() != "dummy"]:
          curr_num = name_to_gt_node_dict[curr_gtm_node.getName()].getNumber()
          result = name_to_gt_node_dict[curr_gtm_node.getCMNPA().getName()].getNumber() if curr_gtm_node.haveCMNPA() == True else 0
          # generate four-tuple
          curr_four_tuple = (curr_parent_signal, curr_mark_signal, curr_num, result)
          answer_four_tuples.append(curr_four_tuple)
    # fill out answer table
    # define microfind, find
    # use macrosets
    answer_three_tuple_to_num_dict = {}
    for curr_answer_four_tuple in answer_four_tuples:
      parent_signal, mark_signal, num, result = curr_answer_four_tuple
      curr_key = (parent_signal, mark_signal, num)
      answer_three_tuple_to_num_dict[curr_key] = result
    for curr_microset in microsets:
      curr_microset._resetMarkSignal()
    # preparing s.t. we create macroset singletons
    root_names = []
    for root_group_tuple in root_group_tuples:
      root, node_group = root_group_tuple
      if root != None:
        root_names.append(root.getName())
    # we must use named union find so that the name of a macroset is always highest element in it
    macroset_uf = NamedUnionFind()
    macroset_uf.insert_objects(root_names)
    # each macroset item is a name of a node from original sets
    # epilogue
    self._setNameToUTNodeDict(name_to_ut_node_dict)
    self._setNameToGTNodeDict(name_to_gt_node_dict)
    self._setNameToGTMNodeDict(name_to_gtm_node_dict)
    self._setMacrosetUF(macroset_uf)
    self._setMicrosetIDNodeNumTupleToNodeDict(microset_id_node_num_tuple_to_node_dict)
    self._setAnswerThreeTupleToNumDict(answer_three_tuple_to_num_dict)
  def link(self, name):
    name_to_gt_node_dict = self._getNameToGTNodeDict()
    self._link(name_to_gt_node_dict[name])
  def find(self, name):
    return self._find(name)

if __name__ == '__main__':

  t1 = UnionTree()

  v1 = UnionTreeVertex(1)
  v2 = UnionTreeVertex(2)
  v3 = UnionTreeVertex(3)
  v4 = UnionTreeVertex(4)
  v5 = UnionTreeVertex(5)
  v6 = UnionTreeVertex(6)
  v7 = UnionTreeVertex(7)
  v8 = UnionTreeVertex(8)
  v9 = UnionTreeVertex(9)
  v10 = UnionTreeVertex(10)
  v11 = UnionTreeVertex(11)
  v12 = UnionTreeVertex(12)
  v13 = UnionTreeVertex(13)
  v14 = UnionTreeVertex(14)
  v15 = UnionTreeVertex(15)
  v16 = UnionTreeVertex(16)
  v17 = UnionTreeVertex(17)
  v18 = UnionTreeVertex(18)
  v19 = UnionTreeVertex(19)
  v20 = UnionTreeVertex(20)
  v21 = UnionTreeVertex(21)
  v22 = UnionTreeVertex(22)
  v23 = UnionTreeVertex(23)
  v24 = UnionTreeVertex(24)
  v25 = UnionTreeVertex(25)
  v26 = UnionTreeVertex(26)
  v27 = UnionTreeVertex(27)
  # v28 = UnionTreeVertex(28)

  t1.setRoot(v1)

  v1.addChild(v2)
  v1.addChild(v3)
  v1.addChild(v4)
  v2.addChild(v5)
  v2.addChild(v6)
  v3.addChild(v7)
  v3.addChild(v8)
  v4.addChild(v9)
  v4.addChild(v10)
  v5.addChild(v11)
  v5.addChild(v12)
  v5.addChild(v13)
  v7.addChild(v14)
  v7.addChild(v15)
  v9.addChild(v16)
  v16.addChild(v17)
  v17.addChild(v18)
  v18.addChild(v19)
  v18.addChild(v20)
  v18.addChild(v21)
  v18.addChild(v22)
  v18.addChild(v23)

  v2.setParent(v1)
  v3.setParent(v1)
  v4.setParent(v1)
  v5.setParent(v2)
  v6.setParent(v2)
  v7.setParent(v3)
  v8.setParent(v3)
  v9.setParent(v4)
  v10.setParent(v4)
  v11.setParent(v5)
  v12.setParent(v5)
  v13.setParent(v5)
  v14.setParent(v7)
  v15.setParent(v7)
  v16.setParent(v9)
  v17.setParent(v16)
  v18.setParent(v17)
  v19.setParent(v18)
  v20.setParent(v18)
  v21.setParent(v18)
  v22.setParent(v18)
  v23.setParent(v18)
  v10.addChild(v24)
  v24.setParent(v10)
  v10.addChild(v25)
  v25.setParent(v10)
  v10.addChild(v26)
  v26.setParent(v10)
  v10.addChild(v27)
  v27.setParent(v10)

  # v10.addChild(v28)
  # v28.setParent(v10)

  """

  v1.addChild(v2)
  v2.addChild(v3)
  v2.addChild(v4)
  v2.addChild(v5)
  v1.addChild(v6)
  v6.addChild(v7)
  v6.addChild(v8)
  v6.addChild(v9)

  v2.setParent(v1)
  v3.setParent(v2)
  v4.setParent(v2)
  v5.setParent(v2)
  v6.setParent(v1)
  v7.setParent(v6)
  v8.setParent(v6)
  v9.setParent(v6)

  """

  utuf = UnionTreeUnionFind(t1)
  # utuf.link(2)
  utuf.link(5)
  utuf.link(11)
  utuf.link(7)
  utuf.link(14)
  utuf.link(18)
  utuf.link(22)
  # should be 2
  result1 = utuf.find(11)
  print result1
  # should be 3
  result2 = utuf.find(14)
  print result2
  # should be 17
  result3 = utuf.find(22)
  print result3


