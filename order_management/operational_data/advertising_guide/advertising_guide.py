import re
import time
import datetime
from operator import itemgetter
from itertools import groupby
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from order_management.settings import order_sql

from settings import conf_fun
# conf_fun.connect_mysql_re

country_dict = {
    '澳洲': 'AU',
    '加拿大': 'CA',
    '西班牙': 'ES',
    '英国': 'UK',
    '法国': 'FR',
    '意大利': 'IT',
    '德国': 'DE',
    '日本': 'JP',
    '美国': 'US',
    '墨西哥': 'MX',
    '新加坡': 'SG',
    '马来西亚': 'MY',
}

site_dict = {
    '胤佑': 'YY',
    '京汇': 'JH',
    '中睿': 'ZR',
    '爱瑙': 'AN',
    '利百锐': 'LBR',
    '笔漾教育': 'BYJY',
    '景瑞': 'JR'}


def get_time(countries_data):
    # 美国 墨西哥,加拿大 时间
    if countries_data in ['US', 'CA']:
        date_1 = (datetime.datetime.now())
        date_2 = (datetime.datetime.now() + datetime.timedelta(days=-9))
        over_time = date_1.strftime("%Y-%m-%d")
        begin_time = date_2.strftime("%Y-%m-%d")
        fr_over_time = date_1.strftime("%Y.%m.%d")
        fr_begin_time = date_2.strftime("%Y.%m.%d")
    elif countries_data in ['AU', 'ES', 'UK', 'FR', 'IT', 'DE', 'JP', 'MX']:
        date_1 = (datetime.datetime.now())
        date_2 = (datetime.datetime.now() + datetime.timedelta(days=-8))
        over_time = date_1.strftime("%Y-%m-%d")
        begin_time = date_2.strftime("%Y-%m-%d")
        fr_over_time = date_1.strftime("%Y.%m.%d")
        fr_begin_time = date_2.strftime("%Y.%m.%d")
    else:
        over_time = time.strftime("%Y-%m-%d", time.localtime())
        begin_time = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
        fr_over_time = time.strftime("%Y.%m.%d", time.localtime())
        fr_begin_time = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y.%m.%d")

    return over_time, begin_time, fr_over_time, fr_begin_time


def gey_auto_name(request):
    data = request.GET
    auto_str = ''
    for key, value in data.items():
        print(key, value)
        if key == 'countries' and value:
            auto_str += " AND country = '%s'" % (value)
        elif key == 'company' and value:
            auto_str += " AND  company = '%s'" % (value)
    print(order_sql.auto_sql.format(auto_str))
    spu_num_list = conf_fun.connect_mysql_re(order_sql.auto_sql.format(auto_str), type='dict')
    ret = {}
    ret['spu_num'] = spu_num_list
    return JsonResponse(ret)


# 获取排名函数
def get_rank(data, front_sql, inventory_sql,fbm_sql):
    re_front_data = conf_fun.connect_mysql_operation(front_sql, type='dict')
    re_front_data_1 = {}
    re_inventory_data = {}
    print('89这是库存和排名\n', inventory_sql)
    inventory_data = conf_fun.connect_mysql_re(inventory_sql, type='dict')
    fbm_data = conf_fun.connect_mysql_re(fbm_sql,type='dict')

    for date, items_1 in groupby(inventory_data, key=(itemgetter('times'))):
        dt = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_1 = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        re_inventory_data[date_1] = {}
        for i in items_1:
            if i.get('sum_num'):
                re_inventory_data[date_1] = i.get('sum_num')
            else:re_inventory_data[date_1] = '0'

    for date,items_1 in groupby(fbm_data,key=(itemgetter('times'))):
        for i in items_1:
           z = float(re_inventory_data.get(date)) if re_inventory_data.get(date) else 0
           w = float(items_1.get('nums')) if items_1.get('nums') else 0
           re_front_data[date] = z+w

    pattern = '\d+'
    pattern_1 = '\d+.\d+|\d+,\d+'
    pattern_2= '\d+|\d+\s'
    for spu_num, items in groupby(re_front_data, key=itemgetter('spu')):
        if spu_num not in re_front_data_1:
            re_front_data_1[spu_num] = {}
        for dates, items_1 in groupby(items, key=itemgetter('dates')):
            _date = dates
            dates = dates.replace('.', '-')
            if dates not in re_front_data_1[spu_num]:
                re_front_data_1[spu_num][dates] = []
            for i in items_1:
