import poplib
import datetime
import email
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import pymysql
import os
from django.http import JsonResponse
from customer_management.settings import conf_fun


def decode_str(str_in):
    value, charset = decode_header(str_in)[0]
    if charset:
        value = value.decode(charset)
    return value


def connect_mysql(sql_text, dbs='operation', type='tuple'):
    conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)
    # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)

    if type == 'tuple':
        cursor = conn.cursor()
    else:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_text)
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    try:
        # 执行sql语句
        cursor.execute(sql_text)
        # 提交到数据库执行
        conn.commit()
    except:
        # 如果发生错误则回滚
        conn.rollback()
    conn.close()
    return response


'''向email_handling存放顾客的邮件'''


def storage_sql(outbox_email, email_content, email_title, email_file_path, memory_time,
                attachment_files_str, email_address):
    # 先判断目标邮件 是否存在 以 顾客邮箱,标题来判断

    outbox_email_1 = outbox_email.split(' ')[-1].rstrip('>').lstrip('<')
    print('这里又是什么', outbox_email_1, attachment_files_str)
    email_content = re.sub(r'<[^>]+>', '', email_content)
    email_translation, match_language = conf_fun.translate_func(email_content)
    recent_email_content = email_content.replace("'" , '').replace('"', '')

    

    email_date = ''
    judge_sql = "SELECT email_date FROM email_handling WHERE outbox_email ='{0}' and email_title ='{1}'" \
        .format(outbox_email_1, email_title)
    # print(judge_sql)
    judge_data = connect_mysql(judge_sql, type='dict')
    print('这是验证的吗\n', judge_data, 1231231, type(judge_data))
    if judge_data:
        email_date = judge_data[0].get('email_date')
    print(email_date, '对比的时间', memory_time)
    if memory_time != email_date and email_date:
        print('这是更新吗', memory_time, email_date)
        update_sql = " UPDATE email_handling SET email_content ='{0}' ,email_date ='{1}', reply_situation = '{2}' ," \
                     "email_translation = '{5}'} WHERE outbox_email ='{3}' and email_title ='{4}'" \
            .format(email_content, memory_time, '未回复', outbox_email_1, email_title, email_translation)
        print('这是更新邮件的sql', update_sql)
        connect_mysql(update_sql, type='dict')

    elif email_date == '':
        sql = "INSERT ignore INTO email_handling " \
              "(Inbox_email, outbox_email , email_date, email_content, accessory_addr , " \
              "email_path ,email_title , type ," \
              "reply_situation ,email_translation ,match_language , recent_email_content) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}' , " \
              " '{5}', '{6}', '{7}' ,'{8}', '{9}' , '{10}' ,'{11}')" \
            .format(email_address, outbox_email_1, memory_time, email_content,
                    attachment_files_str, email_file_path,
                    email_title, '站外', '未回复', email_translation, match_language , recent_email_content)
        # print(sql)
        print('插入新的email数据')
        connect_mysql(sql, type='dict')


def get_att(msg_in, str_day_in, email_time_num):
    # import email
    count = 0
    attachment_files = []
    accessory_list = []
    for part in msg_in.walk():
        # 获取附件名称类型
        file_name = part.get_filename()
        # print('邮件附件名字 file_name', file_name)
        # contType = part.get_content_type()
        if file_name:
            h = email.header.Header(file_name)
            # 对附件名称进行解码
            dh = email.header.decode_header(h)
            filename = dh[0][0]

            if dh[0][1]:
                # 将附件名称可读化
                filename = decode_str(str(filename, dh[0][1]))
                # print('将附件名称可读化 filename', filename)
                count += 1
                # filename = filename.encode("utf-8")
            # 下载附件
            data = part.get_payload(decode=True)
            # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            # 文件后缀
            hz_name = filename.split('.')[-1]
            # 将所有HEIC后缀的图片文件换成jpg格式，方便预览
            if hz_name == 'HEIC':
                hz_name = 'jpg'

            email_file_site = "{0}{1}{2}{3}{4}{5}{6}" \
                .format(r'static/data/email/image/', str(str_day_in), '-%s' % str(email_time_num), '_', str(count), '.',
                        hz_name)
            # file_path = os.path.join(os.getcwd(), r'static/data/email/')
            path = os.path.join(os.getcwd(), email_file_site)

            print('附件地址啊', path)
            att_file = open(path, 'wb')
            attachment_files.append(email_file_site)
            att_file.write(data)  # 保存附件
            att_file.close()
            # accessory_list.append(site_fil.split('/beyoung')[1])
    print('你说你没有附件地址？？', attachment_files)
    return attachment_files


def run_get_email(request):
    ret = {'code': 200, 'msg': 'ok'}
    recv_email_by_pop3("1055405738@qq.com", "mqoaluziuwsxbdbh", "pop.qq.com", 995)
    recv_email_by_pop3('homeyfine@foxmail.com', 'qyzoirojotowdedf', 'pop.qq.com', 995)
    return JsonResponse(ret)


