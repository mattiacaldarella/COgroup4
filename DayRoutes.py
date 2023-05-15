import numpy as np
from problem import ProblemData, Request

def day_divider2(problem_data: ProblemData):
    availability = {i.id : i.number_available for i in problem_data.tools}
    total_availability = {i: availability.copy() for i in range(1, problem_data.days+1)} #

    sort = sorted(problem_data.requests, key=lambda request: (request.last_day, request.last_day - request.first_day))
    dub = {i: [] for i in range(1, problem_data.days+1)}
    for i in sort:
        dub[i.first_day].append(i)

    dic_request = {i: [] for i in range(1,problem_data.days+1)}
    dic_pickup = {i: [] for i in range(1,problem_data.days+1)}

    for day_request in dub.keys():
        for request in dub[day_request]:
            enough_tools = tool_checker(request, total_availability, day_request)
            if enough_tools == True:

                dic_request[day_request] += [request]
                dic_pickup[day_request + request.days_needed] += [request]

                for days in range(request.days_needed + 1): #Fix!!
                    dic = total_availability[day_request + days]
                    dic[request.tool_kind_id] -= request.tools_needed
            else:
                request.first_day += 1 #mistake maybe here
                dub[day_request + 1] = [request] + dub[day_request + 1]

    dic_request_filtered = delete_empty_list_values(dic_request)
    dic_pickup_filtered = delete_empty_list_values(dic_pickup)

    return dic_request_filtered, dic_pickup_filtered

def delete_empty_list_values(dictionary):
    return {key: value for key, value in dictionary.items() if value != []}

def tool_checker(request: Request, total_availability: dict, day: int):
    dic = total_availability[day].copy()

    if dic[request.tool_kind_id] - request.tools_needed >= 0:
        return True
    else:
        #print('yes')
        return False

'''
def day_divider1(problem_data: ProblemData):
    dic_request = {}
    dic_pickup = {}
    for request in problem_data.requests:
        fd = request.first_day
        if fd in dic_request.keys():
            dic_request[fd].append(request)

            deadline = fd + request.days_needed
            if deadline in dic_pickup:
                dic_pickup[deadline].append(request)
            else:
                dic_pickup[deadline] = [request]
        else:
            dic_request[fd] = [request]

            deadline = fd + request.days_needed
            if deadline in dic_pickup:
                dic_pickup[deadline].append(request)
            else:
                dic_pickup[deadline] = [request]

    return dic_request, dic_pickup

def day_divider(problem_data: ProblemData):
    dic = {}
    for request in problem_data.requests:
        fd = request.first_day
        if fd in dic.keys():
            dic[fd].append(request)
        else:
            dic[fd] = [request]
    return dic
'''