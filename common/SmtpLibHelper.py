#!/usr/bin/python
#coding=utf-8

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class SendMailHelper():
    def __init__(self,host,port,sender,receivers,subject,password=None):
        self.host = host
        self.port = port
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.password = password
        self.msg = MIMEMultipart('mixed')
        self.msg['Subject'] = subject
        self.msg['From'] = sender
        self.msg['To'] =  Header(','.join(receivers))

    def add_text(self, text_plain):
        text_plain = MIMEText(text_plain, 'plain', 'utf-8')
        self.msg.attach(text_plain)

    def add_html(self, html):
        text_html = MIMEText(html, 'html', 'utf-8')
        self.msg.attach(text_html)

    def add_img(self, img_name, sendimagefile):
        '''
        发送图片
        调用示例:
            sendimagefile = open(img_path, 'rb').read()
            add_img('ima_name',sendimagefile)
        :param imgname: 图片路径
        :return:
        '''

        image = MIMEImage(sendimagefile)
        image.add_header('Content-ID', '<image1>')
        image["Content-Disposition"] = 'attachment; filename="{}"'.format(img_name)
        self.msg.attach(image)

    def add_file(self,filename,sendfile):
        '''
        发送附件
            调用示例：
                    sendfile = open(r'xxxx.xls', 'rb').read()
                    add_file('file_name',sendfile)
        :param filename: 附件名称
        :param sendfile: 附件文件
        :return:
        '''
        # 构造附件
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # 以下附件可以重命名成aaa.txt
        # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
        # 另一种实现方式
        text_att.add_header('Content-Disposition', 'attachment', filename=filename)
        # 以下中文测试不ok
        # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
        self.msg.attach(text_att)

    def send(self):
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self.host, self.port)
            #smtpobj.login(self.sender,self.password) # 不需要验密的postfix-smtp server
            smtpobj.sendmail(self.sender, self.receivers, self.msg.as_string())
            smtpobj.quit()
            smtpobj.close()
        except smtplib.SMTPException as e:
            print(e)