#!/bin/sh

source venv/bin/activate
exec gunicorn -b :5000 --acess-logfile - --error-logfile - "app:create_app('prod')"
