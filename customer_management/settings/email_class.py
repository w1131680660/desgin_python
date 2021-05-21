import poplib
import datetime
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import pymysql
import os
from django.http import JsonResponse
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests, json


# 翻译
def translate_func(content):
    translate_url = 'http://www.beyoung.group/translate/'  # 翻译地址
    translate_data = {'passwd': '50fffff9f0225513a93f041e9b939c0b', 'translate_str': content}
    response_data = requests.post(translate_url, data=translate_data)
    json_response_data = json.loads(response_data.content).get('msg')  # 翻译的内容
    data = json.loads(json_response_data)
    language = data.get('from')
    translate_content = data.get('trans_result')
    data_str = ''
    for i in translate_content:
        data_str += i.get('dst')
    # print('翻译后的数据',data_str ,'\n' )
    return data_str, language


# def decode_str(str_in):
#     value, charset = decode_header(str_in)[0]
#     if charset:
#         value = value.decode(charset)
#     return value


# 连接总数据库
def connect_mysql(sql_text, dbs='operation', type='tuple'):
    # conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)
    # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql',
                           passwd='Bymy2021_', db=dbs)
    if type == 'tuple':
        cursor = conn.cursor()
    else:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_text)
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return response


class Get_Email(object):
    # 肖飞的邮件发送
    def __init__(self):
        pass

    ''' 将邮件信息存放到数据库里面'''

    def storage_sql(self, outbox_email, email_content, email_title, email_file_path, memory_time,
                    attachment_files_str, email_address):
        # 先判断目标邮件 是否存在 以 顾客邮箱,标题来判断
        try:
            print(123)
            outbox_email_1 = outbox_email.split(' ')[-1].rstrip('>').lstrip('<')
            email_content_e = email_content.replace('>', ' ').replace('</div>', ' ') \
                .replace('<div>', ' ').replace("'", ' ').replace('"', ' ')
            email_content_e = re.sub(r'<[^>]+>', '', email_content_e)
            # email_content_e  = email_content_e.replace('</div>', '')

            email_translation, match_language = translate_func(email_content_e)
            email_date = ''
            judge_sql = "SELECT email_date FROM email_handling WHERE outbox_email ='{0}' and email_title ='{1}'" \
                .format(outbox_email_1, email_title)

            email_translation = email_translation.replace('>', ' ')

            judge_data = connect_mysql(judge_sql, type='dict')
            if judge_data: email_date = judge_data[0].get('email_date')
            print('\njudge_data', judge_data, email_date)
            if memory_time != email_date and email_date:
                print('这是更新吗', memory_time, email_date)
                update_sql = " UPDATE email_handling SET email_content ='{0}' ,email_date ='{1}', reply_situation = '{2}' ," \
                             "email_translation = '{5}'} WHERE outbox_email ='{3}' and email_title ='{4}'" \
                    .format(pymysql.escape_string(email_content_e), memory_time, '未回复', outbox_email_1, email_title,
                            pymysql.escape_string(email_translation))
                #                update_sql = pymysql.escape_string(update_sql)
                connect_mysql(update_sql, type='dict')

            elif email_date == '':
                sql = "INSERT ignore INTO email_handling " \
                      "(Inbox_email, outbox_email , email_date, email_content, accessory_addr , " \
                      "email_path ,email_title , type ," \
                      " reply_situation ,email_translation ,match_language)  " \
                      "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}' , " \
                      " '{5}', '{6}', '{7}' ,'{8}', '{9}' , '{10}' )" \
                    .format(email_address, outbox_email_1, memory_time, pymysql.escape_string(email_content_e),
                            attachment_files_str,
                            email_file_path, email_title, '站外', '未回复', pymysql.escape_string(email_translation),
                            match_language, )
                #                sql = pymysql.escape_string(sql)
                print('插入新的email数据\n\n', memory_time)
                connect_mysql(sql, type='dict')
        except:
            pass

    def decode_str(self,str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value

    def run_get_email(self):

        self.recv_email_by_pop3("1055405738@qq.com", "mqoaluziuwsxbdbh", "pop.qq.com", 995)
        self.recv_email_by_pop3('homeyfine@foxmail.com', 'qyzoirojotowdedf', 'pop.qq.com', 995)

    def get_att(self, msg_in, str_day_in, email_time_num):
        count = 0
        attachment_files = []
        accessory_list = []
        print('153行\n\n开始接收附件', )
        for part in msg_in.walk():

            file_name = part.get_filename()

#            print('124行\n\n这是附件名字', file_name)
            if file_name:

                h = email.header.Header(file_name)

                dh = email.header.decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
#                    print('\n\n\n138行这里没有是=事吧')
                    filename = self.decode_str(str(filename, dh[0][1]))
#                    print('\n\n\n140行这里没有是=事吧',filename)
                    count += 1

                data = part.get_payload(decode=True)

                hz_name = filename.split('.')[-1]

#                print('\n\n\n139行这里没有是=事吧')
                if hz_name == 'HEIC':
                    hz_name = 'jpg'
                email_file_site = "{0}{1}{2}{3}{4}{5}{6}" \
                    .format(r'static/data/email/image/', str(str_day_in), '-%s' % str(email_time_num), '_', str(count),
                            '.',
                            hz_name)

#                print('是这里报错了？？？？', email_file_site)
                path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), email_file_site)
