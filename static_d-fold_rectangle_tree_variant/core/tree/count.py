import time
from core.tree.StaticFoldRectangleTree import DInterval
import random
"""
value = 0
for i in xrange(100 ** 2 * 35 * 100):
  # print i
  # value += 1
  value += random.randint(0, 1)
  pass
"""
intervals = []
num_intervals = 1000
d = 35
for i in xrange(num_intervals):
  d_to_end_value_pair_dict = {}
  for j in xrange(1, d + 1):
    start = random.randint(0, 100)
    end = start + 0.5
    end_value_pair = (start, end)
    d_to_end_value_pair_dict[j] = end_value_pair
  curr_interval = DInterval.constructDInterval(d_to_end_value_pair_dict, d)
  intervals.append(curr_interval)
time1 = time.time()
query_d_to_end_value_pair_dict = {}
for i in xrange(1, d + 1):
  start = 0
  end = 50
  end_value_pair = (start, end)
  query_d_to_end_value_pair_dict[i] = end_value_pair
query_interval = DInterval.constructDInterval(query_d_to_end_value_pair_dict, d)
for i in xrange(1):
  for curr_interval in intervals:
    brute_force_result = []
    for next_curr_interval in intervals:
      if curr_interval == next_curr_interval:
        continue
      does_intersect = DInterval.intersectCompletelyBruteForce(curr_interval, next_curr_interval)
      if does_intersect == True:
        brute_force_result.append(curr_interval)
    brute_force_result_set = set(brute_force_result)
    next_brute_force_result = list(brute_force_result_set)
time2 = time.time()
print time2 - time1, "seconds"
