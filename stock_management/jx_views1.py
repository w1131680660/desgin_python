import pymysql
import datetime
import math
import copy
from django.http import JsonResponse
import time
from settings import conf_fun

# # 连接总数据库的运营数据库
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
#
#
# # 连接老数据库
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


# 从commodity_information，product_message中获取侧边栏
def get_calculated_inventory_sidebar(request):
    print("=======================从commodity_information，product_message中获取侧边栏")
    select_sql = "select a.platform,a.country,a.site from commodity_information a join product_message b " \
                 "on a.product_code=b.product_code where b.product_state='在售';"
    platform_country_site = conf_fun.connect_mysql_operation(sql_text=select_sql)

    platform_list = []
    country_list = []
    site_list = []

    for platform_country_site_item in platform_country_site:
        try:
            platform_index = platform_list.index(platform_country_site_item[0])
            # ==============================================
            try:
                country_index = country_list[platform_index].index(platform_country_site_item[1])
                # ==============================================
                try:
                    site_list[platform_index][country_index].index(platform_country_site_item[2])
                except IndexError:
                    site_list[platform_index].append([platform_country_site_item[2]])
                except ValueError:
                    site_list[platform_index][country_index].append(platform_country_site_item[2])
                # ==============================================
            except IndexError:
                country_list.append([platform_country_site_item[1]])
                site_list.append([[platform_country_site_item[2]]])
            except ValueError:
                country_list[platform_index].append(platform_country_site_item[1])
                site_list[platform_index].append([platform_country_site_item[2]])
            # ==============================================
        except ValueError:
            platform_list.append(platform_country_site_item[0])
            country_list.append([platform_country_site_item[1]])
            site_list.append([[platform_country_site_item[2]]])

    print("platform_list: ", platform_list)
    print("country_list: ", country_list)
    print("site_list: ", site_list)

    res = {"code": 200, "platform_list": platform_list, "country_list": country_list, "site_list": site_list}
    print("res: ", res)
    return JsonResponse(res)


# 得到符合渠道，国家，站点，商品类型的((spu,sku,体积,重量),())
def get_spu_sku(platform, country, site, product_type):
    select_sql = "select a.spu,a.sku,b.product_volume,b.product_weight " \
                 "from commodity_information a join product_message b " \
                 "on a.product_code=b.product_code " \
                 "where a.platform='%s' and a.country='%s' and a.site='%s' and b.product_type='%s';" \
                 % (platform, country, site, product_type)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    return select_res


# 得到91天前到昨天的日期列表
def get_all_date_list():
    start_date = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=90), "%Y-%m-%d")
    all_date_list = [start_date]
    for i in range(89):
        new_date = datetime.datetime.strftime(
            datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=(i + 1)), "%Y-%m-%d")
        all_date_list.append(new_date)
    return all_date_list


# 接收((spu,sku,体积,重量),()),返回[spu,spu],[[sku,sku],[sku,sku]]
def get_class_spu_sku(iterator):
    spu_list = []
    sku_list = []
    for item in iterator:
        try:
            spu_list_index = spu_list.index(item[0])
            try:
                sku_list[spu_list_index].index(item[1])
            except ValueError:
                sku_list[spu_list_index].append(item[1])
        except ValueError:
            spu_list.append(item[0])
            sku_list.append([item[1]])
    return [spu_list, sku_list]


# 获得单个spu的所有sku的90天内销量
def get_spu_sell(sku_list):
    start_date = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=90), "%Y-%m-%d")
    end_date = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y-%m-%d")
    sku_tup = tuple(sku_list)
    if len(sku_tup) == 1:
        select_sql = "select sku,times,nums from sku_report where sku='%s' and times>='%s' and times<='%s';" \
                     % (sku_tup[0], start_date, end_date)
    else:
        select_sql = "select sku,times,nums from sku_report where sku in %s and times>='%s' and times<='%s';" \
                     % (sku_tup, start_date, end_date)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    return select_res


# 获取一个spu的90天内销量矩阵
def get_spu_all_sell(all_date_list, sku_list, spu_sell_list):
    spu_all_sell_list = []
    for i in range(len(sku_list)):
        spu_all_sell_list.append([0] * 90)
    for item in spu_sell_list:
        sku_index = sku_list.index(item[0])
        all_date_index = all_date_list.index(item[1])
        spu_all_sell_list[sku_index][all_date_index] = int(item[2])
    return spu_all_sell_list


# 获取一个spu的90天内销量矩阵中零销最少的一个15天矩阵
def get_min_zero_list(spu_all_sell_list):
    target_index = 0
    min_zero_num = 999
    target_sell_num = 0
    for i in range(76):
        zero_num = 0
        sell_num = 0
        for j in range(len(spu_all_sell_list)):
            zero_num += spu_all_sell_list[j][i:i + 15].count(0)
            sell_num += sum(spu_all_sell_list[j][i:i + 15])
        if zero_num < min_zero_num:
            target_index = i
            min_zero_num = zero_num
            target_sell_num = sell_num
        elif zero_num == min_zero_num:
            if target_sell_num < sell_num:
                target_index = i
                min_zero_num = zero_num
                target_sell_num = sell_num
    target_list = []
    for k in range(len(spu_all_sell_list)):
        target_list.append(spu_all_sell_list[k][target_index:target_index + 15])
    return target_list


