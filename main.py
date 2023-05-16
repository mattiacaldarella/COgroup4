import Optimize
import WriteResults
import os

from ReadInstance import read_instance
from PlotCoordinates import *
#from Optimize import optimize
from Optimize2 import optimize
from WriteResults import write_results
from validate import validate

from config import INSTANCES_DIR
# file_name = "challenge_r100d10_1.txt"

if __name__ == "__main__":

    valid_solutions = []
    invalid_solutions = []

    for file_name in os.listdir(INSTANCES_DIR):
        print(f"Reading {file_name}\n")
        problem_data = read_instance(os.path.join(INSTANCES_DIR, file_name))
        is_valid = False
        # print(problem_data)
        try:
            solution = optimize(problem_data)
            write_results(file_name, problem_data, solution)
            is_valid = validate(file_name)
        except Exception as e:
            print(f"Ignoring validation exception {e}\n")
        if is_valid:
            valid_solutions.append(file_name)
        else:
            invalid_solutions.append(file_name)
    print(f"VALID SOLUTIONS ({len(valid_solutions)}): {valid_solutions}\n")
    print(f"INVALID SOLUTIONS ({len(invalid_solutions)}): {invalid_solutions}\n")
