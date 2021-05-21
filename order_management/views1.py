import datetime, time
import pymysql
import requests
import json
import re
import os
import math
import pandas as pd
import numpy as np
from urllib.parse import unquote
from django.http import JsonResponse, FileResponse
# from databases.views1 import connect_mysql,connect_mysql1,connect_mysql2
from settings import conf_fun
# import could_yc, could_sf, could_mf
# from django.utils.http import urlquote
# from docxtpl import DocxTemplate

# 连接数据库
# def connect_mysql3(sql_text, dbs='order', type='tuple'):
#     conn = pymysql.Connect(host='106.53.250.215', port=3306, user='beyoungsql', passwd='Bymy2021.', db=dbs)
#
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


# 颜劲 2021-01-08
# 获取门牌号方法
def get_house_number(str2, str1):
    num_true_front = 0
    num_true_after = 0
    str1 = str(str1)
    str2 = str(str2)
    if str1 != '':
        if str1[0].isdigit():
            num_true_front += 1
        if str1[-1].isdigit():
            num_true_after += 1
        if num_true_front + num_true_after == 1:
            try:
                for n in range(len(str1)):
                    if str1[n].isdigit() is True and str1[n + 1].isdigit() is False and str1[n + 2].isdigit() is True:
                        return '-', str2, str1
            except:
                pass
            str_house_numb = ''
            err_num_count = 0
            if num_true_front == 1:
                for n in range(len(str1)):
                    if str1[n].isdigit() and err_num_count < 1:
                        str_house_numb += str1[n]
                    else:
                        err_num_count += 1
            else:
                for n in range(len(str1)-1, -1, -1):
                    if str1[n].isdigit() and err_num_count < 1:
                        str_house_numb = str1[n] + str_house_numb
                    else:
                        err_num_count += 1
            if str_house_numb == '':
                print('num_true_front1', num_true_front)
            if num_true_front == 1:
                str1 = str1.split(str_house_numb, 1)[1]
            else:
                str1 = str1.rsplit(str_house_numb, 1)[0]

            return str_house_numb, str2, str1

        elif num_true_front + num_true_after == 2:
            return '-', str2, str1
        else:
            try:
                if str2[0].isdigit():
                    num_true_front += 1
                if str2[-1].isdigit():
                    num_true_after += 1
                if num_true_front + num_true_after == 1:
                    try:
                        for n in range(len(str2)):
                            if str2[n].isdigit() is True and str2[n + 1].isdigit() is False and str2[n + 2].isdigit() is True:
                                return '-', str2, str1
                    except:
                        pass

                    str_house_numb = ''
                    err_num_count = 0
                    if num_true_front == 1:
                        for n in range(len(str2)):
                            if str2[n].isdigit() and err_num_count < 1:
                                str_house_numb += str2[n]
                            else:
                                err_num_count += 1
                    else:
                        for n in range(len(str2) - 1, -1, -1):
                            if str2[n].isdigit() and err_num_count < 1:
                                str_house_numb = str2[n] + str_house_numb
                            else:
                                err_num_count += 1
                    if str_house_numb == '':
                        print('num_true_front2', num_true_front)

                    if num_true_front == 1:
                        str2 = str2.split(str_house_numb, 1)[1]
                    else:
                        str2 = str2.rsplit(str_house_numb, 1)[0]
                    return str_house_numb, str2, str1
                else:
                    return '-', str2, str1
            except:
                return '-', str2, str1
    else:
        try:
            if str2[0].isdigit():
                num_true_front += 1
            if str2[-1].isdigit():
                num_true_after += 1
            if num_true_front + num_true_after == 1:
                try:
                    for n in range(len(str2)):
                        if str2[n].isdigit() is True and str2[n + 1].isdigit() is False and str2[
                            n + 2].isdigit() is True:
                            return '-', str2, str1
                except:
                    pass

                str_house_numb = ''
                err_num_count = 0
                if num_true_front == 1:
                    for n in range(len(str2)):
                        if str2[n].isdigit() and err_num_count < 1:
                            str_house_numb += str2[n]
                        else:
                            err_num_count += 1
                else:
                    for n in range(len(str2) - 1, -1, -1):
                        if str2[n].isdigit() and err_num_count < 1:
                            str_house_numb = str2[n] + str_house_numb
                        else:
                            err_num_count += 1
                if str_house_numb == '':
                    print('num_true_front2', num_true_front)

                if num_true_front == 1:
                    str2 = str2.split(str_house_numb, 1)[1]
                else:
                    str2 = str2.rsplit(str_house_numb, 1)[0]
                return str_house_numb, str2, str1
            else:
                return '-', str2, str1
        except:
            return '-', str2, str1


#判断指定的文件夹存不存在，不存在就创建
def creatDir(dir):
    '''
    判断指定的文件夹存不存在
    :param dir:
    :return:
    '''
    dirlist = dir.split("/")
    for i,name in enumerate(dirlist):
        itemdir = os.path.join(os.getcwd(),name)
        #判断当前文件夹是否存在
        if not os.path.exists(itemdir):
            os.mkdir(itemdir)
            print("创建")
        #如果当前文件夹存在并且不是最后一层
        if i < len(dirlist)-1:
            dirlist[i+1] = os.path.join(itemdir,dirlist[i+1])


# 公共获取渠道、站点、国家
def get_channel_site_country(request):

    sql = "select * from store_information;"
    res = conf_fun.connect_mysql_operation(sql,type='dict')

    data = []   # 渠道站点对应列表
    data1 = []  # 站点国家对应列表
    for i in res:
        # 整理渠道、站点
        if len(data) == 0:
            _dict = {
                "channel":i["platform"],
                "station":[i["site"]]
            }
            data.append(_dict)
        else:
            for index,j in enumerate(data):
                if i["platform"] == j["channel"]:
                    j["station"].append(i["site"])
                    break
                elif i["platform"] == j["channel"] and index == len(data)-1:
                    _dict = {
                        "channel": i["platform"],
                        "station": [i["site"]]
                    }
                    data.append(_dict)
                    break

        # 整理站点、国家
        if len(data1) == 0:
            _dict = {
                "channel":i["platform"],
                "station":i["site"],
                "country":[i["country"]]
            }
            data1.append(_dict)
        else:
            for index,j in enumerate(data1):
                if i["platform"] == j["channel"] and i["site"] == j["station"]:
                    j["country"].append(i["country"])
                    break
                else:
                    if index == len(data1)-1:
                        _dict = {
                            "channel": i["platform"],
                            "station": i["site"],
                            "country": [i["country"]]
                        }
                        data1.append(_dict)
                        break

    for i in data:
        i["station"] = list(set(i["station"]))

    for i in data1:
        i["country"] = list(set(i["country"]))
    return JsonResponse({"code":200,"msg":"success","data":data,"data1":data1})


# ------------------>订单管理
# 在途货柜---------2021/01/12 修改人：黄继成
def get_search(request):
    try:
        sql1 = "SELECT DISTINCT ar.*,ci.warehouse_name,ci.sku,ci.cargo_num FROM arrival_receive as ar LEFT JOIN cargo_information as " \
               "ci ON ar.container=ci.container_num where ar.warehousing_date is NULL OR ar.warehousing_date='';"
        data1 = conf_fun.connect_mysql_operation(sql1,dbs='product_supplier', type='dict')
        print('246\n', sql1)
        
        # 得到所有sku的平台、品名
        sql2 = "SELECT * FROM commodity_information;"
        data2 = conf_fun.connect_mysql_operation(sql2, type='dict')
        for i in data1:
            for index,j in enumerate(data2):
                if i["sku"] is not None:
                    if i["sku"] == j["sku"]:
                        i["channel"] = j["platform"]
                        i["product_name"] = j["commodity_name"]
                        i["product_code"] = j["product_code"]
                        break
                    elif i["sku"] != j["sku"] and index == len(data2)-1:
                        i["channel"] = "--"
                        i["product_name"] = "--"
                        i["product_code"] = "--"
                        break
                else:
                    i["channel"] = "--"
                    i["product_name"] = "--"
                    i["product_code"] = "--"
        # print(data1)
        products = [{"site":i["store"],"country":i["country"],"product_code":i["product_code"],"product_name":i["product_name"]} for i in data1]
        channel_list = list(set([(i["channel"],i["store"]) for i in data1]))
        site_list = list(set([(i["store"],i["country"])for i in data1]))
        # print("---",channel_list)
        # print("===",site_list)
        _list = []
        for i in channel_list:
            _dict = {
                "channel":i[0],
                "site":i[1],
                "country":[]
            }
            for j in site_list:
                if i[1] == j[0]:
                    _dict["country"].append(j[1])
            _list.append(_dict)

        _list1 = []
        for item in _list:
            if len(_list1) == 0:
                _dic = {
                    "channel":item["channel"],
                    "store":[
                        {
                            "site":item["site"],
                            "country":item["country"]
                        }
                    ]

                }
                _list1.append(_dic)
            else:
                for index,item1 in enumerate(_list1):
                    if item["channel"] == item1["channel"]:
                        _dic = {
                            "site":item["site"],
                            "country":item["country"]
                        }
                        item1["store"].append(_dic)
                        break
                    elif item["channel"] != item1["channel"] and index == len(_list1)-1:
                        _dic = {
                            "channel": item["channel"],
                            "store": [
                                {
                                    "site": item["site"],
                                    "country": item["country"]
                                }
                            ]

                        }
                        _list1.append(_dic)
                        break
        return JsonResponse({"code": 200, "msg": "success","data1":_list1,"product":products})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})

# 在途货柜盘点---------2021/01/12 修改人：黄继成
def on_way_container(request):
    _list = request.GET.get("data", None)
    page = request.GET.get("page",1)
    # 查找所有的在途货柜以及货柜中的sku
    sql = ""
    sql2 = ""
    if _list is not None:
        _data = json.loads(_list)
        if len(_data) > 0:
            sql = "SELECT ar.*,ci.warehouse_name,ci.sku,ci.cargo_num FROM arrival_receive as ar LEFT JOIN cargo_information as " \
                  "ci ON ar.container=ci.container_num where ar.warehousing_date is NULL OR ar.warehousing_date='' "
            sql2 = "SELECT * FROM commodity_information where "
            for i in _data:
                if i["key"] == "store" or i["key"] == "country" or i["key"] == "type":
                    sql += "and ar." + i["key"] + "='" + i["value"] + "'"
                elif i["key"] == "warehouse":
                    pass
                else:
                    sql2 += i["key"] + "='" + i["value"] + "' and "
            sql2 = sql2[:-5]
    else:
        sql = "SELECT ar.*,ci.warehouse_name,ci.sku,ci.cargo_num FROM arrival_receive as ar LEFT JOIN cargo_information as " \
               "ci ON ar.container=ci.container_num where ar.warehousing_date is NULL OR ar.warehousing_date='';"
        sql2 = "SELECT * FROM commodity_information;"

    print("sql===",sql)
    print("sql2===", sql2)
    try:
        data = conf_fun.connect_mysql_operation(sql,dbs='product_supplier', type='dict')
        # 得到所有sku的平台、品名
        data2 = conf_fun.connect_mysql_operation(sql2, type='dict')
        for i in data:
            if len(data2) == 0:
                i["channel"] = "--"
                i["product_name"] = "--"
                i["product_code"] = "--"
            else:
                for index,j in enumerate(data2):
                    if i['sku'] is not None:
                        if i["sku"] == j["sku"]:
                            i["channel"] = j["platform"]
                            i["product_name"] = j["commodity_name"]
                            i["product_code"] = j["product_code"]
                            break
                        elif i["sku"] != j["sku"] and index == len(data2)-1:
                            i["channel"] = "--"
                            i["product_name"] = "--"
                            i["product_code"] = "--"
                            break
                    else:
                        i["channel"] = "--"
                        i["product_name"] = "--"
                        i["product_code"] = "--"
    
        container = list(set([i["container"] for i in data]))
        _list1 = [
            {
                'stock_all_num': 0,
                'fba_all_num': 0,
                'fbm_all_num': 0,
            }
        ]
    
        for i in data:
            if len(_list1) < 2:
                _dict = {
                    'product_code': i["product_code"],
                    'product_name': i["product_name"],
                    'stock_num':0,
                    'sku_data':[
                        {
                            "stock_num":0,
                            'sku':i["sku"],
                            "fba":0,
                            "fbm": 0,
                            i["container"]:0
                        }
                    ],
                    'fba': 0,
                    'fbm': 0,
                }
                if i["cargo_num"] is not None:
                    _dict["stock_num"] = int(i["cargo_num"])
                    _dict["fba"] = int(i["cargo_num"])
                    _dict["sku_data"][0]["stock_num"] = int(i["cargo_num"])
                    _dict["sku_data"][0]["fba"] = int(i["cargo_num"])
                    _dict["sku_data"][0][i["container"]] = int(i["cargo_num"])
                _list1.append(_dict)
            else:
                for index,j in enumerate(_list1):
                    if index > 0:
                        if i["product_code"] == j["product_code"]:
                            _dic = {
                                "stock_num":0,
                                'sku':i["sku"],
                                "fba":0,
                                "fbm": 0,
                                i["container"]:0
                            }
                            if i["cargo_num"] is not None:
                                _dic["stock_num"] = int(i["cargo_num"])
                                _dic["fba"] = int(i["cargo_num"])
                                _dic[i["container"]] = int(i["cargo_num"])
                            j["stock_num"] += int(i["cargo_num"]) if i["cargo_num"] is not None else 0
                            j["sku_data"].append(_dic)
                            j["fba"] += int(i["cargo_num"]) if i["cargo_num"] is not None else 0
                            j[i["container"]] = int(i["cargo_num"]) if i["cargo_num"] is not None else 0
                            break
                        elif i["product_code"] != j["product_code"] and index == len(_list1)-1:
                            _dict = {
                                'product_code': i["product_code"],
                                'product_name': i["product_name"],
                                'stock_num': 0,
                                'sku_data': [
                                    {
                                        "stock_num": 0,
                                        'sku': i["sku"],
                                        "fba": 0,
                                        "fbm": 0,
                                        i["container"]: 0
                                    }
                                ],
                                'fba': 0,
                                'fbm': 0,
                            }
                            if i["cargo_num"] is not None:
                                _dict["stock_num"] = int(i["cargo_num"])
                                _dict["fba"] = int(i["cargo_num"])
                                _dict["sku_data"][0]["stock_num"] = int(i["cargo_num"])
                                _dict["sku_data"][0]["fba"] = int(i["cargo_num"])
                                _dict["sku_data"][0][i["container"]] = int(i["cargo_num"])
                            _list1.append(_dict)
                            break
    
        total_num = len(_list1)
        start = int(page) * 50 - 50
        end = int(page) * 50
        _list2 = _list1[start:end]
    
        data1 = {
            "header":container,
            "data":_list2
        }
        return JsonResponse({"code": 200, "msg": "success", "data": data1,"total_num":total_num})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 广告管理
def get_arg(request):
    try:
        now = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=30),"%Y-%m-%d")
        sql1 = "select * from advertising_report where times>='%s';"%(now)
        data1 = conf_fun.connect_mysql_re(sql1,type='dict')
        channel_list = list(set([('Amazon',i["company"]) for i in data1]))
        site_list = list(set([(i["company"],i["countries"])for i in data1]))

        _list = []
        for i in channel_list:
            _dict = {
                "channel":i[0],
                "site":i[1],
                "country":[]
            }
            for j in site_list:
                if i[1] == j[0]:
                    _dict["country"].append(j[1])
            _list.append(_dict)

        _list1 = []
        for item in _list:
            if len(_list1) == 0:
                _dic = {
                    "channel":item["channel"],
                    "store":[
                        {
                            "site":item["site"],
                            "country":item["country"]
                        }
                    ]

                }
                _list1.append(_dic)
            else:
                for index,item1 in enumerate(_list1):
                    if item["channel"] == item1["channel"]:
                        _dic = {
                            "site":item["site"],
                            "country":item["country"]
                        }
                        item1["store"].append(_dic)
                        break
                    elif item["channel"] != item1["channel"] and index == len(_list1)-1:
                        _dic = {
                            "channel": item["channel"],
                            "store": [
                                {
                                    "site": item["site"],
                                    "country": item["country"]
                                }
                            ]

                        }
                        _list1.append(_dic)
                        break

        _list2 = []
        for i in _list1:
            _dict = {
                "channel": i["channel"],
                "store": []

            }
            for j in i["store"]:
                _dic = {
                    "site": "",
                    "country": []
                }
                for item in j["country"]:
                    store1, country1 = store_country_code(j["site"], item, 'zh')
                    _dic["site"] = store1
                    _dic["country"].append(country1)
                _dict["store"].append(_dic)
            _list2.append(_dict)
        return JsonResponse({"code": 200, "msg": "success","data":_list2})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 请求spu---------2020/12/28 修改人：黄继成
