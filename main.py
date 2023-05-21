import json
import sys

from corner_points import BestCornerFinder
from plotting import Plotter
import suport

ERROR_CODE = -1

if __name__ == '__main__':
    function: list[float]
    restrictions_a: list[[float, float]]
    restrictions_b: list[float]
    restrictions_s: list[int]
    find_max: bool
    try:
        with open("input1.json", "r") as json_file:
            input_dict = json.load(json_file)
            function = input_dict["F"]
            restrictions_a = input_dict["A"]
            restrictions_b = input_dict["B"]
            restrictions_s = input_dict["SIGN"]
            find_max = input_dict["MAX"]
        # error_check(sources, purposes, table)
    except FileNotFoundError as fnfe:
        print(f"Файл input1.json не найден.\n{fnfe}")
        sys.exit(ERROR_CODE)

    bcf = BestCornerFinder(function, restrictions_a, restrictions_b, restrictions_s, find_max)
    bcf.find_best_l()
    print(f"FUNCTION: {bcf.get_function()}\n\n"
          f"RESTRICTIONS:\n" + '\n'.join(map(str, bcf.get_restrictions()))
          + f"\nCORNER POINTS: " + ' '.join(map(str, bcf.get_corner_points()))
          + f"\n\nRESULT POINT: {bcf.get_result_point()}"
          + f"\nRESULT FUNCTION: {bcf.get_result_f()}")
    plotter = Plotter(
        bcf.get_restrictions(), bcf.get_corner_points(),
        bcf.get_result_f(), bcf.get_result_point()
    )
    plotter.build_plot()
