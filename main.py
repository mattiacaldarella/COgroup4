import Optimize
import WriteResults
import os

from ReadInstance import read_instance
from Optimize import optimize
from WriteResults import write_results
from validate import validate

from config import INSTANCES_DIR
# file_name = "challenge_r100d10_1.txt"

if __name__ == "__main__":
    valid_solutions = []
    for file_name in os.listdir(INSTANCES_DIR):
        print(f"Reading {file_name}")
        problem_data = read_instance(os.path.join(INSTANCES_DIR, file_name))
        # print(problem_data)
        try:
            solution = optimize(problem_data)
            write_results(file_name, problem_data, solution)
            is_valid = validate(file_name)
        except Exception as e:
            print(f"Ignoring validation exception {e}")
        else:
            if is_valid:
                valid_solutions.append(file_name)
    print(f"VALID SOLUTIONS: {valid_solutions}")