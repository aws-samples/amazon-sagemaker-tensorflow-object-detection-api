FROM tensorflow/tensorflow:2.9.0-gpu

ARG DEBIAN_FRONTEND=noninteractive

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
# Adding the above 2 lines to workaround a recent issue introduced by NVIDIA https://github.com/NVIDIA/nvidia-docker/issues/1632

# Install apt dependencies
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
