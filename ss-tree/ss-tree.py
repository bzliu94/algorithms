# 2015-07-04

# ss-tree featuring insert, nn and k-nn search with threshold distance

# tie-breaking for same distance is identifier value with largest values appearing earlier

# have root entry instead of solely root node

# updated on 2016-08-22 to fix some bugs

# updated on 2016-08-23 to fix traditional/non-traditional isLeafNode() distinction

# updated on 2016-11-03 to re-structure and modify adjustTree(); 
#   stop at root instead of non-existent parent of root; 
#   note that there is a bug with setting M to two; 
#   also, we implement delete(); note that our tree 
#   lacks entry-aware nodes

# note that we don't necessarily need Image, ImageDraw, or PythonMagick

import sys
import Image, ImageDraw
import PythonMagick
import heapq
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    # priorities are (-1 * distance, -1 * id-value) pairs
    def  __init__(self):
        self.heap = []
    def push(self, item, priority):
        pair = (priority,item)
        heapq.heappush(self.heap,pair)
    def pop(self):
        (priority,item) = heapq.heappop(self.heap)
        return item
    def isEmpty(self):
        return len(self.heap) == 0
    # returns a (priority, item) pair
    def peek(self):
      heap = self.heap
      pair = heap[0]
      # item = pair[1]
      result = pair
      return result
    def toList(self):
      pair_list = self.heap
      items = [x[1] for x in pair_list]
      return items
    def getSize(self):
      return len(self.heap)
