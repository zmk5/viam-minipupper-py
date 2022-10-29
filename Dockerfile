FROM ubuntu:jammy

ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=1000

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl \
        git \
        nano \
        python3-pip \
        sudo \
        tmux \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -U pip && \
    python3 -m pip install \
        black \
        numpy \
        rich \
        scipy \
        viam-sdk


RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

WORKDIR /home/$USERNAME