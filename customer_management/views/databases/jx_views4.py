from django.http import JsonResponse
from django.http import FileResponse
import pymysql
import os
import requests
from PIL import Image
from django.utils.http import urlquote


# 连接主系统数据库
def connect_mysql1(sql_text, dbs='reports', type='tuple'):
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


# 连接总数据库
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


# --------------------------------------------------割割割割割割割割

# 功能函数-组织数据(条码表的查询结果)（产品条码）
def organization_barcode_data(select_res):
    # status_dict = {"0": "上传待审核", "1": "审核通过", "2": "删除待审核"}
    # # id, 站点，国家，sku，品名，路径、fnsku、状态
    # res_data = []
    # for item in select_res:
    #     small_list = list()
    #     # id
    #     small_list.append(item[0])
    #     # 平台，站点，国家，sku，品名，路径，fnsku
    #     small_list.extend(item[2:9])
    #     # 状态
    #     small_list.append(status_dict[item[9]])
    #     # 产品类型
    #     small_list.append(item[1])
    #
    #     res_data.append(small_list)
    # return res_data

    data = []
    for item in select_res:
        print("item: ", item)
        small_list = list()
        try:
            # 渠道、站点、国家、sku、品名、文件名、fnsku
            small_list.append(item['platform'])
            small_list.append(item['site'])
            small_list.append(item['country'])
            small_list.append(item['sku'])
            small_list.append(item['commodity_name'])
            small_list.append(item['commodity_name'] + "_" + item['fnsku'] + ".btw")
            small_list.append(item['fnsku'])
            data.append(small_list)
        except:
            continue
    return data


# 功能函数-查询产品表（commodity_information）数据（产品条码）
def select_product_barcode(platform=None, site=None, country=None, sku=None):
    # select_sql = "select * from product_barcode where status='1'"
    # if barcode_type:
    #     select_sql += " and barcode_type='" + barcode_type + "'"
    # if site:
    #     select_sql += " and site='" + site + "'"
    # if country:
    #     select_sql += " and country='" + country + "'"
    # if sku:
    #     select_sql += " and sku='" + sku + "'"
    # select_sql += ";"
    # select_res = connect_mysql(sql_text=select_sql)
    # return select_res

    select_sql = "select * from commodity_information where id!=''"
    if platform:
        select_sql += " and platform='" + platform + "'"
    if site:
        select_sql += " and site='" + site + "'"
    if country:
        select_sql += " and country='" + country + "'"
    if sku:
        select_sql += " and sku='" + sku + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = connect_mysql(sql_text=select_sql, type='dict')
    return select_res


# 数据库-产品条码-查询
def select_barcode(request):
    print("-------------数据库-产品条码-查询: ", request.GET)
    platform = request.GET.get("platform", "")
    site = request.GET.get("site", "")
    country = request.GET.get("country", "")
    sku = request.GET.get("sku", "")
    page = request.GET.get("page", "")
    res_data = organization_barcode_data(select_product_barcode
                                         (platform=platform, site=site, country=country, sku=sku))

    sku_list = []
    for res_data_item in res_data:
        if res_data_item[3] not in sku_list:
            sku_list.append(res_data_item[3])

    # 总行数
    all_number = len(res_data)
    # 分页
    if page:
        page_start = int(page) * 50 - 50
        page_end = int(page) * 50
        res_data = res_data[page_start:page_end]
    res = {"code": 200, "data": res_data, "all_number": all_number, "sku_list": sku_list}
    print("res: ", res)
    return JsonResponse(res)


# 数据库-产品条码-获取条码框数据(加上了id，点击侧边栏查询时)(旧版本，已弃用)
def get_barcode(request):
    print("--------数据库-产品条码-获取条码框数据-----")
    res_data = []
    select_sql = "select file_path,id from product_barcode where status='1';"
    select_res = connect_mysql(sql_text=select_sql)
    for item in select_res:
        small_list = [item[0].split("/")[-1].split(".")[0], item[1]]
        res_data.append(small_list)
    res = {"code": 200, "data": res_data}
    print("res: ", res)
    return JsonResponse(res)


