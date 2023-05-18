import gurobipy as gp
from gurobipy import GRB
import numpy as np
from problem import ProblemData
from DayToDayPlanner import get_dates
from collections import defaultdict

class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }

def optimize(problem_data: ProblemData):
    solution = Solution()
    dict_request, dict_pickup = get_dates(problem_data)
    theta = polar_order(problem_data)
    dist_matrix = distance_matrix(problem_data)

    for j in sorted(list(set(dict_request) | set(dict_pickup))):
        tot_routes = []

        if j in dict_request.keys():
            tot_route_request = sweeping_method(theta, dict_request[j], problem_data, dist_matrix, True)
            tot_routes += tot_route_request
        if j in dict_pickup.keys():
            tot_route_pickup = sweeping_method(theta, dict_pickup[j], problem_data, dist_matrix, False)
            tot_routes += tot_route_pickup

        solution.routes[j] = tot_routes

    return solution

def sweeping_method(theta: list, lst: list, problem_data: ProblemData, dist_matrix: np.ndarray, sgn: bool):
    sort = sort_request(theta, lst)
    routes = []
    i = 0
    tool_sizes = {tool.id: tool.size for tool in problem_data.tools}

    while i < len(sort):
        i, request_list = fill_capacity(i, sort, tool_sizes, problem_data)
        succes, route = TSP(request_list, problem_data, dist_matrix, sgn)

        while succes == False:
            del request_list[-1]
            i -= 1
            succes, route = TSP(request_list, problem_data, dist_matrix, sgn)

        routes.append(route)

    return routes

def fill_capacity(i: int, sort: dict, tool_sizes: dict, problem_data: ProblemData):
    request_list = []
    capacity = problem_data.capacity

    while i < len(sort) and capacity >= tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed:
        item = sort[i]
        request_list.append(item)
        capacity -= tool_sizes[item.tool_kind_id] * item.tools_needed
        i += 1
    return i, request_list


def TSP(request_list: list, problem_data: ProblemData, dist_matrix: np.ndarray, sgn: bool):
    new = []
    for i in request_list:
        if i.location_id not in new:
            new.append(i.location_id)
    new.append(0)
    route_id_list = new

    mask = np.zeros(dist_matrix.shape, dtype=bool)
    mask[np.ix_(route_id_list, route_id_list)] = True
    reduced_dist_matrix = dist_matrix[mask].reshape(len(route_id_list), len(route_id_list))

    n = len(route_id_list)

    m = gp.Model('TSP')
    m.setParam('OutputFlag', 0)
    x = m.addVars(n, n, vtype=gp.GRB.BINARY, name='x')
    u = m.addVars(n, vtype=GRB.CONTINUOUS, lb=0.0, name='u')

    obj = gp.quicksum(reduced_dist_matrix[i][j] * (problem_data.distance_cost) * x[i, j] for i in range(n) for j in range(n))
    m.setObjective(obj, gp.GRB.MINIMIZE)

    #constraints
    m.addConstrs(gp.quicksum(x[i, j] for j in range(n) if i != j) == 1 for i in range(n))
    m.addConstrs(gp.quicksum(x[i, j] for i in range(n) if i != j) == 1 for j in range(n))
    m.addConstr(gp.quicksum(x[i, j] * reduced_dist_matrix[i][j] for i in range(n) for j in range(n) if i != j) <= problem_data.max_trip_distance)

    # sub tour elimination constraint
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)
    m.addConstr(u[0] == 1)

    m.optimize()

    # Print the route_order if an optimal solution is found
    if m.status == GRB.OPTIMAL:
        route_order = [0]
        i = 0
        while len(route_order) < n:
            for j in range(n):
                if x[i, j].x > 0.5 and j not in route_order:
                    route_order.append(j)
                    i = j
                    break
        route_order.remove(0)

        route = compiler(route_order, request_list, sgn)
        m.dispose()

        return True, route
    else:
        m.dispose()

        return False, None

def compiler(route_order: list, request_list: list, sgn: bool):
    request_list = sorted(request_list, key=lambda request: request.location_id)
    dub = {i.location_id: [] for i in request_list}
    for i in request_list:
        dub[i.location_id].append(i)

    new_dub = {i: dub[key] for i, key in enumerate(dub)}
    defaultlist = [new_dub[key - 1] for key in route_order]
    route = [0] + [element.id for sublist in defaultlist for element in sublist] + [0]
    route = [-i for i in route] if not sgn else route

    return route

def distance_matrix(problem_data: ProblemData):
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

def sort_request(theta: list, lst: list):
    theta1 = theta[[i.location_id - 1 for i in lst]]
    sorted_indices = np.argsort(theta1)
    sorted_lst = [lst[i] for i in sorted_indices]

    return sorted_lst

def polar_order(problem_data: ProblemData):
    x_cent = problem_data.coordinates[:, 1] - problem_data.coordinates[problem_data.depot_coordinate, 1]
    y_cent = problem_data.coordinates[:, 2] - problem_data.coordinates[problem_data.depot_coordinate, 2]
    theta = np.where(x_cent == 0, 0, np.arctan2(y_cent, x_cent))

    return theta