def get_spu(request):
    channel = request.GET.get("channel",None)
    store = request.GET.get("store",None)
    country = request.GET.get("country",None)
    print(channel,store,country)
    if country == '英国' or country == '法国' or country == '德国' or country == '意大利' or country == '西班牙':
        country = '欧洲'
    # store1, country1 = store_country_code('', country, 'en',type='upper')
    # print(store1,country1)
    # 查询所有商品数据
    sql = "SELECT * FROM commodity_information where platform='%s' and country='%s' and site='%s';"%(channel,country,store)
    print("sql===",sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    mp_list = []
    gm_list = []
    for i in data:
        if i["category"] == "魔片":
            mp_list.append(i["spu"])
        else:
            gm_list.append(i["spu"])
    mp_list = list(set(mp_list))
    gm_list = list(set(gm_list))
    return JsonResponse({"code":200,"msg":"success","mp_list":mp_list,"gm_list":gm_list})


# 获取最近n天的时间列表
def get_days(date,nums):
    date_list = []
    for i in range(nums):
        if '-' in date:
            _str = datetime.datetime.strftime(datetime.datetime.strptime(date,"%Y-%m-%d")-datetime.timedelta(i),"%Y-%m-%d")
        else:
            _str = datetime.datetime.strftime(datetime.datetime.strptime(date,"%Y.%m.%d")-datetime.timedelta(i),"%Y.%m.%d")
        date_list.append(_str)
    return date_list


# 站点、国家编码转换
def store_country_code(store,country,language,type=''):
    if language == "en":
        if type == "low":
            if store == "胤佑":
                store = "yy"
            elif store == "爱瑙":
                store = "an"
            elif store == "中睿":
                store = "zr"
            elif store == "京汇":
                store = "jh"
            elif store == "利百锐":
                store = "lbr"

            if country == "美国":
                country = "us"
            elif country == "英国":
                country = "uk"
            elif country == "加拿大":
                country = "ca"
            elif country == "日本":
                country = "jp"
            elif country == "欧洲":
                country = "eu"
            elif country == "澳洲":
                country = "au"
            elif country == "法国":
                country = "fr"
            elif country == "德国":
                country = "de"
            elif country == "意大利":
                country = "it"
            elif country == "西班牙":
                country = "es"
            elif country == "墨西哥":
                country = "mx"
            elif country == "西班牙":
                country = "ie"
            elif country == "葡萄牙":
                country = "pt"
            elif country == "瑞典":
                country = "se"
            elif country == "奥地利":
                country = "at"
        else:
            if store == "胤佑":
                store = "YY"
            elif store == "爱瑙":
                store = "AN"
            elif store == "中睿":
                store = "ZR"
            elif store == "京汇":
                store = "JH"
            elif store == "利百锐":
                store = "LBR"

            if country == "美国":
                country = "US"
            elif country == "英国":
                country = "UK"
            elif country == "加拿大":
                country = "CA"
            elif country == "日本":
                country = "JP"
            elif country == "欧洲":
                country = "EU"
            elif country == "澳洲":
                country = "AU"
            elif country == "法国":
                country = "FR"
            elif country == "德国":
                country = "DE"
            elif country == "意大利":
                country = "IT"
            elif country == "西班牙":
                country = "ES"
            elif country == "墨西哥":
                country = "MX"
            elif country == "西班牙":
                country = "IE"
            elif country == "葡萄牙":
                country = "PT"
            elif country == "瑞典":
                country = "SE"
            elif country == "奥地利":
                country = "AT"
    else:
        if store == "yy" or store == "YY":
            store = "胤佑"
        elif store == "an" or store == "AN":
            store = "爱瑙"
        elif store == "zr" or store == "ZR":
            store = "中睿"
        elif store == "jh" or store == "JH":
            store = "京汇"
        if country == "us" or country == "US":
            country = "美国"
        elif country == "uk" or country == "UK" or country == "GB":
            country = "英国"
        elif country == "ca" or country == "CA":
            country = "加拿大"
        elif country == "jp" or country == "JP":
            country = "日本"
        elif country == "eu" or country == "EU":
            country = "欧洲"
        elif country == "au" or country == "AU":
            country = "澳洲"
        elif country == "fr" or country == "FR":
            country = "法国"
        elif country == "de" or country == "DE":
            country = "德国"
        elif country == "it" or country == "IT":
            country = "意大利"
        elif country == "es" or country == "ES":
            country = "西班牙"
        elif country == "mx" or country == "MX":
            country = "墨西哥"
        elif country == "ie" or country == "IE":
            country = "西班牙"
        elif country == "pt" or country == "PT":
            country = "葡萄牙"
        elif country == "se" or country == "SE":
            country = "瑞典"
        elif country == "at" or country == "AT":
            country = "奥地利"
    return store,country


# 请求评分
def get_star(store,country,spu,start_date,end_date):
    store1,country1 = store_country_code(store,country,'en',type='upper')
    date1 = datetime.datetime.strptime(start_date,"%Y.%m.%d")
    date2 = datetime.datetime.strptime(end_date,"%Y.%m.%d")
    date_list = []
    while date1 <= date2:
        _str = datetime.datetime.strftime(date1, "%Y.%m.%d")
        date_list.append(_str)
        date1 += datetime.timedelta(days=1)

    print(date_list)
    t = tuple(date_list)
    sql = "select comment_amount,star_level,dates from front_display where country='%s' and area='%s' and SPU='%s' and dates in %s;" % (country, store1, spu, t)
    data = conf_fun.connect_mysql_re(sql, type='dict')
    # 查询30天的数据
    _time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y.%m.%d")
    sql1 = "select * from front_display as fd where fd.area in ('%s' ,'%s') and fd.country='%s' and dates >= '%s';" % (store1, store, country, _time)
    res = conf_fun.connect_mysql_re(sql1, type='dict')
    # 获取30天内最高和最低数据
    _list = [float(j["star_level"]) for j in res if j["star_level"] is not None and j["star_level"] != 'NONE']
    mins = min(_list) if len(_list) > 0 else 0
    maxs = max(_list) if len(_list) > 0 else 0
    data1 = []
    for i in data:
        if len(data1) == 0:
            _dic = {
                "dates": i["dates"],
                "star_level": i["star_level"],
                "comment_amount": i["comment_amount"]
            }
            data1.append(_dic)
        else:
            for index, j in enumerate(data1):
                if i["dates"] == j["dates"]:
                    break
                elif i["dates"] != j["dates"] and index == len(data1) - 1:
                    _dic = {
                        "dates": i["dates"],
                        "star_level": i["star_level"],
                        "comment_amount": i["comment_amount"]
                    }
                    data1.append(_dic)
                    break
    print("data1===", data1)
    return {"mins":mins,"maxs":maxs,"data":data1}


# 获取默认前台检查的数据
def get_rank(store,country,spu,days='',start_date='',end_date=''):
    if days == '':
        days = 7
    data = []
    day = 0
    time = ""
    now = datetime.datetime.now()
    site_dict = {
    'AN':'爱瑙',
    'YY':'胤佑',
    'JH':'京汇',
    'ZR':'中睿',
    'DNY':'东南亚'
    }
    site_z = site_dict.get(store)
    while len(data) == 0 and day < 10:
        time = (now - datetime.timedelta(days=day)).strftime("%Y.%m.%d")
        select = "select fd.* from front_display as fd where fd.dates='" + time + "' and fd.area in ('%s','%s') and country='%s' and SPU='%s';"%(store,site_z,country,spu)
        data = conf_fun.connect_mysql_operation(sql_text=select, type='dict')
        day += 1

    # 查询30天的数据
    _time = (now - datetime.timedelta(days=30)).strftime("%Y.%m.%d")
    sql1 = "select * from front_display as fd where fd.area in ('%s' ,'%s') and fd.country='%s' and SPU='%s' and dates >= '%s';"%(store, site_z, country,spu,_time)
    print("sql1===", sql1)
    res = conf_fun.connect_mysql_operation(sql1,type='dict')
    print("len===",len(res))
    # 得到数据库中最近日期往前n天的日期，目的是为了查询n天的排名数据
    if start_date == '' and end_date == '':
        date_list = [datetime.datetime.strftime(datetime.datetime.strptime(time, "%Y.%m.%d") - datetime.timedelta(days=i),"%Y.%m.%d") for i in range(days)][::-1]
    else:
        date1 = datetime.datetime.strptime(start_date, "%Y.%m.%d")
        date2 = datetime.datetime.strptime(end_date, "%Y.%m.%d")
        date_list = []
        while date1 <= date2:
            _str = datetime.datetime.strftime(date1, "%Y.%m.%d")
            date_list.append(_str)
            date1 += datetime.timedelta(days=1)
    # 查询前n天的数据
    if len(date_list) <= 30:
        datas = [i for i in res if i["dates"] in date_list]
    else:
        t = tuple(date_list)
        sql = "select * from front_display as fd where fd.area in ('%s','%s') and fd.country='%s' and SPU='%s' and dates in %s;" % (store,site_z, country,spu,t)
        datas = conf_fun.connect_mysql_re(sql_text=sql, type='dict')

    for item in data:
        data2 = [0 for i in date_list]
        for index, i in enumerate(date_list):
            for j in datas:
                if j["SKU"] == item["SKU"] and j["dates"] == i:
                    pattern = re.compile(r'\d+')
                    if j.get("ranking"):
                        result = pattern.findall(j["ranking"])
                        _rank = ''.join(result)
                        data2[index] = int(_rank)
           

        item["seven_data"] = [str(i) for i in data2]
        item["seven_labels"] = date_list
        item["min"] = "0"
        if max(data2) <= 10:
            item["max"] = "10"  # 获取离它最近的整万
            item["stepSize"] = str(10 // 4)  # 求步长
        elif max(data2) > 10 and max(data2) < 100:
            item["max"] = str((max(data2) // 10 + 1) * 10)  # 获取离它最近的整万
            item["stepSize"] = str((max(data2) // 10 + 1) * 10 // 4)  # 求步长
        elif max(data2) >= 100 and max(data2) < 1000:
            item["max"] = str((max(data2) // 100 + 1) * 100)  # 获取离它最近的整万
            item["stepSize"] = str((max(data2) // 100 + 1) * 100 // 4)  # 求步长
        elif max(data2) >= 1000 and max(data2) < 10000:
            item["max"] = str((max(data2) // 1000 + 1) * 1000)  # 获取离它最近的整万
            item["stepSize"] = str((max(data2) // 1000 + 1) * 1000 // 4)  # 求步长
        elif max(data2) >= 10000:
            item["max"] = str((max(data2) // 10000 + 1) * 10000)  # 获取离它最近的整万
            item["stepSize"] = str((max(data2) // 10000 + 1) * 10000 // 4)  # 求步长

    # 替换
    for i in data:
        pattern = re.compile(r'\d+')
        result = pattern.findall(i["ranking"])
        _ranking = ''.join(result)
        i["ranking"] = _ranking
        # 获取30天内最高和最低数据
        _list = [j["ranking"] for j in res if j["SKU"] == i["SKU"]]
        _list1 = []
        for n in _list:
            pattern = re.compile(r'\d+')
            result = pattern.findall(n)
            _rank = ''.join(result)
            if _rank:
                _list1.append(int(_rank))
           
        print("_list1===",_list1)
        if len(_list1) == 0:
        	 _list1 = [0]
        i["mins"] = min(_list1)
        i["maxs"] = max(_list1)
    return data


# 获取sku10日均单量
def get_order_num(store, country, sku):
    store,country = store_country_code(store,country,"en",type='upper')

    if country in ["UK", "FR", "DE", "IT", "ES"]:
        sql = "select * from order_sublist where company='%s' and countries='%s' and sku='%s' order by id desc LIMIT 10;" % (
        store, country, sku)
    else:
        sql = "select * from sku_report where company='%s' and countries='%s' and sku='%s' order by id desc LIMIT 10;" % (
        store, country, sku)
    data = conf_fun.connect_mysql_re(sql, type='dict')
    num = 0
    avg = 0
    if len(data) > 0:
        for i in data:
            num += int(i["nums"])
    if num > 0:
        avg = num / 10

    return avg


# 获取库存数据
def get_stock_data(channel,store,country,spu):
    if channel == "amazon":
        channel = "Amazon"
    sql = "SELECT c.product_code,c.spu,c.sku,c.platform,c.country,c.site,c.commodity_price,p.product_name " \
          "FROM commodity_information as c join product_message as p ON c.product_code=p.product_code where " \
          "c.platform='%s' and c.site='%s' and c.country='%s' and c.spu='%s';"%(channel,store,country,spu)
    print("sql---", sql)
    # 查询商品信息
    data = conf_fun.connect_mysql_operation(sql, type='dict')
    print(data)
    # 查询详细信息
    for i in data:
        sku = i["sku"]
        # 查询fba库存
        sql1 = "select * from sku_report where sku='%s' order by id desc LIMIT 1;" % (sku)
        res = conf_fun.connect_mysql_re(sql1, type='dict')
        if len(res) > 0:
            i["fba"] = int(res[0]["fba"])
            i["on_warehouse_num"] = int(res[0]["fba"])
            i["all_nums"] = int(res[0]["fba"])
        else:
            i["fba"] = 0
            i["on_warehouse_num"] = 0
            i["all_nums"] = 0

        # 查询fbm库存
        sql2 = "select * from fbm_data" \
               " where sku='%s' order by id desc LIMIT 1;" % (sku)
        data2 = conf_fun.connect_mysql_re(sql2, type='dict')
        if len(data2) > 0:
            i["fbm"] = int(data2[0]["nums"])
            i["on_warehouse_num"] += int(data2[0]["nums"])
            i["all_nums"] += int(data2[0]["nums"])
        else:
            i["fbm"] = 0

        # 获取在途fba
        i["on_way_nums"] = 0
        i["on_way_fba"] = 0
        i["on_way_fbm"] = '--'
        # 查找当前sku在途数量
        sql3 = "SELECT ar.*,ci.sku FROM arrival_receive as ar JOIN cargo_information as ci" \
               " ON ar.container=ci.container_num where ar.country='%s' and ar.store='%s' and ar.warehousing_date is NULL and ci.sku='%s' " \
               "OR ar.country='%s' and ar.store='%s' and ar.warehousing_date ='' and ci.sku='%s';"%(country,store,sku,country,store,sku)
        data3 = conf_fun.connect_mysql_product_supplier(sql3, type='dict')
        if len(data3) > 0:
            i["on_way_nums"] = int(data3[0]["issue_count"])
            i["on_way_fba"] = int(data3[0]["issue_count"])

        # 获取10日均单量
        avg = get_order_num(i["site"], i["country"], i["sku"])
        i["avg"] = avg

        # 期望营业额
        expect_turnover = avg * float(i["commodity_price"]) if i["commodity_price"] is not None else avg * 0
        i["expect_turnover"] = expect_turnover

        # 预计售空天数
        if avg > 0:
            estimate_sell_out_days = i["on_warehouse_num"] / avg
        else:
            estimate_sell_out_days = 0
        i["estimate_sell_out_days"] = estimate_sell_out_days
        # 预计售空日期
        estimate_sell_out_date = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=estimate_sell_out_days), "%Y-%m-%d")
        i["estimate_sell_out_date"] = estimate_sell_out_date

    # 查询待入仓货柜
    sql4 = "SELECT ar.container,ar.delivery_date,ar.warehousing_date,ci.sku,ci.warehouse_name FROM arrival_receive as ar JOIN cargo_information as ci" \
           " ON ar.container=ci.container_num where ar.country='%s' and ar.store='%s' and ar.warehousing_date is not NULL " \
           "OR ar.country='%s' and ar.store='%s' and ar.warehousing_date !='';"%(country,store,country,store)
    data4 = conf_fun.connect_mysql_product_supplier(sql4, type='dict')
    for i in data4:
        for j in data:
            if i["sku"] == j["sku"]:
                i["product_name"] = j["product_name"]
    return data,data4


# 获取sku订单默认15天的数据
def get_sku_data(store,country,spu):
    store, country = store_country_code(store, country, "en", type='upper')
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    date_list = get_days(now,15)
    date_list.reverse()
    try:
        _list = [
            {
                "name": "销售额",
                "value": []
            },
            {
                "name": spu,
                "value": []
            }
        ]
        for i in date_list:
            sql = "select * from sku_report where company='%s' and countries='%s' and spu='%s' and times='%s';" % (
            store, country, spu, i)
            res = conf_fun.connect_mysql_operation(sql, type='dict')
            num = 0
            cost = 0
            for j in res:
                for index, item in enumerate(_list):
                    if item["name"] == j["sku"]:
                        _dict = {
                            "date": i,
                            "num": int(j["num"])
                        }
                        item["value"].append(_dict)
                    elif item["name"] != j["sku"] and index == len(_list) - 1:
                        _dict = {
                            "name": j["sku"],
                            "value": [{"date": i, "num": int(j["num"])}]
                        }
                        _list.append(_dict)
                num += int(j["num"])
                cost += round(float(j["prices"]), 2)
            _list[0]["value"].append({"date": i, "cost": cost})
            _list[1]["value"].append({"date": i, "num": num})

        data = {"code":200,"header":date_list,"data":_list}
        return data
    except Exception as e:
        return {"code": 500, "msg": "error:" + str(e)}


# 获取近3天spu销售数据,计算广告指导价
def get_spu_price_data(channel,store,country,spu):
    store, country = store_country_code(store, country, "en", type='upper')
    date_list = []
    for i in range(3):
        now = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i + 1), "%Y-%m-%d")
        date_list.append(now)

    _str = "','".join(date_list)
    sql = "select * from sku_report where spu='"+spu+"' and countries='"+country+"' and company='"+store+"' and times in ('"+_str+"');"
    data = conf_fun.connect_mysql_operation(sql,type='dict')
    _list = []
    for i in date_list:
        _dic = {
            "date":i,
            "num":0,
            "cost":0
        }
        for j in data:
            if i == j["times"]:
                _dic["num"] += float(j["price"])
        _list.append(_dic)

    # 获取spu广告花费
    sql1 = "select advertising_costs,times from advertising_report where company='"+store+"' and countries='"+country+"' and spu='"+spu+"' and times in ('"+_str+"');"
    costs = conf_fun.connect_mysql_re(sql1,type='dict')
    for i in _list:
        for j in costs:
            if i["date"] == j["times"]:
                i["cost"] = round(float(j["advertising_costs"]),2)
    # 获取当前spu最近日期的广告系数
    sql2 = "select * from advertisement_guidance where channel='"+channel+"' and store='"+store+"' and country='"+country+"' and spu='"+spu+"' and dates in ('"+_str+"') order by id desc;"
    res = conf_fun.connect_mysql_operation(sql2,type='dict')
    for i in _list:
        i["dates"] = i["date"]
        if len(res) > 0:
            i["guidance_price_manual"] = i["num"] * float(res[0]["advertisement_coefficient_manual"])
            i["guidance_price_auto"] = i["num"] * float(res[0]["advertisement_coefficient_auto"])
            for j in res:
                if i["date"] == j["dates"]:
                    i["remark_manual"] = j["remark_manual"]
                    i["remark_auto"] = j["remark_auto"]
                    i["advertisement_proportion"] = j["advertisement_proportion"]
                    i["advertisement_coefficient_manual"] = float(res[0]["advertisement_coefficient_manual"])
                    i["advertisement_coefficient_auto"] = float(res[0]["advertisement_coefficient_auto"])

        else:
            # 默认自定义广告系数为 0.3
            i["guidance_price_manual"] = i["num"] * 0.3
            i["guidance_price_auto"] = i["num"] * 0.3
            i["remark_manual"] = ""
            i["remark_auto"] = ""
            i["advertisement_proportion"] = ""
            i["advertisement_coefficient_manual"] = 0.3
            i["advertisement_coefficient_auto"] = 0.3
    return _list


# 获取列表最大值、步长
def get_max_step(list):
    _max = ""
    stepSize = ""
    if max(list) <= 10:
        _max = "10"  # 获取离它最近的整万
        stepSize = str(10 // 4)  # 求步长
    elif max(list) > 10 and max(list) < 100:
        _max = str((max(list) // 10 + 1) * 10)  # 获取离它最近的整数
        stepSize = str((max(list) // 10 + 1) * 10 // 4)  # 求步长
    elif max(list) >= 100 and max(list) < 1000:
        _max = str((max(list) // 100 + 1) * 100)  # 获取离它最近的整数
        stepSize = str((max(list) // 100 + 1) * 100 // 4)  # 求步长
    elif max(list) >= 1000 and max(list) < 10000:
        _max = str((max(list) // 1000 + 1) * 1000)  # 获取离它最近的整数
        stepSize = str((max(list) // 1000 + 1) * 1000 // 4)  # 求步长
    elif max(list) >= 10000:
        _max = str((max(list) // 10000 + 1) * 10000)  # 获取离它最近的整数
        stepSize = str((max(list) // 10000 + 1) * 10000 // 4)  # 求步长
    return _max,stepSize

# 获取广告词监控数据---------2020/12/28 修改人：黄继成
def get_advertising_monitor_data(channel,store,country,spu,date=''):
    if channel == 'amazon':
        channel = 'Amazon'

    if date == '':
        now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
        date = now

    sql = "select * from advertising_words_monitor where channel='"+channel+"' and store='"+store+"' " \
          "and country='"+country+"' and spu='"+spu+"' and times like'%"+date+"%';"
    print(sql)
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    print(len(res))
    proposal_bidding_list = []
    key_word_bidding_list = []
    exposure_list = []
    click_num_list = []
    click_rate_list = []
    cost_list = []
    every_click_free_list = []
    order_num_list = []
    sales_volume_list = []
    acos_list = []
    _list1 = []
    _list2 = []
    _list3 = []
    _list4 = []
    data = {}
    datas = []
    data_labels = ["10:00", "14:00", "17:00", "24:00"]
    if len(res) == 0:
        data = {
            "datas": datas,
            "proposal_bidding_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": proposal_bidding_list},
            "key_word_bidding_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": key_word_bidding_list},
            "exposure_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": exposure_list},
            "click_num_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": click_num_list},
            "click_rate_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": click_rate_list},
            "cost_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": cost_list},
            "every_click_free_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": every_click_free_list},
            "order_num_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": order_num_list},
            "sales_volume_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": sales_volume_list},
            "acos_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": acos_list},
        }
    else:
        # 先按时间排序
        res.sort(key=lambda x:x["times"])
        for i in res:
            if "T10:00" in i["times"]:
                _list1.append(i)
            elif "T14:00" in i["times"]:
                _list2.append(i)
            elif "T17:00" in i["times"]:
                _list3.append(i)
            elif "T24:00" in i["times"]:
                _list4.append(i)
            proposal_bidding_list.append(float(i["proposal_bidding"]))
            key_word_bidding_list.append(float(i["key_word_bidding"]))
            exposure_list.append(int(i["exposure"]))
            click_num_list.append(int(i["click_num"]))
            click_rate_list.append(float(i["click_rate"]))
            cost_list.append(float(i["cost"]))
            every_click_free_list.append(float(i["every_click_free"]))
            order_num_list.append(int(i["order_num"]))
            sales_volume_list.append(float(i["sales_volume"]))
            acos_list.append(float(i["acos"]))

        if len(_list4) > 0:
            datas = _list4
        elif len(_list3) > 0:
            datas = _list3
        elif len(_list2) > 0:
            datas = _list2
        elif len(_list1) > 0:
            datas = _list1

        max1, stepSize1 = get_max_step(proposal_bidding_list)
        max2, stepSize2 = get_max_step(key_word_bidding_list)
        max3, stepSize3 = get_max_step(exposure_list)
        max4, stepSize4 = get_max_step(click_num_list)
        max5, stepSize5 = get_max_step(click_rate_list)
        max6, stepSize6 = get_max_step(cost_list)
        max7, stepSize7 = get_max_step(every_click_free_list)
        max8, stepSize8 = get_max_step(order_num_list)
        max9, stepSize9 = get_max_step(sales_volume_list)
        max10, stepSize10 = get_max_step(acos_list)
        data = {
            "datas":datas,
            "proposal_bidding_list":{"min":'0',"max":max1,"stepSize":stepSize1,"data_labels":data_labels,"datas":proposal_bidding_list},
            "key_word_bidding_list": {"min":'0',"max":max2,"stepSize":stepSize2,"data_labels":data_labels,"datas":key_word_bidding_list},
            "exposure_list": {"min":'0',"max":max3,"stepSize":stepSize3,"data_labels":data_labels,"datas":exposure_list},
            "click_num_list": {"min":'0',"max":max4,"stepSize":stepSize4,"data_labels":data_labels,"datas":click_num_list},
            "click_rate_list": {"min":'0',"max":max5,"stepSize":stepSize5,"data_labels":data_labels,"datas":click_rate_list},
            "cost_list": {"min":'0',"max":max6,"stepSize":stepSize6,"data_labels":data_labels,"datas":cost_list},
            "every_click_free_list": {"min":'0',"max":max7,"stepSize":stepSize7,"data_labels":data_labels,"datas":every_click_free_list},
            "order_num_list": {"min":'0',"max":max8,"stepSize":stepSize8,"data_labels":data_labels,"datas":order_num_list},
            "sales_volume_list": {"min":'0',"max":max9,"stepSize":stepSize9,"data_labels":data_labels,"datas":sales_volume_list},
            "acos_list": {"min":'0',"max":max10,"stepSize":stepSize10,"data_labels":data_labels,"datas":acos_list},
        }
    return data

# 请求数据
def get_data(request):
    channel = request.GET.get("channel",None)
    site = request.GET.get("store", None)
    country = request.GET.get("country", None)
    spu = request.GET.get("spu",None)
    print(channel,site,country,spu)
    # 请求运营日报
    date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1), "%Y-%m-%d")
    type = "everyday"
    url = 'http://www.beyoung.group/history_report?zr_all?中睿运营数据?' + date + '?' + type
    re = requests.get(url=url)
    print(re)
    data_res = json.loads(re.text)
    res = data_res["data"]
    report = {"yye":"","gghf":"","ggzb":""}
    for i in res["zr"]:
        _store1,_country1 = store_country_code(site, country, "en", type='low')
        print(_store1 + _country1+"_yye")
        print(_store1 + _country1 + "_gghf")
        print(_store1 + _country1 + "_ggzb")
        report["yye"] = i[_store1+_country1+"_yye"]
        report["gghf"] = i[_store1 + _country1 + "_gghf"]
        report["ggzb"] = i[_store1 + _country1 + "_ggzb"]

    # 请求评分
    print("请求评分")
    if site == "胤佑":
        store1 = "YY"
    elif site == "爱瑙":
        store1 = "AN"
    elif site == "中睿":
        store1 = "ZR"
    elif site == "京汇":
        store1 = "JH"
    elif site =='利百锐':
    	   store1 ='LBR'
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y.%m.%d")
    date_list = get_days(now,7)
    t = tuple(date_list)
    sql = "select comment_amount,star_level,dates from front_display where country='%s' and area='%s' and SPU='%s' and dates in %s;"%(country,store1,spu,t)
    data = conf_fun.connect_mysql_operation(sql,type='dict')

    # 查询30天的数据
    print("请求30天的数据")
    _time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y.%m.%d")
    sql1 = "select * from front_display as fd where fd.area in ('%s','%s') and fd.country='%s' and dates >= '%s';" % (store1, site,country, _time)
    res = conf_fun.connect_mysql_operation(sql1, type='dict')
    # 获取30天内最高和最低数据
    _list = []
    for i in res:
        if i["star_level"] is not None and i["star_level"] != 'NONE' and i["star_level"] != '':
            if i["star_level"].isdigit() == True:
                _list.append(float(i["star_level"]))
            else:
                _list.append(0)
        else:
            _list.append(0)

    if len(_list) == 0:
        mins = 0
        maxs = 0
    else:
        mins = min(_list)
        maxs = max(_list)
    data1 = []
    for i in data:
        if len(data1) == 0:
            _dic = {
                "dates":i["dates"],
                "star_level":i["star_level"],
                "comment_amount":i["comment_amount"]
            }
            data1.append(_dic)
        else:
            for index,j in enumerate(data1):
                if i["dates"] == j["dates"]:
                    break
                elif i["dates"] != j["dates"] and index == len(data1)-1:
                    _dic = {
                        "dates": i["dates"],
                        "star_level": i["star_level"],
                        "comment_amount": i["comment_amount"]
                    }
                    data1.append(_dic)
                    break

    # 请求前台检查默认数据
    rank_data = get_rank(store1,country,spu,days=7)
    print("请求前台检查默认数据完成")
    # 请求库存数据
    print("请求库存数据")
    stock_data,arrival_data = get_stock_data(channel,site,country,spu)

    # 请求sku订单默认15天的数据
    print("请求sku订单默认15天的数据")
    sku_data = get_sku_data(site,country,spu)

    if sku_data["code"] == 500:
        sku_data = {}

    # 请求当前spu广告指导数据
    print("请求当前spu广告指导数据")
    spu_data = get_spu_price_data(channel,site,country,spu)

    #获取广告监控数据
    print("获取广告监控数据")
    advertising_monitor = get_advertising_monitor_data(channel,site,country,spu)

    print(advertising_monitor)
    return JsonResponse({"code":200,"msg":"success","report":report,"star_min":mins,"star_max":maxs,"star":data1,
                         "rank_data":rank_data,"stock_data":stock_data,"arrival_data":arrival_data,"sku_data":sku_data,
                         "advertisement_data":spu_data,"advertising_monitor":advertising_monitor})


# 广告监控数据上传  修改人：黄继成 时间：2021-01-15
def advertising_monitor_upload(request):
    channel = request.POST.get("channel",None)
    store = request.POST.get("store", None)
    country = request.POST.get("country", None)
    spu = request.POST.get("spu", None)
    times = request.POST.get("times", None)
    dates = request.POST.get("dates",None)
    file = request.FILES.get("file",None)
    cover = request.POST.get("cover",None)
    print(channel,store,country,spu,times,dates,file.name)
    # if dates == "24:00":
    #     now = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),"%Y-%m-%d")
    # else:
    #     now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    _date = times + "T" + dates
    # 先查询数据库是否存在
    sql = "select * from advertising_words_monitor where channel='%s' and store='%s' and country='%s' and spu='%s' and" \
          " times='%s';"%(channel,store,country,spu,_date)
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    if len(res) > 0 and cover is None:
        return JsonResponse({"code":403,"cover":1,"msg":"当天已存在此时间节点的数据，是否需要覆盖？"})
    else:
        try:
            # 读取文件内容,存入数据库
            path = "/static/data/advertising_data/" + store + country + "/" + _date
            print(path)
            creatDir(path)
            path1 = "/home/by_operate" + path + "/" + file.name
            with open(path1, "wb") as f:
                for line in file:
                    f.write(line)
            if cover is None:
                sql1 = "insert into advertising_words_monitor (channel,store,country,spu,times,key_word,matching_type,proposal_bidding," \
                       "key_word_bidding,exposure,click_num,click_rate,cost,every_click_free,order_num,sales_volume,acos) values "
                df = pd.read_csv(path1)
                for m in range(df.shape[0]):
                    middel = np.median([df.iloc[m, 4],df.iloc[m, 5],df.iloc[m, 6]])
                    sql1 += "('" + channel + "','" + store + "','" + country + "','" + spu + "','" + _date + "','" + str(df.iloc[m, 1]) + "','" + \
                            str(df.iloc[m, 2]) + "','" + str(middel) + "','" + str(df.iloc[m, 7]) + "','" + str(df.iloc[m, 8]) + "','" + \
                            str(df.iloc[m, 9]) + "','" + str(df.iloc[m, 10]) + "','" + str(df.iloc[m, 11]) + "','" + str(df.iloc[m, 12]) + "','" + \
                            str(df.iloc[m, 13]) + "','" + str(df.iloc[m, 14]) + "','" + str(df.iloc[m, 15]) + "'),"
                sql1 = sql1[:-1] + ";"
                conf_fun.connect_mysql_operation(sql1)
            else:
                df = pd.read_csv(path1)
                for m in range(df.shape[0]):
                    middel = np.median([df.iloc[m, 4], df.iloc[m, 5], df.iloc[m, 6]])
                    sql2 = "update advertising_words_monitor set matching_type='%s',proposal_bidding='%s',key_word_bidding='%s'," \
                           "exposure='%s',click_num='%s',click_rate='%s',cost='%s',every_click_free='%s',order_num='%s',sales_volume='%s',acos='%s' where " \
                           "channel='%s' and store='%s' and country='%s' and spu='%s' and times='%s' and key_word='%s';"%(str(df.iloc[m, 2]),str(middel),
                           str(df.iloc[m, 7]),str(df.iloc[m, 8]),str(df.iloc[m, 9]),str(df.iloc[m, 10]),str(df.iloc[m, 11]),str(df.iloc[m, 12]),str(df.iloc[m, 13]),
                           str(df.iloc[m, 14]),str(df.iloc[m, 15]),channel,store,country,spu,_date,str(df.iloc[m, 1]))
                    conf_fun.connect_mysql_operation(sql2)

            sql3 = "select * from advertising_words_monitor where times='%s';"%(_date)
            data = conf_fun.connect_mysql_operation(sql3,type='dict')
            return JsonResponse({"code":200,"msg":"success","data":data})
        except Exception as e:
            return JsonResponse({"code":500,"msg":"error:" + str(e)})


# 选择时间查找评分
def get_star_data(request):
    channel = request.POST.get("channel", None)
    store = request.POST.get("store", None)
    country = request.POST.get("country", None)
    spu = request.POST.get("spu", None)
    start_date = request.POST.get("start_date",None)
    end_strat = request.POST.get("end_date",None)
    try:
        _dic = get_star(store,country,spu,start_date,end_strat)
        return JsonResponse({"code":200,"msg":"success","data":_dic})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 更改日期请求排名数据
def get_rank_data(request):
    channel = request.POST.get("channel", None)
    store = request.POST.get("store", None)
    country = request.POST.get("country", None)
    spu = request.POST.get("spu", None)
    start_date = request.POST.get("start_date",None)
    end_date = request.POST.get("end_date",None)
    try:
        store1, country1 = store_country_code(store, country, 'en', type='upper')
        data = get_rank(store1,country,spu,start_date=start_date,end_date=end_date)
        return JsonResponse({"code": 200, "msg": "success", "data": data})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 广告指导编辑提交
def advertising_edit_submit(request):
    data = json.loads(request.POST.get("data",None))
    print("data===",data)
    # try:
    for i in data:
        # 先查询此数据是否存在
        sql = "select * from advertisement_guidance where channel='%s' and store='%s' and country='%s' and spu='%s' and dates='%s';"%(i["channel"],i["store"],i["country"],i["spu"],i["dates"])
        res = conf_fun.connect_mysql_operation(sql)
        if len(res) == 0:
            # 插入新数据
            sql1 = "insert into advertisement_guidance (channel,store,country,spu,dates,guidance_price_manual," \
                   "actual_price_manual,remark_manual,guidance_price_auto,actual_price_auto,remark_auto," \
                   "advertisement_proportion,advertisement_coefficient_manual,advertisement_coefficient_auto) values " \
                   "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(i["channel"],i["store"],
                    i["country"],i["spu"],i["dates"],i["guidance_price_manual"],i["actual_price_manual"],i["remark_manual"],
                    i["guidance_price_auto"],i["actual_price_auto"],i["remark_auto"],i["advertisement_proportion"],
                    i["advertisement_coefficient_manual"],i["advertisement_coefficient_auto"])

        else:
            sql1 = "update advertisement_guidance set guidance_price_manual='%s',actual_price_manual='%s'," \
                   "remark_manual='%s',guidance_price_auto='%s',actual_price_auto='%s',remark_auto='%s'," \
                   "advertisement_proportion='%s',advertisement_coefficient_manual='%s',advertisement_coefficient_auto='%s' where " \
                   "channel='%s' and store='%s' and country='%s' and spu='%s' and dates='%s';"%(i["guidance_price_manual"],
                    i["actual_price_manual"],i["remark_manual"],i["guidance_price_auto"],i["actual_price_auto"],
                    i["remark_auto"],i["advertisement_proportion"],i["advertisement_coefficient_manual"],
                    i["advertisement_coefficient_auto"],i["channel"],i["store"],i["country"],i["spu"],i["dates"])
        conf_fun.connect_mysql_operation(sql1)
    return JsonResponse({"code": 200, "msg": "编辑完成"})
    # except Exception as e:
    #     return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 更改时间请求广告词监控数据
def advertising_monitor_data(request):
    channel = request.POST.get("channel", None)
    store = request.POST.get("store", None)
    country = request.POST.get("country", None)
    spu = request.POST.get("spu", None)
    key_word = request.POST.get("key_word",None)
    dates = request.POST.get("dates",None)
    date_list = []
    if '_' in dates:
        # 选择一段时间
        start_date = dates.split('_')[0]
        end_date = dates.split('_')[1].split('T')[0]
        date1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        date2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while date1 <= date2:
            _str = datetime.datetime.strftime(date1, "%Y-%m-%d")
            date_list.append(_str + "T" + dates.split('_')[1].split('T')[1])
            date1 += datetime.timedelta(days=1)
        t = tuple(date_list)
        sql = "select * from advertising_words_monitor where channel='%s' and store='%s' " \
               "and country='%s' and spu='%s' and times in %s;"%(channel,store,country,spu,t)
    else:
        sql = "select * from advertising_words_monitor where channel='" + channel + "' and store='" + store + "' " \
        "and country='" + country + "' and spu='" + spu + "' and times like'%" + dates + "%';"
    try:
        res = conf_fun.connect_mysql_operation(sql,type='dict')
        datas = []
        if len(res) == 0:
            if '_' in dates:
                data_labels = date_list
            else:
                data_labels = ["10:00","14:00","17:00","24:00"]
            data = {
                "key_word": key_word,
                "proposal_bidding_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "key_word_bidding_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "exposure_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "click_num_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "click_rate_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "cost_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "every_click_free_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "order_num_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "sales_volume_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
                "acos_list": {"min": '0', "max": "0", "stepSize": "0", "data_labels": data_labels,"datas": []},
            }
            datas.append(data)
        else:
            # 先按时间排序
            res.sort(key=lambda x: x["times"])
            key_word_list = list(set([i["key_word"] for i in res]))
            if '_' in dates:
                data_labels = date_list
            else:
                data_labels = ["09:00","11:00","14:00","17:00","24:00"]
            for i in res:
                    proposal_bidding_list = []
                    key_word_bidding_list = []
                    exposure_list = []
                    click_num_list = []
                    click_rate_list = []
                    cost_list = []
                    every_click_free_list = []
                    order_num_list = []
                    sales_volume_list = []
                    acos_list = []
                    for j in key_word_list:
                        if i["key_word"] == j:
                            if i["proposal_bidding"] is None:
                                proposal_bidding_list.append(0)
                            else:
                                proposal_bidding_list.append(float(i["proposal_bidding"]))

                            if i["key_word_bidding"] is None:
                                key_word_bidding_list.append(0)
                            else:
                                key_word_bidding_list.append(float(i["key_word_bidding"]))

                            if i["exposure"] is None:
                                exposure_list.append(0)
                            else:
                                exposure_list.append(float(i["exposure"]))

                            if i["click_num"] is None:
                                click_num_list.append(0)
                            else:
                                click_num_list.append(float(i["click_num"]))

                            if i["click_rate"] is None:
                                click_rate_list.append(0)
                            else:
                                click_rate_list.append(float(i["click_rate"]))

                            if i["cost"] is None:
                                cost_list.append(0)
                            else:
                                cost_list.append(float(i["cost"]))

                            if i["every_click_free"] is None:
                                every_click_free_list.append(0)
                            else:
                                every_click_free_list.append(float(i["every_click_free"]))

                            if i["order_num"] is None:
                                order_num_list.append(0)
                            else:
                                order_num_list.append(float(i["order_num"]))

                            if i["sales_volume"] is None:
                                sales_volume_list.append(0)
                            else:
                                sales_volume_list.append(float(i["sales_volume"]))

                            if i["acos"] is None:
                                acos_list.append(0)
                            else:
                                acos_list.append(float(i["acos"]))

                    max1, stepSize1 = get_max_step(proposal_bidding_list)
                    max2, stepSize2 = get_max_step(key_word_bidding_list)
                    max3, stepSize3 = get_max_step(exposure_list)
                    max4, stepSize4 = get_max_step(click_num_list)
                    max5, stepSize5 = get_max_step(click_rate_list)
                    max6, stepSize6 = get_max_step(cost_list)
                    max7, stepSize7 = get_max_step(every_click_free_list)
                    max8, stepSize8 = get_max_step(order_num_list)
                    max9, stepSize9 = get_max_step(sales_volume_list)
                    max10, stepSize10 = get_max_step(acos_list)
                    data = {
                        "key_word":i["key_word"],
                        "proposal_bidding_list": {"min": '0', "max": max1, "stepSize": stepSize1, "data_labels": data_labels,
                                                  "datas": proposal_bidding_list},
                        "key_word_bidding_list": {"min": '0', "max": max2, "stepSize": stepSize2, "data_labels": data_labels,
                                                  "datas": key_word_bidding_list},
                        "exposure_list": {"min": '0', "max": max3, "stepSize": stepSize3, "data_labels": data_labels,
                                          "datas": exposure_list},
                        "click_num_list": {"min": '0', "max": max4, "stepSize": stepSize4, "data_labels": data_labels,
                                           "datas": click_num_list},
                        "click_rate_list": {"min": '0', "max": max5, "stepSize": stepSize5, "data_labels": data_labels,
                                            "datas": click_rate_list},
                        "cost_list": {"min": '0', "max": max6, "stepSize": stepSize6, "data_labels": data_labels,
                                      "datas": cost_list},
                        "every_click_free_list": {"min": '0', "max": max7, "stepSize": stepSize7, "data_labels": data_labels,
                                                  "datas": every_click_free_list},
                        "order_num_list": {"min": '0', "max": max8, "stepSize": stepSize8, "data_labels": data_labels,
                                           "datas": order_num_list},
                        "sales_volume_list": {"min": '0', "max": max9, "stepSize": stepSize9, "data_labels": data_labels,
                                              "datas": sales_volume_list},
                        "acos_list": {"min": '0', "max": max10, "stepSize": stepSize10, "data_labels": data_labels,
                                      "datas": acos_list},
                    }
                    datas.append(data)
        return JsonResponse({"code":200,"msg":"success","data":datas})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 广告监控编辑
def advertising_monitor_edit(request):
    data = request.POST.get("data",None)
    try:
        if data is not None:
            datas = json.loads(data)
            for i in datas:
                sql = "update advertising_words_monitor set acos_status='%s' and remarks='%s' where id=%s;"%(i["acos_status"],i["remarks"],i["id"])
                conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code": 200, "msg": "success"})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 广告管理一键同步广告指导
def advertisement_guidance_synchro(request):
    channel = request.POST.get("channel",None)
    station = request.POST.get("station", None)
    country = request.POST.get("channel", None)
    dates = request.POST.get("dates", None)
    datas = request.POST.get("datas",[])
    type = request.POST.get("type",None)
    if len(datas) > 0:
        datas = json.loads(datas)

    # 遍历存储数据
    for i in datas:
        # 先查询此spu此日期的数据是否存在
        sql = "select * from advertisement_guidance where channel='%s' and store='%s' and country='%s' and spu='%s' and dates='%s';"
        res = conf_fun.connect_mysql_operation(sql,type='dict')
        sql1 = ''
        if len(res) == 0:
            if type == 'guidance_price':
                sql1 = "insert into advertisement_guidance (channel,store,country,spu,dates,guidance_price_manual,guidance_price_auto) " \
                       "values ('%s','%s','%s','%s','%s','%s','%s')"%(channel,station,country,i["spu"],dates,i["guidance_price_manual"],i["guidance_price_auto"])
            else:
                sql1 = "insert into advertisement_guidance (channel,store,country,spu,dates,actual_price_manual,actual_price_auto,advertisement_proportion) " \
                       "values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (channel, station, country, i["spu"], dates, i["actual_price_manual"], i["actual_price_auto"],i["advertisement_proportion"])
        else:
            if type == 'guidance_price':
                sql1 = "update advertisement_guidance set guidance_price_manual='%s',guidance_price_auto='%s' where " \
                       "channel='%s' and store='%s' and country='%s' and spu='%s' and dates='%s';"%(i["guidance_price_manual"],i["guidance_price_auto"],channel,station,country,i["spu"],dates)
            else:
                sql1 = "update advertisement_guidance set actual_price_manual='%s',actual_price_auto='%s',advertisement_proportion='%s' where " \
                       "channel='%s' and store='%s' and country='%s' and spu='%s' and dates='%s';"%(i["actual_price_manual"], i["actual_price_auto"],i["advertisement_proportion"],channel,station,country,i["spu"],dates)
        conf_fun.connect_mysql_operation(sql1)
    return JsonResponse({"code":200,"msg":"success"})

#广告管理——店铺
# 获取国家站点
def advertising_shop_country(request):
    # 获取最近一个月的数据，提取国家站点
    channel = "Amazon"
    now = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=30),"%Y-%m-%d")
    try:
        sql = "select * from advertising_report where times>'%s';"%(now)
        res = conf_fun.connect_mysql_re(sql,type='dict')
        data = []
        for i in res:
            # 整理渠道、站点、国家数据
            if len(data) == 0:
                _dict = {
                    "channel":channel,
                    "station":i["company"],
                    "countries":[i["countries"]]
                }
                data.append(_dict)
            else:
                for index,j in enumerate(data):
                    if i["company"] == j["station"]:
                        j["countries"].append(i["countries"])
                        break
                    elif i["company"] != j["station"] and index == len(data)-1:
                        _dict = {
                            "channel": channel,
                            "station": i["company"],
                            "countries": [i["countries"]]
                        }
                        data.append(_dict)
                        break
        # 整理数据
        for item in data:
            _list = list(set(item["countries"]))
            _list1 = []
            for item1 in _list:
                store,country = store_country_code(item["station"],item1,'zh')
                item["station"] = store
                _list1.append(country)
            item["countries"] = _list1
        return JsonResponse({"code":200,"msg":"success","data":data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:"+str(e)})


# 获取广告监控数据
def advertising_shop_monitor_data(channel,station,country,dates=''):
    if channel == 'amazon':
        channel = 'Amazon'

    if '_' in dates:
        # 选择一段时间
        date_list = []
        start_date = dates.split('_')[0]
        end_date = dates.split('_')[1].split('T')[0]
        date1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        date2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while date1 <= date2:
            _str = datetime.datetime.strftime(date1, "%Y-%m-%d")
            date_list.append(_str + "T" + dates.split('_')[1].split('T')[1])
            date1 += datetime.timedelta(days=1)
        t = tuple(date_list)
        sql = "select * from advertising_shop_monitor where channel='%s' and station='%s' " \
              "and country='%s' and times in %s;" % (channel, station, country, t)
    else:
        date_list = ["10:00","14:00","17:00","24:00"]
        sql = "select * from advertising_shop_monitor where channel='" + channel + "' and station='" + station + "' " \
              "and country='" + country + "' and times like'%" + dates + "%';"
    print(sql)
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    print(len(res))
    # 手动组
    exposure_list = []
    click_num_list = []
    click_rate_list = []
    cost_list = []
    click_cost_list = []
    order_num_list = []
    sales_list = []
    acos_list = []
    datas = []
    data = {}
    # 自动组
    exposure_list1 = []
    click_num_list1 = []
    click_rate_list1 = []
    cost_list1 = []
    click_cost_list1 = []
    order_num_list1 = []
    sales_list1 = []
    acos_list1 = []
    datas1 = []
    data1 = {}
    if len(res) == 0:
        data = {
            "datas": datas,
            "exposure_list": exposure_list,
            "click_num_list": click_num_list,
            "click_rate_list": click_rate_list,
            "cost_list": cost_list,
            "click_cost_list": click_cost_list,
            "order_num_list": order_num_list,
            "sales_list": sales_list,
            "acos_list": acos_list
        }
        data1 = {
            "datas": datas1,
            "exposure_list": exposure_list1,
            "click_num_list": click_num_list1,
            "click_rate_list": click_rate_list1,
            "cost_list": cost_list1,
            "click_cost_list": click_cost_list1,
            "order_num_list": order_num_list1,
            "sales_list": sales_list1,
            "acos_list": acos_list1
        }
    else:
        # 先按时间排序
        res.sort(key=lambda x:x["times"])
        for i in res:
            if i["launch"] == "MANUAL":
                if "T10:00" in i["times"]:
                    datas.append(i)
                exposure_list.append(int(i["exposure"]))
                click_num_list.append(int(i["click_num"]))
                click_rate_list.append(float(i["click_rate"]))
                cost_list.append(float(i["cost"]))
                click_cost_list.append(float(i["click_cost"]))
                order_num_list.append(int(i["order_num"]))
                sales_list.append(float(i["sales"]))
                acos_list.append(float(i["acos"]))
            else:
                if "T10:00" in i["times"]:
                    datas1.append(i)
                exposure_list1.append(int(i["exposure"]))
                click_num_list1.append(int(i["click_num"]))
                click_rate_list1.append(float(i["click_rate"]))
                cost_list1.append(float(i["cost"]))
                click_cost_list1.append(float(i["click_cost"]))
                order_num_list1.append(int(i["order_num"]))
                sales_list1.append(float(i["sales"]))
                acos_list1.append(float(i["acos"]))

        data_labels =  date_list
        # 手动组
        max1, stepSize1 = get_max_step(exposure_list) if len(exposure_list) > 0 else 0,0
        max2, stepSize2 = get_max_step(click_num_list) if len(click_num_list) > 0 else 0,0
        max3, stepSize3 = get_max_step(click_rate_list) if len(click_rate_list) > 0 else 0,0
        max4, stepSize4 = get_max_step(cost_list) if len(cost_list) > 0 else 0,0
        max5, stepSize5 = get_max_step(click_cost_list) if len(click_cost_list) > 0 else 0,0
        max6, stepSize6 = get_max_step(order_num_list) if len(order_num_list) > 0 else 0,0
        max7, stepSize7 = get_max_step(sales_list) if len(sales_list) > 0 else 0,0
        max8, stepSize8 = get_max_step(acos_list) if len(acos_list) > 0 else 0,0
        # 自动组
        max9, stepSize9 = get_max_step(exposure_list1) if len(exposure_list1) > 0 else 0,0
        max10, stepSize10 = get_max_step(click_num_list1) if len(click_num_list1) > 0 else 0,0
        max11, stepSize11 = get_max_step(click_rate_list1) if len(click_rate_list1) > 0 else 0,0
        max12, stepSize12 = get_max_step(cost_list1) if len(cost_list1) > 0 else 0,0
        max13, stepSize13 = get_max_step(click_cost_list1) if len(click_cost_list1) > 0 else 0,0
        max14, stepSize14 = get_max_step(order_num_list1) if len(order_num_list1) > 0 else 0,0
        max15, stepSize15 = get_max_step(sales_list1) if len(sales_list1) > 0 else 0,0
        max16, stepSize16 = get_max_step(acos_list1) if len(acos_list1) > 0 else 0,0
        data = {
            "datas":datas,
            "exposure_list":{"min":'0',"max":max1,"stepSize":stepSize1,"data_labels":data_labels,"datas":exposure_list},
            "click_num_list": {"min":'0',"max":max2,"stepSize":stepSize2,"data_labels":data_labels,"datas":click_num_list},
            "click_rate_list": {"min":'0',"max":max3,"stepSize":stepSize3,"data_labels":data_labels,"datas":click_rate_list},
            "cost_list": {"min":'0',"max":max4,"stepSize":stepSize4,"data_labels":data_labels,"datas":cost_list},
            "click_cost_list": {"min":'0',"max":max5,"stepSize":stepSize5,"data_labels":data_labels,"datas":click_cost_list},
            "order_num_list": {"min":'0',"max":max6,"stepSize":stepSize6,"data_labels":data_labels,"datas":order_num_list},
            "sales_list": {"min":'0',"max":max7,"stepSize":stepSize7,"data_labels":data_labels,"datas":sales_list},
            "acos_list": {"min":'0',"max":max8,"stepSize":stepSize8,"data_labels":data_labels,"datas":acos_list},
        }
        data1 = {
            "datas": datas1,
            "exposure_list": {"min": '0', "max": max9, "stepSize": stepSize9, "data_labels": data_labels,"datas": exposure_list1},
            "click_num_list": {"min": '0', "max": max10, "stepSize": stepSize10, "data_labels": data_labels,"datas": click_num_list1},
            "click_rate_list": {"min": '0', "max": max11, "stepSize": stepSize11, "data_labels": data_labels,"datas": click_rate_list1},
            "cost_list": {"min": '0', "max": max12, "stepSize": stepSize12, "data_labels": data_labels,"datas": cost_list1},
            "click_cost_list": {"min": '0', "max": max13, "stepSize": stepSize13, "data_labels": data_labels,"datas": click_cost_list1},
            "order_num_list": {"min": '0', "max": max14, "stepSize": stepSize14, "data_labels": data_labels,"datas": order_num_list1},
            "sales_list": {"min": '0', "max": max15, "stepSize": stepSize15, "data_labels": data_labels,"datas": sales_list1},
            "acos_list": {"min": '0', "max": max16, "stepSize": stepSize16, "data_labels": data_labels,"datas": acos_list1},
        }
    return res,data,data1


# 获取数据
def advertising_shop(request):
    company = request.GET.get("station",None)
    country = request.GET.get("country",None)
    store1,country1 = store_country_code(company,country,'en','upper')
    # 默认获取七天的spu广告数据
    now = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1),"%Y-%m-%d")
    date_list = get_days(now,7)
    t = tuple(date_list)
    sql = "select * from advertising_report where company='%s' and countries='%s' and times in %s;"%(store1,country1,t)
    res = conf_fun.connect_mysql_re(sql,type='dict')
    print("res===",res)
    sql1 = "select * from advertisement_group;"
    res1 = conf_fun.connect_mysql_operation(sql1,type='dict')

    today_data = []
    _dic = {
        "sales": 0,
        "advertising_costs": 0,
        "cost_rate": 0,
        "manual_acos": 0,
        "auto_acos": 0,
    }
    print("now===",now)
    for i in res:
        # 获取当天的数据
        if i["times"] == now:
            _dic["sales"] += float(i["sales"])
            _dic["advertising_costs"] += float(i["advertising_costs"])
            _dic["cost_rate"] += float(i["cost_rate"].split('%')[0])
            _dict = {
                "spu":i["spu"],
                "sales":round(float(i["sales"]),2),
                "advertising_costs":round(float(i["advertising_costs"]),2),
                "cost_rate":i["cost_rate"],
                "manual_acos":0,
                "auto_acos":0,
                "days_sales_data": [0] * len(date_list),
                "days_advertising_costs_data": [0] * len(date_list),
                "days_cost_rate_data": [0] * len(date_list),
                "days_manual_acos_data": [0] * len(date_list),
                "days_auto_acos_data": [0] * len(date_list)
            }
            if i["total_sales"] is not None:
                # 判断当前spu是手动组还是自动组
                for j in res1:
                    if i["spu"] == j["spu"]:
                        if j["group_type"] == "手动组":
                            _dict["manual_acos"] = round(i["advertising_costs"]/i["total_sales"], 2)
                            _dic["manual_acos"] += round(i["advertising_costs"]/i["total_sales"], 2)
                        else:
                            _dict["auto_acos"] = round(i["advertising_costs"] / i["total_sales"], 2)
                            _dic["auto_acos"] += round(i["advertising_costs"] / i["total_sales"], 2)
            today_data.append(_dict)
    _dic["cost_rate"] = str(round(_dic["cost_rate"],2)) + '%'
    _dic["advertising_costs"] = round(_dic["advertising_costs"],2)
    _dic["sales"] = round(_dic["sales"], 2)
    today_data.insert(0,_dic)

    print("today_data===",today_data)
    # 获取图表数据
    for index1,i in enumerate(today_data):
        if index1 > 0:
            for index,j in enumerate(date_list):
                for item in res:
                    if i["spu"] == item["spu"] and item["times"] == j:
                        i["days_sales_data"][index] = item["sales"]
                        i["days_advertising_costs_data"][index] = round(float(item["advertising_costs"]),2)
                        i["days_cost_rate_data"][index] = item["cost_rate"]

                        if item["total_sales"] is not None:
                            # 判断当前spu是手动组还是自动组
                            for item1 in res1:
                                if item["spu"] == item1["spu"]:
                                    if item1["group_type"] == "手动组":
                                        i["manual_acos"] = round(item["advertising_costs"] / item["total_sales"], 2)
                                    else:
                                        i["auto_acos"] = round(item["advertising_costs"] / item["total_sales"], 2)

    # 获取广告监控数据
    _list,data,data1 = advertising_shop_monitor_data('Amazon',company,country)
    return JsonResponse({"code":200,"msg":"success","today_data":today_data,"date_list":date_list,"advertising_data":_list,"manual_data":data,"auto_data":data1})


# 改变时间获取某个spu的数据
def get_spu_advertising_data(request):
    channel = request.POST.get("channel",None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    spu = request.POST.get("spu", None)
    start_time = request.POST.get("start_time", None)
    end_time = request.POST.get("end_time", None)
    # 获取开始日期和结束日期之间的所有日期
    start_time = datetime.datetime.strptime(start_time,"%Y-%m-%d")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
    date_list = []
    while start_time <= end_time:
        _str = datetime.datetime.strftime(start_time, "%Y-%m-%d")
        date_list.append(_str)
        start_time += datetime.timedelta(days=1)
    t = tuple(date_list)
    # 查询数据
    store1,country1 = store_country_code(station,country,'en','upper')
    sql = "select * from advertising_report where company='%s' and countries='%s' and spu='%s' and times in %s;"%(store1,country1,spu,t)
    res = conf_fun.connect_mysql_re(sql,type='dict')

    sql1 = "select * from advertisement_group;"
    res1 = conf_fun.connect_mysql_operation(sql1, type='dict')

    # 整理数据
    # 先排序
    if len(res) > 0:
        res.sort(key=lambda x:x["times"])

    _dict = {
        "spu": spu,
        "days_sales_data": [0] * len(date_list),
        "days_advertising_costs_data": [0] * len(date_list),
        "days_cost_rate_data": [0] * len(date_list),
        "days_manual_acos_data": [0] * len(date_list),
        "days_auto_acos_data": [0] * len(date_list)
    }
    for index,i in enumerate(date_list):
        for j in res:
            if i == j["times"]:
                _dict["days_sales_data"][index] = round(float(j["sales"]),2)
                _dict["days_advertising_costs_data"][index] = round(float(j["advertising_costs"]), 2)
                _dict["days_cost_rate_data"][index] = round(float(j["cost_rate"].split('%')[0]), 2)
                if j["total_sales"] is not None:
                    # 判断当前spu是手动组还是自动组
                    for item in res1:
                        if j["spu"] == item["spu"]:
                            if j["group_type"] == "手动组":
                                _dict["days_manual_acos_data"][index] = round(j["advertising_costs"] / j["total_sales"], 2)
                            else:
                                _dict["days_auto_acos_data"][index] = round(j["advertising_costs"] / j["total_sales"], 2)

    return JsonResponse({"code":200,"msg":"success","data":_dict,"date_list":date_list})


# 店铺广告管理上传数据
def upload_advertising_shop_data(request):
    channel = request.POST.get("channel", None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    times = request.POST.get("times", None)
    dates = request.POST.get("dates", None)
    file = request.FILES.get("file", None)
    cover = request.POST.get("cover", None)
    print(channel, station, country, times, dates, file.name)

    # if dates == "24:00":
    #     now = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1), "%Y-%m-%d")
    # else:
    #     now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    _date = times + "T" + dates
    # 先查询数据库是否存在
    sql = "select * from advertising_shop_monitor where channel='%s' and station='%s' and country='%s' and" \
          " times='%s';" % (channel, station, country, _date)
    print(sql)
    res = conf_fun.connect_mysql_operation(sql, type='dict')
    if len(res) > 0 and cover is None:
        return JsonResponse({"code": 403, "cover": 1, "msg": "当天已存在此时间节点的数据，是否需要覆盖？"})
    else:
        try:
            # 读取文件内容,存入数据库
            path = "/static/data/advertising_shop_data/" + station + country + "/" + _date
            print(path)
            creatDir(path)
            path1 = "/home/by_operate" + path + "/" + file.name
            with open(path1, "wb") as f:
                for line in file:
                    f.write(line)
            if cover is None:
                sql1 = "insert into advertising_shop_monitor (channel,station,country,advertising_campaign,launch,times,budget,exposure,click_num," \
                       "click_rate,cost,click_cost,order_num,sales,acos) values "
                if 'csv' in file.name:
                    df = pd.read_csv(path1)
                elif 'xlsx' in file.name or 'xls' in file.name or 'excel' in file.name:
                    df = pd.read_excel(path1)
                for m in range(df.shape[0]):
                    sql1 += "('" + channel + "','" + station + "','" + country + "','" + str(df.iloc[m, 1]) + "','" + \
                            str(df.iloc[m, 4]) + "','" + _date + "','" + str(df.iloc[m, 9]) + "','" + str(
                        df.iloc[m, 10]) + "','" + \
                            str(df.iloc[m, 11]) + "','" + str(df.iloc[m, 12]) + "','" + str(
                        df.iloc[m, 13]) + "','" + str(df.iloc[m, 14]) + "','" + \
                            str(df.iloc[m, 15]) + "','" + str(df.iloc[m, 16]) + "','" + str(df.iloc[m, 17]) + "'),"
                sql1 = sql1[:-1] + ";"
                conf_fun.connect_mysql_operation(sql1)
            else:
                if 'csv' in file.name:
                    df = pd.read_csv(path1)
                elif 'xlsx' in file.name or 'xls' in file.name or 'excel' in file.name:
                    df = pd.read_excel(path1)
                for m in range(df.shape[0]):
                    sql2 = "update advertising_shop_monitor set advertising_campaign='%s',launch='%s',budget='%s'," \
                           "exposure='%s',click_num='%s',click_rate='%s',cost='%s',click_cost='%s',order_num='%s',sales='%s',acos='%s' where " \
                           "channel='%s' and station='%s' and country='%s' and times='%s';" % (
                               str(df.iloc[m, 1]), str(df.iloc[m, 4]),
                               str(df.iloc[m, 9]), str(df.iloc[m, 10]), str(df.iloc[m, 11]), str(df.iloc[m, 12]),
                               str(df.iloc[m, 13]), str(df.iloc[m, 14]), str(df.iloc[m, 15]),
                               str(df.iloc[m, 16]), str(df.iloc[m, 17]), channel, station, country, _date)
                    conf_fun.connect_mysql_operation(sql2)

            sql3 = "select * from advertising_shop_monitor where station='%s' and country='%s' and times='%s';" % (
            station, country, _date)
            data = conf_fun.connect_mysql_operation(sql3, type='dict')
            return JsonResponse({"code": 200, "msg": "success", "data": data})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 改变时间选择店铺广告监控数据
def choose_advertising_shop_data(request):
    channel = request.POST.get("channel", None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    dates = request.POST.get("dates", None)
    print(dates)
    # store1, country1 = store_country_code(station, country, 'en', 'upper')

    # 获取广告监控数据
    _list, data, data1 = advertising_shop_monitor_data(channel, station, country,dates=dates)
    return JsonResponse({"code":200,"msg":"success","advertising_data":_list,"manual_data":data,"auto_data":data1})


# 店铺广告管理数据编辑
def edit_advertising_shop_data(request):
    data = request.POST.get("data",[])
    if len(data) > 0:
        data = json.loads(data)

    # 遍历修改
    for i in data:
        sql = "update advertising_shop_monitor set acos_status='%s' and remarks='%s' where id='%s';"%(i["acos_status"],i["remarks"],i["id"])
        conf_fun.connect_mysql_operation(sql)
    return JsonResponse({"code":200,"msg":"编辑成功"})


# ---------------->FBM
# 海外仓手动发货——excel
def yc_batch_create_order(request):
    file = request.FILES.get('files')
    millis = str(round(time.time() * 1000))
    with open('/home/by_operate/static/data/order_data/order_upload/' + millis + '.xlsx', "wb") as f:
        for line in file:
            f.write(line)

    df = pd.read_excel('/home/by_operate/static/data/order_data/order_upload/' + millis + '.xlsx',
                       dtype={'phone': str, 'zipcode': str})
    order_codes = []
    err_data = []
    for i in range(df.shape[0]):

        dates = str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H-%M'))
        df.iloc[i, 3] = df.iloc[i, 3].replace("'", " ")
        df.iloc[i, 3] = df.iloc[i, 3].replace("\n", " ")
        df.iloc[i, 0] = df.iloc[i, 0].replace(" ", "")

        sql1 = "select * from manually_create_order_yc where reference_no='{}'"
        sql1 = sql1.format(df.iloc[i, 0])
        sql_data = conf_fun.connect_mysql_re(sql1, dbs='order')
        if len(sql_data) == 0:
            err_data.append([df.iloc[i, 0], "数据库缺失该数据!"])
            continue

        order = df.iloc[i, 0].replace(" ", "")
        city = df.iloc[i, 2].replace("'", " ")

        name = df.iloc[i, 4].replace("'", " ")
        address = df.iloc[i, 3]

        # 处理电话号码
        tel = re.sub("\D", "", str(df.iloc[i, 5]))

        if len(name) > 29:
            err_data.append([order, "名字超长!,有" + str(len(name)) + '长度: ' + name])
            sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                  " ('{}','{}','{}','{}','{}','{}','{}','{}')"
            sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6],
                             "名字有" + str(len(name) + '长度'))
            conf_fun.connect_mysql_re(sql, dbs='order')
            continue

        if len(address) > 58:
            err_data.append([order, "地址超长!,有" + str(len(address)) + '长度: ' + address])
            sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                  " ('{}','{}','{}','{}','{}','{}','{}','{}')"
            sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6], "地址有" + str(len(address) + '长度'))
            conf_fun.connect_mysql_re(sql, dbs='order')
            continue

        if '-ABCDEF' in sql_data[0][11]:
            sku = sql_data[0][11].split('-ABCDEF')[0]
        else:
            sku = sql_data[0][11]

        sql = "select yy_sku from sku_comparison where an_sku='{}'"
        sql = sql.format(sku)
        print(sql)
        zr_sku_data = conf_fun.connect_mysql_re(sql, dbs='order')
        if len(zr_sku_data) > 0:
            sku = zr_sku_data[0][0]

        sql = "select product_declared_name,product_declared_value from warehouse_product_yc where product_sku='{}'"
        sql = sql.format(sku)

        sku_data = conf_fun.connect_mysql_re(sql, dbs='order')

        try:
            items = [{"product_sku": sku, "reference_no": sql_data[0][13], "product_name_en": sku_data[0][0],
                      "product_declared_value": str(sku_data[0][1]), "quantity": sql_data[0][12]}]
        except:
            err_data.append([order, "没有该SKU"])
            continue

        sql = "select product_length,product_width,product_height from warehouse_product_yc where product_sku='{}'"
        sql = sql.format(sku)
        try:
            product_size = conf_fun.connect_mysql_re(sql, dbs='order')
            product_length = product_size[0][0]
            product_width = product_size[0][1]
            product_height = product_size[0][2]
            girth = (float(product_width) + float(product_height)) * 2 + float(product_length)
        except:
            err_data.append([order, "没有该SKU的详细数据!"])
            continue
        if df.iloc[i, 1] in ['GB', 'IE', 'JE', 'GY']:

            zip_code_2 = str(sql_data[0][10])[:2]
            zip_code_3 = str(sql_data[0][10]).split(' ')[0]
            sql = "select * from zip_data"
            zipdata = conf_fun.connect_mysql_re(sql, dbs='order')
            zip_data = [x[0] for x in zipdata]
            if df.iloc[i, 1] not in ['GB', 'IE', 'JE', 'GY']:
                if (float(product_length) > 175 or float(product_width) > 175 or float(product_height) > 175) or girth > 300:
                    shipment_method = 'GB-DPD-EU-LL'
                else:
                    shipment_method = 'DPDEU'
            else:
                if df.iloc[i, 23] in ['JE', 'GY']:
                    shipment_method = 'GB-DPD-USC'
                else:
                    if zip_code_3 in zip_data or df.iloc[i, 1] in ['IE']:
                        if float(product_length) >= 100 or float(product_width) >= 70 or float(product_height) >= 60:
                            shipment_method = 'GB-DPD-UK2-LL'
                        else:
                            shipment_method = 'GB-DPD-IRL'
                    elif zip_code_2 in ['IV', 'PA', 'ZE', 'TR', 'BT']:
                        if float(product_length) > 100 or float(product_width) > 70 or float(product_height) > 60:
                            shipment_method = 'GB-DPD-UKN-LL'
                        else:
                            shipment_method = 'GB-DPD-ZONE1'
                    else:
                        if float(product_length) > 140 or float(product_width) > 80 or float(product_height) > 80:
                            shipment_method = 'GB_DHL_L_PAR'
                        else:
                            shipment_method = 'GB-DHL'

            sql = "select order_code from manually_create_order_yc where reference_no='{}'"
            sql = sql.format(order)
            res_data = conf_fun.connect_mysql_re(sql, dbs='order')

            if res_data[0][0] is not None and res_data[0][0] != '':
                continue

            res = could_yc.create_order(sql_data[0][1], shipment_method, sql_data[0][3], df.iloc[i, 1], '', city,
                                        name, tel, address, str(sql_data[0][10]), items)

            obj = re.compile('>\{(.*?)\}<')
            ret = obj.search(res.text)
            try:
                res_data = ret.group()[1:-1]
            except:
                sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                      " ('{}','{}','{}','{}','{}','{}','{}','{}')"
                sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6], res.text)
                conf_fun.connect_mysql_re(sql, dbs='order')
                err_data.append([order, "ERROR！"])
                continue
            res_data_dict = json.loads(res_data)
            if res_data_dict['ask'] == 'Failure':
                sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                      " ('{}','{}','{}','{}','{}','{}','{}','{}')"
                sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6],
                                 res_data_dict['Error']['errMessage'])
                conf_fun.connect_mysql_re(sql, dbs='order')
                err_data.append([order, res_data_dict['Error']['errMessage']])
                continue

            sql = "update manually_create_order_yc set country_code='{}',city='{}',name='{}',phone='{}',address1='{}',"\
                  "zipcode='{}',order_code='{}',dates='{}',shipping_method='{}' where reference_no='{}'"
            sql = sql.format(df.iloc[i, 1], city, name, tel, address, sql_data[0][10], res_data_dict['order_code'],
                             dates, shipment_method, order)
            conf_fun.connect_mysql_re(sql, dbs='order')
            order_codes.append(order)
        else:
            door = '-'
            if sku not in ['ZR-LDTW40-C5', 'ZR-LDTW47-C5']:
                if df.iloc[i, 1] in ['FR', 'IT', 'ES']:
                    if float(product_length) < 130 and float(product_width) < 80 and float(product_height) < 30:
                        shipment_method = 'DE_DPD_EU_DR'
                    else:
                        shipment_method = 'DE_GLS_LL'
                elif df.iloc[i, 1] == 'DE':
                    if float(product_length) < 120 and float(product_width) < 60 and float(product_height) < 60:
                        shipment_method = 'DHL_DE_DR'
                    elif float(product_length) < 130 and float(product_width) < 80 and float(product_height) < 80:
                        shipment_method = 'DE_DPD_DR'
                    else:
                        shipment_method = 'DE_GLS_LL'
                else:
                    if min([float(product_length), float(product_width), float(product_height)]) < 120:
                        shipment_method = 'DE_GLS'
                    else:
                        shipment_method = 'DE_GLS_LL'

                sql = "select order_code from manually_create_order_yc where reference_no='{}'"
                sql = sql.format(order)
                res_data = conf_fun.connect_mysql_re(sql, dbs='order')

                if res_data[0][0] is not None and res_data[0][0] != '':
                    continue

                res = could_yc.create_order_de(sql_data[0][1], shipment_method, 'DEPJ', df.iloc[i, 1], '', city,
                                               name, tel, address, str(sql_data[0][10]), items, door)

                obj = re.compile('>\{(.*?)\}<')
                ret = obj.search(res.text)
                try:
                    res_data = ret.group()[1:-1]
                except:
                    sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                          " ('{}','{}','{}','{}','{}','{}','{}','{}')"
                    sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6], res.text)
                    conf_fun.connect_mysql_re(sql, dbs='order')
                    err_data.append([order, "ERROR！"])
                    continue
                res_data_dict = json.loads(res_data)
                print(res_data_dict)
                if res_data_dict['ask'] == 'Failure':
                    sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                          " ('{}','{}','{}','{}','{}','{}','{}','{}')"
                    sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6], res.text)
                    conf_fun.connect_mysql_re(sql, dbs='order')
                    err_data.append([order, res_data_dict['Error']['errMessage']])
                    continue

                sql = "update manually_create_order_yc set country_code='{}',city='{}',name='{}',phone='{}'," \
                      "address1='{}',zipcode='{}',order_code='{}',dates='{}',shipping_method='{}'," \
                      "warehouse_code='{}' where reference_no='{}'"
                sql = sql.format(df.iloc[i, 1], city, name, tel, address, sql_data[0][10],
                                 res_data_dict['order_code'], dates, shipment_method, 'DEPJ', order)
                print(sql)
                conf_fun.connect_mysql_re(sql, dbs='order')
                order_codes.append(order)
            else:
                print(df.iloc[i, 1])
                res = could_sf.create_order(str(order), str(df.iloc[i, 1]), 'DEDCB', 'D29', name, city, '', address,
                                            str(sql_data[0][10]), str(tel), sku, '1', door)
                print('res:', res)
                obj = re.compile('code=(.*?)&')
                ret = obj.search(str(res))
                try:
                    print(ret.group())
                    res_data = ret.group()[6:-2]
                except:
                    sql = "insert into err_order_data(order_id,country_code,city,address,name,tel,zip_code,reason) values" \
                          " ('{}','{}','{}','{}','{}','{}','{}','{}')"
                    sql = sql.format(order, df.iloc[i, 1], city, address, name, tel, df.iloc[i, 6], res)
                    conf_fun.connect_mysql_re(sql, dbs='order')
                    err_data.append([order, "ERROR！"])
                    continue
                sql = "update manually_create_order_yc set country_code='{}',city='{}',name='{}',phone='{}'," \
                      "address1='{}',zipcode='{}',order_code='{}',dates='{}',shipping_method='{}'," \
                      "warehouse_code='{}' where reference_no='{}'"
                sql = sql.format(df.iloc[i, 1], city, name, tel, address, sql_data[0][10], res_data, dates,
                                 'D29', 'DEDCB', order)
                print(sql)
                conf_fun.connect_mysql_re(sql, dbs='order')
                order_codes.append(order)

    if len(err_data) == 0:
        return JsonResponse({"code": 200, "msg": "订单创建成功!订单号为: " + str(order_codes)})
    else:
        err_str = ''
        for i in err_data:
            err_str += '订单号为' + i[0] + ',错误原因为:' + i[1] + ','
        return JsonResponse({"code": 200, "msg": "如下订单创建成功,订单号为: " + str(order_codes) + "如下订单创建失败:" + err_str})


# txt上传订单
def txt_order(request):
    file = request.FILES.get('files')
    if 'ZR' in file.name:
        station = 'ZR'
    elif 'AN' in file.name:
        station = 'AN'
    elif 'JH' in file.name:
        station = 'JH'
    else:
        return JsonResponse({"code": 400, "msg": '文件名错误!'})
    millis = str(round(time.time() * 1000))
    with open('/home/by_operate/static/data/order_data/order_upload/' + millis + '.txt', "wb") as f:
        for line in file:
            f.write(line)
    try:
        df = pd.read_table('/home/by_operate/static/data/order_data/order_upload/' + millis + '.txt')
    except:
        return JsonResponse({"code": 400, "msg": '文件格式有问题,请换成utf-8格式再进行上传!'})
    try:
        dfs = df['order-id'].value_counts()
    except:
        return JsonResponse({"code": 400, "msg": '联系IT处理!'})

    list1 = []
    list2 = []
    list3 = []
    list4 = []

    order_lis = []

    for i in range(df.shape[0]):
        order_num = 1
        for j in range(0, int(df.iloc[i, 12])):
            try:
                if int(df.iloc[i, 12]) > 1 or dfs[df.iloc[i, 0]] > 1:
                    for k in order_lis:
                        if df.iloc[i, 0] == k:
                            order_num += 1
                            break
                    if order_num > 1:
                        order = df.iloc[i, 0] + '-' + str(order_num)
                        order_lis.append(df.iloc[i, 0])
                    else:
                        order = df.iloc[i, 0] + '-1'
                        order_lis.append(df.iloc[i, 0])
                else:
                    order = df.iloc[i, 0]

                dates = str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H-%M'))

                # 获取门牌号
                if df.iloc[i, 23] not in ['GB', 'IE', 'JE', 'GY']:
                    doorplate, address, address2 = get_house_number(df.iloc[i, 17], df.iloc[i, 18])
                else:
                    doorplate = '-'
                    address = str(df.iloc[i, 17])
                    address2 = str(df.iloc[i, 18])
                true_site = str(df.iloc[i, 17])
                if address2 == 'nan' or address2 is None or address2 == '':
                    address += ''
                    true_site += ''
                else:
                    address += ' ' + str(address2)
                    true_site += ' ' + str(df.iloc[i, 18])
                if df.iloc[i, 19] == 'nan' or df.iloc[i, 19] is None or df.iloc[i, 19] == '':
                    address += ''
                    true_site += ''
                else:
                    address += ' ' + str(df.iloc[i, 19])
                    true_site += ' ' + str(df.iloc[i, 19])
                address = address.replace("'", " ")
                address = address.replace("&", " and ")
                true_site = true_site.replace("'", " ")
                true_site = true_site.replace("&", " and ")
                address = address.replace("\n", " ")
                if address[-3:] == 'nan':
                    address = address[:-3]
                if address[-3:] == 'nan':
                    address = address[:-3]

                order = order.replace(" ", "")
                city = df.iloc[i, 20].replace("'", " ")

                # 处理电话号码
                tel = re.sub("\D", "", str(df.iloc[i, 9]))

                # 查询是否发过
                if len(order) > 19:
                    sql = "select order_code,is_bad from manually_create_order_yc where reference_no like '{}'"
                    sql = sql.format(order + '%')
                else:
                    sql = "select order_code,is_bad from manually_create_order_yc where reference_no='{}'"
                    sql = sql.format(order)
                res_data1 = conf_fun.connect_mysql_re(sql, dbs='order')
                try:
                    if (res_data1[0][0] is not None and res_data1[0][0] != '') or res_data1[0][1] in ('3', '4'):
                        list3.append(order)
                        continue
                except:
                    pass

                name = df.iloc[i, 16].replace("'", " ")

                sql = "select id from manually_create_order_yc where reference_no='{}'"
                sql = sql.format(order)
                id_res = conf_fun.connect_mysql_re(sql, dbs='order')
                if len(id_res) > 0:
                    sql = "update manually_create_order_yc set country_code='{}',city='{}',name='{}',phone='{}'," \
                          "address1='{}',zipcode='{}',is_bad='1',doorplate='{}',true_site='{}' where reference_no='{}'"

                    sql = sql.format(df.iloc[i, 23], city, name, tel, address, df.iloc[i, 22], doorplate, true_site, order)
                    print(sql)
                    conf_fun.connect_mysql_re(sql, dbs='order')
                    list1.append(order)
                    
                else:
                    sql = "insert into manually_create_order_yc(reference_no,country_code,city,name,phone,address1," \
                          "zipcode,product_sku,quantity,reference_no1,ShipmentServiceLevelCategory,OrderItemId," \
                          "reference_ture,get_dates,station,is_bad,doorplate,true_site) values ('{}','{}','{}','{}','{}','{}'," \
                          "'{}','{}','{}','{}','{}','{}','{}','{}','{}','1','{}','{}')"
                    sql = sql.format(order, df.iloc[i, 23], city, name, tel, address, df.iloc[i, 22], df.iloc[i, 10],
                                     '1', df.iloc[i, 23] + order, df.iloc[i, 15], df.iloc[i, 1], df.iloc[i, 0], dates,
                                     station, doorplate, true_site)
                    print(sql)
                    conf_fun.connect_mysql_re(sql, dbs='order')
                    list2.append(order)
            except:
                list4.append(df.iloc[i, 0])

    return JsonResponse({"code": 200, "msg": "更新成功!,更新了如下订单:" + str(list1) + "新增了如下订单:" + str(list2)
                        + "跳过了如下订单:" + str(list3) + "未上传成功如下订单:" + str(list4) + "共有" + str(df.shape[0]) + "条数据"})


# 下载错误报告
def download_err_report(request):
    path = '/home/by_operate/static/data/order_data/address_longer/地址超长.xlsx'
    files = open(path, 'rb')
    response = FileResponse(files)
    response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote('地址超长.xlsx')
    return response


# 文件上传
def upload_file(request):
    files = request.FILES.get('files')
    file_name = files.name
    now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    path = '/static/data/orders/DE_SF/' + now
    creatDir(path)
    path1 = '/home/by_operate' + path + "/" + file_name
    # path2 = os.path.join(r'static/data/Germany_S_F/', str(file_name))
    # path = os.path.join(os.getcwd(), path2)
    with open(path1, 'wb') as f:
        for line in files:
            f.write(line)
    return path1


# 海外仓问题订单
def get_warehouse(request):
    # 查询所有的订单
    # try:
    sql = "select * from problem_data order by id limit 0,200;"
    data = conf_fun.connect_mysql_or(sql,type='dict')
    warehouse_list = list(set([i["common_carrier"] for i in data])) if len(data) > 0 else []

    _list = []
    _list1 = []
    type_list = []
    for i in data:
        type_list.append(i["state"])
        if len(_list) == 0:
            _dic = {
                "warehouse":i["common_carrier"],
                "country":[i["country"]]
            }
            _list.append(_dic)
        else:
            for index,j in enumerate(_list):
                if i["common_carrier"] == j["warehouse"]:
                    j["country"].append(i["country"])
                    break
                elif i["common_carrier"] != j["warehouse"] and index == len(_list)-1:
                    _dic = {
                        "warehouse": i["common_carrier"],
                        "country": [i["country"]]
                    }
                    _list.append(_dic)
                    break

        if len(_list1) == 0:
            _dic1 = {
                "country":i["country"],
                "orderid":[i["orderid"]]
            }
            _list1.append(_dic1)
        else:
            for index,j in enumerate(_list1):
                if i["country"] == j["country"]:
                    j["orderid"].append(i["orderid"])
                    break
                elif i["country"] != j["country"] and index == len(_list1)-1:
                    _dic1 = {
                        "country": i["country"],
                        "orderid": [i["orderid"]]
                    }
                    _list1.append(_dic1)
                    break

    return JsonResponse({"code": 200, "msg": "success","warehouse_list":warehouse_list,"warehouse_country":_list,"country_order":_list1})
    # except Exception as e:
    #     return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 获取数据 修改人：黄继成 时间：2021-01-21
def get_bad_order(request):
    warehouse = request.GET.get("warehouse",None)
    country = request.GET.get("country", None)
    orderid = request.GET.get("orderid", None)
    state = request.GET.get("state", None)
    page = request.GET.get("page",1)
    every_page_num = request.GET.get("every_page_num",50)
    start = int(page) * int(every_page_num) - int(every_page_num)

    _lists = [
        {"key":"common_carrier","value":warehouse},
        {"key": "country", "value": country},
        {"key": "orderid", "value": orderid},
        {"key": "state", "value": state}
    ]
    try:
        # 查询产品编码表
        select = "select * from commodity_information;"
        _list = conf_fun.connect_mysql_operation(select,type='dict')
        data = []

        sql = "select * from problem_data"
        sql1 = "select count(*) from problem_data"
        count = 0
        for i in _lists:
            if count == 0:
                if i["value"] is not None:
                    sql += " where " + i["key"] + "='" + i["value"] + "' and "
                    sql1 += " where " + i["key"] + "='" + i["value"] + "' and "
                    count += 1
            else:
                if i["value"] is not None:
                    sql += i["key"] + "='" + i["value"] + "' and "
                    sql1 += i["key"] + "='" + i["value"] + "' and "
                    count += 1
        if count > 0:
            sql = sql[:-5]
            sql1 = sql1[:-5]
        sql = sql + " order by id limit %s,%s;"%(start,int(every_page_num))
        res = conf_fun.connect_mysql_or(sql,type='dict')

        for i in res:
            _dic = {
                "id":i["id"],
                "system_id": i["sysorder_id"],
                "Amazon_id": i["orderid"],
                "product_code": "",
                "warehouse": i["common_carrier"],
                "product_name": "",
                "sku": i["sku"],
                "country": i["country"],
                "name": i["recipient"],
                "question": i["reason"],
                "state":i["state"]
            }

            if i["reason"] is None:
                _dic["reason"] = "暂无详细描述"

            for j in _list:
                if i["sku"] == j["sku"]:
                    _dic["product_code"] = j["product_code"]
                    _dic["product_name"] = j["commodity_name"]
            data.append(_dic)
        res1 = conf_fun.connect_mysql_or(sql1)
        total_num = res1[0][0] if len(res1) > 0 else 0
        return JsonResponse({"code":200,"msg":"success","data":data,"total_num":total_num})
    except Exception as e:
        return JsonResponse({"code":500,"mag":"error:"+str(e)})


# 问题订单——订单修改——已处理
def order_edit(request):
    id = request.POST.get("id",None)
    try:
        sql = "update problem_data set state='1' where id=%s;"%(id)
        conf_fun.connect_mysql_or(sql)
        return JsonResponse({"code": 200, "msg": "success"})
    except Exception as e:
        return JsonResponse({"code":500,"mag":"error:"+str(e)})


# 订单追踪
# 获取仓库数据 修改：黄继成 2021-01-21
def warehouse_datas(request):
    country = request.GET.get("country",None)
    try:
        sql = "select warehouse_name,warehouse_code from oversea_location_data where country='"+country+"' and warehouse_type='海外仓';"
        res = conf_fun.connect_mysql_operation(sql,dbs='product_supplier',type='dict')
        _list = ["UPS","DPD","DHL","GLS","FEDEX","YODEL-XL"]
        data = []
        if len(res) > 0:
            data = [{"warehouse_name":i["warehouse_name"],"warehouse_code":i["warehouse_code"]} for i in res]
        return JsonResponse({"code": 200,"msg":"success","data":data,"supplier_list":_list})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 获取数据  修改：黄继成 2021-01-28
def order_track(request):
    channel = request.POST.get("channel",None)
    station = request.POST.get("station", None)
    country_zh = request.POST.get("country", None)
    warehouse_code = request.POST.get("warehouse", None)
    purchase_date = request.POST.get("purchase_date", None)
    latest_ship_date = request.POST.get("latest_ship_date",None)
    order_status = request.POST.get("order_status", None)
    tracking_no = request.POST.get("tracking_no", None)
    order_id = request.POST.get("AmazonId", None)
    shipping_method = request.POST.get("supplier", None)
    page = request.POST.get("page",1)
    start = int(page) * 50 - 50
    end = 50
    print("当前页：",page,shipping_method)
    store,country = store_country_code(station,country_zh,'en',type='upper')
    if country == 'UK':
        country = 'GB'
    if station is not None:
        station = store
    if country_zh is not None:
        country_code = country
    else:
        country_code = country_zh
    if channel == 'Amazon' or channel == 'amazon' or channel is None:
        _list = [
            {"key":"station", "value":station},
            {"key": "country_code", "value": country_code},
            {"key": "warehouse_code", "value": warehouse_code},
            {"key": "get_dates", "value": purchase_date},
            {"key": "latest_ship_date", "value": latest_ship_date},
            {"key": "tracking_no", "value": tracking_no},
            {"key": "reference_ture", "value": order_id},
            {"key": "shipping_method", "value": shipping_method},
            {"key": "order_status", "value": order_status}
        ]
        # 遍历查询
        sql1 = "select * from manually_create_order_yc where "
        sql2 = "select * from manually_create_order where "
        sql3 = "select * from manually_create_order_ups where "

        select1 = "select count(*) from manually_create_order_yc where "
        select2 = "select count(*) from manually_create_order where "
        select3 = "select count(*) from manually_create_order_ups where "
        _str = ""
        count = 0
        count1 = 0
        for i in _list:
            if i["value"] is not None:
                if i["key"] == "shipping_method":
                    _str += i["key"] + " like'%" + i["value"] + "%' and "
                    count += 1
                elif i["key"] == "get_dates" or i["key"] == "latest_ship_date":
                    time_list = i["value"].split(',')
                    if len(time_list) == 1:
                        _str += i["key"] + " like'%" + time_list[0] + "%' and "
                    else:
                        start_time = time_list[0] + "T00:00:00"
                        end_time = time_list[1] + "T23:59:59"
                        _str += i["key"] + ">='" + start_time + "' and " + i["key"] + "<='" + end_time + "' and "
                    count += 1
                elif i["key"] == "reference_ture":
                    order_list = i["value"].split(' ')
                    _tuple = ""
                    if len(order_list) == 1:
                        _tuple = str(tuple(order_list)).replace(',','')
                    else:
                        _tuple = str(tuple(order_list))

                    sql1 = "select * from manually_create_order_yc where reference_ture in %s"%(_tuple)
                    sql2 = "select * from manually_create_order where reference_ture in %s"%(_tuple)
                    sql3 = "select * from manually_create_order_ups where reference_ture in %s"%(_tuple)

                    select1 = "select count(*) from manually_create_order_yc where reference_ture in %s"%(_tuple)
                    select2 = "select count(*) from manually_create_order where reference_ture in %s"%(_tuple)
                    select3 = "select count(*) from manually_create_order_ups where reference_ture in %s"%(_tuple)
                    count += 1
                    count1 += 1
                    break
                elif i["key"] == "order_status":
                    _list1 = i["value"].split(',')
                    _str1 = ""
                    if len(_list1) == 1:
                        if _list1[0] == "暂无物流信息":
                            _str += "order_status='-1' and "
                        elif _list1[0] == "未发货":
                            _str += "delivery_date is NULL and start_time is NULL and end_time is NULL and order_status='1' and "
                        elif _list1[0] == "已发货":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "已发货但物流商未揽件":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "物流商已揽件":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is NULL and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "已送达":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is not NULL and end_time != '' and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "派件中":
                            _str += "order_status='5' and "
                        elif _list1[0] == "退回中":
                            _str += "order_status='6' and "
                        elif _list1[0] == "已退签":
                            _str += "order_status='4' and "
                        elif _list1[0] == "更改地址":
                            _str += "order_status='7' and "
                        elif _list1[0] == "货件取消":
                            _str += "order_status='8' and "
                    else:
                        for j in _list1:
                            if j == "暂无物流信息":
                                _str1 += _str + "order_status='-1' or  "
                            elif j == "未发货":
                                _str1 += _str + "delivery_date is NULL and start_time is NULL and end_time is NULL and order_status='1' or  "
                            elif j == "已发货":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "已发货但物流商未揽件":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "物流商已揽件":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is NULL and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "已送达":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is not NULL and end_time != '' and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "派件中":
                                _str1 += _str + "order_status='5' or  "
                            elif j == "退回中":
                                _str1 += _str + "order_status='6' or  "
                            elif j == "已退签":
                                _str1 += _str + "order_status='4' or  "
                            elif j == "更改地址":
                                _str1 += _str + "order_status='7' or  "
                            elif j == "货件取消":
                                _str1 += _str + "order_status='8' or  "

                        _str = _str1
                    count += 1
                elif i["key"] == "tracking_no":
                    sql1 = "select * from manually_create_order_yc where tracking_no is NULL or tracking_no='' order by id desc "
                    sql2 = "select * from manually_create_order where tracking_no is NULL or tracking_no='' order by id desc "
                    sql3 = "select * from manually_create_order_ups where tracking_no is NULL or tracking_no='' order by id desc "

                    select1 = "select count(*) from manually_create_order_yc where tracking_no is NULL or tracking_no='' order by id desc;"
                    select2 = "select count(*) from manually_create_order where tracking_no is NULL or tracking_no='' order by id desc;"
                    select3 = "select count(*) from manually_create_order_ups where tracking_no is NULL or tracking_no='' order by id desc;"
                    count += 1
                    count1 += 2
                    break
                else:
                    _str += i["key"] + "='" + i["value"] + "' and "
                    count += 1

        if count1 == 1:
            country_code = None
        elif count1 == 2:
            print("无追踪编码")
            sql1 = sql1 + "limit %s,%s;" % (start, end)
            sql2 = sql2 + "limit %s,%s;" % (start, end)
            sql3 = sql3 + "limit %s,%s;" % (start, end)
        else:
            sql1 += _str
            sql2 += _str
            sql3 += _str
            select1 += _str
            select2 += _str
            select3 += _str

            if count == 0:
                sql1 = sql1 + "status='1' order by id desc limit %s,%s;" % (start, end)
                sql2 = sql2 + "status='1' order by id desc limit %s,%s;" % (start, end)
                sql3 = sql3 + "status='1' order by id desc limit %s,%s;" % (start, end)

                select1 = select1 + "status='1';"
                select2 = select2 + "status='1';"
                select3 = select3 + "status='1';"
            else:
                sql1 = sql1[:-5] + " order by id desc limit %s,%s;"%(start,end)
                sql2 = sql2[:-5] + " order by id desc limit %s,%s;"%(start,end)
                sql3 = sql3[:-5] + " order by id desc limit %s,%s;"%(start,end)

                select1 = select1[:-5]
                select2 = select2[:-5]
                select3 = select3[:-5]
        # try:
        if country_code == 'US':
            print("sql2===", sql2)
            data = conf_fun.connect_mysql_or(sql2, type='dict')
            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select2)
            total_num = res1[0][0]
        elif country_code == 'CA':
            print("sql3===", sql3)
            data = conf_fun.connect_mysql_or(sql3, type='dict')
            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select3)
            total_num = res1[0][0]
        elif country_code is None:
            print("sql1===", sql1)
            print("sql2===", sql2)
            print("sql3===", sql3)
            data1 = conf_fun.connect_mysql_or(sql1, type='dict')
            data2 = conf_fun.connect_mysql_or(sql2, type='dict')
            data3 = conf_fun.connect_mysql_or(sql3, type='dict')
            data = []

            if len(data1) > 0:
                data += data1
            if len(data2) > 0:
                data += data2
            if len(data3) > 0:
                data += data3

            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select1)
            res2 = conf_fun.connect_mysql_or(select2)
            res3 = conf_fun.connect_mysql_or(select3)

            total_num = res1[0][0] + res2[0][0] + res3[0][0]
        else:
            print("sql1===", sql1)
            data = conf_fun.connect_mysql_or(sql1, type='dict')
            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select1)
            total_num = res1[0][0]

        # 查询产品编码表
        sql4 = "select ci.product_code,ci.sku,p.product_name from commodity_information as ci LEFT JOIN product_zr as p ON ci.product_code=p.product_number;"
        res = conf_fun.connect_mysql_operation(sql4,type='dict')
        _data = []

        # 查询所有仓库信息
        sql5 = "select warehouse_name,warehouse_code from oversea_location_data where country='" + country_zh + "' and warehouse_type='海外仓';"
        res5 = conf_fun.connect_mysql_operation(sql5, dbs='product_supplier', type='dict')

        print(len(data))
        for j in data:
            store1, country1 = store_country_code(j["station"], j["country_code"], 'zh')
            _dic = {
                "dates": j["get_dates"],
                "station": store1,
                "country": country1,
                "warehouse": j["warehouse_code"],
                "AmazonId":j["reference_ture"],
                "tracking_no":j["tracking_no"],
                "order_create_reduce_delivery":"--",    # 订单创建减出库
                "delivery_reduce_start": "--",          # 出库减物流商
                "start_reduce_end": "--",               # 物流商减送达
                "order_create_reduce_end": "--",        # 订单创建减出库
                "latest_ship_date": "--"                # 最晚送达时间
            }
            # 对比获取仓库名
            for item in res5:
                if j["warehouse_code"] == item["warehouse_code"]:
                    _dic["warehouse"] = item["warehouse_name"]
                    break

            latest_ship_date_zh = ""
            if j["latest_ship_date"] is not None:
                if "Z" in j["latest_ship_date"]:
                    latest_ship_date = j["latest_ship_date"].split('Z')[0]
                else:
                    latest_ship_date = j["latest_ship_date"]

                if j["country_code"] == 'US' or j["country_code"] == 'CA':
                    latest_ship_date_zh = datetime.datetime.strftime((datetime.datetime.strptime(latest_ship_date,
                                          "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=16)), "%Y-%m-%dT%H:%M:%S")
                    if j["country_code"] == 'US':
                        _dic["latest_ship_date"] = latest_ship_date
                    else:
                        _dic["latest_ship_date"] = '/'.join(latest_ship_date.split('T')[0].split('-'))
                else:
                    latest_ship_date_zh = datetime.datetime.strftime((datetime.datetime.strptime(latest_ship_date,
                                          "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=7)),"%Y-%m-%dT%H:%M:%S")
                    _dic["latest_ship_date"] = latest_ship_date

            if j["country_code"] == 'US' or j["country_code"] == 'CA' or j["country_code"] == 'PR':
                _dic["sku"] = j["sku"]
                if j["shipping_method"] is None:
                    _dic["supplier"] = ""
                else:
                    if "FEDEX" in j["shipping_method"]:
                        _dic["supplier"] = "FEDEX"
                    elif "UPS" in j["shipping_method"]:
                        _dic["supplier"] = "UPS"
            else:
                _dic["sku"] = j["product_sku"]
                if j["shipping_method"] is None:
                    _dic["supplier"] = ""
                else:
                    if "DHL" in j["shipping_method"] or "D51" in j["shipping_method"]:
                        _dic["supplier"] = "DHL"
                    elif "DPD" in j["shipping_method"] or "D29" in j["shipping_method"]:
                        _dic["supplier"] = "DPD"
                    elif "GLS" in j["shipping_method"]:
                        _dic["supplier"] = "GLS"
                    elif "YODEL" in j["shipping_method"]:
                        _dic["supplier"] = "YODEL"
                    elif "FEDEX" in j["shipping_method"]:
                        _dic["supplier"] = "FEDEX"
                    else:
                        _dic["supplier"] = ""
            # 查询此订单sku的配送时效
            getdates = ''
            getdates_zh = ''
            if j["get_dates"] is not None:
                if ' ' in j["get_dates"]:
                    if country_code == "US" or country_code == "CA" or country_code == "PR":
                        getdates = j["get_dates"] + ":00"
                    else:
                        getdates = j["get_dates"]
                elif 'T' in j["get_dates"]:
                    if "-" in j["get_dates"].split('T')[1]:
                        getdates = j["get_dates"].split('T')[0] + " " + j["get_dates"].split('T')[1].replace('-',':') + ":00"
                    else:
                        getdates = j["get_dates"].replace('T', ' ')
                else:
                    getdates = j["get_dates"] + ' ' + '00:00:00'

                if 'Z' in getdates:
                    getdates = getdates.replace('Z','')

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    getdates_zh = datetime.datetime.strftime(datetime.datetime.strptime(getdates, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=16),"%Y-%m-%d %H:%M:%S")
                else:
                    getdates_zh = datetime.datetime.strftime(datetime.datetime.strptime(getdates, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=7),"%Y-%m-%d %H:%M:%S")

            # 判断是否可能超时
            if j["latest_logistics_date"] is not None and j["latest_logistics_date"] != '':
                # print("latest_logistics_date===",j["latest_logistics_date"])
                latest_logistics_date = ""
                latest_logistics_date_zh = ""
                timeout = 0

                if "-" in j["latest_logistics_date"]:
                    latest_logistics_date = j["latest_logistics_date"].replace('-','/')
                else:
                    latest_logistics_date = j["latest_logistics_date"]

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    latest_logistics_date_zh = datetime.datetime.strftime(
                        datetime.datetime.strptime(latest_logistics_date, "%Y/%m/%d") + datetime.timedelta(hours=13),"%Y-%m-%dT%H:%M:%S")
                    if latest_ship_date_zh == "":
                        timeout = 0
                    else:
                        timeout = (datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y-%m-%dT%H:%M:%S")).days + \
                                  round((datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y-%m-%dT%H:%M:%S")).seconds / 60 / 60, 2)
                else:
                    latest_logistics_date_zh = latest_logistics_date
                    if latest_ship_date_zh == "":
                        timeout = 0
                    else:
                        timeout = (datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y/%m/%d")).days + \
                                  round((datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y/%m/%d")).seconds / 60 / 60, 2)

                if timeout > 0:
                    _dic["is_timeout"] = "可能超时"
                else:
                    _dic["is_timeout"] = ""

                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _dic["is_timeout_content"] = [
                            {"key":"亚马逊规定最晚送达时间","value":_dic["latest_ship_date"]},
                            {"key": "参考中国时间", "value": latest_ship_date_zh},
                            {"key": "物流商预计送达时间", "value": _dic["latest_ship_date"]},
                            {"key": "参考中国时间", "value": latest_logistics_date_zh},
                            {"key": "差值", "value": str(timeout)},
                            {"key": "计算方式", "value": "参考中国时间计算"},
                        ]
                    else:
                        _dic["is_timeout_content"] = [
                            {"key": "亚马逊规定最晚送达时间", "value": _dic["latest_ship_date"]},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "物流商预计送达时间", "value": _dic["latest_ship_date"]},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值", "value": str(timeout)},
                            {"key": "计算方式", "value": "参考欧洲时间计算"},
                        ]
            else:
                _dic["is_timeout"] = "未获取到物流商预计送达时间"

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["is_timeout_content"] = [
                        {"key": "亚马逊规定最晚送达时间", "value": _dic["latest_ship_date"]},
                        {"key": "参考中国时间", "value": latest_ship_date_zh},
                        {"key": "物流商预计送达时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考中国时间计算"},
                    ]
                else:
                    _dic["is_timeout_content"] = [
                        {"key": "亚马逊规定最晚送达时间", "value": _dic["latest_ship_date"]},
                        {"key": "参考中国时间", "value": "我"},
                        {"key": "物流商预计送达时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考欧洲时间计算"},
                    ]


            # 判断物流状态
            if j["order_status"] == '-1' or j["order_status"] == '':
                _dic["logistics_type"] = '暂无物流信息'
            elif j["order_status"] == '2':
                _dic["logistics_type"] = '寄送出错'
            elif j["order_status"] == '4':
                _dic["logistics_type"] = '已退签'
            elif j["order_status"] == '5':
                _dic["logistics_type"] = '派件中'
            elif j["order_status"] == '6':
                _dic["logistics_type"] = '退回中'
            elif j["order_status"] == '7':
                _dic["logistics_type"] = '更改地址'
            elif j["order_status"] == '8':
                _dic["logistics_type"] = '货件取消'
            else:
                if j["delivery_date"] is None or j["delivery_date"] == '':
                    _dic["logistics_type"] = '未发货'
                else:
                    _dic["logistics_type"] = '已发货'

                    if j["start_time"] is None or j["start_time"] != '':
                        _dic["logistics_type"] = '已发货但物流商未揽件'
                    else:
                        _dic["logistics_type"] = '物流商已揽件'

                        if j["end_time"] is not None and j["end_time"] != '':
                            _dic["logistics_type"] = '已送达'

                if j["start_time"] is not None and j["start_time"] != '':
                    _dic["logistics_type"] = '物流商已揽件'

                if j["end_time"] is not None and j["end_time"] != '':
                    _dic["logistics_type"] = '已送达'


            delivery_date = ""
            if j["delivery_date"] is None or j["delivery_date"] == '' or j["delivery_date"] == "None":
                _dic["delivery_date"] = '--'
                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["order_create_reduce_delivery_content"] = [
                        {"key": "订单创建时间", "value": getdates},
                        {"key": "参考中国时间", "value": getdates_zh},
                        {"key": "出库时间(中国时间)", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考中国时间计算"},
                    ]
                else:
                    _dic["order_create_reduce_delivery_content"] = [
                        {"key": "订单创建时间", "value": getdates},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "出库时间(中国时间)", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考欧洲时间计算"},
                    ]
            elif j["delivery_date"] == '0000-00-00 00:00:00':
                _dic["delivery_date"] = '0000-00-00 00:00:00'
                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["order_create_reduce_delivery_content"] = [
                        {"key": "订单创建时间", "value": getdates},
                        {"key": "参考中国时间", "value": getdates_zh},
                        {"key": "出库时间(中国时间)", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考中国时间计算"},
                    ]
                else:
                    _dic["order_create_reduce_delivery_content"] = [
                        {"key": "订单创建时间", "value": getdates},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "出库时间(中国时间)", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考欧洲时间计算"},
                    ]
            else:
                if len(j["delivery_date"].split(':')) == 2:
                    delivery_date = j["delivery_date"] + ":00"
                else:
                    delivery_date = j["delivery_date"]

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["delivery_date"] = delivery_date
                else:
                    _dic["delivery_date"] = datetime.datetime.strftime(datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=7),"%Y-%m-%d %H:%M:%S")

                if getdates == "":
                    _dic["order_create_reduce_delivery"] = '--'

                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _dic["order_create_reduce_delivery_content"] = [
                            {"key": "订单创建时间", "value": "无"},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "出库时间(中国时间)", "value": delivery_date},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值", "value": "无"},
                            {"key": "计算方式", "value": "参考中国时间计算"},
                        ]
                    else:
                        _dic["order_create_reduce_delivery_content"] = [
                            {"key": "订单创建时间", "value": getdates},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "出库时间(欧洲时间)", "value": _dic["delivery_date"]},
                            {"key": "参考中国时间", "value": delivery_date},
                            {"key": "差值", "value": "无"},
                            {"key": "计算方式", "value": "参考欧洲时间计算"},
                        ]
                else:
                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _days1 = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates_zh,"%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_delivery"] = str(_days1.days) + "天" + str(round((_days1.seconds) / 60 / 60, 2)) + "小时"

                        _dic["order_create_reduce_delivery_content"] = [
                            {"key": "订单创建时间", "value": getdates},
                            {"key": "参考中国时间", "value": getdates_zh},
                            {"key": "出库时间(中国时间)", "value": delivery_date},
                            {"key": "参考中国时间", "value": delivery_date},
                            {"key": "差值","value": str(_days1.days) + "天" + str(round((_days1.seconds) / 60 / 60, 2)) + "小时"},
                            {"key": "计算方式", "value": "参考中国时间计算"},
                        ]
                    else:
                        _days1 = (datetime.datetime.strptime(_dic["delivery_date"],"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates,"%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_delivery"] = str(_days1.days) + "天" + str(round((_days1.seconds) / 60 / 60, 2)) + "小时"

                        _dic["order_create_reduce_delivery_content"] = [
                            {"key": "订单创建时间", "value": getdates},
                            {"key": "参考中国时间", "value": getdates_zh},
                            {"key": "出库时间(欧洲时间)", "value": _dic["delivery_date"]},
                            {"key": "参考中国时间", "value": delivery_date},
                            {"key": "差值", "value": str(_days1.days) + "天" + str(round((_days1.seconds) / 60 / 60, 2)) + "小时"},
                            {"key": "计算方式", "value": "参考欧洲时间计算"},
                        ]

            start_time = ""
            start_time_zh = ""
            if j["start_time"] is None or j["start_time"] == '':
                _dic["start_time"] = '--'
                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["delivery_reduce_start_content"] = [
                        {"key": "物流商取货时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "出库时间(中国时间)", "value": delivery_date},
                        {"key": "参考中国时间", "value": delivery_date},
                        {"key": "差值", "value": "无"},
                    ]
                else:
                    _dic["delivery_reduce_start_content"] = [
                        {"key": "物流商取货时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "出库时间(欧洲时间)", "value": _dic['delivery_date']},
                        {"key": "参考中国时间", "value": delivery_date},
                        {"key": "差值", "value": "无"},
                    ]
            else:
                if len(j["start_time"].split(':')) == 2:
                    start_time = j["start_time"] + ":00"
                else:
                    start_time = j["start_time"]
                if j["country_code"] == "CA":
                    _dic["start_time"] = '/'.join(start_time.split(' ')[0].split('-'))
                else:
                    _dic["start_time"] = start_time

                start_time_zh = datetime.datetime.strftime(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=13),"%Y-%m-%d %H:%M:%S")

                if delivery_date == "":
                    _dic["delivery_reduce_start"] = '--'

                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _dic["delivery_reduce_start_content"] = [
                            {"key": "物流商取货时间", "value": start_time},
                            {"key": "参考中国时间", "value": start_time_zh},
                            {"key": "出库时间(中国时间)", "value": "无"},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值", "value": "无"},
                            {"key": "计算方式", "value": "参考中国时间计算"}
                        ]
                    else:
                        _dic["delivery_reduce_start_content"] = [
                            {"key": "物流商取货时间", "value": start_time},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "出库时间(欧洲时间)", "value": "无"},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值", "value": "无"},
                            {"key": "计算方式", "value": "参考欧洲时间计算"}
                        ]
                else:
                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _days2 = (datetime.datetime.strptime(start_time_zh,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S"))
                        _dic["delivery_reduce_start"] = str(_days2.days) + "天" + str(round((_days2.seconds) / 60 / 60, 2)) + "小时"

                        _dic["delivery_reduce_start_content"] = [
                            {"key": "物流商取货时间", "value": start_time},
                            {"key": "参考中国时间", "value": start_time_zh},
                            {"key": "出库时间(中国时间)", "value": delivery_date},
                            {"key": "参考中国时间", "value": delivery_date},
                            {"key": "差值", "value": str(_days2.days)+"天"+str(round((_days2.seconds)/60/60,2))+"小时"},
                            {"key": "计算方式", "value": "参考中国时间计算"}
                        ]
                    else:
                        _days2 = (datetime.datetime.strptime(_dic["start_time"],"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(_dic["delivery_date"], "%Y-%m-%d %H:%M:%S"))
                        _dic["delivery_reduce_start"] = str(_days2.days) + "天" + str(round((_days2.seconds) / 60 / 60, 2)) + "小时"

                        _dic["delivery_reduce_start_content"] = [
                            {"key": "物流商取货时间", "value": _dic["start_time"]},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "出库时间(欧洲时间)", "value": _dic["delivery_date"]},
                            {"key": "参考中国时间", "value": delivery_date},
                            {"key": "差值","value": str(_days2.days) + "天" + str(round((_days2.seconds) / 60 / 60, 2)) + "小时"},
                            {"key":"计算方式","value":"参考欧洲时间计算"}
                        ]

            end_time = ""
            end_time_zh = ""
            if j["end_time"] is None or j["end_time"] == '':
                _dic["end_time"] = '--'

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["start_reduce_end_content"] = [
                        {"key": "物流商取货时间", "value": start_time},
                        {"key": "参考中国时间", "value": start_time_zh},
                        {"key": "送达时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考中国时间计算"}
                    ]

                    _dic["order_create_reduce_end_content"] = [
                        {"key": "订单创建时间", "value": start_time},
                        {"key": "参考中国时间", "value": start_time_zh},
                        {"key": "送达时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考中国时间计算"}
                    ]
                else:
                    _dic["start_reduce_end_content"] = [
                        {"key": "物流商取货时间", "value": _dic["start_time"]},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "送达时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考欧洲时间计算"}
                    ]

                    _dic["order_create_reduce_end_content"] = [
                        {"key": "订单创建时间", "value": _dic["start_time"]},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "送达时间", "value": "无"},
                        {"key": "参考中国时间", "value": "无"},
                        {"key": "差值", "value": "无"},
                        {"key": "计算方式", "value": "参考欧洲时间计算"}
                    ]
            else:

                if len(j["end_time"].split(':')) == 2:
                    end_time = j["end_time"] + ":00"
                else:
                    end_time = j["end_time"]

                _dic["end_time"] = j["end_time"]

                end_time_zh = datetime.datetime.strftime(datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=13),"%Y-%m-%d %H:%M:%S")

                if start_time == "":
                    _dic["start_reduce_end"] = "--"

                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _dic["start_reduce_end_content"] = [
                            {"key": "物流商取货时间", "value": "无"},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "送达时间", "value": end_time},
                            {"key": "参考中国时间", "value": end_time_zh},
                            {"key": "差值", "value": "无"},
                            {"key": "计算方式", "value": "参考中国时间计算"}
                        ]
                    else:
                        _dic["start_reduce_end_content"] = [
                            {"key": "物流商取货时间", "value": "无"},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "送达时间", "value": _dic["end_time"]},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值", "value": "无"},
                            {"key": "计算方式", "value": "参考欧洲时间计算"}
                        ]
                else:
                    _days3 = (datetime.datetime.strptime(end_time_zh,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start_time_zh, "%Y-%m-%d %H:%M:%S"))
                    _dic["start_reduce_end"] = str(_days3.days)+"天"+str(round((_days3.seconds)/60/60,2))+"小时"

                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _dic["start_reduce_end_content"] = [
                            {"key": "物流商取货时间", "value": start_time},
                            {"key": "参考中国时间", "value": start_time_zh},
                            {"key": "送达时间", "value": end_time},
                            {"key": "参考中国时间", "value": end_time_zh},
                            {"key": "差值", "value": str(_days3.days)+"天"+str(round((_days3.seconds)/60/60,2))+"小时"},
                            {"key": "计算方式", "value": "参考中国时间计算"}
                        ]
                    else:
                        _dic["start_reduce_end_content"] = [
                            {"key": "物流商取货时间", "value": _dic["start_time"]},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "送达时间", "value": _dic["end_time"]},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值","value": str(_days3.days) + "天" + str(round((_days3.seconds) / 60 / 60, 2)) + "小时"},
                            {"key": "计算方式", "value": "参考欧洲时间计算"}
                        ]

                if j["order_status"] == '3':
                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _days = (datetime.datetime.strptime(end_time_zh,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates_zh, "%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_end"] = str(_days.days)+"天"+str(round((_days.seconds)/60/60,2))+"小时"

                        _dic["order_create_reduce_end_content"] = [
                            {"key": "订单创建时间", "value": getdates},
                            {"key": "参考中国时间", "value": getdates_zh},
                            {"key": "送达时间", "value": end_time},
                            {"key": "参考中国时间", "value": end_time_zh},
                            {"key": "差值","value": str(_days.days)+"天"+str(round((_days.seconds)/60/60,2))+"小时"},
                            {"key": "计算方式", "value": "参考中国时间计算"}
                        ]
                    else:
                        _days = (datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates, "%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_end"] = str(_days.days) + "天" + str(round((_days.seconds) / 60 / 60, 2)) + "小时"

                        _dic["order_create_reduce_end_content"] = [
                            {"key": "订单创建时间", "value": getdates},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "送达时间", "value": end_time},
                            {"key": "参考中国时间", "value": "无"},
                            {"key": "差值","value": str(_days.days) + "天" + str(round((_days.seconds) / 60 / 60, 2)) + "小时"},
                            {"key": "计算方式", "value": "参考欧洲时间计算"}
                        ]
                else:
                    if j["capture_time"] != "0":
                        capture_time = j["capture_time"] if ":" in j["capture_time"] else j["capture_time"] + " 00:00"
                        if j["country_code"] == "US" or j["country_code"] == "CA":
                            days = (datetime.datetime.strptime(capture_time,"%Y-%m-%d %H:%M") - datetime.datetime.strptime(getdates_zh, "%Y-%m-%d %H:%M:%S"))
                            _dic["order_create_reduce_end"] = str(days.days)+"天"+str(round((days.seconds)/60/60,2))+"小时"

                            _dic["order_create_reduce_end_content"] = [
                                {"key": "订单创建时间", "value": getdates},
                                {"key": "参考中国时间", "value": getdates_zh},
                                {"key": "送达时间", "value": end_time},
                                {"key": "参考中国时间", "value": end_time_zh},
                                {"key": "差值","value": str(days.days) + "天" + str(round((days.seconds) / 60 / 60, 2)) + "小时"},
                                {"key": "计算方式", "value": "参考中国时间计算"}
                            ]
                        else:
                            print(_dic["AmazonId"])
                            capture_time = datetime.datetime.strftime(datetime.datetime.strptime(capture_time, "%Y-%m-%d %H:%M") - datetime.timedelta(hours=7),"%Y-%m-%d")
                            days = (datetime.datetime.strptime(capture_time,"%Y-%m-%d") - datetime.datetime.strptime(getdates,"%Y-%m-%d %H:%M:%S"))
                            _dic["order_create_reduce_end"] = str(days.days) + "天" + str(round((days.seconds) / 60 / 60, 2)) + "小时"

                            _dic["order_create_reduce_end_content"] = [
                                {"key": "订单创建时间", "value": getdates},
                                {"key": "参考中国时间", "value": "无"},
                                {"key": "送达时间", "value": end_time},
                                {"key": "参考中国时间", "value": "无"},
                                {"key": "差值","value": str(days.days) + "天" + str(round((days.seconds) / 60 / 60, 2)) + "小时"},
                                {"key": "计算方式", "value": "参考欧洲时间计算"}
                            ]
                    else:
                        _dic["order_create_reduce_end"] = '--'

                        if j["country_code"] == "US" or j["country_code"] == "CA":
                            _dic["order_create_reduce_end_content"] = [
                                {"key": "订单创建时间", "value": getdates},
                                {"key": "参考中国时间", "value": getdates_zh},
                                {"key": "送达时间", "value": "无"},
                                {"key": "参考中国时间", "value": "无"},
                                {"key": "差值","value": "无"},
                                {"key": "计算方式", "value": "参考中国时间计算"}
                            ]
                        else:
                            _dic["order_create_reduce_end_content"] = [
                                {"key": "订单创建时间", "value": getdates},
                                {"key": "参考中国时间", "value": "无"},
                                {"key": "送达时间", "value": "无"},
                                {"key": "参考中国时间", "value": "无"},
                                {"key": "差值","value": "无"},
                                {"key": "计算方式", "value": "参考欧洲时间计算"}
                            ]

            for i in res:
                if j["country_code"] == 'US' or j["country_code"] == 'CA' or j["country_code"] == 'PR':
                    if i["sku"] in j["sku"]:
                        _dic["product_name"] = i["product_name"]
                        break
                    else:
                        _dic["product_name"] = "未查询到sku对应的品名"
                else:
                    if i["sku"] in j["product_sku"]:
                        _dic["product_name"] = i["product_name"]
                        break
                    else:
                        _dic["product_name"] = "未查询到sku对应的品名"

            _data.append(_dic)
        return JsonResponse({"code":200,"msg":"success","data":_data,"total_num":total_num})
        # except Exception as e:
        #     return JsonResponse({"code":500,"msg":"error:"+str(e)})
    else:
        return JsonResponse({"code":200,"msg":"暂无除Amazon以外的其他渠道！"})


# 导出数据
def order_track_download(request):
    channel = request.GET.get("channel",None)
    station = request.GET.get("station", None)
    country_zh = request.GET.get("country", None)
    warehouse_code = request.GET.get("warehouse", None)
    purchase_date = request.GET.get("purchase_date", None)
    latest_ship_date = request.GET.get("latest_ship_date",None)
    order_status = request.GET.get("order_status", None)
    tracking_no = request.GET.get("tracking_no", None)
    order_id = request.GET.get("AmazonId", None)
    shipping_method = request.GET.get("supplier", None)
    page = request.GET.get("page",1)
    start = int(page) * 50 - 50
    end = 50
    print("当前页：",page,shipping_method)
    store,country = store_country_code(station,country_zh,'en',type='upper')
    if country == 'UK':
        country = 'GB'
    if station is not None:
        station = store
    if country_zh is not None:
        country_code = country
    else:
        country_code = country_zh
    if channel == 'Amazon' or channel == 'amazon' or channel is None:
        _list = [
            {"key":"station", "value":station},
            {"key": "country_code", "value": country_code},
            {"key": "warehouse_code", "value": warehouse_code},
            {"key": "get_dates", "value": purchase_date},
            {"key": "latest_ship_date", "value": latest_ship_date},
            {"key": "tracking_no", "value": tracking_no},
            {"key": "reference_ture", "value": order_id},
            {"key": "shipping_method", "value": shipping_method},
            {"key": "order_status", "value": order_status}
        ]
        # 遍历查询
        sql1 = "select * from manually_create_order_yc where "
        sql2 = "select * from manually_create_order where "
        sql3 = "select * from manually_create_order_ups where "

        select1 = "select count(*) from manually_create_order_yc where "
        select2 = "select count(*) from manually_create_order where "
        select3 = "select count(*) from manually_create_order_ups where "
        _str = ""
        count = 0
        count1 = 0
        for i in _list:
            if i["value"] is not None:
                if i["key"] == "shipping_method":
                    _str += i["key"] + " like'%" + i["value"] + "%' and "
                    count += 1
                elif i["key"] == "get_dates" or i["key"] == "latest_ship_date":
                    time_list = i["value"].split(',')
                    if len(time_list) == 1:
                        _str += i["key"] + " like'%" + time_list[0] + "%' and "
                    else:
                        start_time = time_list[0] + "T00:00:00"
                        end_time = time_list[1] + "T23:59:59"
                        _str += i["key"] + ">='" + start_time + "' and " + i["key"] + "<='" + end_time + "' and "
                    count += 1
                elif i["key"] == "reference_ture":
                    order_list = i["value"].split(' ')
                    _tuple = ""
                    if len(order_list) == 1:
                        _tuple = str(tuple(order_list)).replace(',', '')
                    else:
                        _tuple = str(tuple(order_list))

                    sql1 = "select * from manually_create_order_yc where reference_ture in %s" % (_tuple)
                    sql2 = "select * from manually_create_order where reference_ture in %s" % (_tuple)
                    sql3 = "select * from manually_create_order_ups where reference_ture in %s" % (_tuple)

                    select1 = "select count(*) from manually_create_order_yc where reference_ture in %s" % (_tuple)
                    select2 = "select count(*) from manually_create_order where reference_ture in %s" % (_tuple)
                    select3 = "select count(*) from manually_create_order_ups where reference_ture in %s" % (_tuple)
                    count += 1
                    count1 += 1
                    break
                elif i["key"] == "order_status":
                    _list1 = i["value"].split(',')
                    _str1 = ""
                    if len(_list1) == 1:
                        if _list1[0] == "暂无物流信息":
                            _str += "order_status='-1' and "
                        elif _list1[0] == "未发货":
                            _str += "delivery_date is NULL and start_time is NULL and end_time is NULL and order_status='1' and "
                        elif _list1[0] == "已发货":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "已发货但物流商未揽件":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "物流商已揽件":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is NULL and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "已送达":
                            _str += "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is not NULL and end_time != '' and order_status not in ('-1','4','5','6','7','8') and "
                        elif _list1[0] == "派件中":
                            _str += "order_status='5' and "
                        elif _list1[0] == "退回中":
                            _str += "order_status='6' and "
                        elif _list1[0] == "已退签":
                            _str += "order_status='4' and "
                        elif _list1[0] == "更改地址":
                            _str += "order_status='7' and "
                        elif _list1[0] == "货件取消":
                            _str += "order_status='8' and "
                    else:
                        for j in _list1:
                            if j == "暂无物流信息":
                                _str1 += _str + "order_status='-1' or  "
                            elif j == "未发货":
                                _str1 += _str + "delivery_date is NULL and start_time is NULL and end_time is NULL and order_status='1' or  "
                            elif j == "已发货":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "已发货但物流商未揽件":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is NULL and end_time is NULL and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "物流商已揽件":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is NULL and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "已送达":
                                _str1 += _str + "delivery_date is not NULL and delivery_date != '' and start_time is not NULL and start_time != '' and end_time is not NULL and end_time != '' and order_status not in ('-1','4','5','6','7','8') or  "
                            elif j == "派件中":
                                _str1 += _str + "order_status='5' or  "
                            elif j == "退回中":
                                _str1 += _str + "order_status='6' or  "
                            elif j == "已退签":
                                _str1 += _str + "order_status='4' or  "
                            elif j == "更改地址":
                                _str1 += _str + "order_status='7' or  "
                            elif j == "货件取消":
                                _str1 += _str + "order_status='8' or  "

                        _str = _str1
                    count += 1
                elif i["key"] == "tracking_no":
                    sql1 = "select * from manually_create_order_yc where tracking_no is NULL or tracking_no='' order by id desc;"
                    sql2 = "select * from manually_create_order where tracking_no is NULL or tracking_no='' order by id desc;"
                    sql3 = "select * from manually_create_order_ups where tracking_no is NULL or tracking_no='' order by id desc;"

                    select1 = "select count(*) from manually_create_order_yc where tracking_no is NULL or tracking_no='' order by id desc;"
                    select2 = "select count(*) from manually_create_order where tracking_no is NULL or tracking_no='' order by id desc;"
                    select3 = "select count(*) from manually_create_order_ups where tracking_no is NULL or tracking_no='' order by id desc;"
                    count += 1
                    count1 += 2
                    break
                else:
                    _str += i["key"] + "='" + i["value"] + "' and "
                    count += 1

        if count1 == 1:
            country_code = None
        elif count1 == 2:
            print("无追踪编码")
            pass
        else:
            sql1 += _str
            sql2 += _str
            sql3 += _str
            select1 += _str
            select2 += _str
            select3 += _str

            if count == 0:
                sql1 = sql1 + "status='1';"
                sql2 = sql2 + "status='1';"
                sql3 = sql3 + "status='1';"

                select1 = select1 + "status='1';"
                select2 = select2 + "status='1';"
                select3 = select3 + "status='1';"
            else:
                sql1 = sql1[:-5]
                sql2 = sql2[:-5]
                sql3 = sql3[:-5]

                select1 = select1[:-5]
                select2 = select2[:-5]
                select3 = select3[:-5]
        # try:
        if country_code == 'US':
            print("sql2===", sql2)
            data = conf_fun.connect_mysql_or(sql2, type='dict')
            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select2)
            total_num = res1[0][0]
        elif country_code == 'CA':
            print("sql3===", sql3)
            data = conf_fun.connect_mysql_or(sql3, type='dict')
            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select3)
            total_num = res1[0][0]
        elif country_code is None:
            print("sql1===", sql1)
            print("sql2===", sql2)
            print("sql3===", sql3)
            data1 = conf_fun.connect_mysql_or(sql1, type='dict')
            data2 = conf_fun.connect_mysql_or(sql2, type='dict')
            data3 = conf_fun.connect_mysql_or(sql3, type='dict')
            data = []

            if len(data1) > 0:
                data += data1
            if len(data2) > 0:
                data += data2
            if len(data3) > 0:
                data += data3

            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select1)
            res2 = conf_fun.connect_mysql_or(select2)
            res3 = conf_fun.connect_mysql_or(select3)

            total_num = res1[0][0] + res2[0][0] + res3[0][0]
        else:
            print("sql1===", sql1)
            data = conf_fun.connect_mysql_or(sql1, type='dict')
            # 查询总条数
            res1 = conf_fun.connect_mysql_or(select1)
            total_num = res1[0][0]

        # 查询产品编码表
        sql4 = "select ci.product_code,ci.sku,p.product_name from commodity_information as ci LEFT JOIN product_zr as p ON ci.product_code=p.product_number;"
        res = conf_fun.connect_mysql_operation(sql4,type='dict')
        _data = []

        # 查询所有仓库信息
        sql5 = "select warehouse_name,warehouse_code from oversea_location_data where country='" + country_zh + "' and warehouse_type='海外仓';"
        res5 = conf_fun.connect_mysql_operation(sql5, dbs='product_supplier', type='dict')

        print(len(data))
        for j in data:
            store1, country1 = store_country_code(j["station"], j["country_code"], 'zh')
            _dic = {
                "AmazonId": j["reference_ture"],
                "sku":"--",
                "tracking_no": j["tracking_no"],
                "product_name":"--",
                "logistics_type":"--",
                "dates": j["get_dates"],
                "delivery_date":"--",
                "start_time":"--",
                "end_time": "--",
                "order_create_reduce_delivery":"--",    # 订单创建到出库
                "delivery_reduce_start": "--",          # 出库到物流商
                "start_reduce_end": "--",               # 物流商到送达
                "order_create_reduce_end": "--",        # 订单创建到送达
                "latest_ship_date": "--",               # 最晚送达时间
                "is_timeout":"--",                      # 是否可能超时
                "station": store1,
                "country": country1,
                "warehouse": j["warehouse_code"],
                "supplier":"--"
            }
            # 对比获取仓库名
            for item in res5:
                if j["warehouse_code"] == item["warehouse_code"]:
                    _dic["warehouse"] = item["warehouse_name"]
                    break

            latest_ship_date_zh = ""
            if j["latest_ship_date"] is not None:
                if "Z" in j["latest_ship_date"]:
                    latest_ship_date = j["latest_ship_date"].split('Z')[0]
                else:
                    latest_ship_date = j["latest_ship_date"]

                if j["country_code"] == 'US' or j["country_code"] == 'CA':
                    latest_ship_date_zh = datetime.datetime.strftime((datetime.datetime.strptime(latest_ship_date,
                                          "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=16)), "%Y-%m-%dT%H:%M:%S")
                    if j["country_code"] == 'US':
                        _dic["latest_ship_date"] = latest_ship_date
                    else:
                        _dic["latest_ship_date"] = '/'.join(latest_ship_date.split('T')[0].split('-'))
                else:
                    latest_ship_date_zh = datetime.datetime.strftime((datetime.datetime.strptime(latest_ship_date,
                                          "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=7)),"%Y-%m-%dT%H:%M:%S")
                    _dic["latest_ship_date"] = latest_ship_date

            if j["country_code"] == 'US' or j["country_code"] == 'CA':
                _dic["sku"] = j["sku"]
                if j["shipping_method"] is None:
                    _dic["supplier"] = ""
                else:
                    if "FEDEX" in j["shipping_method"]:
                        _dic["supplier"] = "FEDEX"
                    elif "UPS" in j["shipping_method"]:
                        _dic["supplier"] = "UPS"
            else:
                _dic["sku"] = j["product_sku"]
                if j["shipping_method"] is None:
                    _dic["supplier"] = ""
                else:
                    if "DHL" in j["shipping_method"]  or "D51" in j["shipping_method"]:
                        _dic["supplier"] = "DHL"
                    elif "DPD" in j["shipping_method"] or "D29" in j["shipping_method"]:
                        _dic["supplier"] = "DPD"
                    elif "GLS" in j["shipping_method"]:
                        _dic["supplier"] = "GLS"
                    elif "YODEL" in j["shipping_method"]:
                        _dic["supplier"] = "YODEL"
                    elif "FEDEX" in j["shipping_method"]:
                        _dic["supplier"] = "FEDEX"
                    else:
                        _dic["supplier"] = ""
            # 查询此订单sku的配送时效
            getdates = ''
            getdates_zh = ''
            if j["get_dates"] is not None:
                if ' ' in j["get_dates"]:
                    if country_code == "US" or country_code == "CA":
                        getdates = j["get_dates"] + ":00"
                    else:
                        getdates = j["get_dates"]
                elif 'T' in j["get_dates"]:
                    if "-" in j["get_dates"].split('T')[1]:
                        getdates = j["get_dates"].split('T')[0] + " " + j["get_dates"].split('T')[1].replace('-',':') + ":00"
                    else:
                        getdates = j["get_dates"].replace('T', ' ')
                else:
                    getdates = j["get_dates"] + ' ' + '00:00:00'

                if 'Z' in getdates:
                    getdates = getdates.replace('Z','')

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    getdates_zh = datetime.datetime.strftime(datetime.datetime.strptime(getdates, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=16),"%Y-%m-%d %H:%M:%S")
                else:
                    getdates_zh = datetime.datetime.strftime(datetime.datetime.strptime(getdates, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=7),"%Y-%m-%d %H:%M:%S")

            # 判断是否可能超时
            if j["latest_logistics_date"] is not None and j["latest_logistics_date"] != '':
                # print("latest_logistics_date===",j["latest_logistics_date"])
                latest_logistics_date = ""
                latest_logistics_date_zh = ""
                timeout = 0

                if "-" in j["latest_logistics_date"]:
                    latest_logistics_date = j["latest_logistics_date"].replace('-','/')
                else:
                    latest_logistics_date = j["latest_logistics_date"]

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    latest_logistics_date_zh = datetime.datetime.strftime(
                        datetime.datetime.strptime(latest_logistics_date, "%Y/%m/%d") + datetime.timedelta(hours=13),
                        "%Y-%m-%dT%H:%M:%S")
                    if latest_ship_date_zh == "":
                        timeout = 0
                    else:
                        timeout = (datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y-%m-%dT%H:%M:%S")).days + \
                                  round((datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y-%m-%dT%H:%M:%S")).seconds / 60 / 60, 2)
                else:
                    latest_logistics_date_zh = latest_logistics_date
                    if latest_ship_date_zh == "":
                        timeout = 0
                    else:
                        timeout = (datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y/%m/%d")).days + \
                                  round((datetime.datetime.strptime(latest_ship_date_zh,"%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(latest_logistics_date_zh, "%Y/%m/%d")).seconds / 60 / 60, 2)

                if timeout > 0:
                    _dic["is_timeout"] = "可能超时"
                else:
                    _dic["is_timeout"] = ""
            else:
                _dic["is_timeout"] = "未获取到物流商预计送达时间"


            # 判断物流状态
            if j["order_status"] == '-1' or j["order_status"] == '':
                _dic["logistics_type"] = '暂无物流信息'
            elif j["order_status"] == '2':
                _dic["logistics_type"] = '寄送出错'
            elif j["order_status"] == '4':
                _dic["logistics_type"] = '已退签'
            elif j["order_status"] == '5':
                _dic["logistics_type"] = '派件中'
            elif j["order_status"] == '6':
                _dic["logistics_type"] = '退回中'
            elif j["order_status"] == '7':
                _dic["logistics_type"] = '更改地址'
            elif j["order_status"] == '8':
                _dic["logistics_type"] = '货件取消'
            else:
                if j["delivery_date"] is None or j["delivery_date"] == '':
                    _dic["logistics_type"] = '未发货'
                else:
                    _dic["logistics_type"] = '已发货'

                    if j["start_time"] is None or j["start_time"] != '':
                        _dic["logistics_type"] = '已发货但物流商未揽件'
                    else:
                        _dic["logistics_type"] = '物流商已揽件'

                        if j["end_time"] is not None and j["end_time"] != '':
                            _dic["logistics_type"] = '已送达'

                if j["start_time"] is not None and j["start_time"] != '':
                    _dic["logistics_type"] = '物流商已揽件'

                if j["end_time"] is not None and j["end_time"] != '':
                    _dic["logistics_type"] = '已送达'


            delivery_date = ""
            if j["delivery_date"] is None or j["delivery_date"] == '' or j["delivery_date"] == "None":
                _dic["delivery_date"] = '--'
            elif j["delivery_date"] == '0000-00-00 00:00:00':
                _dic["delivery_date"] = '0000-00-00 00:00:00'
            else:
                if len(j["delivery_date"].split(':')) == 2:
                    delivery_date = j["delivery_date"] + ":00"
                else:
                    delivery_date = j["delivery_date"]

                if j["country_code"] == "US" or j["country_code"] == "CA":
                    _dic["delivery_date"] = delivery_date
                else:
                    _dic["delivery_date"] = datetime.datetime.strftime(datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=7),"%Y-%m-%d %H:%M:%S")

                if getdates == "":
                    _dic["order_create_reduce_delivery"] = '--'
                else:
                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        print("======",delivery_date,type(delivery_date))
                        _days1 = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates_zh,"%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_delivery"] = str(_days1.days) + "天" + str(round((_days1.seconds) / 60 / 60, 2)) + "小时"
                    else:
                        _days1 = (datetime.datetime.strptime(_dic["delivery_date"],"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates,"%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_delivery"] = str(_days1.days) + "天" + str(round((_days1.seconds) / 60 / 60, 2)) + "小时"

            start_time = ""
            start_time_zh = ""
            if j["start_time"] is None or j["start_time"] == '':
                _dic["start_time"] = '--'
            else:
                if len(j["start_time"].split(':')) == 2:
                    start_time = j["start_time"] + ":00"
                else:
                    start_time = j["start_time"]

                if j["country_code"] == "CA":
                    _dic["start_time"] = '/'.join(start_time.split(' ')[0].split('-'))
                else:
                    _dic["start_time"] = start_time

                start_time_zh = datetime.datetime.strftime(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=13),"%Y-%m-%d %H:%M:%S")

                if delivery_date == "":
                    _dic["delivery_reduce_start"] = '--'
                else:
                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _days2 = (datetime.datetime.strptime(start_time_zh,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S"))
                        _dic["delivery_reduce_start"] = str(_days2.days) + "天" + str(round((_days2.seconds) / 60 / 60, 2)) + "小时"
                    else:
                        _days2 = (datetime.datetime.strptime(_dic["start_time"],"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(_dic["delivery_date"], "%Y-%m-%d %H:%M:%S"))
                        _dic["delivery_reduce_start"] = str(_days2.days) + "天" + str(round((_days2.seconds) / 60 / 60, 2)) + "小时"

            end_time = ""
            end_time_zh = ""
            if j["end_time"] is None or j["end_time"] == '':
                _dic["end_time"] = '--'
            else:

                if len(j["end_time"].split(':')) == 2:
                    end_time = j["end_time"] + ":00"
                else:
                    end_time = j["end_time"]

                _dic["end_time"] = j["end_time"]

                end_time_zh = datetime.datetime.strftime(datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=13),"%Y-%m-%d %H:%M:%S")

                if start_time == "":
                    _dic["start_reduce_end"] = "--"
                else:
                    _days3 = (datetime.datetime.strptime(end_time_zh,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start_time_zh, "%Y-%m-%d %H:%M:%S"))
                    _dic["start_reduce_end"] = str(_days3.days)+"天"+str(round((_days3.seconds)/60/60,2))+"小时"
                if j["order_status"] == '3':
                    if j["country_code"] == "US" or j["country_code"] == "CA":
                        _days = (datetime.datetime.strptime(end_time_zh,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates_zh, "%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_end"] = str(_days.days)+"天"+str(round((_days.seconds)/60/60,2))+"小时"
                    else:
                        _days = (datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(getdates, "%Y-%m-%d %H:%M:%S"))
                        _dic["order_create_reduce_end"] = str(_days.days) + "天" + str(round((_days.seconds) / 60 / 60, 2)) + "小时"
                else:
                    if j["capture_time"] != "0":
                        capture_time = j["capture_time"] if ":" in j["capture_time"] else j["capture_time"] + " 00:00"
                        if j["country_code"] == "US" or j["country_code"] == "CA":
                            days = (datetime.datetime.strptime(capture_time,"%Y-%m-%d %H:%M") - datetime.datetime.strptime(getdates_zh, "%Y-%m-%d %H:%M:%S"))
                            _dic["order_create_reduce_end"] = str(days.days)+"天"+str(round((days.seconds)/60/60,2))+"小时"
                        else:
                            _capture_time = datetime.datetime.strftime(datetime.datetime.strptime(capture_time, "%Y-%m-%d %H:%M") - datetime.timedelta(hours=7),"%Y-%m-%d")
                            days = (datetime.datetime.strptime(_capture_time,"%Y-%m-%d %H:%M") - datetime.datetime.strptime(getdates,"%Y-%m-%d %H:%M:%S"))
                            _dic["order_create_reduce_end"] = str(days.days) + "天" + str(round((days.seconds) / 60 / 60, 2)) + "小时"
                    else:
                        _dic["order_create_reduce_end"] = '--'

            for i in res:
                if j["country_code"] == 'US' or j["country_code"] == 'CA':
                    if i["sku"] in j["sku"]:
                        _dic["product_name"] = i["product_name"]
                        break
                    else:
                        _dic["product_name"] = "未查询到sku对应的品名"
                else:
                    if i["sku"] in j["product_sku"]:
                        _dic["product_name"] = i["product_name"]
                        break
                    else:
                        _dic["product_name"] = "未查询到sku对应的品名"

            _data.append(_dic)

        if len(_data) > 0:
            df = pd.DataFrame(_data)
            df.columns = ['订单编号', 'sku', '追踪编码', '品名', '物流状态', "订单创建时间", "出库日期", "物流商取货日期", "到达日期",
                          "订单创建-出库", "出库-物流商", "物流商-送达", "已配送时长", "最迟送达时间", "是否可能超时", "站点", "国家", "仓库名称", "物流商"]
            filename = '订单.xlsx'
            df.to_excel('/home/by_operate/static/data/order_data/order_download/' + filename, encoding='utf-8',index=False)

            files = open('/home/by_operate/static/data/order_data/order_download/' + filename, 'rb')
            response = FileResponse(files)
            response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(filename)
            return response
        else:
            return JsonResponse({"code": 400, "msg": "未查询到数据，无法下载空文件！"})
        # except Exception as e:
        #     return JsonResponse({"code":500,"msg":"error:"+str(e)})
    else:
        return JsonResponse({"code":200,"msg":"暂无除Amazon以外的其他渠道！"})


# 获取超时订单搜索框数据
def get_search_data(request):
    sql = "select * from timeout_orders;"
    try:
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        _list = []
        for i in data:
            if len(_list) == 0:
                _dict = {
                    "channel":i["channel"],
                    "station":[
                        {
                            "store":i["station"],
                            "country":[i["country"]]
                        }
                    ]
                }
                _list.append(_dict)
            else:
                for index,item in enumerate(_list):
                    if i["channel"] == item["channel"]:
                        for index1,item1 in enumerate(item["station"]):
                            if i["station"] == item1["store"]:
                                item1["country"].append(i["country"])
                                break
                            elif i["station"] != item1["store"] and index1 == len(item["station"])-1:
                                _dict1 = {
                                    "store":i["station"],
                                    "country":[i["country"]]
                                }
                                item["station"].append(_dict1)
                                break
                    elif i["channel"] != item["channel"] and index == len(_list)-1:
                        _dict = {
                            "channel": i["channel"],
                            "station": [
                                {
                                    "store": i["station"],
                                    "country": [i["country"]]
                                }
                            ]
                        }
                        _list.append(_dict)
                        break

        for i in _list:
            for j in i["station"]:
                j["country"] = list(set(j["country"]))

        warehouse_list = [{"warehouse_name":i["warehouse_name"],"warehouse":i["warehouse"],"country":i["country"]} for i in data]
        warehouse_list1 = []
        for i in warehouse_list:
            if len(warehouse_list1) == 0:
                warehouse_list1.append(i)
            else:
                for index,j in enumerate(warehouse_list1):
                    if i["warehouse_name"] == j["warehouse_name"] and i["country"] == j["country"]:
                        break
                    elif i["warehouse_name"] != j["warehouse_name"] and i["country"] != j["country"] and index == len(warehouse_list1)-1:
                        warehouse_list1.append(i)
                        break
        question_type_list = list(set([i["question_type"] for i in data]))
        question_reason_list = list(set([i["question_reason"] for i in data]))
        return JsonResponse({"code":200,"msg":"success","data":_list,"warehouse_list":warehouse_list1,
                             "question_type_list":question_type_list,"question_reason_list":question_reason_list})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 获取超时订单
def get_timeout_order(request):
    channel = request.POST.get("channel", 'Amazon')
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    warehouse_name = request.POST.get("warehouse_name", None)
    warehouse = request.POST.get("warehouse", None)
    logistic_supplier = request.POST.get("logistic_supplier", None)
    question_type = request.POST.get("question_type", None)
    question_reason = request.POST.get("question_reason", None)
    page = request.POST.get("page",1)
    print(channel,station,country)

    if channel == 'Amazon':
        _list = [
            {"key":"channel", "value":channel},
            {"key": "station", "value": station},
            {"key": "country", "value": country},
            {"key": "warehouse_name", "value": warehouse_name},
            {"key": "warehouse", "value": warehouse},
            {"key": "logistic_supplier", "value": logistic_supplier},
            {"key": "question_type", "value": question_type},
            {"key": "question_reason", "value": question_reason},
        ]
        # 查询所有超时订单
        count = 0
        sql = "select * from timeout_orders"
        for i in _list:
            if i["value"] is not None:
                if count == 0:
                    sql += " where " + i["key"] + "='" + i["value"] + "' and "
                    count += 1
                else:
                    sql += i["key"] + "='" + i["value"] + "' and "
                    count += 1
        sql = sql[:-5]
        print("sql===",sql)
        try:
            data = conf_fun.connect_mysql_operation(sql,type='dict')

            total_num = len(data)
            start = int(page) * 50 - 50
            end = int(page) * 50
            data1 = data[start:end]
            return JsonResponse({"code":200,"msg":"success","data":data1,"total_num":total_num})
        except Exception as e:
            return JsonResponse({"code":500,"msg":"error:"+str(e)})
    else:
        return JsonResponse({"code": 200, "msg": "暂无除Amazon以外的其他渠道！"})


# 订单统计
def order_statistics(request):
    country = request.GET.get("country",None)
    days = request.GET.get("days",7)
    _date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=days),"%Y-%m-%d")
    date_list = get_days(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d"),days)
    # 查询所有国家列表
    select = "select * from store_information where state='在售';"
    res = conf_fun.connect_mysql_operation(select,type="dict")
    country_list = list(set([i["country"] for i in res]))

    country_en = ""
    if country is None:
        # 查询欧洲订单数据表
        sql1 = "select * from manually_create_order_yc where status='1' and get_dates>='%s';"%(_date)
        # 查询美国订单表
        sql2 = "select * from manually_create_order where status='1' and get_dates>='%s';"%(_date)
        # 查询加拿大订单表
        sql3 = "select * from manually_create_order_ups where status='1' and get_dates>='%s';"%(_date)
        # 查询物流系统仓库信息表
        sql4 = "select * from oversea_location_data;"
        # 查询所有所有超时订单数量
        sql5 = "select * from timeout_orders where dates>='%s';"%(_date)
    else:
        store1, country_en = store_country_code('', country, "en", type='upper')
        if country_en == "uk" or country_en == "UK":
            country_en = "GB"
        # 查询欧洲订单数据表
        sql1 = "select * from manually_create_order_yc where status='1' and country_code='%s' and get_dates>='%s';"%(country_en,_date)
        # 查询美国订单表
        sql2 = "select * from manually_create_order where status='1' and country_code='%s' and get_dates>='%s';"%(country_en,_date)
        # 查询加拿大订单表
        sql3 = "select * from manually_create_order_ups where status='1' and country_code='%s' and get_dates>='%s';"%(country_en,_date)
        # 查询物流系统仓库信息表
        sql4 = "select * from oversea_location_data;"
        # 查询所有所有超时订单数量
        sql5 = "select * from timeout_orders where country='%s' and dates>='%s';"%(country,_date)

    print("sql1==",sql1)
    print("sql2==", sql2)
    print("sql3==", sql3)
    print("sql4==", sql4)
    print("sql5==", sql5)
    # try:
    data1 = conf_fun.connect_mysql_or(sql1, type='dict')
    data2 = conf_fun.connect_mysql_or(sql2, type='dict')
    data3 = conf_fun.connect_mysql_or(sql3, type='dict')
    res = conf_fun.connect_mysql_operation(sql4,dbs='product_supplier',type='dict')
    res1 = conf_fun.connect_mysql_operation(sql5,type='dict')
    timeout_order_list = [i["Amazon_id"] for i in res1]
    data4 = []
    if len(data1) > 0:
        data4 += data1
    if len(data2) > 0:
        data4 += data2
    if len(data3) > 0:
        data4 += data3

    print("总数据==",len(data4))

    now = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=1), "%Y-%m-%d")
    if country is None:
        # 获取昨日订单
        order_list = [i for i in data4 if i["get_dates"] is not None and now in i["get_dates"]]
    else:
        # 获取单个国家昨日的订单
        order_list = [i for i in data4 if i["get_dates"] is not None and now in i["get_dates"] and i["country_code"]==country_en]

    print("今日订单量==",len(order_list))

    data = [
        {
            "country":"订单总数",
            "num":0
        }
    ]
    warehouse_data_list = []
    warehouse_all_num = 0
    for i in order_list:
        for index,j in enumerate(data):
            if i["country_code"] == j["country"]:
                j["num"] += 1
                data[0]["num"] += 1
                break
            elif i["country_code"] != j["country"] and index == len(data)-1:
                _dic = {
                    "country": i["country_code"],
                    "num": 1
                }
                data.append(_dic)
                data[0]["num"] += 1
                break

        if len(warehouse_data_list) == 0:
            _dict = {
                "warehouse_code":i["warehouse_code"],
                "num":1
            }
            warehouse_all_num += 1
            warehouse_data_list.append(_dict)
        else:
            for index,item in enumerate(warehouse_data_list):
                if i["warehouse_code"] == item["warehouse_code"]:
                    item["num"] += 1
                    warehouse_all_num += 1
                    break
                elif i["warehouse_code"] != item["warehouse_code"] and index == len(warehouse_data_list)-1:
                    _dict = {
                        "warehouse_code": i["warehouse_code"],
                        "num": 1
                    }
                    warehouse_all_num += 1
                    warehouse_data_list.append(_dict)
                    break

    # 国家编码替换
    for index,i in enumerate(data):
        if index > 0:
            store1,country1 = store_country_code('',i["country"],"zh")
            i["country"] = country1 + "订单"

    # 每个仓库的占比
    for i in warehouse_data_list:
        i["warehouse_name"] = i["warehouse_code"]
        i["ratio"] = str(round(i["num"]/warehouse_all_num,2) * 100) + "%"
        for j in res:
            if i["warehouse_code"] == j["warehouse_code"]:
                i["warehouse_name"] = j["warehouse_name"]
    warehouse_data_list.insert(0, {"warehouse_name":"订单总数","num":warehouse_all_num})

    # 获取默认七天的仓库订单数据
    warehouse_seven_data = []
    for i in data4:
        if len(warehouse_seven_data) == 0:
            _dict = {
                "warehouse_code": i["warehouse_code"],
                "num": 1,
                "timeout_num":0,
                "minute":0,
                "delivery_date":0,
                "pick_up_date":0
            }
            # 计算获取跟踪单号的时间
            if i["dates"] is not None:
                times = datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")
                if i["get_tracking_no_date"] is not None:
                    _dict["minute"] = (datetime.datetime.strptime(i["get_tracking_no_date"], "%Y-%m-%d %H:%M:%S") - times).seconds / 60 / 60
                else:
                    now_time = datetime.datetime.now()
                    _dict["minute"] = (now_time - times).seconds / 60 / 60
            else:
                _dict["minute"] = 0
            # 判断是否超时
            if i["reference_ture"] in timeout_order_list:
                _dict["timeout_num"] += 1
            #计算出库时间
            if i["delivery_date"] is not None and i["delivery_date"] != '' and i["dates"] is not None and i["dates"] != '':
                delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                _day = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(i["dates"],"%Y-%m-%dT%H-%M")).days
                _hours = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(i["dates"],"%Y-%m-%dT%H-%M")).seconds / 60 / 60
                _dict["delivery_date"] = _day + round(_hours,2)
            else:
                _dict["delivery_date"] = 0
            # 计算取货
            if i["delivery_date"] is not None and i["delivery_date"] != '' and i["start_time"] is not None and i["start_time"] != '':
                start_time = i["start_time"] + ":00" if len(i["start_time"].split(' ')[1].split(':')) == 2 else i["start_time"]
                delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                _day = (datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).days
                _hours = (datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                _dict["pick_up_date"] = _day + round(_hours,2)
            warehouse_seven_data.append(_dict)
        else:
            for index,item in enumerate(warehouse_seven_data):
                if i["warehouse_code"] == item["warehouse_code"]:
                    # 计算获取追踪号的时间
                    if i["dates"] is not None and i["dates"] != '':
                        times = datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")
                        if i["get_tracking_no_date"] is not None:
                            _hours = (datetime.datetime.strptime(i["get_tracking_no_date"],"%Y-%m-%d %H:%M:%S") - times).seconds / 60 / 60
                            item["minute"] += round(_hours,2)
                        else:
                            now_time = datetime.datetime.now()
                            _hours = (now_time - times).seconds / 60 / 60
                            item["minute"] += round(_hours,2)
                    else:
                        item["minute"] = 0
                    # 判断是否超时
                    if i["reference_ture"] in timeout_order_list:
                        item["timeout_num"] += 1
                    # 计算出库时间
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["dates"] is not None and i["dates"] != '':
                        _day = (datetime.datetime.strptime(i["delivery_date"], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).days
                        _hours = (datetime.datetime.strptime(i["delivery_date"], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).seconds / 60 / 60
                        item["delivery_date"] += _day + round(_hours,2)

                    # 计算取货
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["start_time"] is not None and i["start_time"] != '':
                        start_time = i["start_time"] + ":00" if len(i["start_time"].split(' ')[1].split(':')) == 2 else i["start_time"]
                        _day = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                        _hours = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["delivery_date"], "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                        item["pick_up_date"] += _day + round(_hours,2)

                    item["num"] += 1
                    break
                elif i["warehouse_code"] != item["warehouse_code"] and index == len(warehouse_seven_data)-1:
                    _dict = {
                        "warehouse_code": i["warehouse_code"],
                        "num": 1,
                        "timeout_num": 0,
                        "minute": 0,
                        "delivery_date": 0,
                        "pick_up_date": 0
                    }
                    # 计算获取跟踪单号的时间
                    if i["dates"] is not None and i["dates"] != '':
                        times = datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")
                        if i["get_tracking_no_date"] is not None:
                            _hours = (datetime.datetime.strptime(i["get_tracking_no_date"],"%Y-%m-%d %H:%M:%S") - times).seconds / 60 / 60
                            _dict["minute"] = round(_hours,2)
                        else:
                            now_time = datetime.datetime.now()
                            _hours = (now_time - times).seconds / 60 / 60
                            _dict["minute"] = round(_hours,2)
                    # 判断是否超时
                    if i["reference_ture"] in timeout_order_list:
                        _dict["timeout_num"] += 1
                    # 计算出库时间
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["dates"] is not None and i["dates"] != '':
                        delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                        _day = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).days
                        _hours = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).seconds / 60 / 60
                        _dict["delivery_date"] = _day + round(_hours)
                    else:
                        _dict["delivery_date"] = 0
                    # 计算取货
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["start_time"] is not None and i["start_time"] != '':
                        delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                        start_time = i["start_time"] + ":00" if len(i["start_time"].split(' ')[1].split(':')) == 2 else i["start_time"]
                        _day = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).days
                        _hours = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                        _dict["pick_up_date"] = _day + round(_hours,2)
                    else:
                        _dict["pick_up_date"] = 0
                    warehouse_seven_data.append(_dict)
                    break
    # 计算这些数据的平均值
    for i in warehouse_seven_data:
        i["warehouse_name"] = i["warehouse_code"]
        for j in res:
            if i["warehouse_code"] == j["warehouse_code"]:
                i["warehouse_name"] = j["warehouse_name"]
        # 计算跟踪单号平均获取时间
        i["tracking_no_avg_minute"] = str(round(i["minute"]/i["num"],2)) + "小时"
        # 计算超时订单百分比
        i["timeout_order_ratio"] = str(round(i["timeout_num"]/i["num"],2) * 100) + "%"
        # 计算平均出库时间
        i["delivery_avg_date"] = str(math.ceil(i["delivery_date"]/i["num"])) + "天"
        # 计算平均取货时间
        i["pick_up_avg_date"] = str(math.ceil(i["pick_up_date"]/i["num"])) + "天"
        # 计算平均处理时间
        i["deal_avg_date"] = str(math.ceil(i["delivery_date"]/i["num"] + i["pick_up_date"]/i["num"])) + "天"

    warehouse_name_list = [i["warehouse_name"] for i in warehouse_seven_data]

    if country is None:
        print("查询全部")
        return JsonResponse({"code":200,"msg":"success","country_data":country_list,"today_order":data,
                         "warehouse_data_list":warehouse_data_list,"warehouse_seven_data":warehouse_seven_data,
                         "warehouse_name_list":warehouse_name_list,"date_list":date_list})
    else:
        print("按照国家查询")
        return JsonResponse({"code": 200, "msg": "success","warehouse_data_list": warehouse_data_list,
                             "warehouse_seven_data": warehouse_seven_data,"warehouse_name_list": warehouse_name_list,
                             "date_list": date_list})
    # except Exception as e:
    #     return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 获取n天的仓库订单数据
def get_warehouse_data(request):
    country = request.GET.get("country",None)
    days = request.GET.get("days",7)
    _date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=int(days)), "%Y-%m-%d")
    now = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
    date_list = get_days(now,int(days))
    if country is None:
        # 查询欧洲订单数据表
        sql1 = "select * from manually_create_order_yc where status='1' and get_dates>='%s';" % (_date)
        # 查询美国订单表
        sql2 = "select * from manually_create_order where status='1' and get_dates>='%s';" % (_date)
        # 查询加拿大订单表
        sql3 = "select * from manually_create_order_ups where status='1' and get_dates>='%s';" % (_date)
        # 查询物流系统仓库信息表
        sql4 = "select * from oversea_location_data;"
        # 查询所有所有超时订单数量
        sql5 = "select * from timeout_orders where dates>='%s';" % (_date)
    else:
        store1, country_en = store_country_code('', country, "en", type='upper')
        if country_en == "uk" or country_en == "UK":
            country_en = "GB"
        # 查询欧洲订单数据表
        sql1 = "select * from manually_create_order_yc where status='1' and country_code='%s' and get_dates>='%s';" % (country_en, _date)
        # 查询美国订单表
        sql2 = "select * from manually_create_order where status='1' and country_code='%s' and get_dates>='%s';" % (country_en, _date)
        # 查询加拿大订单表
        sql3 = "select * from manually_create_order_ups where status='1' and country_code='%s' and get_dates>='%s';" % (country_en, _date)
        # 查询物流系统仓库信息表
        sql4 = "select * from oversea_location_data;"
        # 查询所有所有超时订单数量
        sql5 = "select * from timeout_orders where country='%s' and dates>='%s';" % (country, _date)

    data1 = conf_fun.connect_mysql_or(sql1, type='dict')
    data2 = conf_fun.connect_mysql_or(sql2, type='dict')
    data3 = conf_fun.connect_mysql_or(sql3, type='dict')
    res = conf_fun.connect_mysql_product_supplier(sql4, type='dict')
    res1 = conf_fun.connect_mysql_operation(sql5, type='dict')
    timeout_order_list = [i["Amazon_id"] for i in res1]

    data4 = []
    if len(data1) > 0:
        data4 += data1
    if len(data2) > 0:
        data4 += data2
    if len(data3) > 0:
        data4 += data3

    warehouse_days_data = []
    for i in data4:
        if len(warehouse_days_data) == 0:
            _dict = {
                "warehouse_code": i["warehouse_code"],
                "num": 1,
                "timeout_num": 0
            }
            # 计算获取跟踪单号的时间
            if i["dates"] is not None:
                times = datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")
                if i["get_tracking_no_date"] is not None:
                    _hours = (datetime.datetime.strptime(i["get_tracking_no_date"],"%Y-%m-%d %H:%M:%S") - times).seconds / 60 / 60
                    _dict["minute"] = round(_hours,2)
                else:
                    now_time = datetime.datetime.now()
                    _hours = (now_time - times).seconds / 60 / 60
                    _dict["minute"] = round(_hours,2)
            else:
                _dict["minute"] = 0
            # 判断是否超时
            if i["reference_ture"] in timeout_order_list:
                _dict["timeout_num"] += 1
            # 计算出库时间
            if i["delivery_date"] is not None and i["delivery_date"] != '' and i["dates"] is not None and i["dates"] != '':
                delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                _day = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).days
                _hours = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).seconds / 60 / 60
                _dict["delivery_date"] = _day + round(_hours,2)
            else:
                _dict["delivery_date"] = 0
            # 计算取货
            if i["delivery_date"] is not None and i["delivery_date"] != '' and i["start_time"] is not None and i["start_time"] != '':
                start_time = i["start_time"] + ":00" if len(i["start_time"].split(' ')[1].split(':')) == 2 else i["start_time"]
                delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                _day = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).days
                _hours = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                _dict["pick_up_date"] = _day + round(_hours,2)
            warehouse_days_data.append(_dict)
        else:
            for index, item in enumerate(warehouse_days_data):
                if i["warehouse_code"] == item["warehouse_code"]:
                    # 计算获取追踪号的时间
                    if i["dates"] is not None and i["dates"] != '':
                        times = datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")
                        if i["get_tracking_no_date"] is not None:
                            _hours = (datetime.datetime.strptime(i["get_tracking_no_date"],"%Y-%m-%d %H:%M:%S") - times).seconds / 60 / 60
                            item["minute"] += round(_hours,2)
                        else:
                            now_time = datetime.datetime.now()
                            _hours = (now_time - times).seconds / 60 / 60
                            item["minute"] += round(_hours,2)
                    else:
                        item["minute"] = 0
                    # 判断是否超时
                    if i["reference_ture"] in timeout_order_list:
                        item["timeout_num"] += 1
                    # 计算出库时间
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["dates"] is not None and i["dates"] != '':
                        delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                        _day = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"],"%Y-%m-%dT%H-%M")).days
                        _hours = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).seconds / 60 / 60
                        item["delivery_date"] += _day + round(_hours,2)

                    # 计算取货
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["start_time"] is not None and i["start_time"] != '':
                        start_time = i["start_time"] + ":00" if len(i["start_time"].split(' ')[1].split(':')) == 2 else i["start_time"]
                        delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                        _day = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).days
                        _hours = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                        item["pick_up_date"] += _day + round(_hours,2)

                    item["num"] += 1
                    break
                elif i["warehouse_code"] != item["warehouse_code"] and index == len(warehouse_days_data) - 1:
                    _dict = {
                        "warehouse_code": i["warehouse_code"],
                        "num": 1,
                        "timeout_num": 0
                    }
                    # 计算获取跟踪单号的时间
                    if i["dates"] is not None and i["dates"] != '':
                        times = datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")
                        if i["get_tracking_no_date"] is not None:
                            _hours = (datetime.datetime.strptime(i["get_tracking_no_date"],"%Y-%m-%d %H:%M:%S") - times).seconds / 60 / 60
                            _dict["minute"] = round(_hours, 2)
                        else:
                            now_time = datetime.datetime.now()
                            _hours = (now_time - times).seconds / 60 / 60
                            _dict["minute"] = round(_hours, 2)
                    # 判断是否超时
                    if i["reference_ture"] in timeout_order_list:
                        _dict["timeout_num"] += 1
                    # 计算出库时间
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["dates"] is not None and i["dates"] != '':
                        delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                        _day = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"],"%Y-%m-%dT%H-%M")).days
                        _hours = (datetime.datetime.strptime(delivery_date,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).seconds / 60 / 60
                        _dict["delivery_date"] = _day + round(_hours,2)
                    else:
                        _dict["delivery_date"] = 0
                    # 计算取货
                    if i["delivery_date"] is not None and i["delivery_date"] != '' and i["start_time"] is not None and i["start_time"] != '':
                        start_time = i["start_time"] + ":00" if len(i["start_time"].split(' ')[1].split(':')) == 2 else i["start_time"]
                        delivery_date = i["delivery_date"] + ":00" if len(i["delivery_date"].split(' ')[1].split(':')) == 2 else i["delivery_date"]
                        _day = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).days
                        _hours = (datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                        _dict["pick_up_date"] = _day + round(_hours,2)
                    else:
                        _dict["pick_up_date"] = 0
                    warehouse_days_data.append(_dict)
                    break
    # 计算这些数据的平均值
    for i in warehouse_days_data:
        i["warehouse_name"] = i["warehouse_code"]
        for j in res:
            if i["warehouse_code"] == j["code"]:
                i["warehouse_name"] = j["warehouse_name"]
        # 计算跟踪单号平均获取时间
        i["tracking_no_avg_minute"] = str(round(i["minute"] / i["num"], 2)) + "小时"
        # 计算超时订单百分比
        i["timeout_order_ratio"] = str(round(i["timeout_num"] / i["num"], 2) * 100) + "%"
        # 计算平均出库时间
        i["delivery_avg_date"] = str(math.ceil(i["delivery_date"] / i["num"])) + "天"
        # 计算平均取货时间
        i["pick_up_avg_date"] = str(math.ceil(i["pick_up_date"] / i["num"])) + "天"
        # 计算平均处理时间
        i["deal_avg_date"] = str(math.ceil(i["delivery_date"] / i["num"] + i["pick_up_date"] / i["num"])) + "天"

    warehouse_name_list = [i["warehouse_name"] for i in warehouse_days_data]
    return JsonResponse({"code": 200, "msg": "success","warehouse_days_data": warehouse_days_data,
                         "warehouse_name_list": warehouse_name_list,"date_list": date_list})



# 订单查询
# 查询订单详情
def get_order_detail(request):
    country = request.POST.get("country",None)
    tracking_no = request.POST.get("tracking_no",None)
    store1,country1 = store_country_code('',country,'en',type='upper')
    print(country,store1,country1)
    num = 0
    # 查询订单发货渠道
    if country1 == "US":
        num = 13
        sql = "select * from manually_create_order where tracking_no='%s' and country_code='%s';"%(tracking_no,country1)
    elif country1 == "CA":
        num = 13
        sql = "select * from manually_create_order_ups where tracking_no='%s' and country_code='%s';" % (tracking_no, country1)
    else:
        print(store1,country1)
        num = 7
        # 查询欧洲订单数据表
        if country1 == "UK":
            country1 = "GB"
        sql = "select * from manually_create_order_yc where tracking_no='%s' and country_code='%s';"%(tracking_no,country1)
    try:
        print("sql===",sql)
        res = connect_mysql(sql,dbs='order',type='dict')
        if len(res) > 0:
            if res[0]["content"] is not None:
                _list =[]
                _str = res[0]["content"].replace("'",'"')
                if country1 == "US" or country1 == "CA":
                    pass
                else:
                    _str = res[0]["content"].replace("'",'"')
                    print("===",_str)
                    count = 0
                    while count == 0:
                        if '"s' in _str:
                            _str = _str.replace('"s', " is")
                        elif '"ve' in _str:
                            _str = _str.replace('"ve', " have")
                        elif '"re' in _str:
                            _str = _str.replace('"re', " are")
                        else:
                            count += 1

                _dic = eval(_str)
                _list.append(_dic)

                if type(_list[0]).__name__ == "list" or type(_list[0]).__name__ == "tuple":
                    print(type(_list[0]).__name__)
                    data1 = _list[0]
                else:
                    print(type(_list[0]).__name__)
                    data1 = _list

                print("data1==",data1)
                data1 = data1[::-1]
                for i in data1:
                    # 时间转换
                    if len(i["time"].split(' ')[1].split(':')) == 2:
                        if '/' in i["time"]:
                            time_list = i["time"].split(' ')[0].split('/')
                            if len(time_list[2]) == 4:
                                _time = '-'.join(time_list[::-1]) + ' ' + i["time"].split(' ')[1]
                            else:
                                _time = '-'.join(time_list) + ' ' + i["time"].split(' ')[1]
                            i["time_zh"] = datetime.datetime.strftime(datetime.datetime.strptime(_time, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=num),"%Y-%m-%d %H:%M")
                        else:
                            i["time_zh"] = datetime.datetime.strftime(datetime.datetime.strptime(i["time"],"%Y-%m-%d %H:%M") + datetime.timedelta(hours=num),"%Y-%m-%d %H:%M")
                    elif len(i["time"].split(' ')[1].split(':')) == 3:
                        i["time_zh"] = datetime.datetime.strftime(datetime.datetime.strptime(i["time"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=num),"%Y-%m-%d %H:%M:%S")
                    content = ""
                    if "status" in i.keys():
                        content += i["status"] + " "

                    if "place_name" in i.keys():
                        content += " 地点：" + i["place_name"]

                    if content != "":
                        i["content"] = content

                return JsonResponse({"code":200,"msg":"success","data":data1,"last_time":res[0]["capture_time"],"get_tracking_no_date":res[0]["get_tracking_no_date"]})
            else:
                return JsonResponse({"code": 200, "msg": "未查询到详细物流信息", "data": [],"last_time":res[0]["capture_time"],"get_tracking_no_date":res[0]["get_tracking_no_date"]})
        else:
            return JsonResponse({"code":200,"msg":"未查询到此国家下该追踪单号的相关信息，请检查输入的订单号或国家是否有误！"})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# ------------------------>海外仓配送模板监控
# 获取搜索框的数据
def get_template_data(request):
    # 查询数据表中待处理的数据
    sql = "select * from distribution_template where status='0';"
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    _list = []
    _list1 = []
    for i in res:
        # 站点国家归类
        if len(_list) == 0:
            _dict = {
                "station":i["station"],
                "country":[i["country"]]
            }
            _list.append(_dict)
        else:
            for index,j in enumerate(_list):
                if i["station"] == j["station"]:
                    j["country"].append(i["country"])
                    break
                elif i["station"] != j["station"] and index == len(_list)-1:
                    _dict = {
                        "station": i["station"],
                        "country": [i["country"]]
                    }
                    _list.append(_dict)
                    break

        # 国家、sku归类
        if len(_list1) == 0:
            _dict = {
                "station":i["station"],
                "country": i["country"],
                "skus": [{"sku":i["sku"],"change_reason":i["change_reason"],"template_type":i["template_type"]}]
            }
            _list1.append(_dict)
        else:
            for index,j in enumerate(_list1):
                if i["station"] == j["station"] and i["country"] == j["country"]:
                    j["skus"].append({"sku":i["sku"],"change_reason":i["change_reason"],"template_type":i["template_type"]})
                    break
                elif i["station"] != j["station"] and i["country"] != j["country"] and index == len(_list1)-1:
                    _dict = {
                        "station": i["station"],
                        "country": i["country"],
                        "skus": [{"sku":i["sku"],"change_reason":i["change_reason"],"template_type":i["template_type"]}]
                    }
                    _list1.append(_dict)
                    break

    return JsonResponse({"code":200,"msg":"success","data":_list,"data1":_list1})

# 模板上传
def upload_template(request):
    station = request.POST.get("station",None)
    country = request.POST.get("country",None)
    sku = request.POST.get("sku",None)
    step = request.POST.get("step", None)
    file = request.FILES.get("file", None)
    print(station,country,sku,step,file.name)

    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    path = "/static/data/template_data/" + station+country + "/" + sku + "/" + now
    creatDir(path)
    path1 = "/home/by_operate" + path + "/" + file.name
    with open(path1, 'wb') as f:
        for line in file:
            f.write(line)

    # 将数据存储到数据库
    # 先查询数据库原来的资料
    sql = "select * from distribution_template where station='%s' and country='%s' and sku='%s';"%(station,country,sku)
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    _str = ""
    if len(res) == 0:
        _str = file.name
    else:
        _str = res[0][step] + "," + file.name
    _list = ['step_one','step_two','step_three','step_four','step_five']
    _list.remove(step)
    count= 0
    for i in _list:
        if res[0][i] is None:
            count += 1
    if count == 0:
        sql1 = "update distribution_template set %s='%s',status='1' where station='%s' and country='%s' and sku='%s';"%\
               (step,_str,station,country,sku)
    else:
        sql1 = "update distribution_template set %s='%s' where station='%s' and country='%s' and sku='%s';" % \
               (step, _str, station, country, sku)
    conf_fun.connect_mysql_operation(sql1)
    return JsonResponse({"code":200,"msg":"success"})


# 海外仓配模板——主管页面
# 获取选择仓库下所有模板
def get_template(request):
    country = request.GET.get("country", None)
    warehouse_name = request.GET.get("warehouse_name",None)
    try:
        sql = "select * from distribution_warehouse_template where country='%s' and warehouse_name='%s' and status='1';"%(country,warehouse_name)
        res = conf_fun.connect_mysql_operation(sql,type='dict')
        data = [i["template_type"] for i in res]
        return JsonResponse({"code": 200, "msg": "success","data":data})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:" + str(e)})


# 主管新增任务
def add_work(request):
    warehouse_name = request.GET.get("warehouse_name",None)
    station = request.GET.get("station",None)
    country = request.GET.get("country",None)
    reason = request.GET.get("reason",None)
    template_type = request.GET.get("template_type",None)
    # try:
    # 查询仓库模板表，此仓库存在则更新仓库模板表，否则新增
    sql = "select * from distribution_warehouse_template where country='%s' and warehouse_name='%s' and status='1';"%(country,warehouse_name)
    res = conf_fun.connect_mysql_operation(sql)
    _date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    if len(res) > 0:
        sql1 = "update distribution_warehouse_template set template_type='%s' and update_times='%s' where country='%s' and warehouse_name='%s';"\
               %(template_type,_date,country,warehouse_name)
    else:
        sql1 = "insert into distribution_warehouse_template (station,country,warehouse_name,template_type,update_times,update_reason,status) values " \
               "('%s','%s','%s','%s','%s','%s')"%(station,country,warehouse_name,template_type,_date,reason,'1')
    conf_fun.connect_mysql_operation(sql1)

    # 查询此仓库下所有产品对应的sku
    sql2 = "select * from order_integrate where store='%s' and country='%s' and warehouse_name='%s';"%(station,country,warehouse_name)
    res2 = conf_fun.connect_mysql_operation(sql2,dbs='supply_chain',type='dict')
    product_list = []
    for i in res2:
        if len(product_list) == 0:
            _dic = {
                "product_code":i["product_number"],
                "store":i["store"],
                "country":i["country"]
            }
            product_list.append(_dic)
        else:
            for index,j in enumerate(product_list):
                if i["product_number"] != j["product_code"] and index == len(product_list)-1:
                    _dic = {
                        "product_code": i["peoduct_number"],
                        "store": i["store"],
                        "country": i["country"]
                    }
                    product_list.append(_dic)
                    break

    # 通过产品编码查询sku
    sql3 = "select * from commodity_information;"
    res3 = conf_fun.connect_mysql_operation(sql3,type='dict')

    sql4 = "insert into distribution_template (station,country,warehouse_name,sku,change_reason,template_type,dates) values "
    for i in product_list:
        store1,country1 = store_country_code(i["store"],i["country"],'en',type='upper')
        for j in res3:
            if i["product_code"] == j["product_code"] and i["store"] == j["site"] and country1 == j["country"]:
                sql4 += "('" + i["store"] + "','" + i["country"] + "','" + warehouse_name + "','" + j["sku"] + "','" + reason + "','" + template_type + "','" + _date + "'),"

    sql4 = sql4[:-1]
    print("sql4===",sql4)
    # 存入模板表成为待处理sku
    conf_fun.connect_mysql_operation(sql4)
    return JsonResponse({"code":200,"msg":"success"})
    # except Exception as e:
    #     return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 获取所有需要审核的记录
def get_examined_data(request):
    try:
        sql = "select * from distribution_warehouse_template where status='0';"
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        return JsonResponse({"code":200,"msg":"success","data":data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 审核超时更改需求
def examined_template_update(request):
    id = request.GET.get("id",None)
    station = request.GET.get("station", None)
    country = request.GET.get("country",None)
    warehouse_name = request.GET.get("warehouse_name",None)
    try:
        # 修改状态为1
        sql = "update distribution_warehouse_template set status='1' where id='%s';"%(int(id))
        conf_fun.connect_mysql_operation(sql)

        # 查询此仓库下所有产品对应的sku
        sql2 = "select * from order_integrate where store='%s' and country='%s' and warehouse_name='%s';"%(station,country,warehouse_name)
        res2 = conf_fun.connect_mysql_operation(sql2, dbs='supply_chain', type='dict')
        product_list = []
        for i in res2:
            if len(product_list) == 0:
                _dic = {
                    "product_code": i["peoduct_number"],
                    "store": i["store"],
                    "country": i["country"]
                }
                product_list.append(_dic)
            else:
                for index, j in enumerate(product_list):
                    if i["product_number"] != j["product_code"] and index == len(product_list) - 1:
                        _dic = {
                            "product_code": i["peoduct_number"],
                            "store": i["store"],
                            "country": i["country"]
                        }
                        product_list.append(_dic)
                        break

        # 通过产品编码查询sku
        sql3 = "select * from commodity_information;"
        res3 = conf_fun.connect_mysql_operation(sql3, type='dict')

        _date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        sql4 = "insert into distribution_template (station,country,warehouse_name,sku,change_reason,dates) values "
        for i in product_list:
            store1, country1 = store_country_code(i["store"], i["country"], 'en', type='upper')
            for j in res3:
                if i["product_code"] == j["product_code"] and i["store"] == j["site"] and country1 == j["country"]:
                    sql4 += "('" + i["store"] + "','" + i["country"] + "','" + warehouse_name + "','" + j[
                        "sku"] + "','" + reason + "','" + _date + "'),"

        sql4 = sql4[:-1]
        print("sql4===", sql4)
        # 存入模板表成为待处理sku
        conf_fun.connect_mysql_operation(sql4)

        # 获取最新的待审核模板
        sql5 = "select * from distribution_warehouse_template where status='0';"
        data = conf_fun.connect_mysql_operation(sql5, type='dict')
        return JsonResponse({"code": 200, "msg": "success","data":data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 获取待修改的模板数据
def template_datas(request):
    station = request.GET.get("station",None)
    country = request.GET.get("country", None)
    warehouse_name = request.GET.get("warehouse_name", None)
    template_type = request.GET.get("template_type", None)

    sql = "select * from warehouse_template_data where station='%s' and country='%s' and warehouse_name='%s' and template_type='%s';"\
          %(station,country,warehouse_name,template_type)
    print(sql)
    data = conf_fun.connect_mysql_operation(sql,type='dict')
    return JsonResponse({"code": 200, "mag": "success","data":data})

# 模板修改
def template_datas_update(request):
    data = json.loads(request.POST.get("data",None))
    # 遍历修改
    for i in data:
        if i["step"] == "1":
            files = request.FLIES.getlist("files1",[])
        elif i["step"] == "2":
            files = request.FLIES.getlist("files2",[])
        elif i["step"] == "3":
            files = request.FLIES.getlist("files3",[])
        elif i["step"] == "4":
            files = request.FLIES.getlist("files4",[])
        elif i["step"] == "5":
            files = request.FLIES.getlist("files5",[])
        elif i["step"] == "6":
            files = request.FLIES.getlist("files6",[])

        # 遍历存储文件
        _str = ""
        path = "/static/data/template_datas/" + i["station"] + i["country"] + "/" + i["warehouse_name"] + "/" + i["step"]
        creatDir(path)
        for j in files:
            _str += j.name
            path1 = "/home/by_operate" + path + "/" + j.name
            with open(path1, 'wb') as f:
                for line in f:
                    f.write(line)
        # 修改数据库
        sql = "update warehouse_template_data set title='{}' and content='{}' and images='{}' where station='{}' and country='{}' and warehouse_name='{}' and template_type='{}';"
        sql.format(i["title"],i["content"],i["images"],i["station"],i["country"],i["warehouse_name"],i["template_type"])
        conf_fun.connect_mysql_operation(sql)
    return JsonResponse({"code":200,"mag":"success"})


# ---------------->订单分析
# 订单退款率——获取站点、国家
def refund_rate(request):
    # 查询退款订单
    sql = "select * from refund_order;"
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    _list = []
    _list1 = []
    _list2 = []

    for i in res:
        # 整理渠道、站点
        if len(_list) == 0:
            _dict = {
                "channel":i["channel"],
                "station":[i["station"]]
            }
            _list.append(_dict)
        else:
            for index,j in enumerate(_list):
                if i["channel"] == j["channel"]:
                    j["station"].append(i["station"])
                    break
                elif i["channel"] != j["channel"] and index == len(_list)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": [i["station"]]
                    }
                    _list.append(_dict)
                    break

        # 整理站点、国家
        if len(_list1) == 0:
            _dict = {
                "channel":i["channel"],
                "station":i["station"],
                "country":[i["country"]]
            }
            _list1.append(_dict)
        else:
            for index,j in enumerate(_list1):
                if i["channel"] == j["channel"] and i["station"] == j["station"]:
                    j["country"].append(i["country"])
                    break
                elif i["channel"] != j["channel"] and i["station"] != j["station"] and index == len(_list1)-1 \
                    or i["channel"] == j["channel"] and i["station"] != j["station"] and index == len(_list1)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": i["station"],
                        "country": [i["country"]]
                    }
                    _list1.append(_dict)
                    break

        # 整理国家品名
        if len(_list2) == 0:
            _dict = {
                "channel":i["channel"],
                "station":i["station"],
                "country":i["country"],
                "product_name":[i["product_name"]]
            }
            _list2.append(_dict)
        else:
            for index,j in enumerate(_list2):
                if i["channel"] == j["channel"] and i["station"] == j["station"] and i["country"] == j["country"]:
                    j["product_name"].append(i["product_name"])
                    break
                elif i["channel"] != j["channel"] and i["station"] != j["station"] and i["country"] != j["country"] and index == len(_list2)-1 \
                     or i["channel"] != j["channel"] and i["station"] == j["station"] and i["country"] != j["country"] and index == len(_list2)-1 \
                     or i["channel"] == j["channel"] and i["station"] != j["station"] and i["country"] != j["country"] and index == len(_list2)-1 \
                     or i["channel"] == j["channel"] and i["station"] == j["station"] and i["country"] != j["country"] and index == len(_list2)-1\
                     or i["channel"] != j["channel"] and i["station"] == j["station"] and i["country"] == j["country"] and index == len(_list2)-1\
                     or i["channel"] == j["channel"] and i["station"] != j["station"] and i["country"] == j["country"] and index == len(_list2)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": i["station"],
                        "country": i["country"],
                        "product_name": [i["product_name"]]
                    }
                    _list2.append(_dict)
                    break


    print("_list===",_list)
    print("_list1===", _list1)
    print("_list2===", _list2)
    return JsonResponse({"code":200,"msg":"success","data":_list,"data1":_list1,"data2":_list2})


# 订单退款率——获取数据
def refund_rate_data(request):
    channel = request.POST.get("channel",None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    product_name = request.POST.get("product_name", None)
    refund_dates = request.POST.get("days", None)
    page = request.POST.get("page",1)
    print(channel,station,country,product_name,refund_dates)

    _list = [
        {"key":"channel","value":channel},
        {"key": "station", "value": station},
        {"key": "country", "value": country},
        {"key": "product_name", "value": product_name},
        {"key": "refund_dates", "value": refund_dates}
    ]

    sql = "select * from refund_order where "
    for i in _list:
        if i["value"] is not None:
            if i["key"] == "dates":
                now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
                date_list = get_days(now,int(i["value"]))
                t = tuple(date_list)
                sql += i["key"] + " in %s and "%(t)
            else:
                sql += i["key"] + "='" + i["value"] + "' and "
    sql = sql[:-5]
    print("sql===",sql)
    data = conf_fun.connect_mysql_operation(sql,type='dict')
    _dict = {}
    for index,i in enumerate(data):
        if index == 0:
            _dict["channel"] = i["channel"]
            _dict["station"] = i["station"]
            _dict["country"] = i["country"]
            _dict["product_code"] = i["product_code"]
            _dict["product_name"] = i["product_name"]
            _dict["sku"] = ""
            _dict["refund_num"] = int(i["refund_orders"])
            _dict["all_num"] = int(i["all_orders"])
        else:
            _dict["refund_num"] += int(i["refund_orders"])
            _dict["all_num"] += int(i["all_orders"])
    if len(data) > 0:
        _dict["refund_rate"] = str(round(_dict["refund_num"]/_dict["all_num"],2) * 100) + "%"
        data.insert(0,_dict)

    total_num = len(data)
    start = int(page) * 50 - 50
    end = int(page) * 50
    data1 = data[start:end]
    return JsonResponse({"code":200,"msg":"success","data":data1,"total_num":total_num})


# 退货时间监控——获取站点国家数据
def refund_times(request):
    # 查询退款订单
    sql = "select * from refund_order;"
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    _list = []
    _list1 = []

    for i in res:
        # 整理渠道、站点
        if len(_list) == 0:
            _dict = {
                "channel":i["channel"],
                "station":[i["station"]]
            }
            _list.append(_dict)
        else:
            for index,j in enumerate(_list):
                if i["channel"] == j["channel"]:
                    j["station"].append(i["station"])
                    break
                elif i["channel"] != j["channel"] and index == len(_list)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": [i["station"]]
                    }
                    _list.append(_dict)
                    break

        # 整理站点、国家
        if len(_list1) == 0:
            _dict = {
                "channel":i["channel"],
                "station":i["station"],
                "country":[i["country"]]
            }
            _list1.append(_dict)
        else:
            for index,j in enumerate(_list1):
                if i["channel"] == j["channel"] and i["station"] == j["station"]:
                    j["country"].append(i["country"])
                    break
                elif i["channel"] != j["channel"] and i["station"] != j["station"] and index == len(_list1)-1 \
                    or i["channel"] == j["channel"] and i["station"] != j["station"] and index == len(_list1)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": i["station"],
                        "country": [i["country"]]
                    }
                    _list1.append(_dict)
                    break

    print("_list===",_list)
    print("_list1===", _list1)
    return JsonResponse({"code":200,"msg":"success","data":_list,"data1":_list1})


# 退货时间监控——获取条形图数据
def refund_times_monitor(request):
    channel = request.POST.get("channel", None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    days = request.POST.get("days", None)
    print(channel, station, country, days)
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    date_list = get_days(now,int(days))
    t = tuple(date_list)
    # 查询此时间段所有退货订单
    sql = "select * from refund_order where channel='%s' and station='%s' and country='%s' and refund_dates in %s;"%(channel,station,country,t)
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    # 查询此时间段所有订单量
    store1,country1 = store_country_code(station,country,'en','upper')
    # 查询欧洲订单数据表
    sql1 = "select * from manually_create_order_yc where station='%s' and country_code='%s';"%(store1,country1)
    # 查询美国订单表
    sql2 = "select * from manually_create_order where station='%s' and country_code='%s';"%(store1,country1)
    # 查询加拿大订单表
    sql3 = "select * from manually_create_order_ups where station='%s' and country_code='%s';"%(store1,country1)
    data1 = conf_fun.connect_mysql_or(sql1, type='dict')
    data2 = conf_fun.connect_mysql_or(sql2, type='dict')
    data3 = conf_fun.connect_mysql_or(sql3, type='dict')
    data4 = []
    if len(data1) > 0:
        data4 += data1
    if len(data2) > 0:
        data4 += data2
    if len(data3) > 0:
        data4 += data3

    data5 = []
    for i in data4:
        if ":" in i["get_dates"]:
            _time = i["get_dates"].split(' ')[0]
        else:
            _time = i["get_dates"]

        if _time in date_list:
            data5.append(i)

    # 获取不同退货时间的订单数量
    data6 = []
    for i in range(45):
        _dict = {
            "day":str(i+1) + "天",
            "order_num":0
        }
        for j in res:
            days = (datetime.datetime.strptime(j["refund_dates"],"%Y-%m-%d") - datetime.datetime.strptime(j["purchase_date"],"%Y-%m-%d")).days
            if days == (i+1):
                _dict["order_num"] += 1

        data6.append(_dict)

    print("data6==",data6)
    return JsonResponse({"code":200,"msg":"success","all_orders":len(data5),"refund_orders":len(res),"data":data6})



# 退货时间详情——获取国家站点
def refund_times_detail(request):
    # 查询退款订单
    sql = "select * from refund_date_detail;"
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    _list = []
    _list1 = []

    for i in res:
        # 整理渠道、站点
        if len(_list) == 0:
            _dict = {
                "channel":i["channel"],
                "station":[i["station"]]
            }
            _list.append(_dict)
        else:
            for index,j in enumerate(_list):
                if i["channel"] == j["channel"]:
                    j["station"].append(i["station"])
                    break
                elif i["channel"] != j["channel"] and index == len(_list)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": [i["station"]]
                    }
                    _list.append(_dict)
                    break

        # 整理站点、国家
        if len(_list1) == 0:
            _dict = {
                "channel":i["channel"],
                "station":i["station"],
                "country":[i["country"]]
            }
            _list1.append(_dict)
        else:
            for index,j in enumerate(_list1):
                if i["channel"] == j["channel"] and i["station"] == j["station"]:
                    j["country"].append(i["country"])
                    break
                elif i["channel"] != j["channel"] and i["station"] != j["station"] and index == len(_list1)-1 \
                    or i["channel"] == j["channel"] and i["station"] != j["station"] and index == len(_list1)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": i["station"],
                        "country": [i["country"]]
                    }
                    _list1.append(_dict)
                    break
    return JsonResponse({"code":200,"msg":"success","data":_list,"data1":_list1})


# 退货时间详情——获取数据
def refund_times_deatil_data(request):
    channel = request.POST.get("channel",None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    purchase_date = request.POST.get("purchase_date", None)
    sku = request.POST.get("sku", None)
    warehouse_name = request.POST.get("warehouse_name", None)
    order_id = request.POST.get("order_id", None)
    refund_type = request.POST.get("refund_type", None)
    print(channel,country,station,purchase_date,sku,warehouse_name,order_id,refund_type)
    _list = [
        {"key":"channel","value":channel},
        {"key": "station", "value": station},
        {"key": "country", "value": country},
        {"key": "purchase_date", "value": purchase_date},
        {"key": "sku", "value": sku},
        {"key": "warehouse_name", "value": warehouse_name},
        {"key": "order_id", "value": order_id},
        {"key": "refund_type", "value": refund_type}
    ]
    sql = "select * from refund_date_detail"
    count = 0
    for i in _list:
        if i["value"] is not None:
            if count == 0:
                sql += " where " + i["key"] + "='" + i["value"] + "' and "
                count += 1
            else:
                sql += i["key"] + "='" + i["value"] + "' and "
                count += 1


    sql = sql[:-5]
    data = conf_fun.connect_mysql_operation(sql,type='dict')
    return JsonResponse({"code":200,"msg":"success","data":data})



# 退货原因分析——获取国家站点
def refund_reason(request):
    # 查询退款订单
    sql = "select * from refund_date_detail;"
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    _list = []
    _list1 = []

    for i in res:
        # 整理渠道、站点
        if len(_list) == 0:
            _dict = {
                "channel":i["channel"],
                "station":[i["station"]]
            }
            _list.append(_dict)
        else:
            for index,j in enumerate(_list):
                if i["channel"] == j["channel"]:
                    j["station"].append(i["station"])
                    break
                elif i["channel"] != j["channel"] and index == len(_list)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": [i["station"]]
                    }
                    _list.append(_dict)
                    break

        # 整理站点、国家
        if len(_list1) == 0:
            _dict = {
                "channel":i["channel"],
                "station":i["station"],
                "country":[i["country"]]
            }
            _list1.append(_dict)
        else:
            for index,j in enumerate(_list1):
                if i["channel"] == j["channel"] and i["station"] == j["station"]:
                    j["country"].append(i["country"])
                    break
                elif i["channel"] != j["channel"] and i["station"] != j["station"] and index == len(_list1)-1 \
                    or i["channel"] == j["channel"] and i["station"] != j["station"] and index == len(_list1)-1:
                    _dict = {
                        "channel": i["channel"],
                        "station": i["station"],
                        "country": [i["country"]]
                    }
                    _list1.append(_dict)
                    break
    return JsonResponse({"code":200,"msg":"success","data":_list,"data1":_list1})


# 退货原因分析——获取数据
def refund_reason_date(request):
    channel = request.POST.get("channel", None)
    station = request.POST.get("station", None)
    country = request.POST.get("country", None)
    type = request.POST.get("type", None)
    product_code = request.POST.get("product_code", None)
    product_name = request.POST.get("product_name", None)
    sku = request.POST.get("sku", None)
    warehouse_type = request.POST.get("warehouse_type", None)
    warehouse_name = request.POST.get("warehouse_name", None)
    purchase_date = request.POST.get("purchase_date", None)
    refund_date = request.POST.get("refund_date", None)
    refund_type = request.POST.get("refund_type", None)
    refund_reason = request.POST.get("refund_reason", None)
    deal_person = request.POST.get("deal_person", None)
    page = request.POST.get("page", 1)
    print(channel, country, station, type, product_code, product_name, sku, warehouse_type)
    _list = [
        {"key": "channel", "value": channel},
        {"key": "station", "value": station},
        {"key": "country", "value": country},
        {"key": "type", "value": type},
        {"key": "product_code", "value": product_code},
        {"key": "product_name", "value": product_name},
        {"key": "sku", "value": sku},
        {"key": "warehouse_type", "value": warehouse_type},
        {"key": "warehouse_name", "value": warehouse_name},
        {"key": "purchase_date", "value": purchase_date},
        {"key": "refund_date", "value": refund_date},
        {"key": "refund_type", "value": refund_type},
        {"key": "refund_reason", "value": refund_reason},
        {"key": "deal_person", "value": deal_person}
    ]
    sql = "select * from refund_date_detail"
    count = 0
    for i in _list:
        if i["value"] is not None:
            if count == 0:
                if i["key"] == 'purchase_date' or i["key"] == 'refund_date':
                    if '_' in i["value"]:
                        # 获取两个日期之间的所有所有日期
                        start_time = datetime.datetime.strptime(i["value"].split('_')[0],"%Y-%m-%d")
                        end_time = datetime.datetime.strptime(i["value"].split('_')[1],"%Y-%m-%d")
                        date_list = []
                        while start_time <= end_time:
                            _str = datetime.datetime.strftime(start_time, "%Y-%m-%d")
                            date_list.append(_str)
                            start_time += datetime.timedelta(days=1)
                        t = tuple(date_list)
                        sql += " where " + i["key"] + " in " + t + " and "
                    else:
                        sql += " where " + i["key"] + "='" + i["value"] + "' and "

                else:
                    sql += " where " + i["key"] + "='" + i["value"] + "' and "
                count += 1
            else:
                if i["key"] == 'purchase_date' or i["key"] == 'refund_date':
                    if '_' in i["value"]:
                        # 获取两个日期之间的所有所有日期
                        start_time = datetime.datetime.strptime(i["value"].split('_')[0], "%Y-%m-%d")
                        end_time = datetime.datetime.strptime(i["value"].split('_')[1], "%Y-%m-%d")
                        date_list = []
                        while start_time <= end_time:
                            _str = datetime.datetime.strftime(start_time, "%Y-%m-%d")
                            date_list.append(_str)
                            start_time += datetime.timedelta(days=1)
                        t = tuple(date_list)
                        sql += i["key"] + " in " + t + " and "
                    else:
                        sql += i["key"] + "='" + i["value"] + "' and "

                else:
                    sql += i["key"] + "='" + i["value"] + "' and "
                count += 1

    sql = sql[:-5]
    print("sql===",sql)
    data = conf_fun.connect_mysql_operation(sql, type='dict')

    total_num = len(data)
    start = int(page) * 50 - 50
    end = int(page) * 50
    data1 = data[start:end]
    return JsonResponse({"code": 200, "msg": "success", "data": data1,"total_num":total_num})


# 单个订单发货
def single_order_deliver(request):
    order_id = request.POST.getlist('order_id')
    country_code = request.POST.getlist('country_code')
    city = request.POST.getlist('city')
    address = request.POST.getlist('address')
    name = request.POST.getlist('name')
    tel = request.POST.getlist('tel')
    zip_code = request.POST.getlist('zip_code')
    err_order = request.POST.get('err_order')
    doorplate = request.POST.get('doorplate')
    address2 = request.POST.getlist('address2')

    dates = str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H-%M'))

    order_codes = []
    err_data = []

    for i in range(len(order_id)):
        order_id1 = order_id[i]
        country_code = country_code[i]
        city = city[i]
        address = address[i]
        address2 = address2[i]
        name = name[i]
        tel = tel[i]
        zip_code = zip_code[i]

        if len(address) > 29:
            err_data.append([order_id1, "地址1超长!"])
            continue
        if len(address2) > 29:
            err_data.append([order_id1, "地址2超长!"])
            continue

        tel = re.sub("\D", "", tel)
        order_id1 = order_id1.replace(" ", "")
        name = name.replace("\"", "\'")
        if len(name) > 29:
            err_data.append([order_id1, "名字超长!"])
            continue

        if err_order in ['Y', 'YS']:
            if doorplate is None:
                sql = "select doorplate from manually_create_order_yc where reference_no='{}'"
                sql = sql.format(order_id1)
                doorplate_res = conf_fun.connect_mysql_re(sql, dbs='order')
                doorplate = doorplate_res[0][0]

        sql = "select id from manually_create_order_yc where reference_no='{}'"
        sql = sql.format(order_id1)
        order_num = conf_fun.connect_mysql_re(sql, dbs='order')
        if len(order_num) == 0:
            err_data.append([order_id1, "数据库中没有该订单号!"])
            continue
        sql = "update manually_create_order_yc set country_code='{}',city='{}',name='{}',phone='{}'," \
              "address1='{}',zipcode='{}',dates='{}', doorplate='{}',is_bad='1',address2='{}' where reference_no='{}'"
        sql = sql.format(country_code, city, name, tel, address, zip_code, dates, doorplate, address2, order_id1)
        conf_fun.connect_mysql_re(sql, dbs='order')

        order_codes.append(order_id1)

    if err_order == 'YS':
        for i in order_codes:
            sql = "delete from err_order_data where order_id='{}'"
            sql = sql.format(order_codes[i])
            conf_fun.connect_mysql_re(sql, dbs='order')

    if err_order == 'Y' and order_id[0] in order_codes:
        sql = "delete from err_order_data where order_id='{}'"
        sql = sql.format(order_id[0])
        conf_fun.connect_mysql_re(sql, dbs='order')

    if len(err_data) == 0:
        return JsonResponse({"code": 200, "msg": "订单更新成功!订单号为: " + str(order_codes)})
    else:
        err_str = ''
        for i in err_data:
            err_str += '订单号为' + i[0] + ',错误原因为:' + i[1] + ','
        return JsonResponse({"code": 200, "msg": "如下订单更新成功,订单号为: " + str(order_codes) + "如下订单创建失败:" + err_str})


# 错误订单查询
def err_order_select(request):
    sql = "select order_id,eod.country_code,yc.station,reason,eod.remark,eod.dates from err_order_data eod join manually_create_order_yc" \
          " yc on eod.order_id=yc.reference_no"
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res})


