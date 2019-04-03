# for use with DoublyLinkedListNode objects
from DoublyLinkedListNode import *
class DoublyLinkedList:
  def __init__(self):
    # two sentinels
    # self.header = DoublyLinkedListNode(None, None, None)
    self.header = self._createNode(None, None, None)
    # self.trailer = DoublyLinkedListNode(None, self.header, None)
    self.trailer = self._createNode(None, self.header, None)
    (self.header).setNext(self.trailer)
    self.size = 0
  def _createNode(self, item, prev, next):
    node = DoublyLinkedListNode(item, prev, next)
    return node
  def _getHeaderSentinel(self):
    return self.header
  def _getTrailerSentinel(self):
    return self.trailer
  def getSize(self):
    return self.size
  def _setSize(self, size):
    self.size = size
  def isEmpty(self):
    return self.getSize() == 0
  # add a node before a given node
  # in particular, add node v before node z
  def addBefore(self, v, z):
    w = z.getPrev()
    v.setPrev(w)
    v.setNext(z)
    w.setNext(v)
    z.setPrev(v)
    self.size = self.size + 1
  # add a node after a given node
  # in particular, add node v after node z
  def addAfter(self, v, z):
    # print v.getNext()
    w = z.getNext()
    v.setPrev(z)
    v.setNext(w)
    w.setPrev(v)
    z.setNext(v)
    self.size = self.size + 1
  # remove a node
  def remove(self, v):
    u = v.getPrev()
    w = v.getNext()
    w.setPrev(u)
    u.setNext(w)
    v.setPrev(None)
    v.setNext(None)
    self.size = self.size - 1
  # insert a node at head of list
  def addFirst(self, v):
    self.addAfter(v, self.header)
  # insert a node at end of list
  def addLast(self, v):
    self.addBefore(v, self.trailer)
  # get first node in list
  def getFirst(self):
    if self.isEmpty():
      raise Exception("list is empty")
    return (self.header).getNext()
  # get last node in list
  def getLast(self):
    if self.isEmpty():
      raise Exception("list is empty")
    return (self.trailer).getPrev()
  # have non-sentinel predecessor
  def hasPredecessor(self, node):
    predecessor = node.prev
    has_predecessor = not (predecessor == None or predecessor == self._getHeaderSentinel())
    return has_predecessor
  # have non-sentinel successor
  def hasSuccessor(self, node):
    successor = node.next
    has_successor = not (successor == None or successor == self._getTrailerSentinel())
    return has_successor
  """
  def toString(self):
    element_list = self.toElementList()
    element_str_list = [str(x) for x in element_list]
    element_str = "".join(element_str_list)
    return element_str
  """
  # this is destructive and constant-time
  @staticmethod
  def concatenate(dll1, dll2):
    # modify header, trailer, size
    header1 = dll1._getHeaderSentinel()
    trailer1 = dll1._getTrailerSentinel()
    if dll1.getSize() == 0:
      return dll2
    elif dll2.getSize() == 0:
      return dll1
    else:
      last_element1 = dll1.getLast()
      first_element2 = dll2.getFirst()
      last_element2 = dll2.getLast()
      last_element1.setNext(first_element2)
      first_element2.setPrev(last_element1)
      last_element2.setNext(trailer1)
      trailer1.setPrev(last_element2)
      size1 = dll1.getSize()
      size2 = dll2.getSize()
      next_size = size1 + size2
      dll1._setSize(next_size)
      return dll1
  def toElementList(self):
    return self._toElementListHelper(self._getHeaderSentinel(), [])
  def _toElementListHelper(self, node, partial_element_list):
    if self._getTrailerSentinel() == node:
      return partial_element_list
    elif self._getHeaderSentinel() == node:
      return self._toElementListHelper(node.getNext(), partial_element_list)
    else:
      curr_element = node.getElement()
      return self._toElementListHelper(node.getNext(), partial_element_list + [curr_element])
  # retrieve a list of non-sentinel nodes
  def _toNodeList(self):
    return self._toNodeListHelper(self._getHeaderSentinel(), [])
  def _toNodeListHelper(self, node, partial_node_list):
    if self._getTrailerSentinel() == node:
      return partial_node_list
    elif self._getHeaderSentinel() == node:
      return self._toNodeListHelper(node.getNext(), partial_node_list)
    else:
      return self._toNodeListHelper(node.getNext(), partial_node_list + [node])

if __name__ == '__main__':

  list1 = DoublyLinkedList()
  node1 = DoublyLinkedListNode(1, None, None)
  node2 = DoublyLinkedListNode(2, None, None)
  node3 = DoublyLinkedListNode(3, None, None)
  node4 = DoublyLinkedListNode(4, None, None)
  list1.addFirst(node1)
  list1.addLast(node4)
  list1.addBefore(node3, node4)
  list1.addAfter(node2, node1)
  print list1.toElementList()
  print list1._toNodeList()
  print [x.getElement() for x in list1._toNodeList()]

  list2 = DoublyLinkedList()
  node5 = DoublyLinkedListNode(5, None, None)
  list2.addFirst(node5)
  print list2.toElementList()

  list3 = DoublyLinkedList.concatenate(list2, list1)
  print list3.toElementList()

  list4 = DoublyLinkedList()
  node6 = DoublyLinkedListNode(6, None, None)
  list4.addFirst(node6)
  list5 = DoublyLinkedList()
  list6 = DoublyLinkedList.concatenate(list4, list5)
  print list6.toElementList()


