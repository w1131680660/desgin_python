import json
from datetime import datetime, date, timedelta
from urllib.parse import unquote

import pymysql
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from stock_management.scheduling_management import scheduling_sql, scheduling_func

import os, time
import pandas as pd
import requests.models
from stock_management.scheduling_management import post_generation
from stock_management import  scheduling_settings
from settings import conf_fun

# 获取下拉搜索框
def down_box():
    # 平台
    channel_data = conf_fun.connect_mysql_operation(scheduling_sql.channel_sql,type='dict')
    # 站点
    site_data = conf_fun.connect_mysql_operation(scheduling_sql.site_sql,type='dict')
    # 国家
    country_data = conf_fun.connect_mysql_operation(scheduling_sql.country_sql,type='dict')
    re_list = change_type(channel_data, site_data, country_data)
    return re_list


# 将数据转换为element_ui
def change_type(channel_data, site_data, country_data):
    country_data_list, channel_list, site_list, = [], [], []
    re_list = [country_data_list, channel_list, site_list, ]
    an_list = [country_data, channel_data, site_data]
    print(country_data, channel_data, site_data)
    for_list = ['country', 'platform', 'site', ]
    for index, object_list in enumerate(an_list):
        for channel_dict in object_list:
            q = {}

            q['value'] = channel_dict.get(for_list[index])
            q['label'] = channel_dict.get(for_list[index])
            re_list[index].append(q)

    return re_list


def operating_data_get(data):
    page = data.get('page') if data.get('page') else 1
    page = (int(page) - 1) * 50
    container_num = data.get('container')
    ser_str = ''
    print(53,data)
    for key, value in data.items():
            if key in ['platform', 'site', 'country'] and value:
                ser_str += " AND od.{0} = '{1}'".format(key, value)
    if not ser_str and not container_num:  # 这是默认进来的渲染的页面数据
        default_apply_sql = scheduling_sql.operating_data.format(' AND sc.schedule_date > DATE_SUB(CURDATE(), INTERVAL 15 DAY)', page, "'已回传'")
        no_pass_back_sql = scheduling_sql.operating_no_data.format('', page, "'未回传'")

        print(default_apply_sql)
    elif container_num:  # 这就是搜索
        ser_str += " AND od.container_num = '{0}'".format(container_num)
        default_apply_sql = scheduling_sql.operating_data.format(ser_str, page, "'已回传'")
        no_pass_back_sql = scheduling_sql.operating_no_data.format(ser_str, page, "'未回传'")
    else:
        for key, value in data.items():
            if key in ['platform', 'site', 'country'] and value:
                ser_str += " AND od.{0} = '{1}'".format(key, value)
        default_apply_sql = scheduling_sql.operating_data.format(ser_str, page, "'已回传'")
        no_pass_back_sql = scheduling_sql.operating_no_data.format(ser_str, page, "'未回传'")
    print('68\n\n\n已回传', default_apply_sql)
    print('69\n\n\n未回传', no_pass_back_sql)
    # 未回传的货柜号

    re_data = scheduling_func.conn_sql_select(default_apply_sql)
    re_no_data = scheduling_func.conn_sql_select(no_pass_back_sql)
    # print(re_data)
    return re_data, re_no_data


# # 运营测算文件上传
def upload_file(files, file_path):
    path2 = os.path.join(r'static/operation/operating_data/', file_path, str(files))
    if not os.path.exists(os.path.join(r'static/operation/operating_data/', file_path)):
        os.makedirs(os.path.join(r'static/operation/operating_data/', file_path))
    path = os.path.join(os.getcwd(), path2)
    print('只是路径\n', path)
    with open(path, 'wb') as f:
        for line in files:
            f.write(line)
    return path2


# 运营上传文件识别
def operating_file(files):
    file_path_list = []
    for file in files:
        for key, value in scheduling_settings.operating_data_dict.items():
            if key in str(file):
                print('这是key', key)  # master_upload_file 放到主服务器
                file_path_list.append({key: scheduling_func.master_upload_file(file, value[0])})
                upload_file(file, value[0])
    return file_path_list