# 错误订单详细信息
def err_order_detail(request):
    order_id = request.GET.get('order_id')

    sql = "select eod.*,yc.doorplate,yc.true_site from err_order_data eod join manually_create_order_yc yc on " \
          "eod.order_id=yc.reference_no where order_id='{}'"
    sql = sql.format(order_id)
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res})


# 错误订单删除
def err_order_delete(request):
    order_id = request.POST.get('order_id')

    sql = "delete from err_order_data where order_id='{}'"
    sql = sql.format(order_id)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": "删除成功!"})


# 美国发货
def usa_order_deliver(request):
    order_id = request.POST.get('order_id')
    province_code = request.POST.get('province_code')
    city = request.POST.get('city')
    address = request.POST.get('address')
    name = request.POST.get('name')
    tel = request.POST.get('tel')
    zip_code = request.POST.get('zip_code')
    sku = request.POST.get('sku')
    delivery = request.POST.get('delivery')
    order_item_id = request.POST.get('details')
    station = request.POST.get('station')

    dates = str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H-%M'))

    if '-FBM' in sku:
        sku = sku.split('-FBM')[0]

    sql = "select yy_sku from sku_comparison where an_sku='{}'"
    sql = sql.format(sku)
    res = conf_fun.connect_mysql_re(sql, dbs='order')
    if len(res) > 0:
        sku = res[0][0]

    package_list = [{"itemList": [{"sku": sku, "quantity": '1'}]}]

    sql = "select product_code from commodity_information where sku='{}'"
    sql = sql.format(sku)
    print(sql)
    product_res = conf_fun.connect_mysql_re(sql, dbs='order')
    try:
        a = product_res[0][0]
    except:
        return JsonResponse({"code": 400, "msg": "没有该SKU"})
    if product_res[0][0] in ['DNZC47-C1', 'DNZC60-C5', 'DNZC60-C1', 'DNZC40-C1']:
        decide_zip = str(int(zip_code[:3]))

        sql = "select warehouse from zip_prices where product_code='{}' and zip_code='{}'"
        sql = sql.format(product_res[0][0], decide_zip)
        print(sql)
        warehouse_res = conf_fun.connect_mysql_re(sql, dbs='order')

        if len(warehouse_res) == 0:
            return JsonResponse({"code": 400, "msg": "该SKU与邮编没有对应的仓库"})
        if warehouse_res[0][0] == 'east' and product_res[0][0] in ['DNZC60-C5', 'DNZC40-C1']:
            # 美东仓
            warehouse_id = '易仓'
            warehouse_code = 'PJWL'
            items = [{"product_sku": sku, "reference_no": 'US' + order_id, "quantity": '1'}]
            data = could_yc.create_order(order_id, 'DE_UPS', 'PJWL', 'US', province_code, city, name, tel, address,
                                         zip_code, items)
            obj = re.compile('>\{(.*?)\}<')
            ret = obj.search(data.text)
            data = ret.group()[1:-1]

        elif warehouse_res[0][0] == 'east' and product_res[0][0] in ['DNZC47-C1', 'DNZC60-C1']:
            # 纽约仓
            warehouse_id = '易仓'
            warehouse_code = 'NJPJ'
            items = [{"product_sku": sku, "reference_no": 'US' + order_id, "quantity": '1'}]
            data = could_yc.create_order(order_id, 'BY-US-NJ-UPS', 'NJPJ', 'US', province_code, city, name, tel,
                                         address, zip_code, items)
            obj = re.compile('>\{(.*?)\}<')
            ret = obj.search(data.text)
            data = ret.group()[1:-1]

        else:
            warehouse_id = '魔方云仓'
            warehouse_code = 'USA_LA'
            data = could_mf.create_order(order_id, name, 'USA_LA', tel, 'US', city, province_code, address, zip_code,
                                         package_list)

    else:
        warehouse_id = '魔方云仓'
        data = could_mf.create_order(order_id, name, 'USA_LA', tel, 'US', city, province_code, address, zip_code,
                                     package_list)
    data = json.loads(data)

    if warehouse_id == '魔方云仓':
        try:
            order_status = data['orderList'][0]['succeed']
            if order_status == 'false':
                return JsonResponse({"code": 400, "msg": data['orderList'][0]['errorMessage']})

            sysOrderId = data['orderList'][0]['sysOrderId']
            sql = "insert into manually_create_order(customer_order_number,contact_name,warehouse_code,phone_number," \
                  "country_code,city,state,street,zip_code,sku,quantity,sysOrderId,ShipmentServiceLevelCategory," \
                  "OrderItemId,reference_ture,dates,is_all,station) values ('{}','{]','{}','{}','{}','{]','{}','{}'," \
                  "'{}','{]','{}','{}','{}','{]','{}','{}','{}','{]')"
            sql = sql.format(order_id, name, warehouse_code, tel, 'US', city, province_code, address, zip_code, sku,
                             '1', sysOrderId, delivery, order_item_id, order_id, dates, '2', station)
            conf_fun.connect_mysql_re(sql, dbs='order')
        except:
            return JsonResponse({"code": 400, "msg": data['errMsg']})

    else:
        if data['ask'] == 'Failure':
            return JsonResponse({"code": 400, "msg": data['Error']['errMessage']})
        sql = "insert into manually_create_order(customer_order_number,contact_name,warehouse_code,phone_number," \
              "country_code,city,state,street,zip_code,sku,quantity,sysOrderId,ShipmentServiceLevelCategory," \
              "OrderItemId,reference_ture,dates,is_all,station) values ('{}','{]','{}','{}','{}','{]','{}','{}'," \
              "'{}','{]','{}','{}','{}','{]','{}','{}','{}','{]')"
        sql = sql.format(order_id, name, warehouse_code, tel, 'US', city, province_code, address, zip_code, sku,
                         '1', data['order_code'], delivery, order_item_id, order_id, dates, '2', station)
        conf_fun.connect_mysql_re(sql, dbs='order')
    
    return JsonResponse({"code": 200, "msg": "上传成功!"})


