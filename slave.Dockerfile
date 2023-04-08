FROM ubuntu:18.04

USER root
WORKDIR /usr/local

RUN apt update -y
RUN apt install curl \
                wget \
                net-tools \
                gnupg2 \
                mongodb \
                python3 \
                python3-pip \
                software-properties-common \
                apt-transport-https \
                lsb-release -y

RUN apt install erlang rabbitmq-server -y

RUN apt install openjdk-11-jdk -y

COPY . .
RUN pip3 install -r requirements.txt

CMD bash start_slave.sh