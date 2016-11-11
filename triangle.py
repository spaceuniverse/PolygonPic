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
pygame.display.set_caption("_polygonpic_prototype_")

# ---------------------------------------------------------- #
# Var

running = True

# ---------------------------------------------------------- #
# Setup

print "Setup..."

points_number = 70   # 70 !IMPORTANT
dist_from_borders = 21   # !IMPORTANT

X = np.random.randint(dist_from_borders, width - dist_from_borders, size=(points_number,))
Y = np.random.randint(dist_from_borders, height - dist_from_borders, size=(points_number,))

point_cloud_list = zip(list(X), list(Y))
point_cloud_list_new = point_cloud_list[:]

distance_threshold = 77   # 70 !IMPORTANT

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

while running:
  
  # Delay
  # time.sleep(1)
  
  screen.fill((0, 0, 0, 0))
  
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
  
  for p in point_cloud_list:
    c = (255, 255, 255, 255)
    pygame.gfxdraw.filled_circle(screen, p[0], p[1], 5, c)
  
  for i in xrange(tri_coords.shape[0]):
    # c = (0, 0, np.random.randint(70, 170), 255)
    c = (255, 255, 255, 255)
    # filled_trigon | aatrigon for borders only
    pygame.gfxdraw.aatrigon(screen,
                            tri_coords[i, :, :][0, 0], tri_coords[i, :, :][0, 1],
                            tri_coords[i, :, :][1, 0], tri_coords[i, :, :][1, 1],
                            tri_coords[i, :, :][2, 0], tri_coords[i, :, :][2, 1], c)
    # Debug print
    # print i, tri_coords[i, :, :].shape
  
  pygame.display.flip()
  
  for event in pygame.event.get():
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
      running = False
      print "Exit..."
      pygame.image.save(screen, "screen.png")
      pygame.quit()
  
print "All stopped..."

# -------------------------# 
