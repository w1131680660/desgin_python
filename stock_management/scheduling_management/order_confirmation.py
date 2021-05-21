from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from datetime import datetime
from stock_management.scheduling_management import scheduling_sql, scheduling_func
# from stock_management import scheduling_settings

import json
import datetime
from datetime import timedelta

from settings import conf_fun



def fuzzy_matching(condition,field_list):
    field_str = " "
    for i in field_list:
        field_str += " IFNULL(%s, '') ,"%(i)
    field_str = field_str.rstrip(' ,')
    where_str = " AND CONCAT( {0} ) LIKE CONCAT('%', '{1}', '%')".format(field_str,condition)
    return where_str

def order_search(data):


    page = int(data.get('page')) if data.get('page') else 1
    page = (page-1) *50
    ser_str =''
    field_list = ['f.schedule_date' , 'f.container_num', 'f.country',
                  'f.warehouse_type','f.warehouse_name', 'f.platform' , 'f.site', 'f.sku', 'f.product_code', 'f.sku_num',
                  'f.product_name','f.product_type']
    condition = data.get('condition')
    print(data)
    where_str =''
    if len(data.keys()) <=1:
        order_sql =  scheduling_sql.order_confirmation_sql.format('',page)
        count_sql = scheduling_sql.count_order_sql.format('',page)
    else:
        if condition and field_list:
            where_str = fuzzy_matching(condition, field_list)
            print(where_str)
        order_sql = scheduling_sql.order_confirmation_sql.format(where_str, page)
        count_sql = scheduling_sql.count_order_sql.format(where_str, page)
    print('\n\n\n',order_sql)
    order_data = conf_fun.connect_mysql_operation(order_sql, type='dict')
    print('\n',count_sql)
    count_data= conf_fun.connect_mysql_operation(count_sql, type='dict')

    return order_data, count_data

def down_box():
    # 国家下拉框
    country_data = scheduling_func.conn_sql_select(scheduling_sql.country_sql)
    # 类别
    product_type_data = scheduling_func.conn_sql_select(scheduling_sql.product_type_sql)
     # 站点
    channel_data = scheduling_func.conn_sql_select(scheduling_sql.channel_sql)
     # 平台
    site_data = scheduling_func.conn_sql_select(scheduling_sql.site_sql)
    re_list = change_type( country_data, product_type_data,  channel_data ,  site_data )
    return re_list

# 将数据转换为element_ui
def change_type( country_data, product_type_data,  channel_data ,  site_data ):
    country_data_list, product_type_data_list ,channel_list ,site_list = [], [] ,[] ,[]
    re_list = [country_data_list, product_type_data_list ,channel_list ,site_list]
    an_list =  [ country_data, product_type_data ,channel_data ,  site_data ,]
    for_list =['country', 'product_type' ,'platform', 'site',]


    for index, object_list in enumerate(an_list):
        for channel_dict in object_list:
            q = {}

            q['value'] = channel_dict.get(for_list[index])
            q['label'] = channel_dict.get(for_list[index])
            re_list[index].append(q)

    return re_list

def add_order(data_1):

    data_list = json.loads(data_1.get('params'))
    print('\n\n\n\n', type(data_list),data_list)
    i = 0
    now_date = datetime.datetime.strftime(datetime.datetime.now() + timedelta(hours=8), "%Y-%m-%d %H:%M:%S")
    for data in data_list:
        key_str = ''
        value_str = ''
        print(data,type(data))
        for key in data.keys():

            value_list = data.get(key)
            if key =='dates':
                key_str += " %s, " % (key)
                value_str += " '%s' ," % ('/'.join(value_list.split('-')))
            else:
                if key not in ['id']:
                    key_str += " %s, "%(key)
                    value_str += " '%s' ,"%(value_list)
                elif key =='id':

                    where_str = " AND {0} = '{1}'".format(key, value_list)
                    update_str = " integrated_state ='已集成'"
                    scheduling_func.update_conn_sql('order_integration', update_str, where_str)
        key_str = key_str.rstrip(', ')
        value_str = value_str.rstrip(', ')
        key_str_1 , key_str_2 = key_str ,key_str
        value_str_1 ,value_str_2  = value_str , value_str
        key_str_1 += ' ,crete_time'
        value_str_1 += ", '%s'"%(now_date)
        key_str_2 += ' ,surplus_distribution_order'
        value_str_2 += " , '%s'"%(data.get('plan_order'))
        scheduling_func.conn_sql_demo('order_integration_record' ,key_str_1,value_str_1)
        scheduling_func.conn_supply_demo('order_integrate', key_str_2, value_str_2)
        i +=1

    return 123


'''' 订单集成   '''

class Order_Confirmation(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code' :200 ,'msg': '无'}


    def list(self,request):
        data = request.GET
        order_data, count_data = order_search(data)
        re_list = down_box()
        self.ret['data'] = order_data
        self.ret['count_data'] = count_data
        self.ret['re_list'] = re_list
        return Response(self.ret)

    def create(self,request):
        data = request.data
        print('\n\n11111111111111111111',data)
        add_order(data)
        return Response(self.ret)

    def delete(self , request):
        pass

    def alter(self, request):
        pass