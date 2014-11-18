#!/bin/bash
name=services_monitor
cd /usr/local/services/$name/
PIDS=`ps -ef |grep $name |grep -v grep | wc -l`
echo $PIDS
if [ $PIDS -eq 0 ]; then
 python $name.py >>/usr/local/services/$name/log/$name.log 2>&1 &
fi
