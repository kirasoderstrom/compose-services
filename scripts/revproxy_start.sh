#!/bin/sh -e

# check for new certs every 6 hours
while :; do sleep 6h & wait ${!}; nginx -s reload; done & nginx -g "daemon off;" -c /etc/nginx/nginx.conf
