from django.http import HttpResponse
from django.shortcuts import render, redirect

import configparser,re,yaml,json
from common.OperationPasswordHelper import EncryptionHelper
from common.OperationTimeHelper import OperationTimeHelper
from common.SmtpLibHelper import SendMailHelper
from work.AdminInfo import AdminInfoHelper
from work.UsersInfo import UsersInfoHelper
from work.UsersLoginInfo import UsersLoginHelper
from work.MailboxInfo import MailboxHelper
from work.OperationDovecotInfo import OperationDovecotHelper
from work.BlackListInfo import BlackListHelper

id_file = 'config/da_ip.yaml'
config = configparser.ConfigParser()
config.read('config/config.ini')

#newcoremail
newcoremail_ip = config.get('newcoremail-database','ip')
nport = config.get('newcoremail-database','port')
newcoremail_port = int(nport)
newcoremail_dbname = config.get('newcoremail-database','dbname')
newcoremail_db_user = config.get('newcoremail-database','dbuser')
newcoremail_db_password = config.get('newcoremail-database','dbpassword')

#tommail
ip = config.get('tommail-database','ip')
sport = config.get('tommail-database','port')
port = int(sport)
dbname = config.get('tommail-database','dbname')
db_user = config.get('tommail-database','dbuser')
db_password = config.get('tommail-database','dbpassword')

#vmail
vsport = config.get('vmail-database','port')
vmail_port = int(vsport)
vmail_dbname = config.get('vmail-database','dbname')
vmail_dbuser = config.get('vmail-database','dbuser')
vmail_dbpassword = config.get('vmail-database','dbpassword')

#redis
rsport = config.get('new-redis','redis_port')
redis_port = int(rsport)
redis_ip = config.get('new-redis','redis_ip')
redis_key = config.get('new-redis','redis_key')

#admin
admin_ip = config.get('admin-database','ip')
sport = config.get('admin-database','port')
admin_port = int(sport)
admin_dbname = config.get('admin-database','dbname')
admin_dbuser = config.get('admin-database','dbuser')
admin_dbpassword = config.get('admin-database','dbpassword')

#smtp
sender = config.get('smtp','login_username')
smtp_host = config.get('smtp','host')
smtp_port = config.get('smtp','port')
int_smtp_port = int(smtp_port)

def get_dict(id_file):
    with open(id_file,'r') as file_object:
        cfg = file_object.read()
        ip_dict = yaml.load(cfg,Loader=yaml.FullLoader)
    return ip_dict

def get_keys(d, value):
    return [k for k,v in d.items() if v == value]

