from collections import defaultdict
from problem import ProblemData


class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }


def get_dates(problem_data: ProblemData):
    dict_request = defaultdict(list)
    dict_pickup = defaultdict(list)

    available_tools = {
        (day, tool.id): tool.number_available
        for day in range(1, problem_data.days + 1)
        for tool in problem_data.tools
    }

    for request in sorted(
        problem_data.requests, key=lambda request: (request.last_day)
    ):
        days_with_capacity = 0
        deliver_day = request.first_day
        check_day = request.first_day

        while days_with_capacity < request.days_needed + 1:
            if deliver_day > request.last_day:
                raise RuntimeError(f"Request {request} could not be satisfied due to lack of available tools")

            if available_tools[(check_day, request.tool_kind_id)] < request.tools_needed:
                days_with_capacity = 0
                deliver_day = check_day + 1

            else:
                days_with_capacity += 1

            check_day += 1

        return_day = deliver_day + request.days_needed
        dict_request[deliver_day].append(request)
        dict_pickup[return_day].append(request)

        for day in range(deliver_day, return_day+1):
            available_tools[(day, request.tool_kind_id)] -= request.tools_needed

    return (dict_request, dict_pickup)
