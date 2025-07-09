import os
import yaml
from validation.validation import read_job_file, validate_job_file
from database.database import (
    insert_job,
    list_jobs,
    get_job_by_name,
    get_job_by_id,
    rm_job_by_id,
    rm_job_by_name,
)


def add_job_from_file(filename: str):

    job_data = read_job_file(filename)
    if validate_job_file(job_data):
        # Attempt to add job
        try:
            insert_job(job_data)
            print(f"Job {job_data['job_name']} added to database.")
        except Exception as e:
            print(f"Err, failed to insert {filename}: {e}")


def list_jobs_cli():
    """
    Lists all jobs currently stored in scheduler database.

    Retrieves all job entries using `list_jobs()` function and prints them to the
    console in human-readable format. If no jobs found, prints message to indicate this.

    Output includes each job's name and associated metadata (e.g., start time,
    command, retries, etc.).

    This function is intended to be called via the command-line interface.
    """
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
    """
    Display detailed information about a single job from the database.

    Args:
        identifier (str): Job name or job ID to look up.
        by_id (bool, optional): If True, treat the identifier as job ID.
                                If False (default), treat it as job name.

    Behavior:
        - Fetches job row from the database.
        - Prints all job attributes in formatted, human-readable layout.
        - If no job found, prints error message and exits cleanly.
    """
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
    """
    Removes job from the scheduler database via the CLI.

    Parameters:
        identifier (str): Job name or ID to remove.
        by_id (bool, optional): If True, treats 'identifier' as job ID (integer).
                                If False (default), treats it as job name.
        force (bool, optional): If True, skips confirmation prompt before deletion.

    Behavior:
        - Prompts for confirmation unless 'force' set to True.
        - Attempts to remove job by name or ID based on 'by_id'.
        - Prints success or failure message based on whether the job was found and removed.
    """
    if not force:
        confirmed = confirm_removal(identifier, by_id)
        if not confirmed:
            print("Job removal canceled.")
            return

    if by_id:
        removed = rm_job_by_id(identifier)
        if removed:
            print(f"Job ID {identifier} removed")
        else:
            print(f"No job found with ID: '{identifier}'")
    else:
        removed = rm_job_by_name(identifier)
        if removed:
            print(f"Job {identifier} removed")
        else:
            print(f"No job found with name: '{identifier}'")


def confirm_removal(identifier, by_id):
    """
    Prompts user to confirm removal of job by name or ID.

    Args:
        identifier (str): Job name or numeric ID to be removed.
        by_id (bool): True if identifier is job ID, False if job name.

    Returns:
        bool: True if user confirms with 'y', False otherwise.
    """
    target = f"ID {identifier}" if by_id else f"{identifier}"
    response = input(f"Confirm removal of job {target}? [y/n] ").strip().lower()
    return response == "y"
