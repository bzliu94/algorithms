from RedBlackTree import *
from OneDRangeTreeNode import *

class OneDRangeTree(RedBlackTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    RedBlackTree.__init__(self, key_transform, comparator)
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, OneDRangeTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, OneDRangeTreeNode)

  @staticmethod
  def construct(points):
    tree = OneDRangeTree()
    entries = [(x, x) for x in points]
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree

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
  def oneDRangeQuery(self, x1, x2):
    result = []
    self.oneDRangeQueryHelper(x1, x2, result)
    next_result = [x.getElement().getValue() for x in result]
    return next_result
  # if split node is external, consider its parent; assume n >= 1
  def oneDRangeQueryHelper(self, x1, x2, result):
    # pdb.set_trace()
    key_transform = self.getKeyTransform()
    comp = self.getComparator()
    v_split = self.findSplitNode(x1, x2)
    """
    if v_split.isExternal() == True:
      key = v_split.getParent().getElement().getKey()
      if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
        result.append(v_split)
    else:
    """
    if v_split.isExternal() == True:
      return
    else:
      # current
      key = v_split.getElement().getKey()
      if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
        result.append(v_split)
      # left
      v = v_split.getLeftChild()
      while v.isExternal() == False:
        key = v.getElement().getKey()
        # current
        if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
          result.append(v)
        if comp(x1, key_transform(key)) <= 0:
          nodes = self.reportSubtree(v.getRightChild())
          for node in nodes:
            result.append(node)
          v = v.getLeftChild()
        else:
          v = v.getRightChild()
      # key = v.getParent().getElement().getKey()
      # if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
      #   result.append(v.getParent())
      # right
      v = v_split.getRightChild()
      while v.isExternal() == False:
        key = v.getElement().getKey()
        # current
        if comp(key_transform(key), x1) >= 0 and comp(key_transform(key), x2) <= 0:
          result.append(v)
        if comp(key_transform(key), x2) <= 0:
          nodes = self.reportSubtree(v.getLeftChild())
          for node in nodes:
            result.append(node)
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

tree = OneDRangeTree()
one_d_points = [0, 1, 2, 3, 4, 5, 6, -2]
tree = OneDRangeTree.construct(one_d_points)

# result = tree.rangeQuery([-2, 3])
# print result

print tree.toString()

node = tree.findSplitNode(2, 3)

print node.getElement().toString()

result = tree.oneDRangeQuery(-2, 2)

print result

print tree.reportSubtree(tree.getRoot().getRightChild())

print tree.oneDRangeQuery(-2, 3)
print tree.oneDRangeQuery(-2.5, 3.1)
print tree.oneDRangeQuery(2.5, 2.6)

"""


