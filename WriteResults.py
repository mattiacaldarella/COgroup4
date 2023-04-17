import os
SOLUTIONS_DIR = "solutions"

def write_results(file_name, problem_data, solution):
    with open(os.path.join(SOLUTIONS_DIR, file_name), "w+") as f:
        f.write(f"DATASET = {problem_data.data_set}")
        f.write(f"NAME = {problem_data.name}")

        for day, routes in sorted(solution.routes.items()):
            f.write(f"DAY = {day}\n")
            vehicle_index = 1
            for route in routes:
                f.write(f"{vehicle_index} R {' '.join([str(x) for x in route])}\n")
                vehicle_index += 1