from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import FileResponse
import pymysql, os, time
from datetime import datetime
from django import forms
import time
from django.http import HttpResponse,JsonResponse
from customer_management.settings import conf_fun
from databases import conn_sql



'''获取所有的产品信息'''
def all_product_information():
    sql = "SELECT * FROM product_message"
    data = conn_sql.connect_mysql(sql,type='dict')
    return data



'''获取前端下拉框的数据'''
def parameter():


    channel_sql =  "SELECT platform FROM parameter WHERE platform !=''"  # 平台
    product_type_sql =   "SELECT product_type FROM parameter WHERE product_type !=''" # 产品类别
    product_state_sql =   "SELECT state FROM parameter WHERE state !=''" # 店铺(获取产品)状态sql


    channel_data = conn_sql.connect_mysql(channel_sql, type='dict') # 渠道 = 平台
    product_type_data = conn_sql.connect_mysql(product_type_sql, type='dict') # 产品类别
    product_state_data = conn_sql.connect_mysql(product_state_sql, type='dict') # 店铺状态
    channel_data,product_type_data ,product_state_data = type_change(channel_data, product_type_data, product_state_data)

    return channel_data, product_type_data, product_state_data


def type_change(channel_data , product_type_data ,product_state_data ):
    cc,ss,ch,ty,st = [], [],[],[],[]

    for channel_dict in channel_data:
        q= {}
        q['value'] = channel_dict.get('channel')
        q['label'] = channel_dict.get('channel')
        ch.append(q)

    for  type_dict in product_type_data:
        q={}
        q['value'] = type_dict.get('product_type')
        q['label'] = type_dict.get('product_type')
        ty.append(q)

    for store_state_dict in product_state_data:
        q= {}
        q['value'] = store_state_dict.get('state')
        q['label'] = store_state_dict.get('state')
        st.append(q)

    return ch,ty,st

'''新增产品信息'''
def add_product_data(data):
    key_list =[]
    value_list = []
    for key,value in data.items():
        key_list.append(key)
        value_list.append("'%s'"%value)
    print(key_list,value_list)
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)
    sql = "INSERT INTO product_message ( %s ) VALUES (%s)"%(key_str, value_str)
    res = conn_sql.connect_mysql(sql,type='dict')
    return res

def fuzzy_matching(condition,field_list):
    field_str = " "
    for i in field_list:
        field_str += " IFNULL(%s, '') ,"%(i)
    field_str = field_str.rstrip(' ,')
    where_str = " AND CONCAT( {0} ) LIKE CONCAT('%', '{1}', '%')".format(field_str,condition)
    return where_str


''' 修改产品信息'''
def update_store_data(data):

    update_list =[]
    for key,value in data.items():
        if key != 'id':
            update_list.append("%s = '%s'"%(key, value))

    update_str = ','.join(update_list)
    print(update_str)
    sql = "UPDATE product_message SET %s WHERE id=%s"%(update_str, int(data.get('id')))
    conn_sql.connect_mysql(sql)

'''搜索功能产品信息'''
def search_product(data):
    sql = "SELECT * FROM product_message WHERE id >0 {0} limit {1},50"
    count_sql  = "SELECT count(id) as count_id FROM product_message WHERE id >0 {0} "
    page = int(data.get('page')) if data.get('page') else 1
    page = (page-1)*50
    ser_str = ''
    product_code= data.get('product_code')


    if product_code:
        sql  = "SELECT * FROM product_message WHERE  product_code = '%s'"%(product_code)
    else:
        field_list = ['product_code' , 'product_name' , 'product_type',
                      'product_state' ,'product_package_size',
                      'product_size','product_weight', ]
        condition = data.get('condition')
        if condition and field_list:
            where_str = fuzzy_matching(condition, field_list)
        else:
            where_str = ''
        ser_str = where_str


    sql = sql.format(ser_str, page)
    count_sql = count_sql.format(ser_str)

    print('这是全部的sql',sql)
    re_data = conn_sql.connect_mysql(sql, type='dict')
    print(count_sql)
    count_data = conn_sql.connect_mysql(count_sql, type='dict')
    return re_data,count_data

