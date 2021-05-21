import datetime
import pymysql
import requests
import json
import calendar
import urllib
import math
from urllib.parse import unquote
from django.http import JsonResponse



# 连接数据库
def connect_mysql(sql_text, dbs='reports', type='tuple'):
    conn = pymysql.Connect(host='106.53.250.215', port=3306, user='beyoungsql', passwd='Bymy2021.', db=dbs)
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


def connect_mysql1(sql_text, dbs='operation', type='tuple'):
    conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='Bymy2021_', db=dbs)

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


def connect_mysql2(sql_text, dbs='product_supplier', type='tuple'):
    conn = pymysql.Connect(host='42.194.146.85', port=3306, user='beyoungsql', passwd='Bymy2021.', db=dbs)

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
    else:
        if store == "yy" or store == "YY":
            store = "胤佑"
        elif store == "an" or store == "AN":
            store = "爱瑙"
        elif store == "zr" or store == "ZR":
            store = "中睿"
        elif store == "jh" or store == "JH":
            store = "京汇"
        elif store == "lbr" or store == "LBR":
            store = "利百锐"

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
    return store,country


# ----------------->结算报告
def get_store_country(request):
    now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m")
    # 从老系统中查询所有报告的国家站点
    sql = "select company,countries from sku_report where times like'%" + now + "%';"
    try:
        data = connect_mysql(sql)
        _list = list(set([i for i in data]))
        # 数据替换
        _list1 = []
        for item in _list:
            _dict = {"company":"","countries":""}
            if item[0] == "ZR":
                _dict["company"] = "中睿"
            elif item[0] == "YY":
                _dict["company"] = "胤佑"
            elif item[0] == "JH":
                _dict["company"] = "京汇"
            elif item[0] == "AN":
                _dict["company"] = "爱瑙"

            if item[1] == "JP":
                _dict["countries"] = "日本"
            elif item[1] == "AU":
                _dict["countries"] = "澳大利亚"
            elif item[1] == "EU":
                _dict["countries"] = "欧洲"
            elif item[1] == "CA":
                _dict["countries"] = "加拿大"
            elif item[1] == "MX":
                _dict["countries"] = "墨西哥"
            elif item[1] == "US":
                _dict["countries"] = "美国"
            elif item[1] == "UK":
                _dict["countries"] = "英国"
            elif item[1] == "ES":
                _dict["countries"] = "西班牙"
            elif item[1] == "DE":
                _dict["countries"] = "德国"
            elif item[1] == "IT":
                _dict["countries"] = "意大利"
            _list1.append(_dict)
        store_list = []
        for i in _list1:
            if len(store_list) == 0:
                _dict = {
                    "store":i["company"],
                    "countries":[i["countries"]]
                }
                store_list.append(_dict)
            else:
                for index,j in enumerate(store_list):
                    if i["company"] == j["store"]:
                        j["countries"].append(i["countries"])
                        break
                    elif i["company"] != j["store"] and index == len(store_list)-1:
                        _dict = {
                            "store": i["company"],
                            "countries": [i["countries"]]
                        }
                        store_list.append(_dict)
                        break

        print(store_list)
        return JsonResponse({"code":200,"msg":"success","data":store_list})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 所有订单报告
def get_all_order(request):
    channel = request.GET.get("channel",None)
    store = request.GET.get("store", None)
    country = request.GET.get("country", None)
    date = request.GET.get("date", None)
    type = request.GET.get("type",None)
    print(channel,store,country,date,type)
    if channel == "Amazon":
        area = store+country
        # 从老系统请求数据
        try:
            url = 'http://www.beyoung.group/get_report?area=' + area + '&date=' + date + '&type=' + type
            re = requests.get(url=url)
            print(re)
            data_res = json.loads(re.text)
            res = data_res
            print(res)
            for i in res["data"]:
                i["channel"] = "Amazon"
            return JsonResponse(res)
        except Exception as e:
            return JsonResponse({"code":500,"msg":"error:"+str(e)})
    else:
        return JsonResponse({"code":200,"msg":"渠道不在列表内"})


