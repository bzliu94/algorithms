# 2019-10-08

# top layer is for x, lower layer is for y; 
# for each node in x layer we store canonical subset (i.e. all points in subtree); 
# y tree for an x layer node is called associated tree

# import pdb
from collections import defaultdict
from RedBlackTree import *
from TwoDRangeTreeNode import *
from OneDRangeTree import *

class TwoDRangeTree(RedBlackTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    RedBlackTree.__init__(self, key_transform, comparator)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, TwoDRangeTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, TwoDRangeTreeNode)

  @staticmethod
  def construct(points_2d):
    tree = TwoDRangeTree()
    entries = [(x[0], x) for x in points_2d]
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    TwoDRangeTree.setCanonicalSubsets(tree)
    internal_nodes = tree.toInorderList()
    for node in internal_nodes:
      next_tree = OneDRangeTree()
      curr_canonical_subset = node.getCanonicalSubset()
      next_points = [x.getElement().getValue() for x in curr_canonical_subset]
      next_entries = [(x[1], x) for x in next_points]
      for next_entry in next_entries:
        next_key, next_value = next_entry
        next_tree.insert(next_key, next_value)
      node.setAssociatedTree(next_tree)
      # print next_tree
    return tree

  @staticmethod
  def setCanonicalSubsets(x_tree):
    internal_nodes = x_tree.toInorderList()
    for internal_node in internal_nodes:
      curr_canonical_subset = x_tree.toInorderListRooted(internal_node)
      internal_node.setCanonicalSubset(curr_canonical_subset)
      # print len(curr_canonical_subset)

  # we use pseudocode from de berg et al, but that assumes we store items at leaves, 
  # when in reality we store items in internal nodes
  def findSplitNode(self, x1, x2):
    v = self.getRoot()
    key_transform = self.getKeyTransform()
    comp = self.getComparator()
    while v.isExternal() == False and ((comp(x2, key_transform(v.getElement().getKey())) <= 0) or (comp(x1, key_transform(v.getElement().getKey())) == 1)):
      if comp(x2, key_transform(v.getElement().getKey())) <= 0:
        v = v.getLeftChild()
      else:
        v = v.getRightChild()
    return v
  # top layer of 2-d range tree is x
  def twoDRangeQuery(self, x1, x2, y1, y2):
    result = []
    self.twoDRangeQueryHelper(x1, x2, y1, y2, result)
    next_result = [x.getElement().getValue() for x in result]
    return next_result
  # if split node is external, consider its parent; assume n >= 1
  def twoDRangeQueryHelper(self, x1, x2, y1, y2, result):
    # pdb.set_trace()
    key_transform = self.getKeyTransform()
    comp = self.getComparator()
    v_split = self.findSplitNode(x1, x2)
    if v_split.isExternal() == True:
      return
    else:
      # current
      x_key = v_split.getElement().getValue()[0]
      y_key = v_split.getElement().getValue()[1]
      if comp(key_transform(x_key), x1) >= 0 and comp(key_transform(x_key), x2) <= 0 \
       and comp(key_transform(y_key), y1) >= 0 and comp(key_transform(y_key), y2) <= 0:
        result.append(v_split)
      # left
      v = v_split.getLeftChild()
      while v.isExternal() == False:
        x_key = v.getElement().getValue()[0]
        y_key = v.getElement().getValue()[1]
        # current
        if comp(key_transform(x_key), x1) >= 0 and comp(key_transform(x_key), x2) <= 0 \
         and comp(key_transform(y_key), y1) >= 0 and comp(key_transform(y_key), y2) <= 0:
          result.append(v)
        if comp(x1, key_transform(x_key)) <= 0:
          nodes = self.reportSubtree(v.getRightChild())
          for node in nodes:
            node.getAssociatedTree().oneDRangeQueryHelper(y1, y2, result)
            # result.append(node)
          v = v.getLeftChild()
        else:
          v = v.getRightChild()
      # key = v.getParent().getElement().getKey()
      # if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
      #   result.append(v.getParent())
      # right
      v = v_split.getRightChild()
      while v.isExternal() == False:
        x_key = v.getElement().getValue()[0]
        y_key = v.getElement().getValue()[1]
        # current
        if comp(key_transform(x_key), x1) >= 0 and comp(key_transform(x_key), x2) <= 0 \
         and comp(key_transform(y_key), y1) >= 0 and comp(key_transform(y_key), y2) <= 0:
          result.append(v)
        if comp(key_transform(x_key), x2) <= 0:
          nodes = self.reportSubtree(v.getLeftChild())
          for node in nodes:
            node.getAssociatedTree().oneDRangeQueryHelper(y1, y2, result)
            # result.append(node)
          v = v.getRightChild()
        else:
          v = v.getLeftChild()
      # key = v.getParent().getElement().getKey()
      # if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
      #   result.append(v.getParent())
      
  def reportSubtree(self, node):
    return self.toInorderListRooted(node)

"""

# points are degenerate intervals

tree = TwoDRangeTree()
one_d_points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (-2, 0), (-2, 4)]
tree = TwoDRangeTree.construct(one_d_points)

print tree.toString()

node = tree.findSplitNode(2, 3)

print node.getElement().toString()

result = tree.twoDRangeQuery(-2, 2, -10, 10)

print result

print tree.reportSubtree(tree.getRoot().getRightChild())

print tree.twoDRangeQuery(-2, 3, -10, 10)
print tree.twoDRangeQuery(-2.5, 3.1, -10, 10)
print tree.twoDRangeQuery(2.5, 2.6, -10, 10)

print tree.twoDRangeQuery(-10, 10, -10, 10)

"""


