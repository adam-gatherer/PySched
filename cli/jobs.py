import yaml
from database.database import insert_job, list_jobs


def add_job_from_file(filename: str):
    with open(filename, "r") as file:
        try:
            job_data = yaml.safe_load(file)
            insert_job(job_data)
            print(f"Job {job_data['job_name']} added to database.")
        except Exception as e:
            print("Failed to load job: {e}")


def list_jobs_cli():
    jobs = list_jobs()
    if not jobs:
        print("Err, no jobs found.")
        return

    headers = [
        "job_name",
        "command",
        "job_type",
        "start_time",
        "run_days",
        "enabled",
        "description",
    ]

    #
    # Come back to this later - not important
    #
    # print(
    #    f"|{headers[0]:<20} |{headers[1]:<30} |{headers[2]:<15} |{headers[3]:<12} |{headers[4]:<30} |{headers[5]:<10} |{headers[6]:<40}|"
    # )
    # print("-" * 171)

    # for job in jobs:
    #    print(
    #        f"|{job['job_name']:<20} |{job['command']:<30} |{job['job_type']:<15} |{job['start_time']:<12} |{job['run_days']:<30} |{str(job['enabled']):<10} |{job['description']:<40}"
    #    )
    #    print("-" * 171)
    print("JOBS IN SCHEDULER:\n")
    for job in jobs:
        print(f"-{job['job_name']}")
        for key,val in job.items():
            print(f"  {key:<12}: {val}")
    print("\n")
