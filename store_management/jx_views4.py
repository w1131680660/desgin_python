from urllib.parse import unquote
from django.http import JsonResponse
import pymysql
import os
import requests
import time
import datetime
import json
from multiprocessing import Process, Queue
from settings import conf_fun
#
#
# # 连接主系统数据库
# def connect_mysql1(sql_text, dbs='reports', type='tuple'):
#     conn = pymysql.Connect(host='106.53.250.215', port=3306, user='beyoungsql', passwd='Bymy2021.', db=dbs)
#     if type == 'tuple':
#         cursor = conn.cursor()
#     else:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql_text)
#     response = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return response
#
#
# # 连接总数据库
# def connect_mysql(sql_text, dbs='operation', type='tuple'):
#     conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_', db=dbs)
#     if type == 'tuple':
#         cursor = conn.cursor()
#     else:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql_text)
#     response = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return response


# 获取一个表的所有字段名
def get_columns(request):
    table_name = request.GET.get("table_name", "")
    select_sql = "select * from %s limit 1;" % table_name
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, type='dict')[0]
    key_data = ""
    value_date = ""
    for key in select_res:
        key_data += key + ","
        value_date += "'%s',"
    res = {"key": key_data, "value": value_date}
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割-品牌维护


# 店铺管理-品牌维护-获取上传弹窗数据
def get_data_brand(request):
    """
    从店铺信息表中获取
    """
    print("-----店铺管理-品牌维护-获取上传弹窗数据------")
    platform_list = []
    country_list = []
    site_list = []
    store_list = []

    select_sql = "select platform,country,site,name_shop from store_information;"
    select_res = conf_fun.connect_mysql_operation(select_sql)

    for item in select_res:
        if item[0] not in platform_list:
            platform_list.append(item[0])
        if item[1] not in platform_list:
            country_list.append(item[1])
        if item[2] not in platform_list:
            site_list.append(item[2])
        if item[3] not in platform_list:
            store_list.append(item[3])

    res = {"code": 200, "platform_list": platform_list, "country_list": country_list,
           "site_list": site_list, "store_list": store_list}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-品牌维护-确认上传
def insert_brand(request):
    """写进数据库"""
    print("-----------店铺管理-品牌维护-确认上传: ", request.POST)
    brand_platform = request.POST.get("brand_platform", "")
    brand_country = request.POST.get("brand_country", "")
    brand_site = request.POST.get("brand_site", "")
    brand_store = request.POST.get("brand_store", "")
    brand_name = request.POST.get("brand_name", "")
    file_list = request.FILES.getlist("file", "")
    print("file_list: ", file_list)

    person = "难搞哦"
    now_time = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(hours=8), "%Y-%m-%d %H:%M")
    print("now_time: ", now_time)

    for file in file_list:
        # 上传文件
        # brand/站点国家/文件名
        urls = 'https://www.beyoung.group/file_upload/'
        site_country = brand_site + "_" + brand_country
        path = {"path": "operation/brand/" + site_country}
        files = {'file': file}
        post_res = requests.post(url=urls, files=files, data=path)
        post_data = json.loads(post_res.text)
        if post_data['code'] != 200:
            res = {"code": 4041, "msg": "上传失败"}
            return JsonResponse(res)

        # 插入数据库
        insert_sql = "insert into brand(platform,store,site,country,brand,file_path,person,brand_time) " \
                     "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                     % (brand_platform, brand_store, brand_site, brand_country,
                        brand_name, path['path'] + "#" + file.name, person, now_time)
        conf_fun.connect_mysql_operation(sql_text=insert_sql)

    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-品牌维护-获取侧边栏
def get_select_brand(request):
    """
    从店铺信息表中获取，某一渠道下的所有国家，某一国家下所有站点，一一对应
    """
    print("------店铺管理-品牌维护-获取侧边栏-----")
    platform_list = []
    country_list = []
    site_list = []

    select_sql = "select platform,country,site from store_information;"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(select_sql)
    print("select_res: ", select_res)

    # 分级处理
    """
    [1,2,3]
    [ [1,1] , [2,2] , [3] ]
    [ [ [1],[1,1] ] , [ [2],[2,2] ] , [ [3] ] ]
    """
    for item in select_res:
        try:
            platform_index = platform_list.index(item[0])
            # ==============================================
            try:
                country_index = country_list[platform_index].index(item[1])
                # ==============================================
                try:
                    site_list[platform_index][country_index].index(item[2])
                except IndexError:
                    site_list[platform_index].append([item[2]])
                except ValueError:
                    site_list[platform_index][country_index].append(item[2])
                # ==============================================
            except IndexError:
                country_list.append([item[1]])
                site_list.append([[item[2]]])
            except ValueError:
                country_list[platform_index].append(item[1])
                site_list[platform_index].append([item[2]])
            # ==============================================
        except ValueError:
            platform_list.append(item[0])
            country_list.append([item[1]])
            site_list.append([[item[2]]])

    print("platform_list: ", platform_list)
    print("country_list: ", country_list)
    print("site_list: ", site_list)

    # res = {"code": 200, "platform_list": ["Amazon", "Shopee"],
    #        "country_list": [["美国", "加拿大"], ["日本"]], "site_list": [[["胤佑", "爱瑙"], ["爱瑙"]], [["中睿"]]]}

    res = {"code": 200, "platform_list": platform_list, "country_list": country_list, "site_list": site_list}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-品牌维护-查询
def select_brand(request):
    """
    查询表里的数据
    """
    print("-----------店铺管理-品牌维护-查询: ", request.GET)
    brand_platform = request.GET.get("brand_platform", "")
    brand_country = request.GET.get("brand_country", "")
    brand_site = request.GET.get("brand_site", "")
    page = int(request.GET.get("page", ""))

    select_sql = "select * from brand where id!=''"
    if brand_platform:
        select_sql += " and platform='" + brand_platform + "'"
    if brand_country:
        select_sql += " and country='" + brand_country + "'"
    if brand_site:
        select_sql += " and site='" + brand_site + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    res_data = conf_fun.connect_mysql_operation(sql_text=select_sql)

    # 总行数
    all_number = len(res_data)
    # 分页
    if page:
        page_start = int(page) * 50 - 50
        page_end = int(page) * 50
        res_data = res_data[page_start:page_end]
    res = {"code": 200, "data": res_data, "all_number": all_number}
    print("res: ", res)
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割-申诉