# 修复失败订单
def repair_defeated_order(request):
    order_id = request.POST.get('order_id')
    order_code = request.POST.get('order_code')
    print(order_id, order_code)

    sql = "update manually_create_order_yc set order_code='{}' where reference_no='{}'"
    sql = sql.format(order_code, order_id)
    conf_fun.connect_mysql_re(sql, dbs='order')

    sql = "delete from err_order_data where order_id='{}'"
    sql = sql.format(order_id)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": "修复成功!"})


# 地址超长
def address_overlength(request):
    sql = "select eod.id,order_id,eod.country_code,eod.city,eod.address,eod.name,eod.tel,eod.zip_code,yc.station," \
          "reason from err_order_data eod join manually_create_order_yc yc on eod.order_id=yc.reference_no where " \
          "reason like '地址有%' or reason like '名字有%'"
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res})


# 假单号查看
def fake_tracking_no_view(request):
    dates = request.POST.get('dates',None)
    status = request.POST.get("status",None)
    if dates is None or dates == '':
        if status is None or status == "全部":
            sql = "select * from fake_tracking order by id desc limit 0,200"
        else:
            sql = "select * from fake_tracking where status='%s' order by id desc limit 0,200"%(status)
        res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
        return JsonResponse({"code": 200, "data": res})
    else:
        _list = dates.split(',')
        print("==",_list)
        _tuple = tuple(_list)
        print("t==",_tuple,type(_tuple))
        if status is None or status == "全部":
            sql = "select * from fake_tracking where dates in %s order by id desc limit 0,200;"%(str(_tuple))
        else:
            sql = "select * from fake_tracking where dates in %s and status='%s' order by id desc limit 0,200;" % (str(_tuple),status)
        # sql = sql.format(dates)
        res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
        return JsonResponse({"code": 200, "data": res})


