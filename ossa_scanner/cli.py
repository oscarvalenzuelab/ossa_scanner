import argparse
import os
import shutil
from .scanner import Scanner
from .uploader import GitHubUploader

def main():
    parser = argparse.ArgumentParser(description="OSSA Scanner CLI Tool")
    parser.add_argument('--threads', type=int, default=4, help="Number of threads for parallel processing")
    parser.add_argument('--upload', action='store_true', help="Upload results to GitHub")
    parser.add_argument('--repo-owner', type=str, help="GitHub repository owner (required for upload)")
    parser.add_argument('--repo-name', type=str, help="GitHub repository name (required for upload)")
    parser.add_argument('--token', type=str, help="GitHub token (required for upload)")
    parser.add_argument('--repo-dir', type=str, help="Target directory in GitHub repo for results (required for upload)")
    parser.add_argument('--retain-temp', action='store_true', help="Retain the temporary directory for downloaded and extracted packages")
    args = parser.parse_args()

    # Define directories
    reports_dir = os.path.join(os.getcwd(), "ossa_reports")
    temp_dir = "/tmp/ossa_temp"

    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Initialize the scanner
        scanner = Scanner(threads=args.threads, output_dir=reports_dir, temp_dir=temp_dir)

        # Perform scanning
        results = scanner.scan_packages()

        # Handle GitHub upload if specified
        if args.upload:
            if not (args.repo_owner and args.repo_name and args.token and args.repo_dir):
                raise ValueError("GitHub upload requires --repo-owner, --repo-name, --token, and --repo-dir")

            uploader = GitHubUploader(args.token, args.repo_owner, args.repo_name)
            for report_file in os.listdir(reports_dir):
                report_path = os.path.join(reports_dir, report_file)
                if os.path.isfile(report_path):
                    uploader.upload_file(report_path, os.path.join(args.repo_dir, report_file), "Add OSSA report")

    finally:
        # Clean up the temporary directory unless the user opts to retain it
        if not args.retain_temp:
            print(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
