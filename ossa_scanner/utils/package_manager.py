import subprocess
import re


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
    elif package_manager == 'brew':
        result = subprocess.run(
            ['brew', 'search', '.'],
            capture_output=True,
            text=True
        )
    else:
        raise ValueError("ER1: Unsupported package manager for search")

    packages = result.stdout.splitlines()
    extracted_packages = []
    max_packages = 2
    k_packages = 0
    for line in packages:
        if not line.strip() or line.startswith("==>"):
            continue
        extracted_packages.append(line.split()[0])
        if k_packages >= max_packages:
            break
        k_packages += 1

    return extracted_packages


def get_package_info(package_manager, package_name):
    if package_manager == 'apt':
        cmd = ['apt-cache', 'show', package_name]
    elif package_manager in ['yum', 'dnf']:
        cmd = ['repoquery', '--info', package_name]
    elif package_manager == 'brew':
        cmd = ['brew', 'info', package_name]
    else:
        raise ValueError("ER: Unsupported package manager for info")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        if package_manager == 'brew':
            return parse_brew_info(output)
        elif package_manager in ['yum', 'dnf']:
            return parse_yum_info(output)
        elif package_manager == 'apt':
            return parse_apt_info(output)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None


def parse_brew_info(output):
    """Parses brew info output to extract license, website, and description."""
    info = {}
    info["name"] = "NOASSERTION"
    info["version"] = "NOASSERTION"
    info["licenses"] = "NOASSERTION"
    info["severity"] = "NOASSERTION"
    info["references"] = "NOASSERTION"
    info["summary"] = "NOASSERTION"
    lines = output.splitlines()

    for i, line in enumerate(lines):
        if line.startswith("==>") and ":" in line:
            new_line = line.lstrip("==>").strip()
            match1 = re.match(r"([^:]+):.*?([\d\.a-zA-Z]+)\s*\(", new_line)
            match2 = re.match(r"([^:]+):", new_line)
            if match1:
                pname = match1.group(1).strip()
                version = match1.group(2).strip()
            elif match2:
                pname = match2.group(1).strip()
                version = "*"
            info["name"] = pname
            info["version"] = version
        elif i == 1:
            info["summary"] = line.strip()
        elif line.startswith("https://"):  # The website URL
            info["references"] = line.strip()
        elif line.startswith("License:"):  # The license information
            info["licenses"] = line.split(":", 1)[1].strip()
    info["severity"] = license_classificaton(info["licenses"])

    return info

def parse_yum_info(output):
    info = {}
    info["name"] = "NOASSERTION"
    info["version"] = "NOASSERTION"
    info["licenses"] = "NOASSERTION"
    info["severity"] = "NOASSERTION"
    info["references"] = "NOASSERTION"
    info["summary"] = "NOASSERTION"
    lines = output.splitlines()
    for line in lines:
        if line.startswith("License"):
            info["licenses"] = line.split(":", 1)[1].strip()
            info["severity"] = license_classificaton(info["licenses"])
        elif line.startswith("URL"):
            info["references"] = line.split(":", 1)[1].strip()
        elif line.startswith("Name"):
            info["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Version"):
            info["version"] = line.split(":", 1)[1].strip()
        elif line.startswith("Summary"):
            info["summary"] = line.split(":", 1)[1].strip()
    return info


def parse_apt_info(output):
    """Parses apt-cache show output."""
    info = {}
    lines = output.splitlines()

    for line in lines:
        if line.startswith("License:") or "License" in line:
            info["licenses"] = line.split(":", 1)[1].strip()
        elif line.startswith("Homepage:"):
            info["website"] = line.split(":", 1)[1].strip()
        elif "Copyright" in line:
            info["references"] = line.strip()
        severity = license_classificaton(info["licenses"])

    # Ensure all keys are present even if data is missing
    return {
        "licenses": info.get("licenses", "NOASSERTION"),
        "copyright": info.get("copyright", "NOASSERTION"),
        "references": info.get("references", "NOASSERTION"),
        "severity": severity,
    }

def license_classificaton(licenses):
    copyleft_licenses = ['GPL', 'CDDL', 'MPL']
    severity = "Informational"
    for cl_license in copyleft_licenses:
        if cl_license.lower() in licenses:
            severity = "Medium"
    return severity
