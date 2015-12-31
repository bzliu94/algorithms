# 2015-07-04

# r-star-tree featuring insert, nn and k-nn search with threshold distance

# tie-breaking for same distance is identifier value with largest values appearing earlier

# have root entry instead of solely root node

import sys

# import Image, ImageDraw

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

class RTreeNode:

  def __init__(self, parent, entries, is_leaf):

    self.parent = parent

    # self.entries = entries

    self.is_leaf = is_leaf

    self.m = 8

    self.M = 16

    self.child_to_entry_dict = {}

    for entry in entries:

      curr_child = entry.getChild()

      (self.child_to_entry_dict)[curr_child] = entry

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

  def isTraditionalLeafNode(self):

    is_traditional_leaf_node = self.getNumEntries() == 0

    return is_traditional_leaf_node

  def isLeafNode(self):

    # is root or have a child that is traditional leaf

    is_leaf_node = (self.getParent() == None and self.getNumChildren() == 0) or (self.getNumChildren() != 0 and self.getEntries()[0].getChild().getNumEntries() == 0)

    return is_leaf_node

    # return self.getNumChildren() == 0

    # return self.is_leaf

  def setIsLeafNode(self, is_leaf):

    self.is_leaf = is_leaf

  def addEntry(self, entry):

    # print "adding an entry:", entry.getMBR().toString()

    # (self.entries).append(entry)

    curr_child = entry.getChild()

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

  def toString(self):

    return str(self.getEntries())

# an entry is effectively an (mbr, child) pair

# mbr may be composite or raw

class RTreeEntry:

  def __init__(self, mbr, child):

    self.mbr = mbr

    self.child = child

  def getMBR(self):

    return self.mbr

  def setMBR(self, mbr):

    self.mbr = mbr

  def getChild(self):

    return self.child

  def setChild(self, node):

    self.child = node

  @staticmethod

  def draw(tree, entries, image, depth):

    for entry in entries:

      RTreeEntry.drawHelper(tree, entry, image, depth)

  @staticmethod

  # def draw(self, tree, draw, depth):

  def drawHelper(tree, entry, image, depth):

    node = entry.getChild()

    entries = node.getEntries()

    mbr_list = [entry.getMBR()]

    for mbr in mbr_list:

      upper_left = mbr.getUpperLeft()

      lower_right = mbr.getLowerRight()

      x1, y1 = upper_left

      x2, y2 = lower_right

      # multiplier = 3 * 0.8

      # multiplier = 1 / (1.0 * 1302) * 0.8

      multiplier = 1 / (1.0 * 6.5) * 0.8

      # offset = (768 * 0.2) / 2

      offset = (1536 * 0.2) / 2

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

      if upper_left == lower_right:

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

        image.draw(PythonMagick.DrawableRectangle(next_x1, next_y1, next_x2, next_y2))

    # mbr_list = [x.getMBR() for x in entries]

    # if len(entries) == 0 and tree.getRootEntry().getChild() != self:

    if len(entries) == 0:

      # draw a point

      parent = entry.getChild().getParent()

      # entry = parent.retrieveEntryForChild(self)

      # entry = self

      mbr = entry.getMBR()

      location = Point.toPoint(mbr)

      x, y = location

      # multiplier = 3 * 0.8

      # multiplier = 1 / (1.0 * 1302) * 0.8

      multiplier = 1 / (1.0 * 6.5) * 0.8

      # offset = (768 * 0.2) / 2

      offset = (1536 * 0.2) / 2

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