# 获取每日订单左侧导航栏数据
def get_report_beside(request):
    type = request.GET.get("type",None)
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    print("area===", area)
    if type == "history":
        url = "server/databases/get_sku_order_summary/"
    else:
        url = "server/databases/get_everyday_sku_order_summary/"
    data = []
    if area == 'all':
        # 查询全部数据
        sql = "select * from store_information;"
        res = connect_mysql1(sql,type='dict')
        for i in res:
            store, country = store_country_code(i["site"], i["country"], 'en', type='low')
            if len(data) == 0:
                _dict = {
                    "title":"",
                    "children":[]
                }
                if i["country"] in ["欧洲","法国","德国","意大利","西班牙"]:
                    _dict["title"] = i["site"] + "欧洲"

                    if i["country"] == "欧洲":
                        _dict["children"].append({"name":i["site"] + "欧洲SKU订单汇总",
                                                  "url":url,
                                                  "area":store+"_es"})
                        _dict["children"].append({"name": i["site"] + "欧洲SPU订单汇总",
                                                  "url": url,
                                                  "area":store+"_es"})
                        _dict["children"].append({"name": i["site"] + "欧洲每日运营概要",
                                                  "url": "server/databases/get_eu_gy_data/",
                                                  "area":store+"_es"})
                    else:
                        _dict["children"].append({"name": i["site"] + "欧洲" + i["country"] + "订单",
                                                  "url": "server/databases/get_eu_order_data/",
                                                  "area":store+"_es"})
                else:
                    _dict["title"] = i["site"] + i["country"]
                    _dict["children"].append({"name": i["site"] + i["country"] + "SKU订单汇总",
                                              "url": url,
                                              "area":store+"_" + country})
                    _dict["children"].append({"name": i["site"] + i["country"] + "SPU订单汇总",
                                              "url": url,
                                              "area":store+"_" + country})
                    _dict["children"].append({"name": i["site"] + i["country"] + "每日运营概要",
                                              "url": "server/databases/get_gy_data/",
                                              "area":store+"_" + country})
                data.append(_dict)
            else:
                for index,j in enumerate(data):
                    if i["country"] in ["欧洲","法国","德国","意大利","西班牙"]:
                        _str = i["site"] + "欧洲"
                    else:
                        _str = i["site"] + i["country"]

                    if _str == j["title"]:
                        if i["country"] in ["欧洲","法国","德国","意大利","西班牙"]:
                            if i["country"] == "欧洲":
                                j["children"].insert(0,{"name": i["site"] + "欧洲SKU订单汇总",
                                                        "url": url,
                                                        "area":store+"_es"})
                                j["children"].insert(0,{"name": i["site"] + "欧洲SPU订单汇总",
                                                        "url": url,
                                                        "area":store+"_es"})
                                j["children"].insert(0,{"name": i["site"] + "欧洲每日运营概要",
                                                        "url": "server/databases/get_eu_gy_data/",
                                                        "area":store+"_es"})
                            else:
                                j["children"].append({"name": i["site"] + "欧洲" + i["country"] + "订单",
                                                      "url": "server/databases/get_eu_order_data/",
                                                      "area":store+"_es"})
                        else:
                            pass
                        break
                    elif _str != j["title"] and index == len(data)-1:
                        _dict = {
                            "title": "",
                            "children": []
                        }
                        if i["country"] in ["欧洲", "法国", "德国", "意大利", "西班牙"]:
                            _dict["title"] = i["site"] + "欧洲"
                            if i["country"] == "欧洲":
                                _dict["children"].append({"name": i["site"] + "欧洲SKU订单汇总",
                                                          "url": url,
                                                          "area":store+"_es"})
                                _dict["children"].append({"name": i["site"] + "欧洲SPU订单汇总",
                                                          "url": url,
                                                          "area":store+"_es"})
                                _dict["children"].append({"name": i["site"] + "欧洲每日运营概要",
                                                          "url": "server/databases/get_eu_gy_data/",
                                                          "area":store+"_es"})
                            else:
                                _dict["children"].append({"name": i["site"] + "欧洲" + i["country"] + "订单",
                                                          "url": "server/databases/get_eu_order_data/",
                                                          "area":store+"_es"})
                        else:
                            _dict["title"] = i["site"] + i["country"]
                            _dict["children"].append({"name": i["site"] + i["country"] + "SKU订单汇总",
                                                      "url": url,
                                                      "area":store+"_"+country})
                            _dict["children"].append({"name": i["site"] + i["country"] + "SPU订单汇总",
                                                      "url": url,
                                                      "area":store+"_"+country})
                            _dict["children"].append({"name": i["site"] + i["country"] + "每日运营概要",
                                                      "url": "server/databases/get_gy_data/",
                                                      "area":store+"_"+country})
                        data.append(_dict)
                        break
    else:
        _list = area.split(',')
        for i in _list:
            store, country = store_country_code(i.split('_')[0], i.split('_')[1], 'en', type='low')
            if len(data) == 0:

                _dict = {
                    "title": "",
                    "children": []
                }
                if i.split('_')[1] in ["法国", "德国", "意大利", "西班牙"]:
                    _dict["title"] = i.split('_')[0] + "欧洲"
                    _dict["children"].append({"name": i.split('_')[0] + "欧洲" + i.split('_')[1] + "订单",
                                              "url": "server/databases/get_eu_order_data/",
                                              "area":store+"_es"})
                else:
                    _dict["title"] = i.split('_')[0] + i.split('_')[1]
                    _dict["children"].append({"name": i.split('_')[0] + i.split('_')[1] + "SKU订单汇总",
                                              "url": url})
                    _dict["children"].append({"name": i.split('_')[0] + i.split('_')[1] + "SPU订单汇总",
                                              "url": url,
                                              "area":store+"_" + country})
                    _dict["children"].append({"name": i.split('_')[0] + i.split('_')[1] + "每日运营概要",
                                              "url": "server/databases/get_gy_data/",
                                              "area":store+"_" + country})
                data.append(_dict)
            else:
                for index, j in enumerate(data):
                    if i.split('_')[1] in ["法国", "德国", "意大利", "西班牙"]:
                        _str = i.split('_')[0] + "欧洲"
                    else:
                        _str = i.split('_')[0] + i.split('_')[1]

                    if _str == j["title"]:
                        if i.split('_')[1] in ["法国", "德国", "意大利", "西班牙"]:
                            j["children"].append({"name": i.split('_')[0] + "欧洲" + i.split('_')[1] + "订单",
                                                  "url": "server/databases/get_eu_order_data/",
                                                  "area":store+"_es"})
                        else:
                            pass
                        break
                    elif _str == j["title"] and index == len(data) - 1:
                        _dict = {
                            "title": "",
                            "children": []
                        }
                        if i.split('_')[1] in ["法国", "德国", "意大利", "西班牙"]:
                            _dict["title"] = i.split('_')[0] + "欧洲"
                            _dict["children"].append({"name": i["site"] + "欧洲" + i["country"] + "订单",
                                                      "url": "server/databases/get_eu_order_data/",
                                                      "area":store+"_es"})
                        else:
                            _dict["title"] = i["site"] + i["country"]
                            _dict["children"].append({"name": i["site"] + i["country"] + "sku订单汇总",
                                                      "url": url,
                                                      "area":store+"_" + country})
                            _dict["children"].append({"name": i["site"] + i["country"] + "spu订单汇总",
                                                      "url": url,
                                                      "area":store+"_" + country})
                            _dict["children"].append({"name": i["site"] + i["country"] + "每日运营概要",
                                                      "url": "server/databases/get_gy_data/",
                                                      "area":store+"_" + country})
                        data.append(_dict)
                        break

        for item in data:
            store = item["title"][0:2]
            store1,country1 = store_country_code(store,'','en',type='low')
            if "欧洲" in item["title"]:
                item["children"].insert(0,{"name": item["title"] + "SKU订单汇总",
                                           "url": url,
                                           "area":store1+"_es"})
                item["children"].insert(0,{"name": item["title"] + "SPU订单汇总",
                                           "url": url,
                                           "area":store1+"_es"})
                item["children"].insert(0,{"name": item["title"] + "每日运营概要",
                                           "url": "server/databases/get_eu_gy_data/",
                                           "area":store1+"_es"})

    if type == "everyday":
        data.append({"title":"广告报告上传","children":[{"name":"广告报告上传","url":"/AdvertisingReportUpload","area":""}]})
    return JsonResponse({"code":200,"msg":"success","data":data})


