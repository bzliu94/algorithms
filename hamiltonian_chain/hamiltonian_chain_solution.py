# 2015-12-14

# solves hamiltonian chain enumeration problem

# usage: python hamiltonian_chain_solution.py W H
# where W is grid width and H is grid height

# takes O(2 ^ L * L ^ 2) time

# involves memoizing using a surface key

# inspired by anand krishnamoorthi

# algorithm comes from a paper by j. l. jacobsen

import math
from collections import defaultdict
import random
class Grid:
  def __init__(self, W, H):
    self.W = W
    self.H = H
  def getWidth(self):
    return self.W
  def getHeight(self):
    return self.H
def idToLocation(id_value, eff_W, eff_H):
  t = id_value
  row = getRow(t, eff_W, eff_H)
  col = getCol(t, eff_W, eff_H)
  location = (row, col)
  return location
def getRow(t, W, H):
  result = int(math.floor(t / W))
  return result
def getCol(t, W, H):
  return t % W
def getTime(row, col, W, H):
  t = row * W + col
  return t
def getPriorRowAndColumn(row, col, W, H):
  t = getTime(row, col, W, H)
  next_t = t - 1
  next_row = getRow(next_t, W, H)
  next_col = getCol(next_t, W, H)
  if next_t == -1:
    return None
  else:
    return (next_row, next_col)
def getNextRowAndColumn(row, col, W, H):
  t = getTime(row, col, W, H)
  next_t = t + 1
  next_row = getRow(next_t, W, H)
  next_col = getCol(next_t, W, H)
  return (next_row, next_col)
class FullGrid(Grid):
  def __init__(self, W, H):
    Grid.__init__(self, W, H)
    vertex_rows = []
    for i in xrange(H + 1):
      vertex_row = []
      for j in xrange(W + 1):
        vertex = None
        vertex_row.append(vertex)
      vertex_rows.append(vertex_row)
    self.vertex_rows = vertex_rows
    self.id_to_vertex_dict = {}
    self.location_to_incident_path_far_node_id = defaultdict(lambda: [])
    self.num_completed_chains = 0
  def addVertex(self, id_value, row1, col1, path_end_id_value, base_num_connections, non_base_num_connections, is_sentinel):
    vertex = Vertex(id_value, row1, col1, [path_end_id_value], base_num_connections, non_base_num_connections, is_sentinel)
    (self.vertex_rows)[row1][col1] = vertex
    (self.id_to_vertex_dict)[id_value] = vertex
    location1 = (row1, col1)
    location2 = idToLocation(path_end_id_value, self.getWidth() + 1, self.getHeight() + 1)
    (self.location_to_incident_path_far_node_id)[location1].append(path_end_id_value)
    (self.location_to_incident_path_far_node_id)[location2].append(id_value)
    return vertex
  def getVertex(self, row, col):
    return (self.vertex_rows)[row][col]
  def getVertexUsingIDValue(self, id_value):
    return (self.id_to_vertex_dict)[id_value]
  def getVertexRow(self, row):
    return (self.vertex_rows)[row]
  def getPathEndNode(self, row, col):
    vertex = self.getVertex(row, col)
    path_end_id_value = vertex.getPathEndIDValue()
    path_end_node = self.getVertexUsingIDValue(path_end_id_value)
    return path_end_node
  def setPathEnd(self, row1, col1, row2, col2):
    vertex1 = self.getVertex(row1, col1)
    vertex2 = self.getVertex(row2, col2)
    id_value1 = vertex1.getIDValue()
    id_value2 = vertex2.getIDValue()
    old_partner_id = vertex1.getPathEndIDValue()
    old_partner_location = idToLocation(old_partner_id, self.getWidth() + 1, self.getHeight() + 1)
    path_end_id_value = vertex2.getIDValue()
    vertex1.setPathEndIDValue(path_end_id_value)
    location1 = (row1, col1)
    location2 = (row2, col2)
    (self.location_to_incident_path_far_node_id)[old_partner_location].remove(id_value1)
    (self.location_to_incident_path_far_node_id)[location1].remove(old_partner_id)
    (self.location_to_incident_path_far_node_id)[location2].append(id_value1)
    (self.location_to_incident_path_far_node_id)[location1].append(id_value2)
  def setNumConnections(self, row, col, val):
    vertex = self.getVertex(row, col)
    vertex.setNumConnections(val)
  def getNumConnections(self, row, col):
    vertex = self.getVertex(row, col)
    result = vertex.getNumConnections()
    return result
  @staticmethod
  def formKey(grid):
    vertex_rows = grid.vertex_rows
    W = grid.getWidth()
    H = grid.getHeight()
    vertices = []
    for vertex_row in vertex_rows:
      vertices += vertex_row
    vertex_keys = [Vertex.formKey(x) for x in vertices]
    keys = [W, H] + vertex_keys
    result = tuple(keys)
    return result
  @staticmethod
  def formFromKey(key):
    W = key[0]
    H = key[1]
    vertex_keys = key[2 : ]
    grid = FullGrid(W, H)
    for vertex_key in vertex_keys:
      vertex = Vertex.formFromKey(vertex_key)
      id_value = vertex.getIDValue()
      row1 = vertex.getRow()
      col1 = vertex.getCol()
      path_end_id_value = vertex.getPathEndIDValue()
      base_num_connections = vertex.getBaseNumConnections()
      non_base_num_connections = vertex.getNonBaseNumConnections()
      is_sentinel = vertex.getIsSentinel()
      grid.addVertex(id_value, row1, col1, path_end_id_value, base_num_connections, non_base_num_connections, is_sentinel)
    return grid
