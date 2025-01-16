import subprocess

def calculate_swhid(directory_path):
    """Calculate the SWHID for a folder using `sw identify .`."""
    try:
        command = ["swh.identify", directory_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                # Split the output to extract the SWHID
                if line.startswith("swh:1:dir:"):
                    swhid = line.split("\t")[0]  # Extract the SWHID part
                    return swhid
        else:
            print(f"Failed to compute folder SWHID: {result.stderr}")
    except FileNotFoundError:
        print(f"The `swh` command is not installed or not found in PATH.")
    return None