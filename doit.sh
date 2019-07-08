#!/bin/bash

export TIMEZONE=America/Chicago
#export PYTILT_CSVOUTFILE=tiltdata.csv
#export PYTILT_SAMPLE_PERIOD=2
#export PYTILT_SAMPLE_RATE=1
#export PYTILT_COLOR='RED'

docker run -d \
-e TIMEZONE \
-e PYTILT_CSVOUTFILE \
-e PYTILT_SAMPLE_PERIOD \
-e PYTILT_SAMPLE_RATE \
-v $(pwd):/data \
--net=host \
pytiltdev
