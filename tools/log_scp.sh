#!/bin/bash
#contab 
dest_dir="/data/log/"
date=$(date +%Y%m%d -d '1 days ago')
password="jihuanli"
echo "======================start batch scp:$date================="
host="jihuanli@112.124.9.16"
dest_filename=$dest_dir$date"_"$host".tar.gz"
cd $dest_dir
if [ ! -f $dest_filename ];then
  src_filename="/mnt/logs/$date.tar.gz"
  /usr/local/services/services_monitor/tools/scp.exp $host $src_filename $dest_filename $password 
  tar -zxvf $dest_filename 
  cd "/usr/local/services/services_monitor/"
  python analysis_log.py "$dest_dir/$date/dbn-$date.log" "/data/services_monitor/" $date
fi
echo "======================finsh batch scp================="