# 计算传入列表前十个元素的均值和后十个的均值，取大值
def get_avg(target_list):
    avg_list = []
    for item in target_list:
        avg1 = sum(item[0:10]) / len(item[0:10])
        avg2 = sum(item[5:]) / len(item[5:])
        if avg1 > avg2:
            avg_list.append(avg1)
        else:
            avg_list.append(avg2)
    return avg_list


# 获取公共数据，[装柜天数,海运周期,补后可售天数,补后售空日期]
def get_public_data(platform, country, site, product_type):
    select_sql = "select * from calculate_inventory_variable " \
                 "where platform='%s' and country='%s' and site='%s' and product_type='%s' and (sku is NULL or sku='');" \
                 % (platform, country, site, product_type)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, type='dict')
    return select_res


# 计算海运周期
def get_shipping_cycle(site, country):
    shop_name = site + country
    select_shipping_cycle_sql = "select avg(shipping_cycle) from cargo_num_retrieval where shop_name='%s' " \
                                "group by shop_name;" % shop_name
    select_avg_shipping_cycle_res = conf_fun.connect_mysql_re(sql_text=select_shipping_cycle_sql)
    if len(select_avg_shipping_cycle_res) > 0:
        return float(select_avg_shipping_cycle_res[0][0])
    else:
        return 30


# 获取在仓数量/在途数量
def calculated_inventory_total(sku):
    # 获取fba的数量
    select_fba_number_sql = "select fba from sku_report where sku='%s' order by id desc LIMIT 1;" % sku
    select_fba_number_res = conf_fun.connect_mysql_re(sql_text=select_fba_number_sql)
    if len(select_fba_number_res) > 0:
        fba_number = select_fba_number_res[0][0]
    else:
        fba_number = 0
    # 获取fbm的数量
    select_fbm_number_sql = "select nums from fbm_data where sku='%s' order by id desc LIMIT 1;" % sku
    select_fbm_number_res = conf_fun.connect_mysql_re(sql_text=select_fbm_number_sql)
    if len(select_fbm_number_res) > 0:
        fbm_number = select_fbm_number_res[0][0]
    else:
        fbm_number = 0
    # 获取在途数量
    select_on_load_sql = "select sum(b.cargo_num) from arrival_receive a join cargo_information b " \
                         "on a.container_no=b.container_num " \
                         "where (a.receive_count='' or a.receive_count is NULL) and b.sku='%s';" \
                         % sku
    select_on_load_res = conf_fun.connect_mysql_operation(sql_text=select_on_load_sql, dbs='product_supplier')
    if len(select_on_load_res) > 0 and select_on_load_res[0][0] is not None:
        on_load_number = select_on_load_res[0][0]
    else:
        on_load_number = 0
    # ===========
    inventory_total = int(fba_number) + int(fbm_number)
    on_load_total = int(on_load_number)
    # ===========
    return [inventory_total, on_load_total]


# 获取相关sku的在途的数量和预计到港时间
def get_onload_sku(sku_list):
    sku_distinct_list = []
    for item in sku_list:
        for sku_item in item:
            if sku_item not in sku_distinct_list:
                sku_distinct_list.append(sku_item)
    sku_distinct_tup = tuple(sku_distinct_list)
    if len(sku_distinct_tup) > 1:
        select_sql = "select b.sku,b.cargo_num,a.arrival_date " \
                     "from arrival_receive a join cargo_information b " \
                     "on a.container_no=b.container_num " \
                     "where (a.receive_count='' or a.receive_count is NULL) " \
                     "and b.sku in " + str(sku_distinct_tup) + " order by a.arrival_date;"
    else:
        select_sql = "select b.sku,b.cargo_num,a.arrival_date " \
                     "from arrival_receive a join cargo_information b " \
                     "on a.container_no=b.container_num " \
                     "where (a.receive_count='' or a.receive_count is NULL) " \
                     "and b.sku='%s' order by a.arrival_date;" \
                     % sku_distinct_tup[0]
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, dbs="product_supplier")
    # 数据清洗
    return_data = []
    if len(select_res) > 0:
        # ((sku,数量,到港日期),())
        for item in select_res:
            small_list = list(item)
            small_list[2] = small_list[2].split(" ")[0]
            if len(small_list[2].split("-")) != 3:
                continue
            return_data.append(small_list)
    else:
        pass
    return return_data


# 计算两个时间之间的天数差值
def get_date_diff(date_one, date_two):
    day_num = (datetime.datetime.strptime(date_one, "%Y-%m-%d") - datetime.datetime.strptime(date_two, "%Y-%m-%d")).days
    return day_num


