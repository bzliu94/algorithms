def drawCircleEvent(draw, left_arc, arc, right_arc, l_y, color_triple):

  location = CircleEvent.getIntersectionHelper(l_y, left_arc, arc, right_arc)

  radius = CircleEvent.distanceFromBisectorIntersectionToContributingSite(l_y, left_arc, arc, right_arc)

  # print "radius:", radius

  (x, y) = location

  canvas_x = x

  canvas_y = im.size[1] - y

  canvas_pair = (canvas_x, canvas_y)

  ul = (canvas_x - radius, canvas_y - radius)

  br = (canvas_x + radius, canvas_y + radius)

  # draw.ellipse([ul, br], outline = color_triple, fill = color_triple)

  draw.ellipse([ul, br], outline = color_triple)

  left_arc_focus = left_arc.getFocus()

  arc_focus = arc.getFocus()

  right_arc_focus = right_arc.getFocus()

  segment1 = (left_arc_focus, arc_focus)

  segment2 = (arc_focus, right_arc_focus)

  plotLineSegments(draw, [segment1, segment2], (0, 0, 255))

# rgba_value is a four-tuple

def highlightSiteForArc(draw, arc, color_triple):

  focus = arc.getFocus()

  pair = focus

  (x, y) = pair

  canvas_x = x

  canvas_y = im.size[1] - y

  ul = (canvas_x - 4, canvas_y - 4)

  br = (canvas_x + 4, canvas_y + 4)

  # draw.ellipse([ul, br], outline = color_triple, fill = color_triple)

  draw.ellipse([ul, br], outline = color_triple)

def plotPoints(draw, points, color_triple):

  for i in range(len(points)):

    pair = points[i]

    (x, y) = pair

    canvas_x = x

    canvas_y = im.size[1] - y

    canvas_pair = (canvas_x, canvas_y)

    # print canvas_pair

    # im.putpixel(canvas_pair, (0, 0, 0))

    ul = (canvas_x - 2, canvas_y - 2)

    br = (canvas_x + 2, canvas_y + 2)

    # draw.ellipse([ul, br], outline = (0, 0, 0), fill = (0, 0, 0))

    draw.ellipse([ul, br], outline = color_triple, fill = color_triple)

def plotLineSegments(draw, segments, color_triple):

  segment_pairs = segments

  for i in range(len(segment_pairs)):

    curr_segment_pair = segment_pairs[i]

    start_pair, end_pair = curr_segment_pair

    (x1, y1) = start_pair

    (x2, y2) = end_pair

    x1_canvas, y1_canvas = x1, im.size[1] - y1

    x2_canvas, y2_canvas = x2, im.size[1] - y2

    start_canvas_pair = (x1_canvas, y1_canvas)

    end_canvas_pair = (x2_canvas, y2_canvas)

    # draw.line([start_canvas_pair, end_canvas_pair], fill = (0, 0, 0), width = 1)

    draw.line([start_canvas_pair, end_canvas_pair], fill = color_triple, width = 1)

import time

time1 = time.clock()

# for event queue, we are using a priority queue

# we may have site events and circle events with same priority

from core.fortune.SweepLine import *

from core.fortune.arc_tree.ArcTree import *

# from core.priority_queue.PriorityQueue import *

from core.priority_queue.EventQueue import *

from core.fortune.TruncatedBisectorEdgeDict import *

from core.fortune.events.SiteEvent import *

def getPriorityForYValue(y_value):

  return -1 * y_value

def getYValueForPriority(priority):

  return -1 * priority

# planar straight-line graph

# vertices have distinct locations

# edges do not cross

class Subdivision:

  def __init__(self):

    pass
    
"""

class Graph:

  def __init__(self):

    pass

class Edge:

  def __init__(self):

    pass

  def getEndpoints(self):

    pass

class Vertex:

  def __init__(self):

    pass

  def getLocation(self):

    pass

  def setLocation(self, location):

    pass

class SweepLine:

  def __init__(self):

    pass
    
"""

# input: a set of n points

# output: a dcel with n bounded faces

# running time: O(n * log(n))

# note: points must have distinct locations

# diagram = Order_1_voronoi_diagram([(0, 0), (0, 1), (0, 2), (0, 3)])

"""

subdivision = diagram.get_subdivision()

print subdivision

# event_queue = PriorityQueue()

event_queue = EventQueue()

sweep_line = SweepLine()

arc_tree = ArcTree(sweep_line)

"""

sweep_line = SweepLine()

