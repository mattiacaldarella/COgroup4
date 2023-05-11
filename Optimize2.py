import gurobipy as gp
from gurobipy import GRB
import numpy as np
from problem import ProblemData
from DayRoutes import day_divider1, day_divider

class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }

def optimize2(problem_data: ProblemData):
    #dic_request = day_divider(problem_data)
    tot_dic = {}

    dic_request, dic_pickup = day_divider1(problem_data)
    theta = polar_order(problem_data) #, r
    dist_matrix = distance_matrix1(problem_data)
    available_tools = {tool.id: tool.number_available for tool in problem_data.tools}
    print(available_tools)
    newlist = list(dic_request.keys()) + list(dic_request.keys())
    unique_lst = list(set(newlist))

    for j in sorted(unique_lst):
        available_count_re = {}
        available_count_pi = {}
        tot_routes = []

        if j in dic_request.keys():
            tot_route_request, available_count_re = sweep_method(theta, dic_request[j], problem_data, dist_matrix, 1)
            tot_routes += tot_route_request
        if j in dic_pickup.keys():
            tot_route_pickup, available_count_pi = sweep_method(theta, dic_pickup[j], problem_data, dist_matrix, -1)

            tot_routes += tot_route_pickup

        tot_dic[j] = tot_routes

        available_tools = {key: value + available_count_re.get(key, 0) + available_count_pi.get(key, 0) for key, value in available_tools.items()}
        print(j)
        print(available_count_re)
        print(available_count_pi)
        print(available_tools)

    return tot_dic

def sweep_method(theta: list, lst: list, problem_data: ProblemData, dist_matrix: np.ndarray, sgn: int):
    sort = sort_request(theta, lst)
    routes = []
    i = 0
    tool_sizes = {tool.id: tool.size for tool in problem_data.tools}

    while i < len(sort):
        i, route, available_tools = request_vs_pickup(i, sort, tool_sizes, problem_data, sgn)
        route.append(0)
        test, rout = gurobi(route, problem_data, dist_matrix)

        while test == False:
            route.remove(0)

            if sgn == 1:
                available_tools[sort[i].tool_kind_id] -= 1
            else:
                available_tools[sort[i].tool_kind_id] += 1

            del route[-1]
            route.append(0)
            test, rout = gurobi(route, problem_data, dist_matrix)

            i -= 1

        if sgn == -1:
            for j in range(len(rout)):
                rout[j] *= sgn

        routes.append(rout)

    return routes, available_tools

def request_vs_pickup(i: int, sort: dict, tool_sizes: dict, problem_data: ProblemData, sgn: int):
    next_request_cap = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed
    capacity = problem_data.capacity
    packed_cap = 0
    route = []
    available_tools = {tool.id: 0 for tool in problem_data.tools}

    if sgn == 1:
        while capacity >= next_request_cap and i < len(sort):
            route.append(sort[i].location_id)
            capacity -= next_request_cap
            available_tools[sort[i].tool_kind_id] -= 1

            i += 1
            if i >= len(sort):
                break
            next_request_cap = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed
    else:
        while capacity >= packed_cap and i < len(sort):
            route.append(sort[i].location_id)
            packed_cap += next_request_cap

            available_tools[sort[i].tool_kind_id] += 1

            i += 1
            if i >= len(sort):
                break
            next_request_cap = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed

    return i, route, available_tools

def gurobi(route: list, problem_data: ProblemData, dist_matrix: np.ndarray):
    route, dup_dic = give_duplicates(route)

    if len(dup_dic) != 0:
        print(dup_dic)

    m = gp.Model('TSP')

    # set the model parameters to prevent output to the console
    m.setParam('OutputFlag', 0)

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

    m.addConstrs(gp.quicksum(x[i, j] for j in range(n) if i != j) == 1 for i in range(n)) #every row is visit once
    m.addConstrs(gp.quicksum(x[i, j] for i in range(n) if i != j) == 1 for j in range(n)) #every column is visit once
    m.addConstr(gp.quicksum(x[i, j] * reduced_dist_matrix[i][j] for i in range(n) for j in range(n) if i != j) <= problem_data.max_trip_distance) #max trip distance

    # add the subtour elimination constraints
    u = m.addVars(n, vtype=GRB.CONTINUOUS, lb=0.0, name='u')
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)

    m.optimize()

    # Print the tour_order if an optimal solution is found
    if m.status == GRB.OPTIMAL:
        #print(f"Optimal objective value: {m.objVal:.2f}")
        tour_order = [0]
        i = 0
        while len(tour_order) < n:
            for j in range(n):
                if x[i, j].x > 0.5 and j not in tour_order:
                    tour_order.append(j)
                    i = j
                    break

        tour = [route[i] for i in tour_order]
        ind = tour.index(0)
        tour = tour[ind:] + tour[:ind]
        tour.append(0)

        return True, tour
    else:
        return False, None

def give_duplicates(lst: list):
    new = []
    dub = {}

    for i in lst:
        if i not in new:
            new.append(i)
        elif i in dub.keys():
            dub[i] += 1
        elif i not in dub:
            dub[i] = 1

    return new, dub

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

    theta = np.where(x_cent == 0, 0, np.arctan2(y_cent, x_cent))
    # before another
    #r = np.sqrt(np.power(x_cent, 2)+np.power(y_cent, 2))
    #r = np.delete(r, np.where(r == 0)) #wrong

    return theta #, r