class Surface(Grid):
  def __init__(self, W, H, curr_row_index):
    Grid.__init__(self, W, H)
    self.curr_row_index = curr_row_index
    vertex_rows = defaultdict(lambda: defaultdict(lambda: None))
    self.vertex_rows = vertex_rows
    self.id_to_vertex_dict = {}
    self.location_to_horizontal_cut_edge_path_key_list_dict = defaultdict(lambda: [])
    self.location_to_vertical_cut_edge_path_key_list_dict = defaultdict(lambda: [])
    self.num_completed_chains = 0
  def getNumCompletedChains(self):
    return self.num_completed_chains
  def setNumCompletedChains(self, val):
    self.num_completed_chains = val
  def getHorizontalCutEdgeExists(self, location):
    matching_path_keys = self.getHorizontalCutEdgePathKeys(location)
    num_matching_path_keys = len(matching_path_keys)
    return num_matching_path_keys > 0
  def getVerticalCutEdgeExists(self, location):
    matching_path_keys = self.getVerticalCutEdgePathKeys(location)
    num_matching_path_keys = len(matching_path_keys)
    return num_matching_path_keys > 0
  def getHorizontalCutEdgePathKeys(self, location):
    matching_path_keys = (self.location_to_horizontal_cut_edge_path_key_list_dict)[location]
    return matching_path_keys[ : ]
  def getVerticalCutEdgePathKeys(self, location):
    matching_path_keys = (self.location_to_vertical_cut_edge_path_key_list_dict)[location]
    return matching_path_keys[ : ]
  def _addHorizontalCutEdgePathKey(self, location1, location2):
    path_key = Surface.getPathKey(location1, location2)
    (self.location_to_horizontal_cut_edge_path_key_list_dict)[location2].append(path_key)
  def _addVerticalCutEdgePathKey(self, location1, location2):
    path_key = Surface.getPathKey(location1, location2)
    (self.location_to_vertical_cut_edge_path_key_list_dict)[location2].append(path_key)
  def _removeHorizontalCutEdgePathKey(self, location1, location2):
    path_key = Surface.getPathKey(location1, location2)
    (self.location_to_horizontal_cut_edge_path_key_list_dict)[location2].remove(path_key)
  def _removeVerticalCutEdgePathKey(self, location1, location2):
    path_key = Surface.getPathKey(location1, location2)
    (self.location_to_vertical_cut_edge_path_key_list_dict)[location2].remove(path_key)
  def _idempotentRemoveCutEdgePathKey(self, location1, location2):
    path_key = Surface.getPathKey(location1, location2)
    if path_key in self.getHorizontalCutEdgePathKeys(location2):
      self._removeHorizontalCutEdgePathKey(location1, location2)
      return True
    elif path_key in self.getVerticalCutEdgePathKeys(location2):
      self._removeVerticalCutEdgePathKey(location1, location2)
      return False
    else:
      return None
  def addVertex(self, id_value, row1, col1, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel):
    vertex = Vertex(id_value, row1, col1, path_end_id_values[ : ], base_num_connections, non_base_num_connections, is_sentinel)
    (self.vertex_rows)[row1][col1] = vertex
    (self.id_to_vertex_dict)[id_value] = vertex
    return vertex
  def getVertex(self, row, col):
    return (self.vertex_rows)[row][col]
  def getVertexUsingIDValue(self, id_value):
    return (self.id_to_vertex_dict)[id_value]
  def getPathEndNodes(self, row, col):
    vertex = self.getVertex(row, col)
    path_end_id_values = vertex.getPathEndIDValues()
    path_end_nodes = [self.getVertexUsingIDValue(x) for x in path_end_id_values]
    return path_end_nodes
  @staticmethod
  def getPathKey(location1, location2):
    if location1 <= location2:
      return (location1, location2)
    elif location1 > location2:
      return (location2, location1)
  def setPathEnd(self, row1, col1, row2, col2, do_override_non_trivial):
    vertex1 = self.getVertex(row1, col1)
    vertex2 = self.getVertex(row2, col2)
    id_value1 = vertex1.getIDValue()
    id_value2 = vertex2.getIDValue()
    path_end_id_value = vertex1.getIDValue()
    if do_override_non_trivial == True:
      vertex2.setPathEndIDValues([path_end_id_value])
    else:
      vertex2.addPathEndIDValue(path_end_id_value)
    location1 = (row1, col1)
    location2 = (row2, col2)
  def idempotentRemovePathEnd(self, row1, col1, id_value):
    vertex1 = self.getVertex(row1, col1)
    id_value1 = vertex1.getIDValue()
    path_end_id_values = vertex1.getPathEndIDValues()
    next_path_end_id_values = path_end_id_values[ : ]
    if id_value in next_path_end_id_values:
      next_path_end_id_values.remove(id_value)
    vertex1.setPathEndIDValues(next_path_end_id_values)
  def setNumConnections(self, row, col, val):
    vertex = self.getVertex(row, col)
    vertex.setNumConnections(val)
  def getNumConnections(self, row, col):
    vertex = self.getVertex(row, col)
    result = vertex.getNumConnections()
    return result
  def getCurrRowIndex(self):
    return self.curr_row_index
  def setCurrRowIndex(self, curr_row_index):
    self.curr_row_index = curr_row_index
  def _getLocationToHorizontalCutEdgePathKeyListDict(self):
    return self.location_to_horizontal_cut_edge_path_key_list_dict
  def _getLocationToVerticalCutEdgePathKeyListDict(self):
    return self.location_to_horizontal_cut_edge_path_key_list_dict
  @staticmethod
  def formKeyOriginal(grid):
    vertex_rows = grid.vertex_rows
    W = grid.getWidth()
    H = grid.getHeight()
    curr_row_index = grid.getCurrRowIndex()
    k = grid.getNumCompletedChains()
    lthcepkld = grid._getLocationToHorizontalCutEdgePathKeyListDict()
    ltvcepkld = grid._getLocationToVerticalCutEdgePathKeyListDict()
    lthcepkld_components = []
    ltvcepkld_components = []
    for item in lthcepkld.items():
      location, path_key_list = item
      next_items = [(location, x) for x in path_key_list]
      lthcepkld_components += next_items
    lthcepkld_components.sort()
    for item in ltvcepkld.items():
      location, path_key_list = item
      next_items = [(location, x) for x in path_key_list]
      ltvcepkld_components += next_items
    ltvcepkld_components.sort()
    next_lthcepkld_components = tuple(lthcepkld_components)
    next_ltvcepkld_components = tuple(ltvcepkld_components)
    vertices = []
    for vertex_row in vertex_rows.values():
      vertices += vertex_row.values()
    vertex_keys = [Vertex.formKey(x) for x in vertices]
    keys = [W, H, curr_row_index, next_lthcepkld_components, next_ltvcepkld_components, k] + vertex_keys
    result = tuple(keys)
    return result
  @staticmethod
  def formKey(grid, row, col):
    return Surface.formKeyNextPreMerge(grid, row, col)
  @staticmethod
  def formKeyNextPreMerge(grid, row, col):
    W = grid.getWidth()
    H = grid.getHeight()
    k = grid.getNumCompletedChains()
    num_vertical_components = W + 1
    vertical_components = []
    horizontal_component = None
    id_value = 1
    path_key_to_id_dict = {}
    for curr_col in xrange(num_vertical_components):
      far_vertex_location = None
      if curr_col <= col:
        far_vertex_location = (row + 1, curr_col)
      else:
        far_vertex_location = (row, curr_col)
      curr_id_value = None
      if grid.getVerticalCutEdgeExists(far_vertex_location) == True:
        path_keys = grid.getVerticalCutEdgePathKeys(far_vertex_location)
        path_key = path_keys[0]
        if path_key in path_key_to_id_dict:
          curr_id_value = path_key_to_id_dict[path_key]
        else:
          curr_id_value = id_value
          path_key_to_id_dict[path_key] = curr_id_value
          id_value += 1
      else:
        curr_id_value = 0
      vertical_components.append(curr_id_value)
    far_vertex_location = (row, col + 1)
    curr_id_value = None
    if grid.getHorizontalCutEdgeExists(far_vertex_location) == True:
      path_keys = grid.getHorizontalCutEdgePathKeys(far_vertex_location)
      path_key = path_keys[0]
      if path_key in path_key_to_id_dict:
        curr_id_value = path_key_to_id_dict[path_key]
      else:
        curr_id_value = id_value
        path_key_to_id_dict[path_key] = curr_id_value
        id_value += 1
    else:
      curr_id_value = 0
    horizontal_component = curr_id_value
    components = vertical_components + [horizontal_component, k]
    key = tuple(components)
    return key
  @staticmethod
  def formKeyNextPostMerge(grid, row, col):
    W = grid.getWidth()
    H = grid.getHeight()
    k = grid.getNumCompletedChains()
    num_vertical_components = W + 1
    vertical_components = []
    horizontal_component = None
    id_value = 1
    path_key_to_id_dict = {}
    for curr_col in xrange(num_vertical_components):
      far_vertex_location = None
      if curr_col <= col:
        far_vertex_location = (row + 1, curr_col)
      else:
        far_vertex_location = (row, curr_col)
      curr_id_value = None
      if grid.getVerticalCutEdgeExists(far_vertex_location) == True:
        path_keys = grid.getVerticalCutEdgePathKeys(far_vertex_location)
        path_key = path_keys[0]
        if path_key in path_key_to_id_dict:
          curr_id_value = path_key_to_id_dict[path_key]
        else:
          curr_id_value = id_value
          path_key_to_id_dict[path_key] = curr_id_value
          id_value += 1
      else:
        curr_id_value = 0
      vertical_components.append(curr_id_value)
    far_vertex_location = (row, col + 1)
    curr_id_value = None
    if grid.getHorizontalCutEdgeExists(far_vertex_location) == True:
      path_keys = grid.getHorizontalCutEdgePathKeys(far_vertex_location)
      path_key = path_keys[0]
      if path_key in path_key_to_id_dict:
        curr_id_value = path_key_to_id_dict[path_key]
      else:
        curr_id_value = id_value
        path_key_to_id_dict[path_key] = curr_id_value
        id_value += 1
    else:
      curr_id_value = 0
    horizontal_component = curr_id_value
    components = vertical_components + [horizontal_component, k]
    key = tuple(components)
    return key
  @staticmethod
  def formFromKeyOld(key):
    W = key[0]
    H = key[1]
    curr_row_index = key[2]
    next_lthcepkld_components = list(key[3])
    next_ltvcepkld_components = list(key[4])
    k = list(key[5])
    vertex_keys = key[6 : ]
    grid = Surface(W, H, curr_row_index)
    grid.setNumCompletedChains(k)
    for item in next_lthcepkld_components:
      location, path_key = item
      l1, l2 = path_key
      location1 = location
      location2 = l1 if l2 == location else l2
      grid._addHorizontalCutEdgePathKey(location1, location2)
    for item in next_ltvcepkld_components:
      location, path_key = item
      l1, l2 = path_key
      location1 = location
      location2 = l1 if l2 == location else l2
      grid._addVerticalCutEdgePathKey(location1, location2)
    for vertex_key in vertex_keys:
      vertex = Vertex.formFromKey(vertex_key)
      id_value = vertex.getIDValue()
      row1 = vertex.getRow()
      col1 = vertex.getCol()
      path_end_id_values = vertex.getPathEndIDValues()
      base_num_connections = vertex.getBaseNumConnections()
      non_base_num_connections = vertex.getNonBaseNumConnections()
      is_sentinel = vertex.getIsSentinel()
      grid.addVertex(id_value, row1, col1, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel)
    return grid
  def getVertices(self):
    vertex_rows = self.vertex_rows
    H = self.getHeight()
    curr_row_index = self.getCurrRowIndex()
    vertices = []
    for i in xrange(max(curr_row_index - 1, 0), curr_row_index + 2):
      vertex_row = vertex_rows[i]
      next_vertex_row = vertex_row.values()
      vertices += next_vertex_row
    next_vertices = set(vertices)
    for vertex in vertices:
      location = vertex.getLocation()
      row, col = location
      path_ends = self.getPathEndNodes(row, col)
      next_vertices |= set(path_ends)
    next_next_vertices = list(next_vertices)
    return next_next_vertices
  def clone(self):
    W = self.getWidth()
    H = self.getHeight()
    curr_row_index = self.getCurrRowIndex()
    k = self.getNumCompletedChains()
    surface = Surface(W, H, curr_row_index)
    surface.setNumCompletedChains(k)
    lthcepkld = defaultdict(lambda: [])
    for item in self.location_to_horizontal_cut_edge_path_key_list_dict.items():
      location, path_key_list = item
      if len(path_key_list) != 0:
        lthcepkld[location] = path_key_list[ : ]
    ltvcepkld = defaultdict(lambda: [])
    for item in self.location_to_vertical_cut_edge_path_key_list_dict.items():
      location, path_key_list = item
      if len(path_key_list) != 0:
        ltvcepkld[location] = path_key_list[ : ]
    surface.location_to_horizontal_cut_edge_path_key_list_dict = lthcepkld
    surface.location_to_vertical_cut_edge_path_key_list_dict = ltvcepkld
    vertices = self.getVertices()
    for vertex in vertices:
      id_value = vertex.getIDValue()
      path_end_id_values = vertex.getPathEndIDValues()
      base_num_connections = vertex.getBaseNumConnections()
      non_base_num_connections = vertex.getNonBaseNumConnections()
      location = vertex.getLocation()
      is_sentinel = vertex.getIsSentinel()
      row, col = location
      surface.addVertex(id_value, row, col, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel)
    return surface
  def _advanceOneRow(self, reference_full_grid):
    curr_row_index = self.getCurrRowIndex()
    next_row_index = curr_row_index + 1
    prev_row_index = curr_row_index - 1
    self.setCurrRowIndex(curr_row_index + 1)
    have_prev_row = (curr_row_index - 1) >= 0
    next_next_row = reference_full_grid.getVertexRow(curr_row_index + 2)
    next_next_row_safe = [x.clone() for x in next_next_row]
    safe_vertices = self.getVertices() + next_next_row_safe
    safe_vertices_set = set(safe_vertices)
    lthcepkld = self.location_to_horizontal_cut_edge_path_key_list_dict
    ltvcepkld = self.location_to_vertical_cut_edge_path_key_list_dict
    if have_prev_row == True:
      vertices = (self.vertex_rows)[prev_row_index].values()
      for i in xrange(len(vertices)):
        vertex = vertices[i]
        id_value = vertex.getIDValue()
        location = vertex.getLocation()
        if vertex not in safe_vertices_set:
          (self.vertex_rows)[prev_row_index].pop(i)
          (self.id_to_vertex_dict).pop(id_value)
          if location in lthcepkld:
            lthcepkld.pop(location)
          if location in ltvcepkld:
            ltvcepkld.pop(location)
      if len((self.vertex_rows)[prev_row_index]) == 0:
        (self.vertex_rows).pop(prev_row_index)
    for vertex in next_next_row_safe:
      id_value = vertex.getIDValue()
      path_end_id_values = vertex.getPathEndIDValues()
      base_num_connections = vertex.getBaseNumConnections()
      non_base_num_connections = vertex.getNonBaseNumConnections()
      location = vertex.getLocation()
      is_sentinel = vertex.getIsSentinel()
      row, col = location
      self.addVertex(id_value, row, col, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel)
