import numpy as np
from problem import ProblemData

def day_divider2(problem_data: ProblemData):
    for request in sorted(problem_data.requests, key=lambda request: (-request.days_needed + heuristic_weight * request.last_day - request.first_day)):


    return dic_request, dic_pickup

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