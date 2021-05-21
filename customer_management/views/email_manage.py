import pymysql
from settings import conf_fun
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from customer_management.settings import settings
from customer_management.settings import conf_fun as conf_fun_1




def sql_data(sql):
    print('??????????????',sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    return data

''' 在平台，国家，语言的条件下进行搜索'''
def search_email(data):
    sql = " SELECT * FROM email_handling WHERE id >0 {0} order by reply_situation desc ,email_date desc limit {1}, 50"
    count_sql = 'SELECT COUNT(id) as count FROM email_handling where  id>0 {0}'
    page = data.get('page') if data.get('page') else 1
    page = (int(page)- 1) *50
    if data and 'page' in data and len(data.keys()) >1 \
        and data.get('country') and data.get('platform') and data.get('site'):

        search_str =''
        for key,value in data.items() :
            if key !='page' and value:
                search_str +=" AND %s = '%s'" % (key, value)
        sql = sql.format(search_str, page)
        count_sql = count_sql.format(search_str)

    elif data.get('type'):
        ser_str = ''
        reply_situation = data.get('reply_situation')
        if reply_situation:
            ser_str += " AND reply_situation = '{0}'".format(reply_situation)
        ser_str += "  AND type = '%s'  "%(data.get('type'))
        sql  = sql.format(ser_str, page)
        count_sql = count_sql.format(ser_str)
    else:
        sql = sql.format('' ,page)
        count_sql = count_sql.format('')
    print(count_sql, '\n')
    print(sql, '\n')
    count = sql_data(count_sql)
    re_data = sql_data(sql)
    return re_data,count

# 邮件总列表 站内  + 站外
class Email_Manage(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code':200,'msg':'无'}

    def list(self,request):
        data = request.GET
        print('搜索的数据\n\n\n\n',data)
        left_data_dict = conf_fun_1.left_show()

        print('\n这是左侧的数据' ,left_data_dict)
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
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    ret = {'code':200}
    ret['data'] = data
    return JsonResponse(ret)
