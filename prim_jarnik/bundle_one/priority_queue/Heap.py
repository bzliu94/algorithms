from ..tree.CompleteBinaryTree import *
from ..tree.Entry import *
from ..Util import *
# complete binary tree that satisfies heap-order property
# min-heap
class Heap(CompleteBinaryTree):
  def __init__(self, comparator = comp):
    CompleteBinaryTree.__init__(self)
    self.comparator = comparator
  def size(self):
    return CompleteBinaryTree.getSize(self)
  def isEmpty(self):
    return CompleteBinaryTree.isEmpty(self)
  # retrieve an entry object
  def min(self):
    return self.getRoot().getElement()
  def _swap(self, x, y):
    temp = x.getElement()
    self.replace(x, y.getElement())
    self.replace(y, temp)
  # up-heap bubbling
  # have an item to move upwards
  # v is node that serves as resting position for entry
  # return a node that holds entry that is initially associated with v
  def _upHeap(self, v):
    u = None
    while self.getRoot() != v:
      u = v.getParent()
      # if u.getElement().getKey() <= v.getElement().getKey():
      if comp(u.getElement().getKey(), v.getElement().getKey()) <= 0:
        break
      else:
        self._swap(u, v)
        v = u
    return v
  # down-heap bubbling
  # have a hole to move downwards
  # r is node that serves as resting position for entry
  # return a node that holds entry that is initially associated with r
  def _downHeap(self, r):
    while r.isInternal() == True:
      s = None
      if not r.hasRightChild():
        s = r.getLeftChild()
      # elif r.getLeftChild().getElement().getKey() <= r.getRightChild().getElement().getKey():
      elif comp(r.getLeftChild().getElement().getKey(), r.getRightChild().getElement().getKey()) <= 0:
        s = r.getLeftChild()
      else:
        s = r.getRightChild()
      # print s.getElement(), r.getElement()
      # print "root entry:", r.getElement().getKey()
      # print "second entry:", (self.T)[2].getElement().getKey()
      # if s.getElement().getKey() < r.getElement().getKey():
      if comp(s.getElement().getKey(), r.getElement().getKey()) == -1:
        self._swap(r, s)
        r = s
      else:
        break
    return r
  # returns an entry
  def insert(self, k, x):
    node = self._insertHelper(k, x, Entry)
    entry = node.getElement()
    return entry
  # returns a node
  def _insertHelper(self, k, x, entry_class):
    # print "insert priority value:", k
    # self._upHeap(node)
    entry = entry_class(k, x)
    # print k, x
    node = self.add(entry)
    # print entry, node.getElement()
    final_node = self._upHeap(node)
    """
    print entry == entry.getLocation().getElement()
    """
    """
    print "inserting a node and have following event types:", x.isCircleEvent(), node.getElement().getValue().isCircleEvent()
    print entry == node.getElement()
    print entry, node.getElement()
    """
    return final_node
  # remove an arbitrary node
  # returns an entry
  def _removeHelper(self, v):
    entry = v.getElement()
    if self.getSize() == 1:
      self.removeLastItem()
    else:
      self.replace(v, self.removeLastItem())
      # print self.getSize()
      # print self.getRoot().getElement()
      """
      self._downHeap(v)
      """
      # both to support generalized remove
      # doing both without certain checks 
      #   may in a sense be excessive
      self._upHeap(v)
      self._downHeap(v)
    return entry
  # returns an entry
  def removeMin(self):
    if self.isEmpty() == True:
      raise Exception("heap is empty")
    else:
      result = self._removeHelper(self.getRoot())
      # print "removal of an entry with minimal key priority value:", result.getKey()
      return result
"""
h1 = Heap()
h1.insert(1, 1)
h1.insert(2, 1)
h1.insert(3, 1)
print h1.min().toString()
print h1.removeMin().toString()
print h1.toString()
"""
"""
[4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 20, 25]
h2 = Heap()
h2.insert(4, 1)
h2.insert(5, 1)
h2.insert(6, 1)
h2.insert(7, 1)
h2.insert(9, 1)
h2.insert(11, 1)
h2.insert(12, 1)
h2.insert(13, 1)
h2.insert(14, 1)
h2.insert(15, 1)
h2.insert(16, 1)
h2.insert(20, 1)
h2.insert(25, 1)
print h2.toString()
print h2.removeMin().toString()
print h2.toString()
print h2.removeMin()
"""


