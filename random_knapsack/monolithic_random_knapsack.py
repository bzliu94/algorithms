# 2015-08-29

class DoublyLinkedListNode:

  def __init__(self, element, prev, next):

    self.element = element
    
    self.prev = prev
    
    self.next = next

  def getElement(self):

    return self.element

  def getPrev(self):
  
    return self.prev
    
  def getNext(self):
  
    return self.next

  def setElement(self, element):

    self.element = element

  def setPrev(self, prev):
  
    self.prev = prev
    
  def setNext(self, next):
  
    self.next = next

  """

  def hasPrev(self):

    return self.prev != None

  def hasNext(self):

    return self.next != None

  def hasElement(self):

    return self.element != None

  """

# for use with DoublyLinkedListNode objects

class DoublyLinkedList:

  def __init__(self):
  
    # two sentinels

    # self.header = DoublyLinkedListNode(None, None, None)

    self.header = self._createNode(None, None, None)
    
    # self.trailer = DoublyLinkedListNode(None, self.header, None)

    self.trailer = self._createNode(None, self.header, None)
    
    (self.header).setNext(self.trailer)

    self.size = 0

  def _createNode(self, item, prev, next):

    node = DoublyLinkedListNode(item, prev, next)

    return node

  def _getHeaderSentinel(self):

    return self.header

  def _getTrailerSentinel(self):

    return self.trailer

  def getSize(self):
  
    return self.size
    
  def isEmpty(self):
  
    return self.getSize() == 0
    
  # add a node before a given node

  # in particular, add node v before node z
    
  def addBefore(self, v, z):

    w = z.getPrev()
    v.setPrev(w)
    v.setNext(z)
    w.setNext(v)
    z.setPrev(v)
    
    self.size = self.size + 1

  # add a node after a given node

  # in particular, add node v after node z
    
  def addAfter(self, v, z):

    # print v.getNext()
  
    w = z.getNext()
    v.setPrev(z)
    v.setNext(w)
    w.setPrev(v)
    z.setNext(v)

    self.size = self.size + 1

  # remove a node

  def remove(self, v):
  
    u = v.getPrev()
    w = v.getNext()
    w.setPrev(u)
    u.setNext(w)
    v.setPrev(None)
    v.setNext(None)
    
    self.size = self.size - 1

  # insert a node at head of list
    
  def addFirst(self, v):
  
    self.addAfter(v, self.header)

  # insert a node at end of list
    
  def addLast(self, v):
  
    self.addBefore(v, self.trailer)
    
  # get first node in list
  
  def getFirst(self):
  
    if self.isEmpty():
    
      raise Exception("list is empty")
  
    return (self.header).getNext()
  
  # get last node in list
  
  def getLast(self):
  
    if self.isEmpty():
    
      raise Exception("list is empty")
      
    return (self.trailer).getPrev()

  # have non-sentinel predecessor

  def hasPredecessor(self, node):

    predecessor = node.prev

    has_predecessor = not (predecessor == None or predecessor == self._getHeaderSentinel())

    return has_predecessor

  # have non-sentinel successor

  def hasSuccessor(self, node):

    successor = node.next

    has_successor = not (successor == None or successor == self._getTrailerSentinel())

    return has_successor

  """

  def toString(self):

    element_list = self.toElementList()

    element_str_list = [str(x) for x in element_list]

    element_str = "".join(element_str_list)

    return element_str

  """

  def toElementList(self):

    return self._toElementListHelper(self._getHeaderSentinel(), [])

  def _toElementListHelper(self, node, partial_element_list):

    if self._getTrailerSentinel() == node:

      return partial_element_list

    elif self._getHeaderSentinel() == node:

      return self._toElementListHelper(node.getNext(), partial_element_list)

    else:

      curr_element = node.getElement()

      return self._toElementListHelper(node.getNext(), partial_element_list + [curr_element])

  # retrieve a list of non-sentinel nodes

  def _toNodeList(self):

    return self._toNodeListHelper(self._getHeaderSentinel(), [])

  def _toNodeListHelper(self, node, partial_node_list):

    if self._getTrailerSentinel() == node:

      return partial_node_list

    elif self._getHeaderSentinel() == node:

      return self._toNodeListHelper(node.getNext(), partial_node_list)

    else:

      return self._toNodeListHelper(node.getNext(), partial_node_list + [node])

"""

list = DoublyLinkedList()

node1 = DoublyLinkedListNode(1, None, None)

node2 = DoublyLinkedListNode(2, None, None)

node3 = DoublyLinkedListNode(3, None, None)

node4 = DoublyLinkedListNode(4, None, None)

list.addFirst(node1)

list.addLast(node4)

list.addBefore(node3, node4)

list.addAfter(node2, node1)

print list.toElementList()

print list._toNodeList()

print [x.getElement() for x in list._toNodeList()]

"""

# take "point a dominates point b" 
#   to mean point a profit is strictly greater than point b profit 
#   and point a weight is less than or equal to point b weight

# do not assume pareto point (0, 0) will survive

# import decimal

# import cdecimal

def removeParetoPointsWithLargeChangeSetCombinedLoss(partial_solutions, split_item, integrality_gap_estimate, break_solution, additional_partial_solution):

  winnowed_partial_solutions = [x for x in partial_solutions if partialSolutionHasChangeSetCombinedLossLargerThanIntegralityGapEstimate(x, split_item, integrality_gap_estimate, break_solution, additional_partial_solution) == False]

  # print partial_solutions

  # print winnowed_partial_solutions

  return winnowed_partial_solutions

def removeParetoPointsWithLargeChangeSetAnticipatedCombinedLoss(partial_solutions, split_item, integrality_gap_estimate, break_solution, curr_item, additional_partial_solution):

  # winnowed_partial_solutions = removeParetoPointsWithLargeChangeSetCombinedLoss(partial_solutions, split_item, integrality_gap_estimate, break_solution)

  # winnowed_partial_solutions = partial_solutions

  # winnowed_partial_solutions = [x for x in partial_solutions if partialSolutionHasChangeSetAnticipatedCombinedLossLargerThanIntegralityGapEstimate(x, split_item, integrality_gap_estimate, break_solution, curr_item, additional_partial_solution) == False]

  winnowed_partial_solutions = [x for x in partial_solutions if partialSolutionHasChangeSetCombinedLossLargerThanIntegralityGapEstimate(x, split_item, integrality_gap_estimate, break_solution, additional_partial_solution) == False]

  return winnowed_partial_solutions

# output a list of partial solutions

def listDecompositionWithSerialConsiderAndFinalCombineSolve(subproblem_solver1, subproblem_solver2, split_item, capacity, integrality_gap_estimate, break_solution, additional_partial_solution):

  # break into two, solve the subproblems one at a time, combine at end

  while subproblem_solver1.isFinished() == False:

    subproblem_solver1.iterate(additional_partial_solution)

  while subproblem_solver2.isFinished() == False:

    subproblem_solver2.iterate(additional_partial_solution)

  partial_solutions1 = subproblem_solver1.getPartialSolutions()

  partial_solutions2 = subproblem_solver2.getPartialSolutions()

  # print [x.toString() for x in partial_solutions1]

  # print [x.toString() for x in partial_solutions2]

  partial_solution_list = listDecompositionTwoPartialSolutionCollectionScan(partial_solutions1, partial_solutions2, capacity, split_item, break_solution)

  return partial_solution_list

# output a list of partial solutions

def listDecompositionWithNonserialConsiderAndAlternatingExtendAndCombineSolve(subproblem_solver1, subproblem_solver2, split_item, capacity, integrality_gap_estimate, break_solution, additional_partial_solution):

  partial_solutions1 = []

  partial_solutions2 = []

  # break into two, solve the subproblems side-by-side, alternately extending and combining

  # finally, combine

  while not (subproblem_solver1.isFinished() == True and subproblem_solver2.isFinished() == True):

    if subproblem_solver1.isFinished() == False:

      subproblem_solver1.iterate(additional_partial_solution)

    if subproblem_solver2.isFinished() == False:

      subproblem_solver2.iterate(additional_partial_solution)

    partial_solutions1 = subproblem_solver1.getPartialSolutions()

    partial_solutions2 = subproblem_solver2.getPartialSolutions()

    # partial_solution = twoCollectionScan(partial_solutions1, partial_solutions2)

    partial_solutions = listDecompositionTwoPartialSolutionCollectionScan(partial_solutions1, partial_solutions2, capacity, split_item, break_solution)

    # assume at least one partial solution exists

    partial_solution = partial_solutions[0]

    integrality_gap_estimate.updateBestIntegralSolutionProfit(partial_solution.getTotalProfit())

    # updateIntegralityGapEstimate(partial_solution.getProfit())

  partial_solution_list = listDecompositionTwoPartialSolutionCollectionScan(partial_solutions1, partial_solutions2, capacity, split_item, break_solution)

  # partial_solution = twoCollectionScan(partial_solutions1, partial_solutions2)

  # print partial_solution

  return partial_solution_list

# output a list of partial solutions

def listDecompositionWithSerialConsiderAndLengthAwareCombineSolve(subproblem_solver1, subproblem_solver2, split_item, capacity, integrality_gap_estimate, break_solution, additional_partial_solution):

  # break into two, solve the subproblems one at a time

  # for second subproblem, occasionally combine to get better estimate for integrality gap

  # finally, combine

  while subproblem_solver1.isFinished() == False:

    subproblem_solver1.iterate(additional_partial_solution)

  curr_partial_solution_collection_size1 = None

  curr_subproblem_work = 0

  # number of partial solutions being kept for second subproblem 
  #   tends to be less than that for first subproblem 
  #   given that loss filter tends to be more effective 
  #   for the second subproblem

  while subproblem_solver2.isFinished() == False:

    # make sure we have done enough "work" 
    #   (measured in terms of collection size) 
    #   before we perform a scan

    subproblem_solver2.iterate(additional_partial_solution)

    curr_partial_solution_collection_size1 = subproblem_solver1.getPartialSolutionCollectionSize()

    curr_partial_solution_collection_size2 = subproblem_solver2.getPartialSolutionCollectionSize()

    curr_subproblem_work = curr_subproblem_work + curr_partial_solution_collection_size2

    # print curr_partial_solution_collection_size1, curr_partial_solution_collection_size2

    if curr_subproblem_work >= curr_partial_solution_collection_size1:

      curr_subproblem_work = curr_subproblem_work - curr_partial_solution_collection_size1

      # perform a scan

      partial_solutions1 = subproblem_solver1.getPartialSolutions()

      partial_solutions2 = subproblem_solver2.getPartialSolutions()

      # print "current partial solutions #1:", [x.toString() for x in partial_solutions1]

      # print "current partial solutions #2:", [x.toString() for x in partial_solutions2]

      # partial_solution = twoCollectionScan(partial_solutions1, partial_solutions2)

      partial_solution_list = listDecompositionTwoPartialSolutionCollectionScan(partial_solutions1, partial_solutions2, capacity, split_item, break_solution)

      # print "partial solutions arrived at through combining:", [x.toString() for x in partial_solution_list]

      # assume at least one partial solution exists

      partial_solution = partial_solution_list[0]

      profit = partial_solution.getTotalProfit()

      # print "profit:", profit

      integrality_gap_estimate.updateBestIntegralSolutionProfit(profit)

      # print "integrality gap estimate:", integrality_gap_estimate.getValue()

  partial_solutions1 = subproblem_solver1.getPartialSolutions()

  partial_solutions2 = subproblem_solver2.getPartialSolutions()

  # print "partial solutions #1, again:", [x.toString() for x in partial_solutions1]

  # print "partial solutions #2, again:", [x.toString() for x in partial_solutions2]

  partial_solution_list = listDecompositionTwoPartialSolutionCollectionScan(partial_solutions1, partial_solutions2, capacity, split_item, break_solution)

  """

  partial_solution = twoCollectionScan(partial_solutions1, partial_solutions2)

  updateIntegralityGapEstimate(partial_solution.getProfit())

  """

  return partial_solution_list

# state that items with weight zero are not allowed

"""

assume that weights are non-negative

assume that partial_solutions is sorted 
  using a lexicographic ordering 
  with key values nondecreasing; 
  have as keys (weight, profit) tuples

compare weights as usual and compare profits as usual

"""

# assume that given list is non-empty

def removeDominatedParetoPointsGivenThatWeightValuesAreSame(partial_solutions):

  profit_values = [x.getTotalProfit() for x in partial_solutions]

  max_profit_value = max(profit_values)

  candidate_partial_solutions = [x for x in partial_solutions if x.getTotalProfit() == max_profit_value]

  """

  chosen_partial_solution = candidate_partial_solutions[0]

  return chosen_partial_solution

  """

  return candidate_partial_solutions

def removeDominatedParetoPointsGivenThatWeightValuesAreUnique(partial_solutions):

  if len(partial_solutions) == 0:

    return None

  else:

    partial_solution = partial_solutions[0]

    profit = partial_solution.getTotalProfit()

    return removeDominatedParetoPointsGivenThatWeightValuesAreUniqueHelper(partial_solutions[1 : ], profit, [partial_solution])

def removeDominatedParetoPointsGivenThatWeightValuesAreUniqueHelper(partial_solutions, best_profit, partial_result):

  if len(partial_solutions) == 0:

    return partial_result

  else:

    curr_partial_solution = partial_solutions[0]

    curr_profit = curr_partial_solution.getTotalProfit()

    if curr_profit <= best_profit:

      # omit current item

      return removeDominatedParetoPointsGivenThatWeightValuesAreUniqueHelper(partial_solutions[1 : ], best_profit, partial_result)

    elif curr_profit > best_profit:

      # keep current item

      return removeDominatedParetoPointsGivenThatWeightValuesAreUniqueHelper(partial_solutions[1 : ], curr_profit, partial_result + [curr_partial_solution])

# compare two partial solutions

def weightProfitComp(x, y):

  weight_x = x.getTotalWeight()

  ratio_x = x.getEffectiveRatio()

  weight_y = y.getTotalWeight()

  ratio_y = y.getEffectiveRatio()

  if weight_x == weight_y:

    if ratio_x == ratio_y:

      return 0

    elif ratio_x < ratio_y:

      return -1

    elif ratio_x > ratio_y:

      return 1

  elif weight_x < weight_y:

    return -1

  elif weight_x > weight_y:

    return 1

def mergeOnBasisOfWeightAndProfit(partial_solutions1, partial_solutions2):

  if len(partial_solutions1) == 0 and len(partial_solutions2) == 0:

    return []

  elif len(partial_solutions1) == 0 and len(partial_solutions2) != 0:

    partial_solution2 = partial_solutions2[0]

    return [partial_solution2] + mergeOnBasisOfWeightAndProfit(partial_solutions1, partial_solutions2[1 : ])

  elif len(partial_solutions1) != 0 and len(partial_solutions2) == 0:

    partial_solution1 = partial_solutions1[0]

    return [partial_solution1] + mergeOnBasisOfWeightAndProfit(partial_solutions1[1 : ], partial_solutions2)

  elif len(partial_solutions1) != 0 and len(partial_solutions2) != 0:

    partial_solution1 = partial_solutions1[0]

    partial_solution2 = partial_solutions2[0]

    chosen_partial_solution = None

    next_partial_solutions1 = partial_solutions1[ : ]

    next_partial_solutions2 = partial_solutions2[ : ]

    if weightProfitComp(partial_solution1, partial_solution2) == -1:

      chosen_partial_solution = partial_solution1

      next_partial_solutions1.pop(0)

    elif weightProfitComp(partial_solution1, partial_solution2) == 0:

      chosen_partial_solution = partial_solution1

      next_partial_solutions1.pop(0)

    elif weightProfitComp(partial_solution1, partial_solution2) == 1:

      chosen_partial_solution = partial_solution2

      next_partial_solutions2.pop(0)

    return [chosen_partial_solution] + mergeOnBasisOfWeightAndProfit(next_partial_solutions1, next_partial_solutions2)

def removeDuplicateValuesGivenSortedValues(values):

  if len(values) == 0:

    return []

  else:

    value = values[0]

    return [value] + removeDuplicateValuesGivenSortedValuesHelper(values[1 : ], value)

def removeDuplicateValuesGivenSortedValuesHelper(values, prev_value):

  if len(values) == 0:

    return []

  else:

    curr_value = values[0]

    if curr_value == prev_value:

      return removeDuplicateValuesGivenSortedValuesHelper(values[1 : ], curr_value)

    else:

      return [curr_value] + removeDuplicateValuesGivenSortedValuesHelper(values[1 : ], curr_value)

# output a list of lists

# assume input is sorted by weight

# output list will have lists be ordered relative to each other by weight

def groupByWeight(partial_solutions):

  ordered_weight_values = [x.getTotalWeight() for x in partial_solutions]

  ordered_distinct_weight_values = removeDuplicateValuesGivenSortedValues(ordered_weight_values)

  # print ordered_distinct_weight_values

  weight_to_partial_solution_list_dict = {}

  for i in range(len(partial_solutions)):

    curr_partial_solution = partial_solutions[i]

    weight = curr_partial_solution.getTotalWeight()

    if weight in weight_to_partial_solution_list_dict:

      weight_to_partial_solution_list_dict[weight] = weight_to_partial_solution_list_dict[weight] + [curr_partial_solution]

    else:

      weight_to_partial_solution_list_dict[weight] = [curr_partial_solution]

  ordered_weight_list_list = [weight_to_partial_solution_list_dict[x] for x in ordered_distinct_weight_values]

  return ordered_weight_list_list

def toFractionalSolutionProfitWeightTuple(partial_solution, split_item, split_item_fraction):

  profit = partial_solution.getTotalProfit()

  weight = partial_solution.getTotalWeight()

  split_item_profit = split_item.getProfit()

  split_item_weight = split_item.getWeight()

  total_profit = profit + split_item_profit * split_item_fraction

  total_weight = weight + split_item_weight * split_item_fraction

  result = (total_profit, total_weight)

  return result

