from Node import *
class OrderedBinarySearchTreeNode(Node):
  def __init__(self, element, parent, left_child, right_child, prev = None, next = None):
    Node.__init__(self, element, parent, left_child, right_child)
    self.prev = prev
    self.next = next
  def getPrev(self):
    return self.prev
  def getNext(self):
    return self.next
  def setPrev(self, prev):
    self.prev = prev
  def setNext(self, next):
    self.next = next
