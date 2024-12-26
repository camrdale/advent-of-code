#!/usr/bin/env python3

import numpy


def part_one(filename):
  inputfile = open(filename, 'r')
  inputarray = []
  width = 0
  height = 0

  while True:
    line = inputfile.readline()
    if not line:
      break
    
    inputarray.extend(map(int, list(line.strip())))
    if not width:
      width = len(inputarray)
    height += 1
  
  matrix = numpy.array(inputarray).reshape(height, width)

  # Matrices shifted by one in all four directions, filled with 10s.
  down = numpy.insert(numpy.delete(matrix, 0, axis=0), height-1, 10, axis=0)
  up = numpy.vstack([numpy.tile(10, [1, width]), matrix[:-1, :]])
  left = numpy.tile(10, [height, width])
  left[:, :-1] = matrix[:, 1:]
  right = numpy.tile(10, [height, width])
  right[:, 1:] = matrix[:, :-1]

  # Create a vectorized function that will look at the four neighbors of a location.
  def risklevel(i, downi, upi, lefti, righti):
    if i < min(downi, upi, lefti, righti):
      return i + 1
    return 0

  vfunc_risklevel = numpy.vectorize(risklevel)
  output = vfunc_risklevel(matrix, down, up, left, right)

  print(filename, "sum of risk levels:", numpy.sum(output))


def part_two(filename):
  inputfile = open(filename, 'r')
  inputarray = []
  width = 0
  height = 0

  while True:
    line = inputfile.readline()
    if not line:
      break
    
    inputarray.extend(map(int, list(line.strip())))
    if not width:
      width = len(inputarray)
    height += 1
  
  matrix = numpy.array(inputarray).reshape(height, width)

  basin_sizes = []

  # Find the indexes of the first smallest entry in the matrix.
  mini = numpy.unravel_index(matrix.argmin(), matrix.shape)
  while matrix[mini] != 9:
    basin = set()

    # Recursive function to process the neighbors in a basin
    def tryi(i):
      # Check for invalid locations.
      if i[0] < 0 or i[0] >= height or i[1] < 0 or i[1] >= width:
        return
      # Abort recursion if edge reached, or location was already checked.
      if matrix[i] == 9:
        return
      # New location found, add it, and mark as checked by setting to 9.
      basin.add(i)
      matrix[i] = 9
      # Now recursively try all the neighbors.
      tryi((i[0]-1, i[1]))
      tryi((i[0]+1, i[1]))
      tryi((i[0], i[1]-1))
      tryi((i[0], i[1]+1))

    # Start recursion from the current minimum in the matrix.
    tryi(mini)
    basin_sizes.append(len(basin))
    mini = numpy.unravel_index(matrix.argmin(), matrix.shape)

  basin_sizes.sort(reverse=True)
  print(filename, "3 largest basins multipied:", basin_sizes[0]*basin_sizes[1]*basin_sizes[2])


if __name__ == '__main__':
  part_one('example_input.txt')
  part_one('input.txt')
  part_two('example_input.txt')
  part_two('input.txt')