# 生成条码
def bar_code_crate(file_path, data_1):
    list_1 = []
    file_name = []
    q = len('X000ZX8T3Z')
    bar_code_file_t = '-'.join(str(data_1.get('file_name')).split('-')[0:-1]) + '-条码.zip'
    bar_code_path = os.path.join(os.getcwd(), 'static/data/operating_data/bar_code/', bar_code_file_t)

    print(bar_code_file_t)
    path = os.path.join(os.getcwd(), 'static/', file_path)
    pd_data = pd.read_excel(path)
    for i in range(pd_data.shape[0]):
        bar_code = pd_data.iloc[i, 7]

        print(bar_code)
        if len(str(bar_code)) == int(q):
            list_1.append(bar_code)
    path = os.path.join(os.getcwd(), 'static/data/tm_data/')
    print('路径\n', path)
    file_name_list = os.listdir(path)

    for bar_code_str in list_1:
        for bar_code_file in file_name_list:
            if bar_code_str in bar_code_file:
                path_test = os.path.join(path, bar_code_file)
                file_name.append(path_test)

    import zipfile

    # 遍历files文件夹下的文件，压缩发送
    print(213, bar_code_path)
    print(file_name)
    # zip_1 = zipfile.ZipFile(bar_code_path , 'w', zipfile.ZIP_DEFLATED) # 新建一个zip文件
    zip_1 = zipfile.ZipFile(bar_code_path, 'w', zipfile.ZIP_DEFLATED)

    for f in file_name:
        zip_1.write(f)
    zip_1.close()
    # bar_code_path = os.path.join(os.getcwd(), 'static/data/operating_data/bar_code/', bar_code_file_t)
    master_path = os.path.join(r'static/operation/bar_code/%s' % (bar_code_file_t), bar_code_file_t)
    url = 'https://www.beyoung.group/file_upload/'
    data = {'path': master_path}
    # with open(bar_code_path, 'r',encoding='utf-8') as f:
    print('\n', zip_1, data)
    res = requests.post(url, data, files={'file': open(bar_code_path, 'rb')})
    print(res.text)
    master_path = os.path.join(r'operation/bar_code/%s/%s' % (bar_code_file_t, bar_code_file_t), bar_code_file_t)
    return master_path

    # 更新运营上传资料


def update_operating_data(data):
    update_where_str = ''
    update_str = ''
    establish__str = ''

    localtime = time.strftime("%Y-%m-%d", time.localtime())

    for key, value in data.items():
        if key == 'file_name':
            file_path_list = operating_file(data.getlist('file_name'))

            print(165, file_path_list)
            for file in file_path_list:
                print(173,'--',file)
                key = list(file)[0]
                sql_value = scheduling_settings.operating_data_dict.get(key)

                file_path = file.get(key)
                if key in ['建仓信息确认表','海外仓信息确认表']:

                    bar_code_path,bar_code_path_new,error_msg = post_generation.create_post_generation(data)  # 这是条码
                    if error_msg:
                        return { 'msg':error_msg}
                    print(bar_code_path, '------这是产品条码',bar_code_path_new)
                    date_time_1 = localtime
                    date_time = localtime
                    state_type  = '已审核'
                    state_type_1 ='未审核'
                    if not bar_code_path_new:
                        bar_code_path_new =''
                        date_time =''
                        state_type =''
                    if not bar_code_path:
                        bar_code_path =''
                        date_time_1 =''
                        state_type_1 =''
                    #                    bar_code_path = bar_code_crate(file_path,data)

                    update_str += "{0} = '{1}', {2} ='{3}',{4} ='{5}',{6} = '{7}', {8} ='{9}',{10} ='{11}', " \
                        .format('bar_code', bar_code_path, 'bar_code_date', date_time_1, 'bar_code_state', state_type_1,
                                'bar_code_new', bar_code_path_new, 'bar_code_date_new', date_time,
                                'bar_code_state_new',state_type)

                    establish__str += " {0} = '{1}',{2}= '{3}', {4} ='{5}'," \
                        .format(sql_value[1], localtime, sql_value[2], file_path, sql_value[3], '未审核')

                elif key == '下单表':
                    update_str += " {0} = '{1}',{2}= '{3}', {4} ='{5}'," \
                        .format(sql_value[1], localtime, sql_value[2], file_path, sql_value[3], '已审核')
                elif key == '条码附件' and '产品条码附件' not in file_path:
                   update_str += " {0} = '{1}',{2}= '{3}', {4} ='{5}'," \
                       .format(sql_value[1], localtime, sql_value[2], file_path, sql_value[3], '已审核')
                elif key == '产品条码附件' and '产品条码附件' in file_path:
                   update_str += " {0} = '{1}',{2}= '{3}', {4} ='{5}'," \
                       .format(sql_value[1], localtime, sql_value[2], file_path, sql_value[3], '已审核')
                elif key =='箱贴':
                    update_str += " {0} = '{1}',{2}= '{3}', {4} ='{5}'," \
                        .format(sql_value[1], localtime, sql_value[2], file_path, sql_value[3], '未审核')
                else:
                    update_str +=''


        else:
            update_where_str += " AND {0} = '{1}'".format(key, value)
    conn_sql_func(update_str, update_where_str)
    if establish__str:
        conn_sql_func(establish__str, update_where_str)
    return { 'msg':''}

def conn_sql_func(update_str, update_where_str):
    update_str = update_str.rstrip(', ')
    update_file_sql = scheduling_sql.update_file_sql.format(update_str, update_where_str)
    print('\n', update_file_sql, '\n')
    conf_fun.connect_mysql_operation(update_file_sql)


