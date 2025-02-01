# Open Source Advisory Scanner (Generator)
OSSA-Scanner produces OSSA Advisory files per each package available (installed or not) in any Linux OS that uses RPM or Deb packages.

## Installation

### Centos/AL/AlmaLinux

Installing dependencies, including Software Heritage Scanner for SWHIDs and SSDEEP for FuzzyHashing:

```
$ yum -y update && yum -y groupinstall "Development Tools"
$ yum -y install python-pip python3-devel
$ pip3 install swh-scanner
$ BUILD_LIB=1 pip install ssdeep
$ pip3 install ossa-scanner
```
To upgrade, just execute install with --upgrade
```
pip install --upgrade ossa_scanner
```

### License

This project is licensed under MIT.
