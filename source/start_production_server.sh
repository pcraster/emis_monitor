#!/usr/bin/env bash
set -e


docker build -t test/monitor .
docker run -p3031:3031 test/monitor