class Operating_Data_upload(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        data = request.GET
        re_list = down_box()
        re_data, re_no_data = operating_data_get(data)
        self.ret['re_list'] = re_list
        self.ret['re_data'] = re_data
        self.ret['re_no_data'] = re_no_data
        return Response(self.ret)

    def create(self, request):
        data = request.data
        # print(data)
        ret = update_operating_data(data)
        if ret.get('msg'):
            self.ret['code'] =400
            self.ret['msg'] = ret.get('msg')
        return Response(self.ret)

    def alter(self, request):
        # 这是用的修改审批
        data = request.data
        print(data)
        id = data.get('id')
        updata_str = " "
        for key,value in data.items():
            if key not in ['id']:
                updata_str += " %s ='%s' , "%(key,value)

        updata_str = updata_str.rstrip(' , ')
        update_sql = " update operating_data set {0} where {1}".format(updata_str , " id ='%s'"%(id))
        print(update_sql)


        conf_fun.connect_mysql_operation(update_sql)

        # 修改 老系统的资料审核
        return  Response(self.ret)

    def delete(self, request):
        pass

# 修改老系统的治疗审核
def alter_old_system(data):
    id = data.get('id')
    establish_warehouse_state = data.get('establish_warehouse_state') #建仓信息确认表
    box_stuck_state = data.get('box_stuck_state') # 箱贴
    bar_code_state = data.get('bar_code_state') # 条码
    bar_code_state_new = data.get('bar_code_state_new') # 新条码

    ser_sql = " select * from operating_data where id='%s'" % (id)
    re_data = conf_fun.connect_mysql_operation(ser_sql, type='dict')
    if re_data:
        re_data = re_data[0]
    detail_data_name = ''

    if establish_warehouse_state:
        establish_warehouse_path = re_data.get('establish_warehouse')
        detail_data_name = establish_warehouse_path.split('/')[-1]
    elif box_stuck_state:
        box_stuck_state_path = re_data.get('box_stuck')
        detail_data_name =  box_stuck_state_path.split('/')[-1]
    elif bar_code_state_new:
        bar_code_state_path = re_data.get('bar_code_state_new')
        detail_data_name = bar_code_state_path.split('/')[-1]

    container_num = re_data.get('container_num')
    site = re_data.get('site')
    country = re_data.get('country')
    code_hd = re_data.get('calculation_file_path').split('/')[-1].split('-')[1]
    file_name = "%s-%s%s-%s"%(container_num,site,country,code_hd)
    sql6 = "select * from second_audit as sa where sa.file_name='{0}' and sa.detail_data_name= '{0}'".format(file_name,detail_data_name)
    response6 = scheduling_settings.connect_mysql_master(sql_text=sql6, dbs='container_data')

    if len(response6) > 0:
        sql4 = "update second_audit as sa set sa.status='1' where " \
               "sa.file_name='{0}' and sa.detail_data_name='{1}' ".format(file_name,detail_data_name)
        scheduling_settings.connect_mysql_master(sql_text=sql4, dbs='container_data')

def connect_mysql(sql_text, dbs='operation', type='tuple'):
    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_',
                           db=dbs)
    if type == 'tuple':
        cursor = conn.cursor()
    else:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_text)
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return response


# 颜劲-海外仓建仓信息确认表-获取sku
def oversea_location_sku(request):
    country = request.GET.get('country')
    site = request.GET.get('site')

    sql = "select sku from commodity_information where country='{}' and site='{}' order by sku"
    sql = sql.format(country, site)
    res = connect_mysql(sql, type='dict')
    return JsonResponse({"code": 200, "data": res})


# 颜劲-海外仓建仓信息确认表-生成文件
def oversea_location_create_file(request):
    user_name = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[0]
    container_num = request.POST.get('container_num')
    country = request.POST.get('country')
    site = request.POST.get('site')
    sku = request.POST.getlist('sku')
    nums = request.POST.getlist('nums')
    if country in ['英国', '法国', '德国', '意大利', '西班牙']:
        country = '欧洲'

    if country == '美国':
        country_en = 'US'
    elif country == '加拿大':
        country_en = 'CA'
    elif country == '墨西哥':
        country_en = 'MX'
    elif country == '欧洲':
        country_en = 'EU'
    elif country == '日本':
        country_en = 'JP'
    elif country == '澳洲':
        country_en = 'AU'

    sku_data = ''
    nums_data = ''
    for i in range(len(sku)):
        sku_data += sku[i] + ','
        nums_data += nums[i] + ','
    sku_data = sku_data[:-1]
    nums_data = nums_data[:-1]
    urls = 'http://www.beyoung.group/oversea_location_api/'
    data = {"sku_data": sku_data, "nums_data": nums_data, "user_name": user_name, "container_name": container_num,
            "site": site, "country": country_en}
    res = requests.post(url=urls, data=data)
    res_data = json.loads(res.text)
    if res_data['code'] == 200:
        dates = str(datetime.strptime(str(date.today()), '%Y-%m-%d') + timedelta(days=-1))
        sql = "update operating_data set establish_warehouse_state='{}',establish_warehouse_date='{}'," \
              "establish_warehouse='{}',bar_code_date='{}',bar_code='{}',bar_code_state='{}' where container_num='{}' " \
              "and site='{}' and country='{}'"
        sql = sql.format('未审核', dates, res_data['establish_warehouse'], dates, res_data[''], '未审核', container_num
                         , site, country)
        connect_mysql(sql)
        return JsonResponse({"code": 200, "msg": "上传成功!"})
