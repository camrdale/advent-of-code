#!/usr/bin/python

from pathlib import Path
from collections import defaultdict
import colorsys
from abc import ABC, abstractmethod
from typing import NamedTuple

import cairo
import cv2
import numpy
import ffmpeg

INPUT_FILE = Path('input.txt')
FRAMES_DIR = Path('./frames')
FRAMES_DIR.mkdir(exist_ok=True)
WIDTH = 1280
HEIGHT = 720
MIN_COLOR_H = 0.0
MAX_COLOR_H = 300.0 / 360.0
BACKGROUND_COLOR = (1.0, 1.0, 1.0)
TEXT_COLOR = (0.0, 0.0, 0.0)
DONE_TEXT_COLOR = (0.02, 0.66, 0.26)

class SortingAlgorithm(ABC):

    @abstractmethod
    def initialize(self, locations: list[int]) -> None:
        """Called once to pass in the input list of location IDs to sort."""
        pass

    @abstractmethod
    def iterate(self) -> bool:
        """Perform a single iteration, only one change can be made to the list.
        
        Returns true if the input list is now sorted.
        """
        pass


class BubbleSort(SortingAlgorithm):

    def initialize(self, locations: list[int]) -> None:
        self.locations = locations
        self.n = len(locations)
        self.i = 0
        self.j = 0
        self.is_swapped = False
        self.done = False

    def iterate(self) -> bool:
        if self.done:
            return True
        while self.i < self.n:
            while self.j < self.n - 1:
                if self.locations[self.j] > self.locations[self.j + 1]:
                    temp = self.locations[self.j]
                    self.locations[self.j] = self.locations[self.j + 1]
                    self.locations[self.j + 1] = temp
                    self.is_swapped = True
                    self.j += 1
                    return False
                self.j += 1
            if not self.is_swapped:
                self.done = True
                return True
            self.i += 1
            self.j = 0
            self.is_swapped = False
        self.done = True
        return True


class InsertionSort(SortingAlgorithm):

    def initialize(self, locations: list[int]) -> None:
        self.locations = locations
        self.n = len(locations)
        self.i = 1
        self.j = self.i
        self.done = False

    def iterate(self) -> bool:
        if self.done:
            return True
        while self.i < self.n:
            while self.j > 0 and self.locations[self.j] < self.locations[self.j-1]:
                temp = self.locations[self.j]
                self.locations[self.j] = self.locations[self.j - 1]
                self.locations[self.j - 1] = temp
                self.j -= 1
                return False
            self.i += 1
            self.j = self.i
        self.done = True
        return True


class QuickSortOperation(NamedTuple):
    low: int  # low index
    high: int  # high index
    i: int  # greater index
    j: int  # iteration index

class QuickSort(SortingAlgorithm):

    def initialize(self, locations: list[int]) -> None:
        self.locations = locations
        self.stack = [QuickSortOperation(0, len(locations) - 1, -1, 0)]

    def iterate(self) -> bool:
        if len(self.stack) == 0:
            return True
        op = self.stack.pop()
        i = op.i
        j = op.j
        pivot = self.locations[op.high]
        while j < op.high:
            if self.locations[j] <= pivot:
                i += 1
                temp = self.locations[j]
                self.locations[j] = self.locations[i]
                self.locations[i] = temp
                self.stack.append(QuickSortOperation(op.low, op.high, i, j+1))
                return False
            j += 1
        
        temp = self.locations[i+1]
        self.locations[i+1] = self.locations[op.high]
        self.locations[op.high] = temp
        if op.low < i:
            self.stack.append(QuickSortOperation(op.low, i, op.low - 1, op.low))
        if i + 2 < op.high:
            self.stack.append(QuickSortOperation(i + 2, op.high, i + 1, i + 2))
        return len(self.stack) == 0


class MergeSortOperation(NamedTuple):
    l: int  # left index
    m: int  # middle index
    r: int  # right index
    left_array: list[int] | None  # left array
    i: int  # left array index
    right_array: list[int] | None  # right array
    j: int  # right array index
    k: int  # initial index of merged subarray