class Vertex:
  def __init__(self, id_value, row, col, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel):
    self.id_value = id_value
    self.path_end_id_values = path_end_id_values
    self.base_num_connections = base_num_connections
    self.non_base_num_connections = non_base_num_connections
    self.row = row
    self.col = col
    self.is_sentinel = is_sentinel
  def getIDValue(self):
    return self.id_value
  def getRow(self):
    return self.row
  def getCol(self):
    return self.col
  def getNumConnections(self):
    return self.getBaseNumConnections() + self.getNonBaseNumConnections()
  def setNumConnections(self, val):
    base_num_connections = self.getBaseNumConnections()
    non_base_num_connections = val - base_num_connections
    self.setNonBaseNumConnections(non_base_num_connections)
  def getNonBaseNumConnections(self):
    return self.non_base_num_connections
  def setNonBaseNumConnections(self, val):
    self.non_base_num_connections = val
  def getBaseNumConnections(self):
    return self.base_num_connections
  def setBaseNumConnections(self, val):
    self.base_num_connections = val
  def getLocation(self):
    return (self.row, self.col)
  def toLocationString(self):
    return str(self.getLocation())
  def toString(self):
    node1 = self
    node2 = self.getPathEnd()
    node_str1 = node1.toLocationString()
    node_str2 = node2.toLocationString()
    result = "(" + node_str1 + ", " + node_str2 + ")"
    return result
  def getPathEndIDValues(self):
    return self.path_end_id_values
  def addPathEndIDValue(self, path_end_id_value):
    curr_id_value = self.getIDValue()
    all_trivial = True
    for id_value in self.path_end_id_values:
      if id_value != curr_id_value:
        all_trivial = False
        break
    if all_trivial == True:
      self.path_end_id_values = [path_end_id_value]
    else:
      self.path_end_id_values.append(path_end_id_value)
  def setPathEndIDValues(self, path_end_id_values):
    next_path_end_id_values = path_end_id_values[ : ]
    self.path_end_id_values = next_path_end_id_values
  @staticmethod
  def formKey(vertex):
    id_value = vertex.getIDValue()
    path_end_id_values = vertex.getPathEndIDValues()
    base_num_connections = vertex.base_num_connections
    non_base_num_connections = vertex.non_base_num_connections
    location = vertex.getLocation()
    is_sentinel = vertex.getIsSentinel()
    components = [id_value, location, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel]
    next_components = tuple(components)
    return next_components
  @staticmethod
  def formFromKey(key):
    id_value, location, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel = key
    row1, col1 = location
    vertex = Vertex(id_value, row1, col1, path_end_id_values, base_num_connections, non_base_num_connections, is_sentinel)
    return vertex
  def clone(self):
    key = Vertex.formKey(self)
    vertex = Vertex.formFromKey(key)
    return vertex
  def getIsSentinel(self):
    return self.is_sentinel
  def setIsSentinel(self, is_sentinel):
    self.is_sentinel = is_sentinel
