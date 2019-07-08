#!/bin/bash

# Set Timezone
# TIMEZONE must be a valid path in /usr/share/zoneinfo/
if [[ -n "${TIMEZONE}" ]] && [[ -f "/usr/share/zoneinfo/${TIMEZONE}" ]] ; then
    ln -snf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime 
    echo ${TIMEZONE} > /etc/timezone
fi
