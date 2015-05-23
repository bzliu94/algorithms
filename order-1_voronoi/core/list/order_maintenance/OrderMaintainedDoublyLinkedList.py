# avoid adding sentinels to label tree

# use a companion structure

# use path labels as keys

# from OrderMaintainedDoublyLinkedListNode import *

# from LabeledDoublyLinkedListNode import *

# from LabelAwareDoublyLinkedList import *

from ..DoublyLinkedList import *

from LabelTree import *

class OrderMaintainedDoublyLinkedList(DoublyLinkedList):

  def __init__(self):

    DoublyLinkedList.__init__(self)

    self.overlying_tree = LabelTree()

    # self.nodeToLabeledNodeDict = {}

    # self._addHeaderSentinelHelper()

    # self._addTrailerSentinelHelper()

  """

  def _getLabeledNodeForNode(self, node):

    return (self.nodeToLabeledNodeDict)[node]

  def _addNodeToLabeledNodeRelationship(self, node, labeled_node):

    (self.nodeToLabeledNodeDict)[node] = labeled_node

  def _removeNodeToLabeledNodeRelationship(self, node):

    (self.nodeToLabeledNodeDict).pop(node)

  """

  def _createNode(self, item, prev, next):

    node = DoublyLinkedListNode(item, prev, next)

    return node

  def _getOverlyingTree(self):

    # print "retrieving overlying tree"

    # return None

    return self.overlying_tree

  """

  def _addHeaderSentinelHelper(self):

    v = self._getHeaderSentinel()

    labeled_v = DoublyLinkedListNode(v)

    self._addNodeToLabeledNodeRelationship(v, labeled_v)

    self._getOverlyingTree().addFirst(labeled_v)

  def _addTrailerSentinelHelper(self):

    v = self._getTrailerSentinel()

    labeled_v = DoublyLinkedListNode(v)

    self._addNodeToLabeledNodeRelationship(v, labeled_v)

    self._getOverlyingTree().addLast(labeled_v)

  """

  # takes O(log(n)) time

  # know that z exists

  # has no return value

  # z may be a sentinel node

  # add node v before node z

  def addBefore(self, v, z):

    # add node to list

    list_result = DoublyLinkedList.addBefore(self, v, z)

    # create an item to be stored using label tree

    # labeled_v = DoublyLinkedListNode(v)

    # update an auxiliary structure

    # self._addNodeToLabeledNodeRelationship(v, labeled_v)

    # allowing z to be tail sentinel gives us a way 
    #   of using this method to add an item at end of list

    tree_result = None

    if self._getTrailerSentinel() == z:

      # print "adding item to end of list"

      # for tree, instead call addLast method

      tree_result = self._getOverlyingTree().addLast(v)

    else:


      # get labeled item corresponding to node z

      # labeled_z = self._getLabeledNodeForNode(z)

      # find item stored using label tree corresponding to node z

      # find_tree_result = self._getOverlyingTree().find(DoublyLinkedListNode(z))

      # find_entry, find_node = find_tree_result

      # modify tree

      # labeled_z = find_node

      tree_result = self._getOverlyingTree().addBefore(v, z)

    # labeled_z = self._getLabeledNodeForNode(z)

    # self._getOverlyingTree().addBefore(labeled_v, labeled_z)

    # entry, node = tree_result

    # know that item stored using label tree corresponding to node v has correct label

    # label = labeled_v.getLabel()

    # update label for node v (which is a list node)

    # v.setLabel(label)

  # takes O(log(n)) time

  # know that z exists

  # has no return value

  # z may be a sentinel node

  # add node v after node z

  def addAfter(self, v, z):

    # add node to list

    list_result = DoublyLinkedList.addAfter(self, v, z)

    # create an item to be stored using label tree

    # labeled_v = DoublyLinkedListNode(v)

    # update an auxiliary structure

    # self._addNodeToLabeledNodeRelationship(v, labeled_v)

    # allowing z to be tail sentinel gives us a way 
    #   of using this method to add an item at end of list

    tree_result = None

    if self._getHeaderSentinel() == z:

      # print "adding item to front of list"

      # for tree, instead call addFirst method

      # tree_result = self._getOverlyingTree().addFirst(labeled_v)

      tree_result = self._getOverlyingTree().addFirst(v)

    else:

      # get labeled item corresponding to node z

      # labeled_z = self._getLabeledNodeForNode(z)

      # find item stored using label tree corresponding to node z

      # find_tree_result = self._getOverlyingTree().find(DoublyLinkedListNode(z))

      # find_entry, find_node = find_tree_result

      # modify tree

      # labeled_z = find_node

      tree_result = self._getOverlyingTree().addAfter(v, z)

    # labeled_z = self._getLabeledNodeForNode(z)

    # self._getOverlyingTree().addAfter(labeled_v, labeled_z)

    # entry, node = tree_result

    # know that item stored using label tree corresponding to node v has correct label

    # label = labeled_v.getLabel()

    # update label for node v (which is a list node)

    # v.setLabel(label)

  # takes O(log(n)) time

  # know that v exists

  # v is an OrderMaintainedDoublyLinkedListNode object

  def remove(self, v):

    result = DoublyLinkedList.remove(self, v)

    # labeled_node = self._getLabeledNodeForNode(v)

    # self._getOverlyingTree().remove(labeled_node)

    self._getOverlyingTree().remove(v)

    # update an auxiliary structure

    # self._removeNodeToLabeledNodeRelationship(v)

  """

  # takes O(log(n)) time

  def addFirst(self, v):

    # print self._getOverlyingTree().getNumEntries()

    list_result = DoublyLinkedList.addFirst(self, v)

    # print self._getOverlyingTree().getNumEntries()

    # labeled_v = DoublyLinkedListNode(v)

    tree_result = self._getOverlyingTree().addFirst(v)

    # entry, node = tree_result

    # v tree node has correct label

    # label = labeled_v.getLabel()

    # v.setLabel(label)

    # update an auxiliary structure

    # self._addNodeToLabeledNodeRelationship(v, labeled_v)

  # takes O(log(n)) time

  def addLast(self, v):

    list_result = DoublyLinkedList.addLast(self, v)

    # labeled_v = DoublyLinkedListNode(v)

    tree_result = self._getOverlyingTree().addLast(v)

    # entry, node = tree_result

    # v tree node has correct label

    label = labeled_v.getLabel()

    # v.setLabel(label)

    # update an auxiliary structure

    # self._addNodeToLabeledNodeRelationship(v, labeled_v)

  """

  # determine how node x is placed relative to node y

  # takes O(1) time

  def order(self, x, y):

    # x_label = x.getLabel()

    # y_label = y.getLabel()

    # return x_label.compare(y_label)

    entry1, node1 = self._getOverlyingTree().find(x)

    entry2, node2 = self._getOverlyingTree().find(y)

    label1 = node1.getPathLabel()

    label2 = node2.getPathLabel()

    return label1.compare(label2)

  """

  # takes O(n ^ 2) time

  def checkForAgreement(self):

    node_list = self._toNodeList()

    return self._checkForAgreementHelper(node_list)

  def _checkForAgreementHelper(self, node_list):

    if len(node_list) == 0:

      return True

    else:

      curr_node = node_list[0]

      curr_labeled_node = self._getLabeledNodeForNode(curr_node)

      path_labeled_nodes = self.overlying_tree.toInorderInternalNodeList()

      candidate_path_labeled_nodes = [x for x in path_labeled_nodes if x.getElement().getValue() == curr_labeled_node]

      matching_path_labeled_node = candidate_path_labeled_nodes[0]

      # entry, node = self.overlying_tree.find(curr_labeled_node)

      # if not (curr_node.getLabel().getValue() == curr_labeled_node.getNode().getLabel().getValue()):

      # if not (curr_node.getLabel().getValue() == node.getPathLabel()):

      if not (curr_node.getLabel().getValue() == matching_path_labeled_node.getPathLabel()):

        return False

      else:

        next_node_list = node_list[1 : ]

        return self._checkForAgreementHelper(next_node_list)

  """

