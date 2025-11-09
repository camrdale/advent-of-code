def xmas_invalid(data: list[int], preamble: int) -> int:
        for i in range(preamble, len(data)):
            next = data[i]
            for value in data[i-preamble:i]:
                if next - value == value:
                    continue
                if (next - value) in data[i-preamble:i]:
                    break
            else:
                return next

        raise ValueError(f'Failed to find a number that is invalid')
