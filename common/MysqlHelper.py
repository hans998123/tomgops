#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql

class MysqlHelper():
    def __init__(self,host,port,db,user,passwd,charset='utf8'):
        self.host = host
        self.port=port
        self.db=db
        self.user=user
        self.passwd=passwd
        self.charset=charset

    def connect(self):
        self.conn=pymysql.connect(host=self.host,port=self.port,db=self.db,user=self.user,passwd=self.passwd,charset=self.charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_all(self,sql):
        res = ()
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return res
    
    def insert(self,sql):
        try:
            self.connect()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
    
    def update(self,sql):
        try:
            self.connect()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def delete(self,sql):
        try:
            self.connect()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)