class MBR:

  def __init__(self, upper_left, lower_right):

    self.upper_left = upper_left

    self.lower_right = lower_right

  def isRaw(self):

    return False

  def isComposite(self):

    return False

  def getUpperLeft(self):

    return self.upper_left

  def getLowerRight(self):

    return self.lower_right

  def getArea(self):

    upper_left = self.getUpperLeft()

    lower_right = self.getLowerRight()

    x1, y1 = upper_left

    x2, y2 = lower_right

    side1_length = x2 - x1

    side2_length = y2 - y1

    area = side1_length * side2_length

    return area

  # require that base_mbr is composite and mbr is raw or composite

  # return a composite MBR object

  @staticmethod

  def getEnlargedMBR(base_mbr, mbr):

    mbr_list = [base_mbr, mbr]

    upper_left_points = [x.getUpperLeft() for x in mbr_list]

    lower_right_points = [x.getLowerRight() for x in mbr_list]

    points = upper_left_points + lower_right_points

    x_values = [x[0] for x in points]

    y_values = [x[1] for x in points]

    min_x_value = min(x_values)

    max_x_value = max(x_values)

    min_y_value = min(y_values)

    max_y_value = max(y_values)

    upper_left_point = (min_x_value, min_y_value)

    lower_right_point = (max_x_value, max_y_value)

    result_mbr_list = base_mbr.getMBRList() + [mbr]

    mbr = CompositeMBR(upper_left_point, lower_right_point, result_mbr_list)

    return mbr

  @staticmethod

  def getAreaEnlargement(base_mbr, mbr):

    base_mbr_area = base_mbr.getArea()

    enlarged_mbr = MBR.getEnlargedMBR(base_mbr, mbr)

    enlarged_mbr_area = enlarged_mbr.getArea()

    area_change = enlarged_mbr_area - base_mbr_area

    return area_change

  @staticmethod

  def doOverlap(mbr_a, mbr_b):

    upper_left_a = mbr_a.getUpperLeft()

    lower_right_a = mbr_a.getLowerRight()

    upper_left_b = mbr_b.getUpperLeft()

    lower_right_b = mbr_b.getLowerRight()

    x_a1, y_a1 = upper_left_a

    x_a2, y_a2 = lower_right_a

    x_b1, y_b1 = upper_left_b

    x_b2, y_b2 = lower_right_b

    do_overlap = x_a1 < x_b2 and x_a2 > x_b1 and y_a1 < y_b2 and y_a2 > y_b1

    # print mbr_a.toString(), mbr_b.toString(), do_overlap

    return do_overlap

  @staticmethod

  def findOverlapArea(mbr_a, mbr_b):

    if MBR.doOverlap(mbr_a, mbr_b) == False:

      return 0

    else:

      upper_left_a = mbr_a.getUpperLeft()

      x_a1, y_a1 = upper_left_a

      lower_right_a = mbr_a.getLowerRight()

      x_a2, y_a2 = lower_right_a

      upper_left_b = mbr_b.getUpperLeft()

      x_b1, y_b1 = upper_left_b

      lower_right_b = mbr_b.getLowerRight()

      x_b2, y_b2 = lower_right_b

      """

      print x_a1, y_a1

      print x_a2, y_a2

      print x_b1, y_b1

      print x_b2, y_b2

      """

      side1 = max(0, min(x_a2, x_b2) - max(x_a1, x_b1))

      side2 = max(0, min(y_a2, y_b2) - max(y_a1, y_b1))

      intersection_area = side1 * side2

      return intersection_area

  def getMarginValue(self):

    upper_left = self.getUpperLeft()

    lower_right = self.getLowerRight()

    x1, y1 = upper_left

    x2, y2 = lower_right

    margin = 2 * (x2 - x1) + 2 * (y2 - y1)

    return margin

  def getCenter(self):

    upper_left = self.getUpperLeft()

    lower_right = self.getLowerRight()

    x1, y1 = upper_left

    x2, y2 = lower_right

    x_center = (x1 + x2) / (1.0 * 2)

    y_center = (y1 + y2) / (1.0 * 2)

    center = (x_center, y_center)

    return center

  def toString(self):

    upper_left = self.getUpperLeft()

    lower_right = self.getLowerRight()

    x1, y1 = upper_left

    x2, y2 = lower_right

    return "[" + str(x1) + ", " + str(y1) + ", " + str(x2) + ", " + str(y2) + "]"

class RawMBR(MBR):

  def __init__(self, upper_left, lower_right, contained_item):

    MBR.__init__(self, upper_left, lower_right)


    self.contained_item = contained_item

  def isRaw(self):

    return True

  @staticmethod

  def makeMBRFromPoint(point):

    upper_left = point

    lower_right = point

    result_mbr = RawMBR(upper_left, lower_right, point)

    return result_mbr

  def getContainedItem(self):

    # print self.contained_item

    return self.contained_item

  def getMBRList(self):

    return [self]

# mbr_list is a list of mbr's that can be either all raw or all composite

class CompositeMBR(MBR):

  def __init__(self, upper_left, lower_right, mbr_list):

    MBR.__init__(self, upper_left, lower_right)

    self.mbr_list = mbr_list

  def getMBRList(self):

    return self.mbr_list

  def isComposite(self):

    return True

  @staticmethod

  def makeMBR(component_mbr_list):

    upper_left_points = [x.getUpperLeft() for x in component_mbr_list]

    lower_right_points = [x.getLowerRight() for x in component_mbr_list]

    points = upper_left_points + lower_right_points

    x_values = [x[0] for x in points]

    y_values = [x[1] for x in points]

    min_x_value = min(x_values)

    max_x_value = max(x_values)

    min_y_value = min(y_values)

    max_y_value = max(y_values)

    overall_upper_left = (min_x_value, min_y_value)

    overall_lower_right = (max_x_value, max_y_value)

    result_mbr = CompositeMBR(overall_upper_left, overall_lower_right, component_mbr_list)

    return result_mbr

class Point:

  def __init__(self, x, y, id_value):

    self.x = x

    self.y = y

    self.id_value = id_value

  @staticmethod

  def toPoint(mbr):

    if mbr.getUpperLeft() != mbr.getLowerRight():

      raise Exception("attempted to turn a non-point mbr to a point")

    return mbr.getUpperLeft()

  def getX(self):

    return self.x

  def getY(self):

    return self.y

  def getIDValue(self):

    return self.id_value

import string