# 历史运营日报
def get_history_report(request):
    date = request.GET.get("date",None)
    print("date==",date)
    type = "history"
    try:
        url = 'http://www.beyoung.group/history_report?zr_all?中睿运营数据?'+date + '?' + type
        re = requests.get(url=url)
        print(re)
        data_res = json.loads(re.text)
        res = data_res
        print(res)
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 每日运营日报 http://106.53.250.215:8003/ http://www.beyoung.group/
def get_everyday_report(request):
    date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m")
    type = "everyday"
    try:
        url = 'http://www.beyoung.group/history_report?zr_all?中睿运营数据?'+date + '?' + type
        re = requests.get(url=url)
        print(re)
        data_res = json.loads(re.text)
        res = data_res
        print(res)
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# sku订单汇总
def get_sku_order_summary(request):
    area = request.GET.get("area",None)
    name = request.GET.get("name",None)
    page = request.GET.get("page", 1)
    dates = request.GET.get("dates",None)
    print(area,name)
    if dates is None:
        dates = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m")
    type = "all"
    try:
        #106.53.250.215:8003
        url = 'http://www.beyoung.group/get_sku_order_summary?' + area + '?' + name + '?' + type + '?' + dates
        re = requests.get(url=url)
        data_res = json.loads(re.text)
        res = data_res
        # 分页显示
        total_num = len(res["data_list"][0]["value"])
        start = int(page) * 50 - 50
        end = int(page) * 50
        if 'SKU' in name:
            for i in res["data_list"]:
                i["value"] = i["value"][start:end]
            res["spu"]["value"] = res["spu"]["value"][start:end]
            res["sku"]["value"] = res["sku"]["value"][start:end]
            res["fba"]["value"] = res["fba"]["value"][start:end]
            res["link"] = res["link"][start:end]
            res["fbm"]["value"] = res["fbm"]["value"][start:end]
            res["zj"]["value"] = res["zj"]["value"][start:end]
            res["total_num"] = total_num
        else:
            for i in res["data_list"]:
                i["value"] = i["value"][start:end]
            res["spu"]["value"] = res["spu"]["value"][start:end]
            res["fba"]["value"] = res["fba"]["value"][start:end]
            res["link"] = res["link"][start:end]
            res["fbm"]["value"] = res["fbm"]["value"][start:end]
            res["zj"]["value"] = res["zj"]["value"][start:end]
            res["total_num"] = total_num
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 每日sku/spu订单汇总
def get_everyday_sku_order_summary(request):
    area = request.GET.get("area",None)
    name = request.GET.get("name",None)
    page = request.GET.get("page",1)
    print(area,name,page)
    type = "everyday"
    try:
        url = 'http://www.beyoung.group/get_sku_order_summary?' + area + '?' + name + '?' + type
        re = requests.get(url=url)
        # print(re)
        data_res = json.loads(re.text)
        res = data_res
        # 分页显示
        total_num = len(res["data_list"][0]["value"])
        print("total_num===",total_num)
        start = int(page) * 50 - 50
        end = int(page) * 50
        print(start)
        print(end)
        if 'SKU' in name:
            for i in res["data_list"]:
                i["value"] = i["value"][start:end]
            res["spu"]["value"] = res["spu"]["value"][start:end]
            res["sku"]["value"] = res["sku"]["value"][start:end]
            res["fba"]["value"] = res["fba"]["value"][start:end]
            res["link"]= res["link"][start:end]
            res["fbm"]["value"] = res["fbm"]["value"][start:end]
            res["zj"]["value"] = res["zj"]["value"][start:end]
            res["total_num"] = total_num
        else:
            for i in res["data_list"]:
                i["value"] = i["value"][start:end]
            res["spu"]["value"] = res["spu"]["value"][start:end]
            res["fba"]["value"] = res["fba"]["value"][start:end]
            res["link"] = res["link"][start:end]
            res["fbm"]["value"] = res["fbm"]["value"][start:end]
            res["zj"]["value"] = res["zj"]["value"][start:end]
            res["total_num"] = total_num
        print("res==",len(res["data_list"][0]["value"]))
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 每日运营概要
def get_gy_data(request):
    area = request.GET.get("area", None)
    name = request.GET.get("name", None)
    page = request.GET.get("page", "1")
    print(area, name, page)
    try:
        url = 'http://www.beyoung.group/get_gy_data/?' + area + '?' + name + '?' + page
        re = requests.get(url=url)
        print(re)
        data_res = json.loads(re.text)
        res = data_res
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 欧洲每日运营概要
def get_eu_gy_data(request):
    area = request.GET.get("area", None)
    name = request.GET.get("name", None)
    page = request.GET.get("page", "1")
    print(area, name, page)
    try:
        url = 'http://www.beyoung.group/get_eu_gy_data/?' + area + '?' + name + '?' + page
        re = requests.get(url=url)
        print(re)
        data_res = json.loads(re.text)
        res = data_res
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 欧洲四国每日订单
def get_eu_order_data(request):
    area = request.GET.get("area", None)
    name = request.GET.get("name", None)
    page = request.GET.get("page", '1')
    print(area, name, page)
    try:
        url = 'http://www.beyoung.group/get_eu_order_data/?' + area + '?' + name + '?' + page
        re = requests.get(url=url)
        print(re)
        data_res = json.loads(re.text)
        res = data_res
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 库存
# 查询所有筛选条件
def get_search(request):
    sql = "select * from commodity_information;"
    sql1 = "select * from product_message;"
    try:
        data = connect_mysql1(sql,type='dict')
        data1 = connect_mysql1(sql1,type='dict')
        product_name_list = list(set([j["product_name"] for i in data for j in data1 if i["product_code"]==j["product_code"]]))
        sku_list = list(set([i["sku"] for i in data]))
        channel_list = list(set([i["platform"] for i in data]))
        return JsonResponse({"code": 200, "msg": "success","product_name_list":product_name_list,"sku_list":sku_list,"channel_list":channel_list})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 查询条件下的数据
