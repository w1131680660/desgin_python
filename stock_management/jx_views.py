import pymysql
import pandas as pd
import datetime as dt
import math
from django.http import JsonResponse
from settings import conf_fun

# # 连接正式服数据库
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
# # 连接总数据库的运营数据库
# def connect_mysql3(sql_text, dbs='operation', type='tuple'):
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
# # 连接总数据库的物流数据库
# def connect_mysql4(sql_text, dbs='product_supplier', type='tuple'):
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


# 根据sku计算均单量
def calculated_average_order(sku):
    # 计算该sku在sku_report中的30天内，零日销量最少的连续15天，获取其平均日销量
    within_date = dt.datetime.strftime(dt.datetime.today() + dt.timedelta(days=-30), "%Y-%m-%d")
    select_sku_report_sql = "select nums from sku_report " \
                            "where sku='%s' and times>='%s' " \
                            "order by times desc limit 30;" \
                            % (sku, within_date)
    within_sku_report_tup = conf_fun.connect_mysql_operation(sql_text=select_sku_report_sql)
    # ===========
    within_sku_report_list = []
    if len(within_sku_report_tup) > 15:
        for i in range(len(within_sku_report_tup) - 14):
            within_sku_report_list.append(within_sku_report_tup[i:i + 15])
    else:
        within_sku_report_list.extend([x[0] for x in within_sku_report_tup])
    # ===========
    if len(within_sku_report_list) == 0:
        return 0
    min_index = 0
    for i in range(len(within_sku_report_list)):
        min_index = i if within_sku_report_list[i].count("0") \
                         < within_sku_report_list[min_index].count("0") else min_index
    calculate_average_order = sum([int(x[0]) for x in within_sku_report_list[min_index]]) / len(within_sku_report_list)
    # ===========
    print("计算返回的均单量: ", calculate_average_order)
    return calculate_average_order


# 获取海外库存/在途总量
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
                         "where (a.receive_count='' or a.receive_count is NULL) and sku='%s';" \
                         % sku
    select_on_load_res = conf_fun.connect_mysql_product_supplier(sql_text=select_on_load_sql)
    if len(select_on_load_res) > 0 and select_on_load_res[0][0] is not None:
        on_load_number = select_on_load_res[0][0]
    else:
        on_load_number = 0
    # ===========
    inventory_total = int(fba_number) + int(fbm_number)
    on_load_total = int(on_load_number)
    # ===========
    print("获取海外库存/在途总量返回: ", [inventory_total, on_load_total])
    return [inventory_total, on_load_total]


# 获取某所有在途的柜子中某sku的数量和预计到达日
def on_load_container(sku):
    select_on_load_sql = "select b.cargo_num,a.arrival_date from arrival_receive a join cargo_information b " \
                         "on a.container_no=b.container_num " \
                         "where (a.receive_count='' or a.receive_count is NULL) and b.sku='%s' " \
                         "order by a.arrival_date;" \
                         % sku
    on_load_sku = conf_fun.connect_mysql_product_supplier(sql_text=select_on_load_sql)
    on_load_list = []
    if len(on_load_sku) > 0:
        for i in range(len(on_load_sku)):
            item_list = list(on_load_sku[i])
            item_list[1] = item_list[1].split(" ")[0]
            if len(item_list[1].split("-")) != 3:
                continue
            on_load_list.append(item_list)
    print("获取某所有在途的柜子中某sku的数量和预计到达日: ", on_load_list)
    return on_load_list


# 根据传入的渠道/国家/站点/类型获取满足要求的所有在售的sku
def get_spu(platform, country, site, product_type):
    select_spu_sql = "select distinct a.spu " \
                     "from commodity_information a join product_message b " \
                     "on a.product_code=b.product_code " \
                     "where a.platform='%s' and a.country='%s' " \
                     "and a.site='%s' and b.product_state='在售' and b.product_type='%s';" \
                     % (platform, country, site, product_type)
    select_spu_res = conf_fun.connect_mysql_operation(sql_text=select_spu_sql)
    return select_spu_res


# 根据传入的spu求出在售的所有sku
def get_sku_for_spu(spu):
    select_sku_sql = "select sku from commodity_information where spu='%s';" % spu
    select_sku_res = conf_fun.connect_mysql_operation(sql_text=select_sku_sql)
    return select_sku_res


# 求出某个sku连续15天的销量(几天前开始，sku)
def get_sku_sales(start_day, sku):
    """
    查询一个sku指定日期内的所有销量数据（（日期，销量），（））
    将所有的日期存到一个列表
    遍历从昨天开始的连续十五天日期，如果每天的日期存在日期列表，则写入相应数据，否则为零
    """
    end_date = dt.datetime.strftime(dt.datetime.today() - dt.timedelta(days=start_day), "%Y-%m-%d")
    start_date = dt.datetime.strftime(
        dt.datetime.strptime(end_date, "%Y-%m-%d") - dt.timedelta(days=14), "%Y-%m-%d")

    select_sql = "select times,nums from sku_report " \
                 "where sku='%s' and times>='%s' and times<='%s';" \
                 % (sku[0], start_date, end_date)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    date_list = []
    if len(select_res) > 0:
        for res_item in select_res:
            date_list.append([res_item[0], res_item[1]])
    data_list = []
    for i in range(15):
        target_date = dt.datetime.strftime(
            dt.datetime.strptime(start_date, "%Y-%m-%d") + dt.timedelta(days=i), "%Y-%m-%d")
        for item in date_list:
            if target_date == item[0]:
                data_list.append(int(item[1]))
        else:
            data_list.append(0)
    return data_list