# 假单号备注编辑
def edit_remark(request):
    id = request.POST.get("id",None)
    remark = request.POST.get("remark",None)
    print(id,remark,type(id))
    try:
        # 修改备注
        sql = "update fake_tracking set remark='{}' where id={};"
        sql = sql.format(remark,int(id))
        conf_fun.connect_mysql_re(sql,dbs='order')
        return JsonResponse({"code":200,"msg":"success"})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:" + str(e)})


# 假单号导出
def fake_tracking_no_export(request):
    dates = request.GET.get('dates',None)
    if dates is None or dates == '':
        sql = "select * from fake_tracking;"
    else:
        sql = "select * from fake_tracking where dates='{}'"
    sql = sql.format(dates)
    res = conf_fun.connect_mysql_re(sql, dbs='order')

    df = pd.DataFrame(res)
    filename = '假单号_' + dates + '.xlsx'
    df.to_excel('/home/by_operate/static/data/fake_tracking_no/' + filename)

    files = open('/home/by_operate/static/data/fake_tracking_no/' + filename, 'rb')
    response = FileResponse(files)
    response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(filename)
    return response


# 加拿大发货所有数据
def ca_shipment_data(request):
    status = request.GET.get('status')
    page = request.GET.get('page')
    page_num = (int(page) - 1) * 50
    if status == '已发货':
        sql = "select * from manually_create_order_ups order by id desc limit {}, 50"
        sql = sql.format(page_num)
        sql1 = "select count(id) as all_num from manually_create_order_ups"
    elif status == '不发':
        sql = "select * from manually_create_order_ups where is_all='6' order by id desc limit {}, 50"
        sql = sql.format(page_num)
        sql1 = "select count(id) as all_num from manually_create_order_ups where is_all='6'"
    elif status == '错误订单':
        sql = "select * from manually_create_order_ups where is_all='5' and id>8862 order by id desc limit {}, 50"
        sql = sql.format(page_num)
        sql1 = "select count(id) as all_num from manually_create_order_ups where is_all='5' and id>8862"
    else:
        sql = "select * from manually_create_order_ups where tracking_no is null and id>4284 and is_all<>'2' and is_all<>'6' order by" \
              " id desc limit {}, 50"
        sql = sql.format(page_num)
        sql1 = "select count(id) as all_num from manually_create_order_ups where tracking_no is null and id>4284 and is_all<>'2' and is_all<>'6'"
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    num = conf_fun.connect_mysql_re(sql1, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res, 'nums': num})


