# -----------------------------------------------------------
# Released under MIT Public License (MIT)
# (C) Alexander Isaychikov, Minsk, Belarus
# email isaychikov.ai@yahoo.com
# -----------------------------------------------------------

import warnings


class Bitset:
    """
    The Bitset class represents a sequence of bits and implements all bitwise operations

    Parameters
    ----------
    length : int
        Indicates length of bit sequence
    value : int/list/Bitset
        Value for converting into binary format, or container to copy binary sequence from
    sign_bit : bool
        Indicates whether the last bit should be used as sign bit or not

    Variables
    ---------
    length : int
        This is where we store length
    sign_bit : bool
        This is where we store sign bit usage flag
    container : list
        This is where we store sequence of bits
    """

    def __init__(self, length, value, sign_bit=True):

        self.length = length
        self.sign_bit = sign_bit

        if type(value) is type(int()):
            value = self.to_binary(value)
        elif type(value) is not type(list()):
            value = value.container
        self.container = value

    def to_binary(self, decimal):
        """
        Function to convert decimal into bit sequence

        Parameters
        ----------
        decimal : int
            Value in decimal format

        Returns
        -------
        list
            Value in binary format
        """

        overflow_check(self.length, decimal, self.sign_bit)

        output = [0] * self.length

        if self.sign_bit:
            length = self.length - 1
            output[length] = 0 if (decimal >= 0) else 1
            decimal = abs(decimal)
        else:
            length = self.length

        for i in range(length):
            output[i] = 1 if (int(decimal % 2) == 1) else 0
            decimal /= 2

        return output

    def to_decimal(self):
        """
        Function to convert binary into decimal

        Returns
        -------
        int
            Value in decimal format
        """

        length = self.length - 1 if (self.sign_bit == True) else self.length

        output = 0
        for i in range(length):
            output += self[i] * pow(2, i)
        return -output if (self.sign_bit is True and self[length] == 1) else output

    def _binary(self):
        s = ""
        for i, bit in enumerate(self.container):
            s = ("1" if bit == 1 else "0") + s
            if i < self.length - 1 and (i + 1) % 4 == 0:
                s = ' ' + s
        return s

    def __and__(self, other):
        other = Bitset._cast_to_bitset(other, self)

        length_equality_check(self, other)

        result = [0] * self.length
        for i in range(self.length):
            result[i] = 1 if (self[i] & other[i]) else 0

        return Bitset(self.length, result, sign_bit=self.sign_bit)

    def __or__(self, other):
        other = Bitset._cast_to_bitset(other, self)

        length_equality_check(self, other)

        result = [0] * self.length
        for i in range(self.length):
            result[i] = 1 if (self[i] | other[i]) else 0

        return Bitset(self.length, result, sign_bit=self.sign_bit)

    def __invert__(self):
        result = [0] * self.length
        for i in range(self.length):
            result[i] = 1 if (self[i] == 0) else 0

        return Bitset(self.length, result, sign_bit=self.sign_bit)

    def __xor__(self, other):
        other = Bitset._cast_to_bitset(other, self)

        length_equality_check(self, other)

        result = [0] * self.length
        for i in range(self.length):
            result[i] = 1 if (self[i] ^ other[i]) else 0

        return Bitset(self.length, result, sign_bit=self.sign_bit)

    def __lshift__(self, value):
        if value < 0:
            raise Exception("value must be positive")

        result = [0] * self.length
        result[value:self.length] = self[:(self.length - value)]

        return Bitset(self.length, result, sign_bit=self.sign_bit)

    def __rshift__(self, value):
        if value < 0:
            raise Exception("value must be positive")

        result = [0] * self.length
        result[:(self.length - value)] = self[value:self.length]

        return Bitset(self.length, result, sign_bit=self.sign_bit)

    def __eq__(self, other):
        other = Bitset._cast_to_bitset(other, self)
        return self.container == other.container

    def __ne__(self, other):
        other = Bitset._cast_to_bitset(other, self)
        return self.container != other.container

    def __lt__(self, other):
        other = Bitset._cast_to_bitset(other, self)
        return self.to_decimal() < other.to_decimal()

    def __gt__(self, other):
        other = Bitset._cast_to_bitset(other, self)
        return self.to_decimal() > other.to_decimal()

    def __le__(self, other):
        other = Bitset._cast_to_bitset(other, self)
        return self.to_decimal() <= other.to_decimal()

    def __ge__(self, other):
        other = Bitset._cast_to_bitset(other, self)
        return self.to_decimal() >= other.to_decimal()

    def __int__(self):
        return self.to_decimal()

    def __str__(self):
        return self._binary()

    def __repr__(self):
        return f"Bitset({str(self)})"

    def __getitem__(self, s):
        return self.container[s]

    def __setitem__(self, s, value):
        self.container[s] = value
        return self

    def __iter__(self):
        for i in self[:]:
            yield i

    def __len__(self):
        return self.length

    def _cast_to_bitset(value, example):
        if type(value) in [type(int()), type(list())]:
            return Bitset(example.length, value, example.sign_bit)
        return value


def overflow_check(length, decimal, sign_bit):
    length = length - 1 if sign_bit is True else length
    sign = -1 if sign_bit else 0
    if not sign * pow(2, length) - sign <= decimal <= pow(2, length) - 1:
        warnings.warn(f"\n Decimal {decimal} doesn't pass in the" + \
                      (" signed" if sign_bit is True else "") + \
                      f" bitset with range of " + \
                      f"[{sign * pow(2, length) - sign};{pow(2, length) - 1}] \n")


def length_equality_check(left, right):
    if left.length != right.length:
        raise Exception("length of both bitset variables must be equal")
    if left.sign_bit != right.sign_bit:
        raise Exception("both bitsets must be either signed or unsigned")