class Connection:
  def __init__(self):
    self.short_connected = None
    self.long_connected = None
    self.room = None
    self.neighbor = None
    self.room_partner = None
    self.neighbor_partner = None
  def connectShort(self, location1, location2, full_grid, is_for_horizontal_cut_edge, is_for_second_to_last_cell, prev_k, do_override_non_trivial_head, do_override_non_trivial_base):
    row1, col1 = location1
    row2, col2 = location2
    vertex_a = full_grid.getVertex(row1, col1)
    vertex_b = full_grid.getVertex(row2, col2)
    room = vertex_a
    neighbor = vertex_b
    short_connected = False
    num_connections1 = full_grid.getNumConnections(room.getRow(), room.getCol())
    num_connections2 = full_grid.getNumConnections(neighbor.getRow(), neighbor.getCol())
    room_partner = None
    neighbor_partner = None
    created_cycle_for_last_cell = False
    if num_connections1 != 2 and num_connections2 != 2:
      safe_to_continue = False
      if is_for_second_to_last_cell == True and room in full_grid.getPathEndNodes(neighbor.getRow(), neighbor.getCol()) and prev_k == 0:
        safe_to_continue = True
        created_cycle_for_last_cell = True
      if room not in full_grid.getPathEndNodes(neighbor.getRow(), neighbor.getCol()):
        safe_to_continue = True
      if safe_to_continue == True:
        nodes1 = full_grid.getPathEndNodes(room.getRow(), room.getCol())
        nodes2 = full_grid.getPathEndNodes(neighbor.getRow(), neighbor.getCol())
        matches1 = full_grid.getPathEndNodes(nodes1[0].getRow(), nodes1[0].getCol())
        matches2 = full_grid.getPathEndNodes(nodes2[0].getRow(), nodes2[0].getCol())
        room_partner = None
        if len(nodes1) > 1:
          room_partner = nodes1[0] if nodes1[0] in matches1 else nodes1[1]
        else:
          room_partner = nodes1[0]
        neighbor_partner = None
        if len(nodes2) > 1:
          neighbor_partner = nodes2[0] if nodes2[0] in matches2 else nodes2[1]
        else:
          neighbor_partner = nodes2[0]
        assert(room in full_grid.getPathEndNodes(room_partner.getRow(), room_partner.getCol()))
        assert(neighbor in full_grid.getPathEndNodes(neighbor_partner.getRow(), neighbor_partner.getCol()))
        short_connected = True
        full_grid.setPathEnd(room_partner.getRow(), room_partner.getCol(), neighbor.getRow(), neighbor.getCol(), do_override_non_trivial_head)
        full_grid.setPathEnd(neighbor.getRow(), neighbor.getCol(), room_partner.getRow(), room_partner.getCol(), do_override_non_trivial_base)
        full_grid.idempotentRemovePathEnd(room.getRow(), room.getCol(), room_partner.getIDValue())
        full_grid.idempotentRemovePathEnd(room_partner.getRow(), room_partner.getCol(), room.getIDValue())
        full_grid.setNumConnections(room.getRow(), room.getCol(), room.getNumConnections() + 1)
        full_grid.setNumConnections(neighbor.getRow(), neighbor.getCol(), neighbor.getNumConnections() + 1)
        was_horizontal1 = full_grid._idempotentRemoveCutEdgePathKey(room.getLocation(), room_partner.getLocation())
        full_grid._idempotentRemoveCutEdgePathKey(room_partner.getLocation(), room.getLocation())
        if was_horizontal1 == True or (was_horizontal1 == None and is_for_horizontal_cut_edge == True):
          full_grid._addHorizontalCutEdgePathKey(neighbor.getLocation(), room_partner.getLocation())
        elif was_horizontal1 == False or (was_horizontal1 == None and is_for_horizontal_cut_edge == False):
          full_grid._addVerticalCutEdgePathKey(neighbor.getLocation(), room_partner.getLocation())
        if is_for_horizontal_cut_edge == True:
          full_grid._addHorizontalCutEdgePathKey(room_partner.getLocation(), neighbor.getLocation())
        elif is_for_horizontal_cut_edge == False:
          full_grid._addVerticalCutEdgePathKey(room_partner.getLocation(), neighbor.getLocation())
    self.short_connected = short_connected
    self.long_connected = False
    self.room = room
    self.neighbor = neighbor
    self.room_partner = room_partner
    self.neighbor_partner = neighbor_partner
    return created_cycle_for_last_cell
  def connectLong(self, location1, location2, full_grid, is_for_horizontal_cut_edge, is_for_second_to_last_cell, prev_k):
    assert(location1 == location2)
    row1, col1 = location1
    row2, col2 = location2
    vertex_a = full_grid.getVertex(row1, col1)
    vertex_b = full_grid.getVertex(row2, col2)
    room = vertex_a
    neighbor = vertex_b
    merge_connected = False
    num_connections1 = full_grid.getNumConnections(room.getRow(), room.getCol())
    num_connections2 = full_grid.getNumConnections(neighbor.getRow(), neighbor.getCol())
    room_partner = None
    neighbor_partner = None
    short_connected = True
    candidate_nodes = full_grid.getPathEndNodes(room.getRow(), room.getCol())
    room_partner = candidate_nodes[0]
    neighbor_partner = candidate_nodes[1]
    long_connected = True
    full_grid.setPathEnd(room_partner.getRow(), room_partner.getCol(), neighbor_partner.getRow(), neighbor_partner.getCol(), True)
    full_grid.setPathEnd(neighbor_partner.getRow(), neighbor_partner.getCol(), room_partner.getRow(), room_partner.getCol(), True)
    was_horizontal1 = None
    was_horizontal2 = None
    if short_connected == False:
      raise Exception()
    elif short_connected == True:
      was_horizontal1 = full_grid._idempotentRemoveCutEdgePathKey(neighbor.getLocation(), room_partner.getLocation())
      full_grid._idempotentRemoveCutEdgePathKey(room_partner.getLocation(), neighbor.getLocation())
    if short_connected == False:
      raise Exception()
    elif short_connected == True:
      was_horizontal2 = full_grid._idempotentRemoveCutEdgePathKey(neighbor.getLocation(), neighbor_partner.getLocation())
      full_grid._idempotentRemoveCutEdgePathKey(neighbor_partner.getLocation(), neighbor.getLocation())
    if was_horizontal1 == True or (was_horizontal1 == None and is_for_horizontal_cut_edge == True):
      full_grid._addHorizontalCutEdgePathKey(neighbor_partner.getLocation(), room_partner.getLocation())
    elif was_horizontal1 == False or (was_horizontal1 == None and is_for_horizontal_cut_edge == False):
      full_grid._addVerticalCutEdgePathKey(neighbor_partner.getLocation(), room_partner.getLocation())
    if was_horizontal2 == True or (was_horizontal2 == None and is_for_horizontal_cut_edge == True):
      full_grid._addHorizontalCutEdgePathKey(room_partner.getLocation(), neighbor_partner.getLocation())
    elif was_horizontal2 == False or (was_horizontal2 == None and is_for_horizontal_cut_edge == False):
      full_grid._addVerticalCutEdgePathKey(room_partner.getLocation(), neighbor_partner.getLocation())
    self.long_connected = long_connected
    self.room = room
    self.neighbor = neighbor
    self.room_partner = room_partner
    self.neighbor_partner = neighbor_partner
  def successfullyConnected(self):
    return self.short_connected
  @staticmethod
  def formKey(connection):
    connected = connection.connected
    room = connection.room
    neighbor = connection.neighbor
    room_partner = connection.room_partner
    neighbor_partner = connection.neighbor_partner
    components = [connected, room.getLocation(), neighbor.getLocation(), room_partner.getLocation(), neighbor_partner.getLocation()]
    next_components = tuple(components)
    return next_components
  @staticmethod
  def formFromKey(key, location_to_vertex_dict):
    connected, location1, location2, location3, location4 = key
    room = location_to_vertex_dict[location1]
    neighbor = location_to_vertex_dict[location2]
    room_partner = location_to_vertex_dict[location3]
    neighbor_partner = location_to_vertex_dict[location4]
    connection = Connection()
    connection.connected = connected
    connection.room = room
    connection.neighbor = neighbor
    connection.room_partner = room_partner
    connection.neighbor_partner = neighbor_partner
    return connection
