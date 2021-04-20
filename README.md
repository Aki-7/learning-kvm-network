# Leaning network with kvm

This is for my personal studying.
I don't recommend you to run this in your computer.

## Environment

```
$ cat /etc/os-release

NAME="Ubuntu"
VERSION="20.04.2 LTS (Focal Fossa)"
...
```

## Prerequests

- python3

```sh
$ pip install -r requirements.txt
```

### Install dependencies

Install following packages using apt

```
qemu-kvm/focal-updates 1:4.2-3ubuntu6.15 amd64
libvirt-daemon-system/focal-updates,now 6.0.0-0ubuntu8.8 amd64
bridge-utils/focal,now 1.6-2ubuntu1 amd64
libvirt-clients/focal-updates,now 6.0.0-0ubuntu8.8 amd64
virtinst/focal-updates,focal-updates,now 1:2.2.1-3ubuntu2.1 all
cloud-image-utils/focal,focal,now 0.31-7-gd99b2d76-0ubuntu1 all
```

### Install Ubuntu clound image

```sh
$ cd img
$ wget https://cloud-images.ubuntu.com/releases/18.04/release/ubuntu-18.04-server-cloudimg-amd64.img
```

## Setup

```sh
$ ./main.py setup
```

## Teardown

```sh
$ ./main.py teardown
```