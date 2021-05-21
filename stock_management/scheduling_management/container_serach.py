from stock_management.scheduling_management import scheduling_sql
from stock_management import scheduling_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import JsonResponse
from operator import itemgetter
from itertools import groupby
from settings import conf_fun

# 获取下拉框
def down_box():
    country = scheduling_sql.country_ser_sql
    store = scheduling_sql.store_ser_sql
    type = scheduling_sql.type_ser_sql

    warehouse = scheduling_sql.warehouse_ser_sql

    country_data = conf_fun.connect_mysql_product_supplier(country)
    store_data = conf_fun.connect_mysql_product_supplier(store)
    type_data = conf_fun.connect_mysql_product_supplier(type)
    warehouse_data = conf_fun.connect_mysql_product_supplier(warehouse)
    re_list = change_type(country_data,store_data, type_data)
    warehouse_dict = {}
    for warehouse_name, item in groupby(warehouse_data ,key=itemgetter('warehouse_name')):
        warehouse_dict[warehouse_name] = []
        for i in item:
            warehouse_dict[warehouse_name].append(i)
    print(warehouse_dict)
    return  re_list,warehouse_dict



def change_type( country_data, site_data ,type):
    country_data_list,site_list, type_list = [], [], []
    re_list = [country_data_list, site_list, type_list]
    an_list =  [ country_data, site_data , type ]
    for_list =['country', 'store', 'type']


    for index, object_list in enumerate(an_list):
        for channel_dict in object_list:
            q = {}

            q['value'] = channel_dict.get(for_list[index])
            q['label'] = channel_dict.get(for_list[index])
            re_list[index].append(q)


    return re_list

def search_container(data):
    ser_str =''
    for key,value in data.items():
        if key !='page':
            if key in ['warehouse_name', 'warehouse_no'] and value:
                ser_str += " AND ca.{0} = '{1}'".format(key,value)
            else:
                ser_str += " AND ar.{0} = '{1}'".format(key,value)

    return ser_str
def container_search(request):

    ret ={'code' :200, 'msg': '无'}
    data = request.GET
    page = data.get('page')  if data.get('page') else 1
    page = (int(page)-1) *50
    print('\n\n\n\n\n','数据',data)
    if len(data.keys()) == 1 :
        search_sql = scheduling_sql.container_search_sql.format('' ,page)
        count_sql  = scheduling_sql.count_sql.format('')
    else:
        search_sql = scheduling_sql.container_search_sql.format(search_container(data),page)
        count_sql = scheduling_sql.count_sql.format(search_container(data), page)
    print(search_sql)
    count_data = conf_fun.connect_mysql_product_supplier(count_sql)
    re_data = conf_fun.connect_mysql_product_supplier(search_sql)
    re_list, warehouse_dict = down_box()
    ret['count_data'] = count_data
    ret['re_data'] = re_data
    ret['re_list'] = re_list
    ret['warehouse_data'] =warehouse_dict
    print(count_data)
    return JsonResponse(ret)


class Container_serch_v2(ViewSetMixin,APIView):

    def __init__(self):
        self.ret ={'code':200,'msg':'无'}

    def list(self, request):
        data = request.GET
        page = int(data.get('page')) if data.get('page') else 1
        page = (page-1) *50
        limit = 'LIMIT {0},{1}'.format(page,50)
        ser_str = ''
        for k,v in data.items():
            if k in ['container_num','site','product_type','warehouse_type','warehouse_name'] and v:
                ser_str += " AND  ood.%s ='%s'" %(k,v)

        sql = scheduling_sql.container_true_sql.format(ser_str,limit)

        count_sql = scheduling_sql.container_true_sql.format(ser_str,'')

        re_data = conf_fun.connect_mysql_operation(sql,type='dict')
        re_count = conf_fun.connect_mysql_operation(count_sql)
        leng = len(re_count)
        self.ret['re_data'] = re_data
        self.ret['len_data'] = leng
        return Response(self.ret)
