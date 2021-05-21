import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def Mailer(to_list, th1=None, Subject=None, unipath=None,mail_host=None,mail_user =None, mail_pwd  =None ):
    # mail_host = 'smtp.qq.com'  # 邮箱服务器
    # mail_user = '1055405738@qq.com'  # 发件人邮箱密码(当时申请smtp给的口令)
    # mail_pwd = 'dsivefixwfgjbfbj'  # SMTP密码
    s = smtplib.SMTP_SSL(mail_host, 465, timeout=5)
    s.login(mail_user, mail_pwd)
    # 邮件内容
    mail = str(th1)
    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = mail_user
    msg['Subject'] = Subject
    msg['To'] = ",".join(to_list)
    if len(unipath) > 0:
        for i in unipath:
            att1 = MIMEText(open(i, 'rb').read(), 'base64', 'gb2312')
            att1["Content-Type"] = 'application/octet-stream'
            att1.add_header('Content-Disposition', 'attachment', filename=(Subject + '.' + i.split('.')[1]))
            msg.attach(att1)
    msg.attach(msgtext)
    try:
        s.sendmail(mail_user, to_list, msg.as_string())
        s.close()
        print('发送成功')
    except Exception as e:
        print(e)