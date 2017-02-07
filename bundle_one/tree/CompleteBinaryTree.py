from Node import *
# array list representation of a complete binary tree
class CompleteBinaryTree():
  def __init__(self):
    self.T = []
    self.T.append(None)
  def getSize(self):
    return len(self.T) - 1
  def isEmpty(self):
    return self.getSize() == 0
  def getRoot(self):
    if self.isEmpty():
      raise Exception("tree is empty")
      # return (self.T)[0]
    else:
      # print "tree:", self.T
      return (self.T)[1]
  def replace(self, v, o):
    v.setElement(o)
  # return node added
  def add(self, e):
    i = self.getSize() + 1
    parent_ind = i / 2
    # print parent_ind, self.T
    parent = (self.T)[parent_ind]
    is_left_child = i % 2 == 0
    node = Node(e, parent, None, None)
    if self.getSize() > 0:
      if is_left_child == True:
        parent.setLeftChild(node)
      else:
        parent.setRightChild(node)
    (self.T).append(node)
    """
    if e != node.getElement():
      raise Exception("see entry mismatch")
    """
    return node
  # returns an element corresponding to last node
  # according to ordering imposed by complete binary tree
  def removeLastItem(self):
    if self.isEmpty():
      raise Exception("tree is empty")
    else:
      removed_node = (self.T).pop()
      i = self.getSize() + 1
      parent_ind = i / 2
      parent = (self.T)[parent_ind]
      is_left_child = i % 2 == 0
      if self.getSize() > 0:
        if is_left_child == True:
          parent.setLeftChild(None)
        else:
          parent.setRightChild(None)
      return removed_node.getElement()
  # assume that we have entries, and keys cannot be None
  def toString(self):
    return self._toString(self.getRoot())
  def _toString(self, node):
    if node == None:
      # non-existent node
      return "None"
    else:
      left_child_str = self._toString(node.getLeftChild())
      curr_element = node.getElement()
      if curr_element != None:
        curr_entry_str = str(node.getElement().toKeyString())
      else:
        # non-existent key (possibly because entry does not exist)
        curr_entry_str = "None"
      right_child_str = self._toString(node.getRightChild())
      partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"
      return partial_str