"""

def getLossValue(split_item_ratio, item):

  profit = item.getProfit()

  weight = item.getWeight()

  ratio = item.getRatio()

  loss = abs(weight * (split_item_ratio - 1.0 * ratio))

  # print "loss:", loss

  return loss

"""

# get loss value for an item

# def getLossValue(unaltered_break_solution, item, modified_pareto_point):

def getLossValue(split_item_ratio, item):

  # check if item is in break solution; if it is, do not consider its loss value

  """

  if unaltered_break_solution.hasItem(item):

    return 0

  else:

  """

  # use modified pareto point

  # pareto_point = unaltered_break_solution.toParetoPoint()

  """

  break_solution_profit = pareto_point.getProfit()

  break_solution_weight = pareto_point.getWeight()

  """

  # break_solution_ratio = pareto_point.getRatio()

  # modified_break_solution_ratio = modified_pareto_point.getRatio()

  # break_solution_ratio = unaltered_break_solution.getEffectiveRatio()

  profit = item.getProfit()

  weight = item.getWeight()

  ratio = item.getRatio()

  # loss = abs(weight * (break_solution_ratio - 1.0 * ratio))

  # loss = abs(profit - modified_break_solution_ratio * (1.0 * weight))

  # loss = abs(profit - break_solution_ratio * (1.0 * weight))

  loss = abs(weight * (split_item_ratio - 1.0 * ratio))

  return loss

# get loss for change set relative to an arbitrary break solution

def getChangeSetCombinedLossForPartialSolution(break_solution, partial_solution, split_item, additional_partial_solution):

  # item must be in change set for loss to be considered

  # if an item in our current solution is in break solution, we ignore its loss value

  # if an item is in break solution but not in our current solution, we still count its loss value

  # ratio used corresponds to that of a break item

  """

  split_item_ratio = split_item.getRatio()

  profit = partial_solution.getTotalProfit()

  weight = partial_solution.getTotalWeight()

  ratio = partial_solution.getEffectiveRatio()

  loss = abs(weight * (split_item_ratio - 1.0 * ratio))

  return loss

  """

  """

  if partial_solution.getNumItems() == 0:

    loss = 0

    return loss

  else:

  """

  """

  items = partial_solution.getItems()

  # loss_values = [getLossValue(split_item.getRatio(), x) for x in items if break_solution.hasItem(x) == False]

  loss_values = [getLossValue(split_item.getRatio(), x) for x in items]

  total_loss_value = sum(loss_values)

  """

  """

  total_loss_value = partial_solution.getTotalLoss()

  return total_loss_value

  """

  total_loss_value = partial_solution.getTotalLoss(additional_partial_solution)

  return total_loss_value

def partialSolutionHasChangeSetAnticipatedCombinedLossLargerThanIntegralityGapEstimate(partial_solution, split_item, integrality_gap_estimate, break_solution, curr_item):

  total_loss_value = getChangeSetCombinedLossForPartialSolution(break_solution, partial_solution, split_item)

  is_larger = None

  """

  # check if item is in current partial_solution

  if partial_solution.hasItem(curr_item):

    is_larger = total_loss_value > integrality_gap_estimate.getValue()

  elif not partial_solution.hasItem(curr_item):

    curr_loss = getLossValue(break_solution, curr_item)

    # check if item is in break solution

    if break_solution.hasItem(curr_item):

      is_larger = total_loss_value > integrality_gap_estimate.getValue()

    else:

      is_larger = (total_loss_value + curr_loss) > integrality_gap_estimate.getValue()

  """

  # check if item is in current partial solution

  # modified_pareto_point = partial_solution.getAdjustedBreakSolutionParetoPoint()

  if partial_solution.hasItem(curr_item):

    is_larger = total_loss_value > integrality_gap_estimate.getValue()

  elif not partial_solution.hasItem(curr_item):

    curr_loss = getLossValue(split_item.getRatio(), curr_item)

    is_larger = (total_loss_value + curr_loss) > integrality_gap_estimate.getValue()

  return is_larger

  # raise Exception()

  # is_larger = partialSolutionHasChangeSetCombinedLossLargerThanIntegralityGapEstimate(partial_solution, split_item, integrality_gap_estimate, break_solution)

  # return is_larger

def partialSolutionHasChangeSetCombinedLossLargerThanIntegralityGapEstimate(partial_solution, split_item, integrality_gap_estimate, break_solution, additional_partial_solution):

  total_loss_value = getChangeSetCombinedLossForPartialSolution(break_solution, partial_solution, split_item, additional_partial_solution)

  # print total_loss_value, integrality_gap_estimate.getValue()

  is_larger = total_loss_value > integrality_gap_estimate.getValue()

  return is_larger

def updateIntegralityGapEstimateBasedOnProfit(integrality_gap_estimate, profit):

  integrality_gap_estimate.updateBestIntegralSolutionProfit(profit)

# return minus infinity if no partial solutions are available

def getHighestProfit(partial_solutions):

  profit_values = [x.getTotalProfit() for x in partial_solutions]

  if len(profit_values) == 0:

    return float("-inf")

  else:

    largest_profit_value = max(profit_values)

    return largest_profit_value

"""

assume we have values taken from a uniform distribution

uses a core-idea-based approach

takes O(n) expected time, except when we consider sorting

"""

"""

involves solving knapsacks exactly

"""

"""

as an example of a large test case, we could have 4000 size-2000 knapsacks

knapsacks could have repeated items, but the problems are roughly independent

time limit is two seconds

"""

"""

# a* search using heuristic of an upper bound

# we obtain upper bound by calculating solution for relaxed version of problem

"""

"""

class Item:

  def __init__(self, profit, value, do_include):

    self.profit = profit

    self.value = value

    self.do_include = do_include

class PartialSolution:

  def __init__(self, items = []):

    self.item_set = set(items)

class SolutionCollection:

  def __init__(self, solutions = []):

    self.solution_set = set(solutions)

  def addPartialSolution(self, partial_solution)

    solution_set = self.solution_set

    solution_set = solution_set | set([partial_solution])

items = [Item(1, 1), Item(1, 2)]

print items

# assume values chosen from uniform distribution

# dynamic programming with lists

# dominated sets

# grow core in order of increasing loss

# stopping problem for expanding core

# two bounds for core size

# two lists for introducing a power of one-half

# consider items in order of increasing loss

# two additional heuristics

# balance work for two lists based on size

# stopping problem for pruning for whole problem



partial_solutions = SolutionCollection()

initial_partial_solution = PartialSolution()

partial_solutions = initial_partial_solution.addPartialSolution(initial_partial_solution)

"""

"""

(beier and voecking, 2006)

c = beta * (sum of weights)

0 <= beta <= 1

delta = 0.5

R = 2 ^ 30 - 1

(scale by R and round to nearest integer)

1. uniform instances

  w_i <- U[0, 1], p_i <- U[0, 1]

2. delta-correlated instances

  w_i <- U[0, 1], p_i <- w_i + r with r <- U[(-1 * delta) / 2, delta / 2]

3. instances with similar weight

  w_i <- U[(1 - epsilon), 1] and p_i <- U[0, 1]

4. instances with similar profit

  w_i <- U[0, 1] and p_i <- U[(1 - epsilon), 1]

"""

"""

(kellerer and pferschy, 2004)

c = h / (H + 1) * (sum of weights)

h is in 1, ..., H

H = 100

1. uncorrelated data instances

  p_i <- U[1, R], w_i <- U[1, R]

  R = 10 ^ 3 or 10 ^ 4

2. weakly-correlated instances

  p_i <- [(w_j - R / 10), (w_j + R / 10)], w_i <- [1, R]

  p_j >= 1

  R = 10 ^ 3 or 10 ^ 4

3. strongly-correlated instances

  w_i <- [1, R], p_i <- w_i + R / 10

  R = 10 ^ 3 or 10 ^ 4

4. inverse strongly-correlated instances

  p_i <- [1, R], w_i <- p_i + R / 10

  R = 10 ^ 3 or 10 ^ 4

5. almost strongly-correlated instances

  w_i <- [1, R], p_i <- [w_i + R / 10 - R / 500, w_i + R / 10 + R / 500]

  R = 10 ^ 3 or 10 ^ 4

6. subset sum instances

  w_i <- [1, R], p_i <- w_i

  R = 10 ^ 3 or 10 ^ 4

7. uncorrelated instances with similar weights

  w_i <- [100000, 100100], p_i <- [1, 1000]

"""

"""

(martello and toth, 1990)

c = 0.5 * (sum of weights) or 200

1. uncorrelated

  p_i <- [1, v], w_i <- [1, v]

  v = 100 or 1000

2. weakly correlated

  w_i <- [1, v]

  p_i <- [w_i - r, w_i + r]

  r = v / 10

3. strongly correlated

  w_i <- [1, v], p_i = w_i + r

  r = v / 10

"""

"""

import random

# items are (value, weight) pairs

items = []

# n = 10000

n = 100

# R = 2 ** 30 - 1

R = 2 ** 5 - 1

for i in range(n):

  # w_i = random.random()

  # p_i = random.random()

  w_i = int(random.randint(0, R))

  p_i = int(random.randint(0, R))

  item = (w_i, p_i)

  items.append(item)

# items = [(1, 1), (2, 2), (3, 3)]

weights = [x[0] for x in items]

values = [x[1] for x in items]

total_weight = sum(weights)

beta = 0.5

# c = beta * total_weight

W = int(beta * total_weight)

# n = len(items)

K = {}

# W = 4

# j is in [0, n]

# w is in [0, W]

for j in range(0, n + 1):

  K[(0, j)] = 0

for w in range(0, W + 1):

  K[(w, 0)] = 0

for j in range(1, n + 1):

  for w in range(1, W + 1):

    w_j = weights[j - 1]

    v_j = values[j - 1]

    if w_j > w:

      K[(w, j)] = K[(w, j - 1)]

    else:

      K[(w, j)] = max(K[(w, j - 1)], K[(w - w_j, j - 1)] + v_j)

value = K[(W, n)]

print value

"""

"""

integrality gap

initial core size

fractional problem

weight-and-ratio-based ordering

loss-based ordering

exact solution

whole problem

"""

"""

tagged pareto point

tagged pareto point collection size

application

"""

import random

# takes O(n) expected time

# assume size of S is >= 1

# k is in [1, n]

def quickSelect(S, k):

  if len(S) == 0:

    return None

  if len(S) == 1:

    return S[0]

  pivot_index = random.randint(0, len(S) - 1)

  pivot = S[pivot_index]

  L = [x for x in S if x < pivot]

  E = [x for x in S if x == pivot]

  G = [x for x in S if x > pivot]

  if k <= len(L):

    return quickSelect(L, k)

  elif k <= len(L) + len(E):

    return pivot

  else:

    return quickSelect(G, k - len(L) - len(E))

# assume that items is a list of size >= 1

def getMedian(items):

  S = items

  num_items = len(items)

  k = None

  if num_items % 2 == 0:

    k = num_items / 2

  elif num_items % 2 == 1:

    k = (num_items - 1) / 2 + 1

  return quickSelect(S, k)

# assume that items are not all able to fit in knapsack at the same time

# returns a three-tuple

# (break_solution_items, split_item, amount_of_split_item)

# break_solution_items is a list of items for an arbitrary break solution

# split item is an item

def linearTimeFractionalSolve(items, capacity):

  if len(items) == 0:

    return ([], None, None)

  weights = [x.getWeight() for x in items]

  weight_sum = sum(weights)

  if weight_sum <= capacity:

    return (items, None, None)

  z_w_pairs = [(-1 * x.getRatio(), x.getWeight()) for x in items]

  weighted_median_z_w_pair = getWeightedMedian(z_w_pairs, capacity)

  z, w = weighted_median_z_w_pair

  candidate_weighted_median_items = [x for x in items if x.getRatio() == -1 * z]

  chosen_weighted_median_item = candidate_weighted_median_items[0]

  split_item = chosen_weighted_median_item

  split_item_ratio = split_item.getRatio()

  G_items = [x for x in items if x.getRatio() > split_item_ratio]

  E_items = [x for x in items if x.getRatio() == split_item_ratio]

  # winnowed_E_items = [x for x in E_items if x != split_item]

  # chosen_E_items = []

  G_weights = [x.getWeight() for x in G_items]

  G_sum = sum(G_weights)

  # remaining_capacity = capacity - L_sum

  # weight = L_sum

  # chosen_items = L_items + chosen_E_items

  chosen_items = G_items

  amount_of_split_item = (capacity - G_sum) / (1.0 * split_item.getWeight())

  result = (chosen_items, split_item, amount_of_split_item)

  return result

# if there are no items or there is no weighted median 
#   (e.g. all items sum to a value less than or equal to W), 
#   return None

# each item is a (z, w) tuple

# items to left have weights that sum to value 
#   less than or equal to W, and items to left 
#   together with found item have weights 
#   that sum to value greater than W

# weight-guided median-driven selection of item

def getWeightedMedian(items, W):

  if len(items) == 0:

    return None

  z_values = [x[0] for x in items]

  median_z_value = getMedian(z_values)

  candidate_median_items = [x for x in items if x[0] == median_z_value]

  median_item = candidate_median_items[0]

  L_items = [x for x in items if x[0] < median_z_value]

  E_items = [x for x in items if x[0] == median_z_value]

  G_items = [x for x in items if x[0] > median_z_value]

  # get median of efficiencies

  # partition into two

  L_weights = [x[1] for x in L_items]

  E_weights = [x[1] for x in E_items]

  G_weights = [x[1] for x in G_items]

  L_sum = sum(L_weights)

  E_sum = sum(E_weights)

  G_sum = sum(G_weights)

  # print L_sum, E_sum, G_sum, W

  # if sum of items to left is <= c and sum of items to left plus sum of one item from right > c, item from right is split item

  # if sum of items to left is <= c, recursively call method on right portion

  # if sum of items to left is > c, recursively call method on left portion

  if L_sum < W and W <= (L_sum + E_sum):

    return median_item

  elif (L_sum + E_sum) < W:

    return getWeightedMedian(G_items, W - (L_sum + E_sum))

  elif L_sum >= W:

    return getWeightedMedian(L_items, W)

# returns a three-tuple

# (partial_solution, split_item, split_item_fraction)

# split_item can be None

# split_item_fraction is a value >= 0 and <= 1

def fractionalSolve(items, capacity):

  # follow a greedy strategy

  # consider ratio and weight

  items.sort(key = lambda x: x.getRatio(), reverse = True)

  chosen_items = []

  weight = 0

  split_item = None

  split_item_fraction = None

  for i in range(len(items)):

    curr_item = items[i]

    curr_weight = curr_item.getWeight()

    next_weight = weight + curr_weight

    if next_weight <= capacity:

      # choose item

      chosen_items = chosen_items + [curr_item]

      weight = weight + curr_weight

    elif next_weight > capacity:

      split_item = curr_item

      amount_of_split_item = (capacity - weight) / (1.0 * curr_weight)

      break

  partial_solution = PartialSolution(chosen_items, split_item, None)

  # print "chosen whole items:", [x.toParetoPoint().toProfitWeightTuple() for x in chosen_items]

  return (partial_solution, split_item, amount_of_split_item)

  """

  # check if we have space left over

  space_left_over = capacity - weight

  have_space_left_over = space_left_over > 0

  """

# an integrality gap estimate acts as an upper bound

class IntegralityGapEstimate:

  def __init__(self, optimal_fractional_solution_profit, best_integral_solution_profit):

    self.optimal_fractional_solution_profit = optimal_fractional_solution_profit

    self.best_integral_solution_profit = best_integral_solution_profit

  def getOptimalFractionalSolutionProfit(self):

    return self.optimal_fractional_solution_profit

  def getBestIntegralSolutionProfit(self):

    return self.best_integral_solution_profit

  def updateBestIntegralSolutionProfit(self, integral_solution_profit):

    # print self.optimal_fractional_solution_profit, self.best_integral_solution_profit, integral_solution_profit

    self.best_integral_solution_profit = max(self.best_integral_solution_profit, integral_solution_profit)

  def getValue(self):

    optimal_fractional_solution_profit = self.getOptimalFractionalSolutionProfit()

    best_integral_solution_profit = self.getBestIntegralSolutionProfit()

    # print "optimal fractional solution profit:", optimal_fractional_solution_profit

    # print "best integral solution profit:", best_integral_solution_profit

    value = optimal_fractional_solution_profit - best_integral_solution_profit

    return value

# assume that items are provided so that their loss values are in non-decreasing order

class Problem:

  def __init__(self, items, capacity):

    # self.items = items

    self.item_list = DoublyLinkedList()

    self.capacity = capacity

    self.item_to_node_dict = {}

    for item in items:

      self.addItem(item)

  # assume items are to be retrieved so that their loss values are in non-decreasing order

  def getItems(self):

    # return self.items

    return (self.item_list).toElementList()

  def getInitialCoreProblem(self):

    pass

  def getBreakSolution(self):

    pass

  def getSplitItem(self):

    pass

  def getNumItems(self):

    """

    items = self.getItems()

    num_items = len(items)

    return num_items

    """

    return self.item_list.getSize()

  def getCapacity(self):

    return self.capacity

  # assume item added has loss value 
  #   greater than or equal to the loss values 
  #   of items already added to the problem

  # note that this then means that 
  #   we may add the item to end of a list

  def addItem(self, item):

    # self.items = self.items + item

    node = (self.item_list)._createNode(item, None, None)

    (self.item_list).addLast(node)

    (self.item_to_node_dict)[item] = node

  # takes O(1) time

  def removeItem(self, item):

    node = (self.item_to_node_dict)[item]

    (self.item_list).remove(node)

    (self.item_to_node_dict).pop(item)

  def hasItem(self, item):

    has_item = item in self.item_to_node_dict

    return has_item

  def setCapacity(self, capacity):

    self.capacity = capacity

class CoreProblem:

  def __init__(self):

    pass

  def expandByOneItem(self):

    pass