def get_search_data(request):
    name = request.GET.get("name",None)
    value = request.GET.get("value", None)

    try:
        sql = ""
        data = []
        if name == "platform":
            sql = "select site from commodity_information where platform='%s';" % (value)
            res = connect_mysql1(sql, type='dict')
            data = list(set([i["site"] for i in res]))
        elif name == "site":
            channel = request.GET.get("channel", None)
            sql = "select country from commodity_information where platform='%s' and site='%s';" % (channel, value)
            res = connect_mysql1(sql, type='dict')
            data = list(set([i["country"] for i in res]))
        elif name == "country":
            channel = request.GET.get("channel", None)
            site = request.GET.get("site", None)
            sql = "select sku from commodity_information where platform='%s' and site='%s' and country='%s';" % (
            channel, site, value)

            res = connect_mysql1(sql, type='dict')
            data = list(set([i["sku"] for i in res]))

        return JsonResponse({"code": 200, "msg": "success","data":data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 获取sku10日均单量
def get_order_num(store,country,sku):
    if store == "胤佑":
        store = 'YY'
    elif store == "爱瑙":
        store = 'AN'
    elif store == "京汇":
        store = 'JH'
    elif store == "中睿":
        store = 'ZR'

    if country == "美国":
        country = 'US'
    elif country == "加拿大":
        country = 'CA'
    elif country == "墨西哥":
        country = 'MX'
    elif country == "英国":
        country = 'Uk'
    elif country == "法国":
        country = 'FR'
    elif country == "德国":
        country = 'DE'
    elif country == "意大利":
        country = 'IT'
    elif country == "西班牙":
        country = 'ES'
    elif country == "日本":
        country = 'JP'

    if country in ["UK","FR","DE","IT","ES"]:
        sql = "select * from order_sublist where company='%s' and countries='%s' and sku='%s' order by id desc LIMIT 10;"%(store,country,sku)
    else:
        sql = "select * from sku_report where company='%s' and countries='%s' and sku='%s' order by id desc LIMIT 10;"%(store,country,sku)
    data = connect_mysql(sql,type='dict')
    num = 0
    avg = 0
    if len(data) > 0:
        for i in data:
            num += int(i["nums"])
    if num > 0:
        avg = num/10

    return avg


# 查询数据
def get_stock_data(request):
    _list = request.GET.get("data",None)
    page = request.GET.get("page",1)
    start = int(page) * 50 - 50
    end = int(page) * 50

    sql = ""
    if _list is not None:
        _data = json.loads(_list)
        if len(_data) > 0:
            sql = "SELECT c.product_code,c.spu,c.sku,c.platform,c.country,c.site,c.commodity_price,p.product_name " \
                  "FROM commodity_information as c join product_message as p ON c.product_code=p.product_code where "
            sql1 = "select count(*) from where "
            for i in _data:
                if i["key"] == "product_name":
                    _list1 = i["value"].split(',')
                    _str = "','".join(_list1)
                    sql += "p.product_name in ('" + _str + "') and "
                    sql1 += "p.product_name in ('" + _str + "') and "
                else:
                    if i["key"] == "sku":
                        _list1 = i["value"].split(',')
                        _str = "','".join(_list1)
                        sql += "c.sku in ('" + _str + "') and "
                        sql1 += "c.sku in ('" + _str + "') and "
                    else:
                        sql += "c."+i["key"]+ "='" + i["value"] + "' and "
                        sql1 += "c." + i["key"] + "='" + i["value"] + "' and "
            sql = sql[:-5] + " order by c.id limit " + start + "," + end + ";"
            sql1 = sql1[:-5]
        else:
            sql = "SELECT c.product_code,c.spu,c.sku,c.platform,c.country,c.site,c.commodity_price,p.product_name " \
                  "FROM commodity_information as c join product_message as p ON c.product_code=p.product_code order by c.id limit %s,%s;"%(start, end)

            sql1 = "SELECT count(*) FROM commodity_information as c join product_message as p ON " \
                   "c.product_code=p.product_code;"
    else:
        sql = "SELECT c.product_code,c.spu,c.sku,c.platform,c.country,c.site,c.commodity_price,p.product_name " \
              "FROM commodity_information as c join product_message as p ON c.product_code=p.product_code order by c.id limit %s,%s;"%(start, end)

        sql1 = "SELECT count(*) FROM commodity_information as c join product_message as p ON " \
               "c.product_code=p.product_code;"
    print("sql1---",sql1)
    # 查询商品信息
    data = connect_mysql1(sql,type='dict')
    print("data===",len(data))

    # 获取总条数
    res = connect_mysql1(sql1)
    total_num = res[0][0]
    # 查询详细信息
    for i in data:
        sku = i["sku"]
        # 查询fba库存
        sql1 = "select * from sku_report where sku='%s' order by id desc LIMIT 1;"%(sku)
        res = connect_mysql(sql1,type='dict')
        if len(res) > 0:
            i["fba"] = int(res[0]["fba"])
            i["on_warehouse_num"] = int(res[0]["fba"])
            i["all_nums"] = int(res[0]["fba"])
        else:
            i["fba"] = 0
            i["on_warehouse_num"] = 0
            i["all_nums"] = 0

        # 查询fbm库存
        sql2 = "select * from fbm_data where sku='%s' order by id desc LIMIT 1;"%(sku)
        data2 = connect_mysql(sql2, type='dict')
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
        # 查找所有的在途货柜以及货柜中的sku
        sql3 = "SELECT ar.container,GROUP_CONCAT(ci.sku) as sku FROM arrival_receive as ar JOIN cargo_information as ci" \
               " ON ar.container=ci.container_num where ar.warehousing_date is NULL OR ar.warehousing_date ='' GROUP BY ar.id;"
        data3 = connect_mysql2(sql3,type='dict')


        # 获取10日均单量
        avg = get_order_num(i["site"],i["country"],i["sku"])
        i["avg"] = avg

        # 期望营业额
        expect_turnover = avg * float(i["commodity_price"]) if i["commodity_price"] is not None else 0
        i["expect_turnover"] = expect_turnover

        # 预计售空天数
        if i["on_warehouse_num"] > 0 and avg > 0:
            estimate_sell_out_days = math.ceil(i["on_warehouse_num"] / avg)
        else:
            estimate_sell_out_days = 0
        i["estimate_sell_out_days"] = estimate_sell_out_days
        # 预计售空日期
        estimate_sell_out_date = datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=estimate_sell_out_days),"%Y-%m-%d")
        i["estimate_sell_out_date"] = estimate_sell_out_date
    return JsonResponse({"code":200,"msg":"success","data":data,"total_num":total_num})

















