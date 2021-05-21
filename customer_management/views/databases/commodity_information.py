from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import FileResponse
import pymysql, os, time
from datetime import datetime
from django import forms
import time
from django.http import HttpResponse,JsonResponse
from operator import itemgetter
from itertools import groupby
from databases import conn_sql

from urllib.parse import unquote


'''返回左侧的国家/站点'''
def left_show(area):
    if 'all' in area:
        sql = "SELECT platform,country,site FROM store_information group by platform,country,site ORDER BY platform,country"
        data = conn_sql.connect_mysql(sql, type='dict')
    else:
        try:
            area_res = area.split(',')

            area_site = []
            area_country = []
            for i in area_res:
                area_site.append(i.split('_')[0])
                area_country.append(i.split('_')[1])
            area_site = tuple(area_site)
            area_country = tuple(area_country)
        except:
            area_site = tuple(area.split('_')[0])
            area_country = tuple(area.split('_')[1])

        data = []
        for i in range(len(area_site)):
            sql = "SELECT platform,country,site FROM store_information where site='{0}' and country='{1}' group by platform,country,site ORDER BY platform,country"
            sql = sql.format(area_site[i], area_country[i])

            data_res = conn_sql.connect_mysql(sql, type='dict')
            for j in data_res:
                data.append(j)
            # print('\n\n这里是',data)
    data_dict ={}
    for platform,items in groupby(data, key=itemgetter('platform')):
        data_dict[platform] ={}

        for country, items_1 in groupby(items,key=itemgetter('country')):

            data_dict[platform][country] =[]
            for i in items_1:

                data_dict[platform][country].append(i.get('site'))

    print(data_dict)
    return data_dict

def fuzzy_matching(condition,field_list):
    field_str = " "
    for i in field_list:
        field_str += " IFNULL(c.%s, '') ,"%(i)
    field_str = field_str.rstrip(' ,')
    where_str = " AND CONCAT( {0} ) LIKE CONCAT('%', '{1}', '%')".format(field_str,condition)
    return where_str

'''搜索功能包括 左侧的搜索'''
def serach_commodity(data, area):
    field_list = ['product_code', 'spu', 'sku', 'country', 'site', 'platform',
                  'commodity_state', 'commodity_price','asin','fnsku','upc',
                  'begin_sell_date', 'over_sell_date','select_link', 'sku_link'
                  ,'product_link', 'commodity_name', 'category', 'discount_information']
    condition= data.get('condition')
    if condition and field_list:
        where_str = fuzzy_matching(condition,field_list)
    else:
        where_str =''
    if 'all' in area:
        sql = "SELECT c.id,c.product_code, c.spu, c.sku , c.country , c.site , c.platform," \
              "c.commodity_state, c.commodity_price, c.asin , c.fnsku, c.upc ," \
              " c.begin_sell_date,c.over_sell_date, c.select_link," \
              "c.sku_link,c.product_link," \
              "s.product_name,s.product_type from commodity_information as c, product_message as s " \
              " WHERE c.product_code = s.product_code  {0} {2} limit {1},50"
        count_sql =  "SELECT COUNT(c.id) as count_id from commodity_information as c, product_message as s " \
              " WHERE c.product_code = s.product_code {0} {2} limit {1},50"
    else:
        try:
            area_res = area.split(',')
            for i in area_res:
               if i.split('_')[1] == '英国':
                   i.replace('英国', '欧洲')
               elif i.split('_')[1] == '法国':
                   i.replace('法国', '欧洲')
               elif i.split('_')[1] == '德国':
                   i.replace('德国', '欧洲')
               elif i.split('_')[1] == '意大利':
                   i.replace('意大利', '欧洲')
               elif i.split('_')[1] == '西班牙':
                   i.replace('西班牙', '欧洲')
               else:
                   pass
            area_res = list(set(area_res))
            area_site = []
            area_country = []
            for i in area_res:
                area_site.append(i.split('_')[0])
                area_country.append(i.split('_')[1])
            area_site = tuple(area_site)
            area_country = tuple(area_country)
        except:
            area_site = tuple(area.split('_')[0])
            area_country = tuple(area.split('_')[1])
        sql = "SELECT c.id,c.product_code, c.spu, c.sku , c.country , c.site , c.platform," \
              "c.commodity_state, c.commodity_price, c.asin , c.fnsku, c.upc ," \
              " c.begin_sell_date,c.over_sell_date, c.select_link," \
              "c.sku_link,c.product_link," \
              "s.product_name,s.product_type from commodity_information as c, product_message as s " \
              " WHERE  c.product_code = s.product_code {0} {2} limit {1},50"
        count_sql = "SELECT COUNT(c.id) as count_id from commodity_information as c, product_message as s " \
              " WHERE  c.product_code = s.product_code {0} {2} limit {1},50"

    page = int(data.get('page')) if data.get('page') else 1
    page = (page-1) *50
    search_str = ""
    for key,value in data.items():
        if key not in ['id', 'page','condition' ,'field' ] and value:
            search_str += (" AND c.%s = '%s'" % (key, value))

    if 'all' in area:
        sql = sql.format(search_str, page,where_str)
        count_sql = count_sql.format(search_str, page,where_str)
        print('all\n', sql)
        data = conn_sql.connect_mysql(sql, type='dict')
        count_data = conn_sql.connect_mysql(count_sql, type='dict')
    else:
        data = []
        count_data = []
        print('\n',area_site)
        for i in range(len(area_site)):
            sql = sql.format(search_str, page, where_str)
            print('欧洲的？\n\n',sql)
            count_sql = count_sql.format(search_str, page,where_str)
            data_res = conn_sql.connect_mysql(sql, type='dict')

            count_data_res = conn_sql.connect_mysql(count_sql, type='dict')
            for j in data_res:
                if j not in data:
                    data.append(j)
            for j in count_data_res:
                if j not in count_data:
                    count_data.append(j)
        # list(set(count_data))
    return data, count_data

