import yaml, os, re
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

def is_required(key, val):
    if val is None:
        return {"valid": False, "message": f"Property {key} missing"}
    else:
        return {"valid": True, "message": ""}


def is_alphanumeric(key, val):
    if re.match(r'A-Za-z0-9', val):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} must be alphanumeric"}


def max_length(length):
    def validator (key, val):
        if len(val) > length:
            return {"valid": False, "message": f"Property {key} is too long ({length} characters)"}
        else:
            return {"valid": True, "message": ""}
    return validator


def is_integer(key, val):
    try:
        int(val)
        return {"valid": True, "message": ""}
    except:
        return {"valid": False, "message": f"Property {key} is not an integer"}

 
def is_valid_time(key, val):
    pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d$'
    if re.match(pattern, val):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} is not a valid HH:MM time"}


def is_boolean(key, val):
    if val.lower() in ("true", "false"):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} is not 'true' or 'false'"}


def validate_job_file(job_data: dict):
    job_template = {
        "job_name": [is_required, is_alphanumeric, max_length(64)],
        "command": [is_required],
        "job_type": [is_required],
        "start_time": [is_required, is_valid_time],
        "run_days": [is_required],
        "conditions": [],
        "retry_count": [is_integer],
        "timout_seconds": [is_integer],
        "enabled": [is_required, is_boolean],
        "description": [is_required, is_alphanumeric, max_length(256)]
    }

    for key, val in job_template.items():
        if key == "job_name":
            for function in val:
                print(function(key, str(val)))


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

validate_job_file(job_data)
