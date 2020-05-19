FROM alpine:edge
USER root

# VOLUME instances:ro vpnkeys

RUN apk --update add bash gcc musl-dev python3-dev libffi-dev openssl-dev py3-pip openssh-client

RUN pip3 install ansible -U

ENTRYPOINT ["/bin/bash"]
