#!/bin/bash

[[ $# -eq 1 ]] && container_name="$1"

image_name=pytiltdev

# Build Image
docker build . -t $image_name

# Run Image
docker run --rm -it \
  --mount type=bind,src=$HOME,dst=/home/$USER \
  --net=host \
  ${container_name:+--name "$container_name"} \
  $image_name
