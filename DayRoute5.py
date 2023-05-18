from ortools.sat.python import cp_model
from problem import ProblemData, Tool
from config import INSTANCES_DIR
import os
from ReadInstance import read_instance

def schedule_tool_requests(problem_data: ProblemData, tool: Tool):
    tool_requests = []
    for request in problem_data.requests:
        if request.tool_kind_id == tool.id:
            tool_requests.append(request)
    #print(len(tool_requests))
    dict_re = {i: [] for i in range(problem_data.days)}
    dict_pi = {i: [] for i in range(problem_data.days)}

    total_capacity = tool.number_available

    model = cp_model.CpModel()

    num_requests = len(tool_requests)

    # Variables
    start_times = []
    end_times = []
    tool_usage = {i: total_capacity for i in range(problem_data.days)} #model.NewIntVar(0, total_capacity, 'tool_usage')

    for i in range(num_requests):
        start_time = model.NewIntVar(tool_requests[i].first_day, tool_requests[i].last_day, f'start_time_{i}')
        #end_time = model.NewIntVar(tool_requests[i].first_day + tool_requests[i].days_needed, tool_requests[i].last_day + tool_requests[i].days_needed, f'end_time_{i}')
        start_times.append(start_time)
        #end_times.append(end_time)

    # Constraints
    for i in range(num_requests):
        model.Add(start_times[i] >= tool_requests[i].first_day)
        model.Add(start_times[i] <= tool_requests[i].last_day)
        #model.Add(end_times[i] - start_times[i] == tool_requests[i].days_needed)
        for j in range(tool_requests[i].days_needed):
            model.Add(tool_usage[j] >= tool_requests[i].tools_needed)
            #model.Add(tool_usage[j] == tool_usage[j] - tool_requests[i].tools_needed)
        #model.Add(tool_usage >= tool_requests[i].tools_needed)

    #model.Add(tool_usage <= total_capacity)

    # Objective function
    objective = model.NewIntVar(0, sum(tool_request.days_needed for tool_request in tool_requests), 'objective')
    model.AddMaxEquality(objective, end_times)
    model.Minimize(objective)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print the optimal solution
        for i in range(num_requests):
            #print(f"Request {i+1}: Start Time: {solver.Value(start_times[i])}, End Time: {solver.Value(end_times[i])}, ({tool_requests[i].first_day},{tool_requests[i].last_day})")
            dict_re[solver.Value(start_times[i])] += [tool_requests[i]]
            dict_pi[solver.Value(start_times[i]) + tool_requests[i].days_needed] += [tool_requests[i]]
        return dict_re, dict_pi
        #print(dict)
        #print("Objective Value:", solver.ObjectiveValue())
    else:
        print("No feasible solution found.")

def day_by_day_scheduler(problem_data: ProblemData):
    dict_combined_re = {i: [] for i in range(problem_data.days)}
    dict_combined_pi = {i: [] for i in range(problem_data.days)}

    i = 0
    for tool in problem_data.tools:
        dict_re, dict_pi = schedule_tool_requests(problem_data, tool)
        dict_combined_re = {key: dict_combined_re[key] + dict_re[key] for key in dict_combined_re.keys() or dict_re.keys()}
        dict_combined_pi = {key: dict_combined_pi[key] + dict_pi[key] for key in dict_combined_pi.keys() or dict_pi.keys()}

    dict_combined_filtered_re = {k: v for k, v in dict_combined_re.items() if v}
    dict_combined_filtered_pi = {k: v for k, v in dict_combined_pi.items() if v}

    print(dict_combined_filtered_re)
    print(dict_combined_filtered_pi)


problem_data = read_instance(os.path.join(INSTANCES_DIR, 'challenge_r100d10_1.txt'))
#print(problem_data)
day_by_day_scheduler(problem_data)
'''

# Example usage
requests = [
    ToolRequest(release_date=0, due_date=10, service_time=4, num_tools_needed=1),
    ToolRequest(release_date=2, due_date=15, service_time=5, num_tools_needed=2),
    ToolRequest(release_date=5, due_date=20, service_time=3, num_tools_needed=1),
]

total_capacity = 3

schedule_tool_requests(requests, total_capacity)
'''

#schedule_tool_requests(requests, total_capacity)
