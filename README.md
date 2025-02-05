# ossa_scanner
Open Source Advisory Scanner (Generator)

## Centos/AL/AlmaLinux

```
$ yum -y update
$ yum -y groupinstall "Development Tools"
$ yum -y install python-pip python3-devel
$ pip3 install swh-scanner
$ BUILD_LIB=1 pip install ssdeep
$ pip3 install ossa-scanner
```

## Ubuntu/Debian
```
$ apt-get update -y && apt-get upgrade -y
$ apt install python3-pip -y
$ apt remove python3-blinker python3-zipp python3-urllib3 python3-typing-extensions python3-six -y
$ pip install swh-scanner --break-system-packages
$ apt install ssdeep python3-ssdeep -y
$ pip3 install ossa-scanner --break-system-packages
```


### *** Running in background ***
```
> nohup ossa_scanner &
```
> pip install --upgrade ossa_scanner
cp -nf /home/ec2-user/* /home/ec2-user/OpenSourceAdvisoryDatabase/advisories/ && cd /home/ec2-user/OpenSourceAdvisoryDatabase/advisories/ && git add * && git commit -am 'Importing AmazonLinux OSSA' && git push
