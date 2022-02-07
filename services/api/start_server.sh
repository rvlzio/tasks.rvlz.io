#!/bin/sh

gunicorn -c /src/infrastructure/gunicorn/__init__.py \
--chdir /src entrypoints.flask_api:app --bind 0.0.0.0:80 --reload
