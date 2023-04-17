import Optimize
import WriteResults
import os

from ReadInstance import read_instance

instance_dir = "20 Instances CO2023"
file_name = "challenge_r100d10_1.txt"

if __name__ == "__main__":
	problem_data = read_instance(os.path.join(instance_dir, file_name))
	# print(problem_data)
	#Optimize
	#WriteResults