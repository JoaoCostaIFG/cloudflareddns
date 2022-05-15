#!/bin/sh

image_name="joaocostaifg/cfddns"
image_tag="$(git rev-parse --short HEAD)"

curr_tag="${image_name}:${image_tag}"
latest_tag="${image_name}:latest"

docker build -t "$curr_tag" .
docker tag "$curr_tag" "$latest_tag"

docker push "$curr_tag"
docker push "$latest_tag"
