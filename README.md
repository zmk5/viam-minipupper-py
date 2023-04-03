# viam-minipupper-py

Mini Pupper driver using Viam Python SDK

## Prerequisites

Before using this repository, we must first install and setup some prerequiste packages.

### Installing Ubuntu Jammy Server on an SD card.

You can install either of these versions. The main difference is that the Mate version will come with a GUI if you want to connect your pupper to a monitor while the server addition doesn't.

* Desktop: [Ubuntu Mate](www.ubuntu-mate.org)
* Server: [Ubuntu Server](www.ubuntu.com) (I like this a lot)

You can use any SD card writing tool to install the ISO.

#### [Setup Network Before Ejecting](https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup)

You can do this before unmounting the microSD card. Just browse the `/etc` folder using the file manager or command line.

* Create a `50-cloud-init.yaml` file:

``` bash
$ cd /media/$USER/writable/etc/netplan
$ sudo nano 50-cloud-init.yaml
```

* Modify the file with the following contents:

``` yaml
network:
    version: 2
    renderer: networkd
    ethernets:
        eth0:
        dhcp4: true
        dhcp6: true
        optional: true
    wifis:
        wlan0:
        dhcp4: yes
        dhcp6: yes
        access-points:
            MY_WIFI_SSID:
            password: MY_WIFI_PASSWORD
```

* Disable cloud `systemd` service:
    * Create a file `99-disable-network-config.cfg`:

``` bash
$ cd /media/$USER/etc/cloud/cloud.cfg.d
$ sudo nano 99-disable-network-config.cfg
```

* Modify the file with the following contents:

``` yaml
network: {config: disabled}
```

#### Change devices `hostname`

If using the server version, you should change the hostname from `ubuntu` to something more distinct if you are planning to use multiple Raspberry Pis:

``` bash
$ hostnamectl set-hostname <the-new-hostname-you-want>
```
**NOTE**:  Log out and then log in to see a change!

#### Connect to Pi and Install Ubuntu

If using the Server edition, you can skip this step since everything is mostly configured. However, for the Mate version you will need to go through an installation procedure. For both cases you should use the default username **ubuntu**.

*DO NOT USE A DIFFERENT USERNAME OR THE NEXT STEP WILL NOT WORK!*

### Install the `mini_pupper_bsp`

**MAKE SURE YOUR USER NAME IS `ubuntu` OR THIS CRUCIAL STEP WILL NOTE WORK**

We first install the Mini Puppers Board Support Package (BSP) located [here](https://github.com/mangdangroboticsclub/mini_pupper_bsp). In your home directory, follow these steps:

```bash
$ sudo apt install -y git  # if you don't have it!
$ mkdir QuadrupedRobot
$ cd QuadrupedRobot
$ git clone https://github.com/mangdangroboticsclub/mini_pupper_bsp.git
$ cd mini_pupper_bsp
$ ./install.sh
$ sudo reboot
```

Once the reboot has completed, run these commands to make sure everything was installed correctly.

```bash
$ cd QuadrupedRobot/mini_pupper_bsp
$./test.sh
```

### Install `fuse2`

The default version of FUSE in Ubuntu Jammy is `fuse3`, so we'll have to downgrade to `fuse2` for the `viam-server` to work.

```bash
$ sudo apt install fuse libfuse2
```

## Installing and Running the Package

## EXTRA: Running this package within a Docker container

First build the container image:

```bash
~$ cd viam-minipupper-py
~$ docker build -t zmk5/viam:pupper
```

```bash
~$ docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/home/ubuntu/viam_minipupper_py --net=host zmk5/viam:pupper /bin/bash
```