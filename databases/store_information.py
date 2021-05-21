from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import FileResponse
import pymysql, os, time
from datetime import datetime
from django import forms
import time
from django.http import HttpResponse,JsonResponse
from urllib.parse import unquote
from settings import conf_fun



def fuzzy_matching(condition,field_list):
    field_str = " "
    for i in field_list:
        field_str += " IFNULL(%s, '') ,"%(i)
    field_str = field_str.rstrip(' ,')
    where_str = " AND CONCAT( {0} ) LIKE CONCAT('%', '{1}', '%')".format(field_str,condition)
    return where_str

'''获取所有的店铺信息'''
def getting_store_data(data_1,page, area):
    field_list = ['name_shop' , 'site' , 'country', 'platform',
                  'state', 'email', 'company', 'address', 'host_ip', 'next_ip', 'type', 'registration_date', 'cancellation_date']
    condition = data_1.get('condition')
    print(data_1)
    if condition and field_list:
        where_str = fuzzy_matching(condition,field_list)
        print(where_str)
    else:
        where_str =''
    if area == 'all':
        sql = "SELECT * FROM store_information where id >=0 {1} limit {0},50".format((page-1)*50 , where_str)
        count_sql = "SELECT count(id) as count_id FROM store_information where id>0 {0}".format(where_str)
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        count_data = conf_fun.connect_mysql_operation(count_sql,type='dict')
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
        count_data = []
        for i in range(len(area_site)):

            sql = "SELECT * FROM store_information where site='{1}' " \
                  "and country='{2}' {3} limit {0},50".format((page-1)*50, area_site[i], area_country[i], where_str)
            count_sql = "SELECT count(id) as count_id FROM store_information " \
                        " where site='{0}' and country='{1}' {2} ".format(area_site[i], area_country[i], where_str)

            data_res = conf_fun.connect_mysql_operation(sql,type='dict')
            count_data_res = conf_fun.connect_mysql_operation(count_sql,type='dict')
            for j in data_res:
                data.append(j)
            for j in count_data_res:
                count_data.append(j)

    return data,count_data

'''参数新增国家/站点/渠道 '''
def  add_parmeter(data):
    # 新增国家和站点平台
    platform_sql = "insert ignore into parameter ( platform ) VALUES  ('%s')"%(data.get('platform'))
    country_sql = "insert ignore into parameter ( country ) VALUES  ('%s')"%(data.get('country'))
    state_sql = "insert ignore into parameter ( site ) VALUES  ('%s')"%(data.get('site'))
    conf_fun.connect_mysql_operation(platform_sql, type='dict')
    conf_fun.connect_mysql_operation(country_sql ,type='dict')
    conf_fun.connect_mysql_operation(state_sql , type='dict')


'''新增店铺的信息'''
def add_store_data(data):
    key_list =[]
    value_list = []
    for key,value in data.items():
        key_list.append(key)
        value_list.append("'%s'"%value)
    print(key_list,value_list)
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)
    sql = "INSERT INTO store_information ( %s ) VALUES (%s)"%(key_str, value_str)

    add_parmeter(data)
    print('新增店铺语句' ,sql ,'\n')
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    return res

''' 修改店铺信息'''
def update_store_data(data):

    update_list =[]
    for key,value in data.items():
        if key != 'id':
            update_list.append("%s = '%s'"%(key, value))
    # print(update_list)
    update_str = ','.join(update_list)
    print(update_str)
    sql = "UPDATE store_information SET %s WHERE id=%s"%(update_str, int(data.get('id')))
    conf_fun.connect_mysql_operation(sql)

'''获取前端下拉框的数据'''
def parameter():
    # 参数表
    country_sql = "SELECT country FROM parameter WHERE country !=''"
    site_sql = "SELECT site FROM parameter WHERE site !=''"
    channel_sql =  "SELECT platform FROM parameter WHERE platform !=''"
    type_sql =   "SELECT type FROM parameter WHERE type !=''"
    store_state_sql =   "SELECT state FROM parameter WHERE state !=''" # 店铺状态sql

    country_data = conf_fun.connect_mysql_operation(country_sql, type='dict')  # 国家
    site_date = conf_fun.connect_mysql_operation(site_sql, type='dict') # 站点
    channel_data = conf_fun.connect_mysql_operation(channel_sql, type='dict') # 渠道 = 平台
    type_data = conf_fun.connect_mysql_operation(type_sql, type='dict') # 店铺类别
    store_state_data = conf_fun.connect_mysql_operation(store_state_sql, type='dict') # 店铺状态
    country_data,site_date,channel_data,type_data,store_state_data = type_change(country_data, site_date, channel_data, type_data, store_state_data)

    return country_data,site_date,channel_data,type_data,store_state_data

def type_change(country_data, site_data,channel_data, type_data,store_state_data):
    cc,ss,ch,ty,st = [], [],[],[],[]
    for country_dict in country_data: # 国家
        z ={}
        z['value'] = country_dict.get('country')
        z['label'] = country_dict.get('country')
        cc.append(z)

    for site_dict in site_data:  # 站点
        q = {}
        print(site_dict)
        q['value'] = site_dict.get('site')
        q['label'] = site_dict.get('site')
        ss.append(q)

    for channel_dict in channel_data:
        q= {}
        q['value'] = channel_dict.get('platform')
        q['label'] = channel_dict.get('platform')
        ch.append(q)

    for  type_dict in type_data:
        q={}
        q['value'] = type_dict.get('type')
        q['label'] = type_dict.get('type')
        ty.append(q)

    for store_state_dict in store_state_data:
        q= {}
        q['value'] = store_state_dict.get('state')
        q['label'] = store_state_dict.get('state')
        st.append(q)

    return cc,ss,ch,ty,st


class Store_Information(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': ""}

    def list(self, request):
        page =  request.GET.get('page')
        page=  int(page) if page else 1
        print('111', request.META.get('HTTP_AUTHORIZATION'))
        area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
        print(area)
        data_1 = request.GET
        data,count_data= getting_store_data(data_1, page, area)
        country_data,site_date,channel_data,type_data,store_state_data = parameter()

        self.ret['data'] = data
        self.ret['country_data'] = country_data
        self.ret['site_date'] = site_date
        self.ret['channel_data'] = channel_data
        self.ret['type_data'] = type_data
        self.ret['store_state_data'] = store_state_data
        self.ret['count_data'] = count_data
        self.ret['msg'] = '成功'
        return Response(self.ret)

    def create(self,request):
        data = request.data
        res =   add_store_data(data)
        print(self.ret)

        return Response(self.ret)

    def alter(self,request):
        data = request.data
        update_store_data(data)
        return Response(self.ret)

