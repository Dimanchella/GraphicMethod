import copy
from functools import reduce

import suport


class FloatTable:
    table: list[list[float]]

    def __init__(self, list_2d: list[list[float]]):
        self.table = copy.deepcopy(list_2d)

    def __str__(self):
        chars = list(map(lambda row: list(map(
            lambda el: str(round(el, suport.OUTPUT_ACCURACY)), row
        )), self.table))
        max_char_len = max(list(map(
            lambda cs_row: max(list(map(len, cs_row))),
            chars
        )))
        for i in range(len(chars)):
            for j in range(len(chars[0])):
                chars[i][j] = ' ' * (max_char_len - len(chars[i][j])) + chars[i][j]
        return "\n".join(list(map(' '.join, chars)))

    def __copy__(self):
        return FloatTable(copy.deepcopy(self.table))


class Inequality:
    a: list[float]
    b: float
    sign: int

    def __init__(self, coefficients: list[float], sign: int, b: float = None):
        self.a = copy.copy(coefficients)
        self.sign = sign
        self.b = b

    def __copy__(self):
        return Inequality(self.a, self.sign, self.b)

    def __str__(self):
        string = f"{round(self.a[0], suport.OUTPUT_ACCURACY)}*x1"
        for i in range(1, len(self.a)):
            if self.a[i] < 0:
                string += " - "
            else:
                string += " + "
            string += f"{abs(round(self.a[i], suport.OUTPUT_ACCURACY))}*x{i + 1}"
        if self.b is not None:
            if self.sign == 1:
                string += " >= "
            elif self.sign == -1:
                string += " <= "
            else:
                string += " = "
            if type(self.b) is str:
                string += self.b
            else:
                string += f"{round(self.b, suport.OUTPUT_ACCURACY)}"
        else:
            string += f" -> {'max' if self.sign else 'min'}"
        return string