'''新增商品信息'''
def add_commodity_data(data):
    key_list =[]
    value_list = []
    for key,value in data.items():
        key_list.append(key)
        value_list.append("'%s'"%value)
    print(key_list,value_list)
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)
    sql = "INSERT INTO commodity_information ( %s ) VALUES (%s)"%(key_str, value_str)
    res = conn_sql.connect_mysql(sql,type='dict')
    return res

''' 修改商品信息'''
def update_store_data(data):

    update_list =[]
    for key,value in data.items():
        if key != 'id':
            update_list.append("%s = '%s'"%(key, value))
    # print(update_list)
    update_str = ','.join(update_list)
    print(update_str)
    sql = "UPDATE commodity_information  SET %s WHERE id=%s"%(update_str, int(data.get('id')))
    conn_sql.connect_mysql(sql)

'''返回所有的产品编号'''
def product_code_re():
    sql = "SELECT product_code FROM product_message"
    product_state_sql = "SELECT state FROM parameter WHERE state !=''"  # 店铺(获取产品)状态sql
    data = conn_sql.connect_mysql(sql, type='dict')
    data_2 = conn_sql.connect_mysql(product_state_sql, type='dict')
    return data,data_2




class Commodity_Information(ViewSetMixin, APIView):

    def __init__(self):
        self.ret =  {'code':200,'msg':'ok'}


    def list(self,request):
        ser_data = request.GET
        print(123123131231, ser_data,123123)
        area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
        if ser_data:
            data,count_data = serach_commodity(ser_data, area)
            self.ret['count_data'] = count_data
            self.ret['data'] = data
        left_data_dict = left_show(area)
        product_code_data,commodity_data = product_code_re()

        self.ret['left_data_dict']  = left_data_dict
        self.ret['product_code_data'] = product_code_data
        self.ret['commodity_data']  = commodity_data
        return Response(self.ret)

    def create(self,request):
        data = request.data
        print(data)
        add_commodity_data(data)
        return Response(self.ret)

    def alter(self,request):
        data = request.data
        update_store_data(data)
        return Response(self.ret)

    def delete(self,request):
        data = request.GET
        print(data)
        id_list = data.getlist('id[]')
        for id in id_list:
            sql = "DELETE FROM commodity_information WHERE  id= %s" % (int(id))
            print(sql)
            conn_sql.connect_mysql(sql)

        return Response(self.ret)
