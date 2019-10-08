class Node:
  def __init__(self, element, parent, left_child, right_child):
    self.element = element
    self.parent = parent
    self.left_child = left_child
    self.right_child = right_child
  def getElement(self):
    return self.element
  def getParent(self):
    return self.parent
  def getLeftChild(self):
    return self.left_child
  def getRightChild(self):
    return self.right_child
  def setElement(self, element):
    self.element = element
  def setParent(self, parent):
    self.parent = parent
  def setLeftChild(self, node):
    self.left_child = node
  def setRightChild(self, node):
    self.right_child = node
  def getSibling(self):
    parent = self.getParent()
    if parent.getLeftChild() == self:
      return parent.getRightChild()
    else:
      return parent.getLeftChild()
  def hasLeftChild(self):
    return self.getLeftChild() != None
  def hasRightChild(self):
    return self.getRightChild() != None
  def hasParent(self):
    return self.getParent() != None
  def isLeftChild(self):
    if self.hasParent() == False:
      return False
    else:
      parent = self.getParent()
      return parent.getLeftChild() == self
  def isRightChild(self):
    if self.hasParent() == False:
      return False
    else:
      parent = self.getParent()
      return parent.getRightChild() == self
  def isInternal(self):
    return self.hasLeftChild() or self.hasRightChild()
  def isExternal(self):
    return not self.isInternal()
  def hasElement(self):
    return self.getElement() != None

  def hasChildren(self):
    return self.hasLeftChild() or self.hasRightChild()
  """
  def isNonStandardExternal(self):
    if self.isExternal() == True:
      return False
    else:
      if self.hasChildren() == True:
        if self.hasLeftChild() == True and self.getLeftChild().isExternal() == False:
        return False
      if self.hasRightChild() == True and self.getRightChild().isExternal() == False:
        return True
      return False
  """
  # show string corresponding to entry
  def toString(self):
    if self.hasElement() == False:
      return None
    else:
      return self.getElement().toString()
  # show only key corresponding to entry
  def toKeyString(self):
    if self.hasElement() == False:
      return None
    else:
      return self.getElement().toKeyString()
