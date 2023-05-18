from ortools.sat.python import cp_model

class Request:
    def __init__(self, release_day, due_date, service_time, required_people):
        self.release_day = release_day
        self.due_date = due_date
        self.service_time = service_time
        self.required_people = required_people

def solve_scheduling(requests):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    num_requests = len(requests)
    num_people = 10  # Total number of available people

    # Decision variables
    scheduled = []
    start_time = []

    for i in range(num_requests):
        scheduled.append(model.NewBoolVar(f'request_{i}_scheduled'))
        start_time.append(model.NewIntVar(requests[i].release_day, requests[i].due_date, f'request_{i}_start_time'))

    # Constraints
    for i in range(num_requests):
        model.Add(start_time[i] + requests[i].service_time <= requests[i].due_date)
        for j in range(i + 1, num_requests):
            model.Add(start_time[i] + requests[i].service_time <= start_time[j] + (1 - scheduled[j]) * requests[j].due_date)
            model.Add(start_time[j] + requests[j].service_time <= start_time[i] + (1 - scheduled[i]) * requests[i].due_date)
        model.Add(scheduled[i] * requests[i].required_people <= num_people)
        model.Add(scheduled[i] == 1)

    # Objective function
    total_completion_time = model.NewIntVar(0, sum(requests[i].service_time for i in range(num_requests)), 'total_completion_time')
    model.AddMaxEquality(total_completion_time, [start_time[i] + requests[i].service_time for i in range(num_requests)])
    model.Minimize(total_completion_time)

    # Solve the model
    solver.Solve(model)
    status = solver.Solve(model)

    # Retrieve the solution
    schedule = []
    if status == cp_model.OPTIMAL:
        for i in range(num_requests):
            if solver.Value(scheduled[i]):
                schedule.append({'request_id': i, 'start_time': solver.Value(start_time[i])})
        print(1)
        return schedule
    else:
        print('fail')

# Usage example
requests = [
    Request(1, 3, 1, 2),
    Request(2, 5, 2, 3),
    Request(3, 6, 1, 1),
    # Add more requests as needed
]

schedule = solve_scheduling(requests)
print(schedule)

'''
for task in schedule:
    print(f'Request {task["request_id"]} starts at time {task["start_time"]}')
'''


