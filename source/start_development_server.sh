#!/usr/bin/env bash
set -e
docker build -t test/monitor .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/monitor:/monitor test/monitor
