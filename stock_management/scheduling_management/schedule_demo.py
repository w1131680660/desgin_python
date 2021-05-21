from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from datetime import datetime
from stock_management.scheduling_management import scheduling_sql, scheduling_func
# from stock_management import scheduling_settings
from operator import itemgetter
from itertools import  groupby
from django.http import JsonResponse
import uuid
import pandas as pd
from settings import conf_fun
from urllib.parse import unquote

week_dict ={
    0:  '周一',
    1:  '周二',
    2:  '周三',
    3:  '周四',
    4:  '周五',
    5:  '周六',
    6:  '周日',}

# 获取排期日历的的数据库数据
def schedule_all(data):
    ser_str = ''

    schedule_sql = scheduling_sql.schedu_sql.format(ser_str)
    re_data = conf_fun.connect_mysql_operation(schedule_sql, type='dict')
    return re_data

# 获取下拉框数据
def down_box():
    # 仓库类型和产量名称
    warehouse_data = scheduling_func.conn_sql_logistics(scheduling_sql.warehouse_sql)
    warehouse_dict = {}
    for warehouse , items in  groupby(warehouse_data, key= itemgetter('warehouse_type')):
        if warehouse not in warehouse_dict.keys():
            warehouse_dict[warehouse] = []
        for i in items:
            warehouse_dict[warehouse].append( i.get('warehouse_name'))

    # 国家下拉框
    country_data = scheduling_func.conn_sql_select(scheduling_sql.country_sql)
    # 柜子类型
    container_type_data = scheduling_func.conn_sql_select(scheduling_sql.container_type_sql)
    # 站点
    channel_data = scheduling_func.conn_sql_select(scheduling_sql.channel_sql)
    # 平台
    site_data = scheduling_func.conn_sql_select(scheduling_sql.site_sql)
    # 工厂
    factory_data = scheduling_func.conn_sql_select(scheduling_sql.factory_sql)

    re_list =scheduling_func.change_type(country_data,container_type_data ,  channel_data ,  site_data,factory_data  )
    return warehouse_dict ,re_list


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def place_order(request):
    # name = '中睿德国-2154-日成-0112-D575-40HQ-下单表.xlsm'
    # path =  os.path.join(os.getcwd(),'place_order/',name)

    file = request.FILES.get('file')
    print(file,request.FILES)


    re_list = []
    error_list = []
    ret = {}
    try:
        data_pd = pd.read_excel(file, skiprows=3, keep_default_na=False)
        for index, data in data_pd.iterrows():
            data_dict = {}

            # print(data['sku'],data['货名'],data['规格说明'], data['下单数量'])
            # sql = " SELECT product_code,commodity_name FROM commodity_information  where sku ='%s'" % (data['sku'])
            if data['sku'] and data['数量']:
                sql = "select ci.product_code, product_name,product_package_size from commodity_information ci join " \
                      "     product_message pm on ci.product_code=pm.product_code where sku='%s' ;" % (data['sku'])
                print(sql)
                re_data = conf_fun.connect_mysql_operation(sql, type='dict')
                # print(re_list)
                print(123123, re_data)
                re_name = re_data[0].get('product_code') if re_data else ''
                commodity_name = re_data[0].get('product_name') if re_data else ''

                if data['sku'] == '总计':
                    print('这里是11111111111111111', print(data['数量']))
                    pass
                else:
                    print(data['数量'], commodity_name, re_name)

                    if not commodity_name:
                        data_dict['sku'] = data['sku']
                        data_dict['num'] = data['数量']
                        error_list.append(data_dict)
                    else:
                        data_dict['sku'] = data['sku']
                        data_dict['commodity_name'] = commodity_name
                        data_dict['num'] = data['数量']
                        data_dict['product_code'] = re_name
                        re_list.append(data_dict)

            if error_list:
                ret['error_data'] = error_list
                ret['code'] = 500
                ret['error_msg'] = '商品信息和产品信息页面没有对应下的sku的产品编码和产品名字，请新增后在上传'
            else:
                ret['data'] = re_list
                ret['code'] = 200
    except :
        ret ={'code':500,'error_msg':'文件内容和格式错误请参考下单表模板来填写对应的sku和下单数据'}
    return JsonResponse(ret)


# 运营排期日历


class Schedule_Calendar(ViewSetMixin, APIView) :

    def __init__(self):
        self.ret = {'code':200 ,'msg': '无'}


    def list(self,request):
        data = request.GET
        data_dict = {}
        counter_data_dict = schedule_all(data)
        for data in counter_data_dict:
            date = str(data.get('schedule_date'))
            week = week_dict.get(datetime.strptime(date, "%Y-%m-%d").weekday())
            if date not in data_dict:
                data_dict[date] = [week, data]
            else:
                data_dict[date].append(data)
        print(data_dict)
        import collections

        data_dict = collections.OrderedDict(sorted(data_dict.items()))
        warehouse_data, re_list = down_box()

        self.ret['re_data'] = data_dict
        self.ret['warehouse_data'] = warehouse_data
        self.ret['re_list'] = re_list


        return Response(self.ret)

    # 新增货柜
    def create(self, request):
        data = request.data
        print(data)
        unique_id = uuid.uuid4()
        judge_sql = " select * from schedule_container where container_num ='%s'" % (data.get('container_num'))
        judge_data = scheduling_func.conn_sql_select(judge_sql, )
        if judge_data:
            ret = {'code': 500, 'msg': '该货柜已存在，请勿重复新增'}
            return Response(ret)
        else:
            scheduling_func.add_template_data(data, 'schedule_container', unique_id ) #新增货柜
            scheduling_func.add_operating_data(data, 'operating_data',unique_id) # 新增待运营上传的资料
            scheduling_func.add_order_confirmation(data, 'order_integration',unique_id)  # 新增订单集成的数据
            print(1)
            return Response(self.ret)

    def delete(self, request):
        data = request.GET
        container_code = data.get('container_code')
        user_name = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[0]
        if user_name not in ['何鹏']:
            self.ret['code'] = 500
            self.ret['error_msg'] = '货柜只有总监才能删除'
            return Response(self.ret)
        # 运营
        sc_sql = "DELETE  FROM schedule_container WHERE container_num ='{0}' ".format(container_code)
        ord_integration_sql = " DELETE  FROM order_integration WHERE container_num ='{0}' ".format(container_code)
        oper_sql = " DELETE  FROM  operating_data WHERE  container_num ='{0}'".format(container_code)
        list_1 = [sc_sql,ord_integration_sql,oper_sql]
        # 供应链
        ord_dis_sql = "DELETE  FROM order_distribution WHERE container_code ='{0}' ".format(container_code)
        order_integrate_sql_1 = "DELETE  FROM order_integrate  WHERE container_code ='{0}' ".format(container_code)
        list_2 =[ord_dis_sql, order_integrate_sql_1]
        try:
            for i in list_1:
                conf_fun.connect_mysql_operation(i,type='dict')
            for i in list_2:
                conf_fun.connect_mysql_supply(i,type='dict')
        except : pass
        return Response(self.ret)