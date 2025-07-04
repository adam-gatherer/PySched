import yaml
from database.database import insert_job


def add_job_from_file(filename: str):
    with open(filename, "r") as file:
        try:
            job_data = yaml.safe_load(file)
            insert_job(job_data)
            print(f"Job {job_data['job_name']} added to database.")
        except Exception as e:
            print("Failed to load job: {e}")
