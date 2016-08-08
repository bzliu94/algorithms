from ..OrderedBinarySearchTree import *
from SplayTree import SplayTree
from ..Entry import *
from collections import defaultdict
class SubtreeEntryMemoizingSplayTree(SplayTree):
  def __init__(self, key_transform = lambda x: x, comparator = comp):
    SplayTree.__init__(self, key_transform, comparator)
    self.node_to_entry_collection_dict = defaultdict(lambda: [])
  @staticmethod
  def construct(entries, key_transform = lambda x: x, comparator = comp):
    tree = SubtreeEntryMemoizingSplayTree(key_transform, comparator)
    for entry in entries:
      key, value = entry
      tree.insert(key, value)
    return tree
  def crawlNodeToEntryCollectionDict(self):
    nodes = self.toInorderInternalNodeList()
    for node in nodes:
      entry = node.getElement()
      self.crawlNodeToEntryCollectionDictHelper(node, entry)
  def crawlNodeToEntryCollectionDictHelper(self, node, entry):
    if node == None:
      return
    else:
      parent = node.getParent()
      node_to_entry_collection_dict = self.getNodeToEntryCollectionDict()
      node_to_entry_collection_dict[node].append(entry)
      self.crawlNodeToEntryCollectionDictHelper(parent, entry)
  def getNodeToEntryCollectionDict(self):
    return self.node_to_entry_collection_dict
"""
t2 = SubtreeEntryMemoizingSplayTree.construct([(17, 1), (28, 1), (29, 1), (32, 1), (44, 1), (54, 1), (65, 1), (76, 1), (78, 1), (80, 1), (82, 1), (88, 1), (97, 1), (17, 1)])
t2.remove(LocationAwareEntry(32, 1))
print t2.toString()
print t2.toInorderList()
t2.remove(LocationAwareEntry(65, 1))
print t2.toInorderList()
"""
"""
t4 = SubtreeEntryMemoizingSplayTree.construct([(17, 1), (28, 1), (29, 1)])
print t4.toInorderList()
print t4.toString()
# t4.remove(LocationAwareEntry(28, 1))
# t4.remove(LocationAwareEntry(17, 1))
# t4.remove(LocationAwareEntry(32, 1))
print t4.toInorderList()
print t4.toString()
t4.crawlNodeToEntryCollectionDict()
result = t4.getNodeToEntryCollectionDict()
for item in result.items():
  node, entry_collection = item
  print "node:", node.toString()
  print "entries:", [x.toString() for x in entry_collection]
"""
