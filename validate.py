import os
from config import INSTANCES_DIR, SOLUTIONS_DIR
import subprocess
import re


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

    return "correct" in str(result)