# 数据库-产品条码-确认上传（多文件上传）
def upload_barcode(request):
    print("-------------数据库-产品条码-确认上传: ", request.FILES)
    files = request.FILES.getlist("files", "")
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/static/barcode/"
    # --------------- 多个文件上传 ---------
    not_exist_list = list()
    for single_file in files:
        file_name = single_file.name
        file_path = save_path + file_name
        save_file_path = "/static/barcode/" + file_name
        fnsku = file_name.split("_")[1].split(".")[0]
        # 向商品信息查询数据
        select_sql = "select * from commodity_information where fnsku='%s';" % fnsku
        print("select_sql: ", select_sql)
        select_res = connect_mysql(sql_text=select_sql, type='dict')
        print("select_res: ", select_res)
        if not select_res:
            not_exist_list.append(file_name)
            continue
        # 保存文件
        with open(file_path, 'wb') as fw:
            for file_data in single_file:
                fw.write(file_data)

        delete_product_barcode_sql = "delete from product_barcode where fnsku='%s';" % fnsku
        print("delete_product_barcode_sql: ", delete_product_barcode_sql)
        connect_mysql(sql_text=delete_product_barcode_sql)

        insert_sql = "insert into product_barcode(product_type,platform,site,country," \
                     "sku,product_name,file_path,fnsku,status) " \
                     "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                     % (select_res[0]['category'], select_res[0]['platform'], select_res[0]['site'],
                        select_res[0]['country'], select_res[0]['sku'], select_res[0]['commodity_name'],
                        save_file_path, select_res[0]['fnsku'], "0")
        print("insert_sql: ", insert_sql)
        connect_mysql(sql_text=insert_sql)
    if not_exist_list:
        msg = "上传成功！\n" + str(not_exist_list) + "没有对应的数据"
        res = {"code": 4041, "msg": msg}
        return JsonResponse(res)
    res = {"code": 200}
    return JsonResponse(res)


# 数据库-产品条码-删除
def delete_barcode(request):
    print("-------------数据库-产品条码-删除: ", request.GET)
    # barcode_id = request.GET.getlist("barcode_id[]", "")
    # for item in barcode_id:
    #     update_sql = "update product_barcode set status='2' where id='%s';" % item
    #     print("update_sql: ", update_sql)
    #     connect_mysql(sql_text=update_sql)
    # res = {"code": 200}
    # return JsonResponse(res)

    sku_list = request.GET.getlist("barcode_id[]", "")
    print("sku_list: ", sku_list)
    for single_sku in sku_list:
        select_sql = "select * from commodity_information where sku='%s';" % single_sku
        print("select_sql: ", select_sql)
        select_res = connect_mysql(sql_text=select_sql, type='dict')
        # 将相关数据写入数据库，文件路径写入条码文件的文件名，待审核
        insert_sql = "insert into product_barcode(product_type,platform,site," \
                     "country,sku,product_name,file_path,fnsku,status) " \
                     "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                     % (select_res[0]["category"], select_res[0]["platform"], select_res[0]["site"],
                        select_res[0]["country"], select_res[0]["sku"], select_res[0]["commodity_name"],
                        select_res[0]["commodity_name"] + "_" + select_res[0]["fnsku"], select_res[0]["fnsku"], "2")
        print("insert_sql: ", insert_sql)
        connect_mysql(sql_text=insert_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 数据库-产品条码-获取待审核数据
def get_check_barcode(request):
    print("")
    print("数据库-产品条码-获取待审核数据: ", request.GET)
    print("")
    select_sql = "select * from product_barcode where status!='1';"
    select_res = connect_mysql(sql_text=select_sql)
    print("select_res: ", select_res)
    data_list = [list(x) for x in select_res]
    for item in data_list:
        item[-1] = "新增待审核" if item[-1] == "0" else "删除待审核"
    res = {"code": 200, "data": data_list}
    return JsonResponse(res)


# 数据库-产品条码-审核
def check_barcode(request):
    print("-------------数据库-产品条码-审核: ", request.GET)
    barcode_id = request.GET.getlist("barcode_id[]", "")
    check_res = request.GET.get("check_res", "")
    for id_item in barcode_id:
        select_status_sql = "select * from product_barcode where id='%s';" % id_item
        print("select_status_sql: ", select_status_sql)
        select_status_res = connect_mysql(sql_text=select_status_sql, type='dict')
        print("select_status_res: ", select_status_res)
        if check_res == "审核通过":
            print("审核通过")
            if select_status_res[0]["status"] == "0":
                print("上传文件、删除运营服务器待审核文件、删除数据")
                # 上传文件、删除运营服务器待审核文件、删除数据
                upload_request_path = "https://www.beyoung.group/tm_data_upload/"
                upload_file_path = os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))) + select_status_res[0]["file_path"]
                files = {"file": open(upload_file_path, "rb")}
                requests.post(upload_request_path, files=files)
                os.remove(upload_file_path)
                delete_sql = "delete from product_barcode where id='%s';" % id_item
                connect_mysql(sql_text=delete_sql)
            else:
                print("删除主服务器文件、删除数据")
                # 删除主服务器文件、删除数据
                delete_request_path = "https://www.beyoung.group/tm_data_delete/"
                file_name = select_status_res[0]["product_name"] + "_" + select_status_res[0]["fnsku"] + ".btw"
                res = requests.post(delete_request_path, data={"barcode_name": file_name})
                print(res)
                delete_status_sql = "delete from product_barcode where id='%s';" % id_item
                print("delete_status_sql: ", delete_status_sql)
                connect_mysql(sql_text=delete_status_sql)
        else:
            print("审核不通过")
            if select_status_res[0]["status"] == "0":
                print("删除运营服务器待审核文件、删除数据")
                # 删除运营服务器待审核文件、删除数据
                upload_file_path = select_status_res[0]["file_path"]
                os.remove(upload_file_path)

                delete_status_sql = "delete from product_barcode where id='%s';" % id_item
                connect_mysql(sql_text=delete_status_sql)
            else:
                print("删除数据")
                # 删除数据
                update_status_sql = "update product_barcode set status='1' where id='%s';" % id_item
                connect_mysql(sql_text=update_status_sql)
    res = {"code": 200}
    return JsonResponse(res)

