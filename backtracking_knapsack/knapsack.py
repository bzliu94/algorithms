# W = 16

W = 2 * 10 ** 3

# num_best = 0

# max_profit = 0

# n = 4

n = 500

class SolutionContainer:

  def __init__(self, max_profit, best_set, num_best):

    self.max_profit = max_profit

    self.best_set = best_set

    self.num_best = num_best

  def getMaxProfit(self):

    return self.max_profit

  def setMaxProfit(self, value):

    self.max_profit = value

  def getBestSet(self):

    return self.best_set

  def setBestSet(self, best_set):

      self.best_set = best_set

  def getNumBest(self):

    return self.num_best

  def setNumBest(self, num_best):

    self.num_best = num_best

# indexing starts at one

def knapsack(i, profit, weight, W, solution_container, p, w):

  if (weight <= W and profit > solution_container.getMaxProfit()):

    solution_container.setMaxProfit(profit)

    solution_container.setNumBest(i)

    solution_container.setBestSet(include[ : ])

  if promising(i, W, solution_container, p, w, profit, weight) == True:

    include[i + 1 - 1] = True

    knapsack(i + 1, profit + p[i + 1 - 1], weight + w[i + 1 - 1], W, solution_container, p, w)

    include[i + 1 - 1] = False

    knapsack(i + 1, profit, weight, W, solution_container, p, w)

def promising(i, W, solution_container, p, w, profit, weight):

  j = None

  k = None

  tot_weight = None

  bound = None

  weight = weight

  profit = profit

  if (weight >= W):

    return False

  else:

    j = i + 1

    # bound = p[i]

    # tot_weight = w[i]

    bound = profit

    tot_weight = weight

    # print "i, j:", i, j

    # greedy fill

    while (j <= n and tot_weight + w[j - 1] <= W):

      tot_weight = tot_weight + w[j - 1]

      bound = bound + p[j - 1]

      j = j + 1

      # print "curr. j:", j

    # print "total weight:", tot_weight

    # print i, j

    k = j

    # print "pre-fractional-add bound:", bound

    # print "residual capacity:", W - tot_weight

    # print "k:", k

    if (k <= n):

      # print p[k - 1], w[k - 1]

      bound = bound + (W - tot_weight) * p[k - 1] / (1.0 * w[k - 1])

    # print bound, solution_container.getMaxProfit()

    return bound > solution_container.getMaxProfit()

p = []

w = []

include = [False] * n

import random

p_w_pair_list = []

for i in range(n):

  profit = random.randint(1, 100)

  weight = random.randint(1, W)

  p_w_pair = (profit, weight)

  p_w_pair_list.append(p_w_pair)

# print p_w_pair_list

sorted_p_w_pair_list = sorted(p_w_pair_list, key = lambda x: x[0] / (x[1] * 1.0), reverse = True)

# print [x[0] / (x[1] * 1.0) for x in sorted_p_w_pair_list]

"""

sorted_p_w_pair_list = [(100, 29), (94, 49), (100, 60), (82, 52), (35, 26), (32, 30), (65, 81), (65, 86), (59, 79), (26, 38), (42, 67), (50, 98), (10, 22), (33, 96), (16, 48), (18, 66), (11, 59), (14, 96), (4, 41), (7, 77)]

"""

# sorted_p_w_pair_list = [(40, 2), (30, 5), (50, 10), (10, 5)]

for p_w_pair in sorted_p_w_pair_list:

  profit, weight = p_w_pair

  p.append(profit)

  w.append(weight)

# print sorted_p_w_pair_list

solution_container = SolutionContainer(0, [False] * n, 0)

knapsack(0, 0, 0, W, solution_container, p, w)

"""

for i in range(2000):

  knapsack(0, 0, 0, W, solution_container, p, w)

"""

# print solution_container.getMaxProfit()

"""

for i in range(solution_container.getNumBest()):

  print solution_container.getBestSet()[i]

"""

# print p, w

best_set = solution_container.getBestSet()

# print best_set

include_indices = [x for x in range(n) if best_set[x] == True]

profit_values = [p[x] for x in include_indices]

total_profit = sum(profit_values)

weight_values = [w[x] for x in include_indices]

total_weight = sum(weight_values)

print W

# print "weight values:", w

# print "included item profit values:", profit_values

print total_profit

# print "included item weight values:", weight_values

print total_weight


