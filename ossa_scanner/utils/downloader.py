import subprocess

def download_source(package_manager, package_name, output_dir):
    if package_manager == 'apt':
        cmd = ['apt-get', 'source', package_name, '-d', output_dir]
    elif package_manager in ['yum', 'dnf']:
        cmd = ['dnf', 'download', '--source', package_name, '--downloaddir', output_dir]
    else:
        raise ValueError("Unsupported package manager")

    subprocess.run(cmd)