class PartialSolution:

  def __init__(self, items, split_item, break_solution = None):

    # self.items = items

    self.item_list = DoublyLinkedList()

    self.item_to_node_dict = {}

    self.total_profit = 0

    self.total_weight = 0

    # self.total_loss = 0

    self.split_item = split_item

    self.break_solution = break_solution

    for item in items:

      self.addItem(item)

  def getItems(self):

    # return self.items

    return (self.item_list).toElementList()

  def getTotalProfit(self):

    """

    items = self.getItems()

    profit_values = [x.getProfit() for x in items]

    total_profit = sum(profit_values)

    return total_profit

    """

    return self.total_profit

  def getTotalWeight(self):

    """

    items = self.getItems()

    weight_values = [x.getWeight() for x in items]

    total_weight = sum(weight_values)

    return total_weight

    """

    return self.total_weight

  def _getSplitItem(self):

    return self.split_item

  def _getBreakSolution(self):

    return self.break_solution

  # takes O(n) time, 
  #   where n is number of items in current partial solution

  def getChangeSetAdditions(self):

    items = self.getItems()

    break_solution = self._getBreakSolution()

    winnowed_items = [x for x in items if not break_solution.hasItem(x)]

    # print "change set additions:", [x.toString() for x in winnowed_items]

    return winnowed_items

  # takes O(n) time, 
  #   where n is number of items in break solution

  def getChangeSetRemovals(self, additional_partial_solution):

    """

    break_solution = self._getBreakSolution()

    break_solution_items = break_solution.getItems()

    """

    items = additional_partial_solution.getItems()

    # winnowed_items = [x for x in break_solution_items if not self.hasItem(x)]

    winnowed_items = [x for x in items if not self.hasItem(x)]

    # print "change set removals:", [x.toString() for x in winnowed_items]

    return winnowed_items

  # takes O(n + m) time, 
  #   where n is number of items in current partial solution 
  #   and m is number of items in break solution

  def getChangeSet(self, additional_partial_solution):

    change_set_additions = self.getChangeSetAdditions()

    change_set_removals = self.getChangeSetRemovals(additional_partial_solution)

    change_set_items = change_set_additions + change_set_removals

    # print "change set:", [x.toString() for x in change_set_items]

    # raise Exception()

    return change_set_items

  """

  def getAdjustedBreakSolutionParetoPoint(self):

    # retrieve change set, then modify reference (break solution pareto point) accordingly

    change_set_removals = self.getChangeSetRemovals()

    profit_values = [x.getProfit() for x in change_set_removals]

    weight_values = [x.getWeight() for x in change_set_removals]

    change_set_removal_profit = sum(profit_values)

    change_set_removal_weight = sum(weight_values)

    break_solution = self._getBreakSolution()

    break_solution_profit = break_solution.getTotalProfit()

    break_solution_weight = break_solution.getTotalWeight()

    modified_break_solution_profit = break_solution_profit - change_set_removal_profit

    modified_break_solution_weight = break_solution_weight - change_set_removal_weight

    modified_pareto_point = ParetoPoint(modified_break_solution_profit, modified_break_solution_weight)

    return modified_pareto_point

  """

  def getTotalLoss(self, additional_partial_solution):

    """

    items = self.getItems()

    loss_values = [x.getLoss() for x in items]

    total_loss = sum(loss_values)

    return total_loss

    """

    # return self.total_loss

    break_solution = self._getBreakSolution()

    # modified_pareto_point = self.getAdjustedBreakSolutionParetoPoint()

    change_set_items = self.getChangeSet(additional_partial_solution)

    # loss_values = [getLossValue(break_solution, x, modified_pareto_point) for x in change_set_additions]

    split_item = self._getSplitItem()

    split_item_ratio = split_item.getRatio()

    loss_values = [getLossValue(split_item_ratio, x) for x in change_set_items]

    total_loss_value = sum(loss_values)

    # print "total loss value:", total_loss_value

    return total_loss_value

  def getNumItems(self):

    """

    items = self.getItems()

    num_items = len(items)

    return num_items

    """

    return self.item_list.getSize()

  def getEffectiveRatio(self):

    total_profit = self.getTotalProfit()

    total_weight = self.getTotalWeight()

    if self.getNumItems() == 0:

      return None

    else:

      if total_weight == 0:

        return 0

      else:

        effective_ratio = total_profit / (1.0 * total_weight)

        return effective_ratio

  def addItem(self, item):

    """

    items = self.getItems()

    items.append(item)

    """

    node = (self.item_list)._createNode(item, None, None)

    (self.item_list).addLast(node)

    (self.item_to_node_dict)[item] = node

    split_item = self.split_item

    self.total_profit = self.total_profit + item.getProfit()

    self.total_weight = self.total_weight + item.getWeight()

    """

    break_solution = self.break_solution

    have_break_solution = self.break_solution != None

    if have_break_solution == True and break_solution.hasItem(item) == True:

      self.total_loss = self.total_loss + item.getLoss(split_item)

    """

  def toParetoPoint(self):

    pareto_point = ParetoPoint(self.getTotalProfit(), self.getTotalWeight())

    return pareto_point

  # output a string version of a (profit, weight) tuple

  def toString(self):

    pareto_point = self.toParetoPoint()

    profit_weight_tuple = pareto_point.toProfitWeightTuple()

    result = str(profit_weight_tuple)

    return result

  def hasItem(self, item):

    has_item = item in self.item_to_node_dict

    return has_item

class ParetoPoint:

  def __init__(self, profit, weight):

    self.profit = profit

    self.weight = weight

  def getProfit(self):

    return self.profit

  def getWeight(self):

    return self.weight

  def getRatio(self):

    profit = self.getProfit()

    weight = self.getWeight()

    if weight == 0:

      return 0

    else:

      ratio = profit / (1.0 * weight)

      return ratio

  def dominatesParetoPoint(self, pareto_point):

    profit = pareto_point.getProfit()

    weight = pareto_point.getWeight()

    curr_profit = self.getProfit()

    curr_weight = self.getWeight()

    do_dominate = curr_profit > profit and curr_weight <= weight

    return do_dominate

  def toProfitWeightTuple(self):

    profit = self.getProfit()

    weight = self.getWeight()

    result = (profit, weight)

    return result

class Item:

  def __init__(self, profit, weight):

    self.profit = profit

    self.weight = weight

  def getProfit(self):

    return self.profit

  def getWeight(self):

    return self.weight

  def getRatio(self):

    profit = self.getProfit()

    weight = self.getWeight()

    if weight == 0:

      return 0

    else:

      ratio = profit / (1.0 * weight)

      return ratio

  def toParetoPoint(self):

    profit = self.getProfit()

    weight = self.getWeight()

    pareto_point = ParetoPoint(profit, weight)

    return pareto_point

  def getLoss(self, split_item):

    split_item_ratio = split_item.getRatio()

    ratio = self.getRatio()

    weight = self.getWeight()

    signed_loss = (ratio - split_item_ratio) * weight

    loss = abs(signed_loss)

    return loss

  def toString(self):

    pareto_point = self.toParetoPoint()

    profit_weight_tuple = pareto_point.toProfitWeightTuple()

    result = str(profit_weight_tuple)

    return result

import math

"""

# two-subproblem approach

# builds on top of sparse dynamic programming approach

# "list decomposition"

# find highest-profit feasible pair

# consider a list with weight nondecreasing from left to right

# consider a second list with weight nondecreasing from right to left

# break problem into two, find pareto points for each problem, 
#   then find highest-profit pareto point for overall problem

# expect a rough 4x improvement in speed for when values are taken from a uniform distribution

# expect roughly a square-root of the previously required amount of time 
#   if we expect worst-case exponential behavior

# break into two

# solve two subproblems using sparse dynamic programming

# reverse second list of pareto points and consider

"""

def listDecompositionDecompose(problem, split_item):

  # break into two parts based on existing item ordering

  items = problem.getItems()

  num_items = len(items)

  num_items1 = int(math.floor(num_items / 2))

  # num_items1 = num_items

  num_items2 = num_items - num_items1

  items1 = items[0 : num_items1]

  items2 = items[num_items1 : num_items]

  capacity = problem.getCapacity()

  # print "capacity:", capacity

  # print items1, items2

  problem1 = Problem(items1, capacity)

  problem2 = Problem(items2, capacity)

  # print [x.toString() for x in items1]

  # print [x.toString() for x in items2]

  result = (problem1, problem2)

  return result

def listDecompositionSolveIteration(problem1, problem2, integrality_gap_estimate, split_item, break_solution):

  # solve two parts in an alternating fashion

  """

  partial_solutions1 = sparseDPSolve(problem1)

  partial_solutions2 = sparseDPSolve(problem2)

  """

  # print problem1.getItems(), problem2.getItems()

  partial_solutions1 = sparseDPSolveWithLossFilter(problem1, integrality_gap_estimate, split_item, break_solution)

  partial_solutions2 = sparseDPSolveWithLossFilter(problem2, integrality_gap_estimate, split_item, break_solution)

  # print [x.toParetoPoint().toProfitWeightTuple() for x in problem1.getItems()]

  # print [x.toParetoPoint().toProfitWeightTuple() for x in problem2.getItems()]

  # print split_item.toParetoPoint().toProfitWeightTuple()

  # print [x.toParetoPoint().toProfitWeightTuple() for x in break_solution.getItems()]

  # print partial_solutions1, partial_solutions2

  result = (partial_solutions1, partial_solutions2)

  return result

def getWeightForPairOfPartialSolutions(partial_solution_pair):

  partial_solution1, partial_solution2 = partial_solution_pair

  return partial_solution1.getTotalWeight() + partial_solution2.getTotalWeight()

def listDecompositionTwoPartialSolutionCollectionScanBruteForce(left_partial_solutions, right_partial_solutions, capacity, split_item, break_solution):

  # O(n ^ 2) time operation

  pairs = []

  modified_left_partial_solutions = [PartialSolution([], split_item, break_solution)] + left_partial_solutions

  modified_right_partial_solutions = [PartialSolution([], split_item, break_solution)] + right_partial_solutions

  for i in range(len(modified_left_partial_solutions)):

    for j in range(len(modified_right_partial_solutions)):

      curr_left_partial_solution = modified_left_partial_solutions[i]

      curr_right_partial_solution = modified_right_partial_solutions[j]

      curr_pair = (curr_left_partial_solution, curr_right_partial_solution)

      pairs = pairs + [curr_pair]

  winnowed_pairs = [x for x in pairs if ((x[0]).getTotalWeight() + (x[1]).getTotalWeight()) <= capacity]

  # print [getWeightForPairOfPartialSolutions(x) for x in winnowed_pairs], capacity

  profit_values = [((x[0]).getTotalProfit() + (x[1]).getTotalProfit()) for x in winnowed_pairs]

  highest_profit_value = max(profit_values)

  best_pairs = [x for x in winnowed_pairs if ((x[0]).getTotalProfit() + (x[1]).getTotalProfit()) == highest_profit_value]

  partial_solutions = [combinePartialSolutions(x[0], x[1], split_item, break_solution) for x in best_pairs]

  return partial_solutions

# output a list of partial solutions

def listDecompositionTwoPartialSolutionCollectionScan(left_partial_solutions, right_partial_solutions, capacity, split_item, break_solution):

  # first collapse entries on basis of weight, getting best profits for those weights

  # combine based on existing weight-profit-based ordering

  reversed_right_partial_solutions = right_partial_solutions[ : ]

  reversed_right_partial_solutions.reverse()

  # print [x.toString() for x in partial_solutions1]

  # print [x.toString() for x in reversed_partial_solutions2]

  # best_feasible_pairs = LinearTimeLDGetHighestProfitPairs(left_partial_solutions, reversed_right_partial_solutions, capacity, split_item, break_solution)

  # best_feasible_pairs = LinearTimeLDGetHighestProfitPairs(left_partial_solutions, reversed_right_partial_solutions, capacity, split_item, break_solution)

  next_left_partial_solutions = [PartialSolution([], split_item, break_solution)] + left_partial_solutions

  # next_right_partial_solutions = [PartialSolution([], split_item, break_solution)] + right_partial_solutions

  next_right_partial_solutions = reversed_right_partial_solutions + [PartialSolution([], split_item, break_solution)]

  grouped_left_partial_solutions = groupByWeight(next_left_partial_solutions)

  grouped_left_partial_solution_profits = [[x.getTotalProfit() for x in y] for y in grouped_left_partial_solutions]

  left_partial_solution_max_profits = [max(x) for x in grouped_left_partial_solution_profits]

  next_next_left_partial_solutions = []

  for i in range(len(grouped_left_partial_solutions)):

    left_partial_solution_group = grouped_left_partial_solutions[i]

    max_profit = left_partial_solution_max_profits[i]

    candidate_left_partial_solutions = [x for x in left_partial_solution_group if x.getTotalProfit() == max_profit]

    chosen_left_partial_solution = candidate_left_partial_solutions[0]

    next_next_left_partial_solutions = next_next_left_partial_solutions + [chosen_left_partial_solution]

  grouped_right_partial_solutions = groupByWeight(next_right_partial_solutions)

  grouped_right_partial_solution_profits = [[x.getTotalProfit() for x in y] for y in grouped_right_partial_solutions]

  right_partial_solution_max_profits = [max(x) for x in grouped_right_partial_solution_profits]

  next_next_right_partial_solutions = []

  for i in range(len(grouped_right_partial_solutions)):

    right_partial_solution_group = grouped_right_partial_solutions[i]

    max_profit = right_partial_solution_max_profits[i]

    candidate_right_partial_solutions = [x for x in right_partial_solution_group if x.getTotalProfit() == max_profit]

    chosen_right_partial_solution = candidate_right_partial_solutions[0]

    next_next_right_partial_solutions = next_next_right_partial_solutions + [chosen_right_partial_solution]

  # print [x.toString() for x in next_left_partial_solutions]

  # print [x.toString() for x in next_right_partial_solutions]

  best_feasible_pairs = getBestPartialSolutionPairs(next_next_left_partial_solutions, next_next_right_partial_solutions, capacity)

  # print best_feasible_pairs

  partial_solutions = [combinePartialSolutions(x[0], x[1], split_item, break_solution) for x in best_feasible_pairs]

  """

  best_feasible_pair = best_feasible_pairs[0]

  chosen_left_partial_solution = best_feasible_pair[0]

  chosen_right_partial_solution = best_feasible_pair[1]

  print "chosen left partial solution", chosen_left_partial_solution.toString()

  print "chosen right partial solution", chosen_right_partial_solution.toString()

  """

  """

  partial_solution = combinePartialSolutions(chosen_left_partial_solution, chosen_right_partial_solution, split_item, break_solution)

  # raise Exception()

  return partial_solution

  """

  return partial_solutions

# output a list of partial solutions

# solve first subproblem, then second subproblem

# for second subproblem, we periodically scan 
#   partial solution collections of the two subproblems

# at end, we combine

def sparseDPWithLossFilterAndListDecompositionSolveC(problem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution):

  # create solver

  # solve first subproblem

  # solve second subproblem

  # (remember to periodically scan partial solution collections of the two subproblems)

  # note: take into account lengths of lists

  # combine

  capacity = problem.getCapacity()

  solver = None

  problem1, problem2 = listDecompositionDecompose(problem, split_item)

  """

  L_curr1 = [PartialSolution([], split_item, break_solution)]

  L_curr2 = [PartialSolution([], split_item, break_solution)]

  """

  L_curr1 = []

  L_curr2 = []

  solver1 = sparseDPWithImprovedLossFilterSolver(problem1, integrality_gap_estimate, split_item, break_solution, L_curr1)

  solver2 = sparseDPWithImprovedLossFilterSolver(problem2, integrality_gap_estimate, split_item, break_solution, L_curr2)

  partial_solution_list = listDecompositionWithSerialConsiderAndLengthAwareCombineSolve(solver1, solver2, split_item, capacity, integrality_gap_estimate, break_solution, additional_partial_solution)

  return partial_solution_list

# output a list of partial solutions

# solve first subproblem, then second subproblem

# at end, we combine

# alternately extend and combine

def sparseDPWithLossFilterAndListDecompositionSolveB(problem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution):

  # create solver

  # alternately extend and scan

  # combine

  capacity = problem.getCapacity()

  solver = None

  problem1, problem2 = listDecompositionDecompose(problem, split_item)

  """

  L_curr1 = [PartialSolution([], split_item, break_solution)]

  L_curr2 = [PartialSolution([], split_item, break_solution)]

  """

  L_curr1 = []

  L_curr2 = []

  solver1 = sparseDPWithImprovedLossFilterSolver(problem1, integrality_gap_estimate, split_item, break_solution, L_curr1)

  solver2 = sparseDPWithImprovedLossFilterSolver(problem2, integrality_gap_estimate, split_item, break_solution, L_curr2)

  partial_solution_list = listDecompositionWithNonserialConsiderAndAlternatingExtendAndCombineSolve(solver1, solver2, split_item, capacity, integrality_gap_estimate, break_solution, additional_partial_solution)

  return partial_solution_list

# output a list of partial solutions

