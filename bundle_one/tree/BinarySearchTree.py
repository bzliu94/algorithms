from BinaryTree import *
from Entry import *
from ..Util import *
# acknowledge primacy of key transform; 
# methods involving untransformed key 
# deal with matching using untransformed key, 
# but traverse tree using transformed key
# non-empty proper binary tree with entries being stored at internal nodes
# inject an external node for root
# entries are (key, value) pairs
# key_transform refers to a function that is applied to the stored version of key
# when we retrieve entries, keys are not transformed
# also, when we provide keys as arguments, they are not transformed
# comparator refers to a function that is applied to pairs of keys
class BinarySearchTree(BinaryTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    BinaryTree.__init__(self)
    self.num_entries = 0
    self.addRoot(None)
    self.key_transform = key_transform
    self.comparator = comparator
  def getKeyTransform(self):
    return self.key_transform
  def getComparator(self):
    return self.comparator
  def setComparator(self, comparator):
    self.comparator = comparator
  """
  # over-riding previous implementation
  #   so that we have an exception 
  #   raised when the tree is empty
  def getRoot(self):
    if self.isEmpty() == True:
      raise Exception("tree is empty")
    return self.root
  """
  """
  def size(self):
    return self.num_entries
  """
  def getNumEntries(self):
    return self.num_entries
  """
  def isEmpty(self):
    return self.num_entries == 0
  """
  def hasNoEntries(self):
    return self.getNumEntries() == 0
  # entries are (key, value) pairs
  @staticmethod
  def construct(entries):
    tree = BinarySearchTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  # use tree's key transform
  def _treeSearch(self, key, node):
    key_transform = self.getKeyTransform()
    comparator = self.getComparator()
    transformed_key = key_transform(key)
    return self._treeSearchHelper(transformed_key, node, key_transform, comparator)
  # use pre-transformed key
  # also specify a key transform and a comparator
  def _treeSearchWithTransformedKey(self, transformed_key, node, key_transform, comparator):
    # key_transform = self.getKeyTransform()
    return self._treeSearchHelper(transformed_key, node, key_transform, comparator)
  # return a node
  def _treeSearchHelper(self, transformed_key, node, key_transform, comparator):
    if node.isExternal() == True:
      return node
    else:
      curr_key = node.getElement().getKey()
      # comparator = self.getComparator()
      # key_transform = self.getKeyTransform()
      # transformed_key = key_transform(key)
      curr_transformed_key = key_transform(curr_key)
      # print transformed_key, curr_transformed_key
      if comparator(transformed_key, curr_transformed_key) == 0:
        # print "tree search case 1"
        return node
      elif comparator(transformed_key, curr_transformed_key) < 0:
        # print "tree search case 2"
        return self._treeSearchHelper(transformed_key, node.getLeftChild(), key_transform, comparator)
      elif comparator(transformed_key, curr_transformed_key) > 0:
        # print "tree search case 3"
        return self._treeSearchHelper(transformed_key, node.getRightChild(), key_transform, comparator)
      # print "falling through"
  """
  # return a node
  # match and traverse using transformed key
  # consider this method to be protected, not private
  # treat as deterministic given a collection of nodes
  # return a node
  @staticmethod
  def _treeSearch(tree, transformed_key, node):
    return tree._treeSearchHelper(transformed_key, node, traverse_prov_key_transform, traverse_key_transform, match_prov_key_transform, match_key_transform)
  """
  """
  # matching using untransformed key, but use transformed key for traversing
  # return a node
  @staticmethod
  def _treeSearchWithUntransformedKey(tree, untransformed_key, node):
    return tree._treeSearchHelper(untransformed_key, node, traverse_prov_key_transform, traverse_key_transform, match_prov_key_transform, match_key_transform)
  """
  # return an (entry, node) pair
  def find(self, key):
    node = self._treeSearch(key, self.getRoot())
    self.action_node = node
    if node.isInternal() == True:
      entry = node.getElement()
      return (entry, node)
    else:
      return None
  # preserve provided external node object and turn it into an internal node
  def _expandExternalHelper(self, external_node, left_entry, right_entry, node_class):
    node = external_node
    left_child = node_class(left_entry, node, None, None)
    right_child = node_class(right_entry, node, None, None)
    node.setLeftChild(left_child)
    node.setRightChild(right_child)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, Node)
  # auxiliary method
  def _insertAtExternal(self, external_node, entry):
    self._expandExternal(external_node, None, None)
    node = external_node
    self._replaceEntry(node, entry)
    self.num_entries = self.num_entries + 1
    return entry
  # treat as deterministic given a collection of nodes
  def _insertRetrieveNode(self, key, value):
    ins_node = self._treeSearch(key, self.getRoot())
    # print ins_node
    while not ins_node.isExternal():
      ins_node = self._treeSearch(key, ins_node.getLeftChild())
    return ins_node
  # return an entry
  def _insertIntroduceEntry(self, key, value, ins_node):
    return self._insertIntroduceEntryHelper(key, value, ins_node, Entry)
  def _insertIntroduceEntryHelper(self, key, value, ins_node, entry_class):
    return self._insertAtExternal(ins_node, entry_class(key, value))
  # return an (entry, node) pair
  def insert(self, key, value):
    # print key, value
    ins_node = self._insertRetrieveNode(key, value)
    self.action_node = ins_node
    entry = self._insertIntroduceEntry(key, value, ins_node)
    return (entry, ins_node)
    # print ins_node.getElement().toString()
  """
  # return an entry
  def insertWithUntransformedKey(self, untransformed_key, value):
    return (self._insertHelper(untransformed_key, value, self.treeSearchWithUntransformedKey)
  """
  def _removeRetrieveNode(self, entry):
    # two cases:
    # - have at least one child that is an external node
    # - have two children that are internal nodes
    # assume relevant (key, value) pair exists
    key = entry.getKey()
    value = entry.getValue()
    # print key, value
    # print "key:", key.toString()
    curr_node = self._treeSearch(key, self.getRoot())
    return curr_node
  def _removeRetrieveReplacementNode(self, found_node):
    curr_node = found_node
    # print self.getRoot().getElement().getKey()
    # print "key:", curr_node.getElement().getKey()
    # rem_node is an external node
    # for case 2, parent of rem_node is used to fill void
    rem_node = None
    if curr_node.getLeftChild().isExternal() == True:
      rem_node = curr_node.getLeftChild()
    elif curr_node.getRightChild().isExternal() == True:
      # print "current key:", curr_node.getElement().getKey()
      # print "current key, again:", curr_node.getRightChild().getParent().getElement().getKey()
      # print "found node's entry:", curr_node.getElement().toString()
      rem_node = curr_node.getRightChild()
    else:
      # w: node to be removed
      # y: left-most internal node in right subtree of w
      # x: left child of y
      # y takes place of w, x removed, right subtree of y takes place of y
      w = curr_node
      x = curr_node
      x = x.getRightChild()
      while x.isInternal() == True:
        x = x.getLeftChild()
      rem_node = x
    # print rem_node.getElement().getKey()
    # print rem_node.getLeftChild().getElement().getKey()
    return rem_node
  # return an (entry, node) pair
  def _removeHelper(self, node):
    w = node
    rem_node = self._removeRetrieveReplacementNode(w)
    # to_return = rem_node.getElement()
    to_return = w.getElement()
    if w.isInternal() == True:
      x = rem_node
      y_entry = x.getParent().getElement()
      # print "key:", y_entry.getKey()
      self._replaceEntry(w, y_entry)
      # w object is kept, and x and y objects are removed
      # note that w value is removed and y value is kept
    # effectively replace y with x's sibling
    # opt to store for action node the sibling of x
    self.action_node = rem_node.getSibling()
    self._removeExternal(rem_node)
    # print "root key:", self.getRoot().getElement().getKey()
    return (to_return, rem_node)
  # return an (entry, node) pair
  def remove(self, entry):
    # print entry.getKey().toString()
    w = self._removeRetrieveNode(entry)
    return self._removeHelper(w)
  # entry can be non-existent, in which case it is None
  def _replaceEntry(self, node, entry):
    node.setElement(entry)
  # auxiliary method
  def _removeExternal(self, node):
    # print node.getParent().getElement().toString()
    self._removeAboveExternal(node)
    self.num_entries = self.num_entries - 1
  # if v has a parent, 
  # set u to be child of v's parent; 
  # if v does not have a parent, 
  # then it is root, and we set 
  # u to be root
  # note: make sure that v's ancestors
  # are currently appropriate
  # note: v is potentially root
  def _upperSituate(self, u, v):
    # print u.getElement().getKey()
    # print v.getElement().getKey()
    v_parent = v.getParent()
    if v_parent != None:
      if v.isLeftChild():
        v_parent.setLeftChild(u)
      else:
        v_parent.setRightChild(u)
    if v == self.getRoot():
      self._setRoot(u)
  # u is target, v is intended parent
  # u can be nonexistent, an internal node, or an external node
  def _lowerSituate(self, u, v):
    if u == None:
      return
    else:
      u.setParent(v)
  # two approaches:
  # - change by introducing new object
  # - change by re-using existing object
  # given node is an external node
  # parent of given node might not have a parent; 
  # deal with existing object that is 
  # for parent of given node
  def _removeAboveExternal(self, external_node):
    # naming of variables along lines of case one, 
    # even though we have two different cases 
    # that we can handle
    # w: internal node to be removed
    # z: external node to be removed and child of w
    # sibling of z moves into position of w
    z = external_node
    # print "external node:", z.getElement().getKey()
    w = z.getParent()
    # z's parent can also be called w
    # print "internal node:", w.getElement().getKey()
    z_sibling = z.getSibling()
    # print "sibling node:", z_sibling.getElement().getKey()
    w_parent = w.getParent()
    # print "root before:", self.getRoot().getElement().getKey()
    self._upperSituate(z_sibling, w)
    # print "root after:", self.getRoot().getElement().getKey()
    z_sibling.setParent(w_parent)
    # print w_parent
    # print w.getElement().getKey()
    """
    # print (x, y)
    sibling = node.getSibling()
    # change y
    self._replaceEntry(y, sibling.getElement())
    y.setLeftChild(sibling.getLeftChild())
    y.setRightChild(sibling.getRightChild())
    """
  def _addAll(self, L, node, key):
    if node.isExternal() == True:
      return
    node = self._treeSearch(key, node)
    if node.isExternal() == False:
      self._addAll(L, node.getLeftChild(), key)
      entry = node.getElement()
      L.append(entry)
      self._addAll(L, node.getRightChild(), key)
  """
  def addAllWithUntransformedKey(self, L, node, key):
    return self._addAllHelper(L, node, key, self.treeSearchWithUntransformedKey)
  """
  def findAll(self, key):
    L = []
    self._addAll(L, self.getRoot(), key)
    return L
  """
  def findAllWithUntransformedKey(self, key):
    return self._findAllHelper(key, self.addAllWithUntransformedKey)
  """
  # retrieve internal nodes
  # takes O(n) time
  def toInorderInternalNodeList(self):
    # return self._toInorderInternalNodeListHelper(self.getRoot())
    return self._toInorderInternalNodeListHelper(self.getRoot())
  def _toInorderInternalNodeListHelper(self, node):
    if node.isExternal():
      return []
    # print node.getElement().toKeyString()
    left_nodes = self._toInorderInternalNodeListHelper(node.getLeftChild())
    # current_nodes = []
    current_nodes = [node]
    right_nodes = self._toInorderInternalNodeListHelper(node.getRightChild())
    result_nodes = left_nodes + current_nodes + right_nodes
    return result_nodes
"""
# t1 = BinarySearchTree.construct([(1, 1), (2, 1), (3, 1), (4, 1)])
t1 = BinarySearchTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1)])
print t1.toString()
t1.remove(Entry(32, 1))
t1.remove(Entry(65, 1))
print t1.toInorderList()
t1.insert(17, 1)
print t1.find(17)
print t1.findAll(17)
"""
"""
t3 = BinarySearchTree.construct([(17, 1), (28, 1), (29, 1)])
print t3.toInorderList()
t3.remove(Entry(28, 1))
print t3.toInorderList()
"""
"""
t4 = BinarySearchTree.construct([(17, 1)])
print t4.toString()
t4.remove(Entry(17, 1))
print t4.toString()
"""
