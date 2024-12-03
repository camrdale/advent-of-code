from pathlib import Path

import colorsys
import itertools

import cairo
import cv2
import numpy
import ffmpeg

FRAMES_DIR = Path(__file__).parent.resolve() / 'frames'
FRAMES_DIR.mkdir(exist_ok=True)
WIDTH = 1920
HEIGHT = 1080
FPS = 30
BACKGROUND_COLOR = (1.0, 1.0, 1.0)
TEXT_COLOR = (0.0, 0.0, 0.0)
# Mapping of delta values to the RGB color to use.
DELTA_COLORS = {
    7: (0.0, 0.5, 1.0),
    6: (8 / 360.0, 0.5, 1.0),
    5: (15 / 360.0, 0.5, 1.0),
    4: (25 / 360.0, 0.5, 1.0),
    3: (60 / 360.0, 0.5, 1.0),
    2: (75 / 360.0, 0.5, 1.0),
    1: (90 / 360.0, 0.5, 1.0),
    0: (185 / 360.0, 0.86, 0.86),
    -1: (185 / 360.0, 0.5, 1.0),
    -2: (200 / 360.0, 0.5, 1.0),
    -3: (215 / 360.0, 0.5, 1.0),
    -4: (230 / 360.0, 0.5, 1.0),
    }
NUM_PER_COL = 63
NUM_COLUMNS = 16
CELL_HEIGHT = 15
CELL_WIDTH= 15


class Report:
    """A report containing a list of the levels observed."""

    def __init__(self, levels: list[int]) -> None:
        self.levels = levels

    def __eq__(self, other: object) -> bool:
        if type(other) != Report:
            return False
        return tuple(self.levels) == tuple(other.levels)
    
    def __hash__(self) -> int:
        return hash((tuple(self.levels)))
    
    def deltas(self) -> list[int]:
        """Get a list of the changes in the levels."""
        return [self.levels[i] - self.levels[i-1] for i in range(1, len(self.levels))]
    
    def normalize(self) -> 'Report':
        """Normalize the levels to prefer increasing (reverses if decreasing)."""
        num_increasing = len([d for d in self.deltas() if d > 0])
        num_decreasing = len([d for d in self.deltas() if d < 0])
        if num_increasing < num_decreasing:
            normalized = list(self.levels)
            normalized.reverse()
            return Report(normalized)
        return self

    def safe(self) -> bool:
        """Check if the levels are safely increasing/decreasing."""
        deltas = self.deltas()
        return max(deltas) <= 3 and min(deltas) > 0

    def dampen(self) -> 'Report':
        """Dampen the report by removing at most one level."""
        deltas = self.deltas()
        dampened = list(self.levels)
        for i in range(len(deltas)):
            if deltas[i] <= 0 or deltas[i] > 3:
                if i+1 == len(deltas):
                    # Drop the last level/delta in a report
                    del dampened[i+1]
                elif 0 < deltas[i] + deltas[i+1] <= 3:
                    # Safe to add the delta to the following one.
                    del dampened[i+1]
                elif i != 0:
                    # Fallback to try adding the delta to the previous one
                    del dampened[i]
                else:
                    # i is 0 so the first level/delta in the report is dropped.
                    del dampened[i]
                break
        return Report(dampened)


