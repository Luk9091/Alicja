def fromU1toInt(data: int, bitSize: int = 8) -> int:
    sign = 1
    if data & (1 << (bitSize - 1)):
        sign = -1
        data = ~data
    return sign * (data & ((1 << bitSize) -1))