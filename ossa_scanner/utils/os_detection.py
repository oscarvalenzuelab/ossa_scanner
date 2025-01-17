import os
import distro
import subprocess

def detect_os():
    dist = distro.id()
    if 'ubuntu' in dist or 'debian' in dist:
        return 'apt'
    elif 'redhat' in dist or 'centos' in dist or 'almalinux' in dist:
        return 'yum'
    elif 'darwin' in dist:
        return 'brew'
    else:
        raise ValueError("Unsupported OS")

def detect_pm():
    dist = distro.id()
    if 'ubuntu' in dist or 'debian' in dist:
        return 'apt'
    elif 'redhat' in dist or 'centos' in dist or 'almalinux' in dist:
        return 'yum'
    elif 'darwin' in dist:
        return 'brew'
    else:
        raise ValueError("Unsupported OS")
