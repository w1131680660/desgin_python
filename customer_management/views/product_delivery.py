from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import JsonResponse
from customer_management.settings import conf_fun as conf_fun_1, sql
from settings import conf_fun




def parameter():
    shop_data = conf_fun.connect_mysql_operation(sql.shop_email, type='dict')
    new_product_data = conf_fun.connect_mysql_operation(sql.new_product, type='dict')
    country_data = conf_fun.connect_mysql_operation(sql.country_sql, type='dict')
    customer_data = conf_fun.connect_mysql_operation(sql.customer_sql, type='dict')
    old_product_data = conf_fun.connect_mysql_operation(sql.old_product, type='dict')
    return shop_data, new_product_data,country_data, customer_data, old_product_data

class Product_delivery(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg':'无'}


    def list(self, request):
        shop_data, new_product_data, country_data, customer_data, old_product_data = parameter()

        self.ret['shop_data'] = shop_data
        self.ret['new_product_data'] = new_product_data
        self.ret['country_data'] = country_data
        self.ret['customer_data'] = customer_data
        self.ret['old_product_data'] = old_product_data
        return Response(self.ret)


    def create(self, request):
        data = request.data.get('params')
        print(data)
        return Response(self.ret)