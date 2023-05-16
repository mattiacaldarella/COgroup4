import numpy as np
from problem import ProblemData, Request


def day_divider(problem_data: ProblemData):
    availability = {i.id : i.number_available for i in problem_data.tools}
    total_availability = {i: availability.copy() for i in range(1, problem_data.days+1)} #
    #print(total_availability)

    total = 0
    for i in problem_data.tools:
        total += i.number_available

    tool_sizes = {tool.id: tool.number_available / total for tool in problem_data.tools}
    #print(tool_sizes)

    sort = sorted(problem_data.requests, key=lambda request: (request.last_day, -request.days_needed/tool_sizes[request.tool_kind_id])) #request.last_day - request.first_day
    dub = {i: [] for i in range(1, problem_data.days+1)}
    for i in sort:
        dub[i.first_day].append(i)

    dict_request = {i: [] for i in range(1,problem_data.days+1)}
    dict_pickup = {i: [] for i in range(1,problem_data.days+1)}

    for day_request in dub.keys():
        for request in dub[day_request]:
            enough_tools = tool_checker(request, total_availability, day_request)
            if enough_tools == True:

                dict_request[day_request] += [request]
                dict_pickup[day_request + request.days_needed] += [request] #mistake maybe here

                for days in range(request.days_needed + 1): #Fix!!
                    dic = total_availability[day_request + days]
                    dic[request.tool_kind_id] -= request.tools_needed
            else:
                request.first_day += 1 #Fix!!
                dub[day_request + 1] = [request] + dub[day_request + 1]

    dict_request_filtered = delete_empty_list_values(dict_request)
    dict_pickup_filtered = delete_empty_list_values(dict_pickup)
    #exit()
    return dict_request_filtered, dict_pickup_filtered

def delete_empty_list_values(dictionary):
    return {key: value for key, value in dictionary.items() if value != []}

def tool_checker(request: Request, total_availability: dict, day: int):
    dic = total_availability[day].copy()

    if dic[request.tool_kind_id] - request.tools_needed >= 0:
        return True
    else:
        return False
