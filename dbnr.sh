#!/bin/sh

docker build . -t slackstub:dev
docker run -p 5000 slackstub:dev $*