#
                print(i.get('comment_amount'))
                if i.get('ranking'):
                    ranking = re.findall(pattern, i.get("ranking").replace(r',',''))
                    i["ranking"] = ranking[0]  if ranking else i.get('ranking')
                    # i["ranking"] = re.findall(pattern, i.get("ranking").replace(r',',''))[0]
                else:
                    i["ranking"] ='无'
                if i.get('small_rank'):
                    small_rank = re.findall(pattern, i.get('small_rank').replace(r',',''))
                    i['small_rank'] = small_rank[0] if small_rank else i.get('small_rank')
                    # i['small_rank'] = re.findall(pattern, i.get('small_rank').replace(r',',''))[0]
                else:
                    i['small_rank'] ='无'
                if i.get('comment_amount'):
                    zz =i.get('comment_amount').replace(r',','').replace(r'.','').replace(r'\xa0','').replace(r'\u3000','').replace(r'&nbsp','')
                    print(123,zz)
                    commnet_amount = re.findall(pattern_2, zz)
                    if commnet_amount:
                        if commnet_amount[0] ==1:
                            i['comment_amount'] =i.get('comment_amount')
                        else:
                            i['comment_amount'] =  commnet_amount[0]
                    else:i['comment_amount'] = i.get('comment_amount')
                if i.get('star_level'):
                    star_list = re.findall(pattern_1,i.get('star_level'))
                    i['star_level'] = star_list[0] if star_list else i.get('star_level')
                    # i['star_level'] = i.get('star_level').split('，')[0]
                inventory_num = re_inventory_data.get(dates)
                if inventory_num or inventory_num == 0.0:
                    i['inventory'] = re_inventory_data.get(dates) if re_inventory_data.get(dates) else '0'
                else: i['inventory'] = '0'
                if not re_front_data_1[spu_num][dates]:
                    re_front_data_1[spu_num][dates].append(i)
                elif re_front_data_1[spu_num][dates]:
                    comment_amount_small = re_front_data_1[spu_num][dates][0].get('comment_amount')
                    comment_amount_big = i.get('comment_amount')
                    if comment_amount_big > comment_amount_small:
                        re_front_data_1[spu_num][dates][0] = i
    if not re_front_data_1:

        country = data.get('country')
        site = data.get('site')
        auto = data.get('auto')
        sql = " SELECT * FROM auto_ad WHERE country ='{0}' and company ='{1}' and auto='{2}' and type='手动'".format(
            country, site, auto)
        print(sql)
        re_spu_data = conf_fun.connect_mysql_re(sql, type='dict')
        # it 意大利

        country_low = country_dict.get(country).lower()
        if country in ['德国', '意大利', '法国', '西班牙', '英国']:
            country = '欧洲'

        for spu_num, item in groupby(re_spu_data, key=itemgetter('spu')):
            link_sql = " SELECT product_link FROM commodity_information  WHERE  commodity_state ='在售' and country ='{0}' and site ='{1}' and spu ='{2}'" \
                .format(country, site, spu_num)

            link_data = conf_fun.connect_mysql_operation(link_sql, type='dict')
            if link_data:
                for link_dict in link_data:

                    if country_low in ['es', 'uk', 'fr', 'it', 'de']:

                        if country_low in link_dict.get('product_link'):
                            re_front_data_1[spu_num] = [
                                '广告组为 {0} spu为 {1} 链接为 {2}未获取近期排名 请联系IT'.format(auto, spu_num,
                                                                                   link_dict.get('product_link'))]
                    else:
                        re_front_data_1[spu_num] = ['广告组为 {0} spu为 {1} 链接为 {2} 未获取近期排名 请联系IT'.format(auto, spu_num,
                                                                                                        link_dict.get(
                                                                                                            'product_link'))]

            else:
                str_1 = '广告组为 {0} spu为 {1}的产品链接不存在，请前往商品信息页面补充，以便于IT获取'.format(auto, spu_num)
                re_front_data_1[spu_num] = [str_1]

    return re_front_data_1


