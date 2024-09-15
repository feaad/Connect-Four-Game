#!/bin/sh

set -e

# envsubst </etc/nginx/default.conf.tpl >/etc/nginx/conf.d/default.conf

envsubst '$LISTEN_PORT $APP_HOST $APP_PORT $DAPHNE_PORT' </etc/nginx/default.conf.tpl >/etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'
