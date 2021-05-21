from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from customer_management.settings import conf_fun
import uuid


def customer_sql(data):
    page = data.get('page')
    if not page:page =1
    sql = "SELECT * FROM customer_information as c WHERE id>0 LIMIT {},50"\
        .format((int(page) -1) * 50)
    page_sql = "SELECT COUNT(c.id) AS count_num FROM customer_information as c "
    search_list = []
    for key, value in data.items():
        if key != 'page':
            search_list.append("c.%s = '%s'" % (key, value))
    search_str = ' AND '.join(search_list)

    sql += search_str
    page_sql += search_str
    re_data = conf_fun.connect_mysql(sql, type='dict')
    count_data = conf_fun.connect_mysql(page_sql, type='dict')
    return re_data, count_data

# 客户信息管理
class Customer_Information(ViewSetMixin,APIView):

    def __init__(self):
        self.ret = {'code': 200 ,'msg':'无'}


    def list(self,request):
        data = request.GET
        data_all,count_num = customer_sql(data)
        data_dict = conf_fun.left_show()
        self.ret['data_all'] = data_all
        self.ret['data_dict']  = data_dict
        self.ret['count_num'] = count_num
        print(123,self.ret)
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