"""

list = OrderMaintainedDoublyLinkedList()

labeled_node1 = DoublyLinkedListNode(1, None, None)

list.addFirst(labeled_node1)

node_inorder_list = list.overlying_tree.toInorderInternalNodeList()

print node_inorder_list

# element_list = [x.getElement().getValue().getNode().getElement() for x in node_inorder_list]

element_list = [x.getElement().getValue().getElement() for x in node_inorder_list]

print element_list

"""

"""

list = OrderMaintainedDoublyLinkedList()

labeled_node1 = DoublyLinkedListNode(1, None, None)

list.addFirst(labeled_node1)

labeled_node4 = DoublyLinkedListNode(4, None, None)

list.addLast(labeled_node4)

labeled_node2 = DoublyLinkedListNode(2, None, None)

list.addAfter(labeled_node2, labeled_node1)

labeled_node3 = DoublyLinkedListNode(3, None, None)

list.addBefore(labeled_node3, labeled_node4)

labeled_node0 = DoublyLinkedListNode(0, None, None)

list.addBefore(labeled_node0, labeled_node1)

labeled_node5 = DoublyLinkedListNode(5, None, None)

list.addAfter(labeled_node5, labeled_node4)

list.remove(labeled_node0)

list.remove(labeled_node5)

node = list.getFirst()

entry, node = list._getOverlyingTree().find(node)

label = node.getPathLabel()

label_value = label.getValue()

print label_value

labeled_node_one_occurs_earlier = list.order(labeled_node1, labeled_node2) == -1

print labeled_node_one_occurs_earlier

print list.toElementList()

# come up with a test for remove method

print list.order(labeled_node1, labeled_node2)

print list.order(labeled_node2, labeled_node3)

print list.order(labeled_node3, labeled_node4)

print list.order(labeled_node4, labeled_node1)

print list.order(labeled_node2, labeled_node3)

print list.order(labeled_node3, labeled_node2)

print list.order(labeled_node1, labeled_node1)

print list.order(labeled_node2, labeled_node2)

print list.order(labeled_node3, labeled_node3)

list.remove(labeled_node1)

list.remove(labeled_node3)

print list.toElementList()

node_inorder_list = list._toNodeList()

# print node_inorder_list

# node_label_value_list = [(PathLabel.toBaseThreeString(x.getLabel().getNumericPath()), x.getLabel().getPathLength())  for x in node_inorder_list]

# print node_label_value_list

node_inorder_list = list.overlying_tree.toInorderInternalNodeList()

# print node_inorder_list

# element_list = [x.getElement().getValue().getNode().getElement() for x in node_inorder_list]

element_list = [x.getElement().getValue().getElement() for x in node_inorder_list]

print element_list

# print list.checkForAgreement()

"""

