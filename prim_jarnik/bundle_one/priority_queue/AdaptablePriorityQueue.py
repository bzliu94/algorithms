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

# we have a min-heap

priority_queue = AdaptablePriorityQueue()

entry1 = priority_queue.insert(2, 1)
entry2 = priority_queue.insert(4, 1)

result = priority_queue.removeMin()
print result.getKey()

print priority_queue.size()

# priority_queue.removeEntry(entry)
# print priority_queue.size()

print priority_queue.toString()

# to do decrease-key, we remove and add

"""


