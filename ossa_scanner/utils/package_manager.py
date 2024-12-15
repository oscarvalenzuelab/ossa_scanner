import subprocess

def list_packages(package_manager):
    if package_manager == 'apt':
        result = subprocess.run(
            ['apt-cache', 'search', '.'],
            capture_output=True,
            text=True
        )
    elif package_manager in ['yum', 'dnf']:
        result = subprocess.run(
            ['repoquery', '--all'],
            capture_output=True,
            text=True
        )
    else:
        raise ValueError("Unsupported package manager")

    packages = result.stdout.splitlines()
    return [pkg.split()[0] for pkg in packages]

def get_package_info(package_manager, package_name):
    if package_manager == 'apt':
        cmd = ['apt-cache', 'show', package_name]
    elif package_manager in ['yum', 'dnf']:
        cmd = ['repoquery', '--info', package_name]
    else:
        raise ValueError("Unsupported package manager")

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
