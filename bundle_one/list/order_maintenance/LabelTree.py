# assume that each item is unique
# maintain labels for items
# maintain invariant that labels are correct in between operations
# latent key is a (item, prospective label) tuple
# effective key is prospective label value or current label value
# value is an arbitrary item
# we change keys periodically
# note: if we retrieve a path label for an external node 
#   and prospectively associate it with an item to be inserted, 
#   item will be placed at a node that has a location 
#   that is consistent with path label
from ...Util import *
from PathLabeledScapegoatTree import *
# from LabeledMessage import *
from LabelTreeNode import *
from ...tree.Entry import *
class LabelTree(PathLabeledScapegoatTree):
  """
  @staticmethod
  def _keyTransform(x):
    # print x
    # print x.getLabel().getValue()
    return x.getLabel().getValue()
  """
  def __init__(self):
    # key_transform = lambda x: x.getLabel().getValue()
    key_transform = self._key_transform
    # key_transform = LabelTree._keyTransform
    # comparator = comp
    # comparator = lambda x, y: x.compare(y)
    comparator = self._comparator
    PathLabeledScapegoatTree.__init__(self, key_transform, comparator)
    self.key_to_entry_dict = {}
  def _key_transform(self, latent_key):
    item, prospective_label = latent_key
    # print prospective_label
    if item not in self.key_to_entry_dict:
      return prospective_label
    else:
      return ((self.key_to_entry_dict)[item]).getLocation().getPathLabel()
  def _comparator(self, x, y):
    # print x, y
    result = x.compare(y)
    return result
  def _expandExternal(self, external_node, left_entry, right_entry):
    self._expandExternalHelper(external_node, left_entry, right_entry, LabelTreeNode)
  def addRoot(self, entry):
    self._addRootHelper(entry, LabelTreeNode)
  @staticmethod
  def construct(items):
    tree = LabelTree()
    if len(items) >= 1:
      first_item = items[0]
      rest_of_items = items[1 : ]
      tree.addFirst(first_item)
      previous_item = first_item
      for item in rest_of_items:
        tree.addAfter(item, previous_item)
        previous_item = item
    return tree
  """
  # takes O(log(n)) time
  # key is an item
  def find(self, key):
    result = PathLabeledScapegoatTree.find(self, (key, None))
    entry, node = result
    return result
  """
  # takes O(1) time
  # key is an item
  def find(self, key):
    entry = (self.key_to_entry_dict)[key]
    node = entry.getLocation()
    result = entry, node
    return result
  # assumes that an item that serves as key already has associated with it a label
  # not meant to be externally visible
  # modified so that labeled items have their labels maintained
  def insert(self, key, value):
    result = PathLabeledScapegoatTree.insert(self, key, value)
    entry, node = result
    (self.key_to_entry_dict)[key[0]] = entry
    # label = node.getPathLabel()
    # value.setLabel(label)
    return result
  # not meant to be externally visible
  # modified so that labeled items have their labels maintained
  def localRebuild(self, u):
    result = PathLabeledScapegoatTree.localRebuild(self, u)
    subtree_root = result
    # self._localRebuildUpdateLabeledItemLabelsHelper(subtree_root)
    return result
  """
  def _localRebuildUpdateLabeledItemLabelsHelper(self, node):
    if node.isExternal() == True:
      return
    else:
      label = node.getPathLabel()
      value = node.getElement().getValue()
      # print label.getValue()
      value.setLabel(label)
      self._localRebuildUpdateLabeledItemLabelsHelper(node.getLeftChild())
      self._localRebuildUpdateLabeledItemLabelsHelper(node.getRightChild())
  """
  # retrieves a label value
  # takes O(log(n)) time
  def _getProspectiveExternalNodeLabel(self, node):
    label = self.getPathLabel(node)
    # print label.getValue()
    return label
  # v is a labeled item
  # z is a reference labeled item
  def addAfterHelper(self, v, z):
    # get prospective label for an appropriate external node
    # get successor external node
    result = self.find(z)
    entry, node = result
    z_node = node
    # an external node always exists in between an internal node and its internal node successor
    successor_external_node = self._getSuccessorExternalNode(z_node)
    # print successor_external_node.getParent().getElement().getValue().getMessage()
    # print successor_external_node.isRightChild()
    # prospective_location = self._getProspectiveExternalNodeLabel(successor_external_node)
    prospective_label = self._getProspectiveExternalNodeLabel(successor_external_node)
    # prospective_label = PathLabel(prospective_location)
    # v.setLabel(prospective_label)
    result = self.insert((v, prospective_label), v)
    return result
  # z is reference node
  def addBeforeHelper(self, v, z):
    # get prospective label for an appropriate external node
    # get predecessor external node
    result = self.find(z)
    entry, node = result
    z_node = node
    # an external node always exists in between an internal node and its internal node predecessor
    predecessor_external_node = self._getPredecessorExternalNode(z_node)
    # print predecessor_external_node.getParent().getElement().getValue().getMessage()
    # print predecessor_external_node.isLeftChild()
    # prospective_location = self._getProspectiveExternalNodeLabel(predecessor_external_node)
    prospective_label = self._getProspectiveExternalNodeLabel(predecessor_external_node)
    # prospective_label = PathLabel(prospective_location)
    # print "prospective label:", prospective_label.getValue()
    # v.setLabel(prospective_label)
    result = self.insert((v, prospective_label), v)
    return result
  def addFirstHelper(self, v):
    # print "adding an item to be first of sequence"
    prospective_label = None
    if self.getRoot().isExternal() == True:
      prospective_label = PathLabel(1, 0)
    else:
      z_node = self._getMinimumInternalNode(self.getRoot())
      # print z_node
      predecessor_external_node = self._getPredecessorExternalNode(z_node)
      # prospective_location = self._getProspectiveExternalNodeLabel(predecessor_external_node)
      prospective_label = self._getProspectiveExternalNodeLabel(predecessor_external_node)
      # prospective_label = PathLabel(prospective_location)
      # print prospective_label.getValue()
    # print prospective_label.getValue()
    # v.setLabel(prospective_label)
    result = self.insert((v, prospective_label), v)
    return result
  def addLastHelper(self, v):
    # print "adding an item to be last of sequence"
    prospective_label = None
    if self.getRoot().isExternal() == True:
      prospective_label = PathLabel(1, 0)
    else:
      z_node = self._getMaximumInternalNode(self.getRoot())
      # print z_node.isRightChild(), z_node.getParent().getElement().getKey().getMessage()
      """
      if z_node.isRightChild() and z_node.getParent().getElement().getKey() == 54:
        print "match"
      """
      successor_external_node = self._getSuccessorExternalNode(z_node)
      prospective_label = self._getProspectiveExternalNodeLabel(successor_external_node)
    # v.setLabel(prospective_label)
    result = self.insert((v, prospective_label), v)
    return result
  # takes O(log(n)) time
  def addBefore(self, v, z):
    # print "adding an item before an existing item"
    # place item as predecessor
    self.addBeforeHelper(v, z)
  # takes O(log(n)) time
  def addAfter(self, v, z):
    # print "adding an item after an existing item"
    # place item as successor
    self.addAfterHelper(v, z)
  # note: takes as an argument a node rather than an entry
  # takes O(log(n)) time
  def remove(self, v):
    # remove item
    # entry = LocationAwareEntry(v, None)
    entry = LocationAwareEntry(v, None)
    # print "removing labeled item v:", v
    PathLabeledScapegoatTree.remove(self, entry)
    # v.setLabel(None)
  # takes O(log(n)) time
  def addFirst(self, v):
    # place item as overall minimum
    return self.addFirstHelper(v)
  # takes O(log(n)) time
  def addLast(self, v):
    # place item as overall maximum
    return self.addLastHelper(v)
  """
  # takes O(log(n)) time
  def _getPathLabel(self, v):
    pass
  # takes O(1) time
  def getPathLabel(self, v):
    pass
  """
  """
  def checkForAgreement(self):
    return self._checkForAgreementHelper(self.getRoot())
  def _checkForAgreementHelper(self, node):
    if node.isExternal() == True:
      return True
    elif not (node.getPathLabel().getValue() == node.getElement().getValue().getLabel().getValue()):
      return False
    else:
      # print node.getPathLabel().getValue(), node.getElement().getValue().getLabel().getValue()
      left_branch_is_in_agreement = True
      right_branch_is_in_agreement = True
      if node.hasLeftChild() == True:
        left_branch_is_in_agreement = self._checkForAgreementHelper(node.getLeftChild())
      if node.hasRightChild() == True:
        right_branch_is_in_agreement = self._checkForAgreementHelper(node.getRightChild())
      return left_branch_is_in_agreement and right_branch_is_in_agreement
  """
