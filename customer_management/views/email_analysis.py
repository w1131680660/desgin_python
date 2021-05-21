from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from customer_management.settings import conf_fun as conf_fun_1
from customer_management.settings import sql, settings
from settings import conf_fun


# 邮件分析


def search_demo(data):
    platform = data.get('platform')
    site = data.get('site')
    country = settings.country_ch_dict.get(data.get('country'))
    sku = data.get('sku')
    str_sql = ""
    print(1231231, data, '\n')
    for key, value in data.items():
        if key == 'sku' and value:
            str_sql += " AND r.sku = '{0}' ".format(sku)

        elif key == 'platform' and value:
            str_sql += " AND r.platform_channels = '{0}' ".format(platform)

        elif key == 'site' and value:
            str_sql += " AND r.the_store ='{0}'".format(site)

        elif key == 'country' and value:
            str_sql += "AND o.country_code ='{0}'".format(country)

        elif key == 'begin_date' and value:
            print(12312312321321)
            str_sql += " AND o.dates >= '%s'" % (value)

        elif key == 'over_date' and value:
            str_sql += " AND o.dates <= '%s'" % (value)

    if country == 'US':
        sql_sql = sql.sql_date_usa.format(str_sql)

        count_sql = sql.sql_usa_count.format(str_sql)
    elif country == 'CA':
        sql_sql = sql.sql_ups.format(str_sql)

        count_sql = sql.sql_usa_count.format(str_sql)
    else:
        sql_sql = sql.sql_eu_data.format(str_sql)
        count_sql = sql.sql_eu_se_count.format(str_sql)
    print('查询的sql', sql_sql, '\n')
    print('总数的sql', count_sql, '\n')
    data_re = conf_fun.connect_mysql_or(sql_sql, type='dict')
    count_data = conf_fun.connect_mysql_or(count_sql, type='dict')
    print(data_re, '\n')
    print(count_data)
    return data_re, count_data


def search_order(data):
    page = data.get('page') if data.get('page') else 1

    sql_usa = sql.sql_usa.format('')
    print('\n\n美国的', sql_usa)
    sql_eu = sql.sql_eu.format('')
    sql_ups = sql.sql_ups.format('')

    sql_usa_count = sql.sql_usa_count.format('')
    sql_eu_count = sql.sql_eu_count.format('')
    sql_ups_count = sql.sql_ups_count.format('')
    problem_sql = sql.problem_sql.format('')
    problem_data = conf_fun.connect_mysql_operation(problem_sql, type='dict')

    if len(data.keys()) > 1:
        data_1, count_data = search_demo(data)
        print('大于11111111111', data_1, '\n')
        country = settings.country_ch_dict.get(data.get('country'))

        if country == 'US':
            data_re = conf_fun_1.usa_data_analysis(data_1, problem_data)
        elif country == 'CA':
            data_re = conf_fun_1.ups_data_analysis(data_1, problem_data)
        else:
            data_re = conf_fun_1.eu_data_analysis(data_1, problem_data)
        count = count_data[0].get('count_num')

    else:
        print('\n\n\n小于!!!!!!!!!!!!')
        usa_data = conf_fun.connect_mysql_re(sql_usa, type='dict')
        eu_data = conf_fun.connect_mysql_re(sql_eu, type='dict')
        ups_data = conf_fun.connect_mysql_re(sql_ups, type='dict')
        data_re = conf_fun_1.data_analysis(usa_data, eu_data, problem_data, ups_data)

        usa_count = conf_fun.connect_mysql_or(sql_usa_count, type='dict')
        eu_count = conf_fun.connect_mysql_or(sql_eu_count, type='dict')
        ups_count = conf_fun.connect_mysql_or(sql_ups_count, type='dict')
        count = int(usa_count[0].get('count_num')) + int(eu_count[0].get('count_num')) + int(
            ups_count[0].get('count_num'))
        # 对所有的订单数进行合计

    count_dict = {}
    count_dict['count'] = count

    return data_re, count_dict


