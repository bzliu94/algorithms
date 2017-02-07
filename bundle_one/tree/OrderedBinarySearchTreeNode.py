from Node import *
class OrderedBinarySearchTreeNode(Node):
  # def __init__(self, element, parent, left_child, right_child, prev = None, next = None, prev_external, next_external):
  def __init__(self, element, parent, left_child, right_child, prev = None, next = None):
    Node.__init__(self, element, parent, left_child, right_child)
    self.prev = prev
    self.next = next
    """
    self.prev_external = prev_external
    self.next_external = next_external
    """
  def getPrev(self):
    return self.prev
  def getNext(self):
    return self.next
  def setPrev(self, prev):
    self.prev = prev
  def setNext(self, next):
    self.next = next
  """
  def getPrevExternal(self):
    return self.prev_external
  def getNextExternal(self):
    return self.next_external
  def setPrevExternal(self, prev_external):
    self.prev_external = prev_external
  def setNextExternal(self, next_external):
    self.next_external = next_external
  """
