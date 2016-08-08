from BinarySearchTree import *
from LocationAwareEntry import *
class LocationAwareBinarySearchTree(BinarySearchTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    BinarySearchTree.__init__(self, key_transform, comparator)
  @staticmethod
  def construct(entries):
    tree = BinarySearchTree()
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def insert(self, key, value):
    result = BinarySearchTree.insert(self, key, value)
    entry, node = result
    entry.setLocation(node)
    return result
  def _replaceEntry(self, node, entry):
    BinarySearchTree._replaceEntry(self, node, entry)
    entry.setLocation(node)
  def _insertIntroduceEntry(self, key, value, ins_node):
    return self._insertIntroduceEntryHelper(key, value, ins_node, LocationAwareEntry)
"""
from LocationAwareEntry import *
tree = LocationAwareBinarySearchTree()
entry1, node1 = tree.insert(1, 1)
entry2, node2 = tree.insert(2, 1)
entry3, node3 = tree.insert(3, 1)
print entry1.getLocation().getElement().getKey()
print entry2.getLocation().getElement().getKey()
print entry3.getLocation().getElement().getKey()
"""
