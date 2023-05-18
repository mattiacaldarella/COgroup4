from ortools.sat.python import cp_model
from problem import ProblemData, Tool
from config import INSTANCES_DIR
import os
from ReadInstance import read_instance

def schedule_classes_day_by_day(problem_data: ProblemData, tool: Tool):
    requests = []
    for request in problem_data.requests:
        if request.tool_kind_id == tool.id:
            requests.append(request)

    model = cp_model.CpModel()

    # Variables
    requests_vars = []
    day_starts = []

    for i in range(len(requests)):
        requests_var = []
        for d in range(problem_data.days):
            requests_var.append(model.NewBoolVar(f'class_{i}day{d}'))
        requests_vars.append(requests_var)

    tools_need = [request.tools_needed for request in requests]

    for r in range(len(requests)):
        day_start = model.NewIntVar(requests[r].first_day, requests[r].last_day, f'day_start_{r}')
        day_starts.append(day_start)

    for d in range(problem_data.days):
        model.Add(tool.number_available >= sum(tools_need[i]*requests_vars[i][d] for i in range(len(requests))))

    for r in range(len(requests)):
        my_variable = int()
        model.Add(my_variable >= requests[r].first_day)
        model.Add(my_variable <= requests[r].last_day)
        model.Add(my_variable == day_starts[r])
        model.Add(requests[r].days_needed == sum(requests_vars[r][i] for i in range(my_variable, my_variable + requests[r].days_needed)))
        model.Add(requests[r].days_needed == sum(requests_vars[r][i] for i in range(problem_data.days)))

    # Solve the model
    solver = cp_model.CpSolver()
    #solver.parameters.max_time_in_seconds = 60.0  # Set a time limit (optional)
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print the schedule
        for i in range(len(requests)):
            print(f"  Class {i+1}: Start Time: {solver.Value(day_starts[i])}")
    else:
        print("No feasible schedule found.")


problem_data = read_instance(os.path.join(INSTANCES_DIR, 'challenge_r100d10_1.txt'))
schedule_classes_day_by_day(problem_data, problem_data.tools[0])
