import calendar
from datetime import date, timedelta
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
import time
from order_management.settings import order_sql
from settings import conf_fun
from operator import itemgetter
from itertools import groupby


class Container_transit(ViewSetMixin,APIView):

    def __init__(self):
        self.ret ={'code':200}

    def list(self , request):
        data = request.GET
        ser_data = ''
        title_list =['产品编码', 'sku', '库存总计', 'FBA', 'FBM']
        for k,v in data.items():
            if k in ['country','site','product_type','product_num'] and v:
                ser_data += " AND ci.%s = '%s'"%(k,v)

        transit_container_sql = order_sql.transit_sql.format(ser_data)
        transit_container_data = conf_fun.connect_mysql_product_supplier(transit_container_sql,type='dict')
        print(transit_container_data)
        case_when_ser =''' '''
        for i in transit_container_data:
            case_when_ser +=''' IFNULL(SUM(CASE   WHEN  container_code ='{0}' THEN ci.distribution_num END ),0)AS '{0}' ,'''.format(i.get('container'))
            title_list.append(i.get('container'))
        transit_product_sql = order_sql.transit_product_sql.format(ser_data,case_when_ser,'')
        print(transit_product_sql)
        transit_sku_sql = order_sql.transit_product_sql.format(ser_data,case_when_ser,'sku,')
        transit_product_data = conf_fun.connect_mysql_product_supplier(transit_product_sql, type='dict')
        transit_sku_data = conf_fun.connect_mysql_product_supplier(transit_sku_sql, type='dict')
        transit_sku_dict ={}
        for product_num,items in groupby(transit_sku_data, key=itemgetter('product_number')):
            if product_num not  in transit_sku_dict:
                transit_sku_dict[product_num] =[]
            for i in items:
                transit_sku_dict[product_num].append(i)
        self.ret['transit_product_data'] = transit_product_data
        self.ret['transit_sku_data'] =transit_sku_dict
        self.ret['title_list'] =title_list
        return Response(self.ret)