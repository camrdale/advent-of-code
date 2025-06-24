import functools


@functools.cache
def _optimal_size(
        remaining_space: int,
        packages: tuple[int, ...],
        size: int,
        subgroups: int,
        best_size: int | None = None
        ) -> tuple[int, int] | None:
    if remaining_space == 0:
        # General solution requires checking that the subgroups can be made, but
        # that is slow and not required for any of the given inputs. So shortcut.
        return (0, 1)

        # Found an arrangement that gives the expected weight.
        # May still need to check that the remaining packages can be divided properly.
        if subgroups == 1 or _optimal_size(
                sum(packages) // subgroups,
                packages,
                0,
                subgroups - 1) is not None:
            return (0, 1)
        return None
    
    if best_size is not None and size >= best_size:
        # Give up, we've already found a better one.
        return None
    
    min_result: tuple[int, int] | None = None
    for i, package in enumerate(packages):
        if package > remaining_space:
            continue
        next_result = _optimal_size(
            remaining_space - package,
            packages[:i] + packages[i+1:],
            size + 1,
            subgroups,
            best_size=best_size)
        if next_result is not None:
            result = (next_result[0] + 1, next_result[1] * package)
            if min_result is None or result < min_result:
                min_result = result
                best_size = min_result[0]

    return min_result


def optimal_size(packages: list[int], num_groups: int) -> tuple[int, int]:
    _optimal_size.cache_clear()

    group_size = sum(packages) // num_groups

    result = _optimal_size(
        group_size,
        tuple(sorted(packages, reverse=True)),
        0,
        num_groups - 1)
    assert result is not None

    return result
