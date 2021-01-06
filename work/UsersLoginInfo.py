#!/usr/bin/python3
#coding=utf-8

from common.MyRedisHelper import MyRedisHelper
from common.MysqlHelper import MysqlHelper

class UsersLoginHelper():

    def __init__(self,mail_user,ip,port,db_name,db_user,db_password, redis_ip, redis_port, redis_key):
        self.mail_user = mail_user
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.redis_ip = redis_ip
        self.redis_port = redis_port
        self.redis_key = redis_key

    def get_user_client_login(self):
        myredis = MyRedisHelper(self.redis_ip,self.redis_port)
        values = myredis.get(self.redis_key + self.mail_user)
        if values is not None:
            strvalues = str(values, 'utf-8')
            return int(strvalues)
        else:
            return None

    def get_user_webmail_login(self):
        mysqlhelper = MysqlHelper(self.ip,self.port,self.db_name,self.db_user,self.db_password, charset='utf8')
        sql = "select login_time from USER_LOGIN_HISTORY where username='%s' order by login_time desc limit 1" % (self.mail_user)
        data_tuple = mysqlhelper.get_all(sql)
        if len(data_tuple) != 0:
            for data in data_tuple:
                return data
        else:
            return None
        mysqlhelper.close()