# 计算售空日期[[spu,sku,在仓数量,在途数量,均单量,体积,重量],[]]
# [[sku,数量,预计到港时间],[]]
def get_sell_out_date(res_data, onload_sku):
    for item in res_data:
        can_sell_day = item[2] / item[4]
        sell_out_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=can_sell_day), "%Y-%m-%d")
        if item[3] == 0:
            pass
        else:
            for onload_sku_item in onload_sku:
                if onload_sku_item[0] == item[1]:
                    if onload_sku_item[2] < sell_out_date:
                        can_sell_day = float(onload_sku_item[1]) / item[4]
                        sell_out_date = datetime.datetime.strftime(
                            datetime.datetime.strptime(sell_out_date, "%Y-%m-%d") + datetime.timedelta(days=can_sell_day), "%Y-%m-%d")
                    else:
                        can_sell_day = get_date_diff(onload_sku_item[2], sell_out_date)
                        sell_out_date = datetime.datetime.strftime(
                            datetime.datetime.strptime(sell_out_date, "%Y-%m-%d") + datetime.timedelta(
                                days=can_sell_day), "%Y-%m-%d")

                        can_sell_day = float(onload_sku_item[1]) / item[4]
                        sell_out_date = datetime.datetime.strftime(
                            datetime.datetime.strptime(sell_out_date, "%Y-%m-%d") + datetime.timedelta(
                                days=can_sell_day), "%Y-%m-%d")
                else:
                    continue
        item.insert(5, sell_out_date)
    return res_data


# 计算补货数量[[spu,sku,在仓数量,在途数量,均单量,售空日期,体积,重量],[]]
def get_replenish_num(res_data, delivery_day, shipping_cycle, replenish_can_sell_day_number):
    onload_day = int(delivery_day) + int(shipping_cycle)
    onload_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=onload_day), "%Y-%m-%d")
    for item in res_data:
        if item[5] <= onload_date:
            replenish_num = item[4] * float(replenish_can_sell_day_number)
            if 0 < replenish_num < 30:
                item.insert(-2, 30)
            else:
                item.insert(-2, replenish_num)
        else:
            item.insert(-2, 0)
    return res_data


# 将体积重量换成总体积，总重量[[spu,sku,在仓数量,在途数量,均单量,售空日期,补货数量,总体积,总重量],[]]
def get_sum_volume_weight(res_data):
    res_data_new = copy.deepcopy(res_data)
    res_data_one = []
    for res_data_new_item in res_data_new:
        res_data_new_item[-2] = res_data_new_item[-3] * float(res_data_new_item[-2]) if res_data_new_item[-2] else 0
        res_data_new_item[-1] = res_data_new_item[-3] * float(res_data_new_item[-1]) if res_data_new_item[-1] else 0
        res_data_one.append(res_data_new_item)
    return res_data_one


