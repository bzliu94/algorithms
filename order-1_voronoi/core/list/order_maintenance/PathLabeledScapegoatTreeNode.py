from PathLabel import *

from ...tree.bbst.ScapegoatTreeNode import *

class PathLabeledScapegoatTreeNode(ScapegoatTreeNode):

  def __init__(self, element, parent, left_child, right_child, path_label = None):
  
    ScapegoatTreeNode.__init__(self, element, parent, left_child, right_child)

    self.path_label = path_label

  """

  # path label is a (numeric path, path length) pair

  # numeric path is a base-three value

  # path length describes # of edges

  """

  # path label is a PathLabel object

  def setPathLabel(self, path_label):

    self.path_label = path_label

  def getPathLabel(self):

    return self.path_label

