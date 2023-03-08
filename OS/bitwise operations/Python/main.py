# -----------------------------------------------------------
# Released under MIT Public License (MIT)
# (C) Alexander Isaychikov, Minsk, Belarus
# email isaychikov.ai@yahoo.com
# -----------------------------------------------------------

from src.Int32 import int32
from src.Float32 import float32


if __name__ == '__main__':

    x = 4
    y = 19

    print('-' * 100)

    for a, b in zip([int32(x), int32(-x), int32(x), int32(-x)], [int32(y), int32(y), int32(-y), int32(-y)]):
        print(f'[SIGNED]\t {a} + {b} = {int32.sum_signed(a, b)}')
        print(f'[INVERSE]\t {a} + {b} = {int32.sum_inverse(a, b)}')
        print(f'[COMPLIMENTARY]\t {a} + {b} = {int32.sum_complimentary(a, b)}')

    print('-' * 100)

    for a, b in zip([int32(x), int32(-x), int32(x), int32(-x)], [int32(y), int32(y), int32(-y), int32(-y)]):
        print(f'[MUL]\t {a} * {b} = {a * b}')
        print(f'[DIV]\t {a} / {b} = {a / b}')

    print('-' * 100)

    x = 0.5
    y = 0.235

    for a, b in zip([float32(x)], [float32(y)]):
        print(f'[SUM]\t {a} + {b} = {a + b}')

    print('-' * 100)
