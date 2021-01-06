#!/usr/bin/python3
#coding=utf-8

from common.MyRedisHelper import MyRedisHelper

class UserSentNumberHelper():
    def __init__(self,redid_ip,redis_port,userid,domainid):
        self.redis_ip = redid_ip
        self.redis_port = redis_port
        self.userid = userid
        self.domainid = domainid

    def get_mailuser_send_number(self):
        myredis = MyRedisHelper(self.redis_ip,self.redis_port)
        redis_key = self.userid+"@"+str(self.domainid)
        res = myredis.get(redis_key)
        if res is not None:
            return str(res,'utf-8')
        else:
            return None