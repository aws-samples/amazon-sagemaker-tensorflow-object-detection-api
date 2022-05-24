FROM tensorflow/tensorflow:2.2.0-gpu

ARG DEBIAN_FRONTEND=noninteractive

# Install apt dependencies
RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub
# Adding the above 3 lines to workaround a recent issue introduced by NVIDIA https://github.com/NVIDIA/nvidia-docker/issues/1632
RUN apt-get update && apt-get install -y \
    git \
    gpg-agent \
    python3-cairocffi \
    protobuf-compiler \
    python3-pil \
    python3-lxml \
    python3-tk \
    wget

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt --no-cache --upgrade

COPY code /opt/program

ENTRYPOINT ["python3", "/opt/program/prepare_data.py"]
