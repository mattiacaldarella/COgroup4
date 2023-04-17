import Optimize
import WriteResults
import os

from ReadInstance import read_instance
from Optimize import optimize
from WriteResults import write_results

instance_dir = "instances"
file_name = "challenge_r100d10_1.txt"

if __name__ == "__main__":
	problem_data = read_instance(os.path.join(instance_dir, file_name))
	# print(problem_data)
	solution = optimize(problem_data)
	write_results(file_name, problem_data, solution)