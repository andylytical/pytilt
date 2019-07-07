#!/bin/bash

apt update

# get python major version
py_major=$( python -c 'import sys; print(sys.version_info[0])' )

if [[ $py_major == '3' ]] ; then
    # Python 3
    echo Found Python3
    set -x
    apt install -y bluetooth libbluetooth-dev
    pip install pybluez
    set +x
else
    echo Unsupported Python version '$py_major'
    exit 1
fi
