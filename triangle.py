# ---------------------------------------------------------- #
#
# PolygonPic
#
# Links:
# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.Delaunay.html
#
# ---------------------------------------------------------- #
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
from scipy.spatial import Delaunay
# import time
# import itertools
# ---------------------------------------------------------- #
# Init

width = 600
height = 800

w_shift = width / 3   # !IMPORTANT
h_shift = height / 4   # !IMPORTANT

pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("_polygon_pic_prototype_")

# ---------------------------------------------------------- #
# Var

running = True
filled = True
grad_shadow = False

# ---------------------------------------------------------- #
# Setup

print "Setup..."

points_number = 70   # 70 !IMPORTANT
dist_from_borders = 27   # !IMPORTANT

X = np.random.randint(dist_from_borders, width - dist_from_borders, size=(points_number,))
Y = np.random.randint(dist_from_borders, height - dist_from_borders, size=(points_number,))

point_cloud_list = zip(list(X), list(Y))
point_cloud_list_new = point_cloud_list[:]

distance_threshold = 70   # 70 !IMPORTANT

# Combinations using for
for p1 in point_cloud_list:
  for p2 in point_cloud_list_new:
    if p1 != p2:
      dist = np.linalg.norm(np.array(p1) - np.array(p2))
      # print p1, p2, dist
      # print point_cloud_list, point_cloud_list_new
      if dist < distance_threshold:
        # print point_cloud_list, point_cloud_list_new
        try:
          point_cloud_list_new.remove(p1)
        except:
          # print "exeption"
          pass

# Combinations using intertools
"""
combinations =  list(itertools.combinations(point_cloud_list, 2))
for c in combinations:
  dist = np.linalg.norm(np.array(c[0]) - np.array(c[1]))
  # print c, dist
  if dist > 100:
    point_cloud_list_new.append(c[0])
    point_cloud_list_new.append(c[1])
  else:
    point_cloud_list_new.append(c[0])
point_cloud_list_new = list(set(point_cloud_list_new))
"""

# Add corners and borders | Manual | Need tuning
# print point_cloud_list, point_cloud_list_new
point_cloud_list.append((0, 0))
point_cloud_list.append((0, height))
point_cloud_list.append((width, 0))
point_cloud_list.append((width, height))
point_cloud_list_new.append((0, 0))
point_cloud_list_new.append((0, height))
point_cloud_list_new.append((width, 0))
point_cloud_list_new.append((width, height))
#
point_cloud_list.append((0, h_shift))
point_cloud_list.append((0, 2 * h_shift))
point_cloud_list.append((0, 3 * h_shift))
point_cloud_list_new.append((0, h_shift))
point_cloud_list_new.append((0, 2 * h_shift))
point_cloud_list_new.append((0, 3 * h_shift))
#
point_cloud_list.append((width, h_shift))
point_cloud_list.append((width, 2 * h_shift))
point_cloud_list.append((width, 3 * h_shift))
point_cloud_list_new.append((width, h_shift))
point_cloud_list_new.append((width, 2 * h_shift))
point_cloud_list_new.append((width, 3 * h_shift))
#
point_cloud_list.append((w_shift, 0))
point_cloud_list.append((w_shift * 2, 0))
point_cloud_list_new.append((w_shift, 0))
point_cloud_list_new.append((w_shift * 2, 0))
#
point_cloud_list.append((w_shift, height))
point_cloud_list.append((w_shift * 2, height))
point_cloud_list_new.append((w_shift, height))
point_cloud_list_new.append((w_shift * 2, height))

point_cloud = np.array(point_cloud_list)
point_cloud_new = np.array(point_cloud_list_new)

# Use not all points | !IMPORTANT
point_cloud = point_cloud_new
point_cloud_list = point_cloud_list_new

# Debug print
# print point_cloud_list, "\n", point_cloud_list_new, "\n",  point_cloud, point_cloud.shape

tri = Delaunay(point_cloud)
tri_coords = point_cloud[tri.simplices]

# Debug print
# print tri.simplices, point_cloud[tri.simplices], point_cloud[tri.simplices].shape

# ---------------------------------------------------------- #
# Main

# Color 1
# c_const_list = [(0, 0, np.random.randint(70, 170), 255) for _ in xrange(tri_coords.shape[0])]
# print tri_coords.shape[0], len(c_const_list), c_const_list

# Color 2
start_color = np.array((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), 255))
end_color = np.array((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), 255))
color_dist = np.linalg.norm(end_color - start_color)
while color_dist < 310:   # !IMPORTANT
  start_color = np.array((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), 255))
  end_color = np.array((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), 255))
  color_dist = np.linalg.norm(end_color - start_color)
  # print color_dist
color_shift = (end_color - start_color) / (tri_coords.shape[0] * 1.0)
mask_shift = 90 / (tri_coords.shape[0] * 1.0)   # 90 or 170 max opacity
# print start_color, end_color, (end_color - start_color), tri_coords.shape[0], color_shift
c_const_list = [(int(np.clip((start_color[0] + color_shift[0] * i) + np.random.randint(-5, 5), 0, 255)),
                 int(np.clip((start_color[1] + color_shift[1] * i) + np.random.randint(-5, 5), 0, 255)),
                 int(np.clip((start_color[2] + color_shift[2] * i) + np.random.randint(-5, 5), 0, 255)),
                 255) for i in xrange(tri_coords.shape[0])]
