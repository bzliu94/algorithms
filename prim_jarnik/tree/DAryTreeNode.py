class DAryTreeNode:
  # children should be a list, but is not defined by default 
  # because erroneously the same empty list would be used 
  # for all those all nodes with default children list
  def __init__(self, element, parent, children):
    self.element = element
    self.parent = parent
    self.children = children
  def getElement(self):
    return self.element
  def getParent(self):
    return self.parent
  def getChildren(self):
    return self.children
  def setElement(self, element):
    self.element = element
  def setParent(self, parent):
    self.parent = parent
  def addChild(self, node):
    self.children.append(node)
  def removeChild(self, node):
    self.children.remove(node)
  def hasChildren(self):
    return len(self.children) != 0
  def hasParent(self):
    return self.getParent() != None
  def isAChild(self):
    if self.hasParent() == False:
      return False
    else:
      parent = self.getParent()
      return self in parent.getChildren()
  def isInternal(self):
    return self.hasChildren()
  def isExternal(self):
    return not self.isInternal()
  def hasElement(self):
    return self.getElement() != None
  """
  def hasNonExternalNodeChild(self):
    if self.isExternal() == True:
      return False
    else:
      left_child_is_not_external = self.getLeftChild().isExternal() == False
      right_child_is_not_external = self.getRightChild().isExternal() == False
      return left_child_is_not_external or right_child_is_not_external
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
