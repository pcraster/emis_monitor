#!/usr/bin/env bash
set -e


docker build -t test/emis_monitor .
docker run -p3031:3031 test/emis_monitor
