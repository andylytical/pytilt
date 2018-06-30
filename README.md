# pytilt
Save tilt data to a local file

# Dependencies
* https://github.com/iolate/rasp-ble-scanner.git

# Docker container setup - development
Assume RPi setup through [docker setup](https://github.com/andylytical/brewpi-scripts/blob/master/README.md)
step is completed.
* `cd /home/pi`
* `git clone git@github.com:andylytical/pytilt.git`
* `curl -o pytilt/blescan.py https://github.com/iolate/rasp-ble-scanner/blob/master/blescan.py`
* `git clone git@github.com:andylytical/dockerfiles.git`
* `cd dockerfiles/Python3; ./lrun.sh`
