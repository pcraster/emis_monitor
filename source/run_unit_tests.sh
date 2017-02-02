#!/usr/bin/env bash
set -e


docker build -t test/emis_monitor .
docker run --env ENV=TEST -p5000:5000 test/emis_monitor
