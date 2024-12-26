
def next_secret(secret: int) -> int:
    mult = secret * 64
    secret = secret ^ mult
    secret = secret % 16777216
    div = secret // 32
    secret = secret ^ div
    secret = secret % 16777216
    mult2 = secret * 2048
    secret = secret ^ mult2
    secret = secret % 16777216
    return secret