# 店铺管理-申诉-新增2.0
def insert_complain(request):
    print("-----------店铺管理-申诉-确认上传: ", request.POST)
    complain_platform = request.POST.get("complain_platform", "")
    complain_country = request.POST.get("complain_country", "")
    complain_site = request.POST.get("complain_site", "")
    complain_case = request.POST.get("complain_case", "")
    detail_info = request.POST.get("detail_info", "")
    complain_type = request.POST.get("complain_type", "")
    file_list = request.FILES.getlist("file_list", "")
    print("file_list: ", file_list)

    token = request.session.get('UUID_KEY')
    if token:
        select_user_name_sql = "select real_name from userinfo where token='%s';" % token
        user_name = conf_fun.connect_mysql_operation(sql_text=select_user_name_sql)[0][0]
    else:
        user_name = "工具人1"
    now_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    print("now_time: ", now_time)

    # 存入文件
    save_path = ""
    urls = "https://www.beyoung.group/file_upload/"
    path = {"path": "operation/complain/" + complain_platform + "/" + complain_country + "/" + complain_site + "/"}
    for file in file_list:
        files = {'file': file}
        post_res = requests.post(url=urls, files=files, data=path)
        post_data = json.loads(post_res.text)
        if post_data['code'] != 200:
            res = {"code": 4041, "msg": file.name + " 上传失败"}
            return JsonResponse(res)
        # 插入数据库
        save_path += path['path'] + "#" + file.name + "@"
    save_path = save_path[:-1]
    insert_sql = "insert into complain(platform,site,country,case_code,complain_type," \
                 "detail_info,file_path,person,complain_time) " \
                 "values('%s','%s','%s','%s','%s','%s','%s','%s','%s');" \
                 % (complain_platform, complain_site, complain_country, complain_case,
                    complain_type, detail_info, save_path, user_name, now_time)
    conf_fun.connect_mysql_operation(sql_text=insert_sql)

    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-申诉-查询2.0
def select_complain(request):
    print("-----------店铺管理-申诉-查询: ", request.GET)
    complain_platform = request.GET.get("complain_platform", "")
    complain_country = request.GET.get("complain_country", "")
    complain_site = request.GET.get("complain_site", "")
    start_time = request.GET.get("start_time", "")
    end_time = request.GET.get("end_time", "")
    key_word = request.GET.get("key_word", "")
    page = int(request.GET.get("page", ""))

    if end_time:
        end_time_next_date = datetime.datetime.strftime(
            datetime.datetime.strptime(end_time, "%Y-%m-%d") + datetime.timedelta(days=1), "%Y-%m-%d")

    select_sql = "select * from complain where id!=''"
    if complain_platform:
        select_sql += " and platform='" + complain_platform + "'"
    if complain_country:
        select_sql += " and country='" + complain_country + "'"
    if complain_site:
        select_sql += " and site='" + complain_site + "'"
    if start_time:
        select_sql += " and complain_time>'" + start_time + "'"
    if end_time:
        select_sql += " and complain_time<'" + end_time_next_date + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    res_data = conf_fun.connect_mysql_operation(sql_text=select_sql)
    print("res_data: ", res_data)

    if key_word and res_data:
        middle_data = []
        for item in res_data:
            print("item: ", item)
            print("key_word: ", key_word)
            print("item[5]: ", item[5])
            print("item[6]: ", item[6])
            if key_word in item[5] or key_word in item[6]:
                middle_data.append(item)
        res_data = middle_data

    # 总行数
    all_number = len(res_data)
    # 分页
    if page:
        page_start = page * 50 - 50
        page_end = page * 50
        res_data = res_data[page_start:page_end]
    res = {"code": 200, "data": res_data, "all_number": all_number}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-申诉-编辑
def update_complain(request):
    print("-----------店铺管理-申诉-编辑: ", request.POST)
    complain_id = request.POST.get("complain_id", "")
    complain_platform = request.POST.get("complain_platform", "")
    complain_country = request.POST.get("complain_country", "")
    complain_site = request.POST.get("complain_site", "")
    detail_info = request.POST.get("detail_info", "")
    insert_detail_info = request.POST.get("insert_detail_info", "")

    insert_detail_info = detail_info + "\n" + insert_detail_info

    file_list = request.FILES.getlist("file_list", "")
    print("file_list: ", file_list)

    token = request.session.get('UUID_KEY')
    if token:
        select_user_name_sql = "select real_name from userinfo where token='%s';" % token
        user_name = conf_fun.connect_mysql_operation(sql_text=select_user_name_sql)[0][0]
    else:
        user_name = "工具人1"
    now_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    print("now_time: ", now_time)

    # 查询原来的文件路由
    select_save_path_sql = "select file_path from complain where id='%s';" % complain_id
    select_save_path_res = conf_fun.connect_mysql_operation(sql_text=select_save_path_sql)[0][0]
    mark = 0
    if len(select_save_path_res) == 0:
        new_save_path = ""
        mark = 1
    else:
        new_save_path = select_save_path_res

    # 存入文件
    urls = "https://www.beyoung.group/file_upload/"
    path = {"path": "operation/complain/" + complain_platform + "/" + complain_country + "/" + complain_site + "/"}
    for file in file_list:
        files = {'file': file}
        post_res = requests.post(url=urls, files=files, data=path)
        post_data = json.loads(post_res.text)
        if post_data['code'] != 200:
            res = {"code": 4041, "msg": file.name + " 上传失败"}
            return JsonResponse(res)
        # 拼接新的文件路由
        if mark == 0:
            new_save_path += "@" + path["path"] + "#" + file.name
        else:
            new_save_path += path["path"] + "#" + file.name + "@"
        if mark == 1:
            new_save_path = new_save_path[:-1]

    # 数据库
    update_sql = "update complain set detail_info='%s',file_path='%s',person='%s',complain_time='%s' where id='%s';" \
                 % (insert_detail_info, new_save_path, user_name, now_time, complain_id)
    print("update_sql: ", update_sql)
    conf_fun.connect_mysql_operation(sql_text=update_sql)

    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-申诉-删除
