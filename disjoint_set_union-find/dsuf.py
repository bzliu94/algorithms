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
  # for testing purposes
  def __str__(self):
    sets = {}
    for i in xrange(len(self.objects_to_num)):
      sets[i] = []
    for i in self.objects_to_num:
      sets[self.objects_to_num[self.find(i)]].append(i)
    out = []
    for i in sets.itervalues():
      if i:
        out.append(repr(i))
    return ', '.join(out)

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


