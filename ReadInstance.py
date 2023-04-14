from main import instance
import numpy as np

with open(instance) as f:
	# Create variable data_set(string)
	line = f.readline()
	data_set = line.split("= ")[1]

    # Create variable name(string)
	line = f.readline()
	name = line.split("= ")[1]

	# Skip line
	line = f.readline() 

    # Create variable days(int)
	line = f.readline()
	days = int(line.split("= ")[1])

    # Create variable capacity(int)
	line = f.readline()
	capacity = int(line.split("= ")[1])

    # Create variable max_trip_distance(int)
	line = f.readline()
	max_trip_distance = int(line.split("= ")[1])

    # Create variable depot_coordinate(int)
	line = f.readline()
	depot_coordinate = int(line.split("= ")[1])

	# skip line
	line = f.readline() 

    # Create variable vehicle_cost(int)
	line = f.readline()
	vehicle_cost = int(line.split("= ")[1])

    # Create variable vehicle_day_cost(int)
	line = f.readline()
	vehicle_day_cost = int(line.split("= ")[1])

    # Create variable distance_cost(int)
	line = f.readline()
	distance_cost = int(line.split("= ")[1])

	# Skip line
	line = f.readline()

    # Create variable number_of_tool_types(int)
	line = f.readline()
	number_of_tool_types = int(line.split("= ")[1].split("\n")[0])

    # Create variable tools(matrix, int)
	tools = np.zeros((number_of_tool_types, 4))

	for i in range(number_of_tool_types):
		line=f.readline()
		features = np.asarray(line.split())

		tools[i] = features
	
	# Skip line
	line = f.readline()

    # Create variable number_of_coordinates(int)
	line = f.readline()
	number_of_coordinates = int(line.split("= ")[1].split("\n")[0])
	
    # Create variable coordinates(matrix, int)
	coordinates = np.zeros((number_of_coordinates, 3))

	for i in range(number_of_coordinates):
		line=f.readline()
		features = np.asarray(line.split())

		coordinates[i] = features
			
	# Skip line
	line = f.readline()

    # Create variable number_of_requests
	line = f.readline()
	number_of_requests = int(line.split("= ")[1].split("\n")[0])
	
    # Create variable requests(matrix, int)
	requests = np.zeros((number_of_requests, 7))

	for i in range(number_of_requests):
		line=f.readline()
		features = np.asarray(line.split())

		requests[i] = features