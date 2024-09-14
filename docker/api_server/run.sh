#!/bin/bash
# create log directory and file for unit access log 
# and change permissions so that any user can read the log file.
# This is required because originally the unit access log is created by root user
# and the log file has rw permission only for root user.
# It is required so that outside containers can read the log file.
mkdir -p /var/log/unit
touch /var/log/unit/unit-access.log
chmod 644 /var/log/unit/unit-access.log

# start unitd with no-daemon option and control socket
/usr/local/bin/docker-entrypoint.sh unitd --no-daemon --control unix:/var/run/control.unit.sock