from collections import defaultdict
from problem import ProblemData, Tool


class Solution:
    def __init__(self):
        self.routes = defaultdict(list)  # { day: list of routes }


def get_dates(problem_data: ProblemData, tool: Tool):
    tool_requests = []
    for request in problem_data.requests:
        if request.tool_kind_id == tool.id:
            tool_requests.append(request)

    dict_request = defaultdict(list)
    dict_pickup = defaultdict(list)

    available_tools = {
        (day, tool.id): tool.number_available
        for day in range(1, problem_data.days + 1)
        for tool in problem_data.tools
    }

    heuristic_weight = 1  # A value of 4 gives 19 valid sols, and this seems to be true for any higher value as well
    for request in sorted(
        tool_requests, key=lambda tool_request: (tool_request.tools_needed, tool_request.last_day) #, -tool_request.tools_needed 0 * -request.days_needed + heuristic_weight * request.last_day
    ):
        # print(request)
        days_with_capacity = 0
        deliver_day = request.first_day
        check_day = request.first_day
        while days_with_capacity < request.days_needed + 1:
            if deliver_day > request.last_day:
                print(yes)
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

def avail(problem_data: ProblemData):
    dict_combined_re = {i: [] for i in range(problem_data.days)}
    dict_combined_pi = {i: [] for i in range(problem_data.days)}

    i = 0
    for tool in problem_data.tools:
        dict_re, dict_pi = get_dates(problem_data, tool)
        dict_combined_re = {key: dict_combined_re[key] + dict_re[key] for key in dict_combined_re.keys() or dict_re.keys()}
        dict_combined_pi = {key: dict_combined_pi[key] + dict_pi[key] for key in dict_combined_pi.keys() or dict_pi.keys()}

    dict_combined_filtered_re = {k: v for k, v in dict_combined_re.items() if v}
    dict_combined_filtered_pi = {k: v for k, v in dict_combined_pi.items() if v}

    return dict_combined_filtered_re, dict_combined_filtered_pi