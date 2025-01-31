# ossa_scanner
Open Source Advisory Scanner (Generator)

## Centos/AL/AlmaLinux
Install Python PyPI:

> yum -y update
> yum -y groupinstall "Development Tools"
> yum -y install python-pip python3-devel
> pip3 install swh-scanner
> BUILD_LIB=1 pip install ssdeep
> pip3 install ossa-scanner
> nohup ossa_scanner &
> pip install --upgrade --force-reinstall
