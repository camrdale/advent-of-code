
def hash_function(s: str) -> int:
    h = 0
    for i, c in enumerate(s):
        h += 17**(len(s) - i)*ord(c)
    return h % 256
