import re


TWO_DOUBLE_LETTERS = re.compile(r'(.)\1.*(.)\2')
STRAIGHT = re.compile(r'(abc|bcd|cde|def|efg|fgh|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)')
ILLEGAL_LETTERS = re.compile(r'[ilo]')


def valid(string: str) -> bool:
    if TWO_DOUBLE_LETTERS.search(string) is None:
        return False
    if STRAIGHT.search(string) is None:
        return False
    return True


def increment(password: list[str], letter: int = 7) -> None:
    password[letter] = chr(ord(password[letter]) + 1)
    if password[letter] in ('i', 'l', 'o'):
        password[letter] = chr(ord(password[letter]) + 1)
    elif password[letter] > 'z':
        password[letter] = 'a'
        increment(password, letter - 1)


def next_password(password_str: str) -> str:
    password = list(password_str)

    if m := ILLEGAL_LETTERS.search(password_str):
        for i in range(m.start() + 1, len(password)):
            password[i] = 'a'
        increment(password, letter=m.start())
    else:
        increment(password)

    while not valid(''.join(password)):
        increment(password)

    return ''.join(password)