# 加拿大发货 修改数据
def ca_shipment_update_data(request):
    id = request.POST.get('id')
    contact_name = request.POST.get('contact_name')
    phone = request.POST.get('phone')
    city = request.POST.get('city')
    state = request.POST.get('state')
    street = request.POST.get('street')
    zip_code = request.POST.get('zip_code')
    sku = request.POST.get('sku')

    status = request.POST.get('status')

    if status is None:
        sql = "update manually_create_order_ups set contact_name='{}',phone_number='{}',city='{}',state='{}',street='{}'," \
              "zip_code='{}',sku='{}' where id={}"
    else:
        sql = "update manually_create_order_ups set contact_name='{}',phone_number='{}',city='{}',state='{}',street='{}'," \
              "zip_code='{}',sku='{}',is_all='1',failure_reason='' where id={}"

    sql = sql.format(contact_name, phone, city, state, street, zip_code, sku, id)
    print(sql)
    try:
        conf_fun.connect_mysql_re(sql, dbs='order')
        return JsonResponse({"code": 200, "msg": "修改成功"})
    except:
        return JsonResponse({"code": 400, "msg": "修改失败,请联系IT处理!"})


# 加拿大发货 添加追踪编码
def ca_update_tracking_no(request):
    id = request.POST.get('id')
    tracking_no = request.POST.get('tracking_no')
    sql = "update manually_create_order_ups set tracking_no='{}',status='0',is_all='2' where id='{}'"
    sql = sql.format(tracking_no, id)
    try:
        conf_fun.connect_mysql_re(sql, dbs='order')
        return JsonResponse({"code": 200, "msg": "添加成功"})
    except:
        return JsonResponse({"code": 400, "msg": "添加失败,请联系IT处理!"})