# 此函数通过使用poplib实现接收r邮件
def recv_email_by_pop3(email_address, email_password, pop_server_host, pop_server_port):
    # 要进行邮件接收的邮箱。改成自己的邮箱
    # email_address = "1055405738@qq.com"
    # 要进行邮件接收的邮箱的密码。改成自己的邮箱的密码
    # 设置 -> 账户 -> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 -> 开启服务：POP3/SMTP服务
    # 设置 -> 账户 -> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 -> 生成授权码
    # email_password = "mqoaluziuwsxbdbh"
    # golxakvxpxfhbefc
    # dsivefixwfgjbfbj
    # 邮箱对应的pop服务器，也可以直接是IP地址
    # 改成自己邮箱的pop服务器；qq邮箱不需要修改此值
    # pop_server_host = "pop.qq.com"
    # 邮箱对应的pop服务器的监听端口。改成自己邮箱的pop服务器的端口；qq邮箱不需要修改此值
    # pop_server_port = 995

    try:
        # 连接pop服务器。如果没有使用SSL，将POP3_SSL()改成POP3()即可其他都不需要做改动
        email_server = poplib.POP3_SSL(host=pop_server_host, port=pop_server_port, timeout=10)
        print("pop3----connect server success, now will check username")
    except:
        print("pop3----sorry the given email server address connect time out")
        exit(1)
    try:
        # 验证邮箱是否存在
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

    # 邮箱中其收到的邮件的数量
    # email_count = len(email_server.list()[1])

    # list()返回所有邮件的编号:
    resp, mails, octets = email_server.list()

    # 遍历所有的邮件
    for i in range(len(mails), 0, -1):
        try:
            email_id = '-'.join(str(mails[i - 1]).split("b'")[1].split("'")[0].split(' '))
            # print('mails[i]', email_id)
            # 通过retr(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
            resp, lines, octets = email_server.retr(i)
            # lines是邮件内容，列表形式使用join拼成一个byte变量
            email_content = b'\r\n'.join(lines)
            try:
                # 再将邮件内容由byte转成str类型
                email_content = email_content.decode('UTF-8')
            except Exception as e:
                print(str(e))
                continue
            # # 将str类型转换成<class 'email.message.Message'>
            # msg = email.message_from_string(email_content)
            msg = Parser().parsestr(email_content)
            print('------------------------------  华丽分隔符  ------------------------------')
            # 写入邮件内容到文件
            email_time = str(msg).split('\n\t')[2].split('; ')[1].split('\n')[0].split(', ')[1].rsplit(' ', 1)[0]

            email_time_num = str(datetime.datetime.strptime(email_time, '%d %b %Y %H:%M:%S')).split(' ')[0]
            memory_time = str(datetime.datetime.strptime(email_time, '%d %b %Y %H:%M:%S'))  # 存储的时间

            day = datetime.date.today()
            one_day = datetime.timedelta(days=3)
            yesterday = day - one_day
            day_list = [str(day), str(yesterday),'2021-02-16','2021-02-15','2021-02-14','2021-02-13','2021-02-12','2021-02-11','2021-02-10']
            # ['2020-12-09', '2020-12-08']
            if email_time_num not in day_list:
                # 倒叙用break
                # break
                # 顺叙用continue
                break
            else:

                # 收取邮件内容
                print('去收邮件', email_id,  email_time_num,day_list)

                outbox_email, email_content, email_title, email_file_path \
                    = parse_email(msg, 0, email_id, {}, email_time_num)

                attachment_files = get_att(msg, email_id, email_time_num)
                print('时间存储', outbox_email, email_title, email_file_path)
                # 收取邮件附件
                print('附件地址', attachment_files)
                attachment_files_str = '@'.join(attachment_files)
                # print('顾客邮箱',outbox_email,'邮件内容\n','邮件标题',email_title[0],'邮件路径',email_file_path
                #       ,'附件列表' ,attachment_files_str)

                storage_sql(outbox_email, email_content, email_title, email_file_path, memory_time,
                            attachment_files_str, email_address)

        except:
            pass
    # 关闭连接
    email_server.close()
    ret = {'code': 200, 'msg': 'wu'}
    return ret


# indent用于缩进显示:
def parse_email(msg, indent, email_ids, dicts, email_time_nums):
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:

        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))
            dicts[header] = value

    if msg.is_multipart():

        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # 递归打印每一个子对象:
            return parse_email(part, indent + 1, email_ids, dicts, email_time_nums)
    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print('%sText: %s' % ('  ' * indent, content))
            dicts['Text'] = content
        else:
            # 不是文本，作为附件处理:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

    if '<!DOCTYPE html>' not in dicts['Text']:
        status = 0
        for p in ['Desk', 'desk', 'Missing', 'missing', 'Order', 'problems ', 'Part', 'Buy', 'Assembly issue', 'Amazon',
                  'Faulty panel',
                  'Portable Wardrobe', 'Shoe', 'JOISCOPE', 'need', 'help', 'amazon']:
            if p in dicts['Text']:
                status += 1
        if status > 0:
            # 邮件内容存储路径

            email_file_site = "%s%s%s" % (r'static/data/email/file/', '%s-%s' % (email_ids, email_time_nums), '.txt')
            file_path = os.path.join(os.path.dirname(os.getcwd()), r'static/data/email/file')
            path = os.path.join(os.getcwd(), email_file_site)
            print(file_path)

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            print('路径',path)
            with open(path, 'wb') as f:
                f.write(dicts['Text'].encode('utf-8'))

            print('email_id',email_ids,'标题','"%s"' % "'".join(dicts['Subject'].split('"')),
                  '发件人邮箱','"%s"' %dicts['From'].split('<')[1].split('>')[0], '邮件文本存储路径',email_file_site,
                )
            outbox_email = dicts['From']  # 发件箱
            email_content = dicts['Text']  # 邮件内容
            email_title = dicts['Subject'].split('"')[0]  # 邮件标题
            email_file_path = email_file_site  # 邮件文本存放路径
            print(123123131231312312)
            return outbox_email, email_content, email_title, email_file_path


# 猜测字符编码
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        print('字符编码\n\n\n\n\n', content_type)
        for item in content_type.split(';'):
            item = item.strip()
            if item.startswith('charset'):
                charset = item.split('=')[1]
                break
    return charset
