from ...tree.bbst.ScapegoatTreeNode import *
class HeightAwareScapegoatTreeNode(ScapegoatTreeNode):
  def __init__(self, element, parent, left_child, right_child, marked = False, height = None):
    ScapegoatTreeNode.__init__(self, element, parent, left_child, right_child, marked)
    self.height = height
  # height is max. depth
  def setHeight(self, height):
    # print height == None
    self.height = height
  def getHeight(self):
    return self.height
