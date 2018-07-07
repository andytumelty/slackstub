#!/bin/sh

docker build . -t slackstub:dev
docker run -p 5000:5000 --env FLASK_DEBUG=1 slackstub:dev $*