# 获取一个spu下所有sku的用来求出平均销量的销量列表
def get_sales_list(sku_tup):
    min_matrix = []
    for i in range(len(sku_tup)):
        min_matrix.append([0] * 15)
    # ==========================================
    sales_matrix = []
    for i in range(76):
        # ==========================================
        # 获得一个spu的某个时间段的销量矩阵
        print("==============================")
        for single_sku in sku_tup:
            sales_matrix.append(get_sku_sales(i + 1, single_sku))
            print("@$#!", get_sku_sales(i + 1, single_sku))
        # ==========================================
        # 比较零销的天数
        sales_zero_count = 0
        for sales_matrix_item in sales_matrix:
            sales_zero_count += sales_matrix_item.count(0)
        min_zero_count = 60
        # for min_matrix_item in min_matrix:
        #     min_zero_count += min_matrix_item.count(0)
        if sales_zero_count < min_zero_count:
            min_matrix = sales_matrix
            min_zero_count = sales_zero_count
        # 零销天数一样，比较总销量
        elif sales_zero_count == min_zero_count:
            sales_zero_sum = 0
            for sales_matrix_item1 in sales_matrix:
                sales_zero_sum += sum(sales_matrix_item1)
            min_zero_sum = 0
            for min_matrix_item1 in min_matrix:
                min_zero_sum += sum(min_matrix_item1)
            if sales_zero_sum < min_zero_sum:
                min_matrix = sales_matrix
                min_zero_count = sales_zero_count
    print("获取一个spu下所有sku的用来求出平均销量的销量列表", "$$:", min_matrix)
    return min_matrix


# 将一个列表分成头尾两个，各自求平均，取较大值
def get_max_avg(target_list):
    avg1 = sum(target_list[0:11]) / len(target_list[0:11])
    avg2 = sum(target_list[6:-1]) / len(target_list[6:-1])
    if avg1 > avg2:
        return round(avg1, 2)
    else:
        return round(avg2, 2)


# 获取售空日期
def get_sell_out_date(spu_sku_avg, stock_onload):
    sell_out_date = []
    for i in range(len(spu_sku_avg)):
        sell_out_day_number_one = math.ceil(stock_onload[i][0] / spu_sku_avg[i][2])
        sell_out_date_one = dt.datetime.strftime(
            dt.datetime.today() + dt.timedelta(days=sell_out_day_number_one), "%Y-%m-%d")
        on_load_sku_tup = on_load_container(spu_sku_avg[i][1])
        if len(on_load_sku_tup) > 0:
            sell_out_day_number_two = 0
            if on_load_sku_tup[-1][1] < sell_out_date_one:
                on_load_number_list = [float(x[0]) for x in on_load_sku_tup]
                sum_on_load = sum(on_load_number_list)
                sell_out_day_number_two = math.ceil(sum_on_load / spu_sku_avg[i][2])
            else:
                for on_load_sku_item in on_load_sku_tup:
                    if on_load_sku_item[1] < sell_out_date_one:
                        sell_out_day_number_two += math.ceil(float(on_load_sku_item[0]) / spu_sku_avg[i][2])
                    else:
                        # 在途到达前断货天数
                        already_sell_out_day_number = (dt.datetime.strptime(
                            on_load_sku_item[1], "%Y-%m-%d") - dt.datetime.strptime(sell_out_date_one, "%Y-%m-%d")).days
                        sell_out_day_number_two += already_sell_out_day_number
                        sell_out_day_number_two += math.ceil(float(on_load_sku_item[0]) / spu_sku_avg[i][2])
            sell_out_date_two = dt.datetime.strftime(
                dt.datetime.strptime(sell_out_date_one, "%Y-%m-%d") + dt.timedelta(
                    days=sell_out_day_number_two), "%Y-%m-%d")
        else:
            sell_out_date_two = sell_out_date_one
        sell_out_date.append(sell_out_date_two)
    return sell_out_date


# 获取补货数量
def get_supply_num(spu_sku_avg, onload_day_number, replenish_sell_out_date, sell_out_date):
    replenish_num_list = []
    for i in range(len(spu_sku_avg)):
        now_replenish_arrival_date = dt.datetime.strftime(
            dt.datetime.today() + dt.timedelta(days=onload_day_number), "%Y-%m-%d")
        if sell_out_date[i] <= now_replenish_arrival_date:
            print("小于或者等于")
            # 补后售空日期/售空日期，求出两者之间的天数，乘以均单量
            differ_day_number = (dt.datetime.strptime(
                replenish_sell_out_date, "%Y-%m-%d") - dt.datetime.strptime(
                sell_out_date[i], "%Y-%m-%d")).days
            replenish_num = differ_day_number * spu_sku_avg[i][2]
            new_replenish_num = replenish_num // 10
            replenish_num = new_replenish_num * 10 + 10 if replenish_num != new_replenish_num else new_replenish_num
        else:
            replenish_num = 0
        replenish_num_list.append(replenish_num)
    return replenish_num_list


# 求出第一版数据的[总体积,总重量]
def get_max_ratio(middle_data):
    total_volume = 0
    total_weight = 0
    for item in middle_data:
        # [[spu,sku,库存,在途数量,均单量,售空日期,补货数量],[]]
        select_volume_weight_sql = "select b.product_volume,b.product_weight " \
                                   "from commodity_information a join product_message b " \
                                   "on a.product_code=b.product_code where a.sku='%s';" \
                                   % item[1]
        select_volume_weight_res = conf_fun.connect_mysql_operation(sql_text=select_volume_weight_sql)
        if len(select_volume_weight_res) > 0:
            try:
                if float(select_volume_weight_res[0][0]):
                    if item[6] > 30:
                        total_volume += float(select_volume_weight_res[0][0]) * item[6]
                    elif item[6] > 0:
                        total_volume += float(select_volume_weight_res[0][0]) * 30
            except:
                pass

            try:
                if float(select_volume_weight_res[0][1]):
                    if item[6] > 30:
                        total_volume += float(select_volume_weight_res[0][1]) * item[6]
                    elif item[6] > 0:
                        total_volume += float(select_volume_weight_res[0][1]) * 30
            except:
                pass

    return [total_volume, total_weight]