def sparseDPWithLossFilterAndListDecompositionSolveA(problem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution):

  # create solver

  # solve first subproblem

  # solve second subproblem

  # combine

  """

  items = problem.getItems()

  num_items = len(items)

  """

  capacity = problem.getCapacity()

  solver = None

  problem1, problem2 = listDecompositionDecompose(problem, split_item)

  """

  partial_solutions = sparseDPSolve(problem, integrality_gap_estimate, split_item, break_solution)

  print [x.toString() for x in partial_solutions]

  return partial_solutions[2]

  raise Exception()

  """

  """

  L_curr1 = [PartialSolution([], split_item, break_solution)]

  L_curr2 = [PartialSolution([], split_item, break_solution)]

  """

  L_curr1 = []

  L_curr2 = []

  # print [x.toString() for x in problem1.getItems()]

  # print [x.toString() for x in problem2.getItems()]

  # print [x.toString() for x in problem.getItems()]

  solver1 = sparseDPWithImprovedLossFilterSolver(problem1, integrality_gap_estimate, split_item, break_solution, L_curr1)

  solver2 = sparseDPWithImprovedLossFilterSolver(problem2, integrality_gap_estimate, split_item, break_solution, L_curr2)

  # be careful with arguments

  partial_solution_list = listDecompositionWithSerialConsiderAndFinalCombineSolve(solver1, solver2, split_item, capacity, integrality_gap_estimate, break_solution, additional_partial_solution)

  # print partial_solution.toString()

  return partial_solution_list

  """

  partial_solutions1 = sparseDPSolveWithLossFilter(problem1, integrality_gap_estimate, split_item, break_solution)

  partial_solutions2 = sparseDPSolveWithLossFilter(problem2, integrality_gap_estimate, split_item, break_solution)

  reversed_partial_solutions2 = partial_solutions2[ : ]

  reversed_partial_solutions2.reverse()

  best_feasible_pair = LDGetHighestProfitPair(partial_solutions1, reversed_partial_solutions2, capacity, split_item)

  chosen_partial_solution1 = best_feasible_pair[0]

  chosen_partial_solution2 = best_feasible_pair[1]

  partial_solution = combinePartialSolutions(chosen_partial_solution1, chosen_partial_solution2, split_item)

  return partial_solution

  """

  """

  # print partial_solution.toString()

  return partial_solution

  """

  """

  left_subproblem_num_items = int(math.ceil(num_items / 2.0))

  right_subproblem_num_items = num_items - left_subproblem_num_items

  left_subproblem_items = items[0 : left_subproblem_num_items]

  right_subproblem_items = items[left_subproblem_num_items : num_items]

  left_subproblem = Problem(left_subproblem_items, capacity)

  right_subproblem = Problem(right_subproblem_items, capacity)

  # left_partial_solutions = sparseDPSolve(left_subproblem)

  # right_partial_solutions = sparseDPSolve(right_subproblem)

  left_partial_solutions = sparseDPSolveWithLossFilter(left_subproblem, integrality_gap_estimate, split_item, break_solution)

  right_partial_solutions = sparseDPSolveWithLossFilter(right_subproblem, integrality_gap_estimate, split_item, break_solution)

  reversed_right_partial_solutions = right_partial_solutions[ : ]

  reversed_right_partial_solutions.reverse()

  # print "left partial solutions:", [x.toString() for x in left_partial_solutions]

  # print "reversed right partial solutions:", [x.toString() for x in reversed_right_partial_solutions]

  best_feasible_pair = LDGetHighestProfitPair(left_partial_solutions, reversed_right_partial_solutions, capacity, split_item)

  # print best_feasible_pair

  chosen_left_partial_solution = best_feasible_pair[0]

  chosen_right_partial_solution = best_feasible_pair[1]

  # print "left chosen partial solution:", chosen_left_partial_solution.toString()

  # print "right chosen partial solution:", chosen_right_partial_solution.toString()

  partial_solution = combinePartialSolutions(chosen_left_partial_solution, chosen_right_partial_solution, split_item)

  # print partial_solution.toString()

  return partial_solution

  """

"""

def sparseDPWithLossFilterSolve(problem, integrality_gap_estimate, split_item, break_solution):

  items = problem.getItems()

  num_items = len(items)

  capacity = problem.getCapacity()

  partial_solutions = sparseDPSolveWithLossFilter(problem, integrality_gap_estimate, split_item, break_solution)

  # print partial_solutions

  # partial_solutions = sparseDPSolve(problem)

  highest_profit = getHighestProfit(partial_solutions)

  candidate_partial_solutions = [x for x in partial_solutions if x.getTotalProfit() == highest_profit]

  # print "candidate partial solutions:", candidate_partial_solutions

  chosen_partial_solution = candidate_partial_solutions[0]

  return chosen_partial_solution

"""

def combinePartialSolutions(partial_solution1, partial_solution2, split_item, break_solution):

  items1 = partial_solution1.getItems()

  items2 = partial_solution2.getItems()

  items = items1 + items2

  partial_solution = PartialSolution(items, split_item, break_solution)

  return partial_solution

def combinedPartialSolutionIsFeasible(partial_solution1, partial_solution2, capacity, split_item, break_solution):

  partial_solution = combinePartialSolutions(partial_solution1, partial_solution2, split_item, break_solution)

  weight = partial_solution.getTotalWeight()

  is_feasible = weight <= capacity

  return is_feasible

def getCombinedPartialSolutionProfit(partial_solution1, partial_solution2):

  profit1 = partial_solution1.getTotalProfit()

  profit2 = partial_solution2.getTotalProfit()

  total_profit = profit1 + profit2

  return total_profit

def paretoPointTupleWeightProfitLexicographicComp(x, y):

  p1, w1 = x

  p2, w2 = y

  if w1 < w2:

    return -1

  elif w1 > w2:

    return 1

  elif w1 == w2:

    return comp(p1, p2)

"""

# takes O(n * log(n)) time, where n is total number of left partial solutions and right partial solutions

def LDGetHighestProfitPairs(left_partial_solutions, reversed_right_partial_solutions, capacity, split_item, break_solution):

  # order lexicographically by weight, 
  #   with weight ascending (non-decreasing) 

  # order lexicographically by weight, 
  #   with weight descending (non-increasing)

  # find pareto-point pairs that lead to highest profit

  # then relate pareto-point pairs to partial solution pairs 
  #   by relating pareto points to potentially multiple partial solutions

  right_partial_solutions = reversed_right_partial_solutions[ : ]

  left_solution_dict = Dictionary()

  left_weight_to_max_profit_dict = {}

  right_weight_to_max_profit_dict = {}

  for partial_solution in left_partial_solutions:

    # key = partial_solution.toParetoPoint().toProfitWeightTuple()

    key = partial_solution.getTotalWeight()

    value = partial_solution

    left_solution_dict.insert(key, value)

  right_solution_dict = Dictionary()

  for partial_solution in right_partial_solutions:

    # key = partial_solution.toParetoPoint().toProfitWeightTuple()

    key = partial_solution.getTotalWeight()

    value = partial_solution

    right_solution_dict.insert(key, value)

  left_weight_to_max_profit_dict = {}

  right_weight_to_max_profit_dict = {}

  left_pareto_point_tuples = [x.toParetoPoint().toProfitWeightTuple() for x in left_partial_solutions]

  right_pareto_point_tuples = [x.toParetoPoint().toProfitWeightTuple() for x in right_partial_solutions]

  left_weight_values = [x[1] for x in left_pareto_point_tuples]

  left_distinct_weight_values = list(set(left_weight_values))

  right_weight_values = [x[1] for x in right_pareto_point_tuples]

  right_distinct_weight_values = list(set(right_weight_values))

  for left_weight_value in left_distinct_weight_values:

    profit_values = left_solution_dict[left_weight_value]

    max_profit_value = max(profit_values)

    left_weight_to_max_profit_dict[left_weight_value] = max_profit_value

  for right_weight_value in right_distinct_weight_values:

    profit_values = right_solution_dict[right_weight_value]

    max_profit_value = max(profit_values)

    right_weight_to_max_profit_dict[right_weight_value] = max_profit_value

  sorted_left_pareto_point_tuples = left_pareto_point_tuples[ : ]

  sorted_left_pareto_point_tuples.sort(key = lambda x: x[1])

  sorted_right_pareto_point_tuples = right_pareto_point_tuples[ : ]

  sorted_right_pareto_point_tuples.sort(key = lambda x: x[1])

  reversed_sorted_right_pareto_point_tuples = sorted_right_pareto_point_tuples[ : ]

  reversed_sorted_right_pareto_point_tuples.reverse()

best_pairs = LDGetHighestProfitPairs(left_partial_solutions, reversed_right_partial_solutions, capacity, split_item, break_solution)

best_profit_weight_pair_pairs = [(x[0].toParetoPoint().toProfitWeightTuple(), x[1].toParetoPoint().toProfitWeightTuple()) for x in best_pairs]

for profit_weight_pair_pair in best_profit_weight_pair_pairs:

  left_profit_weight_pair, right_profit_weight_pair = profit_weight_pair_pair

  left_profit, left_weight = left_profit_weight_pair

  right_profit, right_weight = right_profit_weight_pair

  weight_matching_left_partial_solutions = left_

  # perform a linear-time scan to retrieve pareto point pairs

  # for each pareto point pair, perform a join on associated left partial solutions and right partial solutions

"""

# an entry is a (key, value) two-tuple

class Dictionary:

  def __init__(self):

    self.entry_dict = {}

  # return number of entries in D

  # takes O(1) time

  def size(self):

    return len(self.entry_dict)

  # test whether D is empty

  # takes O(1) time

  def isEmpty(self):

    return self.size() == 0

  # if D contains an entry with key equal to k, then return such an entry, else return None

  # takes O(1) expected time

  def find(self, k):

    if k not in (self.entry_dict):

      return None

    else:

      values = (self.entry_dict)[k]

      value = values[0]

    entry = (k, value)

    return entry

  # return an iterable collection contaiing all entries with key equal to k

  # takes O(1 + s) expected time

  def findAll(self, k):

    if k not in (self.entry_dict):

      return []

    else:

      values = (self.entry_dict)[k]

      entries = [(k, x) for x in values]

      return entries

  # insert an entry with key k and value v into D, returning the entry created

  # takes O(1) time

  def insert(self, k, v):

    if k in self.entry_dict:

      (self.entry_dict)[k] = (self.entry_dict)[k] + [v]

    else:

      (self.entry_dict)[k] = [v]

  # remove from D an entry e, returning the removed entry; an error occurs if e is not in D

  # takes O(1 + s) expected time

  def remove(self, e):

    key, value = e

    if key in self.entry_dict:

      (self.entry_dict).remove(value)

    elif key not in self.entry_dict:

      raise Exception("key-value pair not found")

  # return an iterable collection of the key-value entries in D

  # takes O(n) time

  def entries(self):

    entries = []

    for key in (self.entry_dict).keys():

      curr_values = (self.entry_dict)[key]

      curr_entries = [(key, x) for x in curr_values]

      entries = entries + curr_entries

    return entries

"""

# assume that the input partial solutions lists 
#   are ordered using lexicographic ordering 
#   based on weight and profit

"""

# output a list of partial solutions

# left_partial_solutions is sorted so that weight is increasing from left to right; all weight values are unique

# reversed_right_partial_solutions is sorted so that weight is decreasing from left to right; all weight values are unique

# if either of the two lists is empty, we have no pairs to consider

# note: we assume that there is a pair to speak of; that is, both lists are of length >= 1

# note: has errors

# takes O(n + m) time, 
#   where n is number of left partial solutions 
#   and m is number of right partial solutions

# assume input left pareto points are relatively distinct

# assume input right pareto points are relatively distinct

def LinearTimeLDGetHighestProfitParetoPointPairs(left_pareto_points, reversed_right_pareto_points, capacity, split_item, break_solution):

  # print "left partial solutions:", [x.toString() for x in left_partial_solutions]

  # print "reversed right partial solutions:", [x.toString() for x in reversed_right_partial_solutions]

  if len(left_pareto_points) == 0 and len(reversed_right_pareto_points) == 0:

    left_pareto_point = ParetoPoint(0, 0)

    right_pareto_point = ParetoPoint(0, 0)

    pair = (left_pareto_point, right_pareto_point)

    return [pair]

  if len(left_pareto_points) == 0 and len(reversed_right_pareto_points) != 0:

    profit_values = [x.getProfit() for x in reversed_right_pareto_points]

    max_profit_value = max(profit_values)

    candidate_pareto_points = [x for x in reversed_right_pareto_points if x.getProfit() == max_profit_value]

    left_pareto_point = ParetoPoint(0, 0)

    pairs = [(left_pareto_point, x) for x in candidate_pareto_points]

    return pairs

  if len(left_pareto_points) != 0 and len(reversed_right_pareto_points) == 0:

    profit_values = [x.getProfit() for x in left_pareto_points]

    max_profit_value = max(profit_values)

    candidate_pareto_points = [x for x in left_pareto_points if x.getProfit() == max_profit_value]

    right_pareto_point = ParetoPoint(0, 0)

    pairs = [(x, right_pareto_point) for x in candidate_pareto_points]

    return pairs

  elif len(left_pareto_points) != 0 and len(reversed_right_pareto_points) != 0:

    # left_partial_solutions has partial solutions in order of nondecreasing weight

    # reversed_right_partial_solutions has partial solutions in order of nonincreasing weight

    # if sum of weights is less than capacity, take next item from left_partial_solutions

    # if sum of weights is greater than capacity, take next item from reversed_right_partial_solutions

    right_pareto_points = reversed_right_pareto_points

    left_empty_pareto_point = ParetoPoint(0, 0)

    right_empty_pareto_point = ParetoPoint(0, 0)

    """

    next_left_partial_solutions = left_partial_solutions[ : ]

    next_right_partial_solutions = right_partial_solutions[ : ]

    """

    # left_partial_solution = left_partial_solutions[0]

    left_pareto_point = left_empty_pareto_point

    right_pareto_point = right_pareto_points[0]

    next_left_pareto_points = [left_empty_pareto_point] + left_pareto_points[ : ]

    next_right_pareto_points = right_pareto_points[1 : ] + [right_empty_pareto_points]

    best_pairs = []

    best_profit = left_pareto_point[0] + right_pareto_point[0]

    result = LDGetHighestProfitParetoPointPairsHelper(next_left_pareto_points, next_right_pareto_points, left_pareto_point, right_pareto_point, best_profit, best_pairs, split_item, capacity, break_solution)

    return result

def getBestPartialSolutionPairs(left_partial_solutions, right_partial_solutions, capacity):

  left_pareto_points = [x.toParetoPoint().toProfitWeightTuple() for x in left_partial_solutions]

  right_pareto_points = [x.toParetoPoint().toProfitWeightTuple() for x in right_partial_solutions]

  best_pareto_point_pairs = getBestParetoPointPairs(left_pareto_points, right_pareto_points, capacity)

  # print best_pareto_point_pairs

  best_profit_weight_pair_pairs = best_pareto_point_pairs

  left_pareto_point_to_partial_solutions_dict = Dictionary()

  right_pareto_point_to_partial_solutions_dict = Dictionary()

  for left_partial_solution in left_partial_solutions:

    profit_weight_tuple = left_partial_solution.toParetoPoint().toProfitWeightTuple()

    left_pareto_point_to_partial_solutions_dict.insert(profit_weight_tuple, left_partial_solution)

  for right_partial_solution in right_partial_solutions:

    profit_weight_tuple = right_partial_solution.toParetoPoint().toProfitWeightTuple()

    right_pareto_point_to_partial_solutions_dict.insert(profit_weight_tuple, right_partial_solution)

  partial_solution_pairs = []

  for best_profit_weight_pair_pair in best_profit_weight_pair_pairs:

    left_profit_weight_pair, right_profit_weight_pair = best_profit_weight_pair_pair

    left_profit, left_weight = left_profit_weight_pair

    right_profit, right_weight = right_profit_weight_pair

    # print left_profit_weight_pair, right_profit_weight_pair

    left_matching_pair_partial_solution_pairs = left_pareto_point_to_partial_solutions_dict.findAll(left_profit_weight_pair)

    right_matching_pair_partial_solution_pairs = right_pareto_point_to_partial_solutions_dict.findAll(right_profit_weight_pair)

    # print left_matching_pair_partial_solution_pairs, right_matching_pair_partial_solution_pairs

    left_matching_partial_solutions = [x[1] for x in left_matching_pair_partial_solution_pairs]

    right_matching_partial_solutions = [x[1] for x in right_matching_pair_partial_solution_pairs]

    for left_matching_partial_solution in left_matching_partial_solutions:

      for right_matching_partial_solution in right_matching_partial_solutions:

        curr_pair = (left_matching_partial_solution, right_matching_partial_solution)

        # print "current pair:", curr_pair

        partial_solution_pairs = partial_solution_pairs + [curr_pair]

  # print partial_solution_pairs

  return partial_solution_pairs

"""

def toPartialSolutionPairs(pareto_point, pareto_point_to_partial_solutions_dict):

  pass

"""

"""

# output a list of pareto point pairs

# best_profit is best profit from a feasible pair

"""

# for each weight value, 
#   get best profit-weight pairs, 
#   consider whether feasible, 
#   and then possibly record 
#   as a best pair

# takes O(n * log(n)) time

def getBestParetoPointPairs(left_pareto_points, right_pareto_points, capacity):

  # print "left pareto points:", left_pareto_points

  # print "right pareto points:", right_pareto_points

  # get distinct weight values

  # get best profit for each weight value

  # get best pairs

  left_pareto_point_weights = [x[1] for x in left_pareto_points]

  right_pareto_point_weights = [x[1] for x in right_pareto_points]

  """

  distinct_left_pareto_point_weights = list(set(left_pareto_point_weights))

  distinct_right_pareto_point_weights = list(set(right_pareto_point_weights))

  sorted_distinct_left_pareto_point_weights = sorted(distinct_left_pareto_point_weights)

  sorted_distinct_right_pareto_point_weights = sorted(distinct_right_pareto_point_weights)

  """

  left_weight_to_max_profit_dict = {}

  right_weight_to_max_profit_dict = {}

  # print "pareto points:", left_pareto_points, right_pareto_points

  for left_pareto_point in left_pareto_points:

    # print "left pareto point:", left_pareto_point

    curr_profit, curr_weight = left_pareto_point

    next_max_profit = None

    if curr_weight in left_weight_to_max_profit_dict:

      curr_max_profit = left_weight_to_max_profit_dict[curr_weight]

      next_max_profit = max(curr_max_profit, curr_profit)

    else:

      next_max_profit = curr_profit

    left_weight_to_max_profit_dict[curr_weight] = next_max_profit

  # print len(right_pareto_points)

  for right_pareto_point in right_pareto_points:

    # print "right pareto point:", right_pareto_point

    curr_profit, curr_weight = right_pareto_point

    next_max_profit = None

    if curr_weight in right_weight_to_max_profit_dict:

      curr_max_profit = right_weight_to_max_profit_dict[curr_weight]

      next_max_profit = max(curr_max_profit, curr_profit)

    else:

      next_max_profit = curr_profit

    right_weight_to_max_profit_dict[curr_weight] = next_max_profit

  # print left_weight_to_max_profit_dict

  # print right_weight_to_max_profit_dict

  best_left_weight_profit_pairs = left_weight_to_max_profit_dict.items()

  best_right_weight_profit_pairs = right_weight_to_max_profit_dict.items()

  best_left_profit_weight_pairs = [(x[1], x[0]) for x in best_left_weight_profit_pairs]

  best_right_profit_weight_pairs = [(x[1], x[0]) for x in best_right_weight_profit_pairs]

  best_left_pareto_points = best_left_profit_weight_pairs

  best_right_pareto_points = best_right_profit_weight_pairs

  sorted_best_left_pareto_points = sorted(best_left_pareto_points, key = lambda x: x[1])

  sorted_best_right_pareto_points = sorted(best_right_pareto_points, key = lambda x: x[1])

  reversed_sorted_best_right_pareto_points = sorted_best_right_pareto_points[ : ]

  reversed_sorted_best_right_pareto_points.reverse()

  return getBestParetoPointPairsHelper(sorted_best_left_pareto_points, reversed_sorted_best_right_pareto_points, (0, 0), (0, 0), 0, [], capacity)

