#!/bin/sh

set -e

# pkill -f 'celery worker'
# pkill -f 'celery beat'

# Start Celery worker
celery -A app worker -E &

# Start Celery Beat
celery -A app beat --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Wait for all background processes to finish
wait