# viam-minipupper-py
Mini Pupper driver using Viam Python SDK

## Running this package within a Docker container

First build the container image:

```bash
~$ cd viam-minipupper-py
~$ docker build -t zmk5/viam:pupper
```

```bash
~$ docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/home/ubuntu/viam_minipupper_py --net=host zmk5/viam:pupper /bin/bash
```
