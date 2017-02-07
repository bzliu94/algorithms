class DoublyLinkedListNode:
  def __init__(self, element, prev, next):
    self.element = element
    self.prev = prev
    self.next = next
  def getElement(self):
    return self.element
  def getPrev(self):
    return self.prev
  def getNext(self):
    return self.next
  def setElement(self, element):
    self.element = element
  def setPrev(self, prev):
    self.prev = prev
  def setNext(self, next):
    self.next = next
