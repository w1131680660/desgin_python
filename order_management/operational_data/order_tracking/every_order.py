import calendar
from datetime import date, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
import time
from order_management.settings import order_sql
from settings import conf_fun


def change_site_country(site, country):
    if country in ['德国', '法国', '意大利', '西班牙', '英国']:
        country = '欧洲'
    site_sql = " SELECT * FROM area_contrast WHERE area ='{0}' ".format(site)
    site_data = conf_fun.connect_mysql_operation(site_sql, type='dict')

    country_sql = " SELECT * FROM country_contrast WHERE country ='{0}'".format(country)
    country_data = conf_fun.connect_mysql_operation(country_sql, type='dict')
    try:
        site_cn = site_data[0].get('area_cn') if site_data else ''
        country_cn = country_data[0].get('country_cn') if country_data else ''
    except:
        site_cn = ''
        country_cn = ''
    return site_cn, country_cn


def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return start_date, end_date


def get_date_list(fba_date, type):
    '''
    获取最近一个的月的日期列表
    :return:
    '''
    a_day = timedelta(days=1)
    if type == 1:
        day_month = (date.today() + timedelta(days=-22))
        fba_date_list = fba_date.split('-')
        y, m, d = fba_date_list[0], fba_date_list[1], fba_date_list[2]
        last_day = date(int(y), int(m), int(d))
        first_day, end_date = get_month_range(day_month)
    else:
        fba_date_list = fba_date.split('-')
        y, m = fba_date_list[0], fba_date_list[1],
        day_month = date(int(y), int(m), 1)
        first_day, end_date = get_month_range(day_month)
        last_day = end_date
        print(last_day, end_date, first_day)
    day_list = []

    while first_day <= last_day:
        day_list.append(str(first_day))
        first_day += a_day
    return day_list


def sku():
    pass


def spu():
    pass


class Sku_Order_every(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': ''}
        global sku_sql

    def list(self, request):
        starttime = time.time()
        ser_date = ''
        where_ser = ''
        turnover_ser = ''
        data = request.GET
        area = data.get('area')
        name = data.get('name')
        ser_month = data.get('dates')
        area_list = area.split('_')
        if '欧洲' in name:
            if '德国' in name:
                country = 'DE'
            elif '英国' in name:
                country = 'UK'
            elif '法国' in name:
                country = 'FR'
            elif '意大利' in name:
                country = 'IT'
            elif '西班牙' in name:
                country = 'ES'
            else:
                country = area_list[1].upper()
            site = area_list[0].upper()
        else:
            site, country = area_list[0].upper(), area_list[1].upper()
        if 'SKU' in name:
            type = 'SKU'
        elif 'SPU' in name:
            type = 'SPU'
        else:
            type = 'SKU'
        title_list = ['SPU', 'SKU', 'FBA', 'FBM', 'sum_spu'] if 'SKU' in name else ['SPU', 'FBA', 'FBM', 'sum_spu']
        site_cn, country_cn = change_site_country(site, country)
        table_name = 'order_sublist' if country in ['UK', 'DE', 'FR', 'ES', 'IT'] else 'sku_report'
        print(site_cn, '------', country_cn)

        date_every_sql = order_sql.date_every_sql.format(site, country, table_name)
        print(date_every_sql)
        fba_date = conf_fun.connect_mysql_re(date_every_sql, type='dict')

        try:
            fba_date = fba_date[0].get('times')
        except:fba_date =time.strftime('%Y-%m-%d', time.localtime())
        print(fba_date, '---', ser_month)
        if ser_month:
            print(3333333333333333)
            recent_day_list = get_date_list(ser_month, 2)
        else:
            recent_day_list = get_date_list(fba_date, 1)
        print(recent_day_list)
        for i in recent_day_list:
            ser_date += "'%s'," % (i)
            where_ser += "FORMAT (SUM(CASE WHEN times ='{0}' THEN nums END),0 ) as '{0}',".format(i)
            turnover_ser += " FORMAT (SUM(CASE WHEN dates ='{0}' THEN turnover END),0) as '{0}',".format(i)
            title_list.append(i)

        where_ser = where_ser.strip(',')
        ser_date = ser_date.strip(',')
        turnover_ser = turnover_ser.strip(',')
        if country_cn in ['英国', '德国', '法国', '意大利', '西班牙']:
            country_cn = '欧洲'

        print(country)
        if country in ['US', 'EU', 'CA', 'UK', 'IT', 'DE', 'FR', 'ES']:
            if country  in ['EU','UK', 'IT', 'DE', 'FR', 'ES']:
                fbm_country = ('UKPJ', 'DEPJ', 'FRWH', 'ITWH')
            elif country == 'CA':
                fbm_country = ('CA_YYZ', 'CA_YOW')
            elif country =='US':
                fbm_country = ('PJWL', 'NJPJ', 'USA_LA')
            else :fbm_country = ('xxx','zzzz')

        else:
            fbm_country = ('xxx','zzzz')

        if type in ['SKU']:

            sku_sql = order_sql.sku_sql.format(country_cn, site_cn, site, country, ser_date,
                                               where_ser, fba_date, table_name, fbm_country)
            #            print(sku_sql)
            turnover_sql = order_sql.turnover_sql.format(site, country, ser_date, turnover_ser)
            print('\n\n\n', turnover_sql)
            turnover_data = conf_fun.connect_mysql_re(turnover_sql, type='dict')
            print('\n\n\n', sku_sql)
            sku_data = conf_fun.connect_mysql_re(sku_sql, type='dict')

            self.ret['sku_data'] = sku_data
            self.ret['turnover_data'] = turnover_data
        elif type in ['SPU']:
            if country =='UK':
                country ='EU'
            spu_sql = order_sql.spu_sql.format(site, country, ser_date, where_ser, fba_date, fbm_country,country_cn,site_cn)
            print(spu_sql)
            spu_data = conf_fun.connect_mysql_re(spu_sql, type='dict')
            spu_table_name = 'order_sublist' if country_cn in ['英国'] else 'spu_report'
            spu_category_sql = order_sql.spu_category_sql.format(where_ser, ser_date, site, country, spu_table_name)
            print(spu_category_sql)
            spu_category_data = conf_fun.connect_mysql_re(spu_category_sql, type='dict')
            self.ret['spu_data'] = spu_data
            self.ret['spu_category_data'] = spu_category_data
        self.ret['title_list'] = title_list

        endtime = time.time()
        print('花费时间', (endtime - starttime))

        return Response(self.ret, content_type='text')


class Eu_Order_every(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': ''}

    def list(self, request):
        ser_date = ''
        where_ser = ''
        turnover_ser = ''
        data = request.GET
        area = data.get('area')
        name = data.get('name')
        return Response