class RTree:

  def __init__(self):

    root_node = RTreeNode(None, [], True)

    root_mbr = CompositeMBR(None, None, None)

    root_entry = RTreeEntry(root_mbr, root_node)

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

    # print "node:", node

    # print "entries:", entries

    children = node.getChildren()

    have_node_str = True

    if node == self.getRootEntry().getChild():

      have_node_str = False

    overall_str_list = None

    # print "current node:", node

    # print "root:", self.getRoot()

    # print "root entries:", self.getRoot().getEntries()

    if have_node_str == True:

      # print node, self.getRoot()

      # print node.getNumEntries(), self.getRoot().getNumEntries()

      overall_str_list = [node.getParent().retrieveEntryForChild(node).getMBR().toString()]

    else:

      overall_str_list = []

    for entry in entries:

      child = entry.getChild()

      child_str = self.toStringHelper(child)

      curr_str = child_str

      # print "child string:", child_str

      overall_str_list.append(curr_str)

    overall_str = "(" + string.join(overall_str_list, " ") + ")"

    return overall_str

  """

  def setRoot(self, node):

    self.root = node

  def getRoot(self):

    return self.root

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

  # return a tuple (x_distributions1, x_distributions2, y_distributions1, y_distributions2)

  # where each element is a list of distributions, with each distribution being a pair

  # (left_entries, right_entries)

  @staticmethod

  def rstarGenDistributions(entries, M, m):

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

    low_x_sorted_entries = entries[ : ]

    low_x_sorted_entries.sort(key = lambda x: x.getMBR().getUpperLeft()[0])

    low_x_distributions = [(low_x_sorted_entries[ : window_left_sizes[i]], low_x_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]

    # print "low x distributions:", low_x_distributions

    upper_x_sorted_entries = entries[ : ]

    upper_x_sorted_entries.sort(key = lambda x: x.getMBR().getLowerRight()[0])

    upper_x_distributions = [(upper_x_sorted_entries[ : window_left_sizes[i]], upper_x_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]

    low_y_sorted_entries = entries[ : ]

    low_y_sorted_entries.sort(key = lambda x: x.getMBR().getUpperLeft()[1])

    low_y_distributions = [(low_y_sorted_entries[ : window_left_sizes[i]], low_y_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]

    upper_y_sorted_entries = entries[ : ]

    upper_y_sorted_entries.sort(key = lambda x: x.getMBR().getLowerRight()[1])

    upper_y_distributions = [(upper_y_sorted_entries[ : window_left_sizes[i]], upper_y_sorted_entries[window_left_sizes[i] : ]) for i in range(len(window_left_sizes))]

    result = (low_x_distributions, upper_x_distributions, low_y_distributions, upper_y_distributions)

    # print "result:", result

    return result

  # returns 0 for x, 1 for y

  @staticmethod

  def rstarChooseSplitAxis(entries, M, m):

    result = RTree.rstarGenDistributions(entries, M, m)

    # print "entries:", entries

    low_x_distributions, upper_x_distributions, low_y_distributions, upper_y_distributions = result

    S_x = 0

    low_x_constituent_mbr_list_pairs = [([y.getMBR() for y in x[0]], [y.getMBR() for y in x[1]]) for x in low_x_distributions]

    low_x_mbr_pairs = [(CompositeMBR.makeMBR(x[0]), CompositeMBR.makeMBR(x[1])) for x in low_x_constituent_mbr_list_pairs]

    low_x_margin_values = [x[0].getMarginValue() + x[1].getMarginValue() for x in low_x_mbr_pairs]

    low_x_margin_value_sum = sum(low_x_margin_values)

    S_x = S_x + low_x_margin_value_sum

    upper_x_constituent_mbr_list_pairs = [([y.getMBR() for y in x[0]], [y.getMBR() for y in x[1]]) for x in upper_x_distributions]

    upper_x_mbr_pairs = [(CompositeMBR.makeMBR(x[0]), CompositeMBR.makeMBR(x[1])) for x in upper_x_constituent_mbr_list_pairs]

    upper_x_margin_values = [x[0].getMarginValue() + x[1].getMarginValue() for x in upper_x_mbr_pairs]

    upper_x_margin_value_sum = sum(upper_x_margin_values)

    S_x = S_x + upper_x_margin_value_sum

    S_y = 0

    low_y_constituent_mbr_list_pairs = [([y.getMBR() for y in x[0]], [y.getMBR() for y in x[1]]) for x in low_y_distributions]

    low_y_mbr_pairs = [(CompositeMBR.makeMBR(x[0]), CompositeMBR.makeMBR(x[1])) for x in low_y_constituent_mbr_list_pairs]

    low_y_margin_values = [x[0].getMarginValue() + x[1].getMarginValue() for x in low_y_mbr_pairs]

    low_y_margin_value_sum = sum(low_y_margin_values)

    S_y = S_y + low_y_margin_value_sum

    upper_y_constituent_mbr_list_pairs = [([y.getMBR() for y in x[0]], [y.getMBR() for y in x[1]]) for x in upper_y_distributions]

    upper_y_mbr_pairs = [(CompositeMBR.makeMBR(x[0]), CompositeMBR.makeMBR(x[1])) for x in upper_y_constituent_mbr_list_pairs]

    upper_y_margin_values = [x[0].getMarginValue() + x[1].getMarginValue() for x in upper_y_mbr_pairs]

    upper_y_margin_value_sum = sum(upper_y_margin_values)

    S_y = S_y + upper_y_margin_value_sum

    if S_x <= S_y:

      return 0

    elif S_x > S_y:

      return 1

  # return a tuple of two lists of entries

  # axis is 0 for x, 1 for y

  @staticmethod

  def rstarChooseSplitIndex(entries, axis, M, m):

    result = RTree.rstarGenDistributions(entries, M, m)

    low_x_distributions, upper_x_distributions, low_y_distributions, upper_y_distributions = result

    # consider cross-group overlap and combined area

    candidate_distributions = None

    if axis == 0:

      candidate_distributions = low_x_distributions + upper_x_distributions

    elif axis == 1:

      candidate_distributions = low_y_distributions + upper_y_distributions

    mbr_list_pair_tagged_candidate_distributions = [(([y.getMBR() for y in x[0]], [y.getMBR() for y in x[1]]), x) for x in candidate_distributions]

    mbr_pair_tagged_candidate_distributions = [((CompositeMBR.makeMBR(x[0][0]), CompositeMBR.makeMBR(x[0][1])), x[1]) for x in mbr_list_pair_tagged_candidate_distributions]

    overlap_value_tagged_candidate_distributions = [(MBR.findOverlapArea(x[0][0], x[0][1]), x[1]) for x in mbr_pair_tagged_candidate_distributions]

    overlap_values = [x[0] for x in overlap_value_tagged_candidate_distributions]

    min_overlap_value = min(overlap_values)

    # print "overlap values:", overlap_values, min_overlap_value

    matching_overlap_value_tagged_candidate_distributions = [x for x in overlap_value_tagged_candidate_distributions if x[0] == min_overlap_value]

    next_next_candidates = [x[1] for x in matching_overlap_value_tagged_candidate_distributions]

    # print next_next_candidates

    if len(matching_overlap_value_tagged_candidate_distributions) > 1:

      next_candidate_distributions = next_next_candidates

      mbr_list_pair_tagged_candidate_distributions = [(([y.getMBR() for y in x[0]], [y.getMBR() for y in x[1]]), x) for x in next_candidate_distributions]

      mbr_pair_tagged_next_candidate_distributions = [((CompositeMBR.makeMBR(x[0][0]), CompositeMBR.makeMBR(x[0][1])), x[1]) for x in mbr_list_pair_tagged_candidate_distributions]

      combined_area_tagged_next_candidate_distributions = [(x[0][0].getArea() + x[0][1].getArea(), x[1]) for x in mbr_pair_tagged_next_candidate_distributions]

      combined_area_values = [x[0] for x in combined_area_tagged_next_candidate_distributions]

      # print "combined area values:", combined_area_values

      # raise Exception()

      min_combined_area_value = min(combined_area_values)

      matching_combined_area_tagged_next_candidate_distributions = [x for x in combined_area_tagged_next_candidate_distributions if x[0] == min_combined_area_value]

      next_next_candidates = [x[1] for x in matching_combined_area_tagged_next_candidate_distributions]

    chosen_distribution_pair = next_next_candidates[0]

    # print "chosen distribution pair:", chosen_distribution_pair

    return chosen_distribution_pair

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

  def chooseLeaf(self, entry):

    return self.chooseLeafHelper(entry, self.getRootEntry().getChild())

  def chooseLeafHelper(self, entry, node):

    if node.isLeafNode() == True:

      return node

    else:

      entries = node.getEntries()

      candidate_entries = self.chooseEntriesWithMinimalAreaEnlargement(entries, entry)

      if len(candidate_entries) != 1:

        # resolve a tie

        candidate_entries = self.resolveEnlargementTie(candidate_entries, entry)

      chosen_entry = candidate_entries[0]

      chosen_child = chosen_entry.getChild()

      return self.chooseLeafHelper(entry, chosen_child)

  def rstarChooseLeaf(self, entry):

    return self.rstarChooseLeafHelper(entry, self.getRootEntry().getChild())

  def rstarChooseLeafHelper(self, entry, node):

    if node.isLeafNode() == True:

      return node

    else:

      entries = node.getEntries()

      candidate_entries = None

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

      chosen_entry = candidate_entries[0]

      chosen_child = chosen_entry.getChild()

      return self.rstarChooseLeafHelper(entry, chosen_child)

  def insert(self, entry):

    # print entry.getMBR().toString()

    # print entry.getMBR().getUpperLeft()[0]

    # if abs(entry.getMBR().getUpperLeft()[0] - 988266.168186) < 0.1:

    # if abs(entry.getMBR().getUpperLeft()[0] - 185061.9338) < 0.1:

    # if abs(entry.getMBR().getUpperLeft()[0] - 75898.2202098) < 0.1:

    if abs(entry.getMBR().getUpperLeft()[0] - 185061.9338) < 0.1:

      # raise Exception()

      pass

    # print "inserting an entry"

    if self.hasConsistentNonTraditionalLeafDepthValues() == False and self.getRootEntry().getChild().isLeafNode() == False:

      # raise Exception()

      pass

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

    leaf_node = self.rstarChooseLeaf(entry)

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

      adjust_result = RTree.rstarAdjustTree(self, leaf_node, [entry], False)

    else:

      # split node

      # split_result = self.rstarSplitNode(leaf_node.getChildren()[0], entry)

      split_result = self.rstarSplitNode(leaf_node, entry)

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

      adjust_result = RTree.rstarAdjustTree(self, l, [e, ee], True)

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

      if (tree.getRootEntry().getChild().getNumEntries() + 1) <= tree.getRootEntry().getChild().getMaximumNumEntriesPerNode():

        # there is space at root

        # tree.getRoot().addEntry(e)

        # raise Exception()

        tree.getRootEntry().getChild().addEntry(ee)

        # l.setParent(tree.getRoot())

        ll.setParent(tree.getRootEntry().getChild())

      else:

        # split_result = tree.rstarSplitNode(tree.getRoot().getChildren()[0], ee)

        split_result = tree.rstarSplitNode(tree.getRootEntry().getChild(), ee)

        l, ll, e, ee = split_result

        # e, ee = resulting_entries_from_split

        # print "resulting entries:", resulting_entries_from_split

        resulting_entries_from_split = [e, ee]

        next_root = RTreeNode(None, resulting_entries_from_split, False)

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

  def rstarSplitNode(self, node, entry):

    curr_node = node

    E_overall = list(set(curr_node.getEntries() + [entry]))

    return self.rstarSplitNodeHelper(node, E_overall, entry)

  def rstarSplitNodeHelper(self, node, E_overall, entry):

    # print "splitting a node"

    # print "pre-split-node tree:", tree.toNumChildrenString()

    # print node == self.getRoot()

    # print node.getNumEntries()

    # find distribution

    # adjust pointers

    # have a recursive call

    prev_leaf_status = node.isLeafNode()

    curr_node = node

    # pick seeds

    # be sure that entry is not included in existing list of entries

    # this takes too much time as it is

    # E_overall = list(set(curr_node.getEntries() + [entry]))

    # print E_overall

    m = self.getRootEntry().getChild().getMinimumNumEntriesPerNode()

    M = self.getRootEntry().getChild().getMaximumNumEntriesPerNode()

    # print "num. of entries overall:", len(E_overall)

    axis = RTree.rstarChooseSplitAxis(E_overall, M, m)

    # print axis

    result = RTree.rstarChooseSplitIndex(E_overall, axis, M, m)

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

    node1 = RTreeNode(parent, entry_group1, prev_leaf_status)

    node2 = RTreeNode(parent, entry_group2, prev_leaf_status)

    # print "num. of children:", node1.getNumChildren(), node2.getNumChildren()

    if node2.getNumChildren() == 1:

      raise Exception()

    for curr_entry in entry_group1:

      curr_entry.getChild().setParent(node1)

    for curr_entry in entry_group2:

      curr_entry.getChild().setParent(node2)

    # seed_entry1.getChild().setParent(node1)

    # seed_entry2.getChild().setParent(node2)

    # remaining_entries = [x for x in E_overall if x != seed_entry1 and x != seed_entry2]

    mbr_group1 = [x.getMBR() for x in entry_group1]

    mbr_group2 = [x.getMBR() for x in entry_group2]

    # error here regarding mbr list

    curr_overall_mbr1 = CompositeMBR.makeMBR(mbr_group1)

    curr_overall_mbr2 = CompositeMBR.makeMBR(mbr_group2)

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

    entry1 = RTreeEntry(curr_overall_mbr1, node1)

    entry2 = RTreeEntry(curr_overall_mbr2, node2)

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

      """

      """

      next_root = RTreeNode(None, [entry1, entry2], False)

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

    result = RTree.quadraticPickSeeds(E_overall)

    seed_entry1, seed_entry2 = result

    parent = curr_node.getParent()

    if parent != None:

      parent.setIsLeafNode(True)

    """

    if parent != None:

      # print "parent has a child:", node in parent.getChildren()

      # print "children and entries:", parent.getChildren(), parent.getEntries()

    if parent != None:

      entries = parent.getEntries()

    """

    if parent != None and (node in parent.getChildren()):
	
      # print node, parent.getChildren()

      # print node in parent.getChildren()

      parent.removeEntry(parent.retrieveEntryForChild(node))

    # possibly questionable

    # entry.getChild().setParent(parent)

    # print "parent:", parent

    # print curr_node == self.getRoot()

    # propagating prev_leaf_status may be unnecessary

    node1 = RTreeNode(parent, [seed_entry1], prev_leaf_status)

    node2 = RTreeNode(parent, [seed_entry2], prev_leaf_status)

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

      """

      if parent != None:

        parent.removeEntry(curr_entry)

      """

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

    entry1 = RTreeEntry(curr_overall_mbr1, node1)

    entry2 = RTreeEntry(curr_overall_mbr2, node2)

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

      next_root = RTreeNode(None, [entry1, entry2], False)

      self.getRootEntry().setChild(next_root)

      # this causes problems

      # entry.getChild().setParent(next_root)

      node1.setParent(next_root)

      node2.setParent(next_root)

    return (node1, node2, entry1, entry2)

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

  def rstarAdjustTree(tree, node, resulting_entries_from_split, have_resulting_second_entry_from_split):

    # return tree.rstarAdjustTreeHelper(tree, node.getParent(), resulting_entries_from_split, have_resulting_second_entry_from_split)

    return tree.rstarAdjustTreeHelper(tree, node, resulting_entries_from_split, have_resulting_second_entry_from_split)

  # node "node" is a parent that has entries that can lead to a split

  # mbr's for entries of parent node "node" can lead to entry in parent having its mbr resized

  # partner mbr from a split from before can lead to its entry in parent having its mbr resized

  @staticmethod

  def rstarAdjustTreeHelper(tree, node, resulting_entries_from_split, 
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

    if node == None:

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

      return (have_resulting_second_entry_from_split, resulting_entries_from_split)

      # return (have_resulting_second_entry_from_split, resulting_entries_from_split)

    else:

      # parent = node.getParent()

      parent = node

      curr_entries = node.getEntries()

      # print "parent:", parent

      # entry = parent.retrieveEntryForChild(node)

      entry = None

      if node.getParent() == None:

        entry = tree.getRootEntry()

      else:

        entry = node.getParent().retrieveEntryForChild(node)

      children = [x.getChild() for x in curr_entries]

      mbr_list = [x.getMBR() for x in curr_entries]

      tight_overall_mbr = CompositeMBR.makeMBR(mbr_list)

      entry.setMBR(tight_overall_mbr)

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

        partner_mbr_list = [x.getMBR() for x in partner_entries]

        partner_tight_overall_mbr = CompositeMBR.makeMBR(partner_mbr_list)

        partner_entry.setMBR(partner_tight_overall_mbr)

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

            return tree.rstarAdjustTreeHelper(tree, node.getParent(), [entry], False)

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

            split_result = tree.rstarSplitNode(parent, partner_entry)

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

            return tree.rstarAdjustTreeHelper(tree, l.getParent(), [e, ee], True)

            """

            if parent != None:

              return tree.rstarAdjustTree(tree, parent, [e, ee], True)

            else:

              return (True, [e, ee])

            """

        else:

          # return (False, [])

          # return tree.rstarAdjustTree(tree, parent, [entry], False)

          return tree.rstarAdjustTree(tree, node.getParent(), [entry], False)

      else:

        return tree.rstarAdjustTree(tree, node.getParent(), resulting_entries_from_split, 
have_resulting_second_entry_from_split)

  # adjustTree modifies parents so that their mbr's 
  # are enlarged and the nodes are possibly split 
  # with the two resulting pieces being added 
  # to parent's entry list

  # consider whether mbr's for a group have changed

  # returns an (ended_with_split, [resulting_first_entry_from_split, resulting_second_entry_from_split?]) tuple

  # ended_with_split tells us whether adjustTree ended by splitting a node that is root of a subtree

  """

  # also, when taken w.r.t. an operation that ends with root, ended_with_split is pre-emptive

  """

  # resulting_entries_from_split give us two entries that are to be children of current node

  # resulting_second_entry_from_split can be omitted

  @staticmethod

  def adjustTree(tree, node, resulting_entries_from_split, have_resulting_second_entry_from_split, is_first_call_after_first_pass):

    # if node == tree.getRootEntry().getChild():

    if node == None:

      # no parent to speak of

      # print "reach root case"

      return (False, [])

      # return (have_resulting_second_entry_from_split, resulting_entries_from_split)

    else:

      parent = node.getParent()

      curr_entries = node.getEntries()

      entry = None

      # print "parent:", parent

      if node.getParent() == None:

        entry = tree.getRootEntry()

      else:

        entry = parent.retrieveEntryForChild(node)

      children = [x.getChild() for x in curr_entries]

      mbr_list = [x.getMBR() for x in curr_entries]

      tight_overall_mbr = CompositeMBR.makeMBR(mbr_list)

      entry.setMBR(tight_overall_mbr)

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

      if have_resulting_second_entry_from_split == True and is_first_call_after_first_pass != True:

        partner_node = partner_entry.getChild()

        partner_entries = partner_node.getEntries()

        partner_children = [x.getChild() for x in partner_entries]

        partner_mbr_list = [x.getMBR() for x in partner_entries]

        partner_tight_overall_mbr = CompositeMBR.makeMBR(partner_mbr_list)

        partner_entry.setMBR(partner_tight_overall_mbr)

      # add E_NN to P if there is room

      # otherwise, invoke SplitNode to produce P and PP 
      # containing E_NN and all P's old entries

      # set N to P and set NN to PP if a split occurred, repeat from AT2

      if have_resulting_second_entry_from_split == True:

        parent.removeEntry(entry)

        """

        index = parent.getIndexForEntry(entry)

        parent.removeIthEntry(index)

        """

        # if parent.isFull() == False:

        if (parent.getNumChildren() + 2) <= parent.getMaximumNumEntriesPerNode():

          parent.addEntry(entry)

          parent.addEntry(partner_entry)

          entry.getChild().setParent(parent)

          partner_entry.getChild().setParent(parent)

          return tree.adjustTree(tree, parent, [entry], False, False)

        else:

          # ought to split

          parent.addEntry(entry)

          entry.getChild().setParent(parent)

          # following is a risky choice

          split_result = tree.splitNode(parent, partner_entry)

          l, ll, e, ee = split_result

          return tree.adjustTree(tree, l, [e, ee], True, False)

      else:

        return (False, [])

          # note that we do not have to update mbr for parent anymore 
          # given that a split changes how mbrs are organized, 
          # but the elements are not changed

          # don't care about parent overall mbr 
          # until we recursively call adjustTree on parent

    # update all MBRs in the path from the root to L, 
    # so that all of them cover E.mbr

    # update the MBRs of nodes that are in the path from root to L, so as to cover L1 and accommodate L2

    # perform splits at the upper levels if necessary

  # assume item is in tree

  # returns a node, which can be None if no match is found

  # finds one match if such a node exists

  # def delete(self, E, RN):

  def findLeaf(self, entry):

    return self.findLeafHelper(entry, self.getRootEntry().getChild())

  def findLeafHelper(self, entry, node):

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

  def delete(self, entry):

    node = self.findLeaf(entry, self.getRootEntry().getChild())

    if node == None:

      raise Exception("expected a node to be found for a delete")

    node.removeEntry(entry)

    self.condenseTree(node)

    root = self.getRootEntry().getChild()

    if root.getNumChildren() == 1:

      # shorten tree

      entries = root.getEntries()

      chosen_entry = entries[0]

      chosen_child = chosen_entry.getChild()

      self.getRootEntry().setChild(chosen_child)

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

  def condenseTree(self, node):

    elim_entries = []

    if node != self.getRootEntry().getChild():

      parent = node.getParent()

      entry = parent.retrieveEntryForChild(node)

      if node.isUnderfull() == True:

        parent.removeEntry(entry)

        elim_entries.append(entry)

        # for symmetric treatment

        if parent.getNumEntries() == 0:

          parent.setIsLeafNode(True)

      else:

        # adjust mbr for entry

        entries = node.getEntries()

        mbr_list = [x.getMBR() for x in entries]

        mbr = MBR.makeMBR(mbr_list)

        entry.setMBR(mbr)

      self.condenseTree(parent)

      for entry in elim_entries:

        self.insert(entry)

    # given is the leaf L from which an entry E has been deleted

    # if after the deletion of E, L has fewer than m entries, then remove entirely 
    # leaf L and reinsert all its entries; updates are propagated upwards and 
    # the MBRs in the path from root too L are modified (possibly become smaller)

    # set X = L

    # let N be the set of nodes that are going to be removed from the tree (initially, N is empty)

    # while X is not the root

      # let parent_X be the fther node of X

      # let E_X be the entry of parent_X that corresponds to X

      # if X contains less than m entries

        # remove EX from parent_X

        # insert X into N

      # if X has not been removed:

        # adjust its corresponding MBR E_X.mbr, so as to enclose 
        # all rectangles in X; note that E_X.mbr may become smaller

        # set X = parent_X

      # reinsert all the entries of nodes that are in the set N

    pass

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

    if node.isTraditionalLeafNode() == True and node.getNumEntries() == 0:

      curr_entry = entry

      # using a more fine-grained definition for leaf

      # parent, rather than current node, has entries

      # print node.getParent().retrieveEntryForChild(node).getMBR().toString()

      # for i in range(node.getNumEntries()):

      # curr_entry = node.getParent().retrieveEntryForChild(node)

      # curr_entry = node.getIthEntry(i)

      mbr = curr_entry.getMBR()

      # print mbr.toString()

      dist = getDistance(point, Point.toPoint(mbr))

      # print "distances:", dist, nearest.getDistance()

      if dist < nearest.getDistance():

        nearest.setDistance(dist)

        nearest.setCloseItem(curr_entry.getMBR().getContainedItem())

    else:

      branchList = RTree.genBranchList(point, entry)

      branchList = RTree.sortBranchList(point, branchList)

      # last = RTree.NNPruneBranchList(node, nearest, branchList, point)

      last = RTree.NNPruneBranchList(nearest, branchList, point)

      while len(last) != 0:

        # print last[0].getChild().isLeafNode(), last

        curr_entry = last.pop(0)

        curr_node = curr_entry.getChild()

        self.nearestNeighborSearchHelper(curr_entry, point, nearest)

        last = RTree.NNPruneBranchList(nearest, last, point)

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

      if node.isTraditionalLeafNode() == True and node.getNumEntries() == 0:

      # if first_node.isTraditionalLeafNode() == True and first_node.getNumEntries() == 0:

        # print "encountering a raw rectangle"

        # encountering a raw rectangle

        # print node.getChildren()

        curr_entry = entry

        # curr_entry = node.getParent().retrieveEntryForChild(node)

        mbr = curr_entry.getMBR()

        dist = getDistance(point, Point.toPoint(mbr))

        # print self.toString()

        # print dist, Point.toPoint(mbr)

        if dist <= kNearest.getFarthestCloseDistance() + 0.001 or kNearest.isFull() == False:

          close_item = curr_entry.getMBR().getContainedItem()

          kNearest.addAndRemoveIfNecessary(close_item)

      else:

        branchList = RTree.genBranchList(point, entry)

        # print len(branchList)

        branchList = RTree.sortBranchList(point, branchList)

        last = branchList

        # print [x.getMBR().toString() for x in branchList]

        # last = RTree.kNNPruneBranchList(node, kNearest, branchList, point)

        while len(last) != 0:

          # last = RTree.kNNPruneBranchList(node, kNearest, last, point)

          last = RTree.kNNPruneBranchList(kNearest, last, point)

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

    entries.sort(key = lambda x: RTree.twoDimensionalMinDist(query_point, x.getMBR()))

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

    min_dist_values = [RTree.twoDimensionalMinDist(point, x.getMBR()) for x in entries]

    min_max_dist_values = [RTree.twoDimensionalMinMaxDist(point, x.getMBR()) for x in entries]

    min_min_max_dist_value = min(min_max_dist_values)

    # print min_dist_values

    # print min_max_dist_values

    # tagged_actual_dist_values = None

    nearest_dist = nearest.getDistance()

    entries_to_keep = []

    for entry in entries:

      min_dist_value = RTree.twoDimensionalMinDist(point, entry.getMBR())

      # min_max_dist_value = RTree.twoDimensionalMinMaxDist(point, entry.getMBR())

      do_prune = False

      # print min_dist_value, min_min_max_dist_value

      # print nearest_dist

      if min_dist_value > min_min_max_dist_value:

        do_prune = True

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

      min_dist_value = RTree.twoDimensionalMinDist(point, entry.getMBR())

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

    # image = PythonMagick.Image(PythonMagick.Geometry("768x768"), "white")

    image = PythonMagick.Image(PythonMagick.Geometry("1536x1536"), "white")

    root_entry = self.getRootEntry()

    entries = [root_entry]

    RTreeEntry.draw(self, entries, image, 0)

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

"""

