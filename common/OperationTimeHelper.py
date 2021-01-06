#!/usr/bin/python3
#coding=utf-8

import datetime,time

class OperationTimeHelper():

    def timestamp_to_strdatetime(self,timestamp):
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def strtdatetime_to_timestamp(self,strtime):
        d = datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        return timeStamp

    def datetime_to_strdatetime(self,dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def cal_time_difference(self,today_timestamp,login_timestamp):
        days = (today_timestamp - login_timestamp)/(24*60*60)
        return int(days)