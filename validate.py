import os
from config import INSTANCES_DIR, SOLUTIONS_DIR
import subprocess


def validate(file_name):
    """Validates a solution using the Validator script, assuming it's stored under the proper file name"""

    print(f"Validating {file_name}...")
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
    print(result)
    return "correct" in str(result)
