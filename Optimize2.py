import gurobipy as gp
from gurobipy import GRB
import numpy as np
from problem import ProblemData

def optimize2(problem_data: ProblemData):
    dic = day_divider(problem_data)
    theta, r = polar_order(problem_data)
    dist_matrix = distance_matrix1(problem_data)

    for j in sorted(dic.keys()):
        print(sweep_method(theta, dic[j], problem_data, dist_matrix))
        lst = [1,1,1, 3,1,6 ,5, 7, 8, 8]
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

        while capacity >= next_request_cap and i < len(sort):
            print(i)
            route.append(sort[i].location_id)
            capacity -= next_request_cap
            next_request_cap = tool_sizes.get(sort[i].tool_kind_id) * sort[i].tools_needed
            i += 1

        route.append(0)
        #removes_multiples_but_remembers()
        test, rout = gurobi(route, problem_data, dist_matrix)
        #add_multiples_()

        while test == False:
            route.remove(0)
            del route[-1]
            route.append(0)
            # removes_multiples_but_remembers()
            test, rout = gurobi(route, problem_data, dist_matrix)
            # add_multiples_()
            i -= 1

        routes.append(rout)

    return routes

def gurobi(route: list, problem_data: ProblemData, dist_matrix: np.ndarray):
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
        #print("Optimal tour_order:")
        tour_order = [0]
        i = 0
        while len(tour_order) < n:
            for j in range(n):
                if x[i, j].x > 0.5 and j not in tour_order:
                    tour_order.append(j)
                    i = j
                    break
        tour = [route[i] for i in tour_order]

        return True, tour
    else:
        #print("No solution found.")
        return False, None

def give_duplicates(lst: list):
    #remember how much
    new = []
    dub = []

    for i in lst:
        if i not in new:
            new.append(i)
        elif i not in dub:
            dub.append(i)

    return dub

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
    theta = np.delete(theta, np.where(theta == 0)) #wrong
    r = np.sqrt(np.power(x_cent, 2)+np.power(y_cent, 2))
    r = np.delete(r, np.where(r == 0)) #wrong

    return theta, r