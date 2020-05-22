#!/bin/sh

interface="wg0"

wg-quick up "$interface"

trap "wg-quick down $interface" INT TERM

sleep infinity &
wait $!
