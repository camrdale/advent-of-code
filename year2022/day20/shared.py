from aoc import log


class EncryptedNumber:
    def __init__(self, value: int):
        self.value = value
        self.mixed = False
        self.next: EncryptedNumber
        self.prev: EncryptedNumber

    def mix(self) -> None:
        self.mixed = True

    def insert(self, next: 'EncryptedNumber'):
        self.next = next
        self.prev = next.prev
        next.prev = self
        self.prev.next = self
    
    def pop(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        del self.prev
        del self.next
    
    def __repr__(self) -> str:
        return str(self.value)


class EncryptedFile:
    def __init__(self, input: list[str], decryption_key: int = 1):
        self.file_len = len(input)
        encrypted_file = EncryptedNumber(int(input[0]) * decryption_key)
        encrypted_file.next = encrypted_file
        encrypted_file.prev = encrypted_file
        self.original_order: list[EncryptedNumber] = [encrypted_file]
        self.zero_number: EncryptedNumber
        for line in input[1:]:
            number = EncryptedNumber(int(line) * decryption_key)
            self.original_order.append(number)
            number.insert(encrypted_file)
            if number.value == 0:
                self.zero_number = number
        assert self.zero_number is not None

    def mix(self):
        for number in self.original_order:
            next = number.next
            log.log(log.DEBUG, f'Moving {number.value} from between {number.prev.value} and {number.next.value}')
            number.pop()
            shift = number.value % (self.file_len - 1)
            if shift > (self.file_len - 1) // 2:
                shift = shift - (self.file_len - 1)
            if shift > 0:
                for _ in range(shift):
                    next = next.next
            if shift < 0:
                for _ in range(abs(shift)):
                    next = next.prev
            log.log(log.DEBUG, f'Shifting {number.value} {shift} spots to between {next.prev.value} and {next.value}')
            number.insert(next)
            log.log(log.DEBUG, self)

    def grove_coordinates(self) -> tuple[int, int, int]:
        next = self.zero_number

        for _ in range(1000):
            next = next.next
        number_1000th = next.value

        for _ in range(1000):
            next = next.next
        number_2000th = next.value

        for _ in range(1000):
            next = next.next
        number_3000th = next.value

        return (number_1000th, number_2000th, number_3000th)

    def __repr__(self) -> str:
        start = self.zero_number
        l: list[str] = [str(start)]
        next = start.next
        while next != start:
            l.append(str(next))
            next = next.next
        return ', '.join(l)
