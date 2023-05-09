import math

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

'''
def plot_coordinates3(problem_data: ProblemData):
    theta, r = polar_order(problem_data)

    fig, ax = plt.subplots()
    ax.scatter(problem_data.coordinates[:, 1], problem_data.coordinates[:, 2])
    for j in range(len(problem_data.coordinates[:, 1])):
        string = str(round(theta[j], 3))
        ax.annotate(string, (problem_data.coordinates[j, 1], problem_data.coordinates[j, 2]))
    plt.show()
'''
