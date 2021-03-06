from ..DoublyLinkedListNode import *

class LabelAwareDoublyLinkedListNode(DoublyLinkedListNode):

  """

  def __init__(self, element, prev, next):

    DoublyLinkedListNode.__init__(self, element, prev, next)

  """

  def __init__(self, element, prev, next, label = None):

    DoublyLinkedListNode.__init__(self, element, prev, next)

    self.label = label

  def getLabel(self):

    return self.label

  def setLabel(self, label):

    self.label = label

