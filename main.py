import os
from pytictoc import TicToc
from ReadInstance import read_instance
from Optimizer import optimize
from WriteResults import write_results
from validate import validate
from config import INSTANCES_DIR

if __name__ == "__main__":
    valid_solutions = []
    invalid_solutions = []

    for file_name in os.listdir(INSTANCES_DIR):
        t = TicToc()
        t.tic()
        print(f"Reading {file_name}\n")
        problem_data = read_instance(os.path.join(INSTANCES_DIR, file_name))
        is_valid = False

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
            
        t.toc()
    print(f"VALID SOLUTIONS ({len(valid_solutions)}): {valid_solutions}\n")
    print(f"INVALID SOLUTIONS ({len(invalid_solutions)}): {invalid_solutions}\n")