# 加拿大发货 查看仓库数据
def ca_warehouse_data(request):
    sql = "select * from warehouse_ups"
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res})


# 加拿大发货 修改仓库数据
def ca_update_warehouse_data(request):
    id = request.POST.get('id')
    sku = request.POST.get('sku')
    lengths = request.POST.get('lengths')
    widths = request.POST.get('widths')
    heights = request.POST.get('heights')
    weights = request.POST.get('weights')
    product_id = request.POST.get('product_id')

    sql = "update warehouse_ups set sku='{}',lengths='{}',widths='{}',heights='{}',weights='{}',product_id='{}' where id='{}'"
    sql = sql.format(sku, lengths, widths, heights, weights, product_id, id)
    try:
        conf_fun.connect_mysql_re(sql, dbs='order')
        return JsonResponse({"code": 200, "msg": "修改成功"})
    except:
        return JsonResponse({"code": 400, "msg": "修改失败,请联系IT处理!"})


# 加拿大发货 新增仓库数据
def ca_insert_warehouse_data(request):
    sku = request.POST.get('sku')
    lengths = request.POST.get('lengths')
    widths = request.POST.get('widths')
    heights = request.POST.get('heights')
    weights = request.POST.get('weights')
    product_id = request.POST.get('product_id')
    sql = "insert into warehouse_ups(sku,lengths,widths,heights,weights,product_id) values ('{}','{}','{}','{}','{}','{}')"
    sql = sql.format(sku, lengths, widths, heights, weights, product_id)
    try:
        print(sql)
        conf_fun.connect_mysql_re(sql, dbs='order')
        return JsonResponse({"code": 200, "msg": "新增成功"})
    except:
        return JsonResponse({"code": 400, "msg": "新增失败,请联系IT处理!"})


