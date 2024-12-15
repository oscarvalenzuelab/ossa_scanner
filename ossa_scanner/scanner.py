import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils.os_detection import detect_os
from .utils.package_manager import list_packages, get_package_info
from .utils.downloader import download_source
from .utils.hash_calculator import calculate_file_hash
from .utils.swhid_calculator import calculate_swhid
from .uploader import GitHubUploader

class Scanner:
    def __init__(self, output_dir, threads=4):
        self.output_dir = output_dir
        self.os_type = detect_os()
        self.threads = threads

    def process_package(self, package):
        """
        Processes a single package: downloads source, extracts, calculates hash and SWHID.

        Args:
            package (str): Package name to process.

        Returns:
            dict: Result of the processed package including hash and SWHID.
        """
        try:
            print(f"Processing package: {package}")
            package_info = get_package_info(self.os_type, package)
            print(f"Fetched metadata for {package}")

            # Download the source code
            source_file = download_source(self.os_type, package, self.output_dir)
            print(f"Downloaded source file: {source_file}")

            # Calculate hash of the source file
            file_hash = calculate_file_hash(source_file)
            print(f"Hash (SHA256) for {package}: {file_hash}")

            # Extract source code directory
            source_dir = os.path.join(self.output_dir, package)
            os.makedirs(source_dir, exist_ok=True)

            # Calculate SWHID
            swhid = calculate_swhid(source_dir)
            print(f"SWHID for {package}: {swhid}")

            return {
                "package": package,
                "info": package_info,
                "hash": file_hash,
                "swhid": swhid,
            }

        except Exception as e:
            print(f"Error processing package {package}: {e}")
            return {
                "package": package,
                "error": str(e)
            }

    def scan_packages(self):
        """
        Scans all packages in the repository and processes them in parallel.

        Returns:
            list: List of results for each package.
        """
        print(f"Detected OS: {self.os_type}")
        print("Listing available packages...")
        packages = list_packages(self.os_type)
        results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit tasks for parallel processing
            future_to_package = {
                executor.submit(self.process_package, package): package
                for package in packages
            }

            for future in as_completed(future_to_package):
                package = future_to_package[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Exception occurred for package {package}: {e}")
        return results

    def save_results(self, results, output_file):
        """
        Save the scan results to a JSON file.

        Args:
            results (list): List of results for each package.
            output_file (str): Path to save the JSON file.
        """
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {output_file}")

    def upload_results(self, results_file, github_uploader, repo_dir):
        """
        Uploads the results file to GitHub.

        Args:
            results_file (str): Local results file path to upload.
            github_uploader (GitHubUploader): Instance of the GitHubUploader class.
            repo_dir (str): Path in the GitHub repository where the results will be uploaded.
        """
        print(f"Uploading results to GitHub: {repo_dir}")
        repo_path = os.path.join(repo_dir, os.path.basename(results_file))
        github_uploader.upload_file(results_file, repo_path, "Add scanning results")