# --------------------------------------------------割割割割割割割割


# 功能函数-查询文字文档表（文字文档）
def select_text_document(platform=None, country=None, site=None, sku=None):
    print("------功能函数-查询文字文档表（文字文档）-------")
    select_sql = "select * from text_document where id!=''"
    if platform:
        select_sql += " and platform='" + platform + "'"
    if site:
        select_sql += " and site='" + site + "'"
    if country:
        select_sql += " and country='" + country + "'"
    if sku:
        select_sql += " and sku='" + sku + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = connect_mysql(sql_text=select_sql)
    return select_res


# 功能函数-组织数据（文字文档）
def organization_text_data(select_res):
    res_data = []
    for item in select_res:
        small_list = list()
        # id
        small_list.append(item[0])
        # 站点，国家，sku，标题，描述
        small_list.extend(item[2:7])

        res_data.append(small_list)
    return res_data


# 功能函数-连表查询（产品+商品信息）（文字文档）
def select_product_commodity(platform=None, country=None, site=None, sku=None):
    print("-------功能函数-连表查询（产品+商品信息）（文字文档）--------")
    select_sql = "select b.platform,b.country,b.site,b.sku from product_message a join commodity_information b " \
                 "on a.product_code=b.product_code where a.id!=''"
    if platform:
        select_sql += " and b.platform='" + platform + "'"
    if country:
        select_sql += " and b.country='" + country + "'"
    if site:
        select_sql += " and b.site='" + site + "'"
    if sku:
        select_sql += " and b.sku='" + sku + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = connect_mysql(sql_text=select_sql)
    return select_res


# 数据库-文字文档-查询
def select_text(request):
    print("-------------数据库-文字文档-查询: ", request.GET)
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    page = request.GET.get("page", "")
    res_data = organization_text_data(select_text_document(platform=platform, country=country, site=site))
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


