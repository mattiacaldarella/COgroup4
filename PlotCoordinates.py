import math
import numpy as np

from problem import ProblemData
#from Optimize2 import polar_order
import matplotlib.pyplot as plt

def plot_coordinates1(problem_data: ProblemData):
    plt.scatter(problem_data.coordinates[:, 1], problem_data.coordinates[:, 2])
    plt.show()

def plot_coordinates2(lst: list, problem_data: ProblemData):
    lst1 = []
    for i in range(len(lst)):
        id = lst[i].location_id
        lst1.append(problem_data.coordinates[id])

    x = [d[1] for d in lst1]
    y = [d[2] for d in lst1]

    fig, ax = plt.subplots()
    ax.scatter(x, y)

    i = 0
    for d in lst1:
        i += 1
        string = str(i)
        ax.annotate(string, (d[1], d[2]))

    plt.show()

def visualize(solution, problem_data):
    first_day = solution.routes[1]
    print(problem_data)
    print(solution.routes)
    all_locs_ids = []

    for i in range(len(first_day)):
        loc_ids = []
        for j in first_day[i]:
            request_id = j
            if request_id != 0:
                loc_id = problem_data.requests[request_id - 1].location_id
                list_coordinate = problem_data.coordinates[loc_id - 1]
                x = list_coordinate[1]
                y = list_coordinate[2]
                loc_ids.append((x, y))
            else:
                list_coordinate = problem_data.coordinates[problem_data.depot_coordinate]
                x = list_coordinate[1]
                y = list_coordinate[2]

                loc_ids.append((x, y))

            all_locs_ids.append(loc_ids)
    print(all_locs_ids)

    # Plot each route
    for route in all_locs_ids:
        x_values = [point[0] for point in route]
        y_values = [point[1] for point in route]
        plt.plot(x_values, y_values, marker='o')

    # Add labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Routes')

    # Set the aspect ratio to 'equal' for a square plot
    plt.axis('equal')

    # Display the plot
    plt.show()
'''
def visualize2(solution, problem_data):

def plot_coordinates3(problem_data: ProblemData):
    theta, r = polar_order(problem_data)

    fig, ax = plt.subplots()
    ax.scatter(problem_data.coordinates[:, 1], problem_data.coordinates[:, 2])
    for j in range(len(problem_data.coordinates[:, 1])):
        string = str(round(theta[j], 3))
        ax.annotate(string, (problem_data.coordinates[j, 1], problem_data.coordinates[j, 2]))
    plt.show()
'''
