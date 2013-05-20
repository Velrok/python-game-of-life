#!/usr/bin/env python
import time
import random
from itertools import chain
import os
from collections import deque

def create_world(width, height, population_prob):
  return [
      [1 if (random.random() <= population_prob) else 0
          for _ in range(width)] 
              for _ in range(height)]


def render_world(world, cycle):
  def output_mapper(x):
    if x == 1:
      return "#"
    else:
     return " "

  print "cycle: {}".format(cycle)
  for row in world:
    print "|{}|".format(
        "".join(
          map(output_mapper, row)))


def new_cell_state(state, neighbors):
  alive_neighbors_count = sum(chain(*neighbors))
  # print "neighbors: " + str(neighbors)
  # print "alive_neighbors_count:" + str(alive_neighbors_count)
  # print "state:" + str(state)
  if (state == 1):
    # alive
    # print "alive"
    alive_neighbors_count -= 1 # sub this alive cell from sum
    if(alive_neighbors_count == 2 or
       alive_neighbors_count == 3):
      return 1
    else:
      return 0
  else:
    # dead cell
    # print "dead"
    if(alive_neighbors_count == 3):
      return 1
    else:
      return 0


def element_at(x, y, world):
  w_height = len(world)
  w_width = len(world[0])
  if x < 0 or y < 0 or x >= w_width or y >= w_height:
    return 0
  else:
    return world[y][x]


def neighbors(x, y, world):
  return [[ element_at(x + dx, y + dy, world)
    for dx in range(-1, 2)] 
      for dy in range(-1, 2)]


def next_state(world):
  return [[new_cell_state(cell, neighbors(x, y, world)) 
    for x, cell in enumerate(row)] 
      for y, row in enumerate(world)]


def spawn_beacon(x, y, world):
  new_world = world
  coords = [(0,0), (1,0), (1,1), (0,1),
            (2,2), (2,3), (3,3), (3,2)]
  
  for dx, dy in coords:
    new_world[y + dy][x + dx] = 1
  
  return new_world


def all_equal(l):
  def eq(tup):
    return tup[0] == tup[1]
  return all(map(eq, zip(list(l)[1:], list(l))))


if __name__ == "__main__":
  world = create_world(50, 20, 0.4)
  world = spawn_beacon(1,1, world)
  cycle = 0
  laste_states = deque([world], maxlen=5)
  while not all_equal(laste_states) or len(laste_states) < 5:
    os.system('clear')
    render_world(world, cycle)
    world = next_state(world)
    laste_states.append(world)
    cycle += 1
    time.sleep(0.2)
  print "world stabe -> quit"

