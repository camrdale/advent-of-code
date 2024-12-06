from pathlib import Path
from collections import defaultdict

import cairo
import cv2
import numpy
import ffmpeg

FRAMES_DIR = Path(__file__).parent.resolve() / 'frames'
FRAMES_DIR.mkdir(exist_ok=True)
WIDTH = 1280
HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (1.0, 1.0, 1.0)
TEXT_COLOR = (0.0, 0.0, 0.0)
OBSTACLE_COLOR = (1.0, 0.0, 0.0)
GUARD_COLOR = (0.0, 0.66, 0.0)
VISITED_COLOR = (0.5, 1.0, 0.5)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Visualizer:
    def __init__(self, width: int, height: int) -> None:
        self.cell_width = WIDTH / width
        self.cell_height = HEIGHT / height
        self.img = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        self.nda = numpy.ndarray(shape = (HEIGHT, WIDTH, 4), dtype = numpy.uint8, buffer = self.img.get_data())
        self.ctx = cairo.Context(self.img)
        self.ffs = [
            cairo.ToyFontFace('Source Sans Pro Semibold'),
            cairo.ToyFontFace('Cascadia Mono'),
            cairo.ToyFontFace('Noto Color Emoji')]
        self.frame = 0
        [f.unlink() for f in FRAMES_DIR.glob("*.png") if f.is_file()]

    def draw_obstacle(
            self, 
            pos: tuple[int, int], 
            ) -> None:
        x = self.cell_width * pos[0]
        y = self.cell_height * pos[1]

        self.ctx.move_to(x, y)
        self.ctx.line_to(x + self.cell_width, y)
        self.ctx.line_to(x + self.cell_width, y + self.cell_height)
        self.ctx.line_to(x, y + self.cell_height)
        self.ctx.close_path()

        self.ctx.set_source_rgb(*OBSTACLE_COLOR)
        self.ctx.fill()

    def draw_visited(
            self, 
            pos: tuple[int, int], 
            directions: set[int]
            ) -> None:
        x = self.cell_width * pos[0]
        y = self.cell_height * pos[1]

        self.ctx.move_to(x, y)
        self.ctx.line_to(x + self.cell_width, y)
        self.ctx.line_to(x + self.cell_width, y + self.cell_height)
        self.ctx.line_to(x, y + self.cell_height)
        self.ctx.close_path()

        self.ctx.set_source_rgb(*VISITED_COLOR)
        self.ctx.fill()

        if len(directions & set([UP, DOWN])) > 0:
            self.ctx.move_to(x + self.cell_width / 2, y)
            self.ctx.line_to(x + self.cell_width / 2, y + self.cell_height)
        if len(directions & set([LEFT, RIGHT])) > 0:
            self.ctx.move_to(x, y + self.cell_height / 2)
            self.ctx.line_to(x + self.cell_width, y + self.cell_height / 2)
        self.ctx.set_source_rgb(*TEXT_COLOR)
        self.ctx.set_line_width(3)
        self.ctx.stroke()
        self.ctx.new_path()


    def draw_guard(
            self,
            pos: tuple[int, int], 
            direction: int, 
            offset: tuple[float, float] = (0.0, 0.0)) -> None:
        x = self.cell_width * (pos[0] + offset[0])
        y = self.cell_height * (pos[1] + offset[1])

        if direction == UP:
            self.ctx.move_to(x, y + self.cell_height)
            self.ctx.line_to(x + self.cell_width / 2, y)
            self.ctx.line_to(x + self.cell_width, y + self.cell_height)
            self.ctx.close_path()
        if direction == DOWN:
            self.ctx.move_to(x, y)
            self.ctx.line_to(x + self.cell_width / 2, y + self.cell_height)
            self.ctx.line_to(x + self.cell_width, y)
            self.ctx.close_path()
        if direction == RIGHT:
            self.ctx.move_to(x, y)
            self.ctx.line_to(x + self.cell_width, y + self.cell_height / 2)
            self.ctx.line_to(x, y + self.cell_height)
            self.ctx.close_path()
        if direction == LEFT:
            self.ctx.move_to(x + self.cell_width, y)
            self.ctx.line_to(x, y + self.cell_height / 2)
            self.ctx.line_to(x + self.cell_width, y + self.cell_height)
            self.ctx.close_path()

        self.ctx.set_source_rgb(*GUARD_COLOR)
        self.ctx.fill()
        self.ctx.set_line_width(1)
        self.ctx.stroke()

    def clear_screen(self) -> None:
        # Paint the background white (overwriting any previous frame's data)
        self.ctx.identity_matrix()
        self.ctx.set_source_rgba(*BACKGROUND_COLOR)
        self.ctx.paint()

    def draw_board(
            self,
            obstacles: set[tuple[int, int]], 
            visited_positions: set[tuple[int, int, int]], 
            current_pos: tuple[int, int], 
            direction: int, 
            delay: int) -> None:
        num_frames = delay * FPS // 2
        for _ in range(num_frames):
            self.clear_screen()
            for pos in obstacles:
                self.draw_obstacle(pos)
            positions: dict[tuple[int, int], set[int]] = defaultdict(set)
            for pos in visited_positions:
                positions[(pos[0], pos[1])].add(pos[2])
            for pos, directions in positions.items():
                self.draw_visited(pos, directions)
            self.draw_guard(current_pos, direction)
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)

    def animate_movement(
            self,
            obstacles: set[tuple[int, int]], 
            visited_positions: set[tuple[int, int, int]], 
            current_pos: tuple[int, int], 
            next_pos: tuple[int, int], 
            direction: int, 
            delay: float) -> None:
        num_frames = int(delay * FPS)
        for f in range(num_frames):
            self.clear_screen()
            for pos in obstacles:
                self.draw_obstacle(pos)
            positions: dict[tuple[int, int], set[int]] = defaultdict(set)
            for pos in visited_positions:
                if pos != current_pos + (direction,):
                    positions[(pos[0], pos[1])].add(pos[2])
            for pos, directions in positions.items():
                self.draw_visited(pos, directions)
            offset: tuple[float, float] = (
                (next_pos[0] - current_pos[0]) * f / num_frames,
                (next_pos[1] - current_pos[1]) * f / num_frames
            )
            self.draw_guard(current_pos, direction, offset=offset)
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)

    def finalize(self) -> None:
        cv2.destroyAllWindows()

    def outputMovie(self, filename: Path) -> None:
        (ffmpeg
            .input(str(FRAMES_DIR.absolute() / 'frame%06d.png'), framerate=FPS)
            .output(str(filename), pix_fmt='yuv420p')
            .overwrite_output()
            .run())
