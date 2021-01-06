#!/usr/bin/python3
#coding=utf-8

from common.MysqlHelper import MysqlHelper

class AdminInfoHelper():

    def __init__(self,username,ip,port,dbname,dbuser,dbpassword):
        self.username = username
        self.ip = ip
        self.port = port
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpassword = dbpassword

    def get_admin_info(self):
        mysqlhelper = MysqlHelper(self.ip,self.port,self.dbname,self.dbuser,self.dbpassword)
        sql = "select * from administrator where username = '%s'"%(self.username)
        json_info = mysqlhelper.get_all(sql)
        for dict in json_info:
            if dict is not None:
                return dict
            else:
                return None
        mysqlhelper.close()

    def register_admin_info(self,password):
        mysqlhelper = MysqlHelper(self.ip, self.port, self.dbname, self.dbuser, self.dbpassword)
        sql = "insert into administrator (username,password) value ('%s','%s')"%(self.username,password)
        mysqlhelper.insert(sql)
        mysqlhelper.close()

    def update_admin_password(self,password):
        mysqlhelper = MysqlHelper(self.ip, self.port, self.dbname, self.dbuser, self.dbpassword)
        sql = "update administrator set password = '%s' where username='%s'"%(password,self.username)
        mysqlhelper.update(sql)
        mysqlhelper.close()