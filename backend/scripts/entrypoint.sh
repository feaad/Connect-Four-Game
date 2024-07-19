#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [[ ! -z "${SUPERUSER_USERNAME}" ]]; then
	python manage.py init_su
fi

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