import math
def getDistance(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  change_x = x2 - x1
  change_y = y2 - y1
  distance = math.sqrt(change_x ** 2 + change_y ** 2)
  return distance
class NearestNeighbor:
  def __init__(self, close_item = None, distance = float("inf")):
    self.close_item = close_item
    self.distance = distance
  def getCloseItem(self):
    return self.close_item
  def getDistance(self):
    return self.distance
  def setCloseItem(self, close_item):
    self.close_item = close_item
  def setDistance(self, distance):
    self.distance = distance
  def toString(self):
    result_str = str(self.getCloseItem()) + " " + str(self.getDistance())
    return result_str
  """
  def toDepthString(self, depth):
    result_str = str(depth)
    return resullt_str
  """
class KNearestNeighbor:
  def __init__(self, query_point, close_item_pq, k = 100):
    self.query_point = query_point
    # priority queue we use uses a min-heap
    # as a result, we negate priorities
    self.close_item_pq = close_item_pq
    self.k = k
  # note that we do not always retrieve k items - could be less or could be more due to threshold
  def getCloseItems(self):
    return (self.close_item_pq).toList()
  # have special behavior for when no items are in queue
  def getFarthestCloseDistance(self):
    if self.getNumCloseItems() == 0:
      return float("inf")
    else:
      result = (self.close_item_pq).peek()
      priority, item = result
      # distance = -1 * priority
      distance = -1 * priority[0]
      id_value = priority[1]
      # print "distance:", distance
      return distance
  def addCloseItem(self, close_item):
    point = close_item
    # id_value = point.getIDValue()
    query_point = self.query_point
    point_location = (point.getX(), point.getY())
    id_value = point.getIDValue()
    # distance = getDistance(query_point, point_location)
    distance = getDistance(query_point, point_location)
    priority = (-1 * distance, id_value)
    # print "priority:", priority
    (self.close_item_pq).push(close_item, priority)
  def removeCloseItem(self):
    (self.close_item_pq).pop()
  def getNumCloseItems(self):
    # print self.close_item_pq.getSize()
    return (self.close_item_pq).getSize()
  def addAndRemoveIfNecessary(self, close_item):
    # print close_item, self.isFull()
    # do_remove = self.isFull() == True
    # use this so that we have enough to work with when we sort and cull
    # print "close item:", close_item
    do_remove = self.isFull() == True and self.passesThresholdForFarthestCloseItem(close_item) == True
    # do_remove = self.isFull() == True
    self.addCloseItem(close_item)
    if do_remove == True:
      self.removeCloseItem()
  def isFull(self):
    return self.getNumCloseItems() >= self.k
  # returns True if distance for item 'close_item' is >= 0.001 that of the farthest close item
  def passesThresholdForFarthestCloseItem(self, close_item):
    distance = self.getFarthestCloseDistance()
    query_point = self.query_point
    point = close_item
    point_location = (point.getX(), point.getY())
    curr_distance = getDistance(query_point, point_location)
    return curr_distance > distance + 0.001
  def toString(self):
    close_items = self.getCloseItems()
    # print close_items
    close_item_str_list = [str(x) for x in close_items]
    close_item_str = string.join(close_item_str_list, " ")
    result_str = close_item_str + " " + str(self.getFarthestCloseDistance())
    return result_str
# internal nodes have entries
# have one-to-one relationship between nodes and entries
class SSTreeNode:
  def __init__(self, parent, entries, is_leaf, n):
    self.parent = parent
    # self.entries = entries
    self.is_leaf = is_leaf
    self.m = 8
    self.M = 16
    self.child_to_entry_dict = {}
    for entry in entries:
      curr_child = entry.getChild()
      (self.child_to_entry_dict)[curr_child] = entry
    # num. of nodes in subtree rooted at current node
    self.n = n
  def getParent(self):
    return self.parent
  def getEntries(self):
    # return self.entries
    return (self.child_to_entry_dict).values()
  def getChildren(self):
    # entries = self.getEntries()
    # children = [x.getChild() for x in entries]
    # return children
    return (self.child_to_entry_dict).keys()
  def getNumEntries(self):
    return len(self.child_to_entry_dict)
  def getNumChildren(self):
    # return len(self.getChildren())
    return self.getNumEntries()
  def setParent(self, node):
    self.parent = node
  def isNonTraditionalLeafNode(self):
    is_non_traditional_leaf_node = (self.getParent() == None and self.getNumChildren() == 0) or (self.getNumChildren() != 0 and False not in [x.getChild().getNumEntries() == 0 for x in self.getEntries()])
    return is_non_traditional_leaf_node
  """
  def isTraditionalLeafNode(self):
    is_traditional_leaf_node = self.getNumEntries() == 0
    return is_traditional_leaf_node
  """
  def isLeafNode(self):
    # is root or have a child that is traditional leaf
    # is_leaf_node = (self.getParent() == None and self.getNumChildren() == 0) or (self.getNumChildren() != 0 and self.getEntries()[0].getChild().getNumEntries() == 0)
    # is_leaf_node = (self.getParent() == None and self.getNumChildren() == 0) or (self.getNumChildren() != 0 and False not in [x.getChild().getNumEntries() == 0 for x in self.getEntries()])
    # is_leaf_node = (self.getParent() == None and self.getNumChildren() == 0) or (self.getNumChildren() != 0 and True in [x.getChild().getNumEntries() == 0 for x in self.getEntries()])
    is_leaf_node = self.getNumChildren() == 0
    return is_leaf_node
    # return self.getNumChildren() == 0
    # return self.is_leaf
  def setIsLeafNode(self, is_leaf):
    self.is_leaf = is_leaf
  def addEntry(self, entry):
    # print "adding an entry:", entry.getMBR().toString()
    # (self.entries).append(entry)
    curr_child = entry.getChild()
    if curr_child.getParent() == None:
      pass
    (self.child_to_entry_dict)[curr_child] = entry
  # entry must match exactly
  def removeEntry(self, entry):
    # index = (self.entries).index(entry)
    # (self.entries).pop(index)
    curr_child = entry.getChild()
    (self.child_to_entry_dict).pop(curr_child)
  def getMinimumNumEntriesPerNode(self):
    return self.m
  def getMaximumNumEntriesPerNode(self):
    return self.M
  def isFull(self):
    return self.getNumEntries() >= self.getMaximumNumEntriesPerNode()
  def isUnderfull(self):
    return self.getNumEntries() < self.getMinimumNumEntriesPerNode()
  """
  # indexing starts at zero
  def getIndexForEntry(self, entry):
    index = (self.entries).index(entry)
    return index
  def removeIthEntry(self, i):
    (self.entries).pop(i)
  """
  def retrieveEntryForChild(self, node):
    return (self.child_to_entry_dict)[node]
    """
    entries = self.getEntries()
    children = [x.getChild() for x in entries]
    # print "children:", [x.toString() for x in children]
    # print "child:", node.toString()
    # print "mbr's:", [x.getMBR().toString() for x in entries]
    index = children.index(node)
    chosen_entry = entries[index]
    return chosen_entry
    """
  """
  # indexing starts at zero
  def getIthEntry(self, i):
    return (self.entries)[i]
  """
  def getNumLeavesInSubtree(self):
    return self.n
  def setNumLeavesInSubtree(self, n):
    self.n = n
  def toString(self):
    return str(self.getEntries())
# an entry is effectively an (mbc, child) pair
# mbc may be composite or raw
class SSTreeEntry:
  def __init__(self, mbc, child):
    if type(mbc) != type(MBC()):
      raise Exception()
    self.mbc = mbc
    self.child = child
  def getMBC(self):
    return self.mbc
  def setMBC(self, mbc):
    self.mbc = mbc
  def getChild(self):
    return self.child
  def setChild(self, node):
    self.child = node
  @staticmethod
  def draw(tree, entries, image, depth):
    for entry in entries:
      SSTreeEntry.drawHelper(tree, entry, image, depth)
  @staticmethod
  # def draw(self, tree, draw, depth):
  def drawHelper(tree, entry, image, depth):
    node = entry.getChild()
    entries = node.getEntries()
    mbc_list = [entry.getMBC()]
    for mbc in mbc_list:
      centroid = mbc.getCentroid()
      radius = mbc.getRadius()
      x1, y1 = centroid
      x2, y2 = x1 + radius, y1
      multiplier = 3 * 0.8
      # multiplier = 1 / (1.0 * 1302) * 0.8
      # multiplier = 1 / (1.0 * 6.5) * 0.8
      offset = (768 * 0.2) / 2
      # offset = (1536 * 0.2) / 2
      next_x1, next_y1 = (multiplier * x1 + offset, multiplier * y1 + offset)
      next_x2, next_y2 = (multiplier * x2 + offset, multiplier * y2 + offset)
      # if depth != 0 and depth != 1:
      if depth != 0:
        # continue
        pass
      """
      matching_entries = [x for x in entries if x.getMBR() == mbr]
      matching_entry = matching_entries[0]
      child = matching_entry.getChild()
      next_entries = child.getEntries()
      # print "num. of children:", len(next_entries)
      """
      """
      for next_entry in next_entries:
        mbr = next_entry.getMBR()
        print "mbr:", mbr.toString()
      """
      color_choice = depth % 3
      # print upper_left, lower_right
      color = None
      if color_choice == 0:
        # color = "rgb(255, 0, 0)"
        color = PythonMagick.Color(65535, 0, 0, 32767)
      elif color_choice == 1:
        # color = "rgb(0, 0, 255)"
        color = PythonMagick.Color(0, 0, 65535, 32767)
      elif color_choice == 2:
        # color = "rgb(0, 255, 0)"
        color = PythonMagick.Color(0, 65535, 0, 32767)
      if radius == 0:
        # draw.ellipse([(next_x1 - 4, next_y1 - 4), (next_x2 + 4, next_y2 + 4)], fill = color)
        # print "drew an ellipse"
        image.strokeColor("none")
        image.fillColor(color)
        center_x = next_x1
        center_y = next_y1
        radius = 4
        perimeter_x = next_x1
        perimeter_y = next_y1 + radius
        image.draw(PythonMagick.DrawableCircle(center_x, center_y, perimeter_x, perimeter_y))
      else:
        # draw.rectangle([next_x1, next_y1, next_x2, next_y2], outline = color)
        image.strokeColor(color)
        image.fillColor("none")
        image.strokeWidth(4)
        center_x, center_y = next_x1, next_y1
        perimeter_x, perimeter_y = next_x2, next_y2
        image.draw(PythonMagick.DrawableCircle(center_x, center_y, perimeter_x, perimeter_y))
        # image.draw(PythonMagick.DrawableRectangle(next_x1, next_y1, next_x2, next_y2))
    # mbr_list = [x.getMBR() for x in entries]
    # if len(entries) == 0 and tree.getRootEntry().getChild() != self:
    if len(entries) == 0:
      # draw a point
      parent = entry.getChild().getParent()
      # entry = parent.retrieveEntryForChild(self)
      # entry = self
      mbc = entry.getMBC()
      location = Point.toPoint(mbc)
      x, y = location
      multiplier = 3 * 0.8
      # multiplier = 1 / (1.0 * 1302) * 0.8
      # multiplier = 1 / (1.0 * 6.5) * 0.8
      offset = (768 * 0.2) / 2
      # offset = (1536 * 0.2) / 2
      next_x = multiplier * x
      next_y = multiplier * y
      """
      draw.ellipse([(next_x - 2 + offset, next_y - 2 + offset), \
        (next_x + 2 + offset, next_y + 2 + offset)], fill = "rgb(0, 0, 0)")
      """
      image.strokeColor("none")
      image.fillColor("black")
      center_x = next_x + offset
      center_y = next_y + offset
      radius = 2
      perimeter_x = next_x + offset
      perimeter_y = next_y + offset + radius
      image.draw(PythonMagick.DrawableCircle(center_x, center_y, perimeter_x, perimeter_y))
    children = [x.getChild() for x in entries]
    # print
    """
    for child in children:
      # child.draw(tree, draw, depth + 1)
      child.draw(tree, image, depth + 1)
    """
    entry.draw(tree, entries, image, depth + 1)
    # del draw
# x goes from left (negative) to right (positive)
# y goes from top (negative) to bottom (positive)
class MBC:
  def __init__(self, centroid = (0, 0), radius = 0, M2 = (0, 0)):
    self.centroid = centroid
    self.radius = radius
    self.M2 = M2
  def getCentroid(self):
    return self.centroid
  def setCentroid(self, centroid):
    self.centroid = centroid
  def getRadius(self):
    return self.radius
  def setRadius(self, radius):
    self.radius = radius
  @staticmethod
  def doOverlap(mbc1, mbc2):
    centroid1 = mbc1.getCentroid()
    centroid2 = mbc2.getCentroid()
    radius1 = mbc1.getRadius()
    radius2 = mbc2.getRadius()
    do_overlap = getDistance(centroid1, centroid2) <= (radius1 + radius2)
    return do_overlap
  def getSumOfSquaredDifferencesFromMean(self):
    return self.M2
  def setSumOfSquaredDifferencesFromMean(self, M2):
    # print M2
    self.M2 = M2
  def getVariance(self, n):
    # print "num. of leaves in subtree:", n
    M2 = self.getSumOfSquaredDifferencesFromMean()
    x, y = M2
    next_x = x / n
    next_y = y / n
    result = (next_x, next_y)
    return result
  # takes O(M) time
  # returns a (prepared MBC object, n) tuple
  @staticmethod
  def combineMBCs(mbc_list, n_values):
    # treat O(M) children as an O(M)-way partitioning
    # use Chan, Golub, LeVeque method
    # mbc_list = [x.getMBC() for x in entry_list]
    # node_list = [x.getChild() for x in entry_list]
    # n_values = [x.getNumLeavesInSubtree() for x in node_list]
    if len(mbc_list) == 0:
      raise Exception()
    # print mbc_list, n_values
    curr_mbc = mbc_list[0]
    curr_n = n_values[0]
    """
    if len(entry_list) == 1:
      curr_entry = entry_list[0]
      curr_mbc = curr_entry.getMBC()
      return (curr_mbc, n_values[0])
    """
    if len(mbc_list) == 1:
      mbc = mbc_list[0]
      n = n_values[0]
      return (mbc, n)
    remaining_mbc_list = mbc_list[1 : ]
    remaining_n_values = n_values[1 : ]
    component_mbc_list = [curr_mbc]
    # print mbc_list, n_values
    # combine pairs
    for i in range(len(remaining_mbc_list)):
      other_mbc = remaining_mbc_list[i]
      other_n = remaining_n_values[i]
      component_mbc_list.append(other_mbc)
      curr_mbc = MBC.combineMBCsHelper(curr_mbc, other_mbc, curr_n, other_n, component_mbc_list)
      curr_n = curr_n + other_n
    # mbc "curr_mbc" has its radius set appropriately
    # determine radius separately
    # use centroid and consider component mbcs' furthest extents
    mbc_centroids = [x.getCentroid() for x in mbc_list]
    mbc_radii = [x.getRadius() for x in mbc_list]
    # print "mbc centroids:", mbc_centroids
    # print "mbc radii:", mbc_radii
    centroid = curr_mbc.getCentroid()
    # print "centroid:", centroid
    distances = [getDistance(centroid, mbc_centroids[i]) + mbc_radii[i] for i in range(len(mbc_centroids))]
    # print "distances:", distances
    chosen_distance = max(distances)
    radius = chosen_distance
    curr_mbc.setRadius(radius)
    result = (curr_mbc, curr_n)
    return result
  # returns an MBC object
  @staticmethod
  def combineMBCsHelper(mbc1, mbc2, n1, n2, component_mbc_list):
    # print "combining mbc's with arguments:", mbc1, mbc2, n1, n2
    """
    mbc1 = entry1.getMBC()
    mbc2 = entry2.getMBC()
    """
    mean1 = mbc1.getCentroid()
    mean2 = mbc2.getCentroid()
    mean_x1, mean_y1 = mean1
    mean_x2, mean_y2 = mean2
    """
    node1 = entry1.getChild()
    node2 = entry2.getChild()
    n1 = node1.getNumLeavesInSubtree()
    n2 = node2.getNumLeavesInSubtree()
    """
    M2_1 = mbc1.getSumOfSquaredDifferencesFromMean()
    M2_2 = mbc2.getSumOfSquaredDifferencesFromMean()
    M2_1_x, M2_1_y = M2_1
    M2_2_x, M2_2_y = M2_2
    delta_x = mean_x2 - mean_x1
    delta_y = mean_y2 - mean_y1
    result_mean_x = (n1 * mean_x1 + n2 * mean_x2) / (1.0 * (n1 + n2))
    result_mean_y = (n1 * mean_y1 + n2 * mean_y2) / (1.0 * (n1 + n2))
    result_mean = (result_mean_x, result_mean_y)
    result_M2_x = M2_1_x + M2_2_x + (delta_x ** 2) * n1 * n2 / (1.0 * (n1 + n2))
    result_M2_y = M2_1_y + M2_2_y + (delta_y ** 2) * n1 * n2 / (1.0 * (n1 + n2))
    result_M2 = (result_M2_x, result_M2_y)
    result_mbc = CompositeMBC(result_mean, None, component_mbc_list)
    result_mbc.setSumOfSquaredDifferencesFromMean(result_M2)
    return result_mbc
  def isRaw(self):
    return False
  def isComposite(self):
    return False
  def toString(self):
    centroid = self.getCentroid()
    radius = self.getRadius()
    return "[" + str(centroid) + ", " + str(radius) + "]"
class RawMBC(MBC):
  def __init__(self, contained_item):
    center = (contained_item.getX(), contained_item.getY())
    radius = 0
    MBC.__init__(self, center, radius, (0, 0))
    self.contained_item = contained_item
  def isRaw(self):
    return True
  # point is a Point object
  @staticmethod
  def makeMBCFromPoint(point):
    result_mbc = RawMBC(point)
    return result_mbc
  def getContainedItem(self):
    # print self.contained_item
    return self.contained_item
  def getMBCList(self):
    return [self]
# mbc_list is a list of mbc's that can be either all raw or all composite
class CompositeMBC(MBC):
  def __init__(self, center, radius, mbc_list, M2 = (0, 0)):
    MBC.__init__(self, center, radius, M2)
    self.mbc_list = mbc_list
  def getMBCList(self):
    return self.mbc_list
  def setMBCList(self, mbc_list):
    self.mbc_list = mbc_list
  def isComposite(self):
    return True
class Point:
  def __init__(self, x, y, id_value):
    self.x = x
    self.y = y
    self.id_value = id_value
  @staticmethod
  def toPoint(mbr):
    # if mbr.getUpperLeft() != mbr.getLowerRight():
    if mbr.getRadius() != 0:
      raise Exception("attempted to turn a non-point mbr to a point")
    # return mbr.getUpperLeft()
    return mbr.getCentroid()
  def getX(self):
    return self.x
  def getY(self):
    return self.y
  def getIDValue(self):
    return self.id_value
import string
class SSTree:
  def __init__(self):
    root_node = SSTreeNode(None, [], True, 1)
    root_mbc = CompositeMBC(None, None, [])
    root_entry = SSTreeEntry(root_mbc, root_node)
    self.setRootEntry(root_entry)
  def getRootEntry(self):
    return self.root_entry
  def setRootEntry(self, root_entry):
    self.root_entry = root_entry
  def hasConsistentNonTraditionalLeafDepthValues(self):
    root = self.getRootEntry().getChild()
    curr_node = root
    depth = 0
    while curr_node.isLeafNode() == False:
      curr_node = curr_node.getChildren()[0]
      depth = depth + 1
    return self.hasConsistentNonTraditionalLeafDepthValuesHelper(root, depth, 0)
  def hasConsistentNonTraditionalLeafDepthValuesHelper(self, node, depth, curr_depth):
    if node == None:
      return
    elif node.isLeafNode() == True:
      if depth != curr_depth:
        return False
      else:
        return True
    else:
      for curr_node in node.getChildren():
        result = self.hasConsistentNonTraditionalLeafDepthValuesHelper(curr_node, depth, curr_depth + 1)
        if result == False:
          return False
      return True
  def toNumChildrenString(self):
    root = self.getRootEntry().getChild()
    return self.toNumChildrenStringHelper(root)
  def toNumChildrenStringHelper(self, node):
    if node == None:
      return ""
    entries = node.getEntries()
    children = node.getChildren()
    have_node_str = True
    """
    if node == self.getRoot():
      have_node_str = False
    """
    overall_str_list = None
    if have_node_str == True:
      curr_leaf_status = str(node.getNumChildren())
      overall_str_list = [curr_leaf_status]
      # overall_str_list = []
    else:
      overall_str_list = []
    for entry in entries:
      child = entry.getChild()
      child_str = self.toNumChildrenStringHelper(child)
      curr_str = child_str
      overall_str_list.append(curr_str)
    # curr_depth = "-" if node.getNumEntries() != 0 else str(depth)
    overall_str = "(" + string.join(overall_str_list, " ") + ")"
    return overall_str
  def toEntriesArePresentString(self):
    root = self.getRootEntry().getChild()
    return self.toEntriesArePresentStringHelper(root)
  def toEntriesArePresentStringHelper(self, node):
    if node == None:
      return ""
    entries = node.getEntries()
    children = node.getChildren()
    have_node_str = True
    """
    if node == self.getRoot():
      have_node_str = False
    """
    overall_str_list = None
    if have_node_str == True:
      curr_leaf_status = "-" if (node.getParent() == None or (node.getParent() != None and node in node.getParent().getChildren())) == False else "+"
      overall_str_list = [curr_leaf_status]
      # overall_str_list = []
    else:
      overall_str_list = []
    for entry in entries:
      child = entry.getChild()
      child_str = self.toEntriesArePresentStringHelper(child)
      curr_str = child_str
      overall_str_list.append(curr_str)
    # curr_depth = "-" if node.getNumEntries() != 0 else str(depth)
    overall_str = "(" + string.join(overall_str_list, " ") + ")"
    return overall_str
  def toLeafStatusString(self):
    root = self.getRootEntry().getChild()
    return self.toLeafStatusStringHelper(root)
  def toLeafStatusStringHelper(self, node):
    if node == None:
      return ""
    entries = node.getEntries()
    children = node.getChildren()
    have_node_str = True
    """
    if node == self.getRoot():
      have_node_str = False
    """
    overall_str_list = None
    if have_node_str == True:
      curr_leaf_status = "-" if node.isLeafNode() == False else "+"
      overall_str_list = [curr_leaf_status]
      # overall_str_list = []
    else:
      overall_str_list = []
    for entry in entries:
      child = entry.getChild()
      child_str = self.toLeafStatusStringHelper(child)
      curr_str = child_str
      overall_str_list.append(curr_str)
    # curr_depth = "-" if node.getNumEntries() != 0 else str(depth)
    overall_str = "(" + string.join(overall_str_list, " ") + ")"
    return overall_str
  def toDepthString(self):
    root = self.getRootEntry().getChild()
    return self.toDepthStringHelper(root, 0)
  def toDepthStringHelper(self, node, depth):
    if node == None:
      return ""
    entries = node.getEntries()
    children = node.getChildren()
    have_node_str = True
    """
    if node == self.getRoot():
      have_node_str = False
    """
    overall_str_list = None
    if have_node_str == True:
      curr_depth = "-" if node.getNumEntries() != 0 else str(depth)
      overall_str_list = [curr_depth]
      # overall_str_list = []
    else:
      overall_str_list = []
    for entry in entries:
      child = entry.getChild()
      child_str = self.toDepthStringHelper(child, depth + 1)
      curr_str = child_str
      overall_str_list.append(curr_str)
    # curr_depth = "-" if node.getNumEntries() != 0 else str(depth)
    overall_str = "(" + string.join(overall_str_list, " ") + ")"
    return overall_str
  # return an in-order string
  def toString(self):
    root = self.getRootEntry().getChild()
    return self.toStringHelper(root)
  def toStringHelper(self, node):
    if node == None:
      return ""
    entries = node.getEntries()
    children = node.getChildren()
    have_node_str = True
    is_root_node = node == self.getRootEntry().getChild()
    if is_root_node == True:
      have_node_str = True
    overall_str_list = None
    if is_root_node == False:
      overall_str_list = [node.getParent().retrieveEntryForChild(node).getMBC().toString()]
    else:
      overall_str_list = [] if node.getNumChildren() == 0 else [self.getRootEntry().getMBC().toString()]
    for entry in entries:
      child = entry.getChild()
      child_str = self.toStringHelper(child)
      curr_str = child_str
      overall_str_list.append(curr_str)
    overall_str = "(" + string.join(overall_str_list, " ") + ")"
    return overall_str
  """
  def setRoot(self, node):
    self.root = node
  def getRoot(self):
    return self.root
  """
  # in case of ties, return multiple candidates
  def chooseEntriesWithClosestCentroid(self, entries, entry):
    mbc_tagged_entries = [(x.getMBC(), x) for x in entries]
    centroid_tagged_entries = [(x[0].getCentroid(), x[1]) for x in mbc_tagged_entries]
    curr_mbc = entry.getMBC()
    curr_centroid = curr_mbc.getCentroid()
    distance_tagged_entries = [(getDistance(curr_centroid, x[0]), x[1]) for x in centroid_tagged_entries]
    distance_values = [x[0] for x in distance_tagged_entries]
    min_distance = min(distance_values)
    matching_entries = [x[1] for x in distance_tagged_entries if x[0] == min_distance]
    return matching_entries
  """
  def chooseEntriesWithMinimalOverlapEnlargement(self, entries, entry):
    mbr_to_entry_dict = {}
    for i in range(len(entries)):
      curr_entry = entries[i]
      curr_mbr = curr_entry.getMBR()
      mbr_to_entry_dict[curr_mbr] = curr_entry
    mbr_list = [x.getMBR() for x in entries]
    mbr = entry.getMBR()
    tagged_enlargement_values = [(MBR.findOverlapArea(x, mbr), x) for x in mbr_list]
    enlargement_values = [x[0] for x in tagged_enlargement_values]
    # print enlargement_values
    min_enlargement_value = min(enlargement_values)
    candidate_tagged_enlargement_values = [x for x in tagged_enlargement_values if x[0] == min_enlargement_value]
    candidate_entries = [mbr_to_entry_dict[x[1]] for x in candidate_tagged_enlargement_values]
    return candidate_entries
  """
  """
  # in case of ties, return multiple candidates
  def chooseEntriesWithMinimalAreaEnlargement(self, entries, entry):
    mbr_to_entry_dict = {}
    for i in range(len(entries)):
      curr_entry = entries[i]
      curr_mbr = curr_entry.getMBR()
      mbr_to_entry_dict[curr_mbr] = curr_entry
    mbr_list = [x.getMBR() for x in entries]
    mbr = entry.getMBR()
    tagged_enlargement_values = [(MBR.getAreaEnlargement(x, mbr), x) for x in mbr_list]
    enlargement_values = [x[0] for x in tagged_enlargement_values]
    # print enlargement_values
    min_enlargement_value = min(enlargement_values)
    candidate_tagged_enlargement_values = [x for x in tagged_enlargement_values if x[0] == min_enlargement_value]
    candidate_entries = [mbr_to_entry_dict[x[1]] for x in candidate_tagged_enlargement_values]
    return candidate_entries
    # chosen_tagged_enlargement_value = candidate_tagged_enlargement_values[0]
    # chosen_enlargement, chosen_mbr = chosen_tagged_enlargement_value
    # tagged_mbr_list = [(children[x], entries[x].getMBR()) for x in range(len(children))]
    # candidate_tagged_mbr_list = [x for x in tagged_mbr_list if x[1] == chosen_mbr]
    # chosen_tagged_mbr = canddiate_tagged_mbr_list[0]
    # chosen_child, chosen_mbr = chosen_tagged_mbr
    # return chosen_child
  """
  """
  def resolveEnlargementTie(self, entries, entry):
    mbr = entry.getMBR()
    tagged_mbr_list = []
    for curr_entry in entries:
      base_mbr = curr_entry.getMBR()
      curr_mbr = MBR.getEnlargedMBR(base_mbr, mbr)
      tagged_mbr_list.append((curr_mbr, curr_entry))
    tagged_area_values = [(x[0].getArea(), x[1]) for x in tagged_mbr_list]
    area_values = [x[0] for x in tagged_area_values]
    # print area_values
    min_area = min(area_values)
    candidate_tagged_area_values = [x for x in tagged_area_values if x[0] == min_area]
    candidate_entries = [x[1] for x in candidate_tagged_area_values]
    return candidate_entries
  """
  """
  @staticmethod
  def quadraticPickSeeds(entries):
    # mbr_list = [x.getMBR() for x in entries]
    # choose pair with largest dead area
    tagged_pairs = []
    for entry1 in entries:
      for entry2 in entries:
        if entry1 == entry2:
          continue
        curr_pair = (entry1, entry2)
        curr_entry_list = [entry1, entry2]
        curr_mbr_list = [x.getMBR() for x in curr_entry_list]
        curr_mbr = CompositeMBR.makeMBR(curr_mbr_list)
        curr_area1 = entry1.getMBR().getArea()
        curr_area2 = entry2.getMBR().getArea()
        curr_mbr_area = curr_mbr.getArea()
        dead_area = curr_mbr_area - (curr_area1 + curr_area2)
        tagged_pair = (dead_area, curr_pair)
        tagged_pairs.append(tagged_pair)
    dead_area_values = [x[0] for x in tagged_pairs]
    max_dead_area_value = max(dead_area_values)
    candidate_tagged_pairs = [x for x in tagged_pairs if x[0] == max_dead_area_value]
    chosen_tagged_pair = candidate_tagged_pairs[0]
    chosen_pair = tagged_pair[1]
    return chosen_pair
  """
  # return a tuple (x_distributions1, x_distributions2, y_distributions1, y_distributions2)
  # where each element is a list of distributions, with each distribution being a pair
  # (left_entries, right_entries)
  @staticmethod
  def ssTreeGenDistributions(tree, entries, M, m):
    # print "num. of entries:", len(entries)
    if len(entries) > (M + 1):
      raise Exception()
    window_left_sizes = [m - 1 + k for k in range(1, M - 2 * m + 2 + 1)]
    # window_left_sizes = [x for x in window_left_sizes if x <= M and x >= m and (M + 1 - x) <= M and (M + 1 - x) >= m]
    window_left_sizes = [x for x in window_left_sizes if x <= M and x >= m and (len(entries) - x) <= M and (len(entries) - x) >= m]
    # window_size_pairs = [(window_left_sizes[i], M + 1 - window_left_sizes[i]) for i in range(len(window_left_sizes))]
    window_size_pairs = [(window_left_sizes[i], len(entries) - window_left_sizes[i]) for i in range(len(window_left_sizes))]
    window_size_pairs = [x for x in window_size_pairs if x[0] <= M and x[0] >= m and x[1] <= M and x[1] >= m]
    # print "window size pairs:", window_size_pairs
    # print "window left sizes:", window_left_sizes
    x_sorted_entries = entries[ : ]
    x_sorted_entries.sort(key = lambda x: x.getMBC().getCentroid()[0])
    x_distributions = [(x_sorted_entries[ : window_left_sizes[i]], x_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]
    """
    # print "low x distributions:", low_x_distributions
    upper_x_sorted_entries = entries[ : ]
    upper_x_sorted_entries.sort(key = lambda x: x.getMBR().getLowerRight()[0])
    upper_x_distributions = [(upper_x_sorted_entries[ : window_left_sizes[i]], upper_x_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]
    """
    y_sorted_entries = entries[ : ]
    y_sorted_entries.sort(key = lambda x: x.getMBC().getCentroid()[1])
    y_distributions = [(y_sorted_entries[ : window_left_sizes[i]], y_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]
    """
    upper_y_sorted_entries = entries[ : ]
    upper_y_sorted_entries.sort(key = lambda x: x.getMBR().getLowerRight()[1])
    upper_y_distributions = [(upper_y_sorted_entries[ : window_left_sizes[i]], upper_y_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]
    """
    # result = (low_x_distributions, upper_x_distributions, low_y_distributions, upper_y_distributions)
    result = (x_distributions, y_distributions)
    # print "result:", result
    return result
  # returns 0 for x, 1 for y
  @staticmethod
  def ssTreeChooseSplitAxis(tree, parent_entry, entries, M, m):
    # result = SSTree.ssTreeGenDistributions(tree, entries, M, m)
    """
    curr_entry = entries[0]
    curr_node = curr_entry.getChild()
    curr_parent_entry = None
    if curr_node == tree.getRootEntry().getChild():
      curr_parent_entry = tree.getRootEntry()
    else:
      curr_parent_entry = curr_node.getParent().retrieveEntryForChild(curr_node)
    """
    curr_node = parent_entry.getChild()
    # parent_entry corresponds to node that we are splitting
    curr_parent_entry = parent_entry
    curr_mbc = curr_parent_entry.getMBC()
    n = curr_node.getNumLeavesInSubtree()
    variance = curr_mbc.getVariance(n)
    x_variance, y_variance = variance
    if x_variance >= y_variance:
      return 0
    elif x_variance < y_variance:
      return 1
  # return a tuple of two lists of entries
  # axis is 0 for x, 1 for y
  @staticmethod
  def ssTreeChooseSplitIndex(tree, parent_entry, entries, axis, M, m):
    result = SSTree.ssTreeGenDistributions(tree, entries, M, m)
    x_distributions, y_distributions = result
    # consider cross-group overlap and combined area
    candidate_distributions = None
    if axis == 0:
      candidate_distributions = x_distributions
    elif axis == 1:
      candidate_distributions = y_distributions
    mbc_list_pair_tagged_candidate_distributions = [(([y.getMBC() for y in x[0]], [y.getMBC() for y in x[1]]), x) for x in candidate_distributions]
    n_list_pair_tagged_candidate_distributions = [(([y.getChild().getNumLeavesInSubtree() for y in x[0]], [y.getChild().getNumLeavesInSubtree() for y in x[1]]), x) for x in candidate_distributions]
    # n_pair_tagged_candidate_distributions = [((sum(x[0][0]), sum(x[0][1])), x[1]) for x in n_list_pair_tagged_candidate_distributions]
    mbc_n_pair_pair_tagged_candidate_distributions = [((MBC.combineMBCs(mbc_list_pair_tagged_candidate_distributions[i][0][0], n_list_pair_tagged_candidate_distributions[i][0][0]), MBC.combineMBCs(mbc_list_pair_tagged_candidate_distributions[i][0][1], n_list_pair_tagged_candidate_distributions[i][0][1])), candidate_distributions[i]) for i in range(len(candidate_distributions))]
    """
    variance_value_pair_tagged_candidate_distributions = [((mbc_pair_tagged_candidate_distributions[i][0][0].getVariance(n_pair_tagged_candidate_distributions[i][0][0]), mbc_pair_tagged_candiate_distributions[i][0][1].getVariance(n_pair_tagged_candidate_distributions[i][0][1])), candidiate_distributions[i]) for i in range(len(candidate_distributions))]
    """
    variance_value_pair_tagged_candidate_distributions = [((x[0][0][0].getVariance(x[0][0][1]), x[0][1][0].getVariance(x[0][1][1])), x[1]) for x in mbc_n_pair_pair_tagged_candidate_distributions]
    variance_sum_tagged_candidate_distributions = [((x[0][0][0] + x[0][1][0], x[0][0][1] + x[0][1][1]), x[1]) for x in variance_value_pair_tagged_candidate_distributions]
    variance_component_sum_values = None
    if axis == 0:
      variance_component_sum_values = [x[0][0] for x in variance_sum_tagged_candidate_distributions]
    elif axis == 1:
      variance_component_sum_values = [x[0][1] for x in variance_sum_tagged_candidate_distributions]
    min_variance_component_sum_value = min(variance_component_sum_values)
    matching_variance_sum_tagged_candidate_distributions = None
    if axis == 0:
      matching_variance_sum_tagged_candidate_distributions = [x for x in variance_sum_tagged_candidate_distributions if x[0][0] == min_variance_component_sum_value]
    elif axis == 1:
      matching_variance_sum_tagged_candidate_distributions = [x for x in variance_sum_tagged_candidate_distributions if x[0][1] == min_variance_component_sum_value]
    next_next_candidates = [x[1] for x in matching_variance_sum_tagged_candidate_distributions]
    chosen_distribution_pair = next_next_candidates[0]
    # print "chosen distribution pair:", chosen_distribution_pair
    return chosen_distribution_pair
  """
  # we assume that >= 2 entries are provided
  # we take special precautions to make the two returned entries be different
  @staticmethod
  def linearPickSeeds(entries):
    mbr_list = [x.getMBR() for x in entries]
    # largest dead space along any dimension
    upper_left_points = [x.getUpperLeft() for x in mbr_list]
    lower_right_points = [x.getLowerRight() for x in mbr_list]
    points = upper_left_points + lower_right_points
    x_values = [x[0] for x in points]
    y_values = [x[1] for x in points]
    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)
    x_size = max_x - min_x
    y_size = max_y - min_y
    x_values_upper_left = [x[0] for x in upper_left_points]
    y_values_upper_left = [x[1] for x in upper_left_points]
    x_values_lower_right = [x[0] for x in lower_right_points]
    y_values_lower_right = [x[1] for x in lower_right_points]
    highest_low_side_x = max(x_values_upper_left)
    lowest_high_side_x = min(x_values_lower_right)
    highest_low_side_y = max(y_values_upper_left)
    lowest_high_side_y = min(y_values_lower_right)
    x_separation = highest_low_side_x - lowest_high_side_x
    y_separation = highest_low_side_y - lowest_high_side_y
    normalized_x_separation = x_separation / (1.0 * x_size + 1)
    normalized_y_separation = y_separation / (1.0 * y_size + 1)
    x_responsible_mbr_candidates1 = [x for x in mbr_list if x.getUpperLeft()[0] == highest_low_side_x]
    chosen_x_responsible_mbr_candidate1 = x_responsible_mbr_candidates1[0]
    x_responsible_mbr_candidates2 = [x for x in mbr_list if x.getLowerRight()[0] == lowest_high_side_x]
    winnowed_x_responsible_mbr_candidates2 = [x for x in x_responsible_mbr_candidates2 if x != chosen_x_responsible_mbr_candidate1]
    chosen_x_responsible_mbr_candidate2 = winnowed_x_responsible_mbr_candidates2[0]
    y_responsible_mbr_candidates1 = [x for x in mbr_list if x.getUpperLeft()[1] == highest_low_side_y]
    chosen_y_responsible_mbr_candidate1 = y_responsible_mbr_candidates1[0]
    y_responsible_mbr_candidates2 = [x for x in mbr_list if x.getLowerRight()[1] == lowest_high_side_y]
    winnowed_y_responsible_mbr_candidates2 = [x for x in y_responsible_mbr_candidates2 if x != chosen_y_responsible_mbr_candidate1]
    chosen_y_responsible_mbr_candidate2 = winnowed_y_responsible_mbr_candidates2[0]
    chosen_x_responsible_entry_candidates1 = [x for x in entries if x.getMBR() == chosen_x_responsible_mbr_candidate1]
    chosen_x_responsible_entry_candidates2 = [x for x in entries if x.getMBR() == chosen_x_responsible_mbr_candidate2]
    chosen_y_responsible_entry_candidates1 = [x for x in entries if x.getMBR() == chosen_y_responsible_mbr_candidate1]
    chosen_y_responsible_entry_candidates2 = [x for x in entries if x.getMBR() == chosen_y_responsible_mbr_candidate2]
    chosen_x_entry1 = chosen_x_responsible_entry_candidates1[0]
    chosen_x_entry2 = chosen_x_responsible_entry_candidates2[0]
    chosen_y_entry1 = chosen_y_responsible_entry_candidates1[0]
    chosen_y_entry2 = chosen_y_responsible_entry_candidates2[0]
    if normalized_y_separation >= normalized_x_separation:
      return (chosen_y_entry1, chosen_y_entry2)
    elif normalized_x_separation > normalized_y_separation:
      # there was an error here
      return (chosen_x_entry1, chosen_x_entry2)
  """
  def chooseLeaf(self, entry):
    return self.chooseLeafHelper(entry, self.getRootEntry().getChild())
  def chooseLeafHelper(self, entry, node):
    if node.isLeafNode() == True:
      if node == self.getRootEntry().getChild():
        return node
      else:
        return node.getParent()
    else:
      entries = node.getEntries()
      candidate_entries = self.chooseEntriesWithMinimalAreaEnlargement(entries, entry)
      if len(candidate_entries) != 1:
        # resolve a tie
        candidate_entries = self.resolveEnlargementTie(candidate_entries, entry)
      chosen_entry = candidate_entries[0]
      chosen_child = chosen_entry.getChild()
      return self.chooseLeafHelper(entry, chosen_child)
  def ssTreeChooseLeaf(self, entry):
    return self.ssTreeChooseLeafHelper(entry, self.getRootEntry().getChild())
  def ssTreeChooseLeafHelper(self, entry, node):
    if node.isLeafNode() == True:
      if node == self.getRootEntry().getChild():
        return node
      else:
        return node.getParent()
    else:
      entries = node.getEntries()
      candidate_entries = None
      candidate_entries = self.chooseEntriesWithClosestCentroid(entries, entry)
      # print "candidate entries:", candidate_entries
      """
      if entries[0].getChild().isLeafNode() == True:
        candidate_entries = self.chooseEntriesWithMinimalOverlapEnlargement(entries, entry)
        if len(candidate_entries) != 1:
          # resolve a tie
          candidate_entries = self.chooseEntriesWithMinimalAreaEnlargement(candidate_entries, entry)
        if len(candidate_entries) != 1:
          # resolve a tie
          candidate_entries = self.resolveEnlargementTie(candidate_entries, entry)
      else:
        candidate_entries = self.chooseEntriesWithMinimalAreaEnlargement(entries, entry)
        if len(candidate_entries) != 1:
          # resolve a tie
          candidate_entries = self.resolveEnlargementTie(candidate_entries, entry)
      """
      chosen_entry = candidate_entries[0]
      chosen_child = chosen_entry.getChild()
      return self.ssTreeChooseLeafHelper(entry, chosen_child)
  def insert(self, entry):
    # print entry.getMBR().toString()
    # print entry.getMBR().getUpperLeft()[0]
    # if abs(entry.getMBR().getUpperLeft()[0] - 988266.168186) < 0.1:
    # if abs(entry.getMBR().getUpperLeft()[0] - 185061.9338) < 0.1:
    # if abs(entry.getMBR().getUpperLeft()[0] - 75898.2202098) < 0.1:
    """
    if abs(entry.getMBR().getUpperLeft()[0] - 185061.9338) < 0.1:
      # raise Exception()
      pass
    """
    # print "inserting an entry"
    """
    if self.hasConsistentNonTraditionalLeafDepthValues() == False and self.getRootEntry().getChild().isLeafNode() == False:
      # raise Exception()
      pass
    """
    """
    if self.getRoot().getNumChildren() > self.getRoot().getMaximumNumEntriesPerNode():
      raise Exception()
    """
    """
    encountered_item = False
    # if entry.getMBR().getContainedItem() == (962736.900780, 317162.3926449):
    if entry.getMBR().getContainedItem()[0] == 835394.40839:
      encountered_item = True
    if encountered_item == True:
      print self.toString()
      raise Exception()
    """
    leaf_node = self.ssTreeChooseLeaf(entry)
    adjust_result = None
    # print "leaf is full:", leaf_node.isFull()
    if leaf_node.isFull() == False:
      # leaf_node.setIsLeafNode(True)
      # do not have to split node
      leaf_node.addEntry(entry)
      # this may be unnecessary
      entry.getChild().setParent(leaf_node)
      # print "leaf node entries:", leaf_node.getEntries()
      # print "added an entry to a leaf:", entry
      # print "leaf node:", leaf_node
      # print "root node:", self.getRoot()
      # print leaf_node == self.getRoot()
      # print leaf_node.toString()
      # entry.getChild().setParent(leaf_node)
      # call adjustTree to resize bounding boxes of current node and ancestors and propagate splits
      # RTree.rstarPreadjustTree(self, leaf_node)
      adjust_result = SSTree.ssTreeAdjustTree(self, leaf_node, [entry], False)
    else:
      # split node
      # split_result = self.rstarSplitNode(leaf_node.getChildren()[0], entry)
      # entry.getChild().setParent(leaf_node)
      if None in [x.getParent() for x in leaf_node.getChildren()]:
        raise Exception()
      split_result = self.ssTreeSplitNode(leaf_node, entry)
      # l and ll are internal nodes
      l, ll, e, ee = split_result
      # print leaf_node == self.getRoot()
      # print leaf_node.getParent().getEntries(), e, ee
      # if leaf_node != self.getRoot() and leaf_node.getParent() != None:
      if leaf_node.getParent() != None:
        # adjust fields related to existence of a parent
        """
        parent = leaf_node.getParent()
        leaf_entry = parent.retrieveEntryForChild(leaf_node)
        index = parent.getIndexForEntry(leaf_entry)
        parent.removeIthEntry(index)
        parent.addEntry(e)
        parent.addEntry(ee)
        l.setParent(parent)
        ll.setParent(parent)
        """
        pass
      else:
        # split but do not have parent; so, we create one
        pass
        # print "split node is root"
        """
        next_root = RTreeNode(None, [e, ee], False)
        l.setParent(next_root)
        ll.setParent(next_root)
        # next_root.addEntry(e)
        # next_root.addEntry(ee)
        self.setRoot(next_root)
        """
      # we might be able to handle propagating the first split manually, 
      # and we would continue as if we currently have no split to propagate
      # e and ee are for entries for the two children that result from split of pre-cursor to l
      # RTree.rstarPreadjustTree(self, l)
      adjust_result = SSTree.ssTreeAdjustTree(self, l, [e, ee], True)
      # check result of tree-adjust to see whether we plan on splitting root
      # in case the root has to be split, create a new root
      # increase the height of the tree by one
      # grow tree taller
    ended_with_split2, resulting_entries_from_split = adjust_result
    # return from an "adjust" action is always to do with root
    # print "ended with split:", ended_with_split2
    # we ended adjust-tree by requiring a split of root
    if ended_with_split2 == True:
      # return
      # raise Exception()
      e, ee = resulting_entries_from_split
      l = e.getChild()
      ll = ee.getChild()
      # print "num. of entries:", tree.getRoot().getNumEntries()
      if (self.getRootEntry().getChild().getNumEntries() + 1) <= self.getRootEntry().getChild().getMaximumNumEntriesPerNode():
        # there is space at root
        # tree.getRoot().addEntry(e)
        # raise Exception()
        self.getRootEntry().getChild().addEntry(ee)
        # l.setParent(tree.getRoot())
        ll.setParent(self.getRootEntry().getChild())
      else:
        # split_result = tree.rstarSplitNode(tree.getRoot().getChildren()[0], ee)
        split_result = self.ssTreeSplitNode(self.getRootEntry().getChild(), ee)
        l, ll, e, ee = split_result
        # e, ee = resulting_entries_from_split
        # print "resulting entries:", resulting_entries_from_split
        resulting_entries_from_split = [e, ee]
        n_values = [x.getChild().getNumLeavesInSubtree() for x in resulting_entries_from_split]
        n_value_sum = sum(n_values)
        next_root = SSTreeNode(None, resulting_entries_from_split, False, n_value_sum)
        # next_root.addEntry(e)
        # next_root.addEntry(ee)
        """
        l = e.getChild()
        ll = ee.getChild()
        """
        l.setParent(next_root)
        ll.setParent(next_root)
        # print "have a next root:", next_root
        self.getRootEntry().setChild(next_root)
        # print "modified root as part of an insert"
    else:
      # print "entries included:", e in l.getParent().getEntries()
      pass
  # make available two nodes l and ll 
  # and make available two entries e and ee
  # "node" is the node that we split 
  # by additionally introducing entry "entry"
  # we also add the created entries to parent
  def ssTreeSplitNode(self, node, entry):
    curr_node = node
    # making a set out of a list leads to lack of order preservation
    E_overall = list(set(curr_node.getEntries() + [entry]))
    # parent_entry corresponds to node that we are splitting
    parent_entry = None
    if curr_node == self.getRootEntry().getChild():
      parent_entry = self.getRootEntry()
    else:
      parent_entry = curr_node.getParent().retrieveEntryForChild(curr_node)
    return self.ssTreeSplitNodeHelper(parent_entry, node, E_overall, entry)
  def ssTreeSplitNodeHelper(self, parent_entry, node, E_overall, entry):
    # print "splitting a node"
    # print "pre-split-node tree:", tree.toNumChildrenString()
    # print node == self.getRoot()
    # print node.getNumEntries()
    # find distribution
    # adjust pointers
    # have a recursive call
    # prev_leaf_status = node.isLeafNode()
    prev_leaf_status = None
    curr_node = node
    # pick seeds
    # be sure that entry is not included in existing list of entries
    # this takes too much time as it is
    # E_overall = list(set(curr_node.getEntries() + [entry]))
    # print E_overall
    m = self.getRootEntry().getChild().getMinimumNumEntriesPerNode()
    M = self.getRootEntry().getChild().getMaximumNumEntriesPerNode()
    # print "num. of entries overall:", len(E_overall)
    axis = SSTree.ssTreeChooseSplitAxis(self, parent_entry, E_overall, M, m)
    # print axis
    result = SSTree.ssTreeChooseSplitIndex(self, parent_entry, E_overall, axis, M, m)
    entry_group1, entry_group2 = result
    # ran into problems with entry groups sometimes being invalid as in terms of number of unique items
    # print "entry groups:", entry_group1, entry_group2
    # print "entry group sizes:", len(entry_group1), len(entry_group2)
    parent = curr_node.getParent()
    if parent != None:
      # a parent exists
      parent.setIsLeafNode(True)
    if parent != None and (node in parent.getChildren()):
      # a parent exists
      # removing an entry so as to be clean
      # parent.removeEntry(parent.retrieveEntryForChild(node))
      # print "current parent entries, again:", parent.getEntries()
      pass
    children1 = [x.getChild() for x in entry_group1]
    children2 = [x.getChild() for x in entry_group2]
    num_children1 = [x.getNumLeavesInSubtree() for x in children1]
    num_children2 = [x.getNumLeavesInSubtree() for x in children2]
    n1 = sum(num_children1)
    n2 = sum(num_children2)
    node1 = SSTreeNode(parent, entry_group1, prev_leaf_status, n1)
    node2 = SSTreeNode(parent, entry_group2, prev_leaf_status, n2)
    # print "num. of children:", node1.getNumChildren(), node2.getNumChildren()
    """
    if node2.getNumChildren() == 1:
      raise Exception()
    """
    for curr_entry in entry_group1:
      curr_entry.getChild().setParent(node1)
    for curr_entry in entry_group2:
      curr_entry.getChild().setParent(node2)
    # seed_entry1.getChild().setParent(node1)
    # seed_entry2.getChild().setParent(node2)
    # remaining_entries = [x for x in E_overall if x != seed_entry1 and x != seed_entry2]
    mbc_group1 = [x.getMBC() for x in entry_group1]
    mbc_group2 = [x.getMBC() for x in entry_group2]
    # error here regarding mbr list
    result1 = MBC.combineMBCs(mbc_group1, num_children1)
    curr_overall_mbr1, n1 = result1
    result2 = MBC.combineMBCs(mbc_group2, num_children2)
    curr_overall_mbr2, n2 = result2
    # print entry_group1, entry_group2, entry
    for curr_entry in entry_group1:
      next_curr_node = curr_entry.getChild()
      if curr_entry != entry:
        # removing entries from node
        curr_node.removeEntry(curr_entry)
      # node1.addEntry(curr_entry)
      next_curr_node.setParent(node1)
    for curr_entry in entry_group2:
      next_curr_node = curr_entry.getChild()
      if curr_entry != entry:
        # removing entries from node
        curr_node.removeEntry(curr_entry)
      # node2.addEntry(curr_entry)
      next_curr_node.setParent(node2)
    # nodes with composite mbr's
    entry1 = SSTreeEntry(curr_overall_mbr1, node1)
    entry2 = SSTreeEntry(curr_overall_mbr2, node2)
    if parent != None:
      original_entry = parent.retrieveEntryForChild(curr_node)
      parent.removeEntry(original_entry)
    if node != self.getRootEntry().getChild():
      # node is not the root; node 'node' is split and parent gains an entry
      # entry.getChild().setParent(parent)
      # print parent.getChildren(), node
      # entry_for_removal = parent.retrieveEntryForChild(node)
      # parent.removeEntry(entry_for_removal)
      # print "current parent entries:", parent.getEntries()
      parent.addEntry(entry1)
      parent.addEntry(entry2)
      # curr_entry = parent.retrieveEntryForChild(curr_node)
      # parent.removeEntry(curr_entry)
      # print "num. of entries for parent:", len(parent.getEntries())
      # parent.addEntry(e)
      # parent.addEntry(ee)
      node1.setParent(parent)
      node2.setParent(parent)
      # node1.setParent(parent)
      # print "node #1:", node1.toString()
      # print "node #2:", node2.toString()
      # node2.setParent(parent)
      # print "parent again:", parent
      # print parent.getNumChildren()
    else:
      """
      print "creating a new root"
      print "node one subtree:", self.toNumChildrenStringHelper(node1)
      print "node two subtree:", self.toNumChildrenStringHelper(node2)
      """
      child1 = entry1.getChild()
      child2 = entry2.getChild()
      n1 = child1.getNumLeavesInSubtree()
      n2 = child2.getNumLeavesInSubtree()
      n = n1 + n2
      next_root = SSTreeNode(None, [entry1, entry2], False, n)
      self.getRootEntry().setChild(next_root)
      # this causes problems
      # entry.getChild().setParent(next_root)
      node1.setParent(next_root)
      node2.setParent(next_root)
      pass
    """
    if parent != None:
      print parent.retrieveEntryForChild(node1)
      print parent.retrieveEntryForChild(node2)
    """
    return (node1, node2, entry1, entry2)
  """
  # split a node associated with many entries while also considering provided entry
  # return a (l, ll, e, ee) tuple
  # break entries into two groups
  # 'node' is a full node that we wish to add 'entry' to
  # assume 'entry' is well-formed, i.e. it has an mbr and a node pointer
  def splitNode(self, node, entry):
    # print "node:", node.toString()
    # print "splitting a node"
    prev_leaf_status = node.isLeafNode()
    # associated with this operation is one for condenseTree
    # this line may be unnecessary
    # node.setIsLeafNode(False)
    curr_node = node
    # pick seeds
    E_overall = curr_node.getEntries() + [entry]
    # print "E_overall:", E_overall
    # result = RTree.linearPickSeeds(E_overall)
    result = SSTree.quadraticPickSeeds(E_overall)
    seed_entry1, seed_entry2 = result
    parent = curr_node.getParent()
    if parent != None:
      parent.setIsLeafNode(True)
    # if parent != None:
      # print "parent has a child:", node in parent.getChildren()
      # print "children and entries:", parent.getChildren(), parent.getEntries()
    # if parent != None:
      # entries = parent.getEntries()
    if parent != None and (node in parent.getChildren()):
      # print node, parent.getChildren()
      # print node in parent.getChildren()
      parent.removeEntry(parent.retrieveEntryForChild(node))
    # possibly questionable
    # entry.getChild().setParent(parent)
    # print "parent:", parent
    # print curr_node == self.getRoot()
    # propagating prev_leaf_status may be unnecessary
    node1 = SSTreeNode(parent, [seed_entry1], prev_leaf_status)
    node2 = SSTreeNode(parent, [seed_entry2], prev_leaf_status)
    # also possibly questionable
    # have seed entries in parent
    seed_entry1.getChild().setParent(node1)
    seed_entry2.getChild().setParent(node2)
    remaining_entries = [x for x in E_overall if x != seed_entry1 and x != seed_entry2]
    # error here regarding mbr list
    curr_overall_mbr1 = CompositeMBR(seed_entry1.getMBR().getUpperLeft(), seed_entry1.getMBR().getLowerRight(), [seed_entry1])
    curr_overall_mbr2 = CompositeMBR(seed_entry2.getMBR().getUpperLeft(), seed_entry2.getMBR().getLowerRight(), [seed_entry2])
    for i in range(len(remaining_entries)):
      curr_entry = remaining_entries[i]
      next_curr_node = curr_entry.getChild()
      # print curr_entry.getMBR().toString()
      # have an error here - num. of remaining entries is not properly decreasing
      num_remaining_entries = len(remaining_entries)
      curr_mbr = curr_entry.getMBR()
      # print curr_mbr.toString()
      enlargement1 = MBR.getAreaEnlargement(curr_overall_mbr1, curr_mbr)
      enlargement2 = MBR.getAreaEnlargement(curr_overall_mbr2, curr_mbr)
      # print enlargement1, enlargement2
      m = next_curr_node.getMinimumNumEntriesPerNode()
      size1 = len(curr_overall_mbr1.getMBRList())
      size2 = len(curr_overall_mbr2.getMBRList())
      lambda_entries = num_remaining_entries
      # if parent != None:
        # parent.removeEntry(curr_entry)
      # print "curr. node entries, curr. entry, entry:", curr_node.getEntries(), curr_entry, entry
      if curr_entry != entry:
        curr_node.removeEntry(curr_entry)
      # print "entries for node #1:", [x.getMBR().toString() for x in node1.getEntries()]
      # print "entries for node #2:", [x.getMBR().toString() for x in node2.getEntries()]
      if size1 == (m - lambda_entries):
        curr_overall_mbr1 = MBR.getEnlargedMBR(curr_overall_mbr1, curr_mbr)
        node1.addEntry(curr_entry)
        next_curr_node.setParent(node1)
        continue
      if size2 == (m - lambda_entries):
        curr_overall_mbr2 = MBR.getEnlargedMBR(curr_overall_mbr2, curr_mbr)
        node2.addEntry(curr_entry)
        next_curr_node.setParent(node2)
        continue
      if enlargement1 > enlargement2:
        curr_overall_mbr1 = MBR.getEnlargedMBR(curr_overall_mbr1, curr_mbr)
        node1.addEntry(curr_entry)
        next_curr_node.setParent(node1)
      elif enlargement2 > enlargement1:
        curr_overall_mbr2 = MBR.getEnlargedMBR(curr_overall_mbr2, curr_mbr)
        node2.addEntry(curr_entry)
        next_curr_node.setParent(node2)
      elif enlargement2 == enlargement1:
        if size1 <= size2:
          curr_overall_mbr1 = MBR.getEnlargedMBR(curr_overall_mbr1, curr_mbr)
          node1.addEntry(curr_entry)
          next_curr_node.setParent(node1)
        elif size1 > size2:
          # print curr_entry.getMBR().toString()
          curr_overall_mbr2 = MBR.getEnlargedMBR(curr_overall_mbr2, curr_mbr)
          node2.addEntry(curr_entry)
          next_curr_node.setParent(node2)
    # nodes with composite mbr's
    entry1 = SSTreeEntry(curr_overall_mbr1, node1)
    entry2 = SSTreeEntry(curr_overall_mbr2, node2)
    if node != self.getRootEntry().getChild():
      # entry.getChild().setParent(parent)
      # print parent.getChildren(), node
      # entry_for_removal = parent.retrieveEntryForChild(node)
      # parent.removeEntry(entry_for_removal)
      parent.addEntry(entry1)
      parent.addEntry(entry2)
      # parent.addEntry(e)
      # parent.addEntry(ee)
      node1.setParent(parent)
      node2.setParent(parent)
      # node1.setParent(parent)
      # print "node #1:", node1.toString()
      # print "node #2:", node2.toString()
      # node2.setParent(parent)
      # print "parent again:", parent
    else:
      next_root = SSTreeNode(None, [entry1, entry2], False)
      self.getRootEntry().setChild(next_root)
      # this causes problems
      # entry.getChild().setParent(next_root)
      node1.setParent(next_root)
      node2.setParent(next_root)
    return (node1, node2, entry1, entry2)
  """
  @staticmethod
  def rstarPreadjustTree(self, leaf_node):
    node = leaf_node
    parent = node.getParent()
    if parent != None:
      curr_entries = node.getEntries()
      entry = node.getParent().retrieveEntryForChild(node)
      children = [x.getChild() for x in curr_entries]
      mbr_list = [x.getMBR() for x in curr_entries]
      tight_overall_mbr = CompositeMBR.makeMBR(mbr_list)
      entry.setMBR(tight_overall_mbr)
  # adjust min. bounding rectangles, propagate a split, and handle pointer changes
  # node "node" is not the node that is shared by two nodes 
  #   as a parent for a split and that gains an entry; 
  #   rather, it is a child of a node that is shared by two 
  #   as a parent for a split that gains an entry
  @staticmethod
  def ssTreeAdjustTree(tree, node, resulting_entries_from_split, have_resulting_second_entry_from_split):
    # return tree.rstarAdjustTreeHelper(tree, node.getParent(), resulting_entries_from_split, have_resulting_second_entry_from_split)
    return tree.ssTreeAdjustTreeHelper(tree, node, resulting_entries_from_split, have_resulting_second_entry_from_split)
  # node "node" is a parent that has entries that can lead to a split
  # mbr's for entries of parent node "node" can lead to entry in parent having its mbr resized
  # partner mbr from a split from before can lead to its entry in parent having its mbr resized
  @staticmethod
  def ssTreeAdjustTreeHelper(tree, node, resulting_entries_from_split, 
have_resulting_second_entry_from_split):
  # def rstarAdjustTree(tree, node, resulting_entries_from_split, have_resulting_second_entry_from_split, is_first_call_after_first_pass):
    # print "adjusting tree"
    # print "pre-adjust-tree tree:", tree.toNumChildrenString()
    """
    e = None
    ee = None
    if have_resulting_second_entry_from_split == True:
      e, ee = resulting_entries_from_split
    else:
      e = resulting_entries_from_split[0]
    """
    # if node == tree.getRoot() or node.getParent() == None:
    # if node == None or node == tree.getRoot() or node.getParent() == None:
    # if node == tree.getRootEntry().getChild() or node == None or node.getParent() == None:
    if node.getParent() == None:
      # print "reached root or parent of root (non-existent)"
      # we have reached the root, which has no enclosing mbr
      # however, we may have to handle a split
      # no parent to speak of
      # print "reach root case"
      # however, we should modify pointers
      # print "num. entries:", resulting_entries_from_split[0].getChild().getNumEntries()
      """
      if have_resulting_second_entry_from_split == True:
        entry1, entry2 = resulting_entries_from_split
        if node.getNumEntries() > node.getMaximumNumEntriesPerNode():
          tree.rstarSplitNode(node, entry2)
      """
      entry = tree.getRootEntry()
      curr_entries = entry.getChild().getEntries()
      children = [x.getChild() for x in curr_entries]
      mbc_list = [x.getMBC() for x in curr_entries]
      n_values = [x.getNumLeavesInSubtree() for x in children]
      result = MBC.combineMBCs(mbc_list, n_values)
      tight_overall_mbc, n = result
      entry.setMBC(tight_overall_mbc)
      return (have_resulting_second_entry_from_split, resulting_entries_from_split)
      # return (have_resulting_second_entry_from_split, resulting_entries_from_split)
    else:
      # parent = node.getParent()
      parent = node.getParent()
      curr_entries = node.getEntries()
      # print "parent:", parent
      # entry = parent.retrieveEntryForChild(node)
      entry = None
      """
      if node.getParent() == None:
        entry = tree.getRootEntry()
      else:
        entry = node.getParent().retrieveEntryForChild(node)
      """
      entry = node.getParent().retrieveEntryForChild(node)
      children = [x.getChild() for x in curr_entries]
      mbc_list = [x.getMBC() for x in curr_entries]
      n_values = [x.getNumLeavesInSubtree() for x in children]
      # print "mbc list:", mbc_list
      result = MBC.combineMBCs(mbc_list, n_values)
      tight_overall_mbc, n = result
      entry.setMBC(tight_overall_mbc)
      # set N, NN
      # if N is root, stop
      # let P be parent of N
      # let E_N be N's entry in P
      # adjust E_N.I so that it tightly encloses all entry rectangles in N
      # if N has partner NN resulting from an earlier split, 
      # create a new entry E_NN with E_NN.p pointing to NN 
      # and E_NN.I enclosing all rectangles in NN
      partner_entry = None
      if have_resulting_second_entry_from_split == True:
        first_entry, second_entry = resulting_entries_from_split
        partner_entry = second_entry
        # parent.addEntry(partner_entry)
        # partner_entry.getChild().setParent(parent)
      if have_resulting_second_entry_from_split == True:
        partner_node = partner_entry.getChild()
        partner_entries = partner_node.getEntries()
        partner_children = [x.getChild() for x in partner_entries]
        partner_mbc_list = [x.getMBC() for x in partner_entries]
        partner_n_values = [x.getNumLeavesInSubtree() for x in partner_children]
        result = MBC.combineMBCs(partner_mbc_list, partner_n_values)
        partner_tight_overall_mbc, n = result
        partner_entry.setMBC(partner_tight_overall_mbc)
      if node.isLeafNode() == False:
        # add E_NN to P if there is room
        # otherwise, invoke SplitNode to produce P and PP 
        # containing E_NN and all P's old entries
        # set N to P and set NN to PP if a split occurred, repeat from AT2
        if have_resulting_second_entry_from_split == True:
          """
          index = parent.getIndexForEntry(entry)
          parent.removeIthEntry(index)
          """
          # remove an entry so as to clean
          # parent.removeEntry(entry)
          # if parent.isFull() == False:
          # print "num. of children seen:", parent.getNumChildren()
          if (parent.getNumChildren() + 1) <= parent.getMaximumNumEntriesPerNode():
            # there is room in parent
            # parent.addEntry(entry)
            parent.addEntry(partner_entry)
            # entry.getChild().setParent(parent)
            partner_entry.getChild().setParent(parent)
            # return tree.rstarAdjustTree(tree, parent, [entry], False, False)
            """
            if tree.hasConsistentNonTraditionalLeafDepthValues() == False:
              raise Exception()
            """
            # return tree.rstarAdjustTree(tree, parent, [entry], False)
            return SSTree.ssTreeAdjustTreeHelper(tree, node.getParent(), [entry], False)
          else:
            # ought to split the parent
            # parent.addEntry(entry)
            # entry.getChild().setParent(parent)
            # following is a risky choice
            # print tree.getRoot() == parent
            """
            print "pre-adjust-tree-split-node tree:", tree.toNumChildrenString()
            print "pre-split num-children string:", tree.toNumChildrenStringHelper(parent)
            print "pre-split splitting root:", parent == tree.getRoot()
            print "partner subtree:", tree.toNumChildrenStringHelper(partner_entry.getChild())
            """
            # split_result = tree.rstarSplitNode(parent.getChildren()[0], partner_entry)
            split_result = tree.ssTreeSplitNode(parent, partner_entry)
            l, ll, e, ee = split_result
            """
            print "post-split did split root:", parent == tree.getRoot()
            print "post-split replacement root exists:", l.getParent() == tree.getRoot()
            print "post-split num-children string:", tree.toNumChildrenStringHelper(l.getParent())
            print "post-adjust-tree-split-node tree:", tree.toNumChildrenString()
            """
            # parent.addEntry(e)
            # return tree.rstarAdjustTree(tree, l, [e, ee], True, False)
            # print "parents:", parent, l.getParent()
            return SSTree.ssTreeAdjustTreeHelper(tree, node.getParent(), [e, ee], True)
            """
            if parent != None:
              return tree.rstarAdjustTree(tree, parent, [e, ee], True)
            else:
              return (True, [e, ee])
            """
        else:
          # return (False, [])
          # return tree.rstarAdjustTree(tree, parent, [entry], False)
          return SSTree.ssTreeAdjustTreeHelper(tree, node.getParent(), [entry], False)
      else:
        return SSTree.ssTreeAdjustTreeHelper(tree, node.getParent(), resulting_entries_from_split, 
have_resulting_second_entry_from_split)
  # assume item is in tree
  # returns a node, which can be None if no match is found
  # finds one match if such a node exists
  # def delete(self, E, RN):
  def findLeaf(self, entry):
    return self.findLeafHelper(entry, self.getRootEntry())
  def findLeafHelper(self, entry, curr_entry):
    """
    if node.isLeafNode() == False:
      curr_mbr = entry.getMBR()
      entries = self.getEntries()
      tagged_mbr_list = [(x.getMBR(), x) for x in entries]
      tagged_overlapped_mbr_list = [x for x in tagged_mbr_list if MBR.doOverlap(curr_mbr, x[0]) == True]
      for tagged_overlapped_mbr in tagged_overlapped_mbr_list:
        curr_mbr, curr_entry = tagged_overlapped_mbr
        curr_node = curr_entry.getChild()
        result = self.findLeafHelper(entry, curr_node)
        if result == None:
          continue
        else:
          return curr_node
      return None
    """
    # a little stilted since we don't need a O(log(n)) time operation 
    # to find the entry containing node; just look at parent of entry child
    if curr_entry.getMBC().isRaw() == True:
      if entry == curr_entry:
        return True
      else:
        return False
    else:
      entries = curr_entry.getChild().getEntries()
      for next_entry in entries:
        if MBC.doOverlap(curr_entry.getMBC(), entry.getMBC()) == True:
          result = self.findLeafHelper(entry, next_entry)
          if result == True:
            return result
      return False
  def delete(self, entry):
    # print "hello"
    did_find_leaf = self.findLeaf(entry)
    child_node = entry.getChild()
    # root node never has a raw mbr
    leaf_node = child_node.getParent() if entry != self.getRootEntry() else None
    if leaf_node == None:
      raise Exception("expected a node to be found for a delete")
    leaf_node.removeEntry(entry)
    self.condenseTree(leaf_node)
    root = self.getRootEntry().getChild()
    """
    if root.getNumChildren() == 1:
      # shorten tree
      entries = root.getEntries()
      chosen_entry = entries[0]
      chosen_child = chosen_entry.getChild()
      self.setRoot(chosen_child)
    """
    # if RN is a leaf node
      # search all entries of RN to find E.mbr
    # else:
      # RN is an internal node
      # find all entries of RN that cover E.mbr
      # follow the corresponding subtrees unti lthe leaf L that contains E is found
      # remove E from L
    # call algorithm condenseTree(L)
    # if the root has only one child (and it is not a leaf)
      # remove the root
      # set as new root its only child
    pass
  def condenseTree(self, leaf_node):
    Q = []
    self.condenseTreeHelper(leaf_node, Q)
    # Q is in order of low-level to high-level; 
    # wish to insert using order of high-level to low-level
    Q.reverse()
    for curr_node in Q:
      # we never encounter a root; we never remove the root
      parent = curr_node.getParent()
      curr_entry = parent.retrieveEntryForChild(curr_node)
      self.insert(curr_entry)
  def condenseTreeHelper(self, node, Q):
    if node.getParent() == None:
      # we are a root node
      if self.getRootEntry().getChild().getNumChildren() == 0:
        root_node = SSTreeNode(None, [], True, 1)
        root_mbc = CompositeMBC(None, None, [])
        root_entry = SSTreeEntry(root_mbc, root_node)
        self.setRootEntry(root_entry)
        return
      else:
        entry = self.getRootEntry()
        curr_entries = entry.getChild().getEntries()
        children = [x.getChild() for x in curr_entries]
        mbc_list = [x.getMBC() for x in curr_entries]
        n_values = [x.getNumLeavesInSubtree() for x in children]
        result = MBC.combineMBCs(mbc_list, n_values)
        tight_overall_mbc, n = result
        entry.setMBC(tight_overall_mbc)
        return
    else:
      if node.isUnderfull() == True:
        parent = node.getParent()
        entry = parent.retrieveEntryForChild(node)
        keep_nodes = [x for x in self.getNodesForNode(node) if x.getParent().retrieveEntryForChild(x).getMBC().isRaw() == True]
        for keep_node in keep_nodes:
          Q.append(keep_node)
        parent.removeEntry(entry)
      if node.isUnderfull() == False:
        parent = node.getParent()
        entry = node.getParent().retrieveEntryForChild(node)
        curr_entries = node.getEntries()
        children = [x.getChild() for x in curr_entries]
        mbc_list = [x.getMBC() for x in curr_entries]
        n_values = [x.getNumLeavesInSubtree() for x in children]
        result = MBC.combineMBCs(mbc_list, n_values)
        tight_overall_mbc, n = result
        entry.setMBC(tight_overall_mbc)
      self.condenseTreeHelper(node.getParent(), Q)
      return
  """
  def BTreeSearch(self, x, k):
    # i = 1
    # while i <= x.n and k >= x.key_i
      # i = i + 1
    # if i <= x.n and k == x.key_i
      # return (x, i)
    # elif x.leaf == True
      # return None
    # else:
      # return BTreeSearch(x.c_i, k)
    pass
  """
  # result stored in NearestNeigbhor object nearest
  def nearestNeighborSearch(self, point, nearest):
    root_entry = self.getRootEntry()
    return self.nearestNeighborSearchHelper(root_entry, point, nearest)
  def nearestNeighborSearchHelper(self, entry, point, nearest):
    # print self.toString()
    """
    if node.isLeafNode() == True and node == self.getRoot():
      # no entries to speak of
      return
    """
    # if node.getNumEntries() == 0 and node != self.getRoot():
    # if node.isTraditionalLeafNode() == True and node != self.getRootEntry().getChild() and node.getNumEntries() == 0:
    node = entry.getChild()
    # if node.isTraditionalLeafNode() == True and node.getNumEntries() == 0:
    if node.isLeafNode() == True and node.getNumEntries() == 0:
      curr_entry = entry
      # using a more fine-grained definition for leaf
      # parent, rather than current node, has entries
      # print node.getParent().retrieveEntryForChild(node).getMBR().toString()
      # for i in range(node.getNumEntries()):
      # curr_entry = node.getParent().retrieveEntryForChild(node)
      # curr_entry = node.getIthEntry(i)
      mbc = curr_entry.getMBC()
      # print mbr.toString()
      dist = getDistance(point, Point.toPoint(mbc))
      # print "distances:", dist, nearest.getDistance()
      if dist < nearest.getDistance():
        nearest.setDistance(dist)
        nearest.setCloseItem(curr_entry.getMBC().getContainedItem())
    else:
      branchList = SSTree.genBranchList(point, entry)
      branchList = SSTree.sortBranchList(point, branchList)
      # last = RTree.NNPruneBranchList(node, nearest, branchList, point)
      last = SSTree.NNPruneBranchList(nearest, branchList, point)
      while len(last) != 0:
        # print last[0].getChild().isLeafNode(), last
        curr_entry = last.pop(0)
        curr_node = curr_entry.getChild()
        self.nearestNeighborSearchHelper(curr_entry, point, nearest)
        last = SSTree.NNPruneBranchList(nearest, last, point)
  def kNearestNeighborSearch(self, point, kNearest, k):
    root_entry = self.getRootEntry()
    return self.kNearestNeighborSearchHelper(root_entry, point, kNearest, k)
  def kNearestNeighborSearchHelper(self, entry, point, kNearest, k):
    # while True:
      """
      if node == self.getRoot():
        pass
      if node.isLeafNode() == True and node == self.getRoot():
        # no entries to speak of
        print "no entries to speak of"
        print node.getEntries()
        return
      """
      # if node.getNumEntries() == 0 and node != self.getRoot():
      # if node.isTraditionalLeafNode() == True and node != self.getRootEntry().getChild() and node.getNumEntries() == 0:
      node = entry.getChild()
      # print "num. of entries:", node.getNumEntries()
      if node.isLeafNode() == True and node.getNumEntries() == 0:
      # if first_node.isTraditionalLeafNode() == True and first_node.getNumEntries() == 0:
        # print "encountering a raw rectangle"
        # encountering a raw rectangle
        # print node.getChildren()
        curr_entry = entry
        # curr_entry = node.getParent().retrieveEntryForChild(node)
        mbc = curr_entry.getMBC()
        dist = getDistance(point, Point.toPoint(mbc))
        # print self.toString()
        # print dist, Point.toPoint(mbr)
        if dist <= kNearest.getFarthestCloseDistance() + 0.001 or kNearest.isFull() == False:
          close_item = curr_entry.getMBC().getContainedItem()
          kNearest.addAndRemoveIfNecessary(close_item)
      else:
        branchList = SSTree.genBranchList(point, entry)
        # print len(branchList)
        branchList = SSTree.sortBranchList(point, branchList)
        last = branchList
        # print [x.getMBR().toString() for x in branchList]
        # last = RTree.kNNPruneBranchList(node, kNearest, branchList, point)
        while len(last) != 0:
          # last = RTree.kNNPruneBranchList(node, kNearest, last, point)
          last = SSTree.kNNPruneBranchList(kNearest, last, point)
          if len(last) == 0:
            break
          curr_entry = last.pop(0)
          curr_node = curr_entry.getChild()
          self.kNearestNeighborSearchHelper(curr_entry, point, kNearest, k)
          # print len(last)
          # last = RTree.kNNPruneBranchList(node, kNearest, last, point)
  @staticmethod
  # def genBranchList(query_point, node):
  def genBranchList(query_point, entry):
    node = entry.getChild()
    # come up with a list of entries
    entries = (node.getEntries())[ : ]
    return entries
  @staticmethod
  def sortBranchList(query_point, branchList):
    # sort the entries to be in order of mindist metric ascending
    entries = branchList[ : ]
    entries.sort(key = lambda x: SSTree.ssTreeTwoDimensionalMinDist(query_point, x.getMBC()))
    # entries_duplicate = branchList[ : ]
    # entries.sort(key = lambda x: RTree.twoDimensionalMinDist(query_point, x.getMBR()))
    # print [RTree.twoDimensionalMinDist(query_point, x.getMBR()) for x in entries]
    # print len(entries)
    return entries
  @staticmethod
  # def NNPruneBranchList(node, nearest, branchList, point):
  def NNPruneBranchList(nearest, branchList, point):
    if len(branchList) == 0:
      return []
    # prune based on mindist and minmaxdist metrics and closest item seen so far
    entries = branchList
    min_dist_values = [SSTree.ssTreeTwoDimensionalMinDist(point, x.getMBC()) for x in entries]
    # min_max_dist_values = [SSTree.ssTreeTwoDimensionalMinMaxDist(point, x.getMBC()) for x in entries]
    # min_min_max_dist_value = min(min_max_dist_values)
    # print min_dist_values
    # print min_max_dist_values
    # tagged_actual_dist_values = None
    nearest_dist = nearest.getDistance()
    entries_to_keep = []
    for entry in entries:
      min_dist_value = SSTree.ssTreeTwoDimensionalMinDist(point, entry.getMBC())
      # min_max_dist_value = RTree.twoDimensionalMinMaxDist(point, entry.getMBR())
      do_prune = False
      # print min_dist_value, min_min_max_dist_value
      # print nearest_dist
      """
      if min_dist_value > min_min_max_dist_value:
        do_prune = True
      """
      if min_dist_value >= nearest_dist:
        do_prune = True
      if do_prune == False:
        entries_to_keep.append(entry)
    return entries_to_keep
  @staticmethod
  # def kNNPruneBranchList(node, kNearest, branchList, point):
  def kNNPruneBranchList(kNearest, branchList, point):
    if len(branchList) == 0:
      return []
    # prune based on mindist and minmaxdist metrics and closest k items seen so far
    entries = branchList
    # min_dist_values = [RTree.twoDimensionalMinDist(point, x.getMBR()) for x in entries]
    # min_max_dist_values = [RTree.twoDimensionalMinMaxDist(point, x.getMBR()) for x in entries]
    # min_min_max_dist_value = min(min_max_dist_values)
    # tagged_actual_dist_values = None
    entries_to_keep = []
    farthest_close_dist = kNearest.getFarthestCloseDistance()
    # print "farthest close dist:", farthest_close_dist
    for entry in entries:
      min_dist_value = SSTree.ssTreeTwoDimensionalMinDist(point, entry.getMBC())
      # print "min. dist. value:", min_dist_value
      # min_max_dist_value = RTree.twoDimensionalMinMaxDist(point, entry.getMBR())
      do_prune = False
      """
      if min_dist_value > min_min_max_dist_value + 0.001 and kNearest.isFull() == True:
        # do_prune = True
        pass
      """
      # prune approach #3
      if min_dist_value > farthest_close_dist + 0.001 and kNearest.isFull() == True:
        do_prune = True
        pass
      # print min_dist_value, min_min_max_dist_value
      # print entry.getMBR().toString(), do_prune
      if do_prune == False:
        entries_to_keep.append(entry)
    return entries_to_keep
  @staticmethod
  def ssTreeTwoDimensionalMinDist(p, mbc):
    centroid = mbc.getCentroid()
    radius = mbc.getRadius()
    distance = max(0, getDistance(p, centroid) - radius)
    return distance
  # s_i <= t_i for i in {1, 2}
  @staticmethod
  def twoDimensionalMinDist(p, mbr):
    p1 = p[0]
    p2 = p[1]
    upper_left = mbr.getUpperLeft()
    lower_right = mbr.getLowerRight()
    x1, y1 = upper_left
    x2, y2 = lower_right
    s1, s2 = (x1, y1)
    t1, t2 = (x2, y2)
    r1 = None
    r2 = None
    if p1 < s1:
      r1 = s1
    elif p1 > t1:
      r1 = t1
    else:
      r1 = p1
    if p2 < s2:
      r2 = s2
    elif p2 > t2:
      r2 = t2
    else:
      r2 = p2
    min_dist_squared = (p1 - r1) ** 2 + (p2 - r2) ** 2
    min_dist = math.sqrt(min_dist_squared)
    return min_dist
  @staticmethod
  def twoDimensionalMinMaxDist(p, mbr):
    p1 = p[0]
    p2 = p[1]
    upper_left = mbr.getUpperLeft()
    lower_right = mbr.getLowerRight()
    x1, y1 = upper_left
    x2, y2 = lower_right
    s1, s2 = (x1, y1)
    t1, t2 = (x2, y2)
    rm1 = None
    rm2 = None
    rM1 = None
    rM2 = None
    if p1 <= (s1 + t1) / (1.0 * 2):
      rm1 = s1
    else:
      rm1 = t1
    if p2 <= (s2 + t2) / (1.0 * 2):
      rm2 = s2
    else:
      rm2 = t2
    if p1 >= (s1 + t1) / (1.0 * 2):
      rM1 = s1
    else:
      rM1 = t1
    if p2 >= (s2 + t2) / (1.0 * 2):
      rM2 = s2
    else:
      rM2 = t2
    max_dist_squared1 = (p1 - rm1) ** 2 + (p2 - rM2) ** 2
    max_dist_squared2 = (p2 - rm2) ** 2 + (p1 - rM1) ** 2
    min_max_dist_squared = min(max_dist_squared1, max_dist_squared2)
    min_max_dist = math.sqrt(min_max_dist_squared)
    return min_max_dist
  def draw(self):
    # im = Image.new("RGB", (512, 512), "white")
    """
    im = Image.new("RGB", (768, 768), "white")
    draw = ImageDraw.Draw(im)
    root = self.getRoot()
    root.draw(self, draw, 0)
    im.save("tree.png", "PNG")
    """
    image = PythonMagick.Image(PythonMagick.Geometry("768x768"), "white")
    # image = PythonMagick.Image(PythonMagick.Geometry("1536x1536"), "white")
    root_entry = self.getRootEntry()
    entries = [root_entry]
    SSTreeEntry.draw(self, entries, image, 0)
    """
    image.strokeColor("orange")
    image.fillColor("none")
    image.strokeWidth(4)
    multiplier = 3 * 0.8
    # offset = (768 * 0.2) / 2
    offset = (1536 * 0.2) / 2
    x1 = 0
    y1 = 0
    x2 = 47
    y2 = 60
    next_x1 = x1 * multiplier + offset
    next_y1 = y1 * multiplier + offset
    next_x2 = x2 * multiplier + offset
    next_y2 = y2 * multiplier + offset
    """
    # image.draw(PythonMagick.DrawableRectangle(next_x1, next_y1, next_x2, next_y2))
    image.write("tree.png")
  # prefix order
  def getNodes(self):
    node_list = []
    self.getNodesHelper(self.getRootEntry().getChild(), node_list)
    return node_list
  def getNodesHelper(self, node, partial_result):
    partial_result.append(node)
    for curr_node in node.getChildren():
      self.getNodesHelper(curr_node, partial_result)
  def getNodesForNode(self, node):
    node_list = []
    self.getNodesHelper(node, node_list)
    return node_list
def main():

  point1 = Point(100, 100, 1)
  point2 = Point(50, 100, 2)
  point3 = Point(60, 100, 3)
  point4 = Point(70, 100, 4)
  point5 = Point(80, 100, 5)
  point6 = Point(90, 100, 6)
  point7 = Point(110, 100, 7)
  point8 = Point(120, 100, 8)
  mbc1 = RawMBC(point1)
  mbc2 = RawMBC(point2)
  mbc3 = CompositeMBC((50, 100), 50, [])
  entry1 = SSTreeEntry(mbc1, None)
  entry2 = SSTreeEntry(mbc2, None)
  entry3 = SSTreeEntry(mbc3, None)
  node1 = SSTreeNode(None, [], True, 1)
  node2 = SSTreeNode(None, [], True, 1)
  node3 = SSTreeNode(None, [entry1, entry2], False, 2)
  entry1.setChild(node1)
  entry2.setChild(node2)
  entry3.setChild(node3)
  node1.setParent(node3)
  node2.setParent(node3)
  tree = SSTree()
  print tree.toString()
  curr_root = tree.getRootEntry().getChild()
  # entry1.setChild(RTreeNode(tree.getRoot(), [entry1]))
  # insert always adds a leaf

  curr_entry1 = SSTreeEntry(RawMBC(point1), SSTreeNode(None, [], True, 1))
  tree.insert(curr_entry1)
  print tree.toString()
  tree.insert(SSTreeEntry(RawMBC(point2), SSTreeNode(None, [], True, 1)))
  tree.insert(SSTreeEntry(RawMBC(point3), SSTreeNode(None, [], True, 1)))
  tree.insert(SSTreeEntry(RawMBC(point4), SSTreeNode(None, [], True, 1)))
  print tree.getRootEntry().getChild()
  tree.insert(SSTreeEntry(RawMBC(point5), SSTreeNode(None, [], True, 1)))
  tree.insert(SSTreeEntry(RawMBC(point6), SSTreeNode(None, [], True, 1)))
  print tree.toString()
  tree.insert(SSTreeEntry(RawMBC(point7), SSTreeNode(None, [], True, 1)))
  curr_entry2 = SSTreeEntry(RawMBC(point8), SSTreeNode(None, [], True, 1))
  tree.insert(curr_entry2)
  print tree.toString()
  nearest_result = NearestNeighbor()
  tree.nearestNeighborSearch((50, 0), nearest_result)
  print nearest_result.toString()
  k_nearest_result = KNearestNeighbor((50, 0), PriorityQueue(), 2)
  tree.kNearestNeighborSearch((50, 0), k_nearest_result, 2)
  print k_nearest_result.toString()

  import sys
  import string
  x = 0
  y = 0
  location = (x, y)
  tree2 = SSTree()
  id_value = 1
  # example insert
  point = Point(location[0], location[1], id_value)
  tree2.insert(SSTreeEntry(RawMBC(point), SSTreeNode(None, [], True, 1)))
  # retrieve a string representation of tree
  print tree.toString()
  # example nn query
  nearest_result = NearestNeighbor()
  tree2.nearestNeighborSearch(location, nearest_result)
  close_item = nearest_result.getCloseItem()
  distance = nearest_result.getDistance()
  found_location = (close_item.getX(), close_item.getY())
  print found_location, distance
  # example k-nn query
  k = 10
  k_nearest_result = KNearestNeighbor(location, PriorityQueue(), k)
  tree2.kNearestNeighborSearch(location, k_nearest_result, k)
  close_items = k_nearest_result.getCloseItems()
  farthest_close_distance = k_nearest_result.getFarthestCloseDistance()
  found_locations = [(x.getX(), x.getY()) for x in close_items]
  print found_locations, farthest_close_distance


  print tree.toString()
  tree.delete(curr_entry2)
  tree.delete(curr_entry1)
  tree.insert(curr_entry2)
  print tree.toString()

  tree3 = SSTree()

  import random
  points = []
  for i in xrange(10):
    x = int(random.random() * 1000)
    y = int(random.random() * 1000)
    point = Point(x, y, None)
    points.append(point)
  for point in points:
    tree3.insert(SSTreeEntry(RawMBC(point), SSTreeNode(None, [], True, 1)))
  print tree3.toString()

  entries = [x.getParent().retrieveEntryForChild(x) for x in tree3.getNodes() if x.getParent() != None and x.getParent().retrieveEntryForChild(x).getMBC().isRaw() == True]
  for entry in entries:
    tree3.delete(entry)
  print tree3.toString()

if __name__ == "__main__":
  main()
