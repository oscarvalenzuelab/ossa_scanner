import argparse
from .scanner import Scanner
from .uploader import GitHubUploader

def main():
    parser = argparse.ArgumentParser(description="OSSA Scanner CLI Tool")
    parser.add_argument('--output-dir', type=str, required=True, help="Directory to save downloaded source")
    parser.add_argument('--results-file', type=str, required=True, help="Path to save the JSON results")
    parser.add_argument('--threads', type=int, default=4, help="Number of threads for parallel processing")
    parser.add_argument('--upload', action='store_true', help="Upload results to GitHub")
    parser.add_argument('--repo-owner', type=str, help="GitHub repository owner")
    parser.add_argument('--repo-name', type=str, help="GitHub repository name")
    parser.add_argument('--token', type=str, help="GitHub token")
    parser.add_argument('--repo-dir', type=str, help="Target directory in GitHub repo for results")
    args = parser.parse_args()

    # Initialize the scanner
    scanner = Scanner(output_dir=args.output_dir, threads=args.threads)
    
    # Perform scanning
    results = scanner.scan_packages()

    # Save results locally
    scanner.save_results(results, args.results_file)

    # Upload results to GitHub if specified
    if args.upload:
        if not (args.repo_owner and args.repo_name and args.token and args.repo_dir):
            raise ValueError("GitHub upload requires --repo-owner, --repo-name, --token, and --repo-dir")

        uploader = GitHubUploader(args.token, args.repo_owner, args.repo_name)
        scanner.upload_results(args.results_file, uploader, args.repo_dir)

if __name__ == "__main__":
    main()
