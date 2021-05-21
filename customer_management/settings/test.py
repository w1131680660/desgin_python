import poplib
import datetime
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import pymysql
import os
from django.http import JsonResponse
from customer_management.settings import conf_fun
from  customer_management.settings import get_email_qq


# mail_host = 'smtp.qq.com'  # 邮箱服务器
# mail_user = '1055405738@qq.com'  # 发件人邮箱密码(当时申请smtp给的口令)
# mail_pwd = 'dsivefixwfgjbfbj'  # SMTP密码


def run_get_email():
    ret = {'code':200, 'msg':'ok'}
    get_email_qq.recv_email_by_pop3("1055405738@qq.com" ,  "mqoaluziuwsxbdbh" ,"pop.qq.com" ,995)
    get_email_qq.recv_email_by_pop3('homeyfine@foxmail.com' ,'qyzoirojotowdedf' ,'pop.qq.com' ,995)
    return 123

run_get_email()