def delete_complain(request):
    print("-------店铺管理-申诉-删除: ", request.GET)
    complain_id = request.GET.getlist("complain_id[]", "")
    for complain_single_id in complain_id:
        delete_sql = "delete from complain where id='%s';" % complain_single_id
        print("delete_sql: ", delete_sql)
        conf_fun.connect_mysql_operation(sql_text=delete_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-申诉-删除文件
def delete_file_complain(request):
    print("-------店铺管理-申诉-删除文件: ", request.GET)
    complain_id = request.GET.get("complain_id", "")
    delete_file_path_list = request.GET.getlist("file_path_list[]", "")

    select_save_file_path_sql = "select file_path from complain where id='%s';" % complain_id
    select_save_file_path_res = conf_fun.connect_mysql_operation(sql_text=select_save_file_path_sql)[0][0]
    print("select_save_file_path_res: ", select_save_file_path_res)
    save_file_path_list = select_save_file_path_res.split("@")
    print("save_file_path_list: ", save_file_path_list)

    for delete_file_path_item in delete_file_path_list:
        for save_file_path_item in save_file_path_list:
            if save_file_path_item == delete_file_path_item:
                save_file_path_list.remove(delete_file_path_item)

    new_delete_file_path = "@".join(save_file_path_list)

    update_sql = "update complain set file_path='%s' where id='%s';" % (new_delete_file_path, complain_id)
    print("update_sql: ", update_sql)
    conf_fun.connect_mysql_operation(sql_text=update_sql)

    res = {"code": 200}
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割-差评管理


# 店铺管理-差评管理-查询2.0
def select_negative_comment_two(request):
    print("-----------店铺管理-差评管理-查询: ", request.GET)
    print("开始时间: ", time.time())
    negative_platform = request.GET.get("negative_platform", "")
    negative_country = request.GET.get("negative_country", "")
    negative_site = request.GET.get("negative_site", "")

    sku = request.GET.get("sku", "")
    status = request.GET.get("status", "")
    page = int(request.GET.get("page", "1"))

    res_data = []

    yesterday_date = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y.%m.%d")

    # 根据中文站点获取英文
    # select_negative_site_change_sql = "select * from area_contrast where area_cn='%s';" % negative_site
    # select_negative_site_change_res = conf_fun.connect_mysql_operation(sql_text=select_negative_site_change_sql, type='dict')
    # if len(select_negative_site_change_res) > 0:
    #     negative_site_change = select_negative_site_change_res[0]['area']
    # else:
    #     negative_site_change = negative_site

    # 查询sku当前页面的差评
    if sku:
        select_front_display_by_sku_sql = "select * from front_display where SKU='%s'  and dates>='%s' " \
                                          "and country='%s' and area='%s' order by id desc;" \
                                             % (sku, yesterday_date, negative_country, negative_site)
        print("查询front_display数据语句: ", select_front_display_by_sku_sql)
        select_front_display_by_sku_res = conf_fun.connect_mysql_operation(sql_text=select_front_display_by_sku_sql, type='dict')

        # 渠道，站点，国家，sku，asin，客户名，评论星级，评论发布时间，网页链接，差评链接
        middle_list = []

        display_sku_list = []  # 用来判断是否有重复

        for front_display_item in select_front_display_by_sku_res:
            only_list = [front_display_item['country'], front_display_item['area'], front_display_item['SKU']]
            if only_list not in display_sku_list:
                middle_list.append(front_display_item)
                display_sku_list.append(only_list)

        # 已得到所有不重复的数据

        # 将多条差评拆开,获取每条差评的用户名，评论星级，评论时间，页面链接，差评连接
        for middle_list_item in middle_list:

            # 将英文站点转换为中文
            # select_site_change_sql = "select * from area_contrast where area='%s';" % middle_list_item['area']
            # select_site_change_res = conf_fun.connect_mysql_operation(sql_text=select_site_change_sql, type='dict')
            # if len(select_site_change_res) > 0:
            #     negative_site_change = select_site_change_res[0]['area_cn']
            # else:
            #     negative_site_change = negative_site

            # 如果有差评
            if middle_list_item['bad_review'] != "0" and "." in middle_list_item['dates']:

                try:
                    # 用户名
                    comment_user_list = middle_list_item['link_break'].split(",")
                    # 评论星级
                    comment_star_list = middle_list_item['person_bad'].split("/")
                    # 评论时间
                    comment_date_list = middle_list_item['date_bad_review'].split("/")
                    # 差评连接
                    comment_url_list = middle_list_item['bad_link'].split(",")
                except:
                    continue

                for i in range(len(comment_user_list)):
                    if not comment_user_list[i]:
                        continue
                    # 渠道，站点，国家，sku，asin，客户名，评论星级，评论发布时间，网页链接，差评链接，状态，处理时间，处理人
                    res_data.append(["Amazon", negative_site,
                                     middle_list_item['country'], middle_list_item['SKU'],
                                     middle_list_item['ASIN'], middle_list_item['dates'], comment_user_list[i],
                                     comment_star_list[i], comment_date_list[i],
                                     middle_list_item['URL'], comment_url_list[i],
                                     "未处理", "", ""])
    else:
        # 查询满足国家，站点的今天或者昨天的差评数据，
        select_front_display_sql = "select * from front_display where country='%s' and area='%s' " \
                                   "and dates>='%s' order by id desc;" \
                                   % (negative_country, negative_site, yesterday_date)
        print("查询front_display表的SQL语句: ", select_front_display_sql)
        select_front_display_res = conf_fun.connect_mysql_operation(sql_text=select_front_display_sql, type='dict')

        # 渠道，站点，国家，sku，asin，客户名，评论星级，评论发布时间，网页链接，差评链接

        middle_list = []

        display_sku_list = []  # 用来判断是否有重复

        for front_display_item in select_front_display_res:
            only_list = [front_display_item['country'], front_display_item['area'], front_display_item['SKU']]
            if only_list not in display_sku_list:
                middle_list.append(front_display_item)
                display_sku_list.append(only_list)

        # 已得到所有不重复的数据

        # 将多条差评拆开,获取每条差评的用户名，评论星级，评论时间，页面链接，差评连接
        for middle_list_item in middle_list:
            # 如果有差评
            if middle_list_item['bad_review'] != "0" and "." in middle_list_item['dates']:
                # 数据清洗
                if middle_list_item['person_bad'] == "0/":
                    continue
                try:
                    # 用户名
                    comment_user_list = middle_list_item['link_break'].split(",")
                    # 评论星级
                    comment_star_list = middle_list_item['person_bad'].split("/")
                    # 评论时间
                    comment_date_list = middle_list_item['date_bad_review'].split("/")
                    # 差评连接
                    comment_url_list = middle_list_item['bad_link'].split(",")
                except:
                    continue

                for i in range(len(comment_user_list)):
                    if not comment_user_list[i] or not comment_star_list[i] \
                            or not comment_date_list[i] or not comment_url_list[i]:
                        continue
                    # 渠道，站点，国家，sku，asin，爬取时间，客户名，评论星级，评论发布时间，网页链接，差评链接
                    res_data.append(["Amazon", negative_site,
                                     middle_list_item['country'], middle_list_item['SKU'],
                                     middle_list_item['ASIN'], middle_list_item['dates'], comment_user_list[i],
                                     comment_star_list[i], comment_date_list[i],
                                     middle_list_item['URL'], comment_url_list[i], "未处理",
                                     "", ""])

    # 插入数据库
    res_data_one = []
    res_data_two = []

    # print("锚点1")
    # if len(res_data) > 0:
    #     print("抽查第一条: ", res_data[0])
    #     if len(res_data) > 1:
    #         print("抽查中间一条: ", res_data[len(res_data) // 2])
    #     print("抽查最后一条: ", res_data[-1])

    if not status:
        # 没有状态

        # 总行数
        all_number = len(res_data)
        # 分页
        if page:
            page_start = page * 20 - 20
            page_end = page * 20
            res_data = res_data[page_start:page_end]
        for insert_item in res_data:
            # 查询数据库中有没有该数据 渠道，站点，国家，sku，asin，客户名，评论星级，爬取时间，评论发布时间，网页链接，差评链接，处理情况，处理时间，处理人
            select_exist_sql = "select * from negative_comment where site='%s' " \
                               "and country='%s' and sku='%s' and comment_time='%s';" \
                               % (insert_item[1], insert_item[2], insert_item[3], insert_item[8])
            # print("查询数据库中有没有该数据", select_exist_sql)
            select_exist_res = conf_fun.connect_mysql_operation(sql_text=select_exist_sql)
            # insert_item = [渠道，站点，国家，sku，asin，爬取时间，客户名，评论星级，评论发布时间，网页链接，差评链接，处理情况，处理时间，处理人]
            if len(select_exist_res) > 0:
                if select_exist_res[0][-3] == "处理中":
                    insert_item = insert_item[:-3]
                    insert_item.extend(list(select_exist_res[0])[-3:])
                elif select_exist_res[0][-3] == "已处理":
                    # 将数据库中数据状态改为未处理
                    update_status_sql = "update negative_comment set status='未处理',spider_date='%s'  " \
                                        "where platform='%s' and site='%s' and country='%s' " \
                                        "and sku='%s' and comment_time='%s';" \
                                        % (insert_item[5], insert_item[0], insert_item[1], insert_item[2],
                                           insert_item[3], insert_item[8])
                    # print("将数据库中数据状态改为未处理", update_status_sql)
                    conf_fun.connect_mysql_operation(sql_text=update_status_sql)
                    # 将更新后的数据替换原数据
                    # insert_item = list(select_exist_res[0])[1:]
                    # insert_item[-3] = '未处理'
                # else:
                    # insert_item = list(select_exist_res[0])[1:]
                res_data_one.append(insert_item)
            else:
                # 没有
                insert_sql = 'insert into negative_comment(platform,site,country,sku,asin,spider_date,user_name,' \
                             'class,comment_time,web_path,comment_path,status) ' \
                             'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' \
                             % (insert_item[0], insert_item[1], insert_item[2], insert_item[3],
                                insert_item[4], insert_item[5], insert_item[6], insert_item[7], insert_item[8],
                                insert_item[9], insert_item[10], "未处理")
                # print("将数据库中数据状态改为未处理", insert_sql)
                conf_fun.connect_mysql_operation(sql_text=insert_sql)
                res_data_one.append(insert_item)

            # print("数据状态保持: ", insert_item)

        for res_data_item in res_data_one:
            res_data_two.append(res_data_item)

    else:
        # 有状态
        for insert_item in res_data:
            # 查询数据库中有没有该数据 渠道，站点，国家，sku，asin，客户名，评论星级，爬取时间，评论发布时间，网页链接，差评链接，处理情况，处理时间，处理人
            select_exist_sql = "select * from negative_comment where site='%s' " \
                               "and country='%s' and sku='%s' and comment_time='%s';" \
                               % (insert_item[1], insert_item[2], insert_item[3], insert_item[8])
            select_exist_res = conf_fun.connect_mysql_operation(sql_text=select_exist_sql)
            # res_data = [渠道，站点，国家，sku，asin，爬取时间，客户名，评论星级，评论发布时间，网页链接，差评链接，处理情况，处理时间，处理人]
            if len(select_exist_res) > 0:
                if select_exist_res[0][-3] == "处理中":
                    insert_item = insert_item[:-3]
                    insert_item.extend(list(select_exist_res[0])[-3:])
                elif select_exist_res[0][-3] == "已处理":
                    # 将数据库中数据状态改为未处理
                    update_status_sql = "update negative_comment set status='未处理',spider_date='%s'  " \
                                        "where platform='%s' and site='%s' and country='%s' " \
                                        "and sku='%s' and comment_time='%s';" \
                                        % (insert_item[5], insert_item[0], insert_item[1], insert_item[2],
                                           insert_item[3], insert_item[8])
                    conf_fun.connect_mysql_operation(sql_text=update_status_sql)
                    # 将更新后的数据替换原数据
                #     insert_item = list(select_exist_res[0])[1:]
                #     insert_item[-3] = '未处理'
                # else:
                #     insert_item = list(select_exist_res[0])[1:]
                res_data_one.append(insert_item)
            else:
                # 没有
                insert_sql = 'insert into negative_comment(platform,site,country,sku,asin,spider_date,user_name,' \
                             'class,comment_time,web_path,comment_path,status) ' \
                             'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' \
                             % (insert_item[0], insert_item[1], insert_item[2], insert_item[3],
                                insert_item[4], insert_item[5], insert_item[6], insert_item[7], insert_item[8],
                                insert_item[9], insert_item[10], "未处理")
                conf_fun.connect_mysql_operation(sql_text=insert_sql)
                res_data_one.append(insert_item)

        # 状态筛选条件
        for res_data_item in res_data_one:
            if res_data_item[-3] == status:
                res_data_two.append(res_data_item)

        # 总行数
        all_number = len(res_data_two)
        # 分页
        if page:
            page_start = page * 20 - 20
            page_end = page * 20
            res_data_two = res_data_two[page_start:page_end]

    # 获取所有sku
    all_sku_list = []
    for item in res_data_two:
        if item[3] not in all_sku_list:
            all_sku_list.append(item[3])

    print("结束时间: ", time.time())
    res = {"code": 200, "data": res_data_two, "all_number": all_number, "all_sku_list": all_sku_list}
    return JsonResponse(res)


# 查询耗时sql操作
def insert_negative_comment(q, res_data):
    for insert_item in res_data:
        # 查询数据库中有没有该数据 渠道，站点，国家，sku，asin，客户名，评论星级，爬取时间，评论发布时间，网页链接，差评链接，处理情况，处理时间，处理人
        select_exist_sql = "select * from negative_comment where site='%s' " \
                           "and country='%s' and sku='%s' and comment_time='%s';" \
                           % (insert_item[1], insert_item[2], insert_item[3], insert_item[8])
        select_exist_res = conf_fun.connect_mysql_operation(sql_text=select_exist_sql)
        # res_data = [渠道，站点，国家，sku，asin，爬取时间，客户名，评论星级，评论发布时间，网页链接，差评链接，处理情况，处理时间，处理人]
        if len(select_exist_res) > 0:
            if select_exist_res[0][-3] == "处理中":
                insert_item = list(select_exist_res[0])[1:]
            elif select_exist_res[0][-3] == "已处理":
                # 将数据库中数据状态改为未处理
                update_status_sql = "update negative_comment set status='未处理',spider_date='%s'  " \
                                    "where platform='%s' and site='%s' and country='%s' " \
                                    "and sku='%s' and comment_time='%s';" \
                                    % (insert_item[5], insert_item[0], insert_item[1], insert_item[2],
                                       insert_item[3], insert_item[8])
                conf_fun.connect_mysql_operation(sql_text=update_status_sql)
                # 将更新后的数据替换原数据
                insert_item = list(select_exist_res[0])[1:]
                insert_item[-3] = '未处理'
            else:
                insert_item = list(select_exist_res[0])[1:]
            # res_data_one.append(insert_item)
            q.put(insert_item)
        else:
            # 没有
            insert_sql = 'insert into negative_comment(platform,site,country,sku,asin,spider_date,user_name,' \
                         'class,comment_time,web_path,comment_path,status) ' \
                         'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' \
                         % (insert_item[0], insert_item[1], insert_item[2], insert_item[3],
                            insert_item[4], insert_item[5], insert_item[6], insert_item[7], insert_item[8],
                            insert_item[9], insert_item[10], "未处理")
            conf_fun.connect_mysql_operation(sql_text=insert_sql)
            # res_data_one.append(insert_item)
            q.put(insert_item)


# 店铺管理-差评管理-查询
def select_negative_comment(request):
    print("-----------店铺管理-差评管理-查询: ", request.GET)
    negative_platform = request.GET.get("negative_platform", "")
    negative_country = request.GET.get("negative_country", "")
    negative_site = request.GET.get("negative_site", "")

    sku = request.GET.get("sku", "")
    status = request.GET.get("status", "")
    page = int(request.GET.get("page", "1"))

    target_date = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=7), "%Y-%m-%d")
    target_date_list = target_date.split("-")
    target_date1 = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=7), "%Y.%m.%d")
    # mark = 0

    # 转换站点
    select_area_contrast_sql = "select area from area_contrast where area_cn='%s';" % negative_site
    print("select_area_contrast_sql: ", select_area_contrast_sql)
    select_area_contrast_res = conf_fun.connect_mysql_operation(sql_text=select_area_contrast_sql)
    if len(negative_site) == 0:
        pass
    else:
        change_negative_site = select_area_contrast_res[0][0]

    # 查询front_display表
    select_front_display_sql = "select * from front_display where dates>='" + target_date1 + "'"
    if negative_country:
        select_front_display_sql += " and country='" + negative_country + "'"
    if negative_site:
        select_front_display_sql += " and area='" + change_negative_site + "'"
    select_front_display_sql += ";"
    select_front_display_res = conf_fun.connect_mysql_operation(sql_text=select_front_display_sql, type='dict')
    for front_display_item in select_front_display_res:
        try:
            # print("查询爬取下来的数据循环写入差评管理表: ", front_display_item)
            # if mark == 1:
            #     break
            # 评论用户列表
            all_negative_user_name_list = front_display_item['link_break'].split(",")[:-1]
            if len(all_negative_user_name_list) != 0:
                # 评论链接列表
                check_bad_link_list = front_display_item['bad_link'].split(",")[:-1]
                # 评论星级列表
                class_list = front_display_item['person_bad'].split("/")[:-1]

                # 评论时间列表
                date_bad_review_list = front_display_item['date_bad_review'].split("/")[:-1]

                for user_name_i in range(len(all_negative_user_name_list)):
                    check_bad_link = check_bad_link_list[user_name_i]
                    check_sql = "select id from negative_comment where comment_path='%s';" % check_bad_link
                    check_res = conf_fun.connect_mysql_operation(sql_text=check_sql)

                    if len(check_res) != 0:
                        # 重复
                        # mark = 1
                        # print("标记: ", mark)
                        break

                    # 转换站点
                    select_area_contrast_sql = "select area_cn from area_contrast where area='%s';" \
                                               % front_display_item['area']
                    select_area_contrast_res = conf_fun.connect_mysql_operation(sql_text=select_area_contrast_sql)

                    insert_sql = "insert into negative_comment(platform,site,country,sku,asin," \
                                 "user_name,class,comment_time,web_path,comment_path,status) " \
                                 "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                                 % ("Amazon", select_area_contrast_res[0][0], front_display_item['country'],
                                    front_display_item['SKU'],
                                    front_display_item['ASIN'], all_negative_user_name_list[user_name_i],
                                    class_list[user_name_i], date_bad_review_list[user_name_i],
                                    front_display_item['URL'], check_bad_link_list[user_name_i], "未处理")
                    print("insert_sql: ", insert_sql)
                    conf_fun.connect_mysql_operation(sql_text=insert_sql)
        except:
            continue

    # 查询negative_comment表
    select_sql = "select * from negative_comment where id!=''"
    if status:
        select_sql += " and status='" + status + "'"
    if negative_platform:
        select_sql += " and platform='" + negative_platform + "'"
    if negative_country:
        select_sql += " and country='" + negative_country + "'"
    if negative_site:
        select_sql += " and site='" + negative_site + "'"
    if sku:
        select_sql += " and sku='" + sku + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    res_data = []
    for item1 in select_res:
        bad_review_time = item1[8]
        try:
            bad_review_year = int(bad_review_time.split("年")[0])
            bad_review_month = int(bad_review_time.split("年")[1].split("月")[0])
            bad_review_day = int(bad_review_time.split("年")[1].split("月")[1].split("日")[0])
            if bad_review_year >= int(
                    target_date_list[0]) and bad_review_month >= int(
                target_date_list[1]) and bad_review_day >= int(
                target_date_list[2]):
                res_data.append(item1)
        except:
            continue

    all_sku_list = []
    for item in res_data:
        if item[4] not in all_sku_list:
            all_sku_list.append(item[4])

    # 总行数
    all_number = len(res_data)
    # 分页
    if page:
        page_start = page * 50 - 50
        page_end = page * 50
        res_data = res_data[page_start:page_end]
    res = {"code": 200, "data": res_data, "all_number": all_number, "all_sku_list": all_sku_list}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-差评管理-导出数据表格改变数据状态(两种)