# 获取广告指导数据
def get_advertising(re_data):
    now_time = time.strftime("%Y-%m-%d", time.localtime())  # 今天日期
    import datetime
    day_7 = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    # 2018-05-07 16:56:59

    re_data_2 = {}
    re_data_3 = {}  # 这个中间变量 用来存储上一天的数据

    for data_dict in re_data:
        day_time = data_dict.get('times')  # 这个是当前数据库存储的日期

        re_data_3[day_time] = data_dict
        if day_time:
            # print('这是日期',day_time)
            day_1 = datetime.datetime.strptime(day_time, "%Y-%m-%d")  # 数据的当前日 datetime化
            to_day = (day_1 + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),  # 这是把数据库的日期加一
            to_day = to_day[0]

            yesterday = (day_1 + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")  # 这个是日期减一
            countries, company = data_dict.get('countries'), data_dict.get('company')  # 国家站点
            judge_str = "%s_%s" % (countries, company)
            print(191,'--------\n\n',judge_str)
            str_day = str(to_day)

            auto_ad_cost, no_auto_ad_cost = data_dict.get('auto_ad_cost'), data_dict.get('no_auto_ad_cost')
            auto_ad_cost = auto_ad_cost if auto_ad_cost else 0.00
            no_auto_ad_cost = no_auto_ad_cost if no_auto_ad_cost else 0.00
            sales = data_dict.get('sales')

            if to_day not in re_data_2.keys() and day_time <= now_time:
                # 验证day_time的日期加一以及加一的日期是否小于当前日期
                #   系统指导价自动，系统指导价手动

                if str_day <= now_time:
                    # 这个是将对应数据库的day_time 加一天
                    # 'auto_ad_cost': auto_ad_cost, 'no_auto_ad_cost': no_auto_ad_cost,
                    if countries in ['美国','加拿大']:
                        re_data_2[str_day] = [{ 'auto_ad_cost': '',
                                                'no_auto_ad_cost': '',
                                               'times': str_day, 'countries': countries, 'company': company,
                                               'manual_guidance': '', 'automatic_guidance': '', 'sales': sales}]
                    else:
                        re_data_2[str_day] = [{ 'auto_ad_cost': '', 'no_auto_ad_cost': '',
                                                'times': str_day, 'countries': countries, 'company': company,
                                                'manual_guidance': '', 'automatic_guidance': '', 'sales': sales}]

            if day_time in re_data_2.keys() and day_time <= now_time:
                # intermediate_dict 这个是中间变量字典用来存放上一天的系统指导价和这一天的其他数据
                # 将美国和加拿大的去获取数据的日期不向后退一天
                print('这是获取最近七天的日期day_time', day_time, '加一天to_day', to_day,'当天new_time', now_time)
                # sales = re_data_3.get(day_time).get('sales') if data_dict.get('countries')in ['加拿大','美国'] \
                #         else re_data_3.get(yesterday).get('sales')
                sales = re_data_3.get(yesterday).get('sales')
                # auto_ad_cost = re_data_3.get(day_time).get('auto_ad_cost') if data_dict.get('countries')in ['加拿大','美国'] else auto_ad_cost
                # no_auto_ad_cost = re_data_3.get(day_time).get('no_auto_ad_cost') if data_dict.get('countries')in ['加拿大','美国'] else no_auto_ad_cost

                intermediate_dict = re_data_2.get(day_time)[0]

                intermediate_dict['id'] = data_dict.get('id')
                intermediate_dict['auto_ad_cost'] = auto_ad_cost
                intermediate_dict['no_auto_ad_cost'] = no_auto_ad_cost
                intermediate_dict['manual_guidance'] = data_dict.get('manual_guidance')
                intermediate_dict['automatic_guidance'] = data_dict.get('automatic_guidance')
                intermediate_dict['cost_rate'] = data_dict.get('cost_rate')  # 花费比
                intermediate_dict['remakes'] = data_dict.get('remakes')  # 备注
                intermediate_dict['company'] = data_dict.get('company')  # 站点
                intermediate_dict['countries'] = data_dict.get('countries')  # 国家
                intermediate_dict['spu'] = data_dict.get('spu')  # spu
                intermediate_dict['sales'] = sales  # spu
                intermediate_dict['times'] = day_time
                re_data_2[day_time] = [intermediate_dict]
                print(str_day )
                if str_day == '2021-03-10':
                    print(205, '--\n', re_data_2[str_day])

            if now_time in re_data_2.keys():

                if len(re_data_2.get(now_time)[0]) == 3:  # 这是用来判断 如果没有今天的数据 就给给他弄个假的，让他填写
                    intermediate_dict = re_data_2.get(to_day)[0]
                    intermediate_dict['id'] = ''
                    intermediate_dict['company'] = data_dict.get('company')  # 站点
                    intermediate_dict['countries'] = data_dict.get('countries')  # 国家
                    intermediate_dict['spu'] = data_dict.get('spu')  # spu
                    intermediate_dict['remakes'] = ''
                    intermediate_dict['cost_rate'] = ''
                    intermediate_dict['manual_guidance'] = ''
                    intermediate_dict['automatic_guidance'] = ''
                    intermediate_dict['sales'] = data_dict.get('sales')
                    re_data_2[now_time] = [intermediate_dict]


    return re_data_2


class Advertising_Guide(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        data = request.GET
        ser_str = ''
        fr_ser_str = ''  # 这个是排名的
        auto_str = ''  # 这个是自动组的
        inventory_str = ''  # 库存检索
        print(123123)
        print(data)
        auto = data.get('auto')
        for key, value in data.items():

            if key == 'auto' and value:
                ser_str += " and %s ='%s'" % (key, value)
            elif key == 'country' and value:
                ser_str += " AND country = '%s'" % (value)
                fr_ser_str += " AND country = '%s'" % (value)
                auto_str += " AND country = '%s'" % (value)
                inventory_str += " AND countries = '{0}'".format(country_dict.get(value))
            elif key == 'site' and value:
                ser_str += " AND site ='%s'" % (value)
                fr_ser_str += " AND area in ('%s' ,'%s')" % (site_dict.get(value), value)
                auto_str += " AND  company = '%s'" % (value)
                inventory_str += " AND company = '%s'" % (site_dict.get(value))
            elif key == 'spu' and value:
                spu_list = value.split(',')
                spu_str = ''
                for spu in spu_list:
                    if spu:
                        spu_str += " '%s' , " % (spu)
                spu_str = spu_str.rstrip(' , ')
                fr_ser_str += " AND SPU IN (%s)" % (spu_str)
                inventory_str += " AND spu IN (%s)" % (spu_str)

        countries_data = country_dict.get(data.get('countries'))
        # 美国 墨西哥,加拿大 时间
        over_time, begin_time, fr_over_time, fr_begin_time = get_time(countries_data)

        ser_str += " AND  dates >= '%s' AND dates <='%s'" % (begin_time, over_time)
        fr_ser_str += " and dates >= '%s' AND dates <='%s' " % (fr_begin_time, fr_over_time)
        inventory_str += " AND times >= '%s' AND times <= '%s'" % (begin_time, over_time)
        sql = order_sql.sql.format(ser_str)
        front_sql = order_sql.front_sql.format(fr_ser_str)
        print('这是同步广告指导的sql',sql)
        re_data = conf_fun.connect_mysql_re(sql, type='dict')
        print('\n这是排名', front_sql, '\n')

        re_data_1 = {}
        # 这个是分组按照 spu
        for data_1, items in groupby(re_data, key=itemgetter('spu')):

            if data_1 not in re_data_1:
                re_data_1[data_1] = []
            for i in items:
                if i.get('spu') in re_data_1.keys():
                    re_data_1[data_1].append(i)
        # 获取广告数据
        re_data_2 = get_advertising(re_data)
        # 这个是分组排序排名和评论的
        # 库存sql
        country = data.get('country')
        if country in ['美国', '欧洲', '加拿大', '英国', '意大利', '德国', '法国', '西班牙']:
            if country in ['欧洲', '英国', '意大利', '德国', '法国', '西班牙']:
                fbm_country = ('UKPJ', 'DEPJ', 'FRWH', 'ITWH')
            elif country == '加拿大':
                fbm_country = ('CA_YYZ', 'CA_YOW')
            elif country == '美国':
                fbm_country = ('PJWL', 'NJPJ', 'USA_LA')
            else:
                fbm_country = ('xxx', 'zzzz')

        else:
            fbm_country = ('xxx', 'zzzz')
        fbm_sql = "SELECT spu,SUM(nums) as nums,times FROM fbm_data " \
                  " where  area in {0} and spu = {1} GROUP BY spu,times ".format(fbm_country,spu)
        if country in ['德国', '英国', '法国', '意大利', '西班牙']:
            inventory_sql = order_sql.eu_sql.format('order_sublist', inventory_str)
        else:
            inventory_sql = order_sql.eu_sql.format('sku_report', inventory_str)
        print('',inventory_sql)
        re_front_data_1 = get_rank(data, front_sql, inventory_sql,fbm_sql)
        self.ret['re_data'] = re_data_2
        self.ret['re_spu_data'] = re_front_data_1

        # self.ret = serializers.serialize('json',self.ret)
        return Response(self.ret)

    def alter(self, request):
        data = request.data
        id = data.get('id')
        update_str = ''
        where_str = ''
        key_str = ''
        value_str = ''
        print(data)
        for key, value in data.items():
            if key not in ['id', 'site', 'country', 'dates', 'auto'] and value:

                update_str += " %s = '%s' , " % (key, value)
            elif key in ['site', 'country', 'dates', 'auto']:
                where_str += " AND %s = '%s'" % (key, value)
            if key not in key_str and value:
                key_str += " %s ," % (key)
                value_str += " '%s' ," % (value.replace("'", '').replace('"', ''))
        key_str = key_str.rstrip(' ,')
        value_str = value_str.rstrip(' ,')
        update_str = update_str.rstrip(' , ')
        judge_sql = " SELECT * FROM advertising_adjustment WHERE id > 0 {0}".format(where_str)
        print(judge_sql)
        re_judge_data = conf_fun.connect_mysql_re(judge_sql, type='dict')
        print(re_judge_data)
        if re_judge_data:
            update_sql = " update advertising_adjustment set {0} where id>0 {1}".format(update_str, where_str)
            print(update_sql)
            conf_fun.connect_mysql_re(update_sql)

        else:
            inster_sql = " INSERT INTO advertising_adjustment ( {0} ) values ( {1})".format(key_str, value_str)
            print('这是插入语句', inster_sql)
            conf_fun.connect_mysql_re(inster_sql)

        print(update_str)

        return Response(self.ret)