point1 = (100, 100)

point2 = (50, 100)

point3 = (60, 100)

point4 = (70, 100)

point5 = (80, 100)

point6 = (90, 100)

point7 = (110, 100)

point8 = (120, 100)

mbr1 = RawMBR((100, 100), (100, 100), point1)

mbr2 = RawMBR((50, 100), (50, 100), point2)

mbr3 = CompositeMBR((50, 100), (100, 100), [mbr1, mbr2])

entry1 = RTreeEntry(mbr1, None)

entry2 = RTreeEntry(mbr2, None)

entry3 = RTreeEntry(mbr3, None)

node1 = RTreeNode(None, [entry3], False)

node2 = RTreeNode(None, [entry1, entry2], True)

entry3.setChild(node2)

node2.setParent(node1)

tree = RTree()

print tree.toString()

curr_root = tree.getRoot()

# entry1.setChild(RTreeNode(tree.getRoot(), [entry1]))

# insert always adds a leaf

tree.insert(RTreeEntry(RawMBR((100, 100), (100, 100), point1), RTreeNode(None, [], True)))

tree.insert(RTreeEntry(RawMBR((50, 100), (50, 100), point2), RTreeNode(None, [], True)))

tree.insert(RTreeEntry(RawMBR((60, 100), (60, 100), point3), RTreeNode(None, [], True)))