def getBestParetoPointPairsHelper(sorted_best_left_pareto_points, reversed_sorted_best_right_pareto_points, left_pareto_point, right_pareto_point, best_profit, best_pairs, capacity):

  # print "sorted best left pareto points:", sorted_best_left_pareto_points

  # print "reversed sorted best right pareto points:", reversed_sorted_best_right_pareto_points

  curr_pair = (left_pareto_point, right_pareto_point)

  left_profit, left_weight = left_pareto_point

  right_profit, right_weight = right_pareto_point

  favor_left = None

  next_best_profit = best_profit

  next_best_pairs = best_pairs

  # moving left will lead us to strictly increase overall weight

  # moving right will lead us to strictly decrease overall weight

  if left_weight + right_weight <= capacity:

    # pair is feasible

    # attempt to increase weight for purpose 
    #   of considering more possibilities 
    #   while making the most 
    #   of our right pareto points

    favor_left = True

    pair_profit = left_profit + right_weight

    if pair_profit > best_profit:

      next_best_profit = pair_profit

      next_best_pairs = [curr_pair]

    elif pair_profit == best_profit:

      next_best_pairs = best_pairs + [curr_pair]

  else:

    favor_left = False

  have_left_pareto_points = len(sorted_best_left_pareto_points) != 0

  have_right_pareto_points = len(reversed_sorted_best_right_pareto_points) != 0

  have_both_left_and_right_pareto_points = have_left_pareto_points == True and have_right_pareto_points == True

  have_neither_left_nor_right_pareto_points = have_left_pareto_points == False and have_right_pareto_points == False

  if have_neither_left_nor_right_pareto_points == True:

    return next_best_pairs

  elif (have_left_pareto_points == True and have_right_pareto_points == False) or (have_both_left_and_right_pareto_points == True and favor_left == True):

    next_left_pareto_point = sorted_best_left_pareto_points[0]

    next_right_pareto_point = right_pareto_point

    next_sorted_best_left_pareto_points = sorted_best_left_pareto_points[1 : ]

    next_reversed_sorted_best_right_pareto_points = reversed_sorted_best_right_pareto_points

    return getBestParetoPointPairsHelper(next_sorted_best_left_pareto_points, next_reversed_sorted_best_right_pareto_points, next_left_pareto_point, next_right_pareto_point, next_best_profit, next_best_pairs, capacity)

  elif (have_left_pareto_points == False and have_right_pareto_points == True) or (have_both_left_and_right_pareto_points == True and favor_left == False):

    next_left_pareto_point = left_pareto_point

    next_right_pareto_point = reversed_sorted_best_right_pareto_points[0]

    next_sorted_best_left_pareto_points = sorted_best_left_pareto_points

    next_reversed_sorted_best_right_pareto_points = reversed_sorted_best_right_pareto_points[1 : ]

    return getBestParetoPointPairsHelper(next_sorted_best_left_pareto_points, next_reversed_sorted_best_right_pareto_points, next_left_pareto_point, next_right_pareto_point, next_best_profit, next_best_pairs, capacity)

def LinearTimeLDGetHighestProfitPairsHelper(left_pareto_points, reversed_right_pareto_points, best_seen_left_pareto_point_for_current_weight, best_seen_right_pareto_point_for_current_weight, best_profit, best_pairs, split_item, capacity, break_solution):

  # print [x.toString() for x in left_partial_solutions]

  # print [x.toString() for x in reversed_right_partial_solutions]

  # print left_partial_solution.toString(), right_partial_solution.toString()

  """

  if best_feasible_pair != None:

    print "best feasible pair:", best_feasible_pair[0].toString(), best_feasible_pair[1].toString()

  """

  # if our current pair is feasible, 
  #   moving left means we attempt 
  #   to find a pair that is also feasible 
  #   but that has associated with it 
  #   higher profit

  # if our current pair is not feasible, 
  #   moving right means we attempt 
  #   to find a pair that is feasible

  # make note of a best pair

  curr_pair = (left_pareto_point, right_pareto_point)

  favor_left = None

  next_best_pairs = best_pairs

  next_best_profit = best_profit

  # print left_partial_solution.toString(), right_partial_solution.toString()

  if left_pareto_point[1] + right_pareto_point[1] <= capacity:

    # pair is feasible

    # possibly unseat current best pair

    curr_profit = left_pareto_point[1] + right_pareto_point[1]

    # curr_profit = getCombinedPartialSolutionProfit(left_partial_solution, right_partial_solution)

    # print curr_profit, best_profit

    next_best_profit = max(curr_profit, best_profit)

    if curr_profit > best_profit:

      next_best_pairs = [curr_pair]

    elif curr_profit == best_profit:

      next_best_pairs = best_pairs + [curr_pair]

    # favor left

    favor_left = True

  else:

    # pair is not feasible

    # favor right

    favor_left = False

  have_left_pareto_points = len(left_pareto_points) != 0

  have_right_pareto_points = len(reversed_right_pareto_points) != 0

  have_only_left_pareto_points = have_left_pareto_points and not have_right_pareto_points

  have_only_right_pareto_points = not have_left_pareto_points and have_right_pareto_points

  have_both_left_and_right_pareto_points = have_left_pareto_points and have_right_pareto_points

  finished = not have_left_pareto_points and not have_right_pareto_points

  take_from_left = have_only_right_pareto_points or (have_both_left_and_right_pareto_points and not favor_left)

  take_from_right = have_only_left_pareto_points or (have_both_left_and_right_pareto_points and favor_left)

  if finished == True:

    # no more to consider; 
    #   return current best pair

    return next_best_pairs

  elif have_only_right_pareto_points == True:

    # if favor left, still look to right

    next_right_pareto_points = reversed_right_pareto_points[0]

    return LinearTimeLDGetHighestProfitParetoPointPairsHelper(left_pareto_points, reversed_right_pareto_points[1 : ], left_pareto_points, next_right_pareto_points, next_best_profit, next_best_pairs, split_item, capacity, break_solution)

  elif have_only_left_partial_solutions == True:

    # if favor right, still look to left

    next_left_pareto_points = left_pareto_points[0]

    return LinearTimeLDGetHighestProfitPairsHelper(left_partial_solutions[1 : ], reversed_right_partial_solutions, next_left_partial_solution, right_partial_solution, next_best_profit, next_best_pairs, split_item, capacity, break_solution)

  elif have_both_left_and_right_partial_solutions == True:

    # if favor left, look to left

    # if favor right, look to right

    if favor_left == True:

      next_left_partial_solution = left_partial_solutions[0]

      return LinearTimeLDGetHighestProfitPairsHelper(left_partial_solutions[1 : ], reversed_right_partial_solutions, next_left_partial_solution, right_partial_solution, next_best_profit, next_best_pairs, split_item, capacity, break_solution)

    elif favor_left == False:

      next_right_partial_solution = reversed_right_partial_solutions[0]

      return LinearTimeLDGetHighestProfitPairsHelper(left_partial_solutions, reversed_right_partial_solutions[1 : ], left_partial_solution, next_right_partial_solution, next_best_profit, next_best_pairs, split_item, capacity, break_solution)

# assume that items are sorted to have loss values in non-decreasing order

class sparseDPWithImprovedLossFilterSolver:

  def __init__(self, problem, integrality_gap_estimate, split_item, break_solution, partial_solutions):

    self.problem = problem

    self.integrality_gap_estimate = integrality_gap_estimate

    self.split_item = split_item

    self.break_solution = break_solution

    self.partial_solutions = partial_solutions

    self.items_remaining = problem.getItems()

  def getProblem(self):

    return self.problem

  def getPartialSolutionCollectionSize(self):

    return len(self.partial_solutions)

  def getPartialSolutions(self):

    return self.partial_solutions

  def isFinished(self):

    return len(self.items_remaining) == 0

  def iterate(self, additional_partial_solution):

    problem = self.problem

    integrality_gap_estimate = self.integrality_gap_estimate

    split_item = self.split_item

    break_solution = self.break_solution

    items_remaining = self.items_remaining

    item = items_remaining[0]

    self.items_remaining = items_remaining[1 : ]

    # sparseDPSolveWithLossFilterIterate()

    partial_solutions = self.getPartialSolutions()

    partial_solutions = sparseDPSolveWithImprovedLossFilterIterate(problem, integrality_gap_estimate, split_item, break_solution, item, partial_solutions, additional_partial_solution)

    # partial_solutions = sparseDPSolveWithLossFilterIterate(problem, integrality_gap_estimate, split_item, break_solution, item, partial_solutions)

    self.partial_solutions = partial_solutions

    # print "current partial solutions:", [x.toString() for x in partial_solutions]

  """

  def _updateIntegralityGapEstimate(self, profit_value):

    (self.integrality_gap_estimate).updateProfit(profit_value)

  """

  """

  def scanForOptimalPairInConjunctionWithOtherSolver(self, other_sparse_dp_with_loss_filter_solver):

    partial_solutions1 = self.partial_solution_collection

    partial_solutions2 = other_sparse_dp_with_loss_filter_solver.partial_solution_collection

    partial_solution = listDecompositionTwoPartialSolutionCollectionScan(partial_solutions1, partial_solutions2)

    profit = partial_solution.getProfit()

    self._updateIntegralityGapEstimate(profit)

  """

class sparseDPWithLossFilterSolver:

  def __init__(self, problem, integrality_gap_estimate, split_item, break_solution, partial_solutions):

    self.problem = problem

    self.integrality_gap_estimate = integrality_gap_estimate

    self.split_item = split_item

    self.break_solution = break_solution

    self.partial_solutions = partial_solutions

    self.items_remaining = problem.getItems()

  def getPartialSolutionCollectionSize(self):

    return len(self.partial_solutions)

  def getPartialSolutions(self):

    return self.partial_solutions

  def isFinished(self):

    return len(self.items_remaining) == 0

  def iterate(self):

    partial_solutions = sparseDPSolveWithLossFilterIterate(problem, integrality_gap_estimate, split_item, break_solution, item, partial_solutions, additional_partial_solution)

    self.partial_solutions = partial_solutions

    # sparseDPSolveWithImprovedLossFilterIterate()

  """

  def _updateIntegralityGapEstimate(self, integrality_gap_estimate, profit_value):

    (self.integrality_gap_estimate).updateProfit(profit_value)

  """

  def scanForOptimalPairInConjunctionWithOtherSolver(self, other_sparse_dp_with_loss_filter_solver):

    listDecompositionTwoPartialSolutionCollectionScan()

# involves use of an improved loss filter

# when combined loss for a partial solution 
#   with current item added is too great, 
#   remove the partial solution 
#   for a collection of items 
#   not including the current item, 
#   rather than remove partial solution 
#   for collection of items with the current item, 
#   given that we consider items 
#   in order of increasing loss value

def winnowByRemovingDominatedSolutionsAndByUsingImprovedLossFilter(partial_solutions, break_solution, split_item, integrality_gap_estimate, curr_item, additional_partial_solution):

  # in addition to checking whether partial solutions 
  #   have combined loss values that exceed 
  #   current estimate for integrality gap, 
  #   we remove the partial solution 
  #   without the current item added 
  #   (that does not necessarily yet 
  #   have a combined loss greater than 
  #   current estimate for integrality gap)

  # raise Exception()

  winnowed_partial_solutions = winnowByRemovingDominatedSolutions(partial_solutions, break_solution, split_item, integrality_gap_estimate, additional_partial_solution)

  # loss filter

  highest_profit = getHighestProfit(winnowed_partial_solutions)

  # print integrality_gap_estimate.getValue(), highest_profit

  updateIntegralityGapEstimateBasedOnProfit(integrality_gap_estimate, highest_profit)

  # further_winnowed_partial_solutions = removeParetoPointsWithLargeChangeSetCombinedLoss(winnowed_partial_solutions, split_item, integrality_gap_estimate, break_solution)

  # further_winnowed_partial_solutions = removeParetoPointsWithLargeChangeSetAnticipatedCombinedLoss(further_winnowed_partial_solutions, split_item, integrality_gap_estimate, break_solution, curr_item)

  further_winnowed_partial_solutions = removeParetoPointsWithLargeChangeSetAnticipatedCombinedLoss(winnowed_partial_solutions, split_item, integrality_gap_estimate, break_solution, curr_item, additional_partial_solution)

  # further_winnowed_partial_solutions = winnowed_partial_solutions

  return further_winnowed_partial_solutions

  # return winnowByRemovingDominatedSolutionsAndByUsingLossFilter(partial_solutions, break_solution, split_item)

# return a list of PartialSolution objects

def sparseDPSolveWithImprovedLossFilterIterate(problem, integrality_gap_estimate, split_item, break_solution, item, L_curr, additional_partial_solution):

  item_to_add = item

  W = problem.getCapacity()

  # raise Exception()

  # winnow_method = lambda a, b, c, d, e: winnowByRemovingDominatedSolutionsAndByUsingImprovedLossFilter(a, b, c, d, item, e)

  # winnow_method = lambda a, b, c: a

  winnow_method = lambda a, b, c, d, e: a

  # winnow_method = winnowByRemovingDominatedSolutionsAndByUsingLossFilter

  # winnow_method = winnowByRemovingDominatedSolutions

  result = sparseDPSolveWithWinnowingIterationHelper(item_to_add, integrality_gap_estimate, split_item, W, L_curr, winnow_method, break_solution, additional_partial_solution)

  return result

def sparseDPSolveWithLossFilterIterate(problem, integrality_gap_estimate, split_item, break_solution, item, L_curr, additional_partial_solution):

  # items_to_add = problem.getItems()

  item_to_add = item

  W = problem.getCapacity()

  """

  L_initial = [PartialSolution([], split_item)]

  L_curr = L_initial[ : ]

  """

  # L_curr = partial_solutions

  # winnow_method = lambda x, y, z: x

  winnow_method = winnowByRemovingDominatedSolutionsAndByUsingLossFilter

  # winnow_method = winnowByRemovingDominatedSolutions

  return sparseDPSolveWithWinnowingIterationHelper(item_to_add, integrality_gap_estimate, split_item, W, L_curr, winnow_method, break_solution, additional_partial_solution)

def sparseDPSolve(problem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution):

# def sparseDPSolve(problem, integrality_gap_estimate, split_item, break_solution, item, L_curr):

# def sparseDPSolve(problem, split_item):

  items_to_add = problem.getItems()

  W = problem.getCapacity()

  # print "W:", W

  L_initial = [PartialSolution([], split_item, break_solution)]

  L_curr = L_initial[ : ]

  # winnow_method = lambda x, y, z: x

  winnow_method = winnowByRemovingDominatedSolutions

  # winnow_method = winnowByRemovingDominatedSolutionsAndByUsingLossFilter

  # return sparseDPSolveWithWinnowingHelper(items_to_add, None, None, W, L_curr, winnow_method, None)

  return sparseDPSolveWithWinnowingHelper(items_to_add, integrality_gap_estimate, split_item, W, L_curr, winnow_method, break_solution, additional_partial_solution)

def sparseDPSolveWithWinnowingIterationHelper(item_to_add, integrality_gap_estimate, split_item, W, L_curr, winnow_method, break_solution, additional_partial_solution):

  """

  if len(items_to_add) == 0:

    return L_curr

  else:

  """

  # item = items_to_add[0]

  item = item_to_add

  w_curr = item.getWeight()

  p_curr = item.getProfit()

  original_partial_solutions = L_curr[ : ]

  # print "W:", W

  single_item_partial_solution_addition = [PartialSolution([item], split_item, break_solution)] if w_curr <= W else []

  proposed_additions = [PartialSolution(x.getItems() + [item], split_item, break_solution) for x in L_curr if (x.getTotalWeight() + w_curr) <= W]

  overall_proposed_additions = single_item_partial_solution_addition + proposed_additions

  partial_solutions = mergeOnBasisOfWeightAndProfit(original_partial_solutions, overall_proposed_additions)

  # print [x.toString() for x in partial_solutions]

  winnowed_partial_solutions = winnow_method(partial_solutions, break_solution, split_item, integrality_gap_estimate, additional_partial_solution)

  next_L_curr = winnowed_partial_solutions

  return next_L_curr

# each iteration takes O(n) time

def sparseDPSolveWithWinnowingHelper(items_to_add, integrality_gap_estimate, split_item, W, L_curr, winnow_method, break_solution, additional_partial_solution):

  if len(items_to_add) == 0:

    return L_curr

  else:

    item = items_to_add[0]

    w_curr = item.getWeight()

    p_curr = item.getProfit()

    original_partial_solutions = L_curr[ : ]

    # print "W:", W

    proposed_additions = [PartialSolution(x.getItems() + [item], split_item, break_solution) for x in L_curr if (x.getTotalWeight() + w_curr) <= W]

    partial_solutions = mergeOnBasisOfWeightAndProfit(original_partial_solutions, proposed_additions)

    winnowed_partial_solutions = winnow_method(partial_solutions, break_solution, split_item, integrality_gap_estimate, additional_partial_solution)

    next_L_curr = winnowed_partial_solutions

    return sparseDPSolveWithWinnowingHelper(items_to_add[1 : ], integrality_gap_estimate, split_item, W, next_L_curr, winnow_method, break_solution, additional_partial_solution)