# 已上传未发货数量
def upload_no_deliver_num(request):
    sql = "select count(id) from manually_create_order_yc where is_bad='1'"
    res = conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "data": res[0][0]})


# 加拿大发货 导出
def ca_export_data(request):
    id = request.GET.get('id')

    sql = "select * from manually_create_order_ups where id>={}"
    sql = sql.format(id)
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    df = pd.DataFrame(res)
    filename = '加拿大发货数据.xlsx'
    df.to_excel('/home/by_operate/static/data/ca_deliver_data/' + filename, index=False)

    path = 'static/data/ca_deliver_data/加拿大发货数据.xlsx'
    return JsonResponse({"code": 200, "data": path})


# 海外仓sku对照表  查看
def oversea_location_sku_contrast_detail(request):
    sku = request.GET.get('sku')
    if sku is not None:
        sql = "select * from sku_comparison where yy_sku='{}' or an_sku='{}'"
        sql = sql.format(sku, sku)
    else:
        sql = "select * from sku_comparison order by an_sku desc"
    res = conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "data": res})


# 海外仓sku对照表 模板
def oversea_location_sku_contrast_template(request):
    path = '/home/by_operate/static/data/海外仓sku对照表_模板.xlsx'
    files = open(path, 'rb')
    response = FileResponse(files)
    response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote('海外仓sku对照表_模板.xlsx')
    return response


# 海外仓sku对照表 上传
def oversea_location_sku_contrast_upload(request):
    files = request.FILES.get('files')

    path = '/home/by_operate/static/data/海外仓sku对照表.xlsx'
    with open(path, "wb") as f:
        for line in files:
            f.write(line)

    df = pd.read_excel(path)
    for i in range(df.shape[0]):
        sql = "select * from sku_comparison where yy_sku='{}' and an_sku='{}'"
        sql = sql.format(df.iloc[i, 0], df.iloc[i, 1])
        res = conf_fun.connect_mysql_re(sql, dbs='order')
        if len(res) == 0:
            sql = "insert into sku_comparison(yy_sku,an_sku) values ('{}', '{}')"
            sql = sql.format(df.iloc[i, 0], df.iloc[i, 1])
            conf_fun.connect_mysql_re(sql, dbs='order')

    return JsonResponse({"code": 200, "msg": "上传成功!"})


# 加拿大发货 导出模板2
def ca_export_data1(request):
    id = request.GET.get('id')

    sql = "select id,customer_order_number,contact_name,tracking_no,sku,quantity from manually_create_order_ups " \
          "where id>={}"
    sql = sql.format(id)
    res = conf_fun.connect_mysql_re(sql, dbs='order')
    df = pd.DataFrame(res)
    for i in range(df.shape[0]):
        sql = "select yy_sku from sku_comparison where an_sku='{}'"
        sql = sql.format(df.iloc[i, 4])
        sku_res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
        if len(sku_res) > 0:
            df.iloc[i, 4] = sku_res[0]['yy_sku']

    filename = '加拿大发货数据(1).xlsx'
    df.to_excel('/home/by_operate/static/data/ca_deliver_data/' + filename, index=False)

    path = 'static/data/ca_deliver_data/加拿大发货数据(1).xlsx'
    return JsonResponse({"code": 200, "data": path})


# 顺丰修改订单号对应
def sf_update_order_id(request):
    sql = "select * from sf_reference"
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res})


# 添加备注
def sf_order_id_remark(request):
    remark = request.GET.get('remark')
    sf_order_id = request.GET.get('sf_order_id')
    sql = "update sf_reference set remark='{}' where sf_order_id='{}'"
    sql = sql.format(remark, sf_order_id)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": '添加成功!'})


# 错误订单添加备注
def err_order_remark(request):
    remark = request.GET.get('remark')
    order_id = request.GET.get('order_id')
    sql = "update err_order_data set remark='{}' where order_id='{}'"
    sql = sql.format(remark, order_id)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": '添加成功!'})


# 加拿大发货  更换状态
def ca_update_state(request):
    id = request.GET.get('id')
    sql = "update manually_create_order_ups set is_all='6' where id='{}'"
    sql = sql.format(id)
    print(sql)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": '更换成功!'})


# sku对照表  修改
def oversea_location_sku_update(request):
    yy_sku = request.POST.get('yy_sku')
    an_sku = request.POST.get('an_sku')
    yy_sku1 = request.POST.get('yy_sku1')
    sql = "update sku_comparison set yy_sku='{}' where yy_sku='{}' and an_sku='{}'"
    sql = sql.format(yy_sku1, yy_sku, an_sku)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": '修改成功!'})


# sku对照表  删除
def oversea_location_sku_delete(request):
    yy_sku = request.POST.get('yy_sku')
    an_sku = request.POST.get('an_sku')
    sql = "delete from sku_comparison where yy_sku='{}' and an_sku='{}'"
    sql = sql.format(yy_sku, an_sku)
    conf_fun.connect_mysql_re(sql, dbs='order')
    return JsonResponse({"code": 200, "msg": '删除成功!'})


# 加拿大发货 仓库数据模板下载
def ca_warehouse_data_template_download(request):
    path = '/home/by_operate/static/data/仓库数据_模板.xlsx'
    files = open(path, 'rb')
    response = FileResponse(files)
    response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote('仓库数据_模板.xlsx')
    return response


# 加拿大发货 仓库数据模板上传
def ca_warehouse_data_template_upload(request):
    files = request.FILES.get('files')
    path = '/home/by_operate/static/data/仓库数据.xlsx'
    with open(path, "wb") as f:
        for line in files:
            f.write(line)

    df = pd.read_excel(path)
    for i in range(df.shape[0]):
        try:
            length = round(float(df.iloc[i, 2]))
            width = round(float(df.iloc[i, 3]))
            height = round(float(df.iloc[i, 4]))
            weight = round(float(df.iloc[i, 5]), 1)
            product_id = df.iloc[i, 1] if df.iloc[i, 1] != 'nan' else ''
        except:
            return JsonResponse({"code": 400, "msg": "数据校验失败!"})
        sql = "select id from warehouse_ups where sku='{}'"
        sql = sql.format(df.iloc[i, 0])
        res = conf_fun.connect_mysql_re(sql, dbs='order')
        if len(res) == 0:
            sql = "insert into warehouse_ups(sku,lengths,widths,heights,weights,product_id) values " \
                  "('{}','{}','{}','{}','{}','{}')"
            sql = sql.format(df.iloc[i, 0], length, width, height, weight, product_id)
        else:
            sql = "update warehouse_ups set lengths='{}',widths='{}',heights='{}',weights='{}' where sku='{}'"
            sql = sql.format(length, width, height, weight, df.iloc[i, 0])
        conf_fun.connect_mysql_re(sql, dbs='order')

    return JsonResponse({"code": 200, "msg": "上传成功!"})


# 导出未发货的订单数据
def no_deliver_order_data(request):
    times = str((datetime.datetime.now() + datetime.timedelta(hours=7.4)).strftime("%Y-%m-%dT%H:%M"))
    times1 = str((datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M"))
    sql = "select reference_no,shipping_method,warehouse_code,station,country_code,order_code,tracking_no,dates,get_tracking_no_date " \
          "from manually_create_order_yc where dates<'{}' and dates>'{}' and order_code is not null and (status is NULL or status='0')"
    sql = sql.format(times, times1)
    res = conf_fun.connect_mysql_re(sql, dbs='order')
    df = pd.DataFrame(res)
    df.columns=['订单号', '渠道编码', '仓库编码', '站点', '国家', '仓库号码', '追踪编码', '发给仓库时间', '获取追踪编码时间']
    path = '/home/by_operate/static/data/超时未回传订单数据.xlsx'
    df.to_excel(path, index=False)

    return JsonResponse({"code": 200, "data": path})



# 计算发票数据
def count_invoice_data(request):
    order_id = request.GET.get('order_id')
    print(order_id)

    month_en = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug',
                '9': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    sql = "select * from manually_create_order_yc where reference_ture='{}'"
    sql = sql.format(order_id)
    print(sql)
    res = conf_fun.connect_mysql_re(sql, dbs='order')
    if len(res) == 0:
        return JsonResponse({"code": 400, "msg": "没有数据!"})
    name = res[0][7]
    address = res[0][9] if res[0][37] is None else res[0][37]
    try:
        address = address.replace(' nan', '')
    except:
        pass
    city = res[0][6]
    zip_code = res[0][10]
    Invoice_date = time.strftime("%Y-%m%d", time.localtime(time.time()))
    Invoice_number = 'INV-GB-291055313-' + Invoice_date
    sql = "select invoice_number from invoice_number where invoice_number like '{}' group by invoice_number order by invoice_number desc"
    sql = sql.format(Invoice_number+ '%')
    invoice_number = conf_fun.connect_mysql_re(sql, dbs='order')
    if len(invoice_number) == 0:
        InvoiceNumber = Invoice_number + '01'
    else:
        InvoiceNumber = Invoice_number + str(int(invoice_number[0][0][-2:]) + 1)

    create_times = time.localtime(time.time())

    dates = str(create_times.tm_mday) + '.' + month_en[str(create_times.tm_mon)] + '.' + str(create_times.tm_year)

    sql = "select product_sku,sum(quantity) from manually_create_order_yc where reference_ture='{}' group by product_sku"
    sql = sql.format(order_id)
    sku_res = conf_fun.connect_mysql_re(sql, dbs='order')

    country = request.GET.get('country')
    if country == 'GB':
        rate = '20%'
    else:
        rate = '18%'

    return JsonResponse({"code": 200, "data": sku_res, "name": name, "address": address, "city": city,
                         "zip_code": zip_code, "Invoice_number": InvoiceNumber, "dates": dates, 'rate': rate})


# 生成发票数据
def create_invoice_data(request):

    data = request.POST.get('data')
    print(data)
    data = list(eval(data))
    print(data)
    name = request.POST.get('name')
    address = request.POST.get('address')
    city = request.POST.get('city')
    zip_code = request.POST.get('zip_code')
    Invoice_number = request.POST.get('Invoice_number')
    dates = request.POST.get('dates')
    order_id = request.POST.get('order_id')
    all_price = request.POST.get('all_price')

    lens = len(data)
    sql = "select country_code from manually_create_order_yc where reference_ture='{}'"
    sql = sql.format(order_id)
    print(sql)
    country_res = conf_fun.connect_mysql_re(sql, dbs='order')
    print(country_res)
    if country_res[0][0] == "GB":
        doc = DocxTemplate("/home/by_operate/static/data/invoice_data/英国发票.docx")
    else:
        doc = DocxTemplate("/home/by_operate/static/data/invoice_data/其他四国发票.docx")
    path = '/home/by_operate/static/data/invoice_data/' + order_id + '.docx'
    path1 = '/home/by_operate/static/data/invoice_data/'
    path2 = '/home/by_operate/static/data/invoice_data/' + order_id + '.pdf'
    context = {'name': name, 'address': address, 'city': city, 'zip_code': zip_code, 'order_id': order_id,
               'Invoice_numbe': Invoice_number, 'dates': dates, 'qty1': '', 'Description1': '', 'VAT1': '',
               'rate1': '', 'vat1': '', 'all_vat1': '', 'qty2': '', 'Description2': '', 'VAT2': '',
               'rate2': '', 'vat2': '', 'all_vat2': '', 'qty3': '', 'Description3': '', 'VAT3': '',
               'rate3': '', 'vat3': '', 'all_vat3': '', 'qty4': '', 'Description4': '', 'VAT4': '',
               'rate4': '', 'vat4': '', 'all_vat4': '', 'qty5': '', 'Description5': '', 'VAT5': '',
               'rate5': '', 'vat5': '', 'all_vat5': '', 'all_price': all_price}

    context['qty1'] = data[0][0]
    context['Description1'] = data[0][2]
    context['VAT1'] = data[0][3]
    context['rate1'] = data[0][4]
    context['vat1'] = data[0][5]
    context['all_vat1'] = data[0][6]
    if lens == 1:
        doc.render(context)  # 执行替换
        doc.save(path)

        os.system('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        print('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        return JsonResponse({"code": 200, "data": path2})

    context['qty2'] = data[1][0]
    context['Description2'] = data[1][2]
    context['VAT2'] = data[1][3]
    context['rate2'] = data[1][4]
    context['vat2'] = data[1][5]
    context['all_vat2'] = data[1][6]

    if lens == 2:
        doc.render(context)  # 执行替换
        doc.save(path)

        os.system('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        print('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        return JsonResponse({"code": 200, "data": path2})

    context['qty3'] = data[2][0]
    context['Description3'] = data[2][2]
    context['VAT3'] = data[2][3]
    context['rate3'] = data[2][4]
    context['vat3'] = data[2][5]
    context['all_vat3'] = data[2][6]

    if lens == 3:
        doc.render(context)  # 执行替换
        doc.save(path)

        os.system('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        print('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        return JsonResponse({"code": 200, "data": path2})

    context['qty4'] = data[3][0]
    context['Description4'] = data[3][2]
    context['VAT4'] = data[3][3]
    context['rate4'] = data[3][4]
    context['vat4'] = data[3][5]
    context['all_vat4'] = data[3][6]

    if lens == 4:
        doc.render(context)  # 执行替换
        doc.save(path)

        os.system('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        print('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        return JsonResponse({"code": 200, "data": path2})

    context['qty5'] = data[4][0]
    context['Description5'] = data[4][2]
    context['VAT5'] = data[4][3]
    context['rate5'] = data[4][4]
    context['vat5'] = data[4][5]
    context['all_vat5'] = data[4][6]

    if lens == 5:
        doc.render(context)  # 执行替换
        doc.save(path)

        os.system('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        print('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        return JsonResponse({"code": 200, "data": path2})

    if lens > 5:
        doc.render(context)  # 执行替换
        path = '/home/by_operate/static/data/invoice_data/' + order_id + '错误.docx'
        doc.save(path)
    
        os.system('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        print('soffice --headless -convert-to pdf ' + path +' --outdir ' + path1)
        return JsonResponse({"code": 200, "data": path2})


# 查询美国错误订单
def get_US_error_order(request):
    sql = "select * from manually_create_order where is_all in ('3', '4')"
    res = conf_fun.connect_mysql_re(sql, dbs='order', type='dict')
    return JsonResponse({"code": 200, "data": res})


# 获取需要上传订单文件的国家
def get_upload_file_country(request):
    site = []
    site_en = []
    sql = "select site,country from store_information where state='在售'"
    res = conf_fun.connect_mysql_operation(sql)
    for i in res:
        site.append(i[0] + i[1])
        site_ = ''
        if i[0] == '胤佑':
            site_ += 'yy'
        elif i[0] == '爱瑙':
            site_ += 'an'
        elif i[0] == '中睿':
            site_ += 'zr'
        elif i[0] == '京汇':
            site_ += 'jh'
        elif i[0] == '利百锐':
            site_ += 'lbr'
        elif i[0] == '笔漾教育':
            site_ += 'byjy'
        else:
            pass
        if i[1] == '美国':
            site_ += '_US'
        elif i[1] == '加拿大':
            site_ += '_CA'
        elif i[1] == '墨西哥':
            site_ += '_MX'
        elif i[1] == '日本':
            site_ += '_JP'
        elif i[1] == '澳洲':
            site_ += '_AU'
        elif i[1] == '英国':
            site_ += '_UK'
        elif i[1] == '法国':
            site_ += '_FR'
        elif i[1] == '德国':
            site_ += '_DE'
        elif i[1] == '意大利':
            site_ += '_IT'
        else:
            site_ += '_ES'
        site_en.append(site_)
    return JsonResponse({'code': 200, "site": site, "site_en": site_en})
            