#                print('文件路径',path)
                att_file = open(path, 'wb')   
#                print(data)             
                att_file.write(data)  #
                att_file.close()
                

#                print('\n\n\n150行是这里',path)
#                path = path.lstrip('/')
#                path = '/'.join(path[4:])
                path = path.split('/')
                path = '/'.join(path[3:])
#                print(path)
                attachment_files.append(path)
        print('你说你没有附件地址？？', attachment_files)
        return attachment_files

    # 此函数通过使用poplib实现接收r邮件
    def recv_email_by_pop3(self, email_address, email_password, pop_server_host, pop_server_port):

        try:

            email_server = poplib.POP3_SSL(host=pop_server_host, port=pop_server_port, timeout=10)
            print("pop3----connect server success, now will check username")
        except:
            print("pop3----sorry the given email server address connect time out")
            exit(1)
        try:

            email_server.user(email_address)
            print("pop3----username exist, now will check password")
        except:
            print("pop3----sorry the given email address seem do not exist")
            exit(1)
        try:
            # 验证邮箱密码是否正确
            email_server.pass_(email_password)
            print("pop3----password correct,now will list email")
        except:
            print("pop3----sorry the given username seem do not correct")
            exit(1)

        resp, mails, octets = email_server.list()

        for i in range(len(mails), 0, -1):
            try:
                email_id = '-'.join(str(mails[i - 1]).split("b'")[1].split("'")[0].split(' '))

                resp, lines, octets = email_server.retr(i)

                email_content = b'\r\n'.join(lines)
                try:

                    email_content = email_content.decode('UTF-8')
                except Exception as e:
                    print(str(e))
                    continue

                msg = Parser().parsestr(email_content)
                print('------------------------------  华丽分隔符  ------------------------------')
                email_time = str(msg).split('\n\t')[2].split('; ')[1].split('\n')[0].split(', ')[1].rsplit(' ', 1)[0]
                email_time_num = str(datetime.datetime.strptime(email_time, '%d %b %Y %H:%M:%S')).split(' ')[0]
                memory_time = str(datetime.datetime.strptime(email_time, '%d %b %Y %H:%M:%S'))  # 存储的时间

                day = datetime.date.today()
                one_day = datetime.timedelta(days=1)
                two_day = datetime.timedelta(days=2)
                qq_day = datetime.timedelta(days=3)
                yesterday = day - one_day
                tow = day - two_day
                qq = day - qq_day
                day_list = ['2021-02-21','2021-02-20',str(day),str(yesterday)]

                print('205日期\n', day_list)
                if email_time_num not in day_list:
                    print('\n日期吗？？', email_time_num, day_list)
                    break
                else:

                    print('\n211行去收邮件')
                    print(email_id, email_time_num)
                    outbox_email, email_content, email_title, email_file_path \
                        = self.parse_email(msg, 0, email_id, {}, email_time_num)

                    print('\n\n220去收附件')
                    attachment_files = self.get_att(msg, email_id, email_time_num)
                    print('221行时间存储', outbox_email, email_title, email_file_path)

                    print('附件地址', attachment_files)
                    attachment_files_str = '@'.join(attachment_files)
                    # 将邮件存放到数据库
                    self.storage_sql(outbox_email, email_content, email_title, email_file_path, memory_time,
                                     attachment_files_str, email_address)
            except:
                pass
        # 关闭连接
        email_server.close()
        ret = {'code': 200, 'msg': 'wu'}
        return ret

    def parse_email(self, msg, indent, email_ids, dicts, email_time_nums):

        if indent == 0:
            # 邮件的From, To, Subject存在于根对象上:
            print(123123123)
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        # 需要解码Subject字符串:
                        value = self.decode_str(value)
                    else:
                        # 需要解码Email地址:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                # print('%s%s: %s' % ('  ' * indent, header, value))
                dicts[header] = value

