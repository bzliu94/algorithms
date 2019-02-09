# 2019-02-04

# SCC algorithm from kosaraju and sharir

# we have n nodes and m edges, overall time is O(n + m)

# we are inspired by dmitry dobrynin, rodion gorkovenko, joaquin g. cabrera, chirag agarwal, mariia mykhailova, anton algmyr, rahul goswami, jakob kogler, prakhar gupta, shadab zafar, chaman agrawal, who helped translate implementation from a russian service maintained by ivanov maxim

# we expect reverse topological ordering

from collections import defaultdict

class SCC_KS:

  def __init__(self, n, adj):

    self.n = n
    self.adj = adj

    self.g = defaultdict(lambda: [])
    self.gr = defaultdict(lambda: [])
    self.used = defaultdict(lambda: False)
    self.order = []
    self.component = []

  def dfs1(self, v):
    self.used[v] = True
    for i in xrange(len(self.g[v])):
      if self.used[self.g[v][i]] == False:
        self.dfs1(self.g[v][i])
    self.order.append(v)

  def dfs2(self, v):
    self.used[v] = True
    self.component.append(v)
    for i in xrange(len(self.gr[v])):
      if self.used[self.gr[v][i]] == False:
        self.dfs2(self.gr[v][i])

  def scc(self):
    n = self.n

    adj = self.adj
    for i in xrange(len(adj)):
      a = i
      for j in xrange(len(adj[i])):
        b = adj[i][j]
        self.g[a].append(b)
        self.gr[b].append(a)

    # print "g:", self.g
    # print "gr:", self.gr

    self.used = [False] * n
    for i in xrange(n):
      if self.used[i] != True:
        self.dfs1(i)
    self.used = [False] * n
    for i in xrange(n):
      v = self.order[n - 1 - i]
      if self.used[v] != True:
        self.dfs2(v)
        print self.component
        self.component = []

# print scc(0, [[]])

"""

n = 8

adj = defaultdict(lambda: [])
adj[0] = [1]
adj[1] = [2]
adj[2] = [0]
adj[3] = [1, 2, 4]
adj[4] = [3, 5]
adj[5] = [2, 6]
adj[6] = [5]
adj[7] = [4, 6, 7]

scc_ks = SCC_KS(n, adj)

scc_ks.scc()

# expected results (with zero-indexing):
# component #1: 0, 1, 2
# component #2: 5, 6
# component #3: 3, 4
# component #4: 7

# expected result is the above, but reversed

"""


