#!/usr/bin/env bash
# run.sh: start the Study Tracker development server with one command.

# Stop at the first error, instead of continuing with a broken setup.
set -e

# Go to the folder this script lives in, so it works no matter where you run it from.
cd "$(dirname "$0")"

# Turn on the virtual environment (same as typing it by hand).
source venv/bin/activate

# Apply any new migrations that came with the latest git pull.
python manage.py migrate

# Start the server. "$@" passes along any extra words you type, e.g. ./run.sh 0.0.0.0:8000
python manage.py runserver "$@"