# 对体积和重量进行限制[[spu,sku,在仓数量,在途数量,均单量,售空日期,补货数量,总体积,总重量],[]](旧，弃用)
def get_ture_data1(res_data, res_data_one, country):
    target_volume = 67
    target_weight = 19500
    change_volume = 67
    change_weight = 19500
    volume_list = [float(x[-2]) for x in res_data_one if x[-2]]
    sum_volume = sum(volume_list)
    if sum_volume > target_volume:
        for i1 in range(len(res_data_one)):
            # 补货数量为30
            if res_data_one[i1][-3] == 30:
                sum_volume -= float(res_data_one[i1][-2])
                change_volume -= res_data_one[i1][-3] * float(res_data[i1][-2])
        ratio_volume = sum_volume / change_volume
        for i in range(len(res_data_one)):
            # 补货数量为30或0
            if res_data_one[i][-3] == 30 or res_data_one[i][-3] == 0:
                continue
            else:
                res_data_one[i][-3] = ((res_data_one[i][-3] / ratio_volume) // 10 + 1) * 10
                # 补货量除以比例后小于30
                if res_data_one[i][-3] < 30:
                    res_data_one[i][-3] = 30
                    res_data_one[i][-2] = 30 * float(res_data[i][-2])
                    res_data_one[i][-1] = 30 * float(res_data[i][-1])
                else:
                    res_data_one[i][-2] = res_data_one[i][-3] * float(res_data[i][-2])
                    res_data_one[i][-1] = res_data_one[i][-3] * float(res_data[i][-1])

    weight_list = [float(x[-1]) for x in res_data_one if x[-1]]
    sum_weight = sum(weight_list)
    if country == "美国" and sum_weight > target_weight:
        for j1 in range(len(res_data_one)):
            # 补货数量为30
            if res_data_one[j1][-3] == 30:
                sum_weight -= float(res_data_one[j1][-1])
                change_weight -= res_data_one[j1][-3] * float(res_data[j1][-1])
        ratio_weight = sum_weight / change_weight

        for j in range(len(res_data_one)):
            # 补货数量为30或0
            if res_data_one[j][-3] == 30 or res_data_one[j][-3] == 0:
                continue
            else:
                res_data_one[j][-3] = ((res_data_one[j][-3] / ratio_weight) // 10 + 1) * 10
                # 补货量除以比例后小于30
                if res_data_one[j][-3] < 30:
                    res_data_one[j][-3] = 30
                    res_data_one[j][-1] = 30 * float(res_data[j][-1])
                    res_data_one[j][-2] = 30 * float(res_data[j][-2])
                else:
                    res_data_one[j][-1] = res_data_one[j][-3] * float(res_data[j][-1])
                    res_data_one[j][-2] = res_data_one[j][-3] * float(res_data[j][-2])
    return res_data_one


# 对体积和重量进行限制[[spu,sku,在仓数量,在途数量,均单量,售空日期,补货数量,总体积,总重量],[]]
def get_ture_data(res_data, res_data_one, country):
    target_volume = 67
    target_weight = 19500
    change_volume = 67
    change_weight = 19500
    volume_list = [float(x[-2]) for x in res_data_one if x[-2]]
    sum_volume = sum(volume_list)
    if sum_volume > target_volume:
        for i1 in range(len(res_data_one)):
            # 补货数量为30
            if res_data_one[i1][-3] == 30:
                sum_volume -= float(res_data_one[i1][-2])
                change_volume -= float(res_data_one[i1][-2])
        ratio_volume = sum_volume / change_volume
        for i in range(len(res_data_one)):
            # 补货数量为30或0
            if res_data_one[i][-3] == 30 or res_data_one[i][-3] == 0:
                continue
            else:
                res_data_one[i][-3] = ((res_data_one[i][-3] / ratio_volume) // 10) * 10
                # 补货量除以比例后小于30
                if res_data_one[i][-3] < 30:
                    res_data_one[i][-3] = 30
                    res_data_one[i][-2] = 30 * float(res_data[i][-2])
                    res_data_one[i][-1] = 30 * float(res_data[i][-1])
                else:
                    res_data_one[i][-2] = res_data_one[i][-3] * float(res_data[i][-2])
                    res_data_one[i][-1] = res_data_one[i][-3] * float(res_data[i][-1])

    weight_list = [float(x[-1]) for x in res_data_one if x[-1]]
    sum_weight = sum(weight_list)
    if country == "美国" and sum_weight > target_weight:
        for j1 in range(len(res_data_one)):
            # 补货数量为30
            if res_data_one[j1][-3] == 30:
                sum_weight -= float(res_data_one[j1][-1])
                change_weight -= float(res_data_one[j1][-1])
        ratio_weight = sum_weight / change_weight

        for j in range(len(res_data_one)):
            # 补货数量为30或0
            if res_data_one[j][-3] == 30 or res_data_one[j][-3] == 0:
                continue
            else:
                res_data_one[j][-3] = ((res_data_one[j][-3] / ratio_weight) // 10) * 10
                # 补货量除以比例后小于30
                if res_data_one[j][-3] < 30:
                    res_data_one[j][-3] = 30
                    res_data_one[j][-1] = 30 * float(res_data[j][-1])
                    res_data_one[j][-2] = 30 * float(res_data[j][-2])
                else:
                    res_data_one[j][-1] = res_data_one[j][-3] * float(res_data[j][-1])
                    res_data_one[j][-2] = res_data_one[j][-3] * float(res_data[j][-2])
    return res_data_one


# 库存测算主函数3.0
def calculate_inventory_three(request):
    print("===========================================库存测算主函数")
    print("接收到: ", request.GET)
    mark_start_time = time.time()
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")

    # 获取满足条件的((spu,sku,体积,重量),())
    spu_sku = get_spu_sku(platform, country, site, product_type)

    # 获取公共数据，[装柜天数,海运周期,补后可售天数]
    public_data = get_public_data(platform, country, site, product_type)
    if len(public_data) > 0:
        delivery_day = public_data[0]['delivery_day'] if public_data[0]['delivery_day'] else 14
        shipping_cycle = public_data[0]['shipping_cycle'] if public_data[0]['shipping_cycle'] \
            else get_shipping_cycle(site, country)
        replenish_can_sell_day_number = public_data[0]['replenish_can_sell_day_number'] \
            if public_data[0]['replenish_can_sell_day_number'] else 45
    else:
        delivery_day = 14
        shipping_cycle = get_shipping_cycle(site, country)
        replenish_can_sell_day_number = 45
    total_onload_day = int(delivery_day) + int(shipping_cycle)

    print("公共数据: ", delivery_day, shipping_cycle, replenish_can_sell_day_number)

    # 对spu，sku进行分级
    spu_sku_list = get_class_spu_sku(spu_sku)
    spu_list = spu_sku_list[0]
    sku_list = spu_sku_list[1]

    print("对spu，sku进行分级: ")
    sku_distinct_list = []
    for item5 in sku_list:
        for item6 in item5:
            if item6 not in sku_distinct_list:
                sku_distinct_list.append(item6)

    # 组织返回的数据[[spu,sku,体积,重量],[]]
    res_data = []
    for i in range(len(spu_list)):
        for sku_item in sku_list[i]:
            small_list = [spu_list[i], sku_item]
            for spu_sku_item in spu_sku:
                if spu_sku_item[0] == spu_list[i] and spu_sku_item[1] == sku_item:
                    small_list.extend(spu_sku_item[2:])
            res_data.append(small_list)
    print("获取在仓数量和在途数量前: ", time.time())
    # 获取在仓数量和在途数量[[spu,sku,在仓数量,在途数量,体积,重量],[]]
    for res_data_item_inventory_onload in res_data:
        inventory_onload = calculated_inventory_total(res_data_item_inventory_onload[1])
        res_data_item_inventory_onload.insert(2, inventory_onload[0])
        res_data_item_inventory_onload.insert(3, inventory_onload[1])

    print("获取均单量前: ", time.time())

    # 获取均单量
    all_date_list = get_all_date_list()
    for spu_index in range(len(spu_list)):
        spu_sell_list = get_spu_sell(sku_list[spu_index])
        spu_all_sell_list = get_spu_all_sell(all_date_list, sku_list[spu_index], spu_sell_list)
        target_list = get_min_zero_list(spu_all_sell_list)
        avg_sell_list = get_avg(target_list)
        mark_index = 0
        for res_data_item in res_data:
            if res_data_item[0] == spu_list[spu_index]:
                if avg_sell_list[mark_index] == 0:
                    res_data_item.insert(4, 0.01)
                else:
                    res_data_item.insert(4, avg_sell_list[mark_index])
                mark_index += 1

    print("获取均单量后: ", time.time())

    # res_data[[spu,sku,在仓数量,在途数量,均单量,体积,重量],[]]
    select_inventory_variable_sql = "select * from calculate_inventory_variable " \
                                    "where platform='%s' and country='%s' and site='%s' " \
                                    "and product_type='%s' and sku in " + str(tuple(sku_distinct_list)) + ";"
    select_inventory_variable_sql = select_inventory_variable_sql % (platform, country, site, product_type)
    select_inventory_variable_res = conf_fun.connect_mysql_operation(sql_text=select_inventory_variable_sql, type='dict')
    for item1 in res_data:
        for item2 in select_inventory_variable_res:
            if item1[1] == item2['sku']:
                item1[4] = float(item2['average_order']) if item2['average_order'] else item1[4]

    # 计算售空日期
    onload_sku = get_onload_sku(sku_list)
    res_data = get_sell_out_date(res_data, onload_sku)

    # res_data[[spu,sku,在仓数量,在途数量,均单量,售空日期,补货数量，体积,重量],[]]

    # 计算补货数量
    res_data = get_replenish_num(res_data, delivery_day, shipping_cycle, replenish_can_sell_day_number)

    # 将体积重量换成总体积，总重量,并计算限制后的补货数量res_data_one
    res_data_one = get_sum_volume_weight(res_data)

    res_data_one = limit_volume_weight(res_data, res_data_one, country)

    # 体积、重量控制小数
    number_one = 0
    number_two = 0
    number_3 = 0
    for res_data_one_item in res_data_one:
        res_data_one_item[-2] = round(res_data_one_item[-2], 2)
        res_data_one_item[-1] = round(res_data_one_item[-1], 3)

        number_one += res_data_one_item[-2]
        number_two += res_data_one_item[-1]
        if res_data_one_item[-3] != 0 and res_data_one_item[-3] != 30:
            number_3 += 1
    print(number_one, number_two, number_3)

    # 计算补后售空日期
    for item in res_data_one:
        if item[-3] == 0:
            item.append(item[5])
        else:
            arrival_date = datetime.datetime.strftime(
                datetime.datetime.today() + datetime.timedelta(days=total_onload_day), "%Y-%m-%d")
            if arrival_date <= item[5]:
                replenish_num_can_sell_day = math.ceil(item[-3] / item[4])
                replenish_can_sell_date = datetime.datetime.strftime(
                    datetime.datetime.strptime(item[5], "%Y-%m-%d") + datetime.timedelta(
                        days=replenish_num_can_sell_day), "%Y-%m-%d")
                item.append(replenish_can_sell_date)
            else:
                replenish_num_can_sell_day = math.ceil(item[-3] / item[4])
                replenish_can_sell_date = datetime.datetime.strftime(
                    datetime.datetime.strptime(arrival_date, "%Y-%m-%d") + datetime.timedelta(
                        days=replenish_num_can_sell_day), "%Y-%m-%d")
                item.append(replenish_can_sell_date)

    # 编辑的补货数量
    for item3 in range(len(res_data_one)):
        for item4 in select_inventory_variable_res:
            if res_data_one[item3][1] == item4['sku']:
                if item4['replenish_num']:
                    res_data_one[item3][-3] = float(item4['replenish_num']) if item4['replenish_num'] else res_data_one[item3][-3]
                    res_data_one[item3][-2] = round(float(res_data[item3][-2]) * res_data_one[item3][-3], 2)
                    res_data_one[item3][-1] = round(float(res_data[item3][-1]) * res_data_one[item3][-3], 2)

    res = {"code": 200, "data": res_data_one}
    print(mark_start_time, "   开始时间")
    print(time.time(), "   结束时间")
    return JsonResponse(res)


# 库存管理-库存测算3.0-编辑
def update_variable(request):
    print("===========库存管理-库存测算3.0版本-编辑: ", request.POST)
    platform = request.POST.get("platform", "")
    country = request.POST.get("country", "")
    site = request.POST.get("site", "")
    product_type = request.POST.get("product_type", "")

    delivery_day = request.POST.get("delivery_day", "")
    shipping_cycle = request.POST.get("shipping_cycle", "")
    replenish_can_sell_day_number = request.POST.get("replenish_can_sell_day_number", "")
    sku = request.POST.get("sku", "")
    average_order = request.POST.get("average_order", "")
    replenish_num = request.POST.get("replenish_num", "")

    if sku:
        select_distinct_sql = "select id from calculate_inventory_variable " \
                              "where platform='%s' and country='%s' and site='%s' and sku='%s' and product_type='%s';" \
                              % (platform, country, site, sku, product_type)
        print("查询修改sku数据是否重复语句: ", select_distinct_sql)
        select_distinct_res = conf_fun.connect_mysql_operation(sql_text=select_distinct_sql)
        print("查询修改sku数据是否重复结果: ", select_distinct_res)
        if len(select_distinct_res) > 0:
            update_variable_sql = "update calculate_inventory_variable " \
                                  "set average_order='%s',replenish_num='%s' " \
                                  "where platform='%s' and country='%s' and site='%s' and sku='%s' and product_type='%s';" \
                                  % (average_order, replenish_num, platform, country, site, sku, product_type)
            print("update_variable_sql: ", update_variable_sql)
            conf_fun.connect_mysql_operation(sql_text=update_variable_sql)
        else:
            insert_variable_sql = "insert into calculate_inventory_variable" \
                                  "(platform,country,site,product_type,sku,average_order,replenish_num) " \
                                  "values('%s','%s','%s','%s','%s','%s','%s');" \
                                  % (platform, country, site, product_type, sku, average_order, replenish_num)
            print("insert_variable_sql: ", insert_variable_sql)
            conf_fun.connect_mysql_operation(sql_text=insert_variable_sql)
    else:
        select_distinct_sql = "select id from calculate_inventory_variable " \
                              "where platform='%s' and country='%s' and site='%s' and (sku is NULL or sku='') " \
                              "and product_type='%s';" \
                              % (platform, country, site, product_type)
        print("select_distinct_sql: ", select_distinct_sql)
        select_distinct_res = conf_fun.connect_mysql_operation(sql_text=select_distinct_sql)
        print("select_distinct_res: ", select_distinct_res)
        if len(select_distinct_res) > 0:
            update_variable_sql = "update calculate_inventory_variable " \
                                  "set delivery_day='%s',shipping_cycle='%s'," \
                                  "replenish_can_sell_day_number='%s' " \
                                  "where platform='%s' and country='%s' and site='%s' " \
                                  "and (sku is NULL or sku='') and product_type='%s';" \
                                  % (delivery_day, shipping_cycle, replenish_can_sell_day_number,
                                     platform, country, site, product_type)
            print("update_variable_sql: ", update_variable_sql)
            conf_fun.connect_mysql_operation(sql_text=update_variable_sql)
        else:
            insert_variable_sql = "insert into calculate_inventory_variable" \
                                  "(platform,country,site,product_type,delivery_day,shipping_cycle," \
                                  "replenish_can_sell_day_number) " \
                                  "values('%s','%s','%s','%s','%s','%s','%s');" \
                                  % (platform, country, site, product_type, delivery_day, shipping_cycle,
                                     replenish_can_sell_day_number)
            print("insert_variable_sql: ", insert_variable_sql)
            conf_fun.connect_mysql_operation(sql_text=insert_variable_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 获取在途的所有货柜号
def get_all_container(platform=None, country=None, site=None, product_type=None):
    select_sql = "select container_no from arrival_receive " \
                 "where (receive_count='' or receive_count is NULL);"
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, dbs='product_supplier')
    return select_res


# 获取所有在途货柜中所有的（（*），（*））
def get_all_sku_onload_num(all_container_list, all_sku_list):
    if len(all_container_list) > 1:
        select_sql = "select * from cargo_information where container_num in " + str(
            tuple(all_container_list)) + "and sku in " + str(tuple(all_sku_list)) + ";"
    else:
        select_sql = "select * from cargo_information where container_num='%s' and sku in " + str(
            tuple(all_sku_list)) + ";" % all_container_list[0]
    print(693,'\n',select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, dbs='product_supplier', type='dict')
    return select_res


# 库存管理-库存监控[[spu,sku,在仓数量,在途货柜中的数量,在途总数量,数量合计,均单量,售空日期,提示(库存不足,正常,库存冗余)],[]]
def monitor_inventory(request):
    print("===============库存管理-库存监控:", request.GET)
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")

    page = int(request.GET.get("page_number", "1"))

    res_data = []

    # 根据传入的渠道，国家，站点，类型获取满足要求的所有在售的spu,sku
    spu_sku = get_spu_sku(platform, country, site, product_type)
    # 对spu，sku进行分级
    spu_sku_list = get_class_spu_sku(spu_sku)
    spu_list = spu_sku_list[0]
    sku_list = spu_sku_list[1]
    # 生成新的返回数据列表
    for i in range(len(spu_list)):
        for sku_item in sku_list[i]:
            res_data.append([spu_list[i], sku_item])
    # 获取所有不重复的sku列表

    # 总行数
    all_number = len(res_data)

    # 分页功能增加点
    page_start = int(page) * 50 - 50
    page_end = int(page) * 50
    res_data = res_data[page_start:page_end]

    all_sku_list = []
    for res_data_item in res_data:
        if res_data_item[1] not in all_sku_list:
            all_sku_list.append(res_data_item[1])
    # 获取在仓数量/在途总量
    onload_total_list = []
    for item1 in res_data:
        onload_total = calculated_inventory_total(item1[1])
        onload_total_list.append(onload_total)

    # 插入在仓数量
    for i in range(len(res_data)):
        res_data[i].append(onload_total_list[i][0])

    # 获取在途的所有柜号
    all_container = get_all_container(platform, country, site, product_type)
    all_container_list = [x[0] for x in all_container if x[0]]

    # 获取所有在途货柜中所有的sku,select * ,type=dict
    all_sku_onload_num = get_all_sku_onload_num(all_container_list, all_sku_list)

    # 获得对应sku在对应的柜号中的数量[[spu,sku,在仓数量],[]]
    all_container_number = len(all_container_list)
    print("在途的货柜数量: ", all_container_number)
    for res_data_item_one in res_data:
        small_list = [0] * all_container_number
        for sku_onload_item in all_sku_onload_num:
            if sku_onload_item['sku'] == res_data_item_one[1]:
                container_index = all_container_list.index(sku_onload_item['container_num'])
                small_list[container_index] = sku_onload_item['cargo_num']
        res_data_item_one.extend(small_list)

    # 在途数量[[spu,sku,在仓数量,在途各个货柜中的数量],[]]
    for i in range(len(res_data)):
        res_data[i].append(onload_total_list[i][1])

    # 合计[[spu,sku,在仓数量,在途各个货柜中的数量,在途总数量],[]]
    for i in range(len(res_data)):
        res_data[i].append(onload_total_list[i][0] + onload_total_list[i][1])

    # 均单量[[spu,sku,在仓数量,在途各个货柜中的数量,在途总数量,数量合计],[]]
    all_date_list = get_all_date_list()
    for spu_index in range(len(spu_list)):
        spu_sell_list = get_spu_sell(sku_list[spu_index])
        spu_all_sell_list = get_spu_all_sell(all_date_list, sku_list[spu_index], spu_sell_list)
        target_list = get_min_zero_list(spu_all_sell_list)
        avg_sell_list = get_avg(target_list)
        mark_index = 0
        for res_data_item in res_data:
            if res_data_item[0] == spu_list[spu_index]:
                if avg_sell_list[mark_index] == 0:
                    res_data_item.append(0.01)
                else:
                    res_data_item.append(avg_sell_list[mark_index])
                mark_index += 1
    # 查看公共数据
    select_inventory_variable_sql = "select * from calculate_inventory_variable " \
                                    "where platform='%s' and country='%s' and site='%s' " \
                                    "and product_type='%s' and sku in " + str(tuple(all_sku_list)) + ";"
    select_inventory_variable_sql = select_inventory_variable_sql % (platform, country, site, product_type)
    print("查询公共数据语句: ", select_inventory_variable_sql)
    select_inventory_variable_res = conf_fun.connect_mysql_operation(sql_text=select_inventory_variable_sql, type='dict')
    for item1 in res_data:
        for item2 in select_inventory_variable_res:
            if item1[1] == item2['sku']:
                item1[4] = float(item2['average_order']) if item2['average_order'] else item1[4]

    # 预计售空日期[[spu,sku,在仓数量,在途各个货柜中的数量,在途总数量,数量合计,均单量],[]]
    onload_sku = get_onload_sku(sku_list)
    for item in res_data:
        can_sell_day = item[2] / item[-1]
        sell_out_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=can_sell_day), "%Y-%m-%d")

        if item[-3] == 0:
            pass
        else:
            for onload_sku_item in onload_sku:
                if onload_sku_item[0] == item[1]:
                    if onload_sku_item[2] < sell_out_date:
                        can_sell_day = float(onload_sku_item[1]) / item[-3]
                        sell_out_date = datetime.datetime.strftime(
                            datetime.datetime.strptime(sell_out_date, "%Y-%m-%d") + datetime.timedelta(
                                days=can_sell_day), "%Y-%m-%d")
                    else:
                        can_sell_day = get_date_diff(onload_sku_item[2], sell_out_date)
                        sell_out_date = datetime.datetime.strftime(
                            datetime.datetime.strptime(sell_out_date, "%Y-%m-%d") + datetime.timedelta(
                                days=can_sell_day), "%Y-%m-%d")

                        can_sell_day = float(onload_sku_item[1]) / item[-3]
                        sell_out_date = datetime.datetime.strftime(
                            datetime.datetime.strptime(sell_out_date, "%Y-%m-%d") + datetime.timedelta(
                                days=can_sell_day), "%Y-%m-%d")
                else:
                    continue
        item.append(sell_out_date)

    # 提示[[spu,sku,在仓数量,在途各个货柜中的数量,在途总数量,数量合计,均单量,预计售空日期],[]]
    date_one = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=30), "%Y-%m-%d")
    date_two = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=90), "%Y-%m-%d")
    for item in res_data:
        if item[-1] < date_one:
            if item[-2] == 0.01:
                item.append("正常")
            else:
                item.append("库存不足")
        elif item[-1] < date_two:
            if item[-2] == 0.01:
                item.append("库存冗余")
            else:
                item.append("正常")
        else:
            item.append("库存冗余")

    res = {"code": 200, "data": res_data, "header": all_container_list, "all_number": all_number}
    print("返回的数据: ", res)
    return JsonResponse(res)


