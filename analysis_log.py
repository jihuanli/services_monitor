#coding:UTF-8
import os
import re
import string
import sys
import time

kInterval = 10 #分钟, 时间间隔
kIntervalBucketArray = range(0, 60*24/kInterval) #统计数组
kMaxCost = 1000 #毫秒,最大延迟，超过该耗时为图形显示直接设置为Max
kInterfaceNameConf = "/usr/local/services/services_monitor/conf/interface.conf"

class IntervalBucket:
  start_time = 0
  interface_cost_sum = 0 
  interface_cost_cnt = 0
  interface_cost_avg = 0
  def toCostString(self):
    return str(self.start_time) + "\t" + str(self.interface_cost_avg) + "\n"
  def toVisitString(self):
    return str(self.start_time) + "\t" + str(self.interface_cost_cnt) + "\n"

#计算线上接口的耗时
def GetInterfaceTimeCost(log_filename, result_dir, day, interface_name):
  cost_file_name = str(result_dir) + interface_name + "_cost_" + day + ".tsv"
  cost_file = open(cost_file_name, "w")
  visit_file_name = str(result_dir) + interface_name + "_visit_" + day + ".tsv"
  visit_file = open(visit_file_name, "w")
  lines = open(log_filename).readlines()
  time_array = time.strptime(day, "%Y%m%d")  
  timestamp_begin = int(time.mktime(time_array))
  for i in range (0, len(kIntervalBucketArray)):
    kIntervalBucketArray[i] = IntervalBucket()

  for ticket in lines:
    ticket_items = ticket.split("|")
    #if len(ticket_items) != 12:
    #  continue
    #日起
    ticket_time = ticket_items[0].split("-")[3]
    bucket_index = (int(ticket_time)/1000 - int(timestamp_begin))/(int(kInterval)*60)
    if (bucket_index < 0) or (bucket_index > len(kIntervalBucketArray)):
      continue
    #接口
    cur_interface_name = ticket_items[6]
    cur_interface_name = str(cur_interface_name).replace(r"/","")
    cur_interface_name = str(cur_interface_name).replace(r".do","")
    cur_interface_name = str(cur_interface_name).strip()
    #print cur_interface_name
    if interface_name != "all" and cur_interface_name != interface_name:
      continue
    #if re.match(r"[0-9.]+$", ticket_items[11]) == None:
    #  continue
    #耗时
    try:
        kIntervalBucketArray[bucket_index].interface_cost_sum = kIntervalBucketArray[bucket_index].interface_cost_sum + int(ticket_items[11])
    except Exception,e:
        print e
    kIntervalBucketArray[bucket_index].interface_cost_cnt = kIntervalBucketArray[bucket_index].interface_cost_cnt + 1

  cost_file.write("date\tclose\n" )
  visit_file.write("date\tclose\n" )
  for i in range(0, len(kIntervalBucketArray)):
    time_stamp = i*(int(kInterval)*60) + int(timestamp_begin)
    time_array = time.localtime(time_stamp)
    style_time = time.strftime("%H:%M", time_array)
    kIntervalBucketArray[i].start_time = style_time 
    if kIntervalBucketArray[i].interface_cost_cnt != 0:
      kIntervalBucketArray[i].interface_cost_avg = int(kIntervalBucketArray[i].interface_cost_sum) / int(kIntervalBucketArray[i].interface_cost_cnt)
      if int(kIntervalBucketArray[i].interface_cost_avg) > int(kMaxCost):
        kIntervalBucketArray[i].interface_cost_avg = kMaxCost
    #hack ---when cost=0
    if kIntervalBucketArray[i].interface_cost_cnt == 0 and kIntervalBucketArray[i].interface_cost_avg == 0 and i >= 1:
      kIntervalBucketArray[i].interface_cost_avg = kIntervalBucketArray[i-1].interface_cost_avg 
    cost_file.write(kIntervalBucketArray[i].toCostString())
    visit_file.write(kIntervalBucketArray[i].toVisitString())
  
  cost_file.flush()
  cost_file.close()
  visit_file.flush()
  visit_file.close()
  
         
def GetAllInterfaceTimeCost(log_filename, result_dir, day):
  lines = open(kInterfaceNameConf).readlines()
  #GetInterfaceTimeCost(log_filename, day, "all")
  for interface_name in lines:
    print interface_name
    GetInterfaceTimeCost(log_filename, result_dir, day, str(interface_name).strip())

# main
if len(sys.argv) != 4:
  print "Error, input need {log file} {result_dir} {day} ..."
  print "Example: python analysis_log.py /data/log/20141020/dbn-20141020.log /data/services_monitor/ 20141020"
  exit(1)
GetAllInterfaceTimeCost(sys.argv[1], sys.argv[2], sys.argv[3])
