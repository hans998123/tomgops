#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.MysqlHelper import MysqlHelper

class MailboxHelper():

    def __init__(self,mail_user,da_ip,port,db_name,db_user,db_password):
        self.mail_user = mail_user
        self.da_ip = da_ip
        self.port = port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_da_path(self):
       mysql_helper = MysqlHelper(self.da_ip,self.port,self.db_name,self.db_user,self.db_password)
       sql = "select home from mailbox where username = '%s'" %(self.mail_user)
       json_da_path = mysql_helper.get_all(sql)
       for dict_da_path in json_da_path:
            if dict_da_path is not None:
                dict_da_path= dict_da_path['home']
                str_da_ip = "".join(dict_da_path)
                return str_da_ip
            else:
                return None

    def get_mailbox_info(self):
        mysql_helper = MysqlHelper(self.da_ip, self.port, self.db_name, self.db_user, self.db_password)
        sql = "select * from mailbox where username='%s'"%(self.mail_user)
        json_mailbox_info = mysql_helper.get_all(sql)
        for dict_mailbox_info in json_mailbox_info:
            if dict_mailbox_info is not None:
                return dict_mailbox_info
            else:
                return None

    def insert_mailbox_info(self,new_da_ip,**dict_mailbox_info):
        mysql_helper = MysqlHelper(new_da_ip, self.port, self.db_name, self.db_user, self.db_password)
        ls = [(k, v) for k, v in dict_mailbox_info.items() if v is not None]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(i[1]) for i in ls)
        sql = "insert into mailbox (" + keys + ") values (" + values + ")"
        mysql_helper.insert(sql)
        mysql_helper.close()

    def update_mailbox_storage(self,storage):
        mysql_helper = MysqlHelper(self.da_ip, self.port, self.db_name, self.db_user, self.db_password)
        sql = "update mailbox set quota_storage='%s' where username='%s';"%(storage,self.mail_user)
        mysql_helper.update(sql)
        mysql_helper.close()