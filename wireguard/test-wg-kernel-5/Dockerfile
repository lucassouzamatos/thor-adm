FROM alpine:edge

USER root

RUN apk add -U wireguard-tools

COPY wg-quick.patch /

RUN patch /usr/bin/wg-quick /wg-quick.patch  

COPY entrypoint.sh /

RUN chown root:root /entrypoint.sh ; chmod 700 /entrypoint.sh

CMD ["/entrypoint.sh"]
