from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
import pymysql
from customer_management.settings import conf_fun,settings





def sql_data(sql):
    print(sql)
    data = conf_fun.connect_mysql(sql, type='dict')
    return data

''' 在平台，国家，语言的条件下进行搜索'''
def search_email(data):
    sql = " SELECT * FROM email_handling "
    count_sql = 'SELECT COUNT(id) as count FROM email_handling'
    page = data.get('page') if data.get('page') else 1
    page = (int(page)- 1) *50
    LIMIT = " LIMIT %s,50"%(page)
    print('data', data ,'\n')
    if data and 'page' in data and len(data.keys()) >1 \
        and data.get('country') and data.get('platform') and data.get('site'):
        sql += ' WHERE '
        count_sql += ' WHERE '
        search_list = []
        for key,value in data.items():
            if key !='page':
                search_list.append("%s = '%s'" % (key, value))
        search_str = ' AND '.join(search_list)
        sql +=  search_str
        sql += ' order by email_date  desc'
        sql += LIMIT

        count_sql += search_str
        count_sql += LIMIT
        count = sql_data(count_sql)
        re_data = sql_data(sql)

    elif data.get('type'):

        count_sql += " WHERE type = '%s'  "%(data.get('type'))
        count_sql += LIMIT
        sql += " WHERE type = '%s'  order by reply_situation desc ,email_date desc "%(data.get('type'))
        sql += LIMIT
        print(count_sql ,'\n')
        print(sql, '\n')
        count = sql_data(count_sql)
        re_data = sql_data(sql)

    else:
        sql += ' order by email_date  desc'
        sql += LIMIT
        count_sql += LIMIT
        count = sql_data(count_sql)
        re_data = sql_data(sql)
    return re_data,count

# 邮件总列表 站内  + 站外
class Email_Manage(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code':200,'msg':'无'}

    def list(self,request):
        data = request.GET
        left_data_dict = conf_fun.left_show()
        re_data, count = search_email(data)
        self.ret['left_data_dict'] = left_data_dict
        self.ret['re_data'] = re_data
        self.ret['count'] = count
        return Response(self.ret)


from django.http import JsonResponse
def email_manage_detail(request):
    data = request.GET
    order_number = data.get('order_number')
    sql = "SELECT * FROM reply_customers WHERE order_number ='{}'".format(order_number)
    data = conf_fun.connect_mysql(sql, type='dict')
    ret = {'code':200}
    ret['data'] = data
    return JsonResponse(ret)