# 求出比例(总体积/限定体积 或 总重量/限定重量)
def get_ratio(country, total_volume_weight, spu_sku_avg):
    for item in spu_sku_avg:
        # [[spu,sku,库存,在途数量,均单量,售空日期,补货数量],[]]
        if item[6] <= 30:
            # 先查出该sku的体积重量，如果有则减去
            select_volume_weight_sql = "select b.product_volume,b.product_weight " \
                                       "from commodity_information a join product_message b " \
                                       "on a.product_code=b.product_code where a.sku='%s';" \
                                       % item[1]
            select_volume_weight_res = conf_fun.connect_mysql_operation(sql_text=select_volume_weight_sql)
            if select_volume_weight_res:
                try:
                    total_volume_weight[0] -= float(select_volume_weight_res[0][0]) * 30
                except:
                    pass
                try:
                    total_volume_weight[1] -= float(select_volume_weight_res[0][1]) * 30
                except:
                    pass
    if country == "美国":
        volume_ratio = total_volume_weight[0] / 67
        weight_ratio = total_volume_weight[1] / 19500
        if volume_ratio > weight_ratio:
            target_ratio = volume_ratio
        else:
            target_ratio = weight_ratio
    else:
        volume_ratio = total_volume_weight[0] / 67
        target_ratio = volume_ratio
    return target_ratio


# 插入最终体积和重量
def append_volume_weight(spu_sku_avg):
    for i in range(len(spu_sku_avg)):
        select_volume_weight_sql = "select b.product_volume,b.product_weight " \
                                   "from commodity_information a join product_message b " \
                                   "on a.product_code=b.product_code where a.sku='%s';" \
                                   % spu_sku_avg[i][1]
        select_volume_weight_res = conf_fun.connect_mysql_operation(sql_text=select_volume_weight_sql)
        new_volume = 0
        new_weight = 0
        if len(select_volume_weight_res) > 0:
            new_volume = float(select_volume_weight_res[0][0]) if select_volume_weight_res[0][0] else 0
            new_weight = float(select_volume_weight_res[0][1]) if select_volume_weight_res[0][1] else 0
        spu_sku_avg[i].append(new_volume * spu_sku_avg[i][6])
        spu_sku_avg[i].append(new_weight * spu_sku_avg[i][6])
    return spu_sku_avg


# 根据传入的渠道/国家/站点/类型获取满足要求的所有在售的sku
def get_sku(platform, country, site, product_type):
    select_commodity_information_sql = "select a.sku,a.spu,b.product_package_size,b.product_weight " \
                                       "from commodity_information a join product_message b " \
                                       "on a.product_code=b.product_code " \
                                       "where a.platform='%s' and a.country='%s' " \
                                       "and a.site='%s' and b.product_state='在售' and product_type='%s';" \
                                       % (platform, country, site, product_type)
    sku_tup = conf_fun.connect_mysql_operation(sql_text=select_commodity_information_sql)
    print("根据传入的渠道国家站点获取满足要求的所有在售的sku: ", sku_tup)
    return sku_tup


