# 2019-03-19

# we also have named sets

# 2019-02-03

# a disjoint set union-find data structure

# borrowed from josiah carlson

# for n union/find operations, overall time is in O(n * alpha(n))

# we use union-by-size and path compression

# union-by-size is also known as weighting

"""

# two items are in same set?
ufset.find(obja) == ufset.find(objb)

# two items are in different sets?
ufset.find(obja) != ufset.find(objb)

# combine two sets?
ufset.union(obja, objb)

"""

from collections import defaultdict
import string

class UnionFind:
  # create empty union-find data structure
  def __init__(self):
    self.num_weights = {}
    self.parent_pointers = {}
    self.num_to_objects = {}
    self.objects_to_num = {}
    self.__repr__ = self.__str__
  # insert a collection of items -- all items must be python-hashable; 
  # each item will be on its own in a distinct set
  def insert_objects(self, obj_list):
    for obj in obj_list:
      self.find(obj)
  # find root of set that object is in; 
  # if object is not previously encountered, we make a singleton set for it; 
  # item must be python-hashable
  def find(self, obj):
    if obj == 0:
      raise Exception("zero encountered")
    if not obj in self.objects_to_num:
      obj_num = len(self.objects_to_num)
      self.num_weights[obj_num] = 1
      self.objects_to_num[obj] = obj_num
      self.num_to_objects[obj_num] = obj
      self.parent_pointers[obj_num] = obj_num
      return obj
    # we maintain stk s.t. it contains ancestors and starts off with one element; 
    # when next parent matches most recent parent, we are at root for current tree in our forest; 
    # this is for path compression
    stk = [self.objects_to_num[obj]]
    par = self.parent_pointers[stk[-1]]
    while par != stk[-1]:
      stk.append(par)
      par = self.parent_pointers[par]
    for i in stk:
      self.parent_pointers[i] = par
    return self.num_to_objects[par]
  # combine the sets that contain the two given objects; 
  # both items must be python-hashable; 
  # if either or both given items we have not previously encountered, 
  # we make singleton sets for those items and perform union
  def union(self, object1, object2):
    o1p = self.find(object1)
    o2p = self.find(object2)
    if o1p != o2p:
      on1 = self.objects_to_num[o1p]
      on2 = self.objects_to_num[o2p]
      w1 = self.num_weights[on1]
      w2 = self.num_weights[on2]
      if w1 < w2:
        o1p, o2p, on1, on2, w1, w2 = o2p, o1p, on2, on1, w2, w1
      # this is for union-by-size
      self.num_weights[on1] = w1+w2
      del self.num_weights[on2]
      self.parent_pointers[on2] = on1
  def getNumObjects(self):
    return len(self.objects_to_num)
  def getSets(self):
    set_root_to_obj_list = defaultdict(lambda: [])
    for obj in self.objects_to_num.keys():
      root = self.find(obj)
      set_root_to_obj_list[root].append(obj)
    curr_sets = set_root_to_obj_list.values()
    print set_root_to_obj_list
    return curr_sets
  # for testing purposes
  def __str__(self):
    sets = self.getSets()
    result_str = string.join([str(x) for x in sets], ", ")
    return result_str

class NamedUnionFind:
  def __init__(self):
    self.uf = UnionFind()
    self.root_to_name_dict = {}
  # prepare singleton sets s.t. each set is named after the item it contains
  def insert_objects(self, obj_list):
    for curr_obj in obj_list:
      self.root_to_name_dict[curr_obj] = curr_obj
    self.uf.insert_objects(obj_list)
  # give name of set containing the object
  def find(self, obj):
    root = self.uf.find(obj)
    return self.root_to_name_dict[root]
  # name is name for set initially containing object1
  def union(self, object1, object2):
    name = self.find(object1)
    root1 = self.uf.find(object1)
    root2 = self.uf.find(object2)
    self.root_to_name_dict.pop(root1)
    # two sets may be the same
    if root1 != root2:
      self.root_to_name_dict.pop(root2)
    self.uf.union(object1, object2)
    next_root = self.uf.find(object1)
    self.root_to_name_dict[next_root] = name
  def renameSet(self, curr_object, next_name):
    root = self.uf.find(curr_object)
    self.root_to_name_dict[root] = next_name
  def __str__(self):
    sets = self.uf.getSets()
    non_official_representatives = [x[0] for x in sets]
    representatives = [self.uf.find(x) for x in non_official_representatives]
    set_names = [self.root_to_name_dict[x] for x in representatives]
    str_list = []
    num_sets = len(sets)
    for i in xrange(num_sets):
      curr_name = set_names[i]
      curr_name_str = str(curr_name)
      curr_set = sets[i]
      curr_set_str_list = [str(x) for x in curr_set]
      curr_str = "[" + curr_name_str + ": " + string.join(curr_set_str_list, ", ") + "]"
      str_list.append(curr_str)
    result_str = string.join(str_list, ", ")
    return result_str

if __name__ == '__main__':

  import random

  uf = UnionFind()
  items = [0, 1, 2, 3, 4, 5, 6]
  uf.insert_objects(items)
  counter = 0
  while len(uf.num_weights) > 3:
    counter += 1
    uf.union(random.choice(items), random.choice(items))
  print uf, counter

  uf = NamedUnionFind()
  items = [0, 1, 2, 3, 4, 5, 6]
  uf.insert_objects(items)
  print uf.find(2)
  print uf.find(3)
  print uf.find(4)
  uf.union(2, 3)
  print uf.find(2)
  print uf.find(3)
  uf.union(2, 4)
  print uf.find(4)
  print uf