def winnowByRemovingDominatedSolutions(partial_solutions, break_solution, split_item, integrality_gap_estimate, additional_partial_solution):

  grouped_partial_solutions = groupByWeight(partial_solutions)

  nonflat_winnowed_partial_solutions = [removeDominatedParetoPointsGivenThatWeightValuesAreSame(x) for x in grouped_partial_solutions]

  flat_winnowed_partial_solutions = reduce(lambda x, y: x + y, nonflat_winnowed_partial_solutions, [])

  return flat_winnowed_partial_solutions

def winnowByRemovingDominatedSolutionsAndByUsingLossFilter(partial_solutions, break_solution, split_item, integrality_gap_estimate, additional_change_set, additional_partial_solution):

  winnowed_partial_solutions = winnowByRemovingDominatedSolutions(partial_solutions, break_solution, split_item)

  # loss filter

  highest_profit = getHighestProfit(winnowed_partial_solutions)

  # print integrality_gap_estimate.getValue(), highest_profit

  updateIntegralityGapEstimateBasedOnProfit(integrality_gap_estimate, highest_profit)

  further_winnowed_partial_solutions = removeParetoPointsWithLargeChangeSetCombinedLoss(winnowed_partial_solutions, split_item, integrality_gap_estimate, break_solution, additional_partial_solution)

  # further_winnowed_partial_solutions = winnowed_partial_solutions

  return further_winnowed_partial_solutions

# sparse dynamic programming with loss filter

# (sum for partial solution, solution tuple)

def sparseDPSolveWithLossFilter(problem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution):

  items = problem.getItems()

  W = problem.getCapacity()

  n = problem.getNumItems()

  # L_initial = [(0, 0)]

  # list of partial solution objects

  L_initial = [PartialSolution([], split_item, break_solution)]

  L_curr = L_initial[ : ]

  # each iteration takes O(n) time

  for i in range(n):

    # print L_curr

    item = items[i]

    # w_curr = item[0]

    # p_curr = item[1]

    w_curr = item.getWeight()

    p_curr = item.getProfit()

    original_partial_solutions = L_curr[ : ]

    proposed_additions = [PartialSolution(x.getItems() + [item], split_item, break_solution) for x in L_curr if (x.getTotalWeight() + w_curr) <= W]

    # print "original:", [(x.getTotalProfit(), x.getTotalWeight()) for x in original_partial_solutions]

    # print "additions:", [(x.getTotalProfit(), x.getTotalWeight()) for x in proposed_additions]

    # print L_curr

    # L_curr = original_partial_solutions + proposed_additions

    partial_solutions = mergeOnBasisOfWeightAndProfit(original_partial_solutions, proposed_additions)

    # print partial_solutions

    grouped_partial_solutions = groupByWeight(partial_solutions)

    # print grouped_partial_solutions

    nonflat_winnowed_partial_solutions = [removeDominatedParetoPointsGivenThatWeightValuesAreSame(x) for x in grouped_partial_solutions]

    flat_winnowed_partial_solutions = reduce(lambda x, y: x + y, nonflat_winnowed_partial_solutions, [])

    # loss filter

    highest_profit = getHighestProfit(winnowed_partial_solutions)

    updateIntegralityGapEstimateBasedOnProfit(integrality_gap_estimate, highest_profit)

    further_winnowed_partial_solutions = removeParetoPointsWithLargeChangeSetCombinedLoss(flat_winnowed_partial_solutions, split_item, integrality_gap_estimate, break_solution, additional_partial_solution)

    # print "further-winnowed partial solutions:", further_winnowed_partial_solutions

    winnowed_partial_solutions = partial_solutions

    L_curr = winnowed_partial_solutions

    # L_curr = further_winnowed_partial_solutions

    # L_curr = removeDominatedParetoPointsGivenThatWeightValuesAreUnique(winnowed_partial_solutions)

    # have one round of merging and use lexicographic ordering

  # print L_curr

  # print [(x.getTotalProfit(), x.getTotalWeight()) for x in L_curr]

  return L_curr

def canStopExpandingCoreSubproblem(integrality_gap_estimate, item, item_loss_value, core_items):

  # current estimate for integrality gap is surpassed 
  #   by loss value for item that is candidate 
  #   for being used to extend core subproblem

  can_stop_expanding = item_loss_value > integrality_gap_estimate.getValue()

  return can_stop_expanding

def moveItemFromNoncoreSubproblemToCoreSubproblem(core_subproblem, noncore_subproblem, item_with_next_lowest_loss):

  # print "moving item"

  """

  if len(remaining_items_sorted_by_loss_value) == 0:

    raise Exception("no more items left to use for expanding our core subproblem")

  """

  # item_with_next_lowest_loss = remaining_items_sorted_by_loss_value[0]

  # item_with_next_lowest_loss = item

  core_subproblem.addItem(item_with_next_lowest_loss)

  noncore_subproblem.removeItem(item_with_next_lowest_loss)

  """

  next_remaining_items_sorted_by_loss_value = remaining_items_sorted_by_loss_value[1 : ]

  return (next_remaining_items_sorted_by_loss_value, item_with_next_lowest_loss)

  """

  # update estimate

  # update collection of core items

  # compare integrality gap estimate with item loss value

def getItemsInABreakSolutionNotInCoreSubproblem(break_solution, non_core_subproblem):

  items = break_solution.getItems()

  non_core_break_solution_items = []

  # print "break solution whole items:", [x.toParetoPoint().toProfitWeightTuple() for x in items]

  # print "non-core subproblem items:", non_core_subproblem.getItems()

  for item in items:

    if non_core_subproblem.hasItem(item):

      non_core_break_solution_items.append(item)

  return non_core_break_solution_items

# returns a list of partial solutions

def combineOptimalCoreSolutionsWithItemsInABreakSolutionNotInCoreSubproblem(core_partial_solutions, break_solution, non_core_subproblem, split_item):

  result = [combineOptimalCoreSolutionWithItemsInABreakSolutionNotInCoreSubproblem(x, break_solution, non_core_subproblem, split_item) for x in core_partial_solutions]

  return result

# returns a single partial solution

def combineOptimalCoreSolutionWithItemsInABreakSolutionNotInCoreSubproblem(core_partial_solution, break_solution, non_core_subproblem, split_item):

  items_in_break_solution_not_in_core_subproblem = getItemsInABreakSolutionNotInCoreSubproblem(break_solution, non_core_subproblem)

  items_in_optimal_core_solution = core_partial_solution.getItems()

  items = items_in_break_solution_not_in_core_subproblem + items_in_optimal_core_solution

  """

  print items

  print non_core_subproblem.getItems()

  """

  # raise Exception()

  partial_solution = PartialSolution(items, split_item, break_solution)

  return partial_solution

def getInitialCoreSubproblemAndInitialNoncoreSubproblem(items_sorted_by_loss_value, initial_core_subproblem_size, original_problem, break_solution):

  # items = items_sorted_by_loss_value[0 : initial_core_subproblem_size]

  # core_subproblem = Problem(items)

  curr_items_sorted_by_loss_value = items_sorted_by_loss_value

  core_subproblem = Problem([], 0)

  non_core_subproblem = Problem(original_problem.getItems(), original_problem.getCapacity())

  for i in range(initial_core_subproblem_size):

    item = curr_items_sorted_by_loss_value[0]

    # result = moveItemFromNoncoreSubproblemToCoreSubproblem(core_subproblem, non_core_subproblem, item)

    # curr_items_sorted_by_loss_value, moved_item = result

    moveItemFromNoncoreSubproblemToCoreSubproblem(core_subproblem, non_core_subproblem, item)

    curr_items_sorted_by_loss_value = curr_items_sorted_by_loss_value[1 : ]

  remaining_items_sorted_by_loss_value = curr_items_sorted_by_loss_value

  updateCoreAndNonCoreSubproblemCapacities(break_solution, non_core_subproblem, core_subproblem, original_problem)

  return (core_subproblem, non_core_subproblem, remaining_items_sorted_by_loss_value)

def updateCoreAndNonCoreSubproblemCapacities(break_solution, non_core_subproblem, core_subproblem, original_problem):

  core_subproblem_capacity = getCoreSubproblemCapacity(break_solution, non_core_subproblem, original_problem)

  original_problem_capacity = original_problem.getCapacity()

  non_core_subproblem_capacity = original_problem_capacity - core_subproblem_capacity

  core_subproblem.setCapacity(core_subproblem_capacity)

  non_core_subproblem.setCapacity(non_core_subproblem_capacity)

def getCoreSubproblemCapacity(break_solution, non_core_subproblem, original_problem):

  # if items are included for break solution and they are not in non-core subproblem, then we include them for overall solution

  # accordingly, we modify capacity for core subproblem

  items = getItemsInABreakSolutionNotInCoreSubproblem(break_solution, non_core_subproblem)

  weight_values = [x.getWeight() for x in items]

  # print "weight values:", weight_values

  total_weight = sum(weight_values)

  capacity = original_problem.getCapacity()

  remaining_capacity = capacity - total_weight

  # print "remaining capacity:", remaining_capacity

  return remaining_capacity

# return a list

def solveCoreSubproblem(problem, integrality_gap_estimate, core_subproblem, non_core_subproblem, items_sorted_by_loss_value, break_solution, split_item):

  return solveCoreSubproblemHelper(problem, integrality_gap_estimate, core_subproblem, non_core_subproblem, items_sorted_by_loss_value, break_solution, None, split_item)

# return a list

def solveCoreSubproblemHelper(problem, integrality_gap_estimate, core_subproblem, non_core_subproblem, items_sorted_by_loss_value, break_solution, core_subproblem_solution_list, split_item):

  capacity = core_subproblem.getCapacity()

  # print items_sorted_by_loss_value

  """

  num_items_in_non_core_problem = len(non_core_problem.getItems())

  num_items_remaining = len(curr_items_sorted_by_loss_value)

  curr_items_sorted_by_loss_value = remaining_items_sorted_by_loss_value

  """

  # partial_solutions = sparseDPSolve(core_problem)

  # partial_solutions = sparseDPSolveWithLossFilter(core_problem, integrality_gap_estimate, split_item, break_solution)

  additional_items = [x for x in non_core_subproblem.getItems() if break_solution.hasItem(x)]

  additional_partial_solution = PartialSolution(additional_items, split_item, break_solution)

  next_core_subproblem_solution_list = sparseDPWithLossFilterAndListDecompositionSolveC(core_subproblem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution)

  # core_subproblem_solution = sparseDPSolve(core_problem, split_item)

  """

  partial_solutions = sparseDPSolve(core_subproblem, integrality_gap_estimate, split_item, break_solution, additional_partial_solution)

  highest_profit = getHighestProfit(partial_solutions)

  candidate_partial_solutions = [x for x in partial_solutions if x.getTotalProfit() == highest_profit]

  """

  """

  chosen_partial_solution = candidate_partial_solutions[0]

  core_subproblem_solution = chosen_partial_solution

  """

  # next_core_subproblem_solution_list = candidate_partial_solutions

  # assume at least one partial solution exists

  core_subproblem_solution = next_core_subproblem_solution_list[0]

  core_subproblem_profit = core_subproblem_solution.getTotalProfit()

  non_core_items = getItemsInABreakSolutionNotInCoreSubproblem(break_solution, non_core_subproblem)

  non_core_item_profits = [x.getProfit() for x in non_core_items]

  non_core_total_profit = sum(non_core_item_profits)

  p_X = core_subproblem_profit + non_core_total_profit

  # print core_subproblem_profit, non_core_total_profit, p_X

  updateIntegralityGapEstimateBasedOnProfit(integrality_gap_estimate, p_X)

  updateCoreAndNonCoreSubproblemCapacities(break_solution, non_core_subproblem, core_subproblem, problem)

  next_items_sorted_by_loss_value = items_sorted_by_loss_value[1 : ]

  # if len(items_sorted_by_loss_value) == 0:

  if len(items_sorted_by_loss_value) == 0:

    return next_core_subproblem_solution_list

  next_item = items_sorted_by_loss_value[0]

  next_item_loss_value = getLossValue(split_item.getRatio(), next_item)

  # print "gamma estimate:", integrality_gap_estimate.getValue()

  # print "item loss value:", next_item_loss_value

  if canStopExpandingCoreSubproblem(integrality_gap_estimate, next_item, next_item_loss_value, core_subproblem.getItems()) == True:

    return next_core_subproblem_solution_list

  else:

    # print "attempting to expand core subproblem"

    """

    curr_item = items_sorted_by_loss_value[0]

    moveItemFromNoncoreSubproblemToCoreSubproblem(core_problem, non_core_problem, curr_item)

    return solveCoreSubproblemHelper(integrality_gap_estimate, core_subproblem, non_core_subproblem, next_items_sorted_by_loss_value, break_solution, core_subproblem_solution, split_item)

    """

    moveItemFromNoncoreSubproblemToCoreSubproblem(core_subproblem, non_core_subproblem, next_item)

    updateCoreAndNonCoreSubproblemCapacities(break_solution, non_core_subproblem, core_subproblem, problem)

    return solveCoreSubproblemHelper(problem, integrality_gap_estimate, core_subproblem, non_core_subproblem, next_items_sorted_by_loss_value, break_solution, next_core_subproblem_solution_list, split_item)

"""

# return an (item_list, total_profit) tuple

"""

# return a (partial_solution_list, total_profit) tuple