def nice_comment_sql(data):
    page = data.get('page') if data.get('page') else 1
    platform = data.get('platform')
    site = data.get('site')
    country = data.get('country')
    upload_people = data.get('upload_people')
    str_sql = ""

    for key, value in data.items():
        if key == 'upload_people' and value:
            str_sql += " AND upload_people  = '{0}' ".format(upload_people)

        elif key == 'platform' and value:
            str_sql += " AND platform = '{0}' ".format(platform)

        elif key == 'site' and value:
            str_sql += " AND site ='{0}'".format(site)

        elif key == 'country' and value:
            str_sql += "AND country ='{0}'".format(country)

        elif key == 'begin_date' and value:
            str_sql += " AND upload_time >= '%s'" % (value)

        elif key == 'over_date' and value:
            str_sql += " AND upload_time  <= '%s'" % (value)
    if data.get('serach'):
        nice_comment_sql_1 = sql.nice_comment_ser_sql.format(str_sql)
        nice_comment_charge_sql = sql.nice_comment_charge_sql.format(str_sql)
    else:
        nice_comment_sql_1 = sql.nice_comment_sql.format(str_sql)
        nice_comment_charge_sql = sql.nice_comment_charge_sql.format(str_sql)

    print(nice_comment_charge_sql)
    nice_comment_data = conf_fun.connect_mysql_operation(nice_comment_sql_1, type='dict')
    nice_comment_people = conf_fun.connect_mysql_operation(nice_comment_charge_sql, type='dict')
    re_data_list = []
    for nice_dict in nice_comment_data:
        for pe_dict in nice_comment_people:
            if nice_dict.get('upload_people') == pe_dict.get('upload_people'):
                nice_dict['count_all'] = pe_dict.get('count_all')
                re_data_list.append(nice_dict)

    print(re_data_list)
    return re_data_list


# 邮件订单分析


def email_ratio_analysis(data):
    sql = " SELECT ord.platform, ord.site, ord.sku, ord.country_code, ord.sku, COUNT(ord.order_id) AS ord_count, " \
          " COUNT(re.order_number) AS pro_count FROM order_record AS ord LEFT JOIN reply_customers AS re " \
          " on  ord.sku = re.sku AND ord.order_id = re.order_number " \
          " where ord.id > 0 {0}" \
          " GROUP BY ord.platform, ord.site, ord.sku, ord.country_code, ord.sku ORDER BY COUNT(re.order_number) DESC LIMIT {1},50"
    count_sql = " SELECT COUNT(s.sku) as count FROM ( SELECT ord.platform, ord.site, ord.sku, ord.country_code, COUNT(ord.order_id) AS ord_count, " \
                " COUNT(re.order_number) AS pro_count FROM order_record AS ord LEFT JOIN reply_customers AS re " \
                " on  ord.sku = re.sku AND ord.order_id = re.order_number " \
                " WHERE ord.id >0 {0} GROUP BY ord.platform, ord.site, ord.sku, ord.country_code, ord.sku ORDER BY COUNT(re.order_number) DESC) s"
    page = data.get('page') if data.get('page') else 1
    print('数据\n', data)
    page_num = (int(page) - 1) * 50
    ser_str = ''
    if len(data.keys()) == 1:
        sql = sql.format(' ', page_num)
        count_sql = count_sql.format(' ')
    elif data.get('recent_date'):
        ser_str = " AND DATE_SUB(CURDATE(), INTERVAL %s day) <= date(re.upload_time)" % (data.get('recent_date'))
        count_sql = count_sql.format(ser_str)
        sql = sql.format(ser_str, page)

    else:
        for key, value in data.items():
            print(key)
            if key not in ['page', 'begin_date', 'over_date'] and value:
                ser_str += " AND ord.%s = '%s' " % (key, value)
            elif key == 'begin_date' and value:
                print('\n', 123123)
                ser_str += " AND re.upload_time >= '%s' " % (value)
            elif key == 'over_date' and value:
                ser_str += " AND re.upload_time <= '%s' " % (value)
        print(ser_str)
        sql = sql.format(ser_str, page_num)
        count_sql = count_sql.format(ser_str)

    print('查询\n\n\n', sql)

    ret_data = conf_fun.connect_mysql_operation(sql, type='dict')
    print('\n\n总和', count_sql)
    count_data = conf_fun.connect_mysql_operation(count_sql, type='dict')
    return ret_data, count_data


