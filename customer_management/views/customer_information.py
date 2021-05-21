from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from customer_management.settings import conf_fun
import uuid
from operator import itemgetter
from itertools import groupby
from customer_management.settings import sql
from settings import conf_fun

def customer_sql(data):
    page = data.get('page')
    search_str = ''
    if not page:page =1
    sql = "SELECT * FROM customer_information as c WHERE c.id>0 {0} LIMIT {1},50"
    page_sql = "SELECT COUNT(c.id) AS count_num FROM customer_information as c  WHERE c.id>0  "
    search_list = []
    for key, value in data.items():
        if key != 'page':
            search_str += (" AND c.%s = '%s' " % (key, value))
    print(search_str)
    sql =sql.format(search_str ,(int(page) -1) * 50)
    page_sql += search_str
    print(123113132112, sql)
    re_data = conf_fun.connect_mysql_operation(sql, type='dict')
    count_data = conf_fun.connect_mysql_operation(page_sql, type='dict')
    return re_data, count_data


def left_show():
    sql = "SELECT platform,country,site FROM store_information where  platform !='' and country !='' and site !='' group by platform,country,site  ORDER BY platform,country"
    print('\n\n\n\n123123123',sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    data_dict ={}
    for platform,items in groupby(data, key=itemgetter('platform')):
        data_dict[platform] ={}

        for country, items_1 in groupby(items,key=itemgetter('country')):

            data_dict[platform][country] =[]
            for i in items_1:

                data_dict[platform][country].append(i.get('site'))

    # print(data_dict)
    return data_dict
# 客户信息管理
class Customer_Information(ViewSetMixin,APIView):

    def __init__(self):
        self.ret = {'code': 200 ,'msg':'无'}


    def list(self,request):
        data = request.GET
        print('\n\n\n',data)

        data_all,count_num = customer_sql(data)
        data_dict =  left_show()
        self.ret['data_all'] = data_all
        self.ret['data_dict']  = data_dict
        self.ret['count_num'] = count_num

        return Response(self.ret)

    def create(self,request):
        data = request.POST
        uid = uuid.uuid4()
        conf_fun.add_template_data(data, 'customer_information', 'uuid', uid)
        return Response(self.ret)

    def alter(self, request):
        data =request.data
        conf_fun.alter_template_data(data, 'customer_information')
        return Response(self.ret)

    def delete(self, request):
        pass
