class Matrix2x2:

  # row 0: a, b

  # row 1: c, d

  def __init__(self, a, b, c, d):

    self.m = [[a, b], [c, d]]

  def getDeterminant(self):

    row0 = (self.m)[0]

    row1 = (self.m)[1]

    a = float(row0[0])

    b = float(row0[1])

    c = float(row1[0])

    d = float(row1[1])

    det = a * d - b * c

    return det

  def getInverse(self):

    row0 = (self.m)[0]

    row1 = (self.m)[1]

    # print row0, row1

    a = float(row0[0])

    b = float(row0[1])

    c = float(row1[0])

    d = float(row1[1])

    # print a, b, c, d

    det = self.getDeterminant()

    # print det

    a_r = (1.0 * d) / det

    # print d, det, a_r

    b_r = (-1.0 * b) / det

    c_r = (-1.0 * c) / det

    d_r = (1.0 * a) / det

    m = Matrix2x2(a_r, b_r, c_r, d_r)

    return m

  def getA(self):

    return (self.m)[0][0]

  def getB(self):

    return (self.m)[0][1]

  def getC(self):

    return (self.m)[1][0]

  def getD(self):

    return (self.m)[1][1]

