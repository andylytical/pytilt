# pytilt
Save tilt data to a local file

# Dependencies
* https://github.com/iolate/rasp-ble-scanner.git

# Docker container setup - development
Assume RPi OS is up to date with git and docker installed (as per https://github.com/andylytical/brewpi-scripts/ through the _Docker Setup_ step.)
* `cd /home/pi`
* `git clone git@github.com:andylytical/pytilt.git`
* `curl -o pytilt/blescan.py https://github.com/iolate/rasp-ble-scanner/blob/master/blescan.py`
* `git clone git@github.com:andylytical/dockerfiles.git`
* `cd dockerfiles/Python3; ./lrun.sh`