"""    
# have inserts
# have removes
# test labels
"""
"""
keys = [17, 28, 29, 32, 44, 54, 65, 76, 78, 80, 82, 88, 97, 17]
messages = [str(x) for x in keys]
# labeled_items = [LabeledMessage(x) for x in messages]
# t3 = LabelTree.construct(labeled_items)
t3 = LabelTree.construct(messages)
# print t3.toString()
node_inorder_list = t3.toInorderInternalNodeList()
# message_inorder_list = [x.getElement() for x in node_inorder_list]
# item_inorder_list = [x.getElement().getValue() for x in node_inorder_list]
# node_label_value_list = [x.getPathLabel().getValue() for x in node_inorder_list]
# node_label_value_list = [PathLabel.toBaseFourString(x.getPathLabel().getValue()) for x in node_inorder_list]
node_label_value_list = [(PathLabel.toBaseThreeString(x.getPathLabel().getNumericPath()), x.getPathLabel().getPathLength())  for x in node_inorder_list]
# items = [x.getMessage() for x in item_inorder_list]
# item_label_value_list = [x.getLabel().getValue() for x in item_inorder_list]
# item_label_value_list = [PathLabel.toBaseFourString(x.getLabel().getValue()) for x in item_inorder_list]
# item_label_value_list = [(PathLabel.toBaseThreeString(x.getLabel().getNumericPath()), x.getLabel().getPathLength()) for x in item_inorder_list]
# print message_inorder_list
print node_label_value_list
# print items
# print item_label_value_list
# print message_inorder_list
# print t3.getRoot().getRightChild().getRightChild().getLeftChild().getLeftChild().getElement().getValue().getMessage() == "44"
"""
"""
keys = [17, 28, 29]
messages = [str(x) for x in keys]
# labeled_items = [LabeledMessage(x) for x in messages]
# labeled_item = labeled_items[2]
# t4 = LabelTree.construct(labeled_items)
t4 = LabelTree.construct(messages)
# print t4.toString()
t4.addBefore("32", "29")
t4.addFirst("44")
t4.addAfter("54", "29")
t4.addLast("64")
node_inorder_list = t4.toInorderInternalNodeList()
# message_inorder_list = [x.getElement().getValue().getMessage() for x in node_inorder_list]
# print message_inorder_list
node_label_value_list = [(PathLabel.toBaseThreeString(x.getPathLabel().getNumericPath()), x.getPathLabel().getPathLength())  for x in node_inorder_list]
print node_label_value_list
labeled_item_inorder_list = [x.getElement().getValue() for x in node_inorder_list]
# labeled_item_label_value_list = [x.getLabel().getValue() for x in labeled_item_inorder_list]
# print labeled_item_label_value_list
# print t4.checkForAgreement()
# label1 = PathLabel(PathLabel.toBaseTenValue("20021"), 4)
# labeled_item.setLabel(label1)
# print t4.checkForAgreement()
"""
