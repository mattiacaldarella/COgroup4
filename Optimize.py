from collections import defaultdict
from problem import ProblemData


class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }


def get_dates(problem_data: ProblemData):
    # dict_request = {i: [] for i in range(1,problem_data.days+1)}
    # dict_pickup = {i: [] for i in range(1,problem_data.days+1)}
    dict_request = defaultdict(list)
    dict_pickup = defaultdict(list)

    available_tools = {
        (day, tool.id): tool.number_available
        for day in range(1, problem_data.days + 1)
        for tool in problem_data.tools
    }

    heuristic_weight = 40  # A value of 4 gives 19 valid sols, and this seems to be true for any higher value as well
    for request in sorted(
        problem_data.requests, key=lambda request: (-request.days_needed + heuristic_weight * request.last_day - request.first_day)
    ):
        # print(request)
        days_with_capacity = 0
        deliver_day = request.first_day
        check_day = request.first_day
        while days_with_capacity < request.days_needed + 1:
            if deliver_day > request.last_day:
                print(available_tools)
                raise RuntimeError(f"Request {request} could not be satisfied due to lack of available tools")
            if available_tools[(check_day, request.tool_kind_id)] < request.tools_needed:
                days_with_capacity = 0
                deliver_day = check_day + 1
            else:
                days_with_capacity += 1
            check_day += 1
        return_day = deliver_day + request.days_needed
        # Dumb solution where every request gets its own vehicle for delivery and pickup
        dict_request[deliver_day].append(request)
        dict_pickup[return_day].append(request)
        # solution.routes[deliver_day].append([0, request.id, 0])
        # solution.routes[return_day].append([0, -request.id, 0])
        for day in range(deliver_day, return_day+1):
            available_tools[(day, request.tool_kind_id)] -= request.tools_needed


    print(available_tools)
    return (dict_request, dict_pickup)