# 数据库-文字文档-获取下拉框数据
def get_select_text(request):
    print("-------------数据库-文字文档-获取下拉框数据: ", request.GET)
    # 平台，国家，站点，sku
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    sku = request.GET.get("sku", "")
    sku_list = []
    select_res = select_product_commodity(platform=platform, country=country, site=site, sku=sku)
    for item in select_res:
        if item[3] not in sku_list:
            sku_list.append(item[3])
    res = {"code": 200, "sku_list": sku_list}
    print("res: ", res)
    return JsonResponse(res)


# 数据库-文字文档-新增确认
def insert_text(request):
    print("-------------数据库-文字文档-新增确认: ", request.POST)
    platform = request.POST.get("platform", "")
    country = request.POST.get("country", "")
    site = request.POST.get("site", "")
    sku = request.POST.get("sku", "")
    title = request.POST.get("title", "")
    describe = request.POST.get("describe", "")
    insert_sql = "insert into text_document(platform,site,country,sku,title,document_describe) " \
                 "values('%s', '%s', '%s', '%s', '%s', '%s');" \
                 % (platform, site, country, sku, title, describe)
    print("insert_sql: ", insert_sql)
    connect_mysql(sql_text=insert_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 数据库-文字文档-编辑确认
def update_text(request):
    print("-------------数据库-文字文档-编辑确认: ", request.POST)
    text_id = request.POST.get("text_id", "")
    title = request.POST.get("title", "")
    describe = request.POST.get("describe", "")
    update_sql = "update text_document set title='%s',document_describe='%s' where id='%s';" \
                 % (title, describe, text_id)
    connect_mysql(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 数据库-文字文档-删除
def delete_text(request):
    print("-------------数据库-文字文档-删除: ", request.GET)
    text_id = request.GET.getlist("text_id[]", "")
    for item in text_id:
        delete_sql = "delete from text_document where id='%s';" % item
        connect_mysql(sql_text=delete_sql)
    res = {"code": 200}
    return JsonResponse(res)


# --------------------------------------------------割割割割割割割割

# 数据库-设计图片-查询(说明书pdf需要)
def old_select_picture(request):
    """
    款式 -> 货号 -> 主副图 / A+图 / 说明书
    从数据库中寻找该款式对应的encoding，再去寻找该encoding下
    数据库-设计图片-查询:  <QueryDict: {'product_number': ['DNZX-C1'], 'item': ['A']}>
    """
    print("-------------数据库-设计图片-查询: ", request.GET)
    # 中文品名
    product_number = request.GET.get("product_number", "")
    # 国家/A+/说明书
    item = request.GET.get("item", "")
    res_data1 = []
    """
    根据中文spu和中文品名，获取encoding和product_code,然后拼接请求链接，获取图片静态路径
    """
    # 获取产品编码和spu的encoding
    select_sql = "select product_number,encoding from product_zr where product_number='%s';" % product_number
    print("select_sql: ", select_sql)
    select_res = connect_mysql1(sql_text=select_sql)
    print("select_res: ", select_res)
    # 拼接去老服务器获取图片地址的链接
    request_path = "http://www.beyoung.group/design/select_picture/?product_number=" \
                   + select_res[0][0] + "&encoding=" + select_res[0][1] + "&item=" + item
    request_data = requests.get(request_path)
    print("request_data.text: ", request_data.text)
    res_data = eval(request_data.text)["data"]
    # 对文件列表进行加工，生成路径:http://www.beyoung.group/static/images/design_data_se/DNZA/a_add_img/1.2m-sku.jpg
    if item == "说明书":
        for list_item in res_data:
            file_path = "http://www.beyoung.group/static/images/design_data_s" \
                        "e/" + select_res[0][1] + "/instructions/" + list_item
            res_data1.append(file_path)
    elif item == "A":
        for list_item in res_data:
            file_path = "https://www.beyoung.group/show_image/?static/images/design_data_se/" \
                        + select_res[0][1] + "/a_add_img/" + list_item
            res_data1.append(file_path)
    else:
        for list_item in res_data:
            file_path = "https://www.beyoung.group/show_image/?static/images/design_data_s" \
                        "e/" + select_res[0][1] + "/" + select_res[0][0] + "/main_figure/" + item + "/" + list_item
            res_data1.append(file_path)

    res = {"code": 200, "data": res_data1}
    print("res: ", res)
    return JsonResponse(res)


# 数据库-设计图片-查询2.0
def select_picture(request):
    print("-------------数据库-设计图片-查询: ", request.GET)
    # 货号
    product_number = request.GET.get("product_number", "")
    # 国家/A+/说明书
    item = request.GET.get("item", "")

    res_data1 = []

    # 获取产品编码和spu的encoding
    select_sql = "select product_number,encoding from product_zr where product_number='%s';" % product_number
    print("select_sql: ", select_sql)
    select_res = connect_mysql1(sql_text=select_sql, type='dict')
    print("select_res: ", select_res)

    # 拼接去老服务器获取图片地址的链接
    request_path = "http://www.beyoung.group/design/select_picture/?product_number=" \
                   + select_res[0]['product_number'] + "&encoding=" + select_res[0]['encoding'] + "&item=" + item
    request_data = requests.get(request_path)
    # 获取的文件名列表
    res_data = eval(request_data.text)["data"]
    thumbnail_pic_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + "/static/images/" + product_number + "/" + item
    for file_name_item in res_data:
        small_list = []
        if os.path.exists(thumbnail_pic_path + "/" + file_name_item):
            small_list.append("/static/images/" + product_number + "/" + item + "/" + file_name_item)
            small_list.append(select_res[0]['encoding'])
            res_data1.append(small_list)
        else:
            # 对文件名中含有+的文件名进行操作
            if "+" in file_name_item:
                print("对含有+的文件名处理前: ", file_name_item)
                file_name_item = file_name_item.replace("+", "replaceStr")
                print("对含有+的文件名处理后: ", file_name_item)

            # 先下载，保存到本地
            # http://www.beyoung.group/design/download_single_pic/?product_code=DNZD60-C1&item=欧美&encoding=DNZD&file_name=木板对比图-1.jpg

            get_pic_path = "http://www.beyoung.group/design/download_single_pic/?" + "product_code=" \
                           + select_res[0]['product_number'] + "&" + "item=" + item + "&" + "encoding=" \
                           + select_res[0]['encoding'] + "&" + "file_name=" + file_name_item

            print("去老服务器获取单个图片的路由: ", get_pic_path)
            pic_data_obj = requests.get(get_pic_path)
            print("pic_data_obj: ", pic_data_obj)

            # 对文件名中含有+的文件名进行恢复
            if "replaceStr" in file_name_item:
                print("对含有replaceStr的文件名处理前: ", file_name_item)
                file_name_item = file_name_item.replace("replaceStr", "+")
                print("对含有replaceStr的文件名处理后: ", file_name_item)

            save_big_pic_dir_path = thumbnail_pic_path + "/big_pic/"
            save_big_pic_path = save_big_pic_dir_path + file_name_item
            print("save_big_pic_path: ", save_big_pic_path)
            if not os.path.exists(save_big_pic_dir_path):
                os.makedirs(save_big_pic_dir_path)
            with open(save_big_pic_path, "wb") as fw:
                for pic_data_obj_item in pic_data_obj:
                    fw.write(pic_data_obj_item)
            # 再缩小，删除文件
            save_pic_path = thumbnail_pic_path + "/" + file_name_item
            # if not os.path.exists(save_pic_path):
            #     os.makedirs(save_pic_path)
            produceImage(save_big_pic_path, save_pic_path)
            print("product_number", product_number, type(product_number))
            print("item", item, type(item))
            print("file_name_item", file_name_item, type(file_name_item))
            small_list.append("/static/images/" + product_number + "/" + item + "/"
                              + file_name_item)
            small_list.append(select_res[0]['encoding'])
            res_data1.append(small_list)
            os.remove(save_big_pic_path)

            # get_pic_path = "http://www.beyoung.group/static/images/design_data_se/" + select_res[0]['encoding'] + "/"
            # if item == "说明书":
            #     get_pic_path += "instructions/" + file_name_item
            # elif item == "A":
            #     get_pic_path += "a_add_img/" + file_name_item
            # else:
            #     get_pic_path += select_res[0]['product_number'] + "/main_figure/" + item + "/" + file_name_item
            # save_pic_path = thumbnail_pic_path + "/" + file_name_item
            # produceImage(get_pic_path, save_pic_path)
            # res_data1.append("/static/images/" + product_number + "/" + item + "/" + file_name_item)
    res = {"code": 200, "data": res_data1}
    print("res: ", res)
    return JsonResponse(res)


# 数据库-设计图片-单个下载(弃用)
def batch_download(request):
    print("-------------数据库-设计图片-批量下载: ", request.GET)
    product_code = request.GET.get("product_code", "")
    item = request.GET.get("item", "")
    file_name = request.GET.get("file_name", "")

    select_sql = "select encoding from product_zr where product_number='%s';" % product_code
    print("select_sql: ", select_sql)
    select_res = connect_mysql1(sql_text=select_sql, type='dict')
    print("select_res: ", select_res)
    encoding = select_res[0]['encoding']
    # http://www.beyoung.group/design/download_single_pic/?product_code=DNZD60-C1&item=欧美&encoding=DNZD&file_name=木板对比图-1.jpg
    request_path = "http://www.beyoung.group/design/download_single_pic/?" + "product_code=" \
                   + product_code + "&" + "item=" + item + "&" + "encoding=" \
                   + encoding + "&" + "file_name=" + file_name
    res_data = requests.get(request_path)
    response = FileResponse(res_data)
    response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(file_name)
    return response


# 数据库-设计图片-查看大图
def get_big_pic(request):
    print("-------------数据库-设计图片-查看大图: ", request.GET)
    # 货号
    product_number = request.GET.get("product_number", "")
    # 国家/A+/说明书
    item = request.GET.get("item", "")
    # 文件名
    file_name = request.GET.get("file_name", "")

    select_sql = "select product_number,encoding from product_zr where product_number='%s';" % product_number
    print("select_sql: ", select_sql)
    select_res = connect_mysql1(sql_text=select_sql, type='dict')
    print("select_res: ", select_res)

    res_path = "http://www.beyoung.group/static/images/design_data_se/" + select_res[0]['encoding']
    if item == "说明书":
        res_path += "/instructions/" + file_name
    elif item == "A":
        res_path += "/a_add_img/" + file_name
    else:
        res_path += "/" + product_number + "/main_figure/" + item + "/" + file_name

    res = {"code": 200, "data": res_path}
    return JsonResponse(res)


# 数据库-设计图片-获取侧边栏数据
def get_select_picture(request):
    """
    1-获取产品类型下有哪些有哪些款式
    2-获取某款式下有哪些品名
    """
    res_data = requests.get("http://www.beyoung.group/design/get_select_picture/")
    print("res_data.text: ", res_data.text)
    spu_list = eval(res_data.text)['spu_list']
    product_name_list = eval(res_data.text)['product_name_list']
    type_list = eval(res_data.text)['type_list']
    res = {"code": 200, "type_list": type_list, "spu_list": spu_list, "product_name_list": product_name_list}
    print("res: ", res)
    return JsonResponse(res)


# 数据库-设计图片-查看链接
def show_url(request):
    print("\n", "获取展示链接", "\n")
    print("接收的参数: ", request.GET)

    encoding = request.GET.get("encoding", "")
    product_code = request.GET.get("product_code", "")
    type_str = request.GET.get("type_str", "")
    file_name = request.GET.get("file_name", "")
    country = request.GET.get("country", "")

    if type_str == "A":
        type_str = "A+图"
        select_sql = "select * from picture_control where spu='%s' and sizes='%s' and picture_name='%s';" \
                     % (encoding, type_str, file_name)
    else:
        select_sql = "select * from picture_control where spu='%s' and sizes='%s' and picture_name='%s' " \
                     "and product_code='%s' and country='%s';" \
                     % (encoding, type_str, file_name, product_code, country)
    select_res = connect_mysql1(sql_text=select_sql, type='dict')
    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


def produceImage(file_in, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((150, 150), Image.ANTIALIAS)
    resized_image.save(file_out)
