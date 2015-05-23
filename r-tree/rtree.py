# r-tree featuring insert, nn and k-nn search with threshold distance

# tie-breaking for same distance is identifier value with largest values appearing earlier

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

    self.entries = entries

    self.is_leaf = is_leaf

    self.m = 1

    self.M = 4

  def getParent(self):

    return self.parent

  def getEntries(self):

    return self.entries

  def getChildren(self):

    entries = self.getEntries()

    children = [x.getChild() for x in entries]

    return children

  def getNumEntries(self):

    return len(self.getEntries())

  def getNumChildren(self):

    return len(self.getChildren())

  def setParent(self, node):

    self.parent = node

  def isLeafNode(self):

    # return self.getNumChildren() == 0

    return self.is_leaf

  def setIsLeafNode(self, is_leaf):

    self.is_leaf = is_leaf

  def addEntry(self, entry):

    # print "adding an entry:", entry.getMBR().toString()

    (self.entries).append(entry)

  # entry must match exactly

  def removeEntry(self, entry):

    index = (self.entries).index(entry)

    (self.entries).pop(index)

  def getMinimumNumEntriesPerNode(self):

    return self.m

  def getMaximumNumEntriesPerNode(self):

    return self.M

  def isFull(self):

    return self.getNumEntries() >= self.getMaximumNumEntriesPerNode()

  def isUnderfull(self):

    return self.getNumEntries() < self.getMinimumNumEntriesPerNode()

  # indexing starts at zero

  def getIndexForEntry(self, entry):

    index = (self.entries).index(entry)

    return index

  def removeIthEntry(self, i):

    (self.entries).pop(i)

  def retrieveEntryForChild(self, node):

    entries = self.getEntries()

    children = [x.getChild() for x in entries]

    # print "children:", [x.toString() for x in children]

    # print "child:", node.toString()

    # print "mbr's:", [x.getMBR().toString() for x in entries]

    index = children.index(node)

    chosen_entry = entries[index]

    return chosen_entry

  # indexing starts at zero

  def getIthEntry(self, i):

    return (self.entries)[i]

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

    x1_a, y1_a = upper_left_a

    x2_a, y2_a = lower_right_a

    x1_b, y1_b = upper_left_b

    x2_b, y2_b = lower_right_b

    do_overlap = x1_a < x2_b and x2_a > x1_b and y1_a < y2_b and y2_a > y1_b

    return do_overlap

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

    root = RTreeNode(None, [], True)

    self.setRoot(root)

  # return an in-order string

  def toString(self):

    root = self.getRoot()

    return self.toStringHelper(root)

  def toStringHelper(self, node):

    if node == None:

      return ""

    entries = node.getEntries()

    # print "node:", node

    # print "entries:", entries

    children = node.getChildren()

    have_node_str = True

    if node == self.getRoot():

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

  def setRoot(self, node):

    self.root = node

  def getRoot(self):

    return self.root
 
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

    min_area = min(area_values)

    candidate_tagged_area_values = [x for x in tagged_area_values if x[0] == min_area]

    candidate_entries = [x[1] for x in candidate_tagged_area_values]

    return candidate_entries

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

    return self.chooseLeafHelper(entry, self.getRoot())

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

  def insert(self, entry):

    """

    encountered_item = False

    # if entry.getMBR().getContainedItem() == (962736.900780, 317162.3926449):

    if entry.getMBR().getContainedItem()[0] == 835394.40839:

      encountered_item = True

    if encountered_item == True:

      print self.toString()

      raise Exception()

    """

    leaf_node = self.chooseLeaf(entry)

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

      # call adjustTree to resize bounding boxes of ancestors and propagate splits

      adjust_result = RTree.adjustTree(self, leaf_node, [entry], False, True)

    else:

      # split node

      split_result = self.splitNode(leaf_node, entry)

      # l and ll are internal nodes

      l, ll, e, ee = split_result

      # print leaf_node == self.getRoot()

      # print leaf_node.getParent().getEntries(), e, ee

      if leaf_node != self.getRoot() and leaf_node.getParent() != None:

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

      # e and ee are for entries for the two children that result from split of l

      adjust_result = RTree.adjustTree(self, l, [e], False, True)

      # check result of tree-adjust to see whether we plan on splitting root

      # in case the root has to be split, create a new root

      # increase the height of the tree by one

      # grow tree taller

    ended_with_split2, resulting_entries_from_split = adjust_result

    # print "ended with split:", ended_with_split2

    # we ended adjust-tree by requiring a split of root

    """

    if ended_with_split2 == True:

      # print "resulting entries:", resulting_entries_from_split

      next_root = RTreeNode(None, resulting_entries_from_split, False)

      next_root.addEntry(e)

      next_root.addEntry(ee)

      l.setParent(next_root)

      ll.setParent(next_root)

      # print "have a next root:", next_root

      self.setRoot(next_root) 

    else:

      # print "entries included:", e in l.getParent().getEntries()

      pass

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

    result = RTree.linearPickSeeds(E_overall)

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

    curr_overall_mbr1 = CompositeMBR(seed_entry1.getMBR().getUpperLeft(), seed_entry1.getMBR().getLowerRight(), [seed_entry1])

    curr_overall_mbr2 = CompositeMBR(seed_entry2.getMBR().getUpperLeft(), seed_entry2.getMBR().getLowerRight(), [seed_entry2])

    for i in range(len(remaining_entries)):

      curr_entry = remaining_entries[i]

      next_curr_node = curr_entry.getChild()

      # print curr_entry.getMBR().toString()

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

    if node != self.getRoot():

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

      self.setRoot(next_root)

      # this causes problems

      # entry.getChild().setParent(next_root)

      node1.setParent(next_root)

      node2.setParent(next_root)

    return (node1, node2, entry1, entry2)

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

    if node == tree.getRoot():

      # no parent to speak of

      # print "reach root case"

      return (False, [])

      # return (have_resulting_second_entry_from_split, resulting_entries_from_split)

    else:

      parent = node.getParent()

      curr_entries = node.getEntries()

      # print "parent:", parent

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

        index = parent.getIndexForEntry(entry)

        parent.removeIthEntry(index)

        if parent.isFull() == False:

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

    return self.findLeafHelper(entry, self.getRoot())

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

  """

  def delete(self, entry):

    node = self.findLeaf(entry, self.getRoot())

    if node == None:

      raise Exception("expected a node to be found for a delete")

    node.removeEntry(entry)

    self.condenseTree(node)

    root = self.getRoot()

    if root.getNumChildren() == 1:

      # shorten tree

      entries = root.getEntries()

      chosen_entry = entries[0]

      chosen_child = chosen_entry.getChild()

      self.setRoot(chosen_child)

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

  """

  """

  def condenseTree(self, node):

    elim_entries = []

    if node != self.getRoot():

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

  """

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

  def nearestNeighborSearch(self, node, point, nearest):

    # print self.toString()

    """

    if node.isLeafNode() == True and node == self.getRoot():

      # no entries to speak of

      return

    """

    # if node.getNumEntries() == 0 and node != self.getRoot():

    if node.isLeafNode() == True and node != self.getRoot():

      # using a more fine-grained definition for leaf

      # parent, rather than current node, has entries

      # print node.getParent().retrieveEntryForChild(node).getMBR().toString()

      # for i in range(node.getNumEntries()):

      curr_entry = node.getParent().retrieveEntryForChild(node)

      # curr_entry = node.getIthEntry(i)

      mbr = curr_entry.getMBR()

      # print mbr.toString()

      dist = getDistance(point, Point.toPoint(mbr))

      # print "distances:", dist, nearest.getDistance()

      if dist < nearest.getDistance():

        nearest.setDistance(dist)

        nearest.setCloseItem(curr_entry.getMBR().getContainedItem())

    else:

      branchList = RTree.genBranchList(point, node)

      branchList = RTree.sortBranchList(point, branchList)

      last = RTree.NNPruneBranchList(node, nearest, branchList, point)

      while len(last) != 0:

        # print last[0].getChild().isLeafNode(), last

        curr_entry = last.pop(0)

        curr_node = curr_entry.getChild()

        self.nearestNeighborSearch(curr_node, point, nearest)

        last = RTree.NNPruneBranchList(node, nearest, last, point)

  def kNearestNeighborSearch(self, node, point, kNearest, k):

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

    if node.isLeafNode() == True and node != self.getRoot() and node.getNumEntries() == 0:

      # print node.getChildren()

      curr_entry = node.getParent().retrieveEntryForChild(node)

      mbr = curr_entry.getMBR()

      dist = getDistance(point, Point.toPoint(mbr))

      # print self.toString()

      # print dist, Point.toPoint(mbr)

      if dist <= kNearest.getFarthestCloseDistance() + 0.001 or kNearest.isFull() == False:

        close_item = curr_entry.getMBR().getContainedItem()

        kNearest.addAndRemoveIfNecessary(close_item)

    else:

      branchList = RTree.genBranchList(point, node)

      branchList = RTree.sortBranchList(point, branchList)

      # print [x.getMBR().toString() for x in branchList]

      last = RTree.kNNPruneBranchList(node, kNearest, branchList, point)

      while len(last) != 0:

        curr_entry = last.pop(0)

        curr_node = curr_entry.getChild()

        self.kNearestNeighborSearch(curr_node, point, kNearest, k)

        last = RTree.kNNPruneBranchList(node, kNearest, last, point)

  @staticmethod

  def genBranchList(query_point, node):

    # come up with a list of entries

    entries = (node.getEntries())[ : ]

    return entries

  @staticmethod

  def sortBranchList(query_point, branchList):

    # sort the entries to be in order of mindist metric ascending

    entries = branchList

    entries.sort(key = lambda x: RTree.twoDimensionalMinDist(query_point, x.getMBR()))

    return entries

  @staticmethod

  def NNPruneBranchList(node, nearest, branchList, point):

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

      min_max_dist_value = RTree.twoDimensionalMinMaxDist(point, entry.getMBR())

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

  def kNNPruneBranchList(node, kNearest, branchList, point):

    if len(branchList) == 0:

      return []

    # prune based on mindist and minmaxdist metrics and closest k items seen so far

    entries = branchList

    min_dist_values = [RTree.twoDimensionalMinDist(point, x.getMBR()) for x in entries]

    min_max_dist_values = [RTree.twoDimensionalMinMaxDist(point, x.getMBR()) for x in entries]

    min_min_max_dist_value = min(min_max_dist_values)

    # tagged_actual_dist_values = None

    farthest_close_dist = kNearest.getFarthestCloseDistance()

    entries_to_keep = []

    for entry in entries:

      min_dist_value = RTree.twoDimensionalMinDist(point, entry.getMBR())

      min_max_dist_value = RTree.twoDimensionalMinMaxDist(point, entry.getMBR())

      do_prune = False

      if min_dist_value > min_min_max_dist_value + 0.001 and kNearest.isFull() == True:

        # do_prune = True

        pass

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

tree.nearestNeighborSearch(tree.getRoot(), location, nearest_result)

close_item = nearest_result.getCloseItem()

distance = nearest_result.getDistance()

found_location = (close_item.getX(), close_item.getY())

print found_location, distance

# example k-nn query

k = 10

k_nearest_result = KNearestNeighbor(location, PriorityQueue(), k)

tree.kNearestNeighborSearch(tree.getRoot(), location, k_nearest_result, k)

close_items = k_nearest_result.getCloseItems()

farthest_close_distance = k_nearest_result.getFarthestCloseDistance()

found_locations = [(x.getX(), x.getY()) for x in close_items]

print found_locations, farthest_close_distance
