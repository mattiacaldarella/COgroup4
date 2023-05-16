import numpy as np
from problem import ProblemData, Tool, Request


def read_instance(instance):
    with open(instance) as f:
        # Create variable data_set(string)
        data_set = f.readline().split("= ")[1]

        # Create variable name(string)
        name = f.readline().split("= ")[1]

        # Skip line
        f.readline()

        # Create variable days(int)
        days = int(f.readline().split("= ")[1])

        # Create variable capacity(int)
        capacity = int(f.readline().split("= ")[1])

        # Create variable max_trip_distance(int)
        max_trip_distance = int(f.readline().split("= ")[1])

        # Create variable depot_coordinate(int)
        depot_coordinate = int(f.readline().split("= ")[1])

        # skip line
        f.readline()

        # Create variable vehicle_cost(int)
        vehicle_cost = int(f.readline().split("= ")[1])

        # Create variable vehicle_day_cost(int)
        vehicle_day_cost = int(f.readline().split("= ")[1])

        # Create variable distance_cost(int)
        distance_cost = int(f.readline().split("= ")[1])

        # Skip line
        f.readline()

        # Create variable number_of_tool_types(int)
        number_of_tool_types = int(f.readline().split("= ")[1].split("\n")[0])

        # Create variable tools(matrix, int)
        tools = []

        for i in range(number_of_tool_types):
            features = [int(i) for i in f.readline().split()]
            tools.append(Tool(*features))

        # Skip line
        f.readline()

        # Create variable number_of_coordinates(int)
        number_of_coordinates = int(f.readline().split("= ")[1].split("\n")[0])

        # Create variable coordinates(matrix, int)
        coordinates = np.zeros((number_of_coordinates, 3))

        for i in range(number_of_coordinates):
            features = [int(i) for i in f.readline().split()]
            coordinates[i] = features

        # Skip line
        f.readline()

        # Create variable number_of_requests
        number_of_requests = int(f.readline().split("= ")[1].split("\n")[0])

        # Create variable requests(matrix, int)[
        requests = []

        for i in range(number_of_requests):
            features = [int(i) for i in f.readline().split()]
            requests.append(Request(*features))

        return ProblemData(
            data_set,
            name,
            days,
            capacity,
            max_trip_distance,
            depot_coordinate,
            vehicle_cost,
            vehicle_day_cost,
            distance_cost,
            number_of_tool_types,
            tools,
            coordinates,
            requests,
        )
