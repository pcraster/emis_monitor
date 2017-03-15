#!/usr/bin/env bash
set -e


docker build -t test/emis_monitor .
docker run \
    --env EMIS_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/emis_monitor:/emis_monitor \
    test/emis_monitor
