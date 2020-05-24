FROM alpine:edge
USER root

RUN apk --update add bash gcc musl-dev python3-dev libffi-dev openssl-dev py3-pip

RUN test -z "$is_setup" ||\
  apk --update add bash gcc musl-dev python3-dev libffi-dev openssl-dev py3-pip openssh-client

RUN pip3 install pip ansible awscli boto3 -U

RUN test -z "$is_setup" ||\
  pip3 install pip ansible awscli boto boto3 -U 

ENTRYPOINT ["/bin/bash", "-c"]