c_const_mask = [(0, 0, 0, int(np.clip((0 + mask_shift * i), 0, 255))) for i in xrange(tri_coords.shape[0])]
# Random mask
c_const_mask2 = [(0, 0, 0, np.random.randint(0, 79)) for i in xrange(tri_coords.shape[0])]
# c_const_mask2 = [(100, 100, 100, 240) for i in xrange(tri_coords.shape[0])]
# print tri_coords.shape[0], len(c_const_list), c_const_list
# np.random.randint(170, 255) np.random.randint(0, 90)
# print len(c_const_mask), len(c_const_mask2)
# For gradient fill
k_of_w = 2.5   # !IMPORTANT
grad_mask_shift = 255 / ((height - (height / k_of_w)) * 1.0)
grad_mask = [(0, 0, 0, int(np.clip((0 + grad_mask_shift * i), 0, 255))) for i in xrange(int(height - (height / k_of_w)))]

while running:
  
  # Delay
  # time.sleep(1)
  
  screen.fill((0, 0, 0, 255))
  #screen.fill((255, 255, 255, 255))
  
  # ------------------ #
  # Tests
  """
  for i in range(100):
    p1 =  (np.random.randint(480), np.random.randint(640))
    p2 =  (np.random.randint(480), np.random.randint(640))
    p3 =  (np.random.randint(480), np.random.randint(640))
    # c = (255, 255, 255, 5)
    c = (np.random.randint(255), np.random.randint(255), np.random.randint(255), 5)
    # pygame.gfxdraw.aatrigon(screen, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], c)
    pygame.gfxdraw.filled_trigon(screen, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], c)
  """  
  """
  for i in range(100):
    p1 =  (np.random.randint(480), np.random.randint(640))
    c = (np.random.randint(255), np.random.randint(255), np.random.randint(255), 255)
    pygame.gfxdraw.filled_circle(screen, p1[0], p1[1], 3, c)
  """
  # ------------------ #

  # Points
  for p in point_cloud_list:
    if filled:
      size_p = 1
      c = (255, 255, 255, 100)
    else:
      size_p = 5
      c = (255, 255, 255, 255)
    pygame.gfxdraw.filled_circle(screen, p[0], p[1], size_p, c)

  # Triangles
  for i in xrange(tri_coords.shape[0]):
    if filled:
      c = (0, 0, 0, 200)
      pygame.gfxdraw.filled_trigon(screen,
                              tri_coords[i, :, :][0, 0], tri_coords[i, :, :][0, 1],
                              tri_coords[i, :, :][1, 0], tri_coords[i, :, :][1, 1],
                              tri_coords[i, :, :][2, 0], tri_coords[i, :, :][2, 1], c_const_list[i])

      pygame.gfxdraw.filled_trigon(screen,
                              tri_coords[i, :, :][0, 0], tri_coords[i, :, :][0, 1],
                              tri_coords[i, :, :][1, 0], tri_coords[i, :, :][1, 1],
                              tri_coords[i, :, :][2, 0], tri_coords[i, :, :][2, 1],
                              (0, 0, 0, c_const_mask[i][0] + c_const_mask2[i][3]))
                              # set [0] or [3] for grad or random shadows

      pygame.gfxdraw.aatrigon(screen,
                              tri_coords[i, :, :][0, 0], tri_coords[i, :, :][0, 1],
                              tri_coords[i, :, :][1, 0], tri_coords[i, :, :][1, 1],
                              tri_coords[i, :, :][2, 0], tri_coords[i, :, :][2, 1], c_const_list[i])

      pygame.gfxdraw.aatrigon(screen,
                              tri_coords[i, :, :][0, 0], tri_coords[i, :, :][0, 1],
                              tri_coords[i, :, :][1, 0], tri_coords[i, :, :][1, 1],
                              tri_coords[i, :, :][2, 0], tri_coords[i, :, :][2, 1],
                              (0, 0, 0, c_const_mask[i][0] + c_const_mask2[i][3]))
    else:
      c = (255, 255, 255, 255)
      pygame.gfxdraw.aatrigon(screen,
                              tri_coords[i, :, :][0, 0], tri_coords[i, :, :][0, 1],
                              tri_coords[i, :, :][1, 0], tri_coords[i, :, :][1, 1],
                              tri_coords[i, :, :][2, 0], tri_coords[i, :, :][2, 1], c)
      # Debug print
      # print i, tri_coords[i, :, :].shape

  # Gradient fill from bottom
  if filled and grad_shadow:
    for k in xrange(int(height - (height / k_of_w))):
      pygame.gfxdraw.hline(screen, 0, width, int(height / k_of_w) + k, grad_mask[k])

  pygame.display.flip()
  
  for event in pygame.event.get():
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
      running = False
      print "Exit..."
      pygame.image.save(screen, "screen.png")
      pygame.quit()
  
print "All stopped..."

# -------------------------# 
