#!/bin/bash

set -x

USER="andylytical"
IMAGE="tiltscanner"
TAG=$( date "+%Y%m%d" )-$( git rev-parse --short HEAD )

# BUILD IMAGE
docker build . -t ${IMAGE}:${TAG}
docker tag ${IMAGE}:${TAG} ${USER}/${IMAGE}:${TAG}
docker push ${USER}/${IMAGE}:${TAG}
