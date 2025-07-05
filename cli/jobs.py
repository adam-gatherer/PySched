import yaml
from database.database import (
    insert_job,
    list_jobs,
    get_job_by_name,
    get_job_by_id,
    rm_job_by_id,
    rm_job_by_name,
)


def add_job_from_file(filename: str):
    with open(filename, "r") as file:
        try:
            job_data = yaml.safe_load(file)
            insert_job(job_data)
            print(f"Job {job_data['job_name']} added to database.")
        except Exception as e:
            print(f"Failed to load job: {e}")


def list_jobs_cli():
    jobs = list_jobs()
    if not jobs:
        print("Err, no jobs found.")
        return

    print("JOBS IN SCHEDULER:")
    for job in jobs:
        print(f"\n-{job['job_name']}")
        for key, val in job.items():
            print(f"  {key:<17}: {val}")
    print("\n")


def show_job_cli(identifier: str, by_id=False):
    if by_id:
        job_row = get_job_by_id(identifier)
    else:
        job_row = get_job_by_name(identifier)

    if not job_row:
        print(f"Job not found: {identifier}")
        return
    (
        job_id,
        job_name,
        command,
        job_type,
        start_time,
        run_days_json,
        conditions,
        retry_count,
        timeout_seconds,
        enabled,
        description,
    ) = job_row

    print(f"\n-{job_name}")
    print(f"  {'id':<17}: {job_id}")
    print(f"  {'command':<17}: {command}")
    print(f"  {'job_type':<17}: {job_type}")
    print(f"  {'start_time':<17}: {start_time}")
    print(f"  {'run_days':<17}: {run_days_json}")
    print(f"  {'conditions':<17}: {conditions}")
    print(f"  {'retry_count':<17}: {retry_count}")
    print(f"  {'timeout_seconds':<17}: {timeout_seconds}")
    print(f"  {'enabled':<17}: {enabled}")
    print(f"  {'description':<17}: {description}")
    print("\n")


def remove_job_cli(identifier: str, by_id=False, force=False):
    if not force:
        confirmed = confirm_removal(identifier, by_id)
        if not confirmed:
            print("Job removal canceled.")
            return

    if by_id:
        removed = rm_job_by_id(identifier)
    else:
        removed = rm_job_by_name(identifier)

    if removed:
        print(f"Job {identifier} removed")
    else:
        print(f"No job found with identifier: '{identifier}'")


def confirm_removal(identifier, by_id):
    target = f"ID {identifier}" if by_id else f"{identifier}"
    response = input(f"Confirm removal of job {target}? [y/n] ").strip().lower()
    return response == "y"
