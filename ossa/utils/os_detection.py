import platform

def detect_os():
    dist, _, _ = platform.linux_distribution(full_distribution_name=False)
    if 'Ubuntu' in dist or 'Debian' in dist:
        return 'apt'
    elif 'Red Hat' in dist or 'CentOS' in dist or 'AlmaLinux' in dist:
        return 'yum'
    else:
        raise ValueError("Unsupported OS")
