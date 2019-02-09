# 2019-02-04

# LCA algorithm from bender and farach-colton

# we have n items, overall pre-processing time is in O(n), query time is in O(1)

# we are inspired by jakob kogler, rodion gorkovenko, mariia mykhailova, who translated an implementation from a russian service maintained by ivanov maxim

# graph must be a tree -- otherwise, we have infinite loop -- we do allow, however, symmetric adjacency (i.e. for each undirected edge its endpoints can have the other in their adjacency list -- in other words, we allow each undirected edge to appear twice overall in our adjacency lists)

# edges are assumed to be undirected

# this is an adjacency list format, not adjacency matrix format

# also, we must make sure adjacency lists reference nodes that exist

# there are c++ esoterica regarding what happens when one references a vector outside of bounds or reserving and resizing

from collections import defaultdict

class LCA_BFC:

  def __init__(self, n, adj):

    self.n = n
    self.adj = adj

    self.block_size = None
    self.block_cnt = None
    self.first_visit = None
    self.euler_tour = None
    self.height = None
    self.log_2 = None
    self.st = None
    self.blocks = None
    self.block_mask = None

  def dfs(self, v, p, h):
    # print self.first_visit, v, self.euler_tour
    self.first_visit[v] = len(self.euler_tour)
    self.euler_tour.append(v)
    self.height[v] = h
    for u in self.adj[v]:
      # print v, p, h, u
      if u == p:
        continue
      self.dfs(u, v, h + 1)
      self.euler_tour.append(v)

  def min_by_h(self, i, j):
    return i if self.height[self.euler_tour[i]] < self.height[self.euler_tour[j]] else j

  def precompute_lca(self, root):

    # reserves from c++ can be omitted when we use python; 
    # capacity is different from size as the latter counts actual items; 
    # single-argument vector constructor adds that many actual items with unspecified value

    n = self.n

    # get euler tour and indices of first occurrences
    self.first_visit = defaultdict(lambda: 0)
    for i in xrange(n):
      self.first_visit[i] = -1
    self.height = defaultdict(lambda: 0)
    for i in xrange(n):
      self.height[i] = 0
    self.euler_tour = []
    self.dfs(root, -1, 0)

    # pre-compute all log values
    m = len(self.euler_tour)
    self.log_2 = []
    self.log_2.append(-1)
    for i in xrange(1, m + 1):
      self.log_2.append(self.log_2[i / 2] + 1)
    self.block_size = max(1, self.log_2[m] / 2)
    self.block_cnt = (m + self.block_size - 1) / self.block_size

    # pre-compute min. of each block and build sparse table; 
    # integer vectors automatically initialize using zero
    self.st = []
    for i in xrange(self.block_cnt):
      self.st.append([0] * (self.log_2[self.block_cnt] + 1))
    b = 0
    j = 0
    for i in xrange(m):
      if (j == self.block_size):
        j = 0
        b += 1
      if (j == 0 or self.min_by_h(i, self.st[b][0]) == i):
        self.st[b][0] = i
      j += 1
    for l in xrange(1, self.log_2[self.block_cnt] + 1):
      for i in xrange(self.block_cnt):
        ni = i + (1 << (l - 1))
        if (ni >= self.block_cnt):
          self.st[i][l] = self.st[i][l - 1]
        else:
          # print self.st, i, l
          self.st[i][l] = self.min_by_h(self.st[i][l - 1], self.st[ni][l - 1])

    # pre-compute mask for each block
    self.block_mask = [0] * self.block_cnt
    b = 0
    j = 0
    for i in xrange(0, m):
      if (j == self.block_size):
        j = 0
        b += 1
      if (j > 0 and (i >= m or self.min_by_h(i - 1, i) == i - 1)):
        self.block_mask[b] += 1 << (j - 1)
      j += 1

    # pre-compute RMQ for each unique block
    # possibilities = 1 << (self.block_size - 1)
    self.blocks = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    for b in xrange(0, self.block_cnt):
      mask = self.block_mask[b]
      # print self.blocks, mask, b
      if len(self.blocks[mask]) != 0:
        continue
      # print self.blocks[mask]
      # self.blocks[mask] = []
      for i in xrange(self.block_size):
        curr_value = [0] * self.block_size
        # print self.blocks[0]
        self.blocks[mask][i] = curr_value
      for l in xrange(self.block_size):
        self.blocks[mask][l][l] = l
        for r in xrange(l + 1, self.block_size):
          self.blocks[mask][l][r] = self.blocks[mask][l][r - 1]
          if (b * self.block_size + r < m):
            self.blocks[mask][l][r] = self.min_by_h(b * self.block_size + self.blocks[mask][l][r], \
                                          b * self.block_size + r) - b * self.block_size

  def lca_in_block(self, b, l, r):
    return self.blocks[self.block_mask[b]][l][r] + b * self.block_size

  def lca(self, v, u):
    l = self.first_visit[v]
    r = self.first_visit[u]
    if (l > r):
      v1 = l
      v2 = r
      l = v2
      r = v1
    bl = l / self.block_size
    br = r / self.block_size
    if (bl == br):
      return self.euler_tour[self.lca_in_block(bl, l % self.block_size, r % self.block_size)]
    ans1 = self.lca_in_block(bl, l % self.block_size, self.block_size - 1)
    ans2 = self.lca_in_block(br, 0, r % self.block_size)
    ans = self.min_by_h(ans1, ans2)
    if (bl + 1 < br):
      l = self.log_2[br - bl - 1]
      ans3 = self.st[bl + 1][l]
      ans4 = self.st[br - (1 << l)][l]
      ans = self.min_by_h(ans, self.min_by_h(ans3, ans4))
    return self.euler_tour[ans]

"""

n = 3

adj = defaultdict(lambda: [])
adj[0] = [1]
adj[1] = [0, 2]
adj[2] = [1]

lca_bfc = LCA_BFC(n, adj)

lca_bfc.precompute_lca(1)

print lca_bfc.lca(0, 0)

"""

"""

n = 7
adj = defaultdict(lambda: [])
adj[0] = [1, 2, 3]
adj[1] = [0, 4, 5]
adj[2] = [0]
adj[3] = [0, 6]
adj[4] = [1]
adj[5] = [1]
adj[6] = [3]

lca_bfc = LCA_BFC(n, adj)

lca_bfc.precompute_lca(0)

print lca_bfc.lca(3, 1)

print lca_bfc.lca(4, 5)

print lca_bfc.lca(3, 6)

print lca_bfc.lca(4, 2)

print lca_bfc.lca(1, 6)

print lca_bfc.lca(4, 1)

print lca_bfc.lca(2, 2)

"""

"""

n = 6
adj = defaultdict(lambda: [])
adj[0] = [1, 2]
adj[1] = [0, 4]
adj[2] = [0, 3]
adj[3] = [2, 5]
adj[4] = [1]
adj[5] = [3]

lca_bfc = LCA_BFC(n, adj)

lca_bfc.precompute_lca(0)

# should be zero
print lca_bfc.lca(1, 2)

# should be two
print lca_bfc.lca(2, 5)

"""