tree = ArcTree(3, sweep_line)

vertex_list = []

# event_queue = PriorityQueue()

event_queue = EventQueue()

truncated_bisector_edge_dict = TruncatedBisectorEdgeDict()

# create voronoi diagram

# 1. process events

# 2. apply bounding box

# 3. retrieve cells

# point_list = [(0, 0), (0, 1), (0, 2), (0, 3)]

# point_list = [(0, 0), (1, 1), (0, 2)]

# point_list = [(0, 4), (1, 1), (2, 3)]

import random

point_set = set([])

# while len(point_set) < 500:

# while len(point_set) < 1000:

# while len(point_set) < 1024:

# while len(point_set) < 10000:

while len(point_set) < 1000:

  # print len(point_set)

  """

  x = random.randint(0, 512)

  y = random.randint(0, 512)

  """

  """

  x = random.randint(128, 384)

  y = random.randint(128, 384)

  """

  """

  x = random.randint(128, 896)

  y = random.randint(128, 384)

  """

  """

  x = random.randint(128, 896)

  y = random.randint(128, 896)

  """

  """

  x = random.uniform(128, 896)

  y = random.uniform(128, 896)

  """

  """

  x = random.uniform(128, 2944)

  y = random.uniform(128, 2944)

  """

  x = random.randint(128, 396)

  y = random.randint(128, 396)

  """

  x = random.random() * 100

  y = random.random() * 100

  """

  location = (x, y)

  # print location

  point_set = point_set | set([location])

point_list = list(point_set)

# this collection of points could lead to jumping event priority values

# point_list = [(100, 200), (200, 400), (300, 200), (400, 400), (500, 200)]

# point_list = [(200, 400), (300, 200), (400, 400)]

# point_list = [(100, 200), (200, 400), (300, 200), (400, 400)]

# point_list = [(100, 200), (200, 400), (300, 200), (400, 400)]

# point_list = [(200, 400), (300, 250), (400, 400)]

# point_list = [(300, 200), (400, 200), (500, 200), (400, 100)]

# point_list = [(300, 200), (400, 200), (400, 100)]

# point_list = [(400, 200), (500, 200), (400, 100)]

# point_list = [(97, 96), (47, 93), (67, 93), (76, 88), (34, 91)]

# point_list = [(10, 62), (30, 79), (60, 48), (39, 27), (16, 64), (84, 92), (93, 4), (44, 73), (61, 68), (38, 69)]

# point_list = [(336, 177), (298, 366), (307, 268), (242, 156), (299, 366), (314, 203), (370, 203)]

# point_list = [(136, 177), (298, 366), (307, 268)]

# point_list = [(359, 228), (179, 172), (291, 179), (170, 314), (178, 163), (305, 155), (230, 271)]

# point_list = [(234, 383), (297, 320), (181, 218), (363, 159), (344, 251), (247, 226), (228, 249), (284, 241), (358, 154), (152, 383)]

# point_list = [(263, 308), (146, 169), (227, 193), (216, 264), (220, 379), (326, 246), (129, 170), (175, 302), (154, 354), (323, 164), (181, 301), (366, 182), (169, 160), (131, 173), (292, 334), (322, 161), (356, 272), (130, 291), (295, 380), (296, 133), (261, 351), (291, 365), (372, 213), (236, 172), (160, 333), (286, 200), (363, 378), (183, 149), (252, 353), (297, 273), (325, 182), (155, 137), (362, 380), (200, 239), (248, 233), (341, 345), (250, 270), (144, 159), (163, 374), (178, 130), (215, 182), (173, 368), (305, 184), (277, 319), (156, 366), (230, 374), (221, 334), (308, 242), (236, 316), (343, 376)]

# point_list = [(336, 198), (270, 330), (250, 219), (298, 324), (321, 346), (273, 382), (223, 143), (365, 335), (309, 382), (358, 340), (220, 303), (251, 225), (332, 382), (356, 323), (192, 228), (290, 275), (265, 300), (266, 162), (356, 253), (200, 131), (129, 153), (204, 200), (327, 158), (128, 240), (383, 280), (225, 382), (304, 282), (372, 313), (187, 219), (297, 143), (317, 156), (254, 317), (134, 128), (286, 266), (321, 182), (183, 364), (222, 326), (271, 187), (376, 128), (333, 301), (255, 237), (192, 244), (321, 301), (273, 331), (264, 136), (145, 185), (197, 177), (287, 190), (168, 368), (358, 312)]