# Create your views here.
def index(request):
    return render(request,'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = AdminInfoHelper(username, admin_ip, admin_port, admin_dbname, admin_dbuser, admin_dbpassword)
        dict_info = admin.get_admin_info()
        if dict_info is not None:
            return render(request, 'register.html', {'dict_info': dict_info['username']+' 已存在'})
        else:
            encry = EncryptionHelper(password)
            db_password = encry.genearteMD5()
            admin.register_admin_info(db_password)
            #return render(request, 'register.html', {'dict_info':'注册成功,可以登录'})
            return redirect("/login/")

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = AdminInfoHelper(username, admin_ip, admin_port, admin_dbname, admin_dbuser, admin_dbpassword)
        dict_info = admin.get_admin_info()
        if dict_info is not None:
            encry = EncryptionHelper(password)
            db_password = encry.genearteMD5()
            if db_password == dict_info['password']:
                request.session['is_login'] = True
                request.session['user_id'] = dict_info['id']
                request.session['user_name'] = dict_info['username']
                return redirect('/index/')
            else:
                return render(request, 'login.html', {'dict_info': '密码不正确'})
        else:
            return render(request, 'login.html', {'dict_info': '用户不存在'})
    return render(request, 'login.html')

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return render(request,'login.html')

def work(request):
    username = request.session.get('user_name')
    if username is None:
        return render(request, 'login.html',{'dict_info': '你尚未登录,请登录系统'})
    else:
        request.session['user_name'] = username
        return render(request,'index.html')

def reset_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        admin = AdminInfoHelper(username, admin_ip, admin_port, admin_dbname, admin_dbuser, admin_dbpassword)
        dict_info = admin.get_admin_info()
        if dict_info is not None:
            receivers = [email]
            smtper = SendMailHelper(smtp_host,int_smtp_port,sender,receivers,'重置您的 TOM运维平台 帐户密码')
            mail_msg = """
            <p>点击下面重置密码的链接</p>
            <p><a href="http://172.25.16.201:8000/update_password/">重置密码</a></p>
            """
            smtper.add_html(mail_msg)
            smtper.send()
            return render(request, 'reset_password.html', {'dict_info': '已发送邮件'})
        else:
            return render(request, 'reset_password.html', {'dict_info': '用户不存在'})
    return render(request,'reset_password.html')

def update_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if re.match("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).*$",password1)==None:
            return render(request, 'update_password.html', {'dict_info': '密码必须包括字母大小写和数字'})
        elif len(password1) < 6 or len(password1) > 20:
            return render(request, 'update_password.html', {'dict_info': '密码不足6位,密码大于10位请重新输入'})
        elif password2 != password1:
            return render(request, 'update_password.html', {'dict_info': '2次输入的密码不一致,请重新输入'})
        admin = AdminInfoHelper(username, admin_ip, admin_port, admin_dbname, admin_dbuser, admin_dbpassword)
        encry = EncryptionHelper(password1)
        db_password = encry.genearteMD5()
        admin.update_admin_password(db_password)
        return render(request, 'update_password.html', {'dict_info': '密码已重置,可以登录'})
    return render(request,'update_password.html')

def get_user_info(request):
    if request.method == "POST":
        mail_user = request.POST.get("mail_user")
        operation = OperationTimeHelper()
        userinfo = UsersInfoHelper(mail_user, ip, port, dbname, db_user, db_password)
        dict_usersinfo = userinfo.get_net_user_info()
        if dict_usersinfo is not None:
            reg_ip = dict_usersinfo['reg_ip']
            if dict_usersinfo['reg_time'] is not None:
                try:
                    reg_time = operation.datetime_to_strdatetime(dict_usersinfo['reg_time'])
                except:
                    reg_time = dict_usersinfo['reg_time']
            else:
                reg_time = ""
            user_status = dict_usersinfo['status']
            if dict_usersinfo['due_date'] is not None:
                try:
                    due_date = operation.datetime_to_strdatetime(dict_usersinfo['due_date'])
                except:
                    due_date = dict_usersinfo['due_date']
            else:
                due_date = ""
            userlogin = UsersLoginHelper(mail_user,ip,port,dbname,db_user,db_password, redis_ip, redis_port, redis_key)
            dict_login_time = userlogin.get_user_webmail_login()
            if dict_login_time is not None:
                webmail_login_time = operation.datetime_to_strdatetime(dict_login_time['login_time'])
            else:
                webmail_login_time = ""
            dict_client_login_time = userlogin.get_user_client_login()
            if dict_client_login_time is not None:
                client_login_time = operation.timestamp_to_strdatetime(dict_client_login_time)
            else:
                client_login_time = ""
            dict_info = {'mail_user': mail_user,'user_status':user_status,'reg_time': reg_time, 'reg_ip': reg_ip, 'due_time': due_date,
                         'webmail_login_time': webmail_login_time,'client_login_time':client_login_time}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")
        else:
            dict_info = {'Message':'not found user'}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")

def get_user_dovecot_info(request):
    if request.method == "POST":
        dovecot_info = request.POST.get("mailbox_user")
        userinfo = UsersInfoHelper(dovecot_info, ip, port, dbname, db_user, db_password)
        dict_usersinfo = userinfo.get_net_user_info()
        values = {'basecdnid':dict_usersinfo['basecdnid'],'nfsid':dict_usersinfo['nfsid']}
        dict_id = get_dict(id_file)
        list_da_ip = get_keys(dict_id,values)
        if len(list_da_ip) == 1:
            mailbox = MailboxHelper(dovecot_info,list_da_ip[0],vmail_port,vmail_dbname,vmail_dbuser,vmail_dbpassword)
            da_info = mailbox.get_mailbox_info()
            return HttpResponse(json.dumps(da_info), content_type="application/json")
        else:
            dict_info = {'Message': 'not found da user'}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")

def get_user_quota_info(request):
    if request.method == "POST":
        mail_user = request.POST.get('da_user')
        userinfo = UsersInfoHelper(mail_user, ip, port, dbname, db_user, db_password)
        dict_usersinfo = userinfo.get_net_user_info()
        values = {'basecdnid': dict_usersinfo['basecdnid'], 'nfsid': dict_usersinfo['nfsid']}
        dict_id = get_dict(id_file)
        list_da_ip = get_keys(dict_id, values)
        if len(list_da_ip) == 1:
            operation = OperationDovecotHelper(mail_user,list_da_ip[0])
            res = operation.get_user_quota()
            values = res[1].split(' ')
            storage = [x for x in values if x != '']
            list_number = res[2].split('Quota')
            number2 = list_number[0]
            values2 = number2.split(' ')
            message = [x for x in values2 if x != '']
            dict_quota = {
                'da_ip': list_da_ip[0],
                'mail_user': mail_user,
                'total_storage': storage[3],
                'used_storage': storage[2],
                'used_storage_percent': storage[4].strip('\n'),
                'total_messgage': message[3],
                'used_message': message[2],
                'used_message_percent': message[4]
            }
            return HttpResponse(json.dumps(dict_quota), content_type="application/json")
        else:
            dict_info = {'Message': 'not found da user'}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")

def recalc_user_quota_info(request):
    if request.method == "POST":
        mail_user = request.POST.get('recalc_user')
        userinfo = UsersInfoHelper(mail_user, ip, port, dbname, db_user, db_password)
        dict_usersinfo = userinfo.get_net_user_info()
        values = {'basecdnid': dict_usersinfo['basecdnid'], 'nfsid': dict_usersinfo['nfsid']}
        dict_id = get_dict(id_file)
        list_da_ip = get_keys(dict_id, values)
        if len(list_da_ip) == 1:
            operation = OperationDovecotHelper(mail_user,list_da_ip[0])
            res = operation.recalc_user_quota()
            da_ip = res[0].split('|')[0]
            return_code = res[0].split('|')[2].split('=')[1].split('>>')[0].strip(' ')
            dict_recalc_result = {'mail_user': mail_user, 'da_ip': da_ip, 'return_code': return_code}
            return HttpResponse(json.dumps(dict_recalc_result), content_type="application/json")
        else:
            dict_info = {'Message': 'not found da user'}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")

def change_user_quota_info(request):
    if request.method == "POST":
        mail_user = request.POST.get('storage_mail_user')
        storage = request.POST.get('storage_mail_value')
        userinfo = UsersInfoHelper(mail_user, ip, port, dbname, db_user, db_password)
        dict_usersinfo = userinfo.get_net_user_info()
        values = {'basecdnid': dict_usersinfo['basecdnid'], 'nfsid': dict_usersinfo['nfsid']}
        dict_id = get_dict(id_file)
        list_da_ip = get_keys(dict_id, values)
        if len(list_da_ip) == 1:
            mailbox = MailboxHelper(mail_user, list_da_ip[0], vmail_port, vmail_dbname, vmail_dbuser,vmail_dbpassword)
            mailbox.update_mailbox_storage(storage)
            dict_storage_result = {'mail_user':mail_user,'da_ip':list_da_ip[0]}
            return HttpResponse(json.dumps(dict_storage_result), content_type="application/json")
        else:
            dict_info = {'Message': 'not found da user'}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")

def select_domain_blacklist_info(request):
    if request.method == "POST":
        rec_domain = request.POST.get('select_domain_blacklist')
        blh = BlackListHelper(rec_domain,newcoremail_ip,newcoremail_port,newcoremail_dbname,newcoremail_db_user,newcoremail_db_password)
        dict_data = blh.get_domain_status()
        if dict_data is not None:
            return HttpResponse(json.dumps(dict_data), content_type="application/json")
        else:
            dict_info = {'Message': 'domain black list'}
            return HttpResponse(json.dumps(dict_info), content_type="application/json")