# 体积重量限制2.0
def limit_volume_weight(res_data, res_data_one, country):
    print("\n", "体积总量限制2.0", "\n")
    # res_data[[spu,sku,在仓数量,在途数量,均单量,售空日期,补货数量，体积,重量],[]]

    volume_list = [float(x[-2]) for x in res_data_one]
    supplement_list = [float(x[-3]) for x in res_data_one if float(x[-3]) !=0 or float(x[-3]) != 30]
    sum_volume = sum(volume_list)
    if sum_volume > 67:
        if len(supplement_list) == 0:
            pass
        else:
            target_volume = 67
            for res_data_one_item in res_data_one:
                if res_data_one_item[-3] == 30:
                    sum_volume -= float(res_data_one_item[-2])
                    target_volume -= float(res_data_one_item[-2])
            volume_ratio = sum_volume / target_volume
            for i in range(len(res_data_one)):
                if res_data_one[i][-3] == 30 or res_data_one[i][-3] == 0:
                    pass
                else:
                    res_data_one[i][-3] = ((float(res_data_one[i][-2]) / volume_ratio) / float(res_data[i][-2])) // 10 * 10
                    if res_data_one[i][-3] < 30:
                        res_data_one[i][-3] = 30
                        res_data_one[i][-2] = 30 * float(res_data[i][-2])
                    else:
                        res_data_one[i][-2] = res_data_one[i][-3] * float(res_data[i][-2])

    if country == "美国":
        weight_list = [float(x[-1]) for x in res_data_one]
        sum_weight = sum(weight_list)
        if sum_weight > 19500:
            supplement_list_one = [float(x[-3]) for x in res_data_one if float(x[-3]) != 0 or float(x[-3]) != 30]
            if len(supplement_list_one) == 0:
                pass
            else:
                target_weight = 19500
                for res_data_one_item_one in res_data_one:
                    if res_data_one_item_one[-3] == 30:
                        sum_weight -= float(res_data_one_item_one[-1])
                        target_weight -= float(res_data_one_item_one[-1])
                weight_ratio = sum_weight / target_weight
                for i in range(len(res_data_one)):
                    if res_data_one[i][-3] == 30 or res_data_one[i][-3] == 0:
                        pass
                    else:
                        res_data_one[i][-3] = ((float(res_data_one[i][-1]) / weight_ratio) / float(res_data[i][-1])) // 10 * 10
                        if res_data_one[i][-3] < 30:
                            res_data_one[i][-3] = 30
                            res_data_one[i][-1] = 30 * float(res_data[i][-1])
                            res_data_one[i][-2] = 30 * float(res_data[i][-2])
                        else:
                            res_data_one[i][-1] = res_data_one[i][-3] * float(res_data[i][-1])
                            res_data_one[i][-2] = res_data_one[i][-3] * float(res_data[i][-2])
    else:
        pass

    return res_data_one


