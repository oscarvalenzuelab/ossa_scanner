from setuptools import setup, find_packages
import os

def get_version():
    """
    Extract the version from __init__.py.
    """
    version_file = os.path.join(os.path.dirname(__file__), "ossa_scanner", "__init__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Version not found in __init__.py")

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ossa_scanner",
    version=get_version(),
    description="Open Source Software Advisory generator for Core and Base Linux Packages.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    license='MIT',
    url='https://github.com/oscarvalenzuelab/ossa_scanner',
    packages=find_packages(),
    install_requires=[
        "click",
        "swh.model",
        "distro",
        "ssdeep",
    ],
    entry_points={
        "console_scripts": [
            "ossa_scanner=ossa_scanner.cli:main",
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="linux packages SWHID open-source compliance ossa advisory",
)
