FROM tensorflow/tensorflow:2.2.0-gpu

ARG DEBIAN_FRONTEND=noninteractive

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