# 获取在仓/在途数量
def get_stoge_onload_number(sku_list):
    # 获取fba的数量
    select_fba_number_sql = "select sku,fba from sku_report where sku in %s order by id desc;" \
                            % str(tuple(sku_list))
    select_fba_number_res = conf_fun.connect_mysql_re(sql_text=select_fba_number_sql, type='dict')
    if len(select_fba_number_res) > 0:
        fba_number = select_fba_number_res[0][0]
    else:
        fba_number = 0
    # 获取fbm的数量
    select_fbm_number_sql = "select nums from fbm_data where sku='%s' order by id desc LIMIT 1;" % sku
    select_fbm_number_res = conf_fun.connect_mysql_re(sql_text=select_fbm_number_sql)
    if len(select_fbm_number_res) > 0:
        fbm_number = select_fbm_number_res[0][0]
    else:
        fbm_number = 0
    # 获取在途数量
    select_on_load_sql = "select sum(b.cargo_num) from arrival_receive a join cargo_information b " \
                         "on a.container_no=b.container_num " \
                         "where (a.receive_count='' or a.receive_count is NULL) and b.sku='%s';" %(sku)
    select_on_load_res = conf_fun.connect_mysql_operation(sql_text=select_on_load_sql, dbs='product_supplier')
    if len(select_on_load_res) > 0 and select_on_load_res[0][0] is not None:
        on_load_number = select_on_load_res[0][0]
    else:
        on_load_number = 0
    # ===========
    inventory_total = int(fba_number) + int(fbm_number)
    on_load_total = int(on_load_number)
    # ===========
    return [inventory_total, on_load_total]