tree.insert(RTreeEntry(RawMBR((70, 100), (70, 100), point4), RTreeNode(None, [], True)))

print tree.getRoot()

tree.insert(RTreeEntry(RawMBR((80, 100), (80, 100), point5), RTreeNode(None, [], True)))

tree.insert(RTreeEntry(RawMBR((90, 100), (90, 100), point6), RTreeNode(tree.getRoot(), [], True)))

print tree.toString()

tree.insert(RTreeEntry(RawMBR((110, 100), (110, 100), point7), RTreeNode(tree.getRoot(), [], True)))

tree.insert(RTreeEntry(RawMBR((120, 100), (120, 100), point8), RTreeNode(tree.getRoot(), [], True)))

print tree.toString()

nearest_result = NearestNeighbor()

tree.nearestNeighborSearch(tree.getRoot(), (50, 0), nearest_result)

print nearest_result.toString()

k_nearest_result = KNearestNeighbor((50, 0), PriorityQueue(), 2)

tree.kNearestNeighborSearch(tree.getRoot(), (50, 0), k_nearest_result, 2)

print k_nearest_result.toString()

"""

import sys

import string

x = 0

y = 0

location = (x, y)

tree = RTree()

id_value = 1

# example insert

point = Point(location[0], location[1], id_value)

tree.insert(RTreeEntry(RawMBR(location, location, point), RTreeNode(None, [], True)))

# retrieve a string representation of tree

print tree.toString()

# example nn query

nearest_result = NearestNeighbor()

tree.nearestNeighborSearch(location, nearest_result)

close_item = nearest_result.getCloseItem()

distance = nearest_result.getDistance()

found_location = (close_item.getX(), close_item.getY())

print found_location, distance

# example k-nn query

k = 10

k_nearest_result = KNearestNeighbor(location, PriorityQueue(), k)

tree.kNearestNeighborSearch(location, k_nearest_result, k)

close_items = k_nearest_result.getCloseItems()

farthest_close_distance = k_nearest_result.getFarthestCloseDistance()

found_locations = [(x.getX(), x.getY()) for x in close_items]

print found_locations, farthest_close_distance


