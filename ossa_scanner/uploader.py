import http.client
import json
import base64
import os


class GitHubUploader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "api.github.com"

    def upload_file(self, file_path, repo_path, commit_message="Add scanner results"):
        """
        Uploads a file to a GitHub repository.
        
        Args:
            file_path (str): Local file path to upload.
            repo_path (str): Path in the GitHub repository.
            commit_message (str): Commit message for the upload.
        """
        # Read the file and encode it in base64
        with open(file_path, "rb") as f:
            content = f.read()
        encoded_content = base64.b64encode(content).decode("utf-8")

        # Create the payload
        payload = {
            "message": commit_message,
            "content": encoded_content,
        }

        # GitHub API endpoint
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/contents/{repo_path}"

        # Make the API request
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "ossa-scanner",
            "Content-Type": "application/json",
        }

        conn.request("PUT", endpoint, body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()

        if response.status == 201:
            print(f"File '{file_path}' successfully uploaded to {repo_path} in {self.repo_name}")
        else:
            print(f"Failed to upload file '{file_path}'. Response: {data}")
            raise Exception(f"GitHub API Error: {response.status}")

    def upload_results(self, results_dir, repo_dir):
        """
        Uploads all files in a directory to a specified path in the GitHub repo.
        
        Args:
            results_dir (str): Local directory containing results to upload.
            repo_dir (str): Target directory in the GitHub repository.
        """
        for root, _, files in os.walk(results_dir):
            for file_name in files:
                local_path = os.path.join(root, file_name)
                repo_path = os.path.join(repo_dir, file_name).replace("\\", "/")
                self.upload_file(local_path, repo_path)
