import yaml
from database.database import insert_job, list_jobs, get_job_by_name, get_job_by_id
import json as jason


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
        for key,val in job.items():
            print(f"  {key:<12}: {val}")
    print("\n")


def show_job_cli(indentifier, by_id=False):
    if by_id:
        job_row = get_job_by_id(indentifier)
    else:
        job_row = get_job_by_name(indentifier)
    
    if not job_row:
        print(f"Job not found: {indentifier}")
        return
    
    (
        job_id,
        job_name,
        command,
        job_type,
        start_time,
        run_days_json,
        conditions,
        enabled,
        description,
    ) = job_row

    

    print(job_id,
        job_name,
        command,
        job_type,
        start_time,
        run_days_json,
        conditions,
        enabled,
        description,)