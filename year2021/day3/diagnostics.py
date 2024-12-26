#!/usr/bin/env python3

def main(filename):
  inputfile = open(filename, 'r')
  
  bits = []
  while True:
    line = inputfile.readline()
    if not line:
      break

    bits.append([ord(c) - ord('0') for c in line.strip()])

  # Sum each of the bit positions.
  bit_sums = list(map(sum, zip(*bits)))
  num_bits = len(bits)

  # If the sum is more than half the number of entries, then the most common is 1.
  gamma_bits = [1 if bit_sum > num_bits/2.0 else 0 for bit_sum in bit_sums]
  epsilon_bits = [1 if bit == 0 else 0 for bit in gamma_bits]

  # Convert back to string and parse as a binary number.
  gamma = int("".join(chr(bit + ord('0')) for bit in gamma_bits), 2)
  epsilon = int("".join(chr(bit + ord('0')) for bit in epsilon_bits), 2)

  print(filename, 'Power consumption:', gamma*epsilon)

  o2_bits = list(bits)
  position = 0
  while len(o2_bits) > 1:
    bit_sums = list(map(sum, zip(*o2_bits)))
    num_bits = len(o2_bits)
    most_common = 1 if bit_sums[position] >= num_bits/2.0 else 0
    o2_bits[:] = [bits for bits in o2_bits if bits[position] == most_common]
    position += 1

  co2_bits = list(bits)
  position = 0
  while len(co2_bits) > 1:
    bit_sums = list(map(sum, zip(*co2_bits)))
    num_bits = len(co2_bits)
    most_common = 1 if bit_sums[position] < num_bits/2.0 else 0
    co2_bits[:] = [bits for bits in co2_bits if bits[position] == most_common]
    position += 1

  # Convert back to string and parse as a binary number.
  o2 = int("".join(chr(bit + ord('0')) for bit in o2_bits[0]), 2)
  co2 = int("".join(chr(bit + ord('0')) for bit in co2_bits[0]), 2)

  print(filename, 'Life support rating:', o2 * co2)


if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
