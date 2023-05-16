import os
import time
from config import INSTANCES_DIR, SOLUTIONS_DIR, SCORES_FILE
import subprocess
import re
import csv


def validate(file_name):
    """Validates a solution using the Validator script, assuming it's stored under the proper file name"""

    print(f"Validating {file_name}...\n")
    # os.system(
    #     f"python3 Validator/Validate.py -i {os.path.join(INSTANCES_DIR, file_name)} -s {os.path.join(SOLUTIONS_DIR, file_name)}"
    # )
    result = subprocess.check_output(
        [
            "python3",
            "Validator/Validate.py",
            "-i",
            os.path.join(INSTANCES_DIR, file_name),
            "-s",
            os.path.join(SOLUTIONS_DIR, file_name),
        ]
    )
    result = result.decode()
    for line in result.split("\n"):
        print(line)
        if "Cost" in line:
            cost = re.findall(r'\d+', line)[0]
            print(cost)
            write_cost(file_name, cost)
    return "correct" in str(result)

def write_cost(file_name, cost):
    # fields=['timestamp','instance','cost']
    with open(SCORES_FILE, 'a') as f:
        writer = csv.writer(f, delimiter="\t")
        instance = file_name.split("_")[1]
        description = "dumb day divider"  # FIXME
        timestamp = int(time.time())
        writer.writerow([description, timestamp, instance, cost])

