#!/bin/bash

set -x

USER="andylytical"
IMAGE="tiltscanner"
TAG=$( date "+%Y%m%d" )
SRCREPO="https://github.com/andylytical/pytilt.git"
SRCDIR="src"

# Ensure latest code
[[ -d $SRCDIR ]] && rm -rf $SRCDIR
(
    git clone "$SRCREPO" "$SRCDIR"
    cd "$SRCDIR"
    git pull
)

# BUILD IMAGE
docker build . -t $IMAGE:$TAG
docker tag $IMAGE:$TAG $USER/$IMAGE:$TAG
#docker push $USER/$IMAGE:$TAG