def solve(n, items, W, R_profit, R_weight):

  # raise Exception()

  """
  
    # L_curr = L_curr + proposed_additions
  
    # O(n) approach for removing dominated solutions; 
    #   make sure items are in sorted order by weight, 
    #   and then keep a running record 
    #   of the highest ratio seen so far
  
    # best_weight_ratio_pair = None
  
    best_ratio = None
  
    L_curr_without_dominated_pareto_points = L_curr[ : ]
  
    for i in range(len(L_curr)):
  
    curr_partial_solution = L_curr[i]
  
    curr_ratio = curr_partial_solution.getEffectiveRatio()
  
    if best_ratio == None:
  
      best_ratio = curr_ratio
  
    else:
  
      if curr_ratio <= best_ratio:
  
      L_curr.pop(i)
  
  """
  
  """
  
  we have a main objective - maximize profit
  
  we have a secondary objective - minimize weight
  
  have two pareto points p_a and p_b
  
  p_b dominates p_a if:
  
  (1) p_b.profit > p_a.profit and p_b.weight <= p_a.weight
  (2) p_b.weight < p_a.weight and p_b.profit >= p_a.weight
  
  summarize this by checking for:
  
  p_b.profit >= p_a.profit and p_b.weight <= p_a.weight
  
  """
  
  # assume weights are non-negative
  
  """
  
  given L.i, which is in sorted order using lexicographic ordering
  
  wish to have L.(i + 1), which will be in sorted order using lexicographic ordering
  
  we can obtain L.(i + 1) from L.i using vector addition in O(n) time
  
  """
  
  """
  
  have a single round of merging, which takes O(n) time
  
  """
  
  """
  
  have lexicographic ordering using (weight, ratio) tuple
  
  """
  
  """
  
  scaled profit difference absolute value
  
  minimal total profit difference absolute value
  
  """

  """

  import random
  
  items = []
  
  n = 750
  
  # n = 10 ** 6
  
  R = 2 ** 5 - 1
  
  for i in range(n):
  
    # w_i = int(random.randint(0, R))
  
    w_i = int(random.randint(1, R))
  
    p_i = int(random.randint(0, R))
  
    # item = (w_i, p_i)
  
    item = Item(p_i, w_i)
  
    items.append(item)
  
  """

  """
  
  weight_profit_pairs = [(14, 9), (3, 6), (25, 23), (27, 3), (20, 10), (15, 20), (20, 15), (28, 21), (18, 8), (6, 8)]
  
  for pair in weight_profit_pairs:
  
    weight, profit = pair
  
    item = Item(profit, weight)
  
    items.append(item)

  # weights = [x[0] for x in items]
  
  # values = [x[1] for x in items]
  
  weights = [x.getWeight() for x in items]
  
  values = [x.getProfit() for x in items]
  
  total_weight = sum(weights)
  
  beta = 0.4
  
  W = int(beta * total_weight)

  """
  
  # K = {}
  
  # print "capacity:", W
  
  # sparseDPWithListDecompositionSolve(problem)
  
  """
  
  result = fractionalSolve(items, W)
  
  partial_solution, split_item, split_item_fraction = result
  
  """

  result = linearTimeFractionalSolve(items, W)

  break_solution_items, split_item, split_item_fraction = result

  # print [x.toString() for x in break_solution_items]

  if split_item == None:

    # all items fit

    item_list = break_solution_items

    profit_values = [x.getProfit() for x in break_solution_items]

    total_profit = sum(profit_values)

    # item_list_list = [item_list]

    # result = (item_list_list, total_profit)

    # result = (item_list, total_profit)

    break_solution = PartialSolution(break_solution_items, split_item, None)

    partial_solution_list = [break_solution]

    result = (partial_solution_list, total_profit)

    return result

  # print "split item:", split_item.toString()

  partial_solution = PartialSolution(break_solution_items, split_item, None)

  split_item_fraction = split_item.getRatio()
  
  # print partial_solution.toString(), split_item, split_item_fraction
  
  # raise Exception()
  
  profit_weight_tuple = toFractionalSolutionProfitWeightTuple(partial_solution, split_item, split_item_fraction)
  
  # print profit_weight_tuple
  
  """
  
  # from fractional solution, we have split item and break solution partial solution
  
  # have core subproblem and non-core subproblem
  
  # have two problems
  
  # find solution to fractional version
  
  """
  
  # print "hello"
  
  """
  
  # break the break solution into two parts - core and non-core
  
  # if we have a valid core, use in conjunction with non-core choices and form a solution for whole problem
  
  """
  
  break_solution_partial_solution = partial_solution
  
  optimal_fractional_solution_profit_weight_tuple = profit_weight_tuple
  
  optimal_fractional_solution_profit = optimal_fractional_solution_profit_weight_tuple[0]
  
  best_optimal_integral_solution_profit = 0
  
  integrality_gap_estimate = IntegralityGapEstimate(optimal_fractional_solution_profit, best_optimal_integral_solution_profit)
  
  items_sorted_by_loss_value = items[ : ]
  
  items_sorted_by_loss_value.sort(key = lambda x: getLossValue(split_item.getRatio(), x))

  problem = Problem(items_sorted_by_loss_value, W)
  
  profit_weight_tuples = [x.toParetoPoint().toProfitWeightTuple() for x in items]
  
  # print "items:", profit_weight_tuples
  
  # initial_core_size = int(math.floor(math.log(problem.getNumItems(), 2)))
  
  # initial_core_size = int(math.floor((math.log(n, 10) ** 2) * 2.244 * (7.64 / 2.0)))
  
  # initial_core_size = min(int(math.ceil((math.log(n, 2) ** 2) * (67.5 / 397.26))), n)
  
  # initial_core_size = min(int(math.ceil((math.log(n, 10) ** 2) * 10.5 / 4.67)), n)
  
  # loss_value_d = 0.057159628
  
  # loss_value_d = 1.690095017
  
  # loss_value_d = 0.000014124
  
  # loss_value_d = 1.689085623
  
  # based on two data points from beier and voecking
  
  gamma_est = 0.730079606 * ((math.log(n, math.e)) ** 2) / (1.0 * n) + 0.000013577
  
  gamma_scaled_est = gamma_est * R_profit

  # core_size_est = 2 * gamma_scaled_est * n
  
  loss_value_d = gamma_scaled_est
  
  # print "initial cut-off loss value for core:", loss_value_d

  """
  
  for x in items_sorted_by_loss_value:
  
    print getLossValue(split_item.getRatio(), x)

  """

  initial_core_items = [x for x in items_sorted_by_loss_value if getLossValue(split_item.getRatio(), x) <= loss_value_d]
  
  initial_core_size = len(initial_core_items)
  
  # initial_core_size = problem.getNumItems()
  
  # print "initial core size:", initial_core_size
  
  # print [(x.toParetoPoint().toProfitWeightTuple(), getLossValue(split_item.getRatio(), x)) for x in items_sorted_by_loss_value]
  
  # print integrality_gap_estimate.getValue()
  
  """
  
  partial_solutions = sparseDPSolve(problem)
  
  """
  
  # partial_solution = sparseDPWithLossFilterSolve(problem, integrality_gap_estimate, split_item, break_solution_partial_solution)
  
  # partial_solutions = sparseDPSolveWithLossFilter(problem, integrality_gap_estimate, split_item, break_solution_partial_solution)
  
  """
  
  pareto_points = [x.toParetoPoint() for x in partial_solutions]
  
  profit_weight_tuples = [x.toProfitWeightTuple() for x in pareto_points]
  
  print profit_weight_tuples
  
  profit_values = [x.getTotalProfit() for x in partial_solutions]
  
  highest_profit_value = max(profit_values)
  
  candidate_partial_solutions = [x for x in partial_solutions if x.getTotalProfit() == highest_profit_value]
  
  chosen_partial_solution = candidate_partial_solutions[0]
  
  print chosen_partial_solution.toParetoPoint().toProfitWeightTuple()
  
  print "items:", [x.toParetoPoint().toProfitWeightTuple() for x in chosen_partial_solution.getItems()]
  
  """
  
  """
  
  # print partial_solution.toParetoPoint().toProfitWeightTuple()
  
  highest_profit = getHighestProfit(partial_solutions)
  
  candidate_partial_solutions = [x for x in partial_solutions if x.getTotalProfit() == highest_profit]
  
  chosen_partial_solution = candidate_partial_solutions[0]
  
  # print "number of items:", chosen_partial_solution.getNumItems()
  
  # print "solution items:", [x.toParetoPoint().toProfitWeightTuple() for x in chosen_partial_solution.getItems()]
  
  print chosen_partial_solution.toParetoPoint().toProfitWeightTuple()
  
  """
  
  # remaining_items_sorted_by_loss_value is sorted to have loss nondecreasing from left to right
  
  # modify existing core subproblem, non-core subproblem
  
  """
  
  # return a (remaining_items_sorted_by_loss_value, item_with_next_lowest_loss) tuple
  
  # remaining_items_sorted_by_loss_value is a collection 
  #   of items that have not yet been used for core subproblem, 
  #   sorted to have loss nondecreasing from left to right
  
  # item_with_next_lowest_loss is item that we move
  
  """
  
  # def moveItemFromNoncoreSubproblemToCoreSubproblem(remaining_items_sorted_by_loss_value, core_subproblem, noncore_subproblem, item_with_next_lowest_loss):
  
  # have initial core subproblem
  
  # repeatedly solve and expand until do not have to expand
  
  # combine solution with that of break solution
  
  # have overall solution
  
  """
  
  # have a dynamic core
  
  # re-determine the items that constitute core and non-core problems
  
  # disqualify on basis of loss value
  
  """

  core_problem, non_core_problem, remaining_items_sorted_by_loss_value = getInitialCoreSubproblemAndInitialNoncoreSubproblem(items_sorted_by_loss_value, initial_core_size, problem, break_solution_partial_solution)
  
  # print core_problem.getCapacity(), non_core_problem.getCapacity()
  
  # print [x.toParetoPoint().toProfitWeightTuple() for x in core_problem.getItems()]
  
  # print [x.toParetoPoint().toProfitWeightTuple() for x in non_core_problem.getItems()]
  
  # print [x.toParetoPoint().toProfitWeightTuple() for x in break_solution_partial_solution.getItems()]
  
  # print getCoreSubproblemCapacity(break_solution_partial_solution, non_core_problem, problem)
  
  """
  
  item = remaining_items_sorted_by_loss_value[0]
  
  item_loss_value = getLossValue(split_item.getRatio(), item)
  
  """
  
  core_items = core_problem.getItems()
  
  # print integrality_gap_estimate.getValue(), item_loss_value
  
  # print canStopExpandingCoreSubproblem(integrality_gap_estimate, item, item_loss_value, core_items)
  
  """
  
  curr_item = curr_items_sorted_by_loss_value[0]
  
  curr_item_loss_value = getLossValue(split_item.getRatio(), curr_item)
  
  """
  
  core_subproblem_solution = None
  
  """
  
  while canStopExpandingCoreSubproblem(integrality_gap_estimate, curr_item, curr_item_loss_value, core_problem.getItems()) == False and len(curr_items_sorted_by_loss_value) != 0:
  
    # print "attempting to expand"
  
    curr_item = curr_items_sorted_by_loss_value[0]
  
    curr_item_loss_value = getLossValue(split_item.getRatio(), curr_item)
  
    # move one item
  
    num_items_in_non_core_problem = len(non_core_problem.getItems())
  
    num_items_remaining = len(curr_items_sorted_by_loss_value)
  
    # print num_items_in_non_core_problem
  
    # print num_items_remaining
  
    moveItemFromNoncoreSubproblemToCoreSubproblem(core_problem, non_core_problem, curr_item)
  
    # result = moveItemFromNoncoreSubproblemToCoreSubproblem(core_problem, non_core_problem, curr_item)
  
    # curr_items_sorted_by_loss_value, moved_item = result
  
    # core_subproblem_solution = sparseDPWithLossFilterAndListDecompositionSolve(core_problem, integrality_gap_estimate, split_item, break_solution_partial_solution)
  
    # core_subproblem_profit = core_subproblem_solution.getTotalProfit()
  
    partial_solutions = sparseDPSolve(core_problem)
  
    highest_profit = getHighestProfit(partial_solutions)
  
    candidate_partial_solutions = [x for x in partial_solutions if x.getTotalProfit() == highest_profit]
  
    chosen_partial_solution = candidate_partial_solutions[0]
  
    core_subproblem_solution = chosen_partial_solution
  
    # core_subproblem_solution = sparseDPWithLossFilterSolve(core_problem, integrality_gap_estimate, split_item, break_solution_partial_solution)
  
    core_subproblem_profit = core_subproblem_solution.getTotalProfit()
  
    non_core_items = getItemsInABreakSolutionNotInCoreSubproblem(break_solution_partial_solution, non_core_problem)
  
    non_core_item_profits = [x.getProfit() for x in non_core_items]
  
    non_core_total_profit = sum(non_core_item_profits)
  
    p_X = core_subproblem_profit + non_core_total_profit
  
    updateIntegralityGapEstimateBasedOnProfit(integrality_gap_estimate, p_X)
  
    # integrality_gap_estimate.updateBestIntegralSolutionProfit(p_X)
  
    updateCoreAndNonCoreSubproblemCapacities(break_solution_partial_solution, non_core_problem, core_problem, problem)
  
    curr_items_sorted_by_loss_value = curr_items_sorted_by_loss_value[1 : ]
  
    # print "gamma estimate:", integrality_gap_estimate.getValue()
  
    # print "current item loss value:", curr_item_loss_value
  
    # curr_item = curr_items_sorted_by_loss_value[0]
  
    # curr_item_loss_value = getLossValue(split_item.getRatio(), curr_item)
  
    # solve core subproblem
  
    # update estimate for integrality gap
  
    # remove one item from collection of items 
    #   that we could introduce to core subproblem
  
    """

  core_subproblem_solution_list = solveCoreSubproblem(problem, integrality_gap_estimate, core_problem, non_core_problem, remaining_items_sorted_by_loss_value, break_solution_partial_solution, split_item)

  partial_solution_list = combineOptimalCoreSolutionsWithItemsInABreakSolutionNotInCoreSubproblem(core_subproblem_solution_list, break_solution_partial_solution, non_core_problem, split_item)

  """

  print core_subproblem_solution.getItems()

  print core_problem.getItems()

  print core_problem.getCapacity()

  """

  # raise Exception()

  # print "number of items:", partial_solution.getNumItems()
  
  # print partial_solution
  
  # print "solution items:", [x.toParetoPoint().toProfitWeightTuple() for x in partial_solution.getItems()]
  
  # print partial_solution.toString()
  
  """
  
  # combined distance
  
  # compare distances of items to ray for a partial solution to estimate for integrality gap
  
  # update estimate for integrality gap
  
  """
  
  """
  
  # update integrality gap before checking if combined loss values for partial solutions are too large
  
  """

  """

  # partial_solution is our optimal solution for integer version of problem

  item_list = partial_solution.getItems()

  total_profit = partial_solution.getTotalProfit()

  result = (item_list, total_profit)

  return result

  """

  # assume at least one partial solution exists

  # print items_sorted_by_loss_value

  partial_solution = partial_solution_list[0]

  total_profit = partial_solution.getTotalProfit()

  result = (partial_solution_list, total_profit)

  # raise Exception()

  return result

"""

import random
  
items = []
  
n = 750

# n = 10 ** 6
  
R = 2 ** 5 - 1
  
for i in range(n):
  
  # w_i = int(random.randint(0, R))
  
  w_i = int(random.randint(1, R))
  
  p_i = int(random.randint(0, R))
  
  # item = (w_i, p_i)
  
  item = Item(p_i, w_i)
  
  items.append(item)

  # weights = [x[0] for x in items]
  
  # values = [x[1] for x in items]
  
  weights = [x.getWeight() for x in items]
  
  values = [x.getProfit() for x in items]
  
  total_weight = sum(weights)
  
  beta = 0.4
  
  W = int(beta * total_weight)

"""

# solve(n, items, W, R, R)

"""

items = [Item(399, 1), Item(799, 2), Item(1199, 3), Item(1999, 5)]

n = 4

W = 6

R_profit = 1999

R_weight = 5

result = solve(n, items, W, R_profit, R_weight)

# item_collection, total_profit = result

# print [(x.getProfit(), x.getWeight()) for x in item_collection]

item_list_list, total_profit = result

# raise Exception()

print [(x.getTotalProfit(), x.getTotalWeight()) for x in item_list_list]

print total_profit

"""

"""

# use core-based knapsack algo. to solve feed optimizer problem

# based on approach described by beier and voecking

# obtain results involving minimal number of items by transforming problem

# have many roughly independent problems

# prepare output

# have events for purpose of introducing and removing items

# retrieve items responsible for an optimal solution 
#   to integer version of knapsack problem

# parse input

"""

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

    def peek(self):

      heap = self.heap

      pair = heap[0]

      item = pair[1]

      return item

# up to 10,000 instructions

# have profits that are up to one million

# have weights that are up to 2,000

# have fixed size for sack - a value that is at most 2,000

# have fixed item life-time size - a value that is at most 2,000

# re-use items

"""

n_instr = 9

n_max = 10

W = 100

import knapsack

item1 = knapsack.Item(50, 30)

item2 = knapsack.Item(40, 20)

item3 = knapsack.Item(45, 40)

item4 = knapsack.Item(45, 20)

# R1: 1

# R2: 1, 2, 3

# R3: 1, 2, 3

# R4: 1, 2, 3, 4

# R5: 2, 3, 4

p_max = 50

R_profit = p_max

w_max = 40

R_weight = w_max

id_to_item_dict = {}

item_to_id_dict = {}

id_to_item_dict[1] = item1

id_to_item_dict[2] = item2

id_to_item_dict[3] = item3

id_to_item_dict[4] = item4

item_to_id_dict[item1] = 1

item_to_id_dict[item2] = 2

item_to_id_dict[item3] = 3

item_to_id_dict[item4] = 4

items1 = [item1]

items2 = [item1, item2, item3]

items3 = [item1, item2, item3]

items4 = [item1, item2, item3, item4]

items5 = [item2, item3, item4]

item_list, total_profit = knapsack.solve(1, items1, W, R_profit, R_weight)

profit_weight_pairs = [x.toParetoPoint().toProfitWeightTuple() for x in item_list]

# print profit_weight_pairs, total_profit

item_identifier_values = [item_to_id_dict[x] for x in item_list]

sorted_item_identifier_values = item_identifier_values[ : ]

sorted_item_identifier_values.sort()

num_items = len(item_list)

# print total_profit, num_items, sorted_item_identifier_values

item_list, total_profit = knapsack.solve(3, items2, W, R_profit, R_weight)

profit_weight_pairs = [x.toParetoPoint().toProfitWeightTuple() for x in item_list]

# print profit_weight_pairs, total_profit

item_identifier_values = [item_to_id_dict[x] for x in item_list]

sorted_item_identifier_values = item_identifier_values[ : ]

sorted_item_identifier_values.sort()

num_items = len(item_list)

# print total_profit, num_items, sorted_item_identifier_values

item_list, total_profit = knapsack.solve(3, items3, W, R_profit, R_weight)

profit_weight_pairs = [x.toParetoPoint().toProfitWeightTuple() for x in item_list]

# print profit_weight_pairs, total_profit

item_identifier_values = [item_to_id_dict[x] for x in item_list]

sorted_item_identifier_values = item_identifier_values[ : ]

sorted_item_identifier_values.sort()

num_items = len(item_list)

# print total_profit, num_items, sorted_item_identifier_values

item_list, total_profit = knapsack.solve(4, items4, W, R_profit, R_weight)

profit_weight_pairs = [x.toParetoPoint().toProfitWeightTuple() for x in item_list]

# print profit_weight_pairs, total_profit

item_identifier_values = [item_to_id_dict[x] for x in item_list]

sorted_item_identifier_values = item_identifier_values[ : ]

sorted_item_identifier_values.sort()

num_items = len(item_list)

# print total_profit, num_items, sorted_item_identifier_values

item_list, total_profit = knapsack.solve(3, items5, W, R_profit, R_weight)

profit_weight_pairs = [x.toParetoPoint().toProfitWeightTuple() for x in item_list]

# print profit_weight_pairs, total_profit

item_identifier_values = [item_to_id_dict[x] for x in item_list]

sorted_item_identifier_values = item_identifier_values[ : ]

sorted_item_identifier_values.sort()

num_items = len(item_list)

# print total_profit, num_items, sorted_item_identifier_values

"""

"""

# transform problem to take into account size of solution in terms of items

# multiply profits by # of items for problem, subtract by one

"""

"""

# transform problem to take into account lexicographic-order-based value for solution

# multiply profits by max. identifier value for problem, subtract by particular items' identifier values

"""

"""

# transform problem to take into account lexicographic-order-based value for solution

# aim is to give preference to most significant bits for a value corresponding to item collection

# multiply each profit by a power of two

# deal with exact arithmetic

"""

"""

# transform result to counter-act changes to profits for purpose of taking into account size of solution in terms of items

# find actual total profit through use of items' actual profit values

# or, we add to profit # of items for solution, divide by # of items for problem

# transform result to counter-act changes to profits for purpose of taking into account lexicographic-order-based value for solution

# find actual total profit through use of items' actual profit values

# or, we add to profit each item's identifier value and divide by max. identifier value for problem

"""

# bound on scale factor is # of items for problem

# returns a problem

# Problem object has associated with it Item objects

def transformForMinimizingSolutionSize(problem):

  # return problem

  # multiply profits by # of items for problem, subtract by one

  items = problem.getItems()

  capacity = problem._getSackCapacity()

  next_items = []

  num_items = len(items)

  for i in range(num_items):

    curr_item = items[i]

    curr_profit = curr_item.getProfit()

    weight = curr_item.getWeight()

    id_value = curr_item.getIDValue()

    next_profit = curr_profit * num_items - 1

    # print "cardinality-related transform profits:", curr_profit, next_profit

    # print curr_profit, next_profit

    curr_next_item = FeedItem(next_profit, weight, id_value)

    next_items = next_items + [curr_next_item]

  next_problem = FeedProblem(next_items, capacity)

  return next_problem

