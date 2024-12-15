import subprocess
import os
import shutil
import glob

def download_source(package_manager, package_name, output_dir):
    try:
        if package_manager == 'apt':
            cmd = ['apt-get', 'source', package_name, '-d', output_dir]
            subprocess.run(cmd, check=True)
        elif package_manager in ['yum', 'dnf']:
            os.makedirs(output_dir, exist_ok=True)
            command = ["yumdownloader", "--source", "--destdir", output_dir, package_name]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                for file in os.listdir(output_dir):
                    if file.endswith(".src.rpm"):
                        srpm_path = os.path.join(output_dir, file)
            else:
                exit()
            try:
                command = f"rpm2cpio {srpm_path} | cpio -idmv -D {output_dir}"
                subprocess.run(command, shell=True, check=True)
                spec_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".spec")]
                if spec_files:
                    print("spec:", spec_files[0])
                    spec_file = spec_files[0]
            except subprocess.CalledProcessError as e:
                print(f"Failed to extract spec file from {srpm_path}: {e}")
            exit()
            
            
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
            return target_path
        else:
            raise ValueError("Unsupported package manager")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
