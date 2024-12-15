import subprocess
import os
import shutil
import glob

def cleanup_extracted_files(folder_path):
    """Recursively clean up files and directories in the specified folder."""
    try:
        for file_path in glob.glob(f"{folder_path}/*"):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Recursively delete directories
                print(f"Deleted directory: {file_path}")
            else:
                os.remove(file_path)  # Delete files
                print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Failed to clean up {folder_path}: {e}")

def download_source(package_manager, package_name, output_dir):
    try:
        if package_manager == 'apt':
            cmd = ['apt-get', 'source', package_name, '-d', output_dir]
            subprocess.run(cmd, check=True)
        elif package_manager in ['yum', 'dnf']:
            p_hash = hash(package_name) % 10000
            output_dir = os.path.join(output_dir, str(p_hash))
            os.makedirs(output_dir, exist_ok=True)
            source_path = get_rpm_source_package(package_name, output_dir)
            if not source_path:
                print(f"Source package for {package_name} not found in {package_name}.")
                return
            spec_file = extract_rpm_spec_file(source_path, output_dir)
            project_url, source_url = (None, None)
            if spec_file:
                project_url, source_url, license = extract_rpm_info_from_spec(spec_file)
                print("extract_rpm_urls_from_spec:",project_url,source_url, license)
                cleanup_extracted_files(spec_file)
            tarballs = extract_rpm_tarballs(source_path)
            return tarballs
        elif package_manager == 'brew':
            # Fetch the source tarball
            cmd = ['brew', 'fetch', '--build-from-source', package_name]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            cache_dir = subprocess.run(
                ['brew', '--cache', package_name],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            prefixes_to_remove = ['aarch64-elf-', 'arm-none-eabi-', 'other-prefix-']
            stripped_package_name = package_name
            for prefix in prefixes_to_remove:
                if package_name.startswith(prefix):
                    stripped_package_name = package_name[len(prefix):]
                    break
            cache_folder = os.path.dirname(cache_dir)
            tarball_pattern = os.path.join(cache_folder, f"*{stripped_package_name}*")
            matching_files = glob.glob(tarball_pattern)
            if not matching_files:
                raise FileNotFoundError(f"Tarball not found for {package_name} in {cache_folder}")
            tarball_path = matching_files[0]
            os.makedirs(output_dir, exist_ok=True)
            target_path = os.path.join(output_dir, os.path.basename(tarball_path))
            shutil.move(tarball_path, target_path)
            return [target_path]
        else:
            raise ValueError("Unsupported package manager")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_rpm_source_package(package_name, dest_dir="./source_packages"):
    os.makedirs(dest_dir, exist_ok=True)
    command = ["yumdownloader", "--source", "--destdir", dest_dir, package_name]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        for file in os.listdir(dest_dir):
            if file.endswith(".src.rpm"):
                return os.path.join(dest_dir, file)
    return None

def extract_rpm_spec_file(srpm_path, dest_dir="./extracted_specs"):
    os.makedirs(dest_dir, exist_ok=True)
    try:
        command = f"rpm2cpio {srpm_path} | cpio -idmv -D {dest_dir}"
        subprocess.run(command, shell=True, check=True)
        spec_files = [os.path.join(dest_dir, f) for f in os.listdir(dest_dir) if f.endswith(".spec")]
        if spec_files:
            return spec_files[0]
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract spec file from {srpm_path}: {e}")
    return None

def extract_rpm_tarballs(srpm_path, dest_dir="./extracted_sources"):
    os.makedirs(dest_dir, exist_ok=True)
    try:
        command = f"rpm2cpio {srpm_path} | cpio -idmv -D {dest_dir}"
        subprocess.run(command, shell=True, check=True)
        tarballs = [os.path.join(dest_dir, f) for f in os.listdir(dest_dir) if f.endswith((".tar.gz", ".tar.bz2", ".tar.xz", ".tgz"))]
        return tarballs
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract tarballs from {srpm_path}: {e}")
    return []

def extract_rpm_info_from_spec(spec_file_path):
    project_url = None
    source_url = None
    license = None
    try:
        with open(spec_file_path, "r") as spec_file:
            for line in spec_file:
                if line.startswith("URL:"):
                    project_url = line.split(":", 1)[1].strip()
                elif line.startswith("Source0:"):
                    source_url = line.split(":", 1)[1].strip()
                elif line.startswith("License:"):
                    license = line.split(":", 1)[1].strip()
    except FileNotFoundError:
        print(f"Spec file not found: {spec_file_path}")
    return project_url, source_url, license