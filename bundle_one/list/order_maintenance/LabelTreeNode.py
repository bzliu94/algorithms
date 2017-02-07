from PathLabeledScapegoatTreeNode import *
class LabelTreeNode(PathLabeledScapegoatTreeNode):
  # def __init__(self, element, parent, left_child, right_child, path_label = None, prospective_path_label = None):
  def __init__(self, element, parent, left_child, right_child, path_label = None):
    PathLabeledScapegoatTreeNode.__init__(self, element, parent, left_child, right_child, path_label)
    # self.prospective_path_label = prospective_path_label
  """
  def getProspectiveLabel(self):
    return self.prospective_path_label
  def setProspectiveLabel(self, prospective_label):
    self.prospective_label = prospective_label
  """