def update_negative_comment(request):
    print("-----------店铺管理-差评管理-改变数据状态: ", request.GET)
    negative_id_list = request.GET.getlist("negative_id[]", "")
    # 处理中/已处理
    status = request.GET.get("status", "")

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    print("user_info: ", user_info)
    reply_person = user_info.split("@")[0]

    reply_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
                  + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    for negative_id in negative_id_list:
        update_sql = "update negative_comment set status='%s',manage_person='%s',manage_time='%s' " \
                     "where country='%s' and site='%s' and sku='%s' and comment_time='%s';" \
                     % (status, reply_person, reply_time, eval(negative_id)[0], eval(negative_id)[1],
                        eval(negative_id)[2], eval(negative_id)[3])
        print("update_sql: ", update_sql)
        # conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割-Q&A


# 店铺管理-Q&A-从表中获取数据
def select_q_a(request):
    print("-----------店铺管理-Q&A-从表中获取数据: ", request.GET)
    q_a_platform = request.GET.get("q_a_platform", "")
    q_a_country = request.GET.get("q_a_country", "")
    q_a_site = request.GET.get("q_a_site", "")
    status = request.GET.get("status", "")
    page = int(request.GET.get("page", ""))

    select_sql = "select * from q_a where id!=''"
    if status:
        select_sql += " and status='" + status + "'"
    if q_a_platform:
        select_sql += " and platform='" + q_a_platform + "'"
    if q_a_country:
        select_sql += " and country='" + q_a_country + "'"
    if q_a_site:
        select_sql += " and site='" + q_a_site + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    # 总行数
    all_number = len(select_res)
    # 分页
    if page:
        page_start = int(page) * 50 - 50
        page_end = int(page) * 50
        select_res = select_res[page_start:page_end]
    res = {"code": 200, "data": select_res, "all_number": all_number}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-Q&A-改变数据状态
