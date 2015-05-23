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

"""

list = DoublyLinkedList()

node1 = DoublyLinkedListNode(1, None, None)

node2 = DoublyLinkedListNode(2, None, None)

node3 = DoublyLinkedListNode(3, None, None)

node4 = DoublyLinkedListNode(4, None, None)

list.addFirst(node1)

list.addLast(node4)

list.addBefore(node3, node4)

list.addAfter(node2, node1)

print list.toElementList()

print list._toNodeList()

print [x.getElement() for x in list._toNodeList()]

"""

