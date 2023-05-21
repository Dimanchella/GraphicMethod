import copy

from matplotlib import hatch
import matplotlib.pyplot as plt
import numpy as np

from tables import Inequality
from suport import SYSTEM_ACCURACY

LIMITS_X = (-4, 4)
LIMITS_Y = (-4, 4)
NUM_POINTS = 81
LINE_WIDTH = 2
HIGHLIGHT_LINE_WIDTH = 5
COLORS = ['b', 'g', 'c', 'm', 'y', 'k']
HATCHES = ['//', '\\\\', '||', '--', 'oo', 'O', '.']
ALPHA_COLOR = 0.15
FUNC_COLOR = 'b'
HL_FUNC_COLOR = 'r'
POINT_SIZE = 7
POINT_COLOR = 'k'
POINT_HATCH = 'o'
HL_POINT_COLOR = 'y'
HL_POINT_HATCH = '*'


class Plotter:
    __functions__: list[Inequality]
    __points__: list[(float, float)]
    __hl_function__: Inequality
    __hl_point__: (float, float)
    __y_down__ = np.array([LIMITS_Y[0]] * NUM_POINTS)
    __y_up__ = np.array([LIMITS_Y[1]] * NUM_POINTS)

    def __init__(
            self, function: list[Inequality], points: list[(float, float)],
            hl_function: Inequality, hl_point: (float, float)
    ):
        self.__functions__ = copy.deepcopy(function)
        self.__points__ = copy.deepcopy(points)
        self.__hl_function__ = copy.copy(hl_function)
        self.__hl_point__ = copy.copy(hl_point)

    @staticmethod
    def __generate_color__():
        ind = 0
        while True:
            yield COLORS[ind]
            ind = (ind + 1) % len(COLORS)

    @staticmethod
    def __generate_hatch__():
        ind = 0
        while True:
            yield HATCHES[ind]
            ind = (ind + 1) % len(HATCHES)

    @staticmethod
    def __calculate_y_from_x__(func: Inequality):
        x = np.linspace(*LIMITS_X, NUM_POINTS)
        y = np.round(
            (func.b - func.a[0] * x)
            / func.a[1],
            SYSTEM_ACCURACY
        )
        return x, y

    @staticmethod
    def __calculate_zero_x__():
        y = np.linspace(*LIMITS_Y, NUM_POINTS)
        x = np.array([0 for _ in range(NUM_POINTS)])
        return x, y

    def __build_hl_function__(self, ax):
        x, y = self.__calculate_y_from_x__(self.__hl_function__) \
            if self.__hl_function__.a[1] != 0 \
            else self.__calculate_zero_x__()
        ax.plot(
            x, y, linewidth=HIGHLIGHT_LINE_WIDTH, color=HL_FUNC_COLOR,
            label=str(self.__hl_function__)
        )

    def __build_ineq_function__(self, ax, func: Inequality, hatch: str):
        if func.a[1] != 0:
            x, y = self.__calculate_y_from_x__(func)
            if func.sign < 0 < func.a[1] or func.sign > 0 > func.a[1]:
                ax.fill_between(
                    x, y, self.__y_down__, where=(y >= self.__y_down__), alpha=ALPHA_COLOR,
                    color=FUNC_COLOR, hatch=hatch, interpolate=True
                )
            elif func.sign > 0 < func.a[1] or func.sign < 0 > func.a[1]:
                ax.fill_between(
                    x, y, self.__y_up__, where=(y <= self.__y_up__), alpha=ALPHA_COLOR,
                    color=FUNC_COLOR, hatch=hatch, interpolate=True
                )
        else:
            x, y = self.__calculate_zero_x__()
            x_hide = np.linspace(*LIMITS_X, NUM_POINTS)
            if func.sign < 0 < func.a[0] or func.sign > 0 > func.a[0]:
                x_hide = list(filter(lambda x_h: x_h <= func.b, x_hide))
            elif func.sign > 0 < func.a[0] or func.sign < 0 > func.a[0]:
                x_hide = list(filter(lambda x_h: x_h >= func.b, x_hide))
            y_hide_up = self.__y_up__[:len(x_hide)]
            y_hide_down = self.__y_down__[:len(x_hide)]
            ax.fill_between(
                x_hide, y_hide_up, y_hide_down, where=(y_hide_up >= y_hide_down),
                alpha=ALPHA_COLOR, color=FUNC_COLOR, hatch=hatch, interpolate=True
            )
        ax.plot(x, y, linewidth=LINE_WIDTH, color=FUNC_COLOR)

    def __build_hl_point__(self, ax):
        ax.plot(
            *self.__hl_point__, f"{HL_POINT_COLOR}{HL_POINT_HATCH}",
            markersize=POINT_SIZE, label=str(self.__hl_point__)
        )

    def __build_points__(self, ax):
        for point in self.__points__:
            ax.plot(
                *point, f"{POINT_COLOR}{POINT_HATCH}",
                markersize=POINT_SIZE, label=str(point)
            )

    def build_plot(self):
        fig, ax = plt.subplots()
        ax.grid(True)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_xlim(*LIMITS_X)
        ax.set_ylim(*LIMITS_Y)

        if self.__hl_function__ is not None and type(self.__hl_function__.b) is not str:
            self.__build_hl_function__(ax)

        gen_htch = self.__generate_hatch__()
        for func in self.__functions__:
            self.__build_ineq_function__(ax, func, next(gen_htch))

        self.__build_points__(ax)
        if self.__hl_point__ is not None and type(self.__hl_point__) is not str:
            self.__build_hl_point__(ax)

        plt.legend()
        plt.show()
