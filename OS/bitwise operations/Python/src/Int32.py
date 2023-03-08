# -----------------------------------------------------------
# Released under MIT Public License (MIT)
# (C) Alexander Isaychikov, Minsk, Belarus
# email isaychikov.ai@yahoo.com
# -----------------------------------------------------------

from src.Bitset import Bitset


class int32(Bitset):
    """
    The int32 class inherits Bitset class and stores signed bitset
    with length of 32 bits, implementing standard arithmetic operations

    Parameters
    ----------
    value : int/list/Bitset
        Value for converting into binary format, or container to copy binary sequence from
    """

    def __init__(self, value):
        super().__init__(32, value, sign_bit=True)

    def __add__(self, other):
        return int32.summation(self, other)

    def __sub__(self, other):
        return int32.summation(self, -other)

    def __neg__(self):
        return self ^ (int32(1) << 31)

    def __mul__(self, other):
        return int32.mul(self, other)

    def __truediv__(self, other):
        return int32.div(self, other)

    def __str__(self):
        return str(self.to_decimal())

    def __repr__(self):
        return f"int32({self._binary()} = {str(self)})"

    def _binary(self):
        return super()._binary()

    @staticmethod
    def sum_signed(left, right):

        x1 = left
        x2 = right
        shift = int32(0)

        while x2 != 0:
            shift = x1 & x2
            x1 = x1 ^ x2
            x2 = shift << 1

        return int32(x1)

    @staticmethod
    def sum_inverse(left, right):

        x1 = left
        x2 = right
        sign_bit = len(left) - 1
        overflow = int32(0)
        shift = int32(0)

        if x1[sign_bit] == 1:
            x1 = ~x1
            x1[sign_bit] = 1

        if x2[sign_bit] == 1:
            x2 = ~x2
            x2[sign_bit] = 1

        overflow = int32._get_overflow(x1, x2)

        while x2 != 0:
            shift = x1 & x2
            x1 = x1 ^ x2
            x2 = shift << 1

        x1 = int32.sum_signed(x1, overflow)

        if x1[sign_bit] == 1:
            x1 = ~x1
            x1[sign_bit] = 1

        return int32(x1)

    @staticmethod
    def sum_complimentary(left, right):

        x1 = int32(left)
        x2 = int32(right)
        sign_bit = len(left) - 1
        shift = int32(0)

        if x1[sign_bit] == 1:
            x1 = ~x1
            x1[sign_bit] = 1
            x1 = int32.sum_signed(x1, 1)

        if x2[sign_bit] == 1:
            x2 = ~x2
            x2[sign_bit] = 1
            x2 = int32.sum_signed(x2, 1)

        while x2 != 0:
            shift = x1 & x2
            x1 = x1 ^ x2
            x2 = shift << 1

        if x1[sign_bit] == 1:
            x1 = ~x1
            x1[sign_bit] = 1
            x1 = int32.sum_signed(x1, 1)

        return int32(x1)

    @staticmethod
    def summation(left, right):
        return int32(int32.sum_complimentary(left, right))

    @staticmethod
    def mul(left, right):

        x1 = left
        x2 = right
        result = int32(0)
        sign = int32(0)

        sign = ((x1 ^ x2) >> 31) << 31
        x1[31] = 0
        x2[31] = 0

        while x2 != 0:
            if x2[0] == 1:
                result = int32.sum_complimentary(result, x1)

            x1 = x1 << 1
            x2 = x2 >> 1

        result = result | sign

        return int32(result)

    @staticmethod
    def div(left, right):

        x1 = int32(left)
        x2 = int32(right)
        counter = int32(1)
        quotient = int32(0)
        sign = ((x1 ^ x2) >> 31) << 31

        x1[31] = 0
        x2[31] = 0

        while x2 <= x1:
            x2 = x2 << 1
            counter = counter << 1

        while counter > 1:
            x2 = x2 >> 1
            counter = counter >> 1
            if x1 >= x2:
                x1 = int32(x1) - int32(x2)
                quotient = int32.sum_complimentary(quotient, counter)

        quotient = quotient | sign

        return int32(quotient)

    def _get_overflow(left, right):

        last_bit = len(left) - 1
        x1 = left
        x2 = right
        shift = int32(0)

        while x2 != int32(0):
            shift = x1 & x2
            if shift[last_bit] == 1:
                return 1

            x1 = x1 ^ x2
            x2 = shift << 1

        return 0
