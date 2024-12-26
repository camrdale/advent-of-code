#!/usr/bin/env python3


def main(filename):
  inputfile = open(filename, 'r')
  matrix = []

  while True:
    line = inputfile.readline()
    if not line:
      break
    matrix.append(list(map(int, list(line.strip()))))
  
  width = len(matrix[0])
  height = len(matrix)
  num_flashes = [0]    

  def neighbors(i):
    return [j for j in ((i[0]-1, i[1]-1), (i[0]-1, i[1]), (i[0]-1, i[1]+1),
                        (i[0], i[1]-1), (i[0], i[1]+1),
                        (i[0]+1, i[1]-1), (i[0]+1, i[1]), (i[0]+1, i[1]+1))
            if j[0] >= 0 and j[0] < height and j[1] >= 0 and j[1] < width
               and matrix[j[0]][j[1]] < 10]

  for step in range(1000000):
    for i0 in range(height):
      for i1 in range(width):
        to_check = [(i0, i1)]
        while to_check:
          i = to_check.pop(0)
          matrix[i[0]][i[1]] += 1
          if matrix[i[0]][i[1]] == 10:
            num_flashes[0] += 1
            to_check.extend(neighbors(i))
    num_reset = 0
    for i0 in range(height):
      for i1 in range(width):
        i = (i0, i1)
        if matrix[i[0]][i[1]] > 9:
          num_reset += 1
          matrix[i[0]][i[1]] = 0
    if step == 99:
      print(filename, 'number of flashes after 100 steps:', num_flashes[0])
    if num_reset == height*width:
      print(filename, 'synchronized flash at step:', step + 1)
      break


if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
