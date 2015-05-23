from Node import *

from Entry import *

class BinaryTree:

  def __init__(self):

    # self.size = 0

    self.root = None
    
  def _addRootHelper(self, element, node_class):
  
    self.root = node_class(element, None, None, None)

  def addRoot(self, element):

    self._addRootHelper(element, Node)

  def _setRoot(self, node):

    self.root = node

  def getRoot(self):

    return self.root

  """

  def size(self):

    return self.size

  def isEmpty(self):

    return self.size() == 0

  """

  # get a string representation of entries

  # for nodes visited using in-order traversal

  def toInorderList(self):

    root = self.getRoot()

    return self._toInorderListHelper(root)

  def _toInorderListHelper(self, node):

    if node.isExternal():

      return []

    else:

      left_child = node.getLeftChild()

      right_child = node.getRightChild()

      # print left_child, right_child

      """

      print node.getElement().toString()

      left_child_entry = left_child.getElement()

      if left_child_entry != None:

        print left_child_entry.toString()

      """

      entry_list_left = []

      entry_list_right = []

      if node.hasLeftChild():

        entry_list_left = self._toInorderListHelper(left_child)

      curr_entry = node.getElement()

      """

      curr_entry_list = []

      if curr_entry != None:

        curr_entry_list = [curr_entry.toString()]

      """

      curr_entry_list = [curr_entry.toString()]

      if node.hasRightChild():

        entry_list_right = self._toInorderListHelper(right_child)

      entry_list = entry_list_left + curr_entry_list + entry_list_right

      return entry_list

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

        curr_entry_str = curr_element.toKeyString()

        # curr_entry_str = node.toKeyString()

      else:

        # non-existent key (possibly because entry does not exist)

        curr_entry_str = "None"

      right_child_str = self._toString(node.getRightChild())

      partial_str = "(" + curr_entry_str + " " + left_child_str + " " + right_child_str + ")"

      return partial_str

  def replace(self, v, o):

    v.setElement(o)

"""

t5 = BinaryTree()

n1 = Node(Entry(29, 1), None, None, None)

n2 = Node(Entry(28, 1), n1, None, None)

n3 = Node(Entry(17, 1), n2, None, None)

t5._setRoot(n1)

n1.setLeftChild(n2)

n2.setLeftChild(n3)

print t5.toString()

"""

