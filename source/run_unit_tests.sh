#!/usr/bin/env bash
set -e


docker build -t test/monitor .
docker run --env ENV=TEST -p5000:5000 test/monitor
