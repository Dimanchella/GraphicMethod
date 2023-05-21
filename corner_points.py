import copy
import operator
from itertools import combinations, product
from functools import reduce

from suport import SYSTEM_ACCURACY
from gauss import GaussMethod
from tables import Inequality


class BestCornerFinder:
    __points__: list[(float, float)]
    __result_point__: (float, float)
    __function__: Inequality
    __result_function__: Inequality
    __restrictions__: list[Inequality]
    __l__: float or str

    def __init__(
            self, function: list[float], restrictions_a: list[[float, float]],
            restrictions_b: list[float], restrictions_s: list[int], find_max: bool
    ):
        self.__function__ = Inequality(function, find_max)
        self.__restrictions__ = list(map(
            lambda a, s, b: Inequality(a, s, b),
            restrictions_a, restrictions_s, restrictions_b
        ))

    def get_function(self):
        return copy.copy(self.__function__)

    def get_restrictions(self):
        return copy.deepcopy(self.__restrictions__)

    def get_result_f(self):
        return copy.copy(self.__result_function__)

    def get_result_l(self):
        return self.__l__

    def get_corner_points(self):
        return copy.deepcopy(self.__points__)

    def get_result_point(self):
        return copy.copy(self.__result_point__)

    @staticmethod
    def __find_cross_point__(func1: Inequality, func2: Inequality):
        basis = [i for i in range(len(func1.a))]
        gm = GaussMethod([func1.a + [func1.b], func2.a + [func2.b]], basis)
        gm.calculate_gauss()
        if gm.get_result() is None:
            return None
        return tuple(map(lambda eq: eq[-1], gm.get_result().table))

    def __calculate_cross_points__(self):
        points = set()
        for rest_pair in combinations(self.__restrictions__, 2):
            point = self.__find_cross_point__(rest_pair[0], rest_pair[1])
            if point is not None:
                points.add(point)
        self.__points__ = list(points)

    @staticmethod
    def is_point_in_field(point: (float, float), functions: list[Inequality]):
        all_less_rests = list(map(
            lambda r: r if r.sign < 0 else Inequality(
                list(map(lambda a: a * -1, r.a)), False, r.b * -1
            ), functions
        ))
        return reduce(
            lambda b1, b2: b1 and b2,
            map(
                lambda r: round(sum(map(operator.mul, r.a, point)), SYSTEM_ACCURACY) <= r.b,
                all_less_rests
            )
        )

    def __calculate_corner_points__(self):
        self.__calculate_cross_points__()
        self.__points__ = list(filter(
            lambda p: self.is_point_in_field(p, self.__restrictions__), self.__points__
        ))
        pass

    def find_best_l(self):
        self.__calculate_corner_points__()
        if not len(self.__points__):
            return "No solutions"
        all_func_vals = dict(map(
            lambda p: (round(sum(map(operator.mul, self.__function__.a, p)), SYSTEM_ACCURACY), p),
            self.__points__
        ))

        result: float
        new_func: Inequality
        if self.__function__.sign > 0:
            result = max(all_func_vals)
            new_func = Inequality(
                self.__function__.a, self.__function__.sign * -1, result + 1
            )
        else:
            result = min(all_func_vals)
            new_func = Inequality(
                self.__function__.a, self.__function__.sign * -1, result - 1
            )
        points_in_field = reduce(lambda b1, b2: b1 or b2, map(
            lambda p: self.is_point_in_field(p, self.__restrictions__), filter(
                lambda p: p is not None, map(
                    lambda r: self.__find_cross_point__(r, new_func),
                    self.__restrictions__
                )
            )
        ))
        if points_in_field:
            self.__l__ = f"{'+' if self.__function__.sign > 0 else '-'}inf"
            self.__result_point__ = "No point"
        else:
            self.__l__ = result
            self.__result_point__ = all_func_vals[result]
        self.__result_function__ = Inequality(
            self.__function__.a, 0, self.__l__
        )
