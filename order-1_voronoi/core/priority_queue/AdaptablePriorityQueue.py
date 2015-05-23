from LocationAwareHeap import *

# consider using a heap queue in the future

class AdaptablePriorityQueue(LocationAwareHeap):

  def __init__(self):

    LocationAwareHeap.__init__(self)

  # remove an arbitrary node

  """

  # returns an entry

  def _remove(self, e):

  """

  # return an entry

  def removeEntry(self, e):

    # print "removal priority value:", e.getKey()

    node = e.getLocation()

    removed_entry = self._removeHelper(node)

    return removed_entry

"""

priority_queue = AdaptablePriorityQueue()

"""