# point_list = [(449, 226), (574, 161), (428, 268), (643, 205), (816, 233), (524, 186), (648, 128), (665, 230), (691, 258), (207, 138), (760, 346), (754, 144), (499, 290), (680, 274), (256, 233), (650, 189), (779, 349), (287, 255), (871, 361), (166, 231), (864, 206), (583, 326), (720, 132), (691, 209), (545, 273), (162, 202), (450, 333), (577, 166), (488, 263), (774, 284), (840, 283), (471, 141), (497, 369), (218, 313), (432, 289), (701, 307), (456, 353), (869, 146), (280, 218), (519, 135), (352, 203), (680, 157), (155, 318), (217, 195), (730, 365), (149, 245), (264, 313), (322, 304), (521, 320), (638, 282), (788, 377), (603, 219), (672, 243), (130, 350), (192, 359), (493, 251), (210, 199), (584, 254), (786, 157), (205, 135), (179, 172), (743, 223), (520, 305), (152, 149), (797, 164), (781, 170), (402, 384), (297, 320), (379, 347), (227, 214), (182, 241), (304, 349), (309, 131), (352, 320), (886, 229), (468, 261), (422, 369), (626, 373), (760, 191), (604, 164), (358, 177), (702, 188), (135, 236), (858, 150), (770, 170), (864, 230), (704, 151), (257, 156), (459, 383), (872, 363), (257, 372), (187, 326), (622, 307), (136, 277), (504, 144), (824, 239), (450, 330), (260, 314), (696, 354), (607, 357), (807, 257), (715, 303), (246, 129), (166, 254), (264, 325), (300, 131), (628, 186), (261, 191), (887, 305), (347, 367), (370, 357), (475, 281), (635, 172), (480, 210), (693, 329), (713, 240), (307, 249), (247, 175), (208, 212), (523, 143), (533, 204), (326, 314), (658, 139), (656, 272), (192, 373), (234, 292), (302, 325), (847, 340), (755, 305), (758, 345), (268, 376), (664, 377), (266, 254), (139, 308), (253, 216), (634, 263), (574, 356), (516, 159), (543, 305), (333, 138), (225, 213), (440, 242), (224, 175), (671, 361), (131, 352), (602, 221), (456, 181), (544, 332), (191, 209), (627, 258), (304, 218), (205, 307), (342, 327), (820, 367), (572, 140), (721, 206), (804, 331), (602, 242), (577, 290), (593, 363), (495, 283), (762, 221), (175, 213), (542, 247), (147, 152), (701, 174), (882, 285), (399, 173), (853, 357), (380, 347), (671, 163), (476, 301), (235, 307), (379, 381), (529, 243), (889, 159), (335, 384), (205, 347), (179, 355), (283, 286), (526, 169), (421, 226), (341, 344), (785, 303), (799, 252), (885, 217), (786, 205), (857, 228), (591, 212), (894, 322), (160, 269), (393, 252), (754, 186), (745, 220), (505, 194), (778, 277), (847, 297), (529, 378), (880, 174), (192, 374), (686, 273), (737, 299), (338, 175), (413, 202), (300, 294), (890, 194), (767, 310), (200, 252), (759, 352), (600, 277), (270, 200), (510, 205), (630, 318), (698, 373), (408, 189), (773, 357), (853, 251), (620, 205), (870, 380), (279, 200), (522, 286), (174, 367), (769, 380), (761, 309), (234, 157), (764, 236), (367, 272), (561, 209), (739, 365), (717, 351), (392, 162), (572, 367), (379, 344), (426, 147), (450, 180), (825, 204), (510, 376), (533, 361), (896, 247), (421, 160), (283, 210), (780, 213), (539, 215), (498, 323), (187, 206), (459, 165), (393, 136), (197, 295), (772, 206), (808, 212), (848, 128), (530, 319), (290, 357), (860, 313), (304, 210), (234, 137), (690, 256), (766, 129), (248, 352), (248, 381), (840, 343), (873, 162), (564, 276), (748, 230), (274, 177), (455, 313), (547, 329), (576, 229), (525, 157), (434, 255), (442, 272), (888, 320), (601, 342), (795, 370), (739, 221), (432, 294), (628, 279), (359, 245), (819, 208), (745, 287), (291, 200), (532, 169), (675, 263), (304, 243), (895, 241), (497, 297), (508, 146), (727, 325), (172, 321), (640, 282), (277, 242), (161, 302), (727, 201), (494, 251), (430, 289), (744, 242), (624, 181), (640, 291), (694, 382), (857, 150), (505, 184), (533, 364), (351, 139), (655, 149), (642, 377), (160, 372), (684, 307), (815, 277), (415, 198), (675, 190), (570, 226), (229, 150), (840, 339), (133, 351), (270, 174), (138, 317), (173, 187), (672, 258), (287, 257), (530, 279), (246, 226), (817, 252), (550, 166), (776, 138), (704, 164), (887, 169), (833, 243), (695, 224), (889, 372), (570, 203), (677, 220), (830, 361), (179, 267), (169, 295), (287, 326), (314, 235), (347, 247), (193, 174), (388, 175), (620, 249), (147, 174), (815, 289), (863, 379), (518, 249), (797, 295), (380, 353), (821, 305), (592, 138), (248, 224), (477, 229), (794, 217), (628, 272), (626, 185), (142, 292), (863, 303), (690, 346), (515, 264), (783, 244), (611, 329), (741, 282), (816, 175), (432, 275), (589, 213), (782, 136), (549, 328), (393, 154), (318, 250), (448, 255), (307, 287), (382, 201), (213, 161), (804, 143), (378, 214), (654, 273), (598, 309), (707, 383), (789, 196), (312, 232), (271, 298), (706, 185), (561, 215), (390, 251), (678, 241), (150, 142), (527, 154), (218, 244), (564, 314), (422, 378), (855, 255), (181, 212), (131, 173), (129, 318), (847, 149), (482, 235), (743, 199), (581, 248), (379, 269), (445, 316), (323, 198), (845, 254), (886, 380), (894, 281), (383, 138), (564, 215), (181, 335), (628, 154), (540, 169), (605, 365), (202, 364), (336, 215), (716, 294), (582, 244), (213, 383), (568, 301), (859, 293), (666, 336), (543, 277), (863, 160), (727, 306), (502, 344), (700, 196), (148, 310), (152, 177), (860, 348), (819, 216), (244, 235), (798, 197), (548, 311), (188, 358), (547, 348), (741, 328), (291, 151), (457, 132), (826, 336), (879, 239), (848, 177), (634, 245), (212, 300), (442, 375), (806, 243), (863, 302), (661, 232), (435, 345), (629, 177), (691, 288), (638, 249), (755, 321), (419, 132), (619, 146), (306, 150), (888, 381), (432, 362), (870, 326), (419, 365), (140, 359), (172, 192), (742, 128), (274, 166), (544, 138), (303, 242), (277, 363), (445, 217), (590, 343), (859, 242), (773, 291), (380, 356), (622, 223), (742, 301), (288, 146), (130, 159), (357, 184), (436, 298), (446, 282), (553, 172), (614, 331), (392, 145), (424, 357), (424, 186), (825, 311), (371, 264), (419, 328), (252, 223), (182, 212), (339, 358), (753, 277), (482, 153), (694, 192), (620, 370), (135, 269), (835, 276), (828, 245), (892, 340), (824, 205), (350, 313), (185, 244), (262, 382), (603, 191), (423, 137), (704, 157), (778, 258)]

