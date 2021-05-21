import pymysql, os, time, requests, json
from operator import itemgetter
from itertools import groupby
import time
from customer_management.settings import settings

from django.http import HttpResponse, JsonResponse
from settings import conf_fun
''' 运营的 '''





def sql_data(sql):
    print(sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    return data


''' 发货的'''




'''返回邮件左侧的国家/站点'''


def left_show():
    sql = "SELECT platform,country,site FROM store_information where  platform !='' and country !='' and site !='' group by platform,country,site  ORDER BY platform,country"
    print('\n\n\n\n123123123', sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    data_dict = {}
    for platform, items in groupby(data, key=itemgetter('platform')):
        data_dict[platform] = {}

        for country, items_1 in groupby(items, key=itemgetter('country')):

            data_dict[platform][country] = []
            for i in items_1:
                data_dict[platform][country].append(i.get('site'))

    # print(data_dict)
    return data_dict


'''获取供应链的数据'''



# 新增的链接数据库
def conn_sql_demo(table_name, key_str, value_str):
    sql = "INSERT INTO  {0}  ( {1} ) VALUES ({2})".format(table_name, key_str, value_str)
    res = conf_fun.connect_mysql_operation(sql, type='dict')
    return res


# 新增数据的统一模板

def add_template_data(data, table_name, key_name, key_value):
    key_list = []
    value_list = []
    for key, value in data.items():
        key_list.append(key)
        value_list.append(r'"{}"'.format(value))
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    key_list.append(key_name)
    value_list.append(r'"{}"'.format(key_value))
    key_str = ','.join(key_list)  # 新增的字段
    value_str = ','.join(value_list)
    res = conn_sql_demo(table_name, key_str, value_str)
    return res


# 修改数据的sql
def alter_sql_demo(table_name, update_str, id):
    sql = "UPDATE {0} SET {1} WHERE id={2}".format(table_name, update_str, id)

    conf_fun.connect_mysql_operation(sql)


# 修改数据的统一模板
def alter_template_data(data, table_name):
    update_list = []
    for key, value in data.items():
        if key != 'id':
            update_list.append("%s = '%s'" % (key, value))

    update_str = ','.join(update_list)
    alter_sql_demo(table_name, update_str, int(data.get('id')))


'''搜索功能包括 左侧的搜索'''


def serach_data(data):
    sql = "SELECT c.id,c.product_code, c.spu, c.sku , c.country , c.site , c.channel," \
          "c.commodity_state, c.commodity_price, c.asin , c.fnsku, c.upc , c.begin_sell_date,c.over_sell_date, c.select_link," \
          "c.sku_link,c.product_link," \
          "s.product_name,s.product_type from commodity_information as c, product_message as s " \
          " WHERE c.product_code = s.product_code AND "
    search_list = []
    for key, value in data.items():
        search_list.append("c.%s = '%s'" % (key, value))
    search_str = ' AND '.join(search_list)
    sql += search_str
    print(sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')

    return data


# 词汇库


# 翻译
def translate_func(content):
    translate_url = 'http://www.beyoung.group/translate/'  # 翻译地址
    translate_data = {'passwd': '50fffff9f0225513a93f041e9b939c0b', 'translate_str': content}
    response_data = requests.post(translate_url, data=translate_data)
    json_response_data = json.loads(response_data.content).get('msg')  # 翻译的内容
    data = json.loads(json_response_data)
    language = data.get('from')
    translate_content = data.get('trans_result')
    print(json_response_data, '1111111111111111111', content)
    data_str = ''
    for i in translate_content:
        data_str += i.get('dst')
    # print('翻译后的数据',data_str ,'\n' )
    return data_str, language


# 词义分析
def keyword_func(content):
    keyword_url = 'http://www.beyoung.group/semantic_analysis/'
    print('\n\n翻译内容', content)
    keyword_data = {'passwd': 'f4645b2fd1847cfe548058d4000f6bfe', 'semantic_analysis_str': content}
    response_keyword_data = requests.post(keyword_url, data=keyword_data)  # 关键字请求分析
    # print(response_keyword_data)
    print(response_keyword_data, '\n\n词义分析')
    data = json.loads(response_keyword_data.content).get('msg')
    # print('关键字匹配',data ,'\n')
    json_keyword_data = data.get('items')
    return json_keyword_data


# 关键字
# 破损/缺少关键字

def data_analysis(usa_data, eu_data, problem_data, ups_data):
    for i in problem_data:
        print(i)

    data_list = []
    data_dict = {}
    for dict_1 in usa_data:
        platform = dict_1.get('platform_channels')
        if platform: platform = platform.title()
        site = dict_1.get('the_store')
        country = settings.country_dict.get(dict_1.get('country_code'))[0]
        sku = dict_1.get('sku')
        data_dict['platform'] = platform
        data_dict['site'] = site
        data_dict['country'] = country
        data_dict['sku'] = sku
        data_dict['sku_num'] = dict_1.get('sku_count')
        data_dict['email_num'] = 0
        for pro_dict in problem_data:

            if pro_dict.get('platform') == platform and pro_dict.get('site') == site and country == pro_dict.get(
                    'country') and sku == pro_dict.get('sku'):
                data_dict['email_num'] = pro_dict.get('sku_count')
        data_list.append(data_dict)
        data_dict = {}

    for dict_eu in eu_data:

        platform = dict_eu.get('platform_channels')
        if platform: platform = platform.title()
        site = dict_eu.get('the_store')
        print('\n???', dict_eu)
        country = settings.country_dict.get(dict_eu.get('country_code').upper())[0]
        sku = dict_eu.get('product_sku')
        data_dict['platform'] = platform
        data_dict['site'] = site
        data_dict['country'] = country
        data_dict['sku'] = sku
        data_dict['sku_num'] = dict_eu.get('sku_count')
        data_dict['email_num'] = 0
        for pro_dict in problem_data:

            if pro_dict.get('platform') == platform and pro_dict.get('site') == site and country == pro_dict.get(
                    'country') and sku == pro_dict.get('sku'):
                data_dict['email_num'] = pro_dict.get('sku_count')
        data_list.append(data_dict)

        data_dict = {}

    for dict_ups in ups_data:
        platform = dict_ups.get('platform_channels')
        if platform: platform = platform.title()
        site = dict_ups.get('the_store')

        country = settings.country_dict.get(dict_ups.get('country_code').upper())[0]
        sku = dict_ups.get('sku')

        data_dict['platform'] = platform
        data_dict['site'] = site
        data_dict['country'] = country
        data_dict['sku'] = sku
        data_dict['sku_num'] = dict_ups.get('sku_count')
        data_dict['email_num'] = 0

        for pro_dict in problem_data:

            if pro_dict.get('platform') == platform and pro_dict.get('site') == site and country == pro_dict.get(
                    'country') and sku == pro_dict.get('sku'):
                data_dict['email_num'] = pro_dict.get('sku_count')
        data_list.append(data_dict)

        data_dict = {}

    return data_list


def usa_data_analysis(usa_data, problem_data):
    data_list = []
    data_dict = {}
    print('????', usa_data)
    for dict_1 in usa_data:
        platform = dict_1.get('platform_channels')
        if platform: platform = platform.title()
        site = dict_1.get('the_store')
        country = settings.country_dict.get(dict_1.get('country_code'))[0]
        sku = dict_1.get('sku')
        data_dict['platform'] = platform
        data_dict['site'] = site
        data_dict['country'] = country
        data_dict['sku'] = sku
        data_dict['sku_num'] = dict_1.get('count')
        data_dict['email_num'] = 0
        data_dict['date'] = dict_1.get('months')
        for pro_dict in problem_data:
            if pro_dict.get('platform') == platform and pro_dict.get('site') == site and country == pro_dict.get(
                    'country') and sku == pro_dict.get('sku'):
                data_dict['email_num'] = pro_dict.get('sku_count')
        data_list.append(data_dict)
        data_dict = {}

    return data_list


def eu_data_analysis(eu_data, problem_data):
    data_list = []
    data_dict = {}

    for dict_eu in eu_data:

        platform = dict_eu.get('platform_channels')
        if platform: platform = platform.title()
        site = dict_eu.get('the_store')

        country = settings.country_dict.get(dict_eu.get('country_code').upper())[0]
        sku = dict_eu.get('product_sku')
        data_dict['platform'] = platform
        data_dict['site'] = site
        data_dict['country'] = country
        data_dict['sku'] = sku
        data_dict['sku_num'] = dict_eu.get('count')
        data_dict['email_num'] = 0
        data_dict['date'] = dict_eu.get('date')
        for pro_dict in problem_data:

            if pro_dict.get('platform') == platform and pro_dict.get('site') == site and country == pro_dict.get(
                    'country') and sku == pro_dict.get('sku'):
                data_dict['email_num'] = pro_dict.get('sku_count')
        data_list.append(data_dict)

        data_dict = {}
    print('\n', '欧洲', data_list, '\n')
    return data_list


def ups_data_analysis(ups_data, problem_data):
    data_list = []
    data_dict = {}
    for dict_ups in ups_data:
        platform = dict_ups.get('platform_channels')
        if platform: platform = platform.title()
        site = dict_ups.get('the_store')

        country = settings.country_dict.get(dict_ups.get('country_code').upper())[0]
        sku = dict_ups.get('sku')
        data_dict['platform'] = platform
        data_dict['site'] = site
        data_dict['country'] = country
        data_dict['sku'] = sku
        data_dict['sku_num'] = dict_ups.get('sku_count')
        data_dict['email_num'] = 0
        for pro_dict in problem_data:

            if pro_dict.get('platform') == platform and pro_dict.get('site') == site and country == pro_dict.get(
                    'country') and sku == pro_dict.get('sku'):
                data_dict['email_num'] = pro_dict.get('sku_count')
        data_list.append(data_dict)

        data_dict = {}
    return data_list


def down_load_file(request):
    url = 'https://www.beyoung.group/file_download/'
    args = request.GET
    print(args)
    path = args.get('path')
    filename = args.get('filename')
    data = {'path': path, 'filename': filename}
    print('\n参数', data)
    res = requests.post(url, data)
    print(res)
    ret = {'re_data': res}
    return JsonResponse(ret)
def upload_file(files):
    path1 = []

    if files:
        for file_key in files:
            file_name = file_key
            path2 = os.path.join(r'static/data/', str(file_name))
            path = os.path.join(os.getcwd(), path2)

            with open(path, 'wb') as f:
                for line in file_key:
                    f.write(line)
            path1.append(path2)
        path1 = ' @ '.join(path1)
    else:
        path1 = ''
    return path1

# 这个上传亚马逊站内邮件上传文件的接口
def save_file(files):
    path_1 = ''
    for file in files.getlist('files'):
        print(file)
        path = os.path.join(r'static/data/email/image',str(file))
        print(path)
        if not os.path.exists('static/data/email/image'):
            os.makedirs('static/data/email/image')
        with open(path, 'wb') as f:
            for line in file:
                f.write(line)
        path_1 += "{0}@".format(path)
    path_1 = path_1.rstrip('@')
    return path_1