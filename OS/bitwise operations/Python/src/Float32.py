# -----------------------------------------------------------
# Released under MIT Public License (MIT)
# (C) Alexander Isaychikov, Minsk, Belarus
# email isaychikov.ai@yahoo.com
# -----------------------------------------------------------

from src.Int32 import int32


class float32(int32):
    """
    The float32 class inherits int32 class and stores signed bitset
    with length of 32 bits, implementing sum operation following IEEE754 standart

    Parameters
    ----------
    value : int/list/Bitset
        Value for converting into binary format, or container to copy binary sequence from
    """

    def __init__(self, value):
        if type(value) in [type(int()), type(float())]:
            super().__init__(self.to_binary(value))
        else:
            super().__init__(value)

    def __add__(self, other):
        return float32.float_sum(self, other)

    def __str__(self):
        return str(self.to_decimal())

    def __repr__(self):
        return f"float32({self._binary()} = {str(self)})"

    def _binary(self):
        return super()._binary()

    def to_binary(self, decimal):
        out = int32(127)

        if decimal == 0:
            return 0

        while decimal >= 2:
            decimal /= 2
            out = out + 1

        while decimal < 1:
            decimal *= 2
            out = out - 1

        out = out << 23

        decimal -= 1

        for i in range(23):
            if pow(2, -i - 1) <= decimal:
                decimal -= pow(2, -i - 1)
                out[22 - i] = 1

        return out

    def to_decimal(self):
        output = 1
        exponent = (self >> 23).to_decimal() - 127

        exponent = pow(2, exponent)
        for i in range(23):
            if self[i] == 1:
                output += pow(2, i - 23)

        return output * exponent

    @staticmethod
    def float_sum(left, right):

        x1 = left
        x2 = right
        output = float32(0)
        bias = (x2 >> 23).to_decimal() - (x1 >> 23).to_decimal()

        mantis_x1 = (x1 << 9) >> 9
        mantis_x2 = (x2 << 9) >> 9
        mantis_x2[23] = 1
        mantis_x1[23] = 1

        if bias > 0:
            exponent = (x2 >> 23) << 23
            mantis_x1 = mantis_x1 >> bias
        elif bias < 0:
            bias = abs(bias)
            exponent = (x1 >> 23) << 23
            mantis_x2 = mantis_x2 >> bias
        else:
            exponent = (x1 >> 23) << 23

        output = int32(mantis_x1) + int32(mantis_x2)
        if output[23] == 0:
            output = output >> 1
            exponent = int32(exponent) + int32(int32(1) << 23)
        output[23] = 0

        output = output | exponent

        return float32(output)
