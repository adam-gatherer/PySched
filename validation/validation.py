import yaml, os, re


def is_required(key, val):
    if val is None:
        return {"valid": False, "message": f"Property {key} missing"}
    else:
        return {"valid": True, "message": ""}


def is_valid_job_name(key, val):
    if re.match(r"[A-Za-z0-9_-]+", val):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} must be alphanumeric"}


def max_length(length):
    def max_length_validator(key, val):
        if len(val) > length:
            return {
                "valid": False,
                "message": f"Property {key} is too long ({length} characters)",
            }
        else:
            return {"valid": True, "message": ""}

    return max_length_validator


def min_length(length):
    def min_length_validator(key, val):
        if len(val) < length:
            return {
                "valid": False,
                "message": f"Property {key} is too short ({length} characters)",
            }
        else:
            return {"valid": True, "message": ""}

    return min_length_validator



def is_integer(key, val):
    try:
        int(val)
        return {"valid": True, "message": ""}
    except:
        return {"valid": False, "message": f"Property {key} is not an integer"}


def is_nullish_integer(key, val):
    if val is None:
        return {"valid": True, "message": ""}
    else:
        try:
            int(val)
            return {"valid": True, "message": ""}
        except:
            return {"valid": False, "message": f"Property {key} is not an integer"}


def is_valid_time(key, val):
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    if re.match(pattern, val):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} is not a valid HH:MM time"}


def is_boolean(key, val):
    if str(val).lower() in ("true", "false"):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} is not 'true' or 'false'"}


def is_job_type(key, val):
    if val in ("command", "box"):
        return {"valid": True, "message": ""}
    else:
        return {
            "valid": False,
            "message": f"Property {key} not valid job type (command, box)",
        }


def is_valid_description(key, val):
    if re.match(r"A-Za-z0-9", val):
        return {"valid": True, "message": ""}
    else:
        return {"valid": False, "message": f"Property {key} must be alphanumeric"}


def validate_job_file(job_data: dict):
    job_template = {
        "job_name": [is_required, is_valid_job_name, max_length(64), min_length(3)],
        "command": [is_required],
        "job_type": [is_required, is_job_type],
        "start_time": [is_required, is_valid_time],
        "run_days": [is_required],
        "conditions": [],
        "retry_count": [is_nullish_integer],
        "timeout_seconds": [is_nullish_integer],
        "enabled": [is_required, is_boolean],
        "description": [is_required, is_valid_description, max_length(256)],
    }

    for key, validators in job_template.items():

        job_data_value = job_data[key]

        # if key == "retry_count":
        print(f"{key}: {job_data_value}")
        for function in validators:
            validation_check = function.__name__
            print(f"  - {validation_check}")
            validation_output = function(key, job_data_value)
            if validation_output["valid"]:
                print("    - okay!")
            else:
                print(f"    - ERROR: {validation_output['message']}")
        print("\n")


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
