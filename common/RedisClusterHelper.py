#!/usr/bin/python
# -*- coding: utf-8 -*-

from rediscluster import RedisCluster

class RedisClusterHelper():

    def __init__(self,redis_node):
        self.redis = RedisCluster(startup_nodes=redis_node,decode_responses=True)

    def get(self,key):
        res = self.redis.get(key)
        return res

    def delete(self,key):
        res = self.redis.delete(key)
        return res