# point_list = [(892, 389), (244, 813), (800, 672), (866, 732), (856, 134), (261, 690), (639, 271), (790, 306), (149, 528), (880, 302), (792, 415), (379, 189), (213, 190), (545, 343), (171, 556), (153, 472), (380, 456), (542, 412), (311, 660), (732, 417), (432, 239), (705, 586), (565, 684), (743, 477), (186, 876), (377, 540), (883, 245), (795, 619), (632, 157), (319, 658), (216, 235), (881, 459), (873, 393), (482, 737), (436, 743), (210, 502), (265, 415), (178, 341), (223, 732), (639, 605), (173, 386), (523, 837), (833, 762), (132, 399), (874, 646), (517, 594), (453, 793), (541, 588), (367, 242), (234, 533), (520, 411), (747, 761), (186, 207), (174, 700), (447, 549), (437, 378), (297, 292), (781, 132), (821, 522), (511, 706), (886, 230), (492, 701), (663, 315), (425, 870), (774, 197), (185, 186), (388, 454), (238, 381), (338, 144), (755, 816), (170, 714), (308, 574), (881, 716), (661, 254), (709, 729), (803, 178), (651, 539), (529, 332), (697, 138), (497, 516), (885, 378), (254, 558), (643, 417), (579, 405), (882, 796), (481, 220), (177, 218), (778, 450), (853, 679), (139, 140), (323, 581), (276, 460), (437, 189), (188, 885), (264, 243), (168, 381), (574, 435), (322, 869), (618, 246), (222, 877)]