class SolutionCounter:
  def __init__(self, count = 0):
    self.count = count
  def getCount(self):
    return self.count
  def setCount(self, count):
    self.count = count
  def increment(self):
    self.count += 1
  def incrementBy(self, val):
    self.count += val
def getKeyWithOrderChanged(key, val):
  num_components = len(key)
  key_list = list(key)
  leading_components = key_list[ : num_components - 1]
  order_component = key_list[num_components - 1]
  next_key_list = leading_components + [val]
  next_key = tuple(next_key_list)
  return next_key
def getKeyWithOrderChangedToNegativeOne(key):
  return getKeyWithOrderChanged(key, -1)
def keyHasNegativeOneK(key):
  num_components = len(key)
  key_list = list(key)
  order_component = key_list[num_components - 1]
  result = order_component == -1
  return result
def getKeyWithOrderIncremented(key):
  num_components = len(key)
  key_list = list(key)
  order_component = key_list[num_components - 1]
  return getKeyWithOrderChanged(key, order_component + 1)
def getOrderForKey(key):
  num_components = len(key)
  key_list = list(key)
  order_component = key_list[num_components - 1]
  return order_component
def solve(full_grid, grid):
  W = grid.getWidth()
  H = grid.getHeight()
  curr_grid_key_to_count_dict = defaultdict(lambda: 0)
  curr_grid_key_to_surface_dict = {}
  initial_surface = grid
  initial_key = tuple([0] * (W + 3))
  curr_grid_key_to_count_dict[initial_key] = 1
  curr_grid_key_to_surface_dict[initial_key] = initial_surface
  next_grid_key_to_count_dict = defaultdict(lambda: 0)
  next_grid_key_to_surface_dict = {}
  for row in xrange(H):
    for col in xrange(W):
      grid_key_count_pairs = curr_grid_key_to_count_dict.items()
      is_for_second_to_last_cell = row == H - 1 and col == W - 2
      for pair in grid_key_count_pairs:
        grid_key, count = pair
        surface = curr_grid_key_to_surface_dict[grid_key]
        curr_k = getOrderForKey(grid_key)
        next_row, next_col = getNextRowAndColumn(row, col, W, H)
        if keyHasNegativeOneK(grid_key) == True:
          next_surface_key = tuple([0] * (W + 3))
          next_surface_key = getKeyWithOrderChangedToNegativeOne(next_surface_key)
          next_grid_key_to_count_dict[next_surface_key] += count
          next_grid_key_to_surface_dict[next_surface_key] = surface
          continue
        if row > 0 and col == 0:
          surface._advanceOneRow(full_grid)
        vertex = surface.getVertex(row, col)
        vertex_right = surface.getVertex(row + 1, col)
        vertex_down = surface.getVertex(row, col + 1)
        num_connections = surface.getNumConnections(row, col)
        intermediate_surface_key = None
        if (row == 0 and col == 0):
          intermediate_surface_key = tuple([0] * (W + 3))
        else:
          prev_row, prev_col = getPriorRowAndColumn(row, col, W, H)
          intermediate_surface_key = Surface.formKeyNextPreMerge(surface, prev_row, prev_col)
        if num_connections == 2:
          surface1 = surface
          left_match = intermediate_surface_key[col]
          top_match = intermediate_surface_key[W + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          if ((left_match != 0 and key_id_values.count(left_match) == 1) and (top_match != 0 and key_id_values.count(top_match) == 1)):
            surface1.setNumCompletedChains(surface1.getNumCompletedChains() + 1)
          c1 = Connection()
          c1.connectLong(vertex.getLocation(), vertex.getLocation(), surface1, False, is_for_second_to_last_cell, curr_k)
          next_surface_key = Surface.formKeyNextPostMerge(surface1, row, col)
          next_grid_key_to_count_dict[next_surface_key] += count
          next_grid_key_to_surface_dict[next_surface_key] = surface1
          continue
        if num_connections == 0:
          surface1 = surface
          surface2 = surface.clone()
          surface3 = surface.clone()
          adjacent_vertical_match = intermediate_surface_key[col + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          c1 = Connection()
          c2 = Connection()
          c1.connectShort(vertex.getLocation(), vertex_right.getLocation(), surface1, False, is_for_second_to_last_cell, curr_k, True, True)
          c2.connectShort(vertex.getLocation(), vertex_down.getLocation(), surface1, True, is_for_second_to_last_cell, curr_k, False, False)
          if c1.successfullyConnected() and c2.successfullyConnected():
            next_surface_key = Surface.formKeyNextPreMerge(surface1, row, col)
            next_grid_key_to_count_dict[next_surface_key] += count
            next_grid_key_to_surface_dict[next_surface_key] = surface1
          left_match = intermediate_surface_key[col]
          top_match = intermediate_surface_key[W + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          c1 = Connection()
          c1.connectShort(vertex.getLocation(), vertex_right.getLocation(), surface2, False, is_for_second_to_last_cell, curr_k, True, True)
          if c1.successfullyConnected():
            next_surface_key = Surface.formKeyNextPreMerge(surface2, row, col)
            next_grid_key_to_count_dict[next_surface_key] += count
            next_grid_key_to_surface_dict[next_surface_key] = surface2
          adjacent_vertical_match1 = intermediate_surface_key[col + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          c1 = Connection()
          ccflc = c1.connectShort(vertex.getLocation(), vertex_down.getLocation(), surface3, True, is_for_second_to_last_cell, curr_k, False, True)
          if c1.successfullyConnected():
            next_surface_key = Surface.formKeyNextPreMerge(surface3, row, col)
            if ccflc == True:
              next_surface_key = getKeyWithOrderChangedToNegativeOne(tuple([0] * (W + 3)))
            next_grid_key_to_count_dict[next_surface_key] += count
            next_grid_key_to_surface_dict[next_surface_key] = surface3
          continue
        elif num_connections == 1:
          surface1 = surface
          surface2 = surface.clone()
          surface3 = surface.clone()
          left_match = intermediate_surface_key[col]
          top_match = intermediate_surface_key[W + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          if (left_match != 0 and key_id_values.count(left_match) == 1) or (top_match != 0 and key_id_values.count(top_match) == 1):
            surface1.setNumCompletedChains(surface1.getNumCompletedChains() + 1)
          next_surface_key = Surface.formKeyNextPreMerge(surface1, row, col)
          next_grid_key_to_count_dict[next_surface_key] += count
          next_grid_key_to_surface_dict[next_surface_key] = surface1
          left_match = intermediate_surface_key[col]
          top_match = intermediate_surface_key[W + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          c1 = Connection()
          c1.connectShort(vertex.getLocation(), vertex_right.getLocation(), surface2, False, is_for_second_to_last_cell, curr_k, True, True)
          if c1.successfullyConnected() == True:
            next_surface_key2 = Surface.formKeyNextPreMerge(surface2, row, col)
            next_grid_key_to_count_dict[next_surface_key2] += count
            next_grid_key_to_surface_dict[next_surface_key2] = surface2
          left_match = intermediate_surface_key[col]
          top_match = intermediate_surface_key[W + 1]
          adjacent_vertical_match = intermediate_surface_key[col + 1]
          key_id_values = list(intermediate_surface_key[ : W + 2])
          c2 = Connection()
          ccflc = c2.connectShort(vertex.getLocation(), vertex_down.getLocation(), surface3, True, is_for_second_to_last_cell, curr_k, False, True)
          if c2.successfullyConnected() == True:
            next_surface_key3 = Surface.formKeyNextPreMerge(surface3, row, col)
            if ccflc == True:
              next_surface_key3 = getKeyWithOrderChangedToNegativeOne(tuple([0] * (W + 3)))
            next_grid_key_to_count_dict[next_surface_key3] += count
            next_grid_key_to_surface_dict[next_surface_key3] = surface3
      curr_grid_key_to_count_dict = next_grid_key_to_count_dict
      next_grid_key_to_count_dict = defaultdict(lambda: 0)
      curr_grid_key_to_surface_dict = next_grid_key_to_surface_dict
      next_grid_key_to_surface_dict = {}
  result_dict = {}
  for key_count_pair in curr_grid_key_to_count_dict.items():
    key, count = key_count_pair
    next_key = key
    result_dict[next_key] = count
  return result_dict
def drawGrid(grid, W, H):
  str_grid = []
  for i in xrange(H):
    row = grid[i]
    str_row = []
    for j in xrange(W):
      vertex = row[j]
      chain = vertex.getChain()
      vertex_right = grid[i][j + 1]
      vertex_down = grid[i + 1][j]
      vertex_str = vertex.toString()
      str_row.append(vertex_str)
    str_grid.append(str_row)
  for row in str_grid:
    print row
import sys
import string
args = sys.argv
file_name = args[0]
raw_W = string.atoi(args[1])
raw_H = string.atoi(args[2])
W = min([raw_W, raw_H])
H = max([raw_W, raw_H])
print "width and height:", W, H
rows = []
for i in xrange(H):
  row = [0] * W
  rows.append(row)
full_grid = FullGrid(W, H)
grid2 = Surface(W, H, 0)
id_value = 0
for i in xrange(H + 1):
  vertex_row = []
  for j in xrange(W + 1):
    kind = 1
    base_num_connections = 0
    if (i < H and j < W):
      kind = rows[i][j]
    if kind == 0:
      base_num_connections = 0
    elif kind == 1:
      base_num_connections = 2
    elif kind == 2:
      base_num_connections = 1
    elif kind == 3:
      base_num_connections = 1
    vertex = grid2.addVertex(id_value, i, j, [id_value], base_num_connections, 0, False)
    full_grid.addVertex(id_value, i, j, id_value, base_num_connections, 0, False)
    id_value += 1
result_dict = solve(full_grid, grid2)
scores = result_dict.items()
next_scores = [(getOrderForKey(x[0]), x[1]) for x in scores]
next_next_scores = [(x[0], x[1]) if x[0] != -1 else (x[0] + 1, x[1]) for x in next_scores]
next_next_scores.sort(key = lambda x: x[0])
for score_pair in next_next_scores:
  score, count = score_pair
  print "order " + str(score) + " count is " + str(count)
