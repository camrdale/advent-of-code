import numpy
import numpy.typing


def to_matrix(pattern: str) -> numpy.typing.NDArray[numpy.bool]:
    return numpy.array([[c for c in row] for row in pattern.split('/')]) == '#'


START = to_matrix('.#./..#/###')


def to_string(matrix: numpy.typing.NDArray[numpy.bool]) -> str:
    result = ''
    for row in matrix:
        for c in row:
            result += '#' if c else '.'
        result += '\n'
    return result[:-1]


def noop_flip(matrix: numpy.typing.NDArray[numpy.bool]) -> numpy.typing.NDArray[numpy.bool]:
    return matrix


def all_possible_orientations(matrix: numpy.typing.NDArray[numpy.bool]) -> set[bytes]:
    """Returns the bytes of all possible flipped/rotated versions of a matrix."""
    possible: set[bytes] = set()
    for _ in range(4):
        for flip_function in [noop_flip, numpy.fliplr, numpy.flipud]:
            possible.add(flip_function(matrix).tobytes())
        matrix = numpy.rot90(matrix)
    return possible


def split(matrix: numpy.typing.NDArray[numpy.bool]) -> list[list[numpy.typing.NDArray[numpy.bool]]]:
    """Splits a matrix into 2x2 or 3x3 sub-matrices to be enhanced."""
    size: int = matrix.shape[0]
    if size % 2 == 0:
        split_size = size // 2
    else:
        assert size % 3 == 0
        split_size = size // 3
    return [numpy.split(m, split_size, axis=1) for m in numpy.split(matrix, split_size, axis=0)]


def join(matrices: list[list[numpy.typing.NDArray[numpy.bool]]]) -> numpy.typing.NDArray[numpy.bool]:
    """Joins sub-matrices back into a single matrix."""
    return numpy.concatenate([numpy.concatenate(m, axis=1) for m in matrices], axis=0)


def build_enhancements(enhancement_input: list[str]) -> dict[bytes, numpy.typing.NDArray[numpy.bool]]:
    """Build a dict mapping all possible 2x2 and 3x3 matrices to the resulting enhanced matrix.
    
    Keys are the matrices in bytes.
    """
    enhancements: dict[bytes, numpy.typing.NDArray[numpy.bool]] = {}
    for line in enhancement_input:
        normalized_pattern, result_pattern = line.split(' => ')
        matrix = to_matrix(result_pattern)
        for possible in all_possible_orientations(to_matrix(normalized_pattern)):
            enhancements[possible] = matrix
    return enhancements


def enhance_matrix(
        matrix: numpy.typing.NDArray[numpy.bool],
        enhancements: dict[bytes, numpy.typing.NDArray[numpy.bool]]
        ) -> numpy.typing.NDArray[numpy.bool]:
    """Enhance a matrix by splitting into sub-matrices, enhancing those, then re-joining."""
    split_matrices = split(matrix)
    enhanced_matrices = [
        [enhancements[m.tobytes()] for m in row]
        for row in split_matrices]
    return join(enhanced_matrices)