print "point list:", point_list

site_list = point_list

# print "locations determined"

# print site_list

# site_event_pairs = [(SiteEvent(p), p[1]) for p in point_list]

y_values = [x[1] for x in point_list]

max_y_value = max(y_values)

# print "max y-value:", max_y_value

y_maximal_point_list = [x for x in point_list if x[1] == max_y_value]

y_not_maximal_point_list = [x for x in point_list if x[1] != max_y_value]

y_maximal_point_list_sorted_by_x = y_maximal_point_list[ : ]

y_maximal_point_list_sorted_by_x.sort(key = lambda x: x[0])

# print y_maximal_point_list_sorted_by_x

leading_arc_site_list = y_maximal_point_list_sorted_by_x

non_leading_arc_site_list = y_not_maximal_point_list

leading_arc_site_event_pair_list = [(SiteEvent(s), s[1]) for s in leading_arc_site_list]

non_leading_arc_site_event_pair_list = [(SiteEvent(s), s[1]) for s in non_leading_arc_site_list]

# print "leading arc site list:", leading_arc_site_list

"""

initial_point_list_sorted_by_x = y_maximal_point_list_sorted_by_x

trailing_point_list = point_with_y_component_not_maximal_list

initial_site_event_pairs_sorted_by_x = [(SiteEvent(p), p[1]) for p in initial_point_list_sorted_by_x]

trailing_site_event_pairs = [(SiteEvent(p), p[1]) for p in trailing_point_list]

"""

initial_y_value = max_y_value

sweep_line.setY(initial_y_value)

# handle leading arcs

for site_event_pair in leading_arc_site_event_pair_list:

  event, y = site_event_pair

  event.handle(tree, vertex_list, event_queue, truncated_bisector_edge_dict, sweep_line, initial_y_value)

# print tree.toIntervalStringList()

# raise Exception()

# create initial truncated bisector edges

num_leading_arcs = len(leading_arc_site_list)

num_initial_truncated_bisector_edges = max(0, num_leading_arcs - 1)

for i in range(num_initial_truncated_bisector_edges):

  site_a = leading_arc_site_list[i]

  site_b = leading_arc_site_list[i + 1]

  truncated_bisector_edge_dict.addTruncatedBisectorEdge(site_a, site_b)

# print site_event_pairs

# for site_event_pair in site_event_pairs:

# handle non-leading arcs

for site_event_pair in non_leading_arc_site_event_pair_list:

  event, y = site_event_pair

  # print event.getLocation(), -1 * y

  # print "y-value for site event:", y
  
  # working with a min-heap
  
  # using negative y values for priorities
  
  event_queue.insert((-1 * y, False), event)

x_values = [x[0] for x in point_list]

y_values = [x[1] for x in point_list]

min_x_value = min(x_values)

max_x_value = max(x_values)

min_y_value = min(y_values)

max_y_value = max(y_values)

circle_event_parameter_value_list_tuple_list = []

# process events with largest y values first

while not event_queue.isEmpty():

  # print "lowest value that serves as a priority:", event_queue.min().getKey()

  # print event_queue.queue

  entry = event_queue.removeMin()

  event = entry.getValue()

  # priority = entry.getKey()

  key = entry.getKey()

  priority, is_for_split_residue_arc = key

  """

  if event.isCircleEvent() == True:

    # raise Exception(priority, event.getArc().getFocus())

    print "circle event:", priority, event.getArc().getFocus()

    print "circle event originated from a site event:", event.getCausingEventIsSiteType()

    arc = event.getArc()

    left_arc = tree.getArcLeftNeighbor(arc)

    right_arc = tree.getArcRightNeighbor(arc)

    print left_arc.getFocus(), arc.getFocus(), right_arc.getFocus()

    l_y = tree.getSweepLine().getY()

    print CircleEvent.getIntersectionHelper(l_y, left_arc, arc, right_arc)

    print CircleEvent.getLargestEmptyCircleLowestExtent(l_y, left_arc, arc, right_arc)

    circle_event_parameter_value_list_tuple_list.append((event, (left_arc, arc, right_arc, l_y)))

  elif event.isSiteEvent() == True:

    print "site event:", priority, event.getLocation()

  """

  # print priority

  # print "y-value for priority:", getYValueForPriority(priority)

  """

  if sweep_line.getY() != None and not (getYValueForPriority(priority) <= (sweep_line.getY() + tree._getTolerance())):

    print event_queue.toString()

    print getYValueForPriority(priority), sweep_line.getY()

    raise Exception("jumping event priority values")

  """
  
  sweep_line.setY(getYValueForPriority(priority))

  # print "sweep-line y:", sweep_line.getY()
  
  # handle event

  # print event_queue.toString()

  initial_y_value = max_y_value

  event.handle(tree, vertex_list, event_queue, truncated_bisector_edge_dict, sweep_line, initial_y_value)

  # print event_queue.toString()

