import yaml, os
"""
# Template job file
job_name: T01_TEST_JOB
command: "echo 'howdy'"
job_type: command
start_time: "00:00"
run_days: ["Mon", "Wed", "Fri"]
conditions:
retry_count:
timout_seconds:
enabled: true
description: "Friendly test job."



"job_name":
"command":
"job_type":
"start_time":
"run_days":
"conditions":
"retry_count":
"timout_seconds":
"enabled":
"description":
"""


def read_job_file(filename: str) -> dict:
    # Check file exists etc.
    if not filename.endswith(".job"):
        print("Err, only .job files are supported.")
        return
    if not os.path.isfile(filename):
        print(f"Err, {filename} does not appear to exist.")
        return
    # Check file is valid
    try:
        with open(filename, "r") as file:
            job_data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Err, YAML error in {filename}: {e}")
    except Exception as e:
        print(f"Failed to load job: {e}")

    return job_data



job_data = read_job_file("template.job")

