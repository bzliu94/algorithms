from Heap import *

from ..tree.LocationAwareEntry import *

class LocationAwareHeap(Heap):

  def __init__(self):

    Heap.__init__(self)

  def insert(self, k, x):

    node = self._insertHelper(k, x, LocationAwareEntry)

    entry = node.getElement()

    entry.setLocation(node)

    if not (x == entry.getValue()):

      raise Exception("values not consistent")

    return entry

  def replace(self, v, o):

    # print "replacing an entry"

    Heap.replace(self, v, o)

    """

    if v == None:

      raise Exception("setting a node to have an entry of 'None'")

    """

    o.setLocation(v)

  """

  def _swap(self, x, y):

    Heap._swap(self, x, y)

    swapped_x_entry = x.getElement()

    swapped_y_entry = y.getElement()

    swapped_x_entry.setLocation(x)

    swapped_y_entry.setLocation(y)

  """

"""

h1 = LocationAwareHeap()

entry1 = h1.insert(1, 1)

entry2 = h1.insert(2, 1)

entry3 = h1.insert(3, 1)

print h1.min().toString()

# print h1.removeMin().toString()

print h1.toString()

print entry1.getLocation().getElement() == entry1

print entry2.getLocation().getElement() == entry2

print entry3.getLocation().getElement() == entry3

"""

"""

print h1.toString()

"""

