import math

import gurobipy as gp
from gurobipy import GRB

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial import distance_matrix
from problem import ProblemData
import matplotlib.pyplot as plt
from PlotCoordinates import plot_coordinates2

def optimize2(problem_data: ProblemData):
    dic = day_divider(problem_data)
    theta, r = polar_order(problem_data)
    dist_matrix = distance_matrix1(problem_data)

    for j in sorted(dic.keys()):
        print(sweep_method(theta, dic[j], problem_data, dist_matrix))
        exit()

def day_divider(problem_data: ProblemData):
    dic = {}
    for request in problem_data.requests:
        fd = request.first_day
        if fd in dic.keys():
            dic[fd].append(request)
        else:
            dic[fd] = [request]
    return dic

def sweep_method(theta: list, lst: list, problem_data: ProblemData, dist_matrix: np.ndarray):
    sort = sort_request(theta, lst)

    routes = []

    # create a dictionary mapping tool IDs to their sizes
    tool_sizes = {tool.id: tool.size for tool in problem_data.tools}

    i = 0

    while i < len(sort):
        next_request_cap = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed
        capacity = problem_data.capacity
        route = []
        while capacity >= next_request_cap:
            print(i)
            route.append(sort[i].location_id)
            capacity -= next_request_cap
            next_request_cap = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed
            i += 1

        route.append(0)
        test, rout = gurobi(route, problem_data, dist_matrix)

        while test == False:
            route = np.delete(route, np.where(r == 0)) #wrong
            del route[-1]
            route.append(0)
            test, rout = gurobi(route, dist_matrix)
            i -= 1

        routes.append(rout)

    return routes

def gurobi(route: list, problem_data: ProblemData, dist_matrix: np.ndarray):
    m = gp.Model()
    # Create a boolean mask to select the relevant rows and columns
    mask = np.zeros(dist_matrix.shape, dtype=bool)
    mask[np.ix_(route, route)] = True

    # Use the mask to select the relevant distances
    reduced_dist_matrix = dist_matrix[mask].reshape(len(route), len(route))

    n = len(route)
    x = m.addVars(n, n, vtype=gp.GRB.BINARY, name='x')
    smaller = 10000

    obj = gp.quicksum(reduced_dist_matrix[i][j] * (problem_data.distance_cost/smaller) * x[i, j] for i in range(n) for j in range(n))
    m.setObjective(obj, gp.GRB.MINIMIZE)

    m.addConstrs(gp.quicksum(x[i, j] for j in range(n) if i != j) == 1 for i in range(n))
    m.addConstrs(gp.quicksum(x[i, j] for i in range(n) if i != j) == 1 for j in range(n))
    m.addConstr(gp.quicksum(x[i, j] * reduced_dist_matrix[i][j] for i in range(n) for j in range(n) if i != j) <= problem_data.max_trip_distance)
    m.optimize()

    if m.status == GRB.OPTIMAL:
        print(f"Optimal objective value: {m.objVal:.2f}")
        print("Optimal tour:")
        tour = [0]
        i = 0
        while len(tour) < n:
            for j in range(n):
                if x[i, j].x > 0.5 and j not in tour:
                    tour.append(j)
                    i = j
                    break
        print(tour)
        return True, tour
    else:
        return False, None

def distance_matrix1(problem_data: ProblemData):
    x = problem_data.coordinates[:, 1]
    y = problem_data.coordinates[:, 2]
    points = list(zip(x, y))
    n = len(points)
    dist_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            dist_matrix[i][j] = dist_matrix[j][i] = np.floor(np.sqrt(
                (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2))

    return dist_matrix

    '''
    print(type(matrix))
    print(distance_matrix(matrix, matrix))
    print(abs(matrix.T - matrix))
    '''

def sort_request(theta: list, lst: list):
    theta1 = theta[[i.location_id for i in lst]]
    sorted_indices = np.argsort(theta1)
    sorted_lst = [lst[i] for i in sorted_indices]

    return sorted_lst

def polar_order(problem_data: ProblemData):
    x_cent = problem_data.coordinates[:, 1] - problem_data.coordinates[problem_data.depot_coordinate, 1]
    y_cent = problem_data.coordinates[:, 2] - problem_data.coordinates[problem_data.depot_coordinate, 2]

    theta = np.where(x_cent == 0, 0, np.arctan2(y_cent, x_cent))
    theta = np.delete(theta, np.where(theta == 0)) #wrong
    r = np.sqrt(np.power(x_cent, 2)+np.power(y_cent, 2))
    r = np.delete(r, np.where(r == 0)) #wrong

    return theta, r

'''
def cluster(lst: list, problemData: ProblemData):
    coordinates = []
    for i in lst:
        coordinate = problemData.coordinates[i.id, :]
        coordinates.append(coordinate)

    coordinates1 = np.array(coordinates)[:, 1:]
    print(coordinates1)

    scores = []
    models = []
    for k in range(2, 10):
        model = KMeans(n_clusters=k, n_init=10, random_state=0)
        labels = model.fit_predict(coordinates1)
        score = silhouette_score(coordinates1, labels)
        models.append(model)
        scores.append(score)

    optimal_k = 2 + scores.index(max(scores))
    print(optimal_k)
    optimal_model = models[scores.index(max(scores))]
    print(optimal_model.labels_)

    fig, ax = plt.subplots()
    ax.scatter(coordinates1[:,0], coordinates1[:,1])
    for i, label in enumerate(optimal_model.labels_):
        ax.annotate(label, (coordinates1[i,0], coordinates1[i,1]))
    plt.show()

def distance_matrix1(matrix: numpy.ndarray):
    print(type(matrix))
    print(distance_matrix(matrix, matrix))
    print(abs(matrix.T - matrix))
'''