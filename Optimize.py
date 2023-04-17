from collections import defaultdict

class Solution():
    def __init__(self):
        self.routes = defaultdict(list)  # day: list of routes

def optimize(problem_data):
    solution = Solution()

    for request in problem_data.requests:
        # Dumb solution where every request gets its own vehicle for delivery and pickup
        deliver_date = request.first_day
        return_date = request.first_day + request.days_needed
        solution.routes[deliver_date].append([0, request.id, 0])
        solution.routes[return_date].append([0, -request.id, 0])

    return solution