# 库存管理-库存测算2.0版本
def calculate_inventory(request):
    print("================================库存管理-库存测算2.0版本: ", request.GET)
    # ==========================================
    # 接收的参数
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")

    # ==========================================
    # 验证状态是否被记录
    # 在途天数onload_day_number(装柜天数/海运周期),补后可售天数onload_day_number,补后售空日期replenish_sell_out_date
    select_have_variable_sql = "select * from calculate_inventory_variable " \
                               "where platform='%s' and country='%s' and site='%s' and sku is NULL;" \
                               % (platform, country, site)
    select_have_variable_res = conf_fun.connect_mysql_operation(sql_text=select_have_variable_sql)
    print("该版面的保存公共状态: ", select_have_variable_res)
    if len(select_have_variable_res) > 0:
        # 在途天数拆分为装柜天数/海运周期
        delivery_day = select_have_variable_res[0][4] if select_have_variable_res[0][4] else 14
        shop_name = site + country
        select_avg_shipping_cycle_sql = "select avg(shipping_cycle) from cargo_num_retrieval where shop_name='%s' " \
                                        "group by shop_name;" % shop_name
        select_avg_shipping_cycle_res = conf_fun.connect_mysql_re(sql_text=select_avg_shipping_cycle_sql)
        shipping_cycle = select_have_variable_res[0][5] \
            if select_have_variable_res[0][5] else select_avg_shipping_cycle_res[0][0]
        onload_day_number = math.ceil(float(delivery_day) + float(shipping_cycle))
        # 补后售空日期
        replenish_sell_out_date = select_have_variable_res[0][7] \
            if select_have_variable_res[0][7] else dt.datetime.strftime(
            dt.datetime.today() + dt.timedelta(
                days=45), "%Y-%m-%d")
    else:
        # 在途天数拆分为装柜天数/海运周期
        shop_name = site + country
        select_avg_shipping_cycle_sql = "select avg(shipping_cycle) from cargo_num_retrieval where shop_name='%s' " \
                                        "group by shop_name;" % shop_name
        select_avg_shipping_cycle_res = conf_fun.connect_mysql_re(sql_text=select_avg_shipping_cycle_sql)
        if len(select_avg_shipping_cycle_res) > 0:
            onload_day_number = 14 + math.ceil(float(select_avg_shipping_cycle_res[0][0]))
        else:
            onload_day_number = 14
        # 补后售空日期
        replenish_sell_out_date = dt.datetime.strftime(
            dt.datetime.today() + dt.timedelta(
                days=45), "%Y-%m-%d")

    # ==========================================
    # 获得满足平台/国家/站点/类型的在售spu
    spu_sku_avg = []
    spu_tup = get_spu(platform, country, site, product_type)
    for single_spu in spu_tup:
        sku_tup = get_sku_for_spu(single_spu)
        # ==========================================
        # 获得一个spu用来计算平均销量的列表[[第一个sku的],[]]
        sales_list = get_sales_list(sku_tup)
        print("====================")
        for i in range(len(sku_tup)):
            if sum(sales_list[i]) != 0:
                spu_sku_avg.append([single_spu[0], sku_tup[i][0], get_max_avg(sales_list[i])])
            else:
                spu_sku_avg.append([single_spu[0], sku_tup[i][0], 0.01])
    # 得到满足平台/国家/站点/类型的在售spu的所有sku的spu_sku_avg = [[spu,sku,均单量],[]]
    # 生成[[spu,sku,库存,在途数量,均单量,售空日期,补货数量,体积,重量,补后售空日期],[]]

    # ==========================================
    # 生成[[库存数量，在途数量],[]]
    stock_onload = []
    for spu_sku_avg_item in spu_sku_avg:
        stock_onload.append(calculated_inventory_total(spu_sku_avg_item[1]))
    # ==========================================
    # 生成[售空日期, ],spu_sku_avg, stock_onload
    sell_out_date = get_sell_out_date(spu_sku_avg, stock_onload)
    # ==========================================
    # 生成[补货数量, ],spu_sku_avg, onload_day_number, replenish_sell_out_date
    supply_num = get_supply_num(spu_sku_avg, onload_day_number, replenish_sell_out_date, sell_out_date)
    # ==========================================
    # 生成第一版数据[[spu,sku,库存,在途数量,均单量,售空日期,补货数量],[]]
    middle_data = []
    for i in range(len(spu_sku_avg)):
        middle_data.append([spu_sku_avg[i][0], spu_sku_avg[i][1], stock_onload[i][0], stock_onload[i][1],
                            spu_sku_avg[i][2], sell_out_date[i], supply_num[i]])
    # ==========================================
    # 求出第一版数据的[总体积,总重量],然后求出比例(总体积/限定体积 或 总重量/限定重量)
    total_volume_weight = get_max_ratio(middle_data)
    target_ratio = get_ratio(country, total_volume_weight, middle_data)
    # ==========================================
    # 现补货数量/该比例,整除以10,生成第二版补货数量
    spu_sku_avg = middle_data
    for i in range(len(spu_sku_avg)):
        if spu_sku_avg[i][6] > 30:
            spu_sku_avg[i][6] = ((spu_sku_avg[i][6] / target_ratio) // 10) * 10
        elif spu_sku_avg[i][6] > 0:
            spu_sku_avg[i][6] = 30
    # ==========================================
    # 计算对应体积，对应重量,如果补货数量为0,体积和重量都为0,并插入
    spu_sku_avg = append_volume_weight(spu_sku_avg)
    # ==========================================
    # 计算补后售空日期,如果补货量为0,补后售空日期等于售空日期,并插入
    for i in range(len(spu_sku_avg)):
        if spu_sku_avg[i][6] == 0:
            spu_sku_avg[i].append(spu_sku_avg[i][5])
        else:
            can_sell_day = int(spu_sku_avg[i][6] / spu_sku_avg[i][4])
            can_sell_date = dt.datetime.strftime(
                dt.datetime.strptime(spu_sku_avg[i][5], "%Y-%m-%d") + dt.timedelta(days=can_sell_day), "%Y-%m-%d")
            spu_sku_avg[i].append(can_sell_date)
    res = {"code": 200, "data": spu_sku_avg}
    return JsonResponse(res)

    # # ==========================================
    # # 获得满足平台/国家/站点的在售sku
    # sku_tup = get_sku(platform, country, site, product_type)
    # print("sku_tup: ", sku_tup)
    # for sku_item in sku_tup:
    #     print("================循环开始的地方")
    #     print("该条数据的sku: ", sku_item)
    #     # ==========================================
    #     # 获得该sku的fba+fbm
    #     overseas_number = calculated_inventory_total(sku_item[0])
    #     overseas_stock = float(overseas_number[0])
    #     print("该sku的仓库库存: ", overseas_stock)
    #     onload_number = overseas_number[1]
    #     print("该sku还在途的数量: ", onload_number)
    #
    #     # ==========================================
    #     # 获得该sku的均单量
    #     select_average_order_sql = "select * from calculate_inventory_variable " \
    #                                "where platform='%s' and country='%s' and site='%s' and sku='%s';" \
    #                                % (platform, country, site, sku_item[0])
    #     select_average_order_res = conf_fun.connect_mysql_operation(sql_text=select_average_order_sql)
    #     if len(select_average_order_res) > 0:
    #         average_order = float(select_average_order_res[0][9]) \
    #             if select_average_order_res[0][9] else float(calculated_average_order(sku_item[0]))
    #     else:
    #         average_order = float(calculated_average_order(sku_item[0]))
    #     if average_order == 0:
    #         average_order = 0.01
    #     print("该sku的均单量: ", average_order)
    #
    #     # ==========================================
    #     # 获得该sku的(fba+fbm)/均单量,得到售空天数1号
    #     sell_out_day_number_one = math.ceil(overseas_stock / average_order)
    #     print("该sku的售空天数1号: ", sell_out_day_number_one)
    #     sell_out_date_one = dt.datetime.strftime(dt.datetime.today() + dt.timedelta(
    #         days=sell_out_day_number_one), "%Y-%m-%d")
    #     print("该sku的售空日期1号: ", sell_out_date_one)
    #
    #     # ==========================================
    #     # 获得该sku的在途的列表[[预计到达时间, 数量], [预计到达时间, 数量]]
    #     on_load_sku_tup = on_load_container(sku_item[0])
    #
    #     # ==========================================
    #     # 根据该sku的在途的列表获得售空天数2号
    #     if len(on_load_sku_tup) > 0:
    #         sell_out_day_number_two = 0
    #         if on_load_sku_tup[-1][1] < sell_out_date_one:
    #             on_load_number_list = [float(x[0]) for x in on_load_sku_tup]
    #             sum_on_load = sum(on_load_number_list)
    #             sell_out_day_number_two = math.ceil(sum_on_load / average_order)
    #         else:
    #             for on_load_sku_item in on_load_sku_tup:
    #                 if on_load_sku_item[1] < sell_out_date_one:
    #                     # 存在误差
    #                     sell_out_day_number_two += math.ceil(float(on_load_sku_item[0]) / average_order)
    #                 else:
    #                     already_sell_out_day_number = (dt.datetime.strptime(
    #                         on_load_sku_item[1], "%Y-%m-%d") - dt.datetime.strptime(sell_out_date_one, "%Y-%m-%d")).days
    #                     sell_out_day_number_two += already_sell_out_day_number
    #                     sell_out_day_number_two += math.ceil(float(on_load_sku_item[0]) / average_order)
    #         print("该sku的售空天数2号: ", sell_out_day_number_two)
    #         sell_out_date_two = dt.datetime.strftime(
    #             dt.datetime.strptime(sell_out_date_one, "%Y-%m-%d") + dt.timedelta(
    #                 days=sell_out_day_number_two), "%Y-%m-%d")
    #     else:
    #         sell_out_date_two = sell_out_date_one
    #     print("该sku的售空日期2号: ", sell_out_date_two)
    #
    #     # ==========================================
    #     # 根据售空日期2号、在途天数、均单量、补后售空日期计算补货数量1号，在途天数=装柜天数（14）+ 海运周期
    #     # 售空日期2号->最终售空日期
    #     finally_sell_out_date = sell_out_date_two
    #
    #     now_replenish_arrival_date = dt.datetime.strftime(
    #         dt.datetime.today() + dt.timedelta(days=onload_day_number), "%Y-%m-%d")
    #     print("补后售空日期: ", replenish_sell_out_date)
    #     print("现在补货到达时间(今天加上在途总天数): ", now_replenish_arrival_date)
    #     print("比较两者计算补货量")
    #     if finally_sell_out_date <= now_replenish_arrival_date:
    #         print("小于或者等于")
    #         # 补后售空日期/售空日期，求出两者之间的天数，乘以均单量
    #         differ_day_number = (dt.datetime.strptime(
    #             replenish_sell_out_date, "%Y-%m-%d") - dt.datetime.strptime(
    #             finally_sell_out_date, "%Y-%m-%d")).days
    #         replenish_num = differ_day_number * average_order
    #         print("原补货数量: ", replenish_num)
    #         new_replenish_num = replenish_num // 10
    #         print("原补货数量整除以10: ", new_replenish_num)
    #         replenish_num = new_replenish_num * 10 + 10 if replenish_num != new_replenish_num else new_replenish_num
    #     else:
    #         print("大于")
    #         replenish_num = 0
    #     print("该sku的补货数量: ", replenish_num)
    #     # ==========================================
    #     # (装柜天数,海运周期,补后可售天数,补后可售日期)
    #     # data = [[spu,sku,仓库库存,在途数量,均单量,售空日期,补货数量,体积,重量,补后售空日期],[]]
    #     print("第一版数据: ", [sku_item[1], sku_item[0], overseas_stock, onload_number, round(average_order, 2),
    #                       sell_out_date_two, replenish_num if replenish_num > 30 else 0,
    #                       sku_item[2], sku_item[3], replenish_sell_out_date])
    #     data.append([sku_item[1], sku_item[0], overseas_stock, onload_number, round(average_order, 2),
    #                  sell_out_date_two, replenish_num if replenish_num > 30 else 0,
    #                  sku_item[2], sku_item[3], replenish_sell_out_date])
    #
    # # ==========================================
    # # 根据体积和重量计算补货数量2号
    # data = volume_weight(data, country)
    #
    # # ==========================================
    # # 根据新的补货数量计算显示的体积/重量/补后售空日期
    # for data_item in data:
    #     if data_item[6]:
    #         # 补货数量/均单量得到补后可售天数，然后售空日期+补后可售天数
    #         new_can_sell_day_number = math.ceil(data_item[6] / data_item[4])
    #         new_replenish_sell_out_date = dt.datetime.strftime(
    #             dt.datetime.strptime(data_item[5], "%Y-%m-%d") + dt.timedelta(
    #                 days=new_can_sell_day_number), "%Y-%m-%d")
    #         data_item[-1] = new_replenish_sell_out_date
    #
    #         if data_item[7]:
    #             data_item[7] = data_item[6] * float(data_item[7])
    #         if data_item[8]:
    #             data_item[8] = data_item[6] * float(data_item[8])
    #     else:
    #         data_item[7] = 0
    #         data_item[8] = 0
    #         data_item[-1] = data_item[5]
    #
    # # ==========================================
    # # 返回
    # res = {"code": 200, "data": data}
    # print("库存测算返回: ", res)
    # return JsonResponse(res)


# 库存管理-库存测算2.0版本-根据体积重量，调整补货数量
def volume_weight(data, country):
    volume_index = -1
    while True:
        volume = 0
        mark = 0
        for i in range(len(data)):
            if data[i][6] != 0:
                if data[i][7]:
                    volume += (float(data[i][7]) * data[i][6])
        if volume > 67:
            for j in range(len(data)):
                if data[j][6] != 0:
                    if data[j][7]:
                        if volume_index >= j:
                            continue
                        volume_index = j
                if j == (len(data) - 1):
                    mark = 1

            data[volume_index][6] -= 10
            if data[volume_index][6] < 30:
                data[volume_index][6] = 0
            if mark == 1:
                volume_index = -1
        else:
            break

    if country == "美国":
        weight_index = -1
        while True:
            weight = 0
            mark = 0
            for i in range(len(data)):
                if data[i][6] != 0:
                    if data[i][8]:
                        weight += (float(data[i][8]) * data[i][6])
            if weight > 19500:
                for j in range(len(data)):
                    if data[j][6] != 0:
                        if data[j][8]:
                            if weight_index >= j:
                                continue
                            weight_index = j
                    if j == (len(data) - 1):
                        mark = 1

                data[weight_index][6] -= 10
                if data[weight_index][6] < 30:
                    data[weight_index][6] = 0
                if mark == 1:
                    weight_index = -1
            else:
                break
    return data


# 库存管理-库存测算2.0版本-编辑
def update_variable(request):
    print("===========库存管理-库存测算2.0版本-编辑: ", request.POST)
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
                              "where platform='%s' and country='%s' and site='%s' " \
                              "and sku='%s' and product_type='%s';" \
                              % (platform, country, site, sku, product_type)
        print("select_distinct_sql: ", select_distinct_sql)
        select_distinct_res = conf_fun.connect_mysql_operation(sql_text=select_distinct_sql)
        print("select_distinct_res: ", select_distinct_res)
        if len(select_distinct_res) > 0:
            update_variable_sql = "update calculate_inventory_variable " \
                                  "set average_order='%s',replenish_num='%s' " \
                                  "where platform='%s' and country='%s' and site='%s' " \
                                  "and sku='%s' and product_type='%s';" \
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
                              "where platform='%s' and country='%s' and site='%s' " \
                              "and (sku is NULL or sku='') and product_type='%s';" \
                              % (platform, country, site, product_type)
        print("select_distinct_sql: ", select_distinct_sql)
        select_distinct_res = conf_fun.connect_mysql_operation(sql_text=select_distinct_sql)
        print("select_distinct_res: ", select_distinct_res)
        if len(select_distinct_res) > 0:
            update_variable_sql = "update calculate_inventory_variable " \
                                  "set delivery_day='%s',shipping_cycle='%s'," \
                                  "replenish_can_sell_day_number='%s',replenish_can_sell_date='%s' " \
                                  "where platform='%s' and country='%s' and site='%s' " \
                                  "and (sku is NULL or sku='') and product_type='%s';" \
                                  % (delivery_day, shipping_cycle, replenish_can_sell_day_number,
                                     replenish_can_sell_date, platform, country, site, product_type)
            print("update_variable_sql: ", update_variable_sql)
            conf_fun.connect_mysql_operation(sql_text=update_variable_sql)
        else:
            insert_variable_sql = "insert into calculate_inventory_variable" \
                                  "(platform,country,site,product_type,delivery_day,shipping_cycle," \
                                  "replenish_can_sell_day_number,replenish_can_sell_date) " \
                                  "values('%s','%s','%s','%s','%s','%s','%s','%s');" \
                                  % (platform, country, site, product_type, delivery_day, shipping_cycle,
                                     replenish_can_sell_day_number, replenish_can_sell_date)
            print("insert_variable_sql: ", insert_variable_sql)
            conf_fun.connect_mysql_operation(sql_text=insert_variable_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 库存管理-库存测算2.0版本-获取公共数据
def get_public_data(request):
    print("========库存管理-库存测算2.0版本-获取公共数据: ", request.GET)
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")

    select_sql = "select delivery_day,shipping_cycle,replenish_can_sell_day_number " \
                 "from calculate_inventory_variable " \
                 "where platform='%s' and country='%s' and site='%s' " \
                 "and (sku='' or sku is NULL) and product_type='%s';" \
                 % (platform, country, site, product_type)
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    print("select_res: ", select_res)
    # ============================
    shop_name = site + country
    select_avg_shipping_cycle_sql = "select avg(shipping_cycle) from cargo_num_retrieval where shop_name='%s' " \
                                    "group by shop_name;" % shop_name
    print("select_avg_shipping_cycle_sql: ", select_avg_shipping_cycle_sql)
    select_avg_shipping_cycle_res = conf_fun.connect_mysql_re(sql_text=select_avg_shipping_cycle_sql)
    print("select_avg_shipping_cycle_res: ", select_avg_shipping_cycle_res)

    if len(select_res) > 0:
        delivery_day = select_res[0][0] if select_res[0][0] else 14

        shipping_cycle = select_res[0][1] if select_res[0][1] else select_avg_shipping_cycle_res[0][0]

        replenish_can_sell_day_number = select_res[0][2] if select_res[0][2] else 45
    else:
        delivery_day = 14
        if select_avg_shipping_cycle_res:
            shipping_cycle = select_avg_shipping_cycle_res[0][0]
        else:
            shipping_cycle = 45
        replenish_can_sell_day_number = 45

    res = {"code": 200, "data": [delivery_day, math.ceil(float(shipping_cycle)),
                                 replenish_can_sell_day_number]}
    return JsonResponse(res)


# 库存管理-库存测算1.0版本
def calculated_inventory(request):
    print("===============库存管理-库存测算(打开页面时，没有输入均单量、补货数量):", request.GET)
    data = []
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    on_load_day = request.GET.get("aog_number", "")
    if not on_load_day:
        on_load_day = "14"
    print("on_load_day: ", on_load_day)

    # 对象有sku/均单量average_order/补后可售天数replenish_sell_out_day
    edit_average_order = request.GET.get("edit_average_order", "")
    if edit_average_order:
        edit_average_order = eval(edit_average_order)
    print("edit_average_order: ", edit_average_order)

    # 根据传入的渠道国家站点获取满足要求的所有在售的sku
    sku_tup = get_sku(platform, country, site)
    # =============================
    # 根据sku获取其预计均单量、库存总量、预计售空日期、预计补后售空日期、建议补货数量
    for tup_item in sku_tup:
        # =============================
        # 获取该sku的预计均单量average_order
        if edit_average_order and edit_average_order["sku"] == tup_item[0]:
            if edit_average_order["average_order"]:
                average_order = edit_average_order["average_order"]
            else:
                average_order = calculated_average_order(tup_item[0])
            if edit_average_order["replenish_sell_out_day"]:
                replenish_sell_out_day = edit_average_order["replenish_sell_out_day"]
            else:
                replenish_sell_out_day = 45
        else:
            # 均单量
            average_order = calculated_average_order(tup_item[0])
            # 补后售空天数
            replenish_sell_out_day = 45
        print("计算得到的均单量average_order：", average_order)
        if average_order == "0":
            average_order = 0.1

        # 海外库存总量inventory_total、在途总量on_load_total
        calculated_inventory_total_res = calculated_inventory_total(tup_item[0])
        inventory_total = calculated_inventory_total_res[0]
        on_load_total = calculated_inventory_total_res[1]
        print("海外库存总量inventory_total：", inventory_total)
        print("在途总量on_load_total：", on_load_total)

        # 预计售空日期sell_out_date
        print("日均量： ", average_order)
        print("inventory_total + on_load_total: ", inventory_total + on_load_total)
        if (inventory_total + on_load_total) == 0:
            print("日均量或海外库存为零")
            can_sell_day = 0
            sell_out_date = dt.datetime.strftime(dt.datetime.today(), "%Y-%m-%d")
        else:
            can_sell_day = math.ceil((inventory_total + on_load_total) / float(average_order))
            sell_out_date = dt.datetime.strftime(
                dt.datetime.today() + dt.timedelta(
                    days=(math.ceil((inventory_total + on_load_total) / float(average_order)))
                ), "%Y-%m-%d"
            )
        print("预计售空日期sell_out_date: ", sell_out_date)
        # =============================
        # 预计售空日期和当天的天数差值
        available_day = (dt.datetime.strptime(sell_out_date, "%Y-%m-%d") - dt.datetime.today()).days
        if available_day < 0:
            available_day = 0
        print("预计售空日期和当天的天数差值: ", available_day)
        # =============================
        # 建议补货数量(如果预计售空日期和当天的天数差值小于等于在途天数，补充日均量的补后售空天数倍)
        if available_day <= int(on_load_day):
            print("需要建议补货了")
            replenish_number = math.ceil(float(average_order) * (int(replenish_sell_out_day) - can_sell_day))
        else:
            replenish_number = "0"

        small_list = []
        # spu
        small_list.append(tup_item[1])
        # sku
        small_list.append(tup_item[0])
        # 库存
        small_list.append(str(inventory_total + on_load_total))
        # 均单量
        small_list.append(average_order)
        # 预计售空日期
        small_list.append(sell_out_date)
        # 建议补货数量
        if average_order != 0.1:
            small_list.append(replenish_number)
        else:
            small_list.append(0.0)
        # 体积/立方、重量
        small_list.extend(tup_item[2:4])
        # 预计补后可售天数
        if int(replenish_number) > 0:
            small_list.append(replenish_sell_out_day)
        else:
            small_list.append(replenish_sell_out_day)

        # ===================
        data.append(small_list)

    # 以上为测算出的第一版数据data
    """
    先判断是不是美国
    再判断具体状态（体积太小重量未超标、体积太小重量超标、体积正常重量超标，体积太大重量未超标、体积太大重量超标）（体积、重量）
    体积不合格：将体积最大的补货数量减一，然后体积第二大的补货数量减一，直至体积合格
    重量不合格：将重量最大的补货数量减一，然后重量第二大的补货数量减一，直至重量合格
    补货数量变了，补后可售天数跟着变化
    """
    # 判断体积合不合格
    while True:
        volume = 0
        volume_index = 0
        for i in range(len(data)):
            data[i][5] = int(data[i][5])
            data[i][6] = float(data[i][6])
            if data[i][5] > 0:
                volume += (data[i][6] * data[i][5])
            if float(data[volume_index][6]) < data[i][6]:
                volume_index = i
        if volume > 67:
            data[volume_index][5] -= 1
        else:
            break
    # 判断是不是美国，是美国需再判断重量合不合格,19.5吨=19500kg
    if country == "美国":
        while True:
            weight = 0
            weight_index = 0
            for i in range(len(data)):
                data[i][5] = int(data[i][5])
                data[i][7] = float(data[i][6])
                if data[i][5] > 0:
                    weight += (data[i][7] * data[i][5])
                if data[weight_index][7] < data[i][7]:
                    weight_index = i
            if weight > 19500:
                data[weight_index][5] -= 1
            else:
                break

    res = {"code": 200, "data": data, "day": on_load_day}
    return JsonResponse(res)


# 库存管理-库存监控
def monitor_inventory(request):
    """
    选择渠道，国家，站点后，获取其在售的sku，计算所有的库存量，和在途的所有货柜，计算每个sku在货柜中的数量，
    然后计算在途总量，计算合计量，均单量，再计算预计售空日期，根据售空日期和当天的天数差，
    <30库存不足，30-90正常,（>90或（日均量为零而库存总计不为零））库存冗余
    """
    print("===============库存管理-库存监控:", request.GET)
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")

    res_data = []

    # 根据传入的渠道国家站点获取满足要求的所有在售的sku
    select_commodity_information_sql = "select a.sku,a.spu " \
                                       "from commodity_information a join product_message b " \
                                       "on a.product_code=b.product_code " \
                                       "where a.platform='%s' and a.country='%s' " \
                                       "and a.site='%s' and b.product_state='在售' and b.product_type='%s';" \
                                       % (platform, country, site, product_type)
    print("select_commodity_information_sql: ", select_commodity_information_sql)
    sku_tup = conf_fun.connect_mysql_operation(sql_text=select_commodity_information_sql)
    print("sku_tup: ", sku_tup)

    # 在途的所有货柜
    select_container_sql = "select container_no from arrival_receive " \
                           "where (receive_count='' or receive_count is NULL);"
    print("select_container_sql: ", select_container_sql)
    select_container_res = conf_fun.connect_mysql_product_supplier(sql_text=select_container_sql)
    print("select_container_res: ", select_container_res)
    if len(select_container_res) > 0:
        on_load_container_list = [x[0] for x in select_container_res]
    else:
        on_load_container_list = []
    print("on_load_container_list: ", on_load_container_list)

    # 满足条件的在售的每一个sku
    for tup_item in sku_tup:
        # 组织返回的spu,sku
        small_list = list()
        small_list.append(tup_item[1])
        small_list.append(tup_item[0])
        # 海外库存总量inventory_total、在途总量on_load_total
        calculated_inventory_total_res = calculated_inventory_total(tup_item[0])
        inventory_total = calculated_inventory_total_res[0]
        on_load_total = calculated_inventory_total_res[1]
        print("海外库存总量inventory_total: ", inventory_total, "在途总量on_load_total: ", on_load_total)
        # 组织返回的海外库存数量
        small_list.append(inventory_total)

        # 该sku在所有在途货柜中的数量
        if len(on_load_container_list) > 0:
            for container in on_load_container_list:
                select_cargo_information_sql = "select cargo_num from cargo_information " \
                                               "where sku='%s' and container_num='%s';" \
                                               % (tup_item[0], container)
                print("select_cargo_information_sql: ", select_cargo_information_sql)
                select_cargo_information_res = conf_fun.connect_mysql_product_supplier(sql_text=select_cargo_information_sql)
                print("select_cargo_information_res: ", select_cargo_information_res)
                # 组织返回的目标在途货柜内的该sku数量
                if len(select_cargo_information_res) > 0:
                    small_list.append(select_cargo_information_res[0][0])
                else:
                    small_list.append(0)
        else:
            pass

        # 组织返回的在途数量
        small_list.append(on_load_total)
        # 组织返回的海外库存和在途数量合计
        small_list.append(inventory_total + on_load_total)

        # 计算该sku的均单量
        average_order = calculated_average_order(tup_item[0])
        if average_order == 0:
            average_order = 0.1
        print("average_order==: ", average_order)
        # 组织返回的均单量
        small_list.append(average_order)

        # 计算售空日期
        if (inventory_total + on_load_total) == 0:
            sell_out_day = "已售空"
            sell_out_day_number = 0
        else:
            sell_out_day_number = math.ceil((inventory_total + on_load_total) / float(average_order))
            sell_out_day = dt.datetime.strftime(
                dt.datetime.today() + dt.timedelta(days=sell_out_day_number), "%Y/%m/%d")
        # 组织返回的售空日期
        small_list.append(sell_out_day)

        # 组织返回的提示
        if sell_out_day_number < 30:
            if average_order == 0.01:
                small_list.append("正常")
            else:
                small_list.append("库存不足")
        elif sell_out_day_number < 90:
            small_list.append("正常")
        else:
            small_list.append("库存冗余")

        res_data.append(small_list)

    res = {"code": 200, "table_data": res_data, "header": on_load_container_list}
    return JsonResponse(res)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++邪恶的分割线


# 库存管理-订单需求-生成
def insert_order_request(request):
    print("")
    print("==================库存管理-订单需求:", request.POST)
    print("")
    platform = request.POST.get("platform", "")
    country = request.POST.get("country", "")
    site = request.POST.get("site", "")
    container = request.POST.get("container", "")
    receive_data = eval(request.POST.get("receive_data", ""))

    print("receive_data: ", receive_data)
    print("receive_data类型: ", type(receive_data))

    delivery_date = request.POST.get("delivery_date", "")
    warehouse_type = request.POST.get("warehouse_type", "")
    # warehouse_code = request.POST.get("warehouse_code", "")
    warehouse_name = request.POST.get("warehouse_name", "")
    # destination_port = request.POST.get("destination_port", "")

    print("delivery_date: ", delivery_date)
    # 月份
    delivery_month = delivery_date[:7]
    # 时段
    delivery_day = delivery_date[8:]
    if int(delivery_day) < 11:
        delivery_frame = "上旬"
    elif int(delivery_day) < 21:
        delivery_frame = "中旬"
    else:
        delivery_frame = "下旬"

    print("delivery_month: ", delivery_month)
    print("delivery_frame: ", delivery_frame)

    for item in receive_data:
        # 根据sku获取产品类型、货号、品名
        select_sql = "select b.product_type,b.product_code,b.product_name " \
                     "from commodity_information a join product_message b " \
                     "on a.product_code=b.product_code where a.sku='%s';" \
                     % item["sku"]
        print("select_sql: ", select_sql)
        select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
        print("select_res: ", select_res)

        insert_sql = "insert into order_request(delivery_month,delivery_frame,platform," \
                     "site,country,container,warehouse_type,warehouse_code,warehouse_name," \
                     "destination_port,product_type,product_code,product_name," \
                     "product_number,delivery_date) values('%s', '%s', '%s', '%s', '%s', '%s', " \
                     "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (delivery_month, delivery_frame, platform, site, country, container, warehouse_type,
                        warehouse_code, warehouse_name, destination_port, select_res[0][0],
                        select_res[0][1], select_res[0][2], item["num"], delivery_date)
        print("insert_sql: ", insert_sql)
        conf_fun.connect_mysql_operation(sql_text=insert_sql)

    res = {"code": 200}
    return JsonResponse(res)


# 库存管理-订单需求-查询
def select_order_request(request):
    print("")
    print("==================库存管理-订单需求-查询:", request.GET)
    print("")
    platform = request.GET.get("platform", "")
    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    delivery_date = request.GET.get("delivery_date", "")
    delivery_month = request.GET.get("delivery_month", "")
    delivery_frame = request.GET.get("delivery_frame", "")
    product_type = request.GET.get("product_type", "")
    product_code = request.GET.get("product_code", "")
    product_name = request.GET.get("product_name", "")
    warehouse_type = request.GET.get("warehouse_type", "")
    warehouse_name = request.GET.get("warehouse_name", "")
    destination_port = request.GET.get("destination_port", "")

    select_sql = "select * from order_request where platform='%s' and country='%s' and site='%s'" \
                 % (platform, country, site)
    if delivery_date:
        select_sql += " and receive_date='" + delivery_date + "'"
    if delivery_month:
        select_sql += " and delivery_month='" + delivery_month + "'"
    if delivery_frame:
        select_sql += " and delivery_frame='" + delivery_frame + "'"
    if product_type:
        select_sql += " and product_type='" + product_type + "'"
    if product_code:
        select_sql += " and product_code='" + product_code + "'"
    if product_name:
        select_sql += " and product_name='" + product_name + "'"
    if warehouse_type:
        select_sql += " and warehouse_type='" + warehouse_type + "'"
    if warehouse_name:
        select_sql += " and warehouse_name='" + warehouse_name + "'"
    if destination_port:
        select_sql += " and destination_port='" + destination_port + "'"
    select_sql += ";"
    print(1163,'\n',select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)

    if len(select_res) > 0:
        res = {"code": 200, "data": select_res}
    else:
        res = {"code": 4041, "msg": "没有符合条件的数据!"}
    return JsonResponse(res)
