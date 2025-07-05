from database.database import ensure_db_exists
from cli.jobs import add_job_from_file, list_jobs_cli
import yaml
import argparse


def main():
    ensure_db_exists()

    # CLI argument setup
    parser = argparse.ArgumentParser(description="PySched Job Scheduler")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Adding a job
    add_parser = subparsers.add_parser(
        "add-job", help="Add a job from a .job YAML file"
    )
    add_parser.add_argument("filename", help="Path to .job YAML file")
    # Show single job
    show_parser = subparsers.add_parser(
        "show-job", help="Show detailed info for a job"
    )
    show_parser.add_argument('idenfitier', help='Job name or job ID')
    show_parser.add_argument('-id', '--job-id', action='store_true', help='Lookup job by ID')
    # Listing all jobs
    list_parser = subparsers.add_parser(
        "list-jobs", help="List jobs in scheduler database"
    )

    # Catch arguments
    args = parser.parse_args()

    if args.command == "add-job":
        add_job_from_file(args.filename)
    elif args.command == "list-jobs":
        list_jobs_cli()
    else:
        parser.print_help()


def load_job_file(filepath: str):
    with open(filepath, "r") as file:
        try:
            job_data = yaml.safe_load(file)
            return job_data
        except yaml.YAMLError as e:
            print(f"Error parsing file {filepath}: {e}")
            return None


if __name__ == "__main__":
    main()