class MergeSort(SortingAlgorithm):
    def initialize(self, locations: list[int]) -> None:
        self.locations = locations
        self.n = len(locations)
        # Stack of current operations: left index, middle index, right index, left array, left array index, right array, right array index, initial index of merged subarray
        # If the left/right arrays are None, then they haven't been initialized yet.
        self.stack: list[MergeSortOperation] = []
        self.buildStack(0, self.n - 1)

    def buildStack(self, l: int, r: int) -> None:
        m = (l + r) // 2
        self.stack.append(MergeSortOperation(l, m, r, None, 0, None, 0, l))
        if l < m:
            self.buildStack(l, m)
        if m+1 < r:
            self.buildStack(m+1, r)

    def iterate(self) -> bool:
        if len(self.stack) == 0:
            return True
        
        op = self.stack.pop()
        left_array: list[int] | None = op.left_array
        i = op.i
        right_array: list[int] | None = op.right_array
        j = op.j
        k = op.k
        n1 = op.m - op.l + 1
        n2 = op.r - op.m
        
        if left_array is None:
            left_array = self.locations[op.l:(op.m+1)]
        if right_array is None:
            right_array = self.locations[(op.m+1):(op.r+1)]
        
        if i < n1 and j < n2:
            if left_array[i] <= right_array[j]:
                self.locations[k] = left_array[i]
                i += 1
            else:
                self.locations[k] = right_array[j]
                j += 1
        elif i < n1:
            self.locations[k] = left_array[i]
            i += 1
        elif j < n2:
            self.locations[k] = right_array[j]
            j += 1
        else:
            # Done with this merge, don't put anything back on the stack.
            return len(self.stack) == 0

        k += 1
        self.stack.append(MergeSortOperation(op.l, op.m, op.r, left_array, i, right_array, j, k))
        return False


img = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
nda = numpy.ndarray(shape = (HEIGHT, WIDTH, 4), dtype = numpy.uint8, buffer = img.get_data())
ctx = cairo.Context(img)
ffs = [
    cairo.ToyFontFace('Source Sans Pro Semibold'),
    cairo.ToyFontFace('Cascadia Mono'),
    cairo.ToyFontFace('Noto Color Emoji')]

left_input: list[int] = []
right_input: list[int] = []
with INPUT_FILE.open() as ifp:
    for line in ifp.readlines():
        val = line.split()
        left_input.append(int(val[0]))
        right_input.append(int(val[1]))

max_value = max(max(left_input), max(right_input))
min_value = min(min(left_input), min(right_input))

sorting_algorithms: list[tuple[str, list[int], SortingAlgorithm]] = [
    ('BubbleSort Left', list(left_input), BubbleSort()),
    ('BubbleSort Right', list(right_input), BubbleSort()),
    ('InsertionSort Left', list(left_input), InsertionSort()),
    ('InsertionSort Right', list(right_input), InsertionSort()),
    ('MergeSort Left', list(left_input), MergeSort()),
    ('MergeSort Right', list(right_input), MergeSort()),
    ('QuickSort Left', list(left_input), QuickSort()),
    ('QuickSort Right', list(right_input), QuickSort()),
    ]

for _, to_sort, sorting_algorithm in sorting_algorithms:
    sorting_algorithm.initialize(to_sort)

frame = 0
done: dict[str, int] = defaultdict(int)
while True:
    all_done = True
    for desc, to_sort, sorting_algorithm in sorting_algorithms:
        if not sorting_algorithm.iterate():
            all_done = False
        elif desc not in done:
            done[desc] = frame

    if all_done:
        break

    # Paint the background white (overwriting any previous frame's data)
    ctx.identity_matrix()
    ctx.set_source_rgba(*BACKGROUND_COLOR)
    ctx.paint()

    algorithm_num = 0
    for desc, to_sort, sorting_algorithm in sorting_algorithms:
        for i, location_id in enumerate(to_sort):
            # Use the location ID number to determine the color, using HLS color space
            rgb = colorsys.hls_to_rgb(
                MIN_COLOR_H + (MAX_COLOR_H - MIN_COLOR_H) * (location_id - min_value) / (max_value - min_value),
                0.5, 1.0)

            # Draw a line for the location ID
            x = 10 + i
            ctx.move_to(x, 10 + 50*algorithm_num)
            ctx.line_to(x, 50 + 50*algorithm_num)
            ctx.set_line_width(1)
            ctx.set_source_rgba(*rgb)
            ctx.stroke()

        ctx.set_font_face(ffs[0])
        ctx.set_font_size(24)
        ctx.move_to(1020, 40 + 50*algorithm_num)
        ctx.set_source_rgba(*(DONE_TEXT_COLOR if desc in done else TEXT_COLOR))
        ctx.show_text(desc)
        ctx.new_path()
        
        algorithm_num += 1

    img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % frame)))
    cv2.imshow('Visualization', nda)
    cv2.waitKey(1)
    frame += 1
    if frame % 1000 == 0:
        print('Frame:', frame)

cv2.destroyAllWindows()


for sorted_left, sorted_right in zip(sorting_algorithms[::2], sorting_algorithms[1::2]):
    algo_name = sorted_left[0].split()[0]

    total_distance = 0
    for left, right in zip(sorted_left[1], sorted_right[1]):
        total_distance += abs(left - right)

    print(algo_name, 'Total Distance:', total_distance, 'Frames:', done[sorted_left[0]], done[sorted_right[0]])

ffmpeg.input(str(FRAMES_DIR.absolute() / 'frame%06d.png'), framerate=60).output('output.mp4', pix_fmt='yuv420p').overwrite_output().run()