# bound on scale factor is two raised to max. identifier value

# returns a problem

# Problem object has associated with it Item objects

def transformForMinimizingSolutionIdentifierCollectionLexicographicOrderBasedValue(problem):

  # return problem

  """

  # multiply profits by max. identifier value for problem, subtract by particular items' identifier values

  """

  """

  # multiply each profit by max. power of two 
  #   based on numerical identifier value 
  #   and subtract based on current 
  #   numerical identifier value 
  #   and max. identifier value

  """

  # multiply each profit by a power of two 
  #   involving max. identifier value, 
  #   then a power of two involving 
  #   the quantity max. identifier value 
  #   minus current identifier value

  # favor having items with low value towards left (at more significant bits)

  """

  # take sum of first n powers of two 
  #   (using indexing starting at one) 
  #   multiplied by max. numerical 
  #   identifier value for an item 
  #   and subtract by a profit value 
  #   multiplied a power of two based on 
  #   numerical identifier value

  """

  items = problem.getItems()

  capacity = problem._getSackCapacity()

  next_items = []

  num_items = len(items)

  if num_items == 0:

    return problem

  identifier_values = [x.getIDValue() for x in items]

  max_identifier_value = max(identifier_values)

  """

  # let n be max_identifier_value minus one

  n = max_identifier_value - 1

  first_n_integers = range(0, n)

  first_n_powers_of_two = [(long(2) ** x) for x in first_n_integers]

  sum_of_first_n_powers_of_two = sum(first_n_powers_of_two)

  print n, first_n_integers, first_n_powers_of_two, sum_of_first_n_powers_of_two

  """

  """

  if num_items == 0:

    return problem

  """

  profit_values = [x.getProfit() for x in items]

  max_profit_value = max(profit_values)

  for i in range(num_items):

    curr_item = items[i]

    curr_profit = curr_item.getProfit()

    weight = curr_item.getWeight()

    id_value = curr_item.getIDValue()

    # next_profit = curr_profit * max_identifier_value - id_value

    # assume numerical identifier values start at one

    # next_profit = (max_profit_value - 1.0 * curr_profit) * (2 ** (max_identifier_value - 1.0 * id_value))

    # next_profit = (curr_profit * (2 ** max_identifier_value)) - (max_identifier_value - 1.0 * id_value)

    # next_profit = (curr_profit * (2 ** max_identifier_value)) + 2 ** max_identifier_value - 2 ** id_value

    next_profit = (curr_profit * (2 ** (max_identifier_value + 1))) + 2 ** id_value

    # print "lexicography-related transform profits:", curr_profit, next_profit

    # next_profit = (sum_of_first_n_powers_of_two * max_identifier_value) - curr_profit * (2 ** (id_value - 1.0))

    curr_next_item = FeedItem(next_profit, weight, id_value)

    next_items = next_items + [curr_next_item]

  next_problem = FeedProblem(next_items, capacity)

  return next_problem

# returns an (item_collection, total_profit) tuple

# modifies properties of existing items; 
#   does not create new objects

# items returned are Item objects

def untransformSolutionForProblemTransformedForMinimizingSolutionSize(original_problem, problem, item_collection, total_profit):

  # return (item_collection, total_profit)

  # modify each problem's profit value by adding a value to it and then dividing by a particular value

  """

  next_item_collection = item_collection

  next_total_profit = total_profit

  result = (next_item_collection, next_total_profit)

  return result

  """

  """

  print [x.getProfit() for x in problem.getItems()]

  print [x.getWeight() for x in problem.getItems()]

  print problem._getSackCapacity()

  print total_profit

  """

  items = problem.getItems()

  num_items = len(items)

  next_item_collection = []

  """

  if num_items == 0:

    result = (item_collection, total_profit)

    return result

  identifier_values = [x.getIDValue() for x in items]

  max_identifier_value = max(identifier_values)

  """

  for item in item_collection:

    profit = item.getProfit()

    weight = item.getWeight()

    id_value = item.getIDValue()

    next_profit = (profit + 1) / (1.0 * num_items)

    # print "cardinality-related un-transform profits:", profit, next_profit

    next_item = FeedItem(next_profit, weight, id_value)

    next_item_collection = next_item_collection + [next_item]

  next_profit_values = [x.getProfit() for x in next_item_collection]

  next_total_profit = sum(next_profit_values)

  result = (next_item_collection, next_total_profit)

  return result

# returns an (item_collection, total_profit) tuple

# items returned are Item objects

def untransformSolutionForProblemTransformedForMinimizingSolutionIdentifierCollectionLexicographicOrderBasedValue(original_problem, problem, item_collection, total_profit):

  # return (item_collection, total_profit)

  """

  # modify each problem's profit value by adding a value to it and then dividing by a particular value

  """

  # modify each problem's profit value 
  #   by dividing it by a power of two 
  #   based on numerical identifer value 
  #   and max. profit value for an item

  """

  # take each profit value, 
  #   subtract by product of sum 
  #   of first n powers of two 
  #   and max. numerical identifier 
  #   value for an item, 
  #   and divide by negated value 
  #   of a power of two based 
  #   on numerical identifier value

  """

  """

  next_item_collection = item_collection

  next_total_profit = total_profit

  result = (next_item_collection, next_total_profit)

  return result

  """

  items = problem.getItems()

  num_items = len(items)

  if num_items == 0:

    result = (item_collection, total_profit)

    return result

  identifier_values = [x.getIDValue() for x in items]

  max_identifier_value = max(identifier_values)

  """

  # let n be max_identifier_value minus one

  n = max_identifier_value - 1

  first_n_integers = range(0, n)

  first_n_powers_of_two = [(long(2) ** x) for x in first_n_integers]

  sum_of_first_n_powers_of_two = sum(first_n_powers_of_two)

  """

  next_item_collection = []

  """

  next_item_collection = []

  if num_items == 0:

    return problem

  """

  profit_values = [x.getProfit() for x in original_problem.getItems()]

  max_profit_value = max(profit_values)

  for item in item_collection:

    profit = item.getProfit()

    weight = item.getWeight()

    id_value = item.getIDValue()

    # assume numerical identifier values start at one

    # next_profit = -1.0 * ((profit / (2 ** (id_value - 1.0))) - max_profit_value)

    # next_profit = (profit - (sum_of_first_n_powers_of_two * max_identifier_value)) / (-1.0 * (2 ** (id_value - 1.0)))

    # next_profit = -1.0 * ((profit / (2 ** (max_identifier_value - id_value))) - max_profit_value)

    # next_profit = (profit + (max_identifier_value - 1.0 * id_value)) / (2 ** max_identifier_value)

    next_profit = (profit - 2 ** id_value) / (2 ** (max_identifier_value + 1))

    # print "lexicography-related un-transform profits:", profit, next_profit

    # print item_collection

    # raise Exception()

    # next_profit = (curr_profit * (2 ** max_identifier_value)) - (max_identifier_value - 1.0 * id_value)

    # next_profit = profit + (2 ** (id_value - 1.0))

    # next_profit = (profit + 1) / (1.0 * num_items)

    next_item = FeedItem(next_profit, weight, id_value)

    next_item_collection = next_item_collection + [next_item]

  next_profit_values = [x.getProfit() for x in next_item_collection]

  next_total_profit = sum(next_profit_values)

  result = (next_item_collection, next_total_profit)

  return result

# output a list of item lists

# takes O(n) time, 
#   where n is number of pareto points

def winnowOnBasisOfCardinality(item_list_list):

  # print [[x.getIDValue() for x in y] for y in item_list_list]

  item_list_sizes = [len(x) for x in item_list_list]

  min_item_list_size = min(item_list_sizes)

  winnowed_item_list_sizes = [x for x in item_list_list if len(x) == min_item_list_size]

  return winnowed_item_list_sizes

# takes O(m * n) time, 
#   where m is number of sack item list lists 
#   and n is max. size of a sack item list

def fromSackItemListListToItemListList(sack_item_list_list, sack_item_to_item_dict):

  item_list_lists = []

  for sack_item_list in sack_item_list_list:

    item_list_list = [sack_item_to_item_dict[x] for x in sack_item_list]

    item_list_lists = item_list_lists + [item_list_list]

  return item_list_lists

# assume a void goes before an identifier value

# assume item lists are sorted to have identifier values be in increasing order

# takes O(n) time, where n is the max. size of an item list in terms of items

def itemListIdentifierBasedLexicographicComp(x, y):

  return itemListIdentifierBasedLexicographicCompHelper(x, y)

def comp(x, y):

  if x < y:

    return -1

  elif x > y:

    return 1

  elif x == y:

    return 0

def itemListIdentifierBasedLexicographicCompHelper(x, y):

  # print x, y

  if len(x) == 0 and len(y) == 0:

    return 0

  elif len(x) == 0 and len(y) != 0:

    return -1

  elif len(x) != 0 and len(y) == 0:

    return 1

  elif len(x) != 0 and len(y) != 0:

    x_item = x[0]

    y_item = y[0]

    # print x_item, y_item

    # print x_item.getIDValue(), y_item.getIDValue()

    comparison = comp(x_item.getIDValue(), y_item.getIDValue())

    # print x_item.getIDValue(), y_item.getIDValue()

    # print comparison

    if comparison == 0:

      x_identifiers = x[1 : ]

      y_identifiers = y[1 : ]

      # print x_identifiers, y_identifiers

      return itemListIdentifierBasedLexicographicCompHelper(x_identifiers, y_identifiers)

    else:

      return comparison

# output a single item list list

# takes O(n ^ 2 * log(n)) time, 
#   where n is number of pareto points

def winnowOnBasisOfLexicography(item_list_list):

  # print [[x.getIDValue() for x in y] for y in item_list_list]

  sorted_item_list_list = item_list_list[ : ]

  sorted_item_list_list.sort(cmp = lambda x, y: itemListIdentifierBasedLexicographicCompHelper(x, y))

  chosen_item_list = sorted_item_list_list[0]

  result = [chosen_item_list]

  return result

class Event:

  def __init__(self, time):

    self.time = time

  def getTime(self):

    return self.time

class ItemEvent(Event):

  def __init__(self, time, item):

    Event.__init__(self, time)

    self.item = item

  def getItem(self):

    return self.item

class ItemTimeSpanningEvent(ItemEvent):

  def __init__(self, time, item):

    ItemEvent.__init__(self, time, item)

  def toString(self):

    item = self.getItem()

    time = self.getTime()

    profit = item.getProfit()

    weight = item.getWeight()

    id_value = item.getIDValue()

    result = string.join(["item time-spanning event:", str(time), str(profit), str(weight), str(id_value)], " ")

    return result

class SolveEvent(Event):

  def __init__(self, time, sack_capacity):

    Event.__init__(self, time)

    self.sack_capacity = sack_capacity

  def _getSackCapacity(self):

    return self.sack_capacity

  def toString(self):

    time = self.getTime()

    result = string.join(["solve event:", str(time)], " ")

    return result

  # item_collection is a dictionary of (id, item) tuples

  def handle(self, item_collection):

    # have a solver, feed to it our item collection, 
    #   take result and prepare for using said result as output

    items = item_collection.values()

    sack_capacity = self._getSackCapacity()

    problem = FeedProblem(items, sack_capacity)

    # result = ([], 0)

    """

    next_problem = transformForMinimizingSolutionSize(problem)

    next_next_problem = next_problem

    """

    """

    next_problem = transformForMinimizingSolutionSize(problem)

    # next_next_problem = next_problem

    next_next_problem = transformForMinimizingSolutionIdentifierCollectionLexicographicOrderBasedValue(next_problem)

    # print [(x.getProfit(), x.getWeight()) for x in next_next_problem.getItems()]

    # don't expect result to involve same Item objects

    result = next_next_problem.solve()

    item_list, total_profit = result

    next_result = untransformSolutionForProblemTransformedForMinimizingSolutionIdentifierCollectionLexicographicOrderBasedValue(next_problem, next_next_problem, item_list, total_profit)

    # next_result = result

    next_item_list, next_total_profit = next_result

    next_next_result = untransformSolutionForProblemTransformedForMinimizingSolutionSize(problem, next_problem, next_item_list, next_total_profit)

    # next_next_result = untransformSolutionForProblemTransformedForMinimizingSolutionIdentifierCollectionLexicographicOrderBasedValue(problem, next_problem, next_item_list, next_total_profit)

    next_next_item_list, next_next_total_profit = next_next_result

    sorted_item_list = next_next_item_list[ : ]

    """

    result = problem.solve()

    item_list_list, total_profit = result

    # sort the item lists in our list

    for item_list in item_list_list:

      item_list.sort(key = lambda x: x.getIDValue())

    # post-process to account for cardinality

    # post-process to account for lexicography

    winnowed_item_list_list = winnowOnBasisOfCardinality(item_list_list)

    chosen_item_list_list = winnowOnBasisOfLexicography(winnowed_item_list_list)

    # assume a solution exists

    # item_list = item_list_list[0]

    item_list = chosen_item_list_list[0]

    # sorted_item_list = item_list[ : ]

    # print sorted_item_list

    # sorted_item_list.sort(key = lambda x: x.getIDValue())

    sorted_item_list = item_list[ : ]

    num_solution_items = len(item_list)

    sorted_item_list_strings = [str(x.getIDValue()) for x in sorted_item_list]

    overall_sorted_item_list_string = string.join(sorted_item_list_strings, " ")

    # print total_profit, num_solution_items, overall_sorted_item_list_string

    # integer version of a total profit value un-transformed twice

    """

    modified_next_next_total_profit = int(next_next_total_profit)

    print modified_next_next_total_profit, num_solution_items, overall_sorted_item_list_string

    """

    # print item_list, total_profit

    modified_total_profit = int(total_profit)

    print modified_total_profit, num_solution_items, overall_sorted_item_list_string

class ItemIntroduceEvent(ItemEvent):

  def __init__(self, time, item):

    ItemEvent.__init__(self, time, item)

  def toString(self):

    item = self.getItem()

    id_value = item.getIDValue()

    result = string.join(["item introduce event:", str(id_value)], " ")

    return result

  # item_collection is a dictionary of (id, item) tuples

  def handle(self, item_collection):

    # add an item to our collection

    item = self.getItem()

    id_value = item.getIDValue()

    item_collection[id_value] = item

    # print item_collection

class ItemExpireEvent(ItemEvent):

  def __init__(self, time, item):

    ItemEvent.__init__(self, time, item)

  def toString(self):

    item = self.getItem()

    id_value = item.getIDValue()

    result = string.join(["item expire event:", str(id_value)], " ")

    return result

  # item_collection is a dictionary of (id, item) tuples

  def handle(self, item_collection):

    # remove an item from our collection

    item = self.getItem()

    id_value = item.getIDValue()

    item_collection.pop(id_value)

class FeedItem:

  def __init__(self, profit, weight, id_value):

    self.profit = profit

    self.weight = weight

    self.id_value = id_value

  def getProfit(self):

    return self.profit

  def getWeight(self):

    return self.weight

  def getIDValue(self):

    return self.id_value

"""

class Solution:

  def __init__(self, time, items):

    self.time = time

    self.items = items

  def getTime(self):

    return self.time

  def getItems(self):

    return self.items

"""

# problem takes into account tie-breaking 
#   based on # of items in solution 
#   and further tie-breaking 
#   based on lexicographic ordering 
#   relating to item identifier values

class FeedProblem:

  def __init__(self, items, sack_capacity):

    self.items = items

    self.sack_capacity = sack_capacity

  def getItems(self):

    return self.items

  def _getSackCapacity(self):

    return self.sack_capacity

  # items is a list of Item objects

  @staticmethod

  def _getMaxItemProfit(items):

    profit_values = [x.getProfit() for x in items]

    if len(profit_values) == 0:

      return None

    else:

      max_profit_value = max(profit_values)

      return max_profit_value

  # items is a list of Item objects

  @staticmethod

  def _getMaxItemWeight(items):

    weight_values = [x.getWeight() for x in items]

    if len(weight_values) == 0:

      return None

    else:

      max_weight_value = max(weight_values)

      return max_weight_value

  # item_collection is a dictionary of (id, item) tuples

  # returns a (item_collection, total_profit) tuple

  # the items provided are Item objects

  # do not expect that the items returned 
  #   are in the form of pre-existing objects

  def solve(self):

    items = self.getItems()

    W = self._getSackCapacity()

    R_profit = FeedProblem._getMaxItemProfit(items)

    R_weight = FeedProblem._getMaxItemWeight(items)

    n = len(items)

    sack_items = [Item(x.getProfit(), x.getWeight()) for x in items]

    sack_item_to_item_dict = {}

    for i in range(len(items)):

      curr_sack_item = sack_items[i]

      curr_item = items[i]

      sack_item_to_item_dict[curr_sack_item] = curr_item

    result = solve(n, sack_items, W, R_profit, R_weight)

    """

    sack_item_collection_list, total_profit = result

    item_list = [sack_item_to_item_dict[x] for x in sack_item_list]

    """

    sack_item_partial_solution_list, total_profit = result

    sack_item_list_list = [x.getItems() for x in sack_item_partial_solution_list]

    item_list_list = [[sack_item_to_item_dict[x] for x in y] for y in sack_item_list_list]

    """

    overall_result = (item_list, total_profit)

    return overall_result

    """

    overall_result = (item_list_list, total_profit)

    return overall_result

import sys

import string

# import cdecimal

# stream = open("tests/test1.in")

# stream = open("tests/test2.in")

# stream = open("tests/test3.in")

# stream = open("tests/test4.in")

# stream = open("tests/test8.in")

# stream = open("tests/test12.in")

# print n_instr, n_max, W

item1 = FeedItem(50, 30, 1)

item2 = FeedItem(40, 20, 2)

item3 = FeedItem(45, 40, 3)

item4 = FeedItem(45, 20, 4)

curr_item_collection = {1 : item1, 2 : item2, 3 : item3, 4 : item4}

solve_event = SolveEvent(None, 100)

solve_event.handle(curr_item_collection)