class Visualizer:
    def __init__(self) -> None:
        self.img = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        self.nda = numpy.ndarray(shape = (HEIGHT, WIDTH, 4), dtype = numpy.uint8, buffer = self.img.get_data())
        self.ctx = cairo.Context(self.img)
        self.ffs = [
            cairo.ToyFontFace('Source Sans Pro Semibold'),
            cairo.ToyFontFace('Cascadia Mono'),
            cairo.ToyFontFace('Noto Color Emoji')]
        self.frame = 0
        [f.unlink() for f in FRAMES_DIR.glob("*.png") if f.is_file()]

    def draw_report(
            self, 
            i: int, 
            report: Report, 
            squished: float = 0.0, 
            alpha: float = 1.0, 
            alpha_only_index: int | None = None,
            squish_index: int | None = None
            ) -> None:
        row = i % NUM_PER_COL
        col = i // NUM_PER_COL
        deltas = report.deltas()

        for j, level in enumerate(report.levels):
            if j == 0:
                hls = (120 / 360, 0.5, 1.0)
            else:
                # Use the delta to determine the color, using HLS color space
                delta = min(max(deltas[j-1], -4), 7)
                hls = DELTA_COLORS[delta]

            if squish_index is not None:
                old_hls = hls
                levels = list(report.levels)
                del levels[squish_index]
                new_deltas = [levels[i] - levels[i-1] for i in range(1, len(levels))]
                new_deltas.insert(max(squish_index-1,0), 0)
                if j == 0 or (squish_index == 0 and j == 1):
                    new_hls = (120 / 360, 0.5, 1.0)
                else:
                    delta = min(max(new_deltas[j-1], -4), 7)
                    new_hls = DELTA_COLORS[delta]
                hls = (
                    old_hls[0] + squished * (new_hls[0] - old_hls[0]),
                    old_hls[1] + squished * (new_hls[1] - old_hls[1]),
                    old_hls[2] + squished * (new_hls[2] - old_hls[2]))

            x = WIDTH * col / NUM_COLUMNS + j * CELL_WIDTH
            if squished > 0.0:
                if squish_index is None:
                    x -= (j - (7 - 1) / 2) * squished * CELL_WIDTH
                else:
                    if j == squish_index:
                        continue
                    elif j > squish_index:
                        x -= CELL_WIDTH * squished
            y = 30 + (HEIGHT - 30) * row / NUM_PER_COL
            self.ctx.move_to(x, y)
            self.ctx.line_to(x + CELL_WIDTH, y)
            self.ctx.line_to(x + CELL_WIDTH, y + CELL_HEIGHT)
            self.ctx.line_to(x, y + CELL_HEIGHT)
            self.ctx.close_path()

            self.ctx.set_source_rgba(*colorsys.hls_to_rgb(*hls), alpha if alpha_only_index is None or alpha_only_index == j else 1.0)
            self.ctx.fill_preserve()

            # self.ctx.set_source_rgb(*TEXT_COLOR)
            # self.ctx.set_line_width(1)
            # self.ctx.stroke()

            self.ctx.set_font_face(self.ffs[0])
            self.ctx.set_font_size(12)
            text_extents = self.ctx.text_extents(str(level))
            
            self.ctx.move_to(x + CELL_WIDTH / 2 - text_extents.width / 2, y + CELL_HEIGHT - 2)
            self.ctx.set_source_rgba(*TEXT_COLOR, alpha if alpha_only_index is None or alpha_only_index == j else 1.0)
            self.ctx.show_text(str(level))
            self.ctx.new_path()

    def clear_screen(self) -> None:
        # Paint the background white (overwriting any previous frame's data)
        self.ctx.identity_matrix()
        self.ctx.set_source_rgba(*BACKGROUND_COLOR)
        self.ctx.paint()

    def draw_header(self, header: str) -> None:
        self.ctx.set_font_face(self.ffs[0])
        self.ctx.set_font_size(20)
        text_extents = self.ctx.text_extents(header)
        
        self.ctx.move_to(WIDTH / 2 - text_extents.width / 2, text_extents.height + 2)
        self.ctx.set_source_rgb(*TEXT_COLOR)
        self.ctx.show_text(header)
        self.ctx.new_path()

    def draw_reports(self, header: str, reports: list[Report], delay: int, safe_only: bool=False) -> None:
        for _ in range(delay * FPS):
            self.clear_screen()
            self.draw_header(header)
            for i, report in enumerate(reports):
                self.draw_report(i, report, alpha=(0.0 if safe_only and not report.safe() else 1.0))
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)

    def animate_normalization(self, header: str, reports: list[Report], normalized: list[Report], delay: int):
        num_frames = delay * FPS // 2
        for f in range(num_frames):
            self.clear_screen()
            self.draw_header(header)
            squished = f / num_frames
            for i, report in enumerate(reports):
                self.draw_report(i, report, squished=(squished if report != normalized[i] else 0.0))
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)
        num_frames = delay * FPS - num_frames
        for f in range(num_frames):
            self.clear_screen()
            self.draw_header(header)
            squished = (num_frames - f) / num_frames
            for i, report in enumerate(normalized):
                self.draw_report(i, report, squished=(squished if report != reports[i] else 0.0))
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)

    def animate_dampening(self, header: str, reports: list[Report], dampened: list[Report], delay: int):
        num_frames = delay * FPS // 2
        for f in range(num_frames):
            self.clear_screen()
            self.draw_header(header)
            for i, report in enumerate(reports):
                dampened_report = dampened[i]
                alpha = 1.0
                diff_index: int | None = None
                if len(dampened_report.levels) < len(report.levels):
                    alpha = 1.0 - f / (num_frames - 1)
                    diff_index = [k for k, (rl, dl) in enumerate(itertools.zip_longest(report.levels, dampened_report.levels)) if rl != dl][0]
                self.draw_report(i, report, alpha=alpha, alpha_only_index=diff_index)
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)
        num_frames = delay * FPS - num_frames
        for f in range(num_frames):
            self.clear_screen()
            self.draw_header(header)
            for i, report in enumerate(reports):
                dampened_report = dampened[i]
                squished = 0.0
                diff_index: int | None = None
                if len(dampened_report.levels) < len(report.levels):
                    squished = (f+1) / num_frames
                    diff_index = [k for k, (rl, dl) in enumerate(itertools.zip_longest(report.levels, dampened_report.levels)) if rl != dl][0]
                self.draw_report(i, report, squished=squished, squish_index=diff_index)
            self.img.write_to_png(str(FRAMES_DIR / ('frame%06d.png' % self.frame)))
            self.frame += 1
            cv2.imshow('Visualization', self.nda)
            cv2.waitKey(1)

    def fade_out_unsafe(self, header: str, reports: list[Report], delay: int):
        num_frames = delay * FPS
        for i in range(num_frames):
            self.clear_screen()
            self.draw_header(header)
            unsafe_alpha = 1.0 - i / (num_frames - 1)
            for i, report in enumerate(reports):
                self.draw_report(i, report, alpha=(1.0 if report.safe() else unsafe_alpha))
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

if __name__ == "__main__":
    report = Report([56, 54, 56, 62, 67])
    dampened_report = report.dampen()
    visualizer = Visualizer()
    visualizer.animate_dampening([report], [dampened_report], 5)
    visualizer.finalize()
