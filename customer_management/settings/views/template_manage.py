from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
import pymysql
from django.http import JsonResponse
from operator import itemgetter
from itertools import groupby
from customer_management.settings import conf_fun


def connect_mysql(sql_text, dbs='operation', type='tuple'):
    conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)

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

def sql_data(sql):
    print(sql)
    data = connect_mysql(sql, type='dict')
    return data

'''获取邮件回复的模板管理下的对应的国家，平台，语言'''
def left_select_condition():
    sql = "SELECT platform,country,language FROM email_reply_template"
    data = sql_data(sql)
    data_dict ={}
    for platform,items in groupby(data, key=itemgetter('platform')):
        data_dict[platform] ={}

        for country, items_1 in groupby(items,key=itemgetter('country')):

            data_dict[platform][country] =[]
            for i in items_1:
                if i.get('language') not in data_dict[platform][country]:
                    data_dict[platform][country].append(i.get('language'))

    print(data_dict)
    return data_dict

''' 在平台，国家，语言的条件下进行搜索'''
def search_template(data):
    sql = " SELECT * FROM email_reply_template "
    count_sql = 'SELECT COUNT(id) as count FROM email_reply_template'

    page = int(data.get('page')) - 1
    LIMIT = " LIMIT %s,20"%(page*20)
    print('data', data ,'\n')
    if data and 'page' in data and len(data.keys()) >1 \
        and data.get('country') and data.get('platform') and data.get('language'):
        sql += ' WHERE '
        count_sql += ' WHERE '
        search_list = []
        for key,value in data.items():
            if key !='page':
                search_list.append("%s = '%s'" % (key, value))
        search_str = ' AND '.join(search_list)
        sql +=  search_str
        sql += LIMIT
        count_sql += search_str
        count = sql_data(count_sql)
        re_data = sql_data(sql)
    else:
        sql += LIMIT
        count = sql_data(count_sql)
        re_data = sql_data(sql)
    return re_data,count

def pull_down_list():

    channel_sql = "SELECT channel FROM parameter WHERE channel !=''"  # 平台
    country_sql = "SELECT country FROM parameter WHERE country !='' " # 国家
    language_sql = "SELECT language_type FROM parameter WHERE language_type !='' " # 语言
    problem_sql = "SELECT problem_type FROM parameter WHERE problem_type !='' " # 语言
    channel_data = sql_data(channel_sql)
    country_data = sql_data(country_sql)
    language_data = sql_data(language_sql)
    problem_sql =  sql_data(problem_sql)
    channel_data, country_data, language_data, problem_sql = \
        type_change(channel_data , country_data ,language_data,problem_sql)
    return channel_data, country_data, language_data, problem_sql

def type_change(channel_data , country_data ,language_data,problem_data ):
    cc, co, ll, pp = [], [],[],[]

    for channel_dict in channel_data:
        q= {}
        q['value'] = channel_dict.get('channel')
        q['label'] = channel_dict.get('channel')
        cc.append(q)

    for  type_dict in country_data:
        q={}
        q['value'] = type_dict.get('country')
        q['label'] = type_dict.get('country')
        co.append(q)

    for store_state_dict in language_data:
        q= {}
        q['value'] = store_state_dict.get('language_type')
        q['label'] = store_state_dict.get('language_type')
        ll.append(q)

    for store_state_dict in problem_data :
        q= {}
        q['value'] = store_state_dict.get('problem_type')
        q['label'] = store_state_dict.get('problem_type')
        pp.append(q)

    return cc, co, ll, pp


'''新增模板信息'''
def add_template_data(data):
    key_list =[]
    value_list = []
    for key,value in data.items():
        key_list.append(key)
        value_list.append("'%s'"%value)

    email_translation = conf_fun.translate_func(data.get('email_content'))
    key_list.append('email_translation')
    value_list.append("'%s'"%(email_translation))
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)
    sql = "INSERT INTO email_reply_template  ( %s ) VALUES (%s)"%(key_str, value_str)
    res = connect_mysql(sql,type='dict')
    return res

''' 检索问题类型/语言/国家 是否存在存在,NO则新增'''
def problem_type_exist(problem_type, country, language ):
    sql = "INSERT IGNORE INTO parameter (problem_type) VALUES ('%s')"%(problem_type)
    country_sql = "INSERT IGNORE INTO parameter (country) VALUES ('%s')"%(country)
    judge_sql = "SELECT * FROM parameter where language_type ='%s' "%(language)
    if not sql_data(judge_sql):
        language_sql = "INSERT  INTO parameter (language_type) VALUES ('%s')"%(language)
        sql_data(language_sql)
    sql_data(sql)
    sql_data(country_sql)

'''返回页数'''
def count_page():
    sql = 'SELECT COUNT(id) as count FROM email_reply_template'
    count = sql_data(sql)
    return count

class Email_Upload_Manage(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg':'无'}

    def list(self,request):
        ser_data_1 = request.GET
        left_data_dict = left_select_condition()
        channel_data, country_data, language_data, problem_data = pull_down_list()
        # count = count_page()
        data,count = search_template(ser_data_1)
        self.ret['channel_data'] = channel_data # 平台下拉框
        self.ret['country_data'] = country_data # 国家下拉框
        self.ret['language_data'] = language_data # 语言下拉框
        self.ret['problem_data'] = problem_data # 问题下拉框
        self.ret['left_data_dict'] = left_data_dict
        self.ret['count'] = count
        self.ret['data']  = data
        print(123)
        return Response(self.ret)

    def create(self,request):
        data = request.data
        print(data)
        problem_type_exist(data.get('problem_type'), data.get('country'), data.get('language'))
        add_template_data(data)
        return Response(self.ret)

    def alter(self,request):
        pass

    def delete(self,request):
        data = request.GET
        id_list = data.getlist('id[]')
        for id in id_list:
            sql = "DELETE FROM email_reply_template WHERE  id= %s" % (int(id))
            connect_mysql(sql)
        return Response(self.ret)

'''sql'''

''' 查询对于邮件模板 '''
def email_template_detail(request):
    ret = {'code' : 200 , 'msg': '无' }
    ser_data_1 = request.GET

    left_data_dict = left_select_condition()
    data, count = search_template(ser_data_1)
    ret['count'] = count
    ret['data'] = data
    ret['left_data_dict'] = left_data_dict

    return JsonResponse(ret)