#        print('250行这这是第一个佛如循环', indent)
        if msg.is_multipart():

            # 如果邮件对象是一个MIMEMultipart,
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                # 递归打印每一个子对象:
                return self.parse_email(part, indent + 1, email_ids, dicts, email_time_nums)
        else:
            # 邮件对象不是一个MIMEMultipart,
            # 就根据content_type判断:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                # print('%sText: %s' % ('  ' * indent, content))
                dicts['Text'] = content
            else:
                # 不是文本，作为附件处理:
                print('%sAttachment: %s' % ('  ' * indent, content_type))

        if '<!DOCTYPE html>' not in dicts['Text']:
            status = 0
            #            print('278\n\n\n\n邮件文本',dicts['Text'])
            for p in ['Desk', 'desk', 'Missing', 'missing', 'Order', 'problems ', 'Part', 'Buy', 'Assembly issue',
                      'Amazon',
                      'Faulty panel',
                      'Portable Wardrobe', 'Shoe', 'JOISCOPE', 'need', 'help', 'amazon']:
                if p in dicts['Text']:
                    status += 1
            if status > 0:
                # 邮件内容存储路径

                email_file_site = "%s%s%s" % (
                    r'static/data/email/file/', '%s-%s' % (email_ids, email_time_nums), '.txt')
                up_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))

                file_path = os.path.join(up_path, r'static/data/email/file')

                path = os.path.join(up_path, email_file_site)
                print('路径地址', file_path)
                print('文本地址', path)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                # print('路径',path)
                with open(path, 'wb') as f:
                    f.write(dicts['Text'].encode('utf-8'))
                print('这里是存储邮件文件份的？？')
                # print('email_id',email_ids,'标题','"%s"' % "'".join(dicts['Subject'].split('"')),
                #       '发件人邮箱','"%s"' %dicts['From'].split('<')[1].split('>')[0], '邮件文本存储路径',email_file_site,
                #     )
                outbox_email = dicts['From']  # 发件箱
                email_content = dicts['Text']  # 邮件内容
                email_title = dicts['Subject'].split('"')[0]  # 邮件标题
                email_file_path = email_file_site  # 邮件文本存放路径
                print(311, '行\n这里是没了吗')
                return outbox_email, email_content, email_title, email_file_path

    # 猜测字符编码
    def guess_charset(self, msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            print('320行字符编码\n\n\n\n\n', content_type)
            for item in content_type.split(';'):
                item = item.strip()
                if item.startswith('charset'):
                    charset = item.split('=')[1]
                    break
        return charset


def Mailer(to_list, th1=None, Subject=None, unipath=None, type=None):
    # mail_host = 'smtp.qq.com'  # 邮箱服务器
    # mail_user = '1055405738@qq.com'  # 发件人邮箱密码(当时申请smtp给的口令)
    # mail_pwd = 'dsivefixwfgjbfbj'  # SMTP密码
    print(23)
    if type == 'qq':
        mail_host = 'smtp.qq.com'  # 邮箱服务器
        mail_user = '1055405738@qq.com'  # 发件人邮箱密码(当时申请smtp给的口令)
        mail_pwd = 'dsivefixwfgjbfbj'  # SMTP密码
        print(22)
    elif type == 'fox':
        mail_host = 'smtp.qq.com'
        mail_user = 'homeyfine@foxmail.com'
        mail_pwd = 'qyzoirojotowdedf'
    else:
        return 'NO'
    s = smtplib.SMTP_SSL(mail_host, 465, timeout=5)
    s.login(mail_user, mail_pwd)
    # 邮件内容
    mail = str(th1)
    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = mail_user  # 发送方信息
    msg['Subject'] = Subject  # 邮件主题
    msg['To'] = to_list  # 接受信息,接受方邮箱
    if len(unipath) > 0:  # 发送附件
        for i in unipath:
            att1 = MIMEText(open(i, 'rb').read(), 'base64', 'gb2312')
            att1["Content-Type"] = 'application/octet-stream'
            att1.add_header('Content-Disposition', 'attachment', filename=(Subject + '.' + i.split('.')[1]))
            msg.attach(att1)
    msg.attach(msgtext)
    # try:
    s.sendmail(mail_user, to_list, msg.as_string())
    s.close()
    print('发送成功')
   