class Mail_Analysis(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        data = request.GET

        left_data = conf_fun_1.left_show()
        data_dict, count_dict = email_ratio_analysis(data)

        self.ret['data_list'] = data_dict
        self.ret['data_count'] = count_dict
        self.ret['left_data'] = left_data
        # 1.返回所有平台国家站点下的
        return Response(self.ret)


# 好评率
class Nice_Comment(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        data = request.GET
        left_data = conf_fun_1.left_show()
        nice_comment_data = nice_comment_sql(data)
        self.ret['Left_data'] = left_data
        self.ret['nice_comment_data'] = nice_comment_data
        return Response(self.ret)


def search_process(data):
    se_list = ['summary_type_se', 'sky_type_se', 'factory_type_se', 'warehouse_type_se', 'operation_type_se', 'page']
    ser_str = ''

    for key, value in data.items():
        if key not in se_list and value:
            if key == 'factory':
                ser_str += " AND  f.%s = '%s' " % (key, value)
            elif key == 'begin_time':
                ser_str += " AND r.upload_time >='%s' " % (value)
            elif key == 'over_time':
                ser_str += " AND r.upload_time >='%s'" % (value)
            else:
                ser_str += " AND r.%s = '%s' " % (key, value)

    return ser_str


def sql_all(data):
    page = int(data.get('page')) if data.get('page') else 1
    page = (page - 1) * 50
    print('请求数据', data, '\n')
    ser_str = search_process(data)
    print(ser_str, '搜索', '\n')
    if len(data.keys()) == 1:
        all_sql = sql.all_sql.format('', page)
        count_sql = sql.count_all_sql.format('')

    elif data.get('summary_type_se') == 'ok':
        all_sql = sql.all_sql.format(ser_str, page)
        count_sql = sql.count_all_sql.format(ser_str)


    elif data.get('sky_type_se') == 'ok':  # 按商品
        all_sql = sql.sku_sql.format(ser_str, page)
        count_sql = sql.count_sku_sql.format(ser_str)

    elif data.get('factory_type_se') == 'ok':  # 按照工厂
        all_sql = sql.factory_sql.format(ser_str, page)
        count_sql = sql.count_factory_sql.format(ser_str)

    elif data.get('warehouse_type_se') == 'ok':  # 按照海外仓
        all_sql = sql.warehouse_sql.format(ser_str, page)
        count_sql = sql.count_warehouse_sql.format(ser_str)

    elif data.get('operation_type_se') == 'ok':  # 按照运营类型
        all_sql = sql.operate_sql.format(ser_str, page)
        count_sql = sql.count_operate_sql.format(ser_str)

    print(all_sql, '\n')
    re_data = conf_fun.connect_mysql_operation(all_sql, type='dict')
    count_data = conf_fun.connect_mysql_operation(count_sql, type='dict')
    return re_data, count_data


def drop_down_demo():
    an_site_list, an_country_list, an_sku_list, an_factory_list, \
    an_essence_list, an_problem_list, an_people_list = [], [], [], [], [], [], []
    for_list = ['site', 'country', 'sku', 'factory', 'problem_reason', 'problem_type', 'upload_people']

    an_site_data = conf_fun.connect_mysql_operation(sql.an_site_sql, type='dict')
    an_country_data = conf_fun.connect_mysql_operation(sql.an_country_sql, type='dict')
    an_sku_data = conf_fun.connect_mysql_operation(sql.an_sku_sql, type='dict')
    an_factory_data = conf_fun.connect_mysql_operation(sql.an_factory_sql, type='dict')

    an_essence_data = conf_fun.connect_mysql_operation(sql.an_essence_sql, type='dict')
    an_problem_type_data = conf_fun.connect_mysql_operation(sql.an_problem_type_sql, type='dict')
    an_people_data = conf_fun.connect_mysql_operation(sql.an_people_sql, type='dict')

    an_list = [an_site_data, an_country_data, an_sku_data, an_factory_data, an_essence_data, an_problem_type_data,
               an_people_data]
    re_list = [an_site_list, an_country_list, an_sku_list, an_factory_list, an_essence_list, an_problem_list,
               an_people_list]

    for index, object_list in enumerate(an_list):
        for channel_dict in object_list:
            q = {}

            q['value'] = channel_dict.get(for_list[index])
            q['label'] = channel_dict.get(for_list[index])
            re_list[index].append(q)

    return re_list


# 问题邮件分析汇总
def email_analysis_all(request):
    ret = {'code': 200, 'msg': '无'}
    data = request.GET
    re_list = drop_down_demo()

    re_data, count_data = sql_all(data)
    ret['re_list'] = re_list
    ret['re_data'] = re_data
    ret['count_data'] = count_data
    return JsonResponse(ret)
