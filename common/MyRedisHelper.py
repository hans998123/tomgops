#!/usr/bin/python3
# -*- coding: utf-8 -*-

import redis

class MyRedisHelper():
    def __init__(self,host='localhost',port=6379,password=None,db=0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.__redis = redis.StrictRedis(host,port,password,db)

    def set(self,key,value):
        return self.__redis.set(key,value)

    def get(self,key):
        if self.__redis.exists(key):
            return self.__redis.get(key)
        else:
            return None