#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [[ ! -z "${LOAD_SAMPLE_DATA}" ]]; then
	if [[ "$LOAD_SAMPLE_DATA" == "True" ]]; then
		python manage.py flush --noinput
		python manage.py loaddata sample_data.json
	fi
fi

if [[ ! -z "${SUPERUSER_USERNAME}" ]]; then
	python manage.py init_su
fi

# Start Daphne
daphne -b 0.0.0.0 -p 9001 app.asgi:application &

# Start uWSGI
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
