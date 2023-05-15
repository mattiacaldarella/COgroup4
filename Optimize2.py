import gurobipy as gp
from gurobipy import GRB
import numpy as np
from problem import ProblemData
from DayRoutes import day_divider2
from collections import defaultdict

class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }

def optimize2(problem_data: ProblemData):
    solution = Solution()

    dic_request, dic_pickup = day_divider2(problem_data)
    theta = polar_order(problem_data)
    dist_matrix = distance_matrix1(problem_data)

    for j in sorted(list(set(dic_request) | set(dic_pickup))):
        tot_routes = []

        if j in dic_request.keys():
            tot_route_request = sweep_method(theta, dic_request[j], problem_data, dist_matrix, True)
            tot_routes += tot_route_request
        if j in dic_pickup.keys():
            tot_route_pickup = sweep_method(theta, dic_pickup[j], problem_data, dist_matrix, False)
            tot_routes += tot_route_pickup

        solution.routes[j] = tot_routes

    return solution

def sweep_method(theta: list, lst: list, problem_data: ProblemData, dist_matrix: np.ndarray, sgn: bool):
    sort = sort_request(theta, lst)
    routes = []
    i = 0
    tool_sizes = {tool.id: tool.size for tool in problem_data.tools}

    while i < len(sort):
        i, route = request_vs_pickup(i, sort, tool_sizes, problem_data, sgn)
        test, routx = gurobi(route, problem_data, dist_matrix)

        while test == False:
            del route[-1]
            i -= 1
            test, routx = gurobi(route, problem_data, dist_matrix)

        route_ids = [0] + [r.id for r in routx] + [0]
        if not sgn:
            route_ids = [-i for i in route_ids]
        routes.append(route_ids)

    return routes

def request_vs_pickup(i: int, sort: dict, tool_sizes: dict, problem_data: ProblemData, sgn: bool):
    fill = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed
    route = []

    while problem_data.capacity >= fill and i < len(sort):
        item = sort[i]
        route.append(item)
        fill += tool_sizes[item.tool_kind_id] * item.tools_needed

        i += 1
        if i >= len(sort):
            break

        fill += tool_sizes[sort[i].tool_kind_id] * sort[i].tools_needed

    return i, route

def gurobi(route: list, problem_data: ProblemData, dist_matrix: np.ndarray):
    new = []
    for i in route:
        if i.location_id not in new:
            new.append(i.location_id)
    new.append(0)
    route_id_list = new

    m = gp.Model('TSP')

    # set the model parameters to prevent output to the console
    m.setParam('OutputFlag', 0)

    # Create a boolean mask to select the relevant rows and columns
    mask = np.zeros(dist_matrix.shape, dtype=bool)
    mask[np.ix_(route_id_list, route_id_list)] = True

    # Use the mask to select the relevant distances
    reduced_dist_matrix = dist_matrix[mask].reshape(len(route_id_list), len(route_id_list))

    n = len(route_id_list)
    x = m.addVars(n, n, vtype=gp.GRB.BINARY, name='x')
    smaller = 10000

    obj = gp.quicksum(reduced_dist_matrix[i][j] * (problem_data.distance_cost/smaller) * x[i, j] for i in range(n) for j in range(n))
    m.setObjective(obj, gp.GRB.MINIMIZE)

    m.addConstrs(gp.quicksum(x[i, j] for j in range(n) if i != j) == 1 for i in range(n)) #every row is visit once
    m.addConstrs(gp.quicksum(x[i, j] for i in range(n) if i != j) == 1 for j in range(n)) #every column is visit once
    m.addConstr(gp.quicksum(x[i, j] * reduced_dist_matrix[i][j] for i in range(n) for j in range(n) if i != j) <= problem_data.max_trip_distance)  # max trip distance

    # add the subtour elimination constraints
    u = m.addVars(n, vtype=GRB.CONTINUOUS, lb=0.0, name='u')
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)

    m.optimize()

    # Print the tour_order if an optimal solution is found
    if m.status == GRB.OPTIMAL:
        tour_order = [0]
        i = 0
        while len(tour_order) < n:
            for j in range(n):
                if x[i, j].x > 0.5 and j not in tour_order:
                    tour_order.append(j)
                    i = j
                    break
        tour_order.remove(0)

        finish = compiler(tour_order, route)

        return True, finish
    else:
        return False, None

def compiler(tour_order: list, route: list):
    dub = {i.location_id: [] for i in route}
    for i in route:
        dub[i.location_id].append(i)

    new_dub = {i: dub[key] for i, key in enumerate(dub)}
    defaultlist = [new_dub.get(i - 1, 0) for i in tour_order]

    flat_list = [x for sublist in defaultlist for x in sublist]
    finish = []

    for x in flat_list:
        finish.append(x)

    return finish

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

def sort_request(theta: list, lst: list):
    theta1 = theta[[i.location_id for i in lst]]
    sorted_indices = np.argsort(theta1)
    sorted_lst = [lst[i] for i in sorted_indices]

    return sorted_lst

def polar_order(problem_data: ProblemData):
    x_cent = problem_data.coordinates[:, 1] - problem_data.coordinates[problem_data.depot_coordinate, 1]
    y_cent = problem_data.coordinates[:, 2] - problem_data.coordinates[problem_data.depot_coordinate, 2]

    theta = np.where(x_cent == 0, 0, np.arctan2(y_cent, x_cent)) #x=0 does not mean y=0
    # before another
    #r = np.sqrt(np.power(x_cent, 2)+np.power(y_cent, 2))
    #r = np.delete(r, np.where(r == 0)) #wrong

    return theta #, r