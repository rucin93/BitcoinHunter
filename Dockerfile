FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip \
                        gcc \
                        g++ \
                        libc-dev \
                        libssl-dev libgmp3-dev

RUN pip3 install --user Cython ecdsa bitcoinlib --no-use-pep517

COPY . .

RUN chmod 777 run_forever.sh