def update_q_a(request):
    print("-----------店铺管理-Q&A-改变数据状态: ", request.GET)
    q_a_id = request.GET.get("q_a_id", "")
    reply_person = "工具人1号"
    reply_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "%Y/%m/%d %H:%M")
                  + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M")
    update_sql = "update q_a set status='%s',reply_person='%s',reply_time='%s' where id='%s';" \
                 % ("已处理", reply_person, reply_time, q_a_id)
    print("update_sql: ", update_sql)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割-邮件预警


# 店铺管理-邮件预警-查询
def select_email_alert(request):
    print("-----------店铺管理-邮件预警-查询: ", request.GET)
    alert_platform = request.GET.get("alert_platform", "")
    alert_country = request.GET.get("alert_country", "")
    alert_site = request.GET.get("alert_site", "")
    alert_type = request.GET.get("alert_type", "")
    page = int(request.GET.get("page", ""))

    select_sql = "select * from email_alert where id!=''"
    if alert_type:
        select_sql += " and alert_type='" + alert_type + "'"
    if alert_platform:
        select_sql += " and alert_platform='" + alert_platform + "'"
    if alert_country:
        select_sql += " and alert_country='" + alert_country + "'"
    if alert_site:
        select_sql += " and alert_site='" + alert_site + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    # 总行数
    all_number = len(select_res)
    # 分页
    if page:
        page_start = int(page) * 50 - 50
        page_end = int(page) * 50
        select_res = select_res[page_start:page_end]
    res = {"code": 200, "data": select_res, "all_number": all_number}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-邮件预警-获取问题类型(已审核/删除待确认)
