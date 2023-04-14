instance = "/Users/jerry/GitHub/COgroup4/20 Instances CO2023/challenge_r100d10_1.txt"
import re
import numpy as np

def ReadInstance():
	with open(instance) as f:
		line = f.readline()
		dataSet = line.split("= ")[1]

		line = f.readline()
		name = line.split("= ")[1]

		# skip line
		line = f.readline() 


		line = f.readline()
		days = line.split("= ")[1]

		line = f.readline()
		capacity = line.split("= ")[1]

		line = f.readline()
		maxTripDistance = line.split("= ")[1]

		line = f.readline()
		depotCoordinate = line.split("= ")[1]

		# skip line
		line = f.readline() 

		line = f.readline()
		vehicleCost = line.split("= ")[1]

		line = f.readline()
		vehicleDayCost = line.split("= ")[1]

		line = f.readline()
		distanceCost = line.split("= ")[1]

		# skip line
		line = f.readline()

		line = f.readline()
		numberOfToolsTypes = int(line.split("= ")[1].split("\n")[0])

		tools = np.zeros((numberOfToolsTypes, 4))

		for i in range(numberOfToolsTypes):
			line=f.readline()
			features = np.asarray(line.split())

			tools[i] = features
	
		# skip line
		line = f.readline()

		line = f.readline()
		coordinateRows = int(line.split("= ")[1].split("\n")[0])
		
		coordinates = np.zeros((coordinateRows, 3))

		for i in range(coordinateRows):
			line=f.readline()
			features = np.asarray(line.split())

			coordinates[i] = features
			
		# skip line
		line = f.readline()

		line = f.readline()
		requestRows = int(line.split("= ")[1].split("\n")[0])
		
		requests = np.zeros((requestRows, 7))

		for i in range(requestRows):
			line=f.readline()
			features = np.asarray(line.split())

			requests[i] = features

	print(coordinates)


def Optimize():
	print("optimizing... \U0001f95d")



def WriteResults():
	print("writing results to file... \U0001f48d")



if __name__ == "__main__":
	ReadInstance()
	#Optimize()
	#WriteResults()
