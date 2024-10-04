#!/bin/sh

set -e

# Redirect all scripts output + leaving stdout to container payload.
exec 3>&1

if [ "$1" = "webserver" ]; then
  echo >&3 "==> Postgres and Server is available - run server..."
  uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload --workers 4 &
fi