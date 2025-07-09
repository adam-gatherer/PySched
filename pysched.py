import argparse
import yaml
from database.database import ensure_db_exists
from cli.jobs import add_job_from_file, list_jobs_cli, show_job_cli, remove_job_cli
from validation.validation import validate_job_file


def main():
    """
    PySched application entry point.

    Initialises the job scheduler database (if not present), sets up the command-line
    interface using argparse, and handles the following commands:

    - add-job: Adds new job to the scheduler from a .job YAML file.
    - rm-job: Removes job from the database using job name or ID.
    - show-job: Displays detailed information for a specific job.
    - list-jobs: Lists all jobs currently in the scheduler database.

    Parses command-line arguments and dispatches to the appropriate CLI handler function.
    """
    ensure_db_exists()

    # CLI argument setup
    parser = argparse.ArgumentParser(description="PySched Job Scheduler")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Adding a job
    add_parser = subparsers.add_parser(
        "add-job", help="Add a job to the database scheduler from a .job YAML file"
    )
    # Removing a job
    rm_parser = subparsers.add_parser(
        "rm-job", help="Remove a job from the scheduler database"
    )
    rm_parser.add_argument("identifier", help="Job name or job ID")
    rm_parser.add_argument(
        "-id", "--job-id", action="store_true", help="Remove job by ID"
    )
    rm_parser.add_argument(
        "-f", "--force", action="store_true", help="Force delete without confirmation"
    )

    add_parser.add_argument("filename", help="Path to .job YAML file")
    # Show single job
    show_parser = subparsers.add_parser("show-job", help="Show detailed info for a job")
    show_parser.add_argument("identifier", help="Job name or job ID")
    show_parser.add_argument(
        "-id", "--job-id", action="store_true", help="Lookup job by ID"
    )
    # Listing all jobs
    list_parser = subparsers.add_parser(
        "list-jobs", help="List jobs in scheduler database"
    )

    # Catch arguments
    args = parser.parse_args()

    # Job handler
    if args.command == "add-job":
        add_job_from_file(args.filename)

    elif args.command == "list-jobs":
        list_jobs_cli()
    elif args.command == "show-job":
        if args.job_id:
            try:
                identifier = int(args.identifier)
                show_job_cli(args.identifier, by_id=args.job_id)
            except ValueError:
                print("Err, job ID must be an integer.")
    elif args.command == "rm-job":
        if args.job_id:
            try:
                identifier = int(args.identifier)
                remove_job_cli(args.identifier, by_id=args.job_id, force=args.force)
            except ValueError:
                print("Err, job ID must be an integer.")
    else:
        parser.print_help()


def load_job_file(filepath: str):
    """
    Loads and parses job definition from YAML file.

    Args:
        filepath (str): Path to the .job YAML file.

    Returns:
        dict or None: Parsed job data as dictionary if successful, otherwise None on error.

    Prints error message if YAML is invalid or cannot be loaded.
    """
    with open(filepath, "r") as file:
        try:
            job_data = yaml.safe_load(file)
            return job_data
        except yaml.YAMLError as e:
            print(f"Error parsing file {filepath}: {e}")
            return None


if __name__ == "__main__":
    main()
