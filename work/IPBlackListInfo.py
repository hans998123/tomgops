#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.MysqlHelper import MysqlHelper

class IPBlackListHelper():

    def __init__(self,ip_info,ip,port,db_name,db_user,db_password):
        self.ip_info = ip_info
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_ip_status(self):
        mysql_helper = MysqlHelper(self.ip, self.port, self.db_name, self.db_user, self.db_password)
        sql = 'select * from ipblacklist where ip_address like "%%%s%%"'%(self.ip_info)
        json_data = mysql_helper.get_all(sql)
        for dict_data in json_data:
            if dict_data is not None:
                return dict_data
            else:
                return None
        mysql_helper.close()