# unique_site_list = list(set(site_list))

edge_list = truncated_bisector_edge_dict.getAllEdgesWithEndpointsThatAreNotIndeterminate()

edge_location_pair_list = [(x.getFirstVertex().getLocation(), x.getSecondVertex().getLocation()) for x in edge_list]

unique_edge_location_pair_list = list(set(edge_location_pair_list))

non_finite_length_edge_list = truncated_bisector_edge_dict.getAllEdgesWithAnEndpointThatIsIndeterminate()

non_finite_length_edge_location_pair_list = [(x.getFirstVertex().getLocation(), x.getSecondVertex().getLocation()) for x in non_finite_length_edge_list]

unique_non_finite_length_edge_location_pair_list = list(set(non_finite_length_edge_location_pair_list))

vertex_location_list = [x.getLocation() for x in vertex_list]

unique_vertex_location_list = list(set(vertex_location_list))

# def isSizeZeroEdge(edge):

def isSizeZeroEdge(edge_location_pair):

  """

  vertex1 = edge.getFirstVertex()

  vertex2 = edge.getSecondVertex()

  location1 = vertex1.getLocation()

  location2 = vertex2.getLocation()

  return location1 == location2

  """

  location1 = edge_location_pair[0]

  location2 = edge_location_pair[1]

  return location1 == location2

unique_non_size_zero_edge_location_pair_list = [x for x in unique_edge_location_pair_list if isSizeZeroEdge(x) == False]

site_points = []

for site in site_list:

  # print site

  # plot

  # note that we output sites in same order in which they were described, 
  #   and not necessarily order in which they were added

  site_points.append(site)

from PIL import Image, ImageDraw

# im = Image.new("RGB", (512, 512), "white")

# im = Image.new("RGB", (1024, 512), "white")

# im = Image.new("RGB", (1024, 1024), "white")

# im = Image.new("RGB", (3072, 3072), "white")

im = Image.new("RGB", (512, 512), "white")

# im = Image.new("RGB", (1024, 1024), "white")

draw = ImageDraw.Draw(im)

plotPoints(draw, site_points, (128, 128, 128))

points = []

"""

print len(circle_event_parameter_value_list_tuple_list)

# raise Exception()

for circle_event_parameter_value_list_tuple in circle_event_parameter_value_list_tuple_list:

  circle_event, parameter_value_list = circle_event_parameter_value_list_tuple

  left_arc, arc, right_arc, l_y = parameter_value_list

  drawCircleEvent(draw, left_arc, arc, right_arc, l_y, (64, 64, 64))

  highlightSiteForArc(draw, arc, (255, 0, 0))

"""

# for vertex in vertex_list:

# for vertex in unique_vertex_list:

for vertex_location in unique_vertex_location_list:

  # print vertex.toString()

  # print vertex_location

  # plot

  # points.append(vertex.getLocation())

  points.append(vertex_location)

plotPoints(draw, points, (0, 0, 0))

segments = []
  
# for edge in edge_list:

# for edge in non_size_zero_edge_list:

for edge_location_pair in unique_non_size_zero_edge_location_pair_list:

  # print edge.toString()

  # print edge_location_pair

  # plot

  """

  vertex1 = edge.getFirstVertex()

  vertex2 = edge.getSecondVertex()

  location1 = vertex1.getLocation()

  location2 = vertex2.getLocation()

  segment = (location1, location2)

  """

  segment = edge_location_pair

  segments.append(segment)

for edge_location_pair in unique_non_finite_length_edge_location_pair_list:

  # print edge_location_pair

  pass

plotLineSegments(draw, segments, (0, 0, 0))

im.save("diagram.png")
  
# deal with graph that may have edges that have indeterminate endpoints

# settle indeterminate endpoints

# overlay subdivision implied by graph with edges with settled endpoints 
#   with subdivision consisting of bounding box

# make sure that we have enough faces identified

# come up with a trapezoidal map

# process queries

time2 = time.clock()

time_diff = time2 - time1

print time_diff
