from collections import defaultdict
from problem import ProblemData


class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }


def optimize(problem_data: ProblemData):
    solution = Solution()

    available_tools = {
        (day, tool.id): tool.number_available
        for day in range(1, problem_data.days + 1)
        for tool in problem_data.tools
    }

    heuristic_weight = 4  # A value of 4 gives 19 valid sols, and this seems to be true for any higher value as well
    for request in sorted(
        problem_data.requests, key=lambda request: (-request.days_needed + heuristic_weight * request.last_day)
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
        solution.routes[deliver_day].append([0, request.id, 0])
        solution.routes[return_day].append([0, -request.id, 0])
        for day in range(deliver_day, return_day+1):
            available_tools[(day, request.tool_kind_id)] -= request.tools_needed

    # When returning a tool, send it directly to a customer who needs it instead
    # for day in range(1, problem_data.days+1):
    #     for route_a in solution.routes[day]:
    #         for route_b in solution.routes[day]:
    #             if route_a[1] < 0 and route_b[1] == -route_a[1]:  # and distance
    #                 solution.routes[day].remove(route_a)
    #                 solution.routes[day].remove(route_b)
    #                 solution.routes[day].append([0, route_a[1], route_b[1], 0])
    print(available_tools)
    return solution
