FROM ubuntu:jammy-20231004

RUN apt update

RUN apt install -y python3.11 python3-pip socat curl unzip npm

COPY requirements.txt .

COPY flag3.txt /flag3.txt

RUN python3.11 -m pip install -r requirements.txt

RUN curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v24.4/protoc-24.4-linux-x86_64.zip

RUN unzip protoc-24.4-linux-x86_64.zip -d /usr/local

RUN npm install -g protoc-gen-js

WORKDIR /app

CMD python3.11 chall.py
