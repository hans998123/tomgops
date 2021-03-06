#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.MysqlHelper import MysqlHelper

class BlackListHelper():

    def __init__(self,domain_name,ip,port,db_name,db_user,db_password):
        self.domain_name = domain_name
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_domain_status(self):
        mysql_helper = MysqlHelper(self.ip, self.port, self.db_name, self.db_user, self.db_password)
        sql = 'select * from blacklist WHERE username like "%%%s%%"' %(self.domain_name)
        json_data = mysql_helper.get_all(sql)
        for dict_data in json_data:
            if dict_data is not None:
                return dict_data
            else:
                return None
        mysql_helper.close()