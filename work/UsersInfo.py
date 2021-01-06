#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.MysqlHelper import MysqlHelper

class UsersInfoHelper():

    def __init__(self,mail_user,ip,port,db_name,db_user,db_password):
        self.mail_user = mail_user
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_baseid_nfsid(self):
        list_mail_user = self.mail_user.split('@')
        user_id = list_mail_user[0]
        domain_name = list_mail_user[1]
        mysql_helper =MysqlHelper(self.ip,self.port,self.db_name,self.db_user,self.db_password)
        sql = "select basecdnid,nfsid from usersinfo where userid='%s' and domainid=(select domain_id from domain where domain_name='%s')" % (user_id, domain_name)
        json_base_id_nf_sid = mysql_helper.get_all(sql)
        for dict_id in json_base_id_nf_sid:
            if dict_id is not None:
                return dict_id
            else:
                return None

    def get_net_user_info(self):
        list_mail_user = self.mail_user.split('@')
        user_id = list_mail_user[0]
        domain_name = list_mail_user[1]
        mysql_helper = MysqlHelper(self.ip, self.port, self.db_name, self.db_user, self.db_password)
        sql = "select * from usersinfo where userid='%s' and domainid=(select domain_id from domain where domain_name='%s')"% (user_id, domain_name)
        json_users_info = mysql_helper.get_all(sql)
        for dict_users_info in json_users_info:
            if dict_users_info is not None:
                return dict_users_info
            else:
                return None

    def update_baseid_nfsid(self,**new_da_id):
        list_mail_user = self.mail_user.split('@')
        user_id = list_mail_user[0]
        domain_name = list_mail_user[1]
        mysql_helper = MysqlHelper(self.ip, self.port, self.db_name, self.db_user, self.db_password)
        setsql = ','.join(['%s=%r' % (k, new_da_id[k]) for k in new_da_id])
        sql = "update usersinfo set %s where userid='%s' and domainid=(select domain_id from domain where domain_name='%s')" % (setsql, user_id, domain_name)
        mysql_helper.update(sql)