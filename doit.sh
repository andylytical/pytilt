#!/bin/bash
set -x

IMAGE=andylytical/tiltscanner:20191007-38b6498
CSV_BASEDIR=tiltdata
BEERNAME='20191013 Pumpkin Joe Brown'

declare -A ENVIRON
ENVIRON[PYTHONUNBUFFERED]=TRUE
ENVIRON[PYTILT_COLOR]=
ENVIRON[PYTILT_CSVOUTFILE]=/${CSV_BASEDIR:-.}/${BEERNAME:-tiltdata}.csv
ENVIRON[PYTILT_SAMPLE_PERIOD]=30
ENVIRON[PYTILT_SAMPLE_RATE]=2
ENVIRON[PYTILT_COLOR]=

for k in "${!ENVIRON[@]}"; do
    envs+=('-e')
    envs+=("$k=${ENVIRON[$k]}")
done

docker run -d --network="host" \
--volume=${HOME}/${CSV_BASEDIR:-.}:/${CSV_BASEDIR} \
"${envs[@]}" \
$IMAGE