def get_select_email_alert(request):
    print("-----------店铺管理-邮件预警-获取问题类型(已审核/删除待确认): ", request.GET)
    select_sql = "select alert_type from alert_type where status!='新增待审核';"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    res = {"code": 200, "data": select_res}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-邮件预警-问题类型新增(新增待审核)
def insert_alert_type(request):
    print("-------店铺管理-邮件预警-问题类型新增(新增待审核): ", request.POST)
    alert_type = request.POST.get("alert_type", "")

    # 判断是否已存在
    select_sql = "select id from alert_type where alert_type='%s';" % alert_type
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    if select_res:
        res = {"code": 4041, "msg": "该问题类型已存在"}
        return JsonResponse(res)

    # 插入数据库，关键词为空
    insert_sql = "insert into alert_type(alert_type, status) " \
                 "values('%s', '%s');" \
                 % (alert_type, "新增待审核")
    print("insert_sql: ", insert_sql)
    conf_fun.connect_mysql_operation(sql_text=insert_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-邮件预警-获取问题类型(已审核)
def get_check_alert_type(request):
    print("-----------店铺管理-邮件预警-获取问题类型(已审核): ", request.GET)
    select_sql = "select distinct alert_type from alert_type where status='已审核';"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    res = {"code": 200, "data": select_res}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-邮件预警-问题类型删除(删除类型待审核)
def delete_alert_type(request):
    print("-------店铺管理-邮件预警-问题类型删除(删除待确认): ", request.GET)
    alert_type_list = request.GET.getlist("alert_type_list[]", "")
    for alert_type_item in alert_type_list:
        update_sql = "update alert_type set status='删除类型待审核' where alert_type='%s';" % alert_type_item
        print("update_sql: ", update_sql)
        conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-邮件预警-问题类型管理-某已审核问题类型的关键词获取(已审核/删除待确认)
def get_keyword(request):
    print("-------店铺管理-邮件预警-问题类型管理-某一问题类型的关键词获取(已审核/删除待确认): ", request.GET)
    alert_type = request.GET.get("alert_type", "")
    select_sql = "select keyword from alert_type where alert_type='%s';" % alert_type
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    res = {"code": 200, "data": select_res}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-邮件预警-问题类型管理-某一问题类型的关键词编辑（增加/删除）
def update_keyword(request):
    print("-------店铺管理-邮件预警-问题类型管理-某一问题类型的关键词编辑（增加/删除）: ", request.POST)
    alert_type = request.POST.get("alert_type", "")
    keyword_list = request.POST.getlist("keyword_list", "")
    # 查询该问题类型所有的关键词，如果不在接收的列表中，改变状态为删除待审核
    select_all_keyword_sql = "select keyword from alert_type where alert_type='%s';" % alert_type
    print("select_all_keyword_sql: ", select_all_keyword_sql)
    select_all_keyword_res = conf_fun.connect_mysql_operation(sql_text=select_all_keyword_sql)
    for all_keyword_item in select_all_keyword_res:
        if all_keyword_item[0] not in keyword_list:
            update_alert_type_sql = "update alert_type set status='删除待审核' where alert_type='%s' and keyword='%s';" \
                                    % (alert_type, all_keyword_item[0])
            print("update_alert_type_sql: ", update_alert_type_sql)
            conf_fun.connect_mysql_operation(sql_text=update_alert_type_sql)
    # 遍历查询接收的列表，如果数据库中该问题类型没有该关键词，则添加
    for keyword_item in keyword_list:
        select_exist_sql = "select id from alert_type where alert_type='%s' and keyword='%s';" \
                           % (alert_type, keyword_item)
        print("select_exist_sql: ", select_exist_sql)
        select_exist_res = conf_fun.connect_mysql_operation(sql_text=select_exist_sql)
        if not select_exist_res:
            insert_alert_type_sql = "insert into alert_type(alert_type, keyword, status) values('%s', '%s', '%s');" \
                                    % (alert_type, keyword_item, "新增待审核")
            print("insert_alert_type_sql: ", insert_alert_type_sql)
            conf_fun.connect_mysql_operation(sql_text=insert_alert_type_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-邮件预警-获取待审核的问题类型(新增待审核/删除待确认,关键词为空)（改为返回待审核问题类型（新增/删除）、待审核关键词（新增/删除））
def get_alert_type(request):
    print("-------店铺管理-邮件预警-获取待审核的问题类型（改为返回待审核问题类型（新增/删除）、待审核关键词（新增/删除））-------")
    select_sql = "select alert_type,status from alert_type where status='删除类型待审核' " \
                 "or (status='新增待审核' and keyword is NULL);"
    print("select_sql: ", select_sql)
    type_list = conf_fun.connect_mysql_operation(sql_text=select_sql)

    select_keyword_sql = "select alert_type,keyword,status from alert_type where  status='删除待审核' " \
                         "or (status='新增待审核' and keyword is not NULL);"
    print("select_keyword_sql: ", select_keyword_sql)
    keyword_list = conf_fun.connect_mysql_operation(sql_text=select_keyword_sql)

    res = {"code": 200, "type_list": type_list, "keyword_list": keyword_list}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-邮件预警-问题类型/关键词管理-审核
def check_keyword(request):
    print("-------店铺管理-邮件预警-问题类型/关键词管理-审核: ", request.GET)
    alert_type = request.GET.get("alert_type", "")
    keyword = request.GET.get("keyword", "")
    check_res = request.GET.get("check_res", "")
    print(alert_type, keyword, check_res)
    if check_res == "审核通过":
        print("进入了审核通过流程")
        # 关键字的审核
        if keyword:
            print("进入了关键字的审核流程")
            # 判断其待审核状态
            select_status_sql = "select status from alert_type where alert_type='%s' and keyword='%s';" \
                                % (alert_type, keyword)
            print("select_status_sql: ", select_status_sql)
            select_status_res = conf_fun.connect_mysql_operation(sql_text=select_status_sql)
            if select_status_res[0][0] == "新增待审核":
                print("进入了关键字的新增待审核状态流程")
                # 状态改为已审核
                update_status_sql = "update alert_type set status='已审核' where alert_type='%s' and keyword='%s';" \
                                    % (alert_type, keyword)
                print("update_status_sql: ", update_status_sql)
                conf_fun.connect_mysql_operation(sql_text=update_status_sql)
            else:
                print("进入了关键字的其他状态流程")
                # 删除
                delete_sql = "delete from alert_type where alert_type='%s' and keyword='%s';" % (alert_type, keyword)
                print("delete_sql: ", delete_sql)
                conf_fun.connect_mysql_operation(sql_text=delete_sql)
        # 问题类型的审核
        else:
            print("进入了问题类型的审核流程")
            # 判断其待审核状态
            select_status_sql = "select status from alert_type where alert_type='%s';" \
                                % alert_type
            print("alert_type: ", alert_type)
            select_status_res = conf_fun.connect_mysql_operation(sql_text=select_status_sql)
            if select_status_res[0][0] == "新增待审核":
                print("进入了问题类型的新增待审核状态流程")
                # 状态改为已审核
                update_status_sql = "update alert_type set status='已审核' where alert_type='%s';" \
                                    % alert_type
                print("update_status_sql: ", update_status_sql)
                conf_fun.connect_mysql_operation(sql_text=update_status_sql)
            else:
                print("进入了问题类型的其他状态流程")
                # 删除
                delete_sql = "delete from alert_type where alert_type='%s';" % alert_type
                print("delete_sql: ", delete_sql)
                conf_fun.connect_mysql_operation(sql_text=delete_sql)
    else:
        # 关键字的审核
        if keyword:
            print("进入了关键字的审核流程")
            # 判断其待审核状态
            select_status_sql = "select status from alert_type where alert_type='%s' and keyword='%s';" \
                                % (alert_type, keyword)
            print("select_status_sql: ", select_status_sql)
            select_status_res = conf_fun.connect_mysql_operation(sql_text=select_status_sql)
            if select_status_res[0][0] == "新增待审核":
                print("进入了关键字的新增待审核状态流程")
                # 删除
                delete_sql = "delete from alert_type where alert_type='%s' and keyword='%s';" % (alert_type, keyword)
                print("delete_sql: ", delete_sql)
                conf_fun.connect_mysql_operation(sql_text=delete_sql)
            else:
                print("进入了关键字的其他状态流程")
                # 状态改为已审核
                update_status_sql = "update alert_type set status='已审核' where alert_type='%s' and keyword='%s';" \
                                    % (alert_type, keyword)
                print("update_status_sql: ", update_status_sql)
                conf_fun.connect_mysql_operation(sql_text=update_status_sql)
        # 问题类型的审核
        else:
            print("进入了问题类型的审核流程")
            # 判断其待审核状态
            select_status_sql = "select status from alert_type where alert_type='%s';" \
                                % alert_type
            print("select_status_sql: ", select_status_sql)
            select_status_res = conf_fun.connect_mysql_operation(sql_text=select_status_sql)
            if select_status_res[0][0] == "新增待审核":
                print("进入了问题类型的新增待审核状态流程")
                # 删除
                delete_sql = "delete from alert_type where alert_type='%s';" % alert_type
                print("delete_sql: ", delete_sql)
                conf_fun.connect_mysql_operation(sql_text=delete_sql)
            else:
                print("进入了问题类型的其他状态流程")
                # 状态改为已审核
                update_status_sql = "update alert_type set status='已审核' where alert_type='%s';" \
                                    % alert_type
                print("update_status_sql: ", update_status_sql)
                conf_fun.connect_mysql_operation(sql_text=update_status_sql)
    res = {"code": 200}
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割-店铺绩效


# 店铺管理-店铺绩效-查询
def select_performance(request):
    print("-----------店铺管理-店铺绩效-查询: ", request.GET)
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")

    select_sql = "select * from performance where id!=''"
    if platform:
        select_sql += " and platform='" + platform + "'"
    if country:
        select_sql += " and country='" + country + "'"
    if site:
        select_sql += " and site='" + site + "'"
    select_sql += " order by id desc limit 0,10;"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    # 将国家站点换成英文
    change_country_sql = "select * from country_contrast where country_cn='%s';" % country
    print("转换国家语句: ", change_country_sql)
    change_country_res = conf_fun.connect_mysql_operation(sql_text=change_country_sql, type='dict')
    change_country = change_country_res[0]['country']

    change_site_sql = "select * from area_contrast where area_cn='%s';" % site
    print("转换站点语句: ", change_site_sql)
    change_site_res = conf_fun.connect_mysql_operation(sql_text=change_site_sql, type='dict')
    change_site = change_site_res[0]['area']

    # 获取spu列表
    select_spu_sql = "select distinct spu from commodity_information " \
                     "where platform='%s' and country='%s' and site='%s';" \
                     % (platform, country, site)
    print("获取spuSQL语句: ", select_spu_sql)
    select_spu_res = conf_fun.connect_mysql_operation(sql_text=select_spu_sql)
    spu_list = [x[0] for x in select_spu_res]

    res_data = []
    for select_res_item in select_res:
        res_data.append(list(select_res_item))

    if len(spu_list) > 0:
        for i in range(len(res_data)):
            print("获取广告比和营业额之前的数据: ", res_data[i])
            if not res_data[i][8]:
                select_revenue_sql = "select * from advertising_report where times='%s' and spu in %s " \
                                     "and countries='%s' and company='%s';" \
                                     % (res_data[i][4], str(tuple(spu_list)), change_country, change_site)
                print("查询广告花费和销售额SQL语句: ", select_revenue_sql)
                select_revenue_res = conf_fun.connect_mysql_re(sql_text=select_revenue_sql, type='dict')
                if len(select_revenue_res) > 0:
                    revenue_list = [float(x['sales']) for x in select_revenue_res]
                    print("营业额列表: ", revenue_list)
                    res_data[i][8] = sum(revenue_list)
                    advertising_costs_list = [float(x['advertising_costs']) for x in select_revenue_res]
                    print("广告花费列表: ", advertising_costs_list)
                    if sum(revenue_list) > 0:
                        res_data[i][7] = sum(advertising_costs_list) / sum(revenue_list)
                    else:
                        res_data[i][7] = 0
    else:
        pass

    select_fields_sql = "select index_name,english_name,index_type from target where status='已审核' or status='删除待确认';"
    print("查询指标SQL语句: ", select_fields_sql)
    select_fields_res = conf_fun.connect_mysql_operation(sql_text=select_fields_sql)
    res = {"code": 200, "data": select_res, "fields": select_fields_res}
    print("res: ", res)
    return JsonResponse(res)


# 店铺管理-店铺绩效-新增
def insert_performance(request):
    print("-----------店铺管理-店铺绩效-插入: ", request.POST)
    platform = request.POST.get("platform", "")
    country = request.POST.get("country", "")
    site = request.POST.get("site", "")
    insert_date = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
                   + datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
    print("insert_date: ", insert_date)
    """
    查询指标表，拿到所有指标的英文名字，拿来接收变量
    """
    item_dict = {}
    fields_list = []
    values_list = [platform, country, site, insert_date]
    select_sql = "select english_name from target where status='已审核' or status='删除待审核';"
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    for select_item in select_res:
        item_dict[select_item[0]] = request.POST.get(select_item[0], "")
        fields_list.append(select_item[0])
    print("item_dict: ", item_dict)
    print("fields_list: ", fields_list)
    """
    判断数据库中有无该数据，有则改、然后直接返回
    """
    select_exist_sql = "select id from performance where platform='%s' " \
                       "and country='%s' and site='%s' and insert_date='%s';" \
                       % (platform, country, site, insert_date)
    print("select_exist_sql: ", select_exist_sql)
    select_exist_res = conf_fun.connect_mysql_operation(sql_text=select_exist_sql)
    print("select_exist_res: ", select_exist_res)
    if select_exist_res:
        update_sql = "update performance set "
        for fields_list_index in range(len(fields_list)):
            update_sql += fields_list[fields_list_index] + "='" \
                          + item_dict[fields_list[fields_list_index]] + "'"
            if fields_list_index == (len(fields_list) - 1):
                update_sql += " "
                break
            update_sql += ","
        update_sql += " where platform='%s' and country='%s' and site='%s' and insert_date='%s';"
        update_sql = update_sql % (platform, country, site, insert_date)
        print("update_sql: ", update_sql)
        conf_fun.connect_mysql_operation(sql_text=update_sql)
        res = {"code": 200}
        return JsonResponse(res)
    """
    已确认数据库中没有该条数据，则插入
    """
    insert_sql = "insert into performance(platform,country,site,insert_date,"
    for fields_list_index in range(len(fields_list)):
        insert_sql += fields_list[fields_list_index]
        values_list.append(item_dict[fields_list[fields_list_index]])
        if fields_list_index == (len(fields_list) - 1):
            insert_sql += ")"
            insert_sql += " values('%s','%s','%s','%s','%s'" + ",'%s'" * (len(fields_list) - 1) + ");"
            break
        insert_sql += ","
    values_tup = tuple(values_list)
    insert_sql = insert_sql % values_tup
    print("insert_sql: ", insert_sql)
    conf_fun.connect_mysql_operation(sql_text=insert_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-店铺绩效-编辑
def update_performance(request):
    print("-----------店铺管理-店铺绩效-编辑: ", request.POST)
    platform = request.POST.get("platform", "")
    country = request.POST.get("country", "")
    site = request.POST.get("site", "")
    update_date = request.POST.get("update_date", "")
    # ==================
    item_dict = {}
    fields_list = []
    select_sql = "select english_name from target where status='已审核' or status='删除待审核';"
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    for select_item in select_res:
        item_dict[select_item[0]] = request.POST.get(select_item[0], "")
        fields_list.append(select_item[0])
    print("item_dict: ", item_dict)
    print("fields_list: ", fields_list)
    # ==================
    update_sql = "update performance set "
    for fields_list_index in range(len(fields_list)):
        update_sql += fields_list[fields_list_index] + "='" \
                      + item_dict[fields_list[fields_list_index]] + "'"
        if fields_list_index == (len(fields_list) - 1):
            break
        update_sql += ","
    update_sql += " where platform='%s' and country='%s' and site='%s' and insert_date='%s';"
    print("更新的sql语句", update_sql)
    print("platform: ", platform, type(platform))
    print("country: ", country, type(country))
    print("site: ", site, type(site))
    print("update_date: ", update_date, type(update_date))
    update_sql = update_sql % (platform, country, site, update_date)
    print("update_sql: ", update_sql)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-店铺绩效-获取所有待审核指标
def get_index_performance(request):
    print("------店铺管理-店铺绩效-获取所有待审核指标-----")
    select_sql = "select * from target where status!='已审核';"
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


# 店铺管理-店铺绩效-增加新指标
def add_index_performance(request):
    print("-----------店铺管理-店铺绩效-增加新指标: ", request.POST)
    index_name = request.POST.get("index_name", "")
    english_name = request.POST.get("english_name", "")
    index_type = request.POST.get("index_type", "")
    alert = request.POST.get("alert", "")
    # 指标表插入数据
    insert_sql = "insert into target(index_name, english_name, index_type, alert, status) " \
                 "values('%s', '%s', '%s', '%s', '%s');" \
                 % (index_name, english_name, index_type, alert, "新增待审核")
    print("insert_sql: ", insert_sql)
    conf_fun.connect_mysql_operation(sql_text=insert_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-店铺绩效-删除新指标
def delete_index_performance(request):
    print("-----------店铺管理-店铺绩效-删除新指标: ", request.GET)
    index_id = request.GET.get("index_id", "")
    update_sql = "update target set status='删除待审核' where id='%s';" % index_id
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 店铺管理-店铺绩效-审核新指标
def check_index_performance(request):
    print("-----------店铺管理-店铺绩效-审核新指标: ", request.GET)
    index_id = request.GET.get("index_id", "")
    check_res = request.GET.get("check_res", "")
    select_status_sql = "select status,english_name from target where id='%s';" % index_id
    print("select_status_sql: ", select_status_sql)
    select_status_res = conf_fun.connect_mysql_operation(sql_text=select_status_sql)
    if check_res == "审核通过":
        if select_status_res[0][0] == "新增待审核":
            # 状态改为已审核
            update_sql = "update target set status='已审核' where id='%s';" % index_id
            print("update_sql: ", update_sql)
            conf_fun.connect_mysql_operation(sql_text=update_sql)
            # 绩效表增加新字段
            add_index_sql = "alter table performance add column %s varchar(255);" % select_status_res[0][1]
            print("add_index_sql: ", add_index_sql)
            conf_fun.connect_mysql_operation(sql_text=add_index_sql)
        else:
            # 删除
            delete_sql = "delete from target where id='%s';" % index_id
            print("delete_sql: ", delete_sql)
            conf_fun.connect_mysql_operation(sql_text=delete_sql)
            # 绩效表删除新字段
            delete_index_sql = "alter table performance drop column %s;" % select_status_res[0][1]
            print("delete_index_sql: ", delete_index_sql)
            conf_fun.connect_mysql_operation(sql_text=delete_index_sql)
    else:
        if select_status_res[0][0] == "新增待审核":
            # 删除
            delete_sql = "delete from target where id='%s';" % index_id
            print("delete_sql: ", delete_sql)
            conf_fun.connect_mysql_operation(sql_text=delete_sql)
        else:
            # 状态改为已审核
            update_sql = "update target set status='已审核' where id='%s';" % index_id
            print("update_sql: ", update_sql)
            conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)