# 产品信息
class Product_Information(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': ""}

    def list(self, request):
        ser_data = request.GET
        re_data, count_data = search_product(ser_data)
        channel_data, product_type_data, product_state_data= parameter()
        self.ret['data'] = re_data
        self.ret['count_data'] = count_data
        self.ret['channel_data'] = channel_data
        self.ret['product_type_data'] = product_type_data
        self.ret['product_state_data'] = product_state_data
        self.ret['msg'] = '成功'
        return Response(self.ret)

    def create(self,request):
        data = request.data
        product_code = data.get('product_code')
        judge_sql = " SELECT * FROM product_message WHERE product_code ='%s'" % (product_code)
        judge_data = conn_sql.connect_mysql(judge_sql)
        if judge_data:
            self.ret['code'] = 500
            self.ret['msg'] = '%s该产品编号已存在' % (product_code)
        else:
            add_product_data(data)
        print(self.ret)
        return Response(self.ret)

    def alter(self,request):
        data = request.data
        update_store_data(data)
        return Response(self.ret)

    def delete(self, request):
        data = request.GET
        id_list = data.getlist('id[]')
        for id in id_list:
            sql = "DELETE FROM product_message WHERE  id= %s"%(int(id))
            conn_sql.connect_mysql(sql)

        return Response(self.ret)


# 产品详情
# from databases import sql

product_sql ="SELECT c.product_code,c.product_name,c.category, c.countries,c.the_store,c.sku ,fba,times, nums FROM commodity_codes_zr as c,sku_report as s " \
             " WHERE c.sku =s.sku  AND c.product_code ='{0}' " \
             " AND DATE(times)  = CURDATE() -1" \
             " ORDER BY times DESC"



moth_sql = " SELECT s.product_code,s.countries, s.the_store, s.sku ,AVG(s.ssm) as avg_sku ,SUM(s.ssm) as sum_sku" \
           " from ( SELECT c.product_code,c.countries , c.the_store, c.sku ,SUM(nums) as ssm,DATE_FORMAT(times,'%Y-%m') as date " \
           " FROM commodity_codes_zr as c,sku_report as s WHERE   c.sku =s.sku  " \
           " AND c.product_code ='{0}'" \
           " GROUP BY c.product_code,c.countries, c.the_store ,c.sku,DATE_FORMAT(times,'%Y-%m')" \
           " ORDER BY DATE_FORMAT(times,'%Y-%m') DESC ) as  s" \
           " GROUP BY s.product_code ,s.countries, s.the_store , s.sku" \
           " ORDER BY s.product_code ,s.countries, s.the_store , s.sku"

day_sql =" SELECT s.product_code,s.countries, s.the_store, s.product_name,s.sku ,AVG(s.ssm) as avg_day_sku, SUM(s.ssm) as sum_sku" \
         " from (SELECT c.product_code,c.countries , c.product_name,c.the_store, c.sku ,SUM(nums) as ssm,DATE_FORMAT(times, '%Y-%m-%d') as date " \
         " FROM commodity_codes_zr as c,sku_report as s  " \
          " WHERE c.sku =s.sku  AND c.product_code ='{0}' " \
         " GROUP BY c.product_code,c.countries, c.the_store ,c.product_name, c.sku,DATE_FORMAT(times,'%Y-%m-%d')" \
         " ORDER BY DATE_FORMAT(times,'%Y-%m-%d') DESC ) as  s" \
         " GROUP BY s.product_code ,s.countries, s.the_store , s.sku,s.product_name " \
         " ORDER BY s.product_code ,s.countries, s.the_store , s.sku"

# 零件
access_sql = "SELECT accessories_list  from product_zr WHERE product_number ='{0}'"

''' 零件查询'''
def part_sql(product_code ):
    sql ="SELECT *  from products_components WHERE product_code ='{0}'".format(product_code)

    data = conf_fun.connect_mysql(sql, type='dict')
    print(data)
    data_list =[]
    # if data:
    #     for  part_dict in data:
    #
    #         part = part_dict.get('accessories_list')
    #
    #         part_list = part.split('\n')
    #         print(12312,part_list)
    #         for i in part_list:
    #             data_list.append(i.split('.'))

    return data

# 产品信息详情
def detail_product(request):
    data  = request.GET
    ret = {'code': 200, 'msg': '无'}
    product_code = data.get('product_code')
    print(data, product_code)
    day_sql_1 = day_sql.format(product_code)
    moth_sql_1 = moth_sql.format(product_code)
    product_sql_1 = product_sql.format(product_code)

    day_data = conf_fun.connect_mysql_re(day_sql_1, type='dict')
    moth_data = conf_fun.connect_mysql_re(moth_sql_1, type='dict')
    product_data = conf_fun.connect_mysql_re(product_sql_1, type='dict')
    access_data = part_sql(product_code)

    re_list =[]
    for  day_dict in day_data:
        for month_dict in moth_data:
            # print(day_dict, month_dict)
            if day_dict.get('sku') == month_dict.get('sku'):
                day_dict['avg_sku'] = month_dict.get('avg_sku')
        re_list.append(day_dict)

    ret['product_data'] = product_data
    ret['date_data'] = re_list
    ret['access_data'] = access_data
    return  JsonResponse(ret)
