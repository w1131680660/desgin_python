import pymysql
from urllib.parse import unquote
from django.http import JsonResponse
from settings import conf_fun

# # 连接总数据库的运营数据库
# def connect_mysql(sql_text, dbs='operation', type='tuple'):
#     conn = pymysql.Connect(
#         host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_', db=dbs)
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


# 货柜检索 获取侧边栏 / 按sku货柜检索 获取侧边栏
def get_sidebar_select_container(request):
    """国家、站点、货物类型、仓库类型、仓库名称、货柜号"""
    print("\n", "货柜检索 获取侧边栏", "\n")

    country_list = list()
    site_list = list()
    product_type_list = list()
    warehouse_type_list = list()
    warehouse_name_list = list()
    container_list = list()
    sku_list = list()

    # 查询所有在售的商品类型不为空的商品信息
    select_commodity_sql = "select * from commodity_information " \
                           "where commodity_state!='停售' and category is not NULL;"
    print("查询所有在售的商品类型不为空的商品信息", select_commodity_sql)
    select_commodity_res = conf_fun.connect_mysql_operation(sql_text=select_commodity_sql, type='dict')
    for select_commodity_res_item in select_commodity_res:
        # 获取所有商品类型列表
        if select_commodity_res_item['category'] not in product_type_list:
            product_type_list.append(select_commodity_res_item['category'])
    # 查询所有仓库信息
    select_warehouse_sql = "select * from warehouse;"
    select_warehouse_res = conf_fun.connect_mysql_operation(sql_text=select_warehouse_sql, type='dict')
    for select_warehouse_res_item in select_warehouse_res:
        # 获取所有仓库类型
        if select_warehouse_res_item['warehouse_type'] not in warehouse_type_list:
            warehouse_type_list.append(select_warehouse_res_item['warehouse_type'])
        # 获取所有仓库名字
        if select_warehouse_res_item['warehouse_name'] not in warehouse_name_list:
            warehouse_name_list.append(select_warehouse_res_item['warehouse_name'])

    print("=============")
    print(unquote(request.META.get('HTTP_AUTHORIZATION')))
    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    allow_site = user_info.split("@")[1]
    print("=============")
    # user_token = request.session.get("user_name", None)
    # select_userinfo_sql = "select * from userinfo where token='%s';" % user_token
    # print("获取登录用户分配站点", select_userinfo_sql)
    # select_userinfo_res = conf_fun.connect_mysql_operation(sql_text=select_userinfo_sql, type='dict')

    # 按照分配站点权限控制显示范围
    if allow_site == "all":
        # 查询所有在售店铺信息
        select_country_sql = "select * from store_information where state='在售';"
        print("查询所有在售的店铺信息", select_country_sql)
        select_country_res = conf_fun.connect_mysql_operation(sql_text=select_country_sql, type='dict')
        for select_country_res_item in select_country_res:
            # 获取所有国家列表
            if select_country_res_item['country'] not in country_list:
                country_list.append(select_country_res_item['country'])
            # 获取所有站点列表
            if select_country_res_item['site'] not in site_list:
                site_list.append(select_country_res_item['site'])
        # 获取所有的货柜号
        select_container_sql = "select * from schedule_container order by container_num desc;"
        print("获取所有的货柜号", select_container_sql)
        select_container_res = conf_fun.connect_mysql_operation(sql_text=select_container_sql, type='dict')
        for select_container_res_item in select_container_res:
            if select_container_res_item['container_num'] not in container_list:
                container_list.append(select_container_res_item['container_num'])
        # 获取所有sku
        select_sku_sql = "select * from commodity_information where commodity_state!='停售';"
        print("获取所有sku", select_sku_sql)
        select_sku_res = conf_fun.connect_mysql_operation(sql_text=select_sku_sql, dbs='operation', type='dict')
        for select_sku_res_item in select_sku_res:
            if select_sku_res_item['sku'] not in sku_list:
                sku_list.append(select_sku_res_item['sku'])

    else:
        # 获得权限范围之内的国家和站点
        site_country_list = [x for x in allow_site.split(",")]
        country_list = [x.split("_")[1] for x in site_country_list]
        country_list = list(set(country_list))
        print("获得权限范围之内的国家", country_list)
        site_list = [x.split("_")[0] for x in site_country_list]
        site_list = list(set(site_list))
        print("获得权限范围之内的站点", site_list)

        # 获得权限范围之内的柜号
        select_container_sql = "select * from schedule_container where id!=''"
        if len(country_list) > 1:
            select_container_sql += " and country in %s" % str(tuple(country_list))
        elif len(country_list) == 1:
            select_container_sql += " and country='%s'" % country_list[0]
        else:
            select_container_sql += " and country=''"
        if len(site_list) > 1:
            select_container_sql += " and (site in %s" % str(tuple(site_list))
            for site_list_item in site_list:
                select_container_sql += " or '%s' in container_data" % site_list_item
        elif len(site_list) == 1:
            select_container_sql += " and (site='%s' or '%s' in container_data" % (site_list[0], site_list[0])
        else:
            select_container_sql += " and site=''"
        print("获得权限范围之内的柜号", select_container_sql)
        select_container_res = conf_fun.connect_mysql_operation(sql_text=select_container_sql, type='dict')
        for select_container_res_item in select_container_res:
            if select_container_res_item['container_num'] not in container_list:
                container_list.append(select_container_res_item['container_num'])
        # 获得权限范围之内的sku
        select_sku_sql = "select * from commodity_information where country in %s and site in %s;" \
                         % (str(tuple(country_list)), str(tuple(site_list)))
        select_sku_res = conf_fun.connect_mysql_operation(sql_text=select_sku_sql, dbs='operation', type='dict')

        for select_sku_res_item in select_sku_res:
            if select_sku_res_item['sku'] not in sku_list:
                sku_list.append(select_sku_res_item['sku'])

    res = {"code": 200, "country_list": country_list, "site_list": site_list,
           "product_type_list": product_type_list, "warehouse_type_list": warehouse_type_list,
           "warehouse_name_list": warehouse_name_list, "container_list": container_list,
           "sku_list": sku_list}
    return JsonResponse(res)


# 货柜检索 查询
def select_container(request):
    print("\n", "货柜检索 查询", "\n")
    print(request.GET)

    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")
    warehouse_type = request.GET.get("warehouse_type", "")
    warehouse_name = request.GET.get("warehouse_name", "")
    container = request.GET.get("container", "")
    page = int(request.GET.get("page", "1"))

    select_sql = "select * from schedule_container where id!=''"
    if country:
        select_sql += " and country='%s'" % country
    if site:
        select_sql += " and site='%s'" % site
    if warehouse_type:
        select_sql += " and warehouse_type='%s'" % warehouse_type
    if warehouse_name:
        select_sql += " and warehouse_name='%s'" % warehouse_name
    if container:
        select_sql += " and container_num='%s'" % container
    if product_type:
        factory_list = list()
        if product_type == "钢木":
            select_factory_sql = "select * from supplier where types='gm';"
        else:
            select_factory_sql = "select * from supplier where types='mp';"
        select_factory_res = conf_fun.connect_mysql_operation(sql_text=select_factory_sql, dbs='supply_chain', type='dict')
        for select_factory_res_item in select_factory_res:
            if select_factory_res_item['supplier'] not in factory_list:
                factory_list.append(select_factory_res_item['supplier'])
        if len(factory_list) > 1:
            select_sql += " and factory in %s" % str(tuple(factory_list))
        elif len(factory_list) == 1:
            select_sql += " and factory='%s'" % factory_list[0]
        else:
            select_sql += " and factory=''"
    select_sql += "order by container_num desc;"
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, dbs='operation', type='dict')

    # 获取总行数&分页
    data = list()
    mark_list = list()
    start_row = page * 50 - 50
    end_row = page * 50
    all_row = 0

    for select_res_item in select_res:
        if start_row <= all_row < end_row:
            if select_res_item['container_num'] not in mark_list:
                data.append(select_res_item)
                mark_list.append(select_res_item['container_num'])
                all_row += 1
            else:
                data.append(select_res_item)
        else:
            all_row += 1

    # 获取所有货柜号
    all_container_list = list()
    for select_res_item in data:
        if select_res_item['container_num'] not in all_container_list:
            all_container_list.append(select_res_item['container_num'])

    # 单个货柜有多少个工厂
    if len(all_container_list) > 1:
        select_number_sql = "select container_num,count(id) from operating_data " \
                            "where container_num in %s group by container_num;" \
                            % str(tuple(all_container_list))
    elif len(all_container_list) == 1:
        select_number_sql = "select container_num,count(id) from operating_data " \
                            "where container_num='%s' group by container_num;" \
                            % all_container_list[0]
    else:
        select_number_sql = "select container_num,count(id) from operating_data " \
                            "where container_num='' group by container_num;"
    select_number_res = conf_fun.connect_mysql_operation(sql_text=select_number_sql, dbs='operation', type='dict')

    # 获取出库单数据
    if len(all_container_list) > 1:
        select_delivery_sql = "select * from delivery where delivery_container in %s;" % str(tuple(all_container_list))
    elif len(all_container_list) == 1:
        select_delivery_sql = "select * from delivery where delivery_container='%s';" % all_container_list[0]
    else:
        select_delivery_sql = "select * from delivery where delivery_container='';"
    print("获取出库单数据: ", select_delivery_sql)
    select_delivery_res = conf_fun.connect_mysql_operation(sql_text=select_delivery_sql, dbs='supply_chain', type='dict')

    # 获取接收数据
    if len(all_container_list) > 1:
        select_receive_sql = "select * from arrival_receive where container in %s;" % str(tuple(all_container_list))
    elif len(all_container_list) == 1:
        select_receive_sql = "select * from arrival_receive where container='%s';" % all_container_list[0]
    else:
        select_receive_sql = "select * from arrival_receive where container='';"
    print("获取接收数据: ", select_receive_sql)
    select_receive_res = conf_fun.connect_mysql_operation(sql_text=select_receive_sql, dbs='product_supplier', type='dict')

    select_factory_res = ""
    if not product_type:
        select_factory_sql = "select * from supplier;"
        select_factory_res = conf_fun.connect_mysql_operation(sql_text=select_factory_sql, dbs='supply_chain', type='dict')

    res = {"code": 200, "data": data, "select_delivery_res": select_delivery_res,
           "select_receive_res": select_receive_res, "select_factory_res": select_factory_res,
           "all_row": all_row, "select_number_res": select_number_res}
    return JsonResponse(res)


# 按sku货柜检索 查询
def select_container_by_sku_old(request):
    print("\n", "按sku货柜检索 查询", "\n")
    print("参数: ", request.GET)

    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")
    sku = request.GET.get("sku", "")
    page = int(request.GET.get("page", "1"))

    # 查询所有满足条件的数据
    select_sql = "select * from order_distribution od join delivery d " \
                 "on od.container_code=d.delivery_container and od.factory=d.delivery_supplier " \
                 "join product_supplier.arrival_receive ar on ar.container=od.container_code " \
                 "and ar.country=od.country and ar.store=od.store " \
                 "where od.id!=''"
    if country:
        select_sql += " and od.country='%s'" % country
    if site:
        select_sql += " and od.store='%s'" % site
    if product_type:
        select_sql += " and od.product_type='%s'" % product_type
    if sku:
        select_product_code_sql = "select * from commodity_information where sku='%s';" % sku
        select_product_code_res = conf_fun.connect_mysql_operation(sql_text=select_product_code_sql, dbs='operation', type='dict')
        select_sql += " and od.product_number='%s'" % select_product_code_res[0]['sku']

    select_sql += "order by container_code desc;"
    print("查询", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql, dbs='supply_chain', type='dict')

    mark_list = list()
    all_row = 0
    start_row = (page * 50) - 50
    end_row = (page * 50)
    data = list()

    # 分页
    for select_res_item in select_res:
        if start_row <= all_row < end_row:
            if [select_res_item['sku'], select_res_item['container_code']] not in mark_list:
                data.append(select_res_item)
                mark_list.append([select_res_item['sku'], select_res_item['container_code']])
                all_row += 1
            else:
                # data.append(select_res_item)
                pass
        else:
            all_row += 1

    all_product_code = list()
    all_container = list()
    # 获取所有的货号 / 获取所有的货柜号
    for data_item in data:
        if data_item['product_number'] not in all_product_code:
            all_product_code.append(data_item['product_number'])
        if data_item['container_code'] not in all_container:
            all_container.append(data_item['container_code'])

    # 获取货号对应的sku
    if len(all_product_code) > 1:
        select_sku_sql = "select * from commodity_information where product_code in %s;" % str(tuple(all_product_code))
    elif len(all_product_code) == 1:
        select_sku_sql = "select * from commodity_information where product_code='%s';" % all_product_code[0]
    else:
        select_sku_sql = "select * from commodity_information where product_code='';"
    select_sku_res = conf_fun.connect_mysql_operation(sql_text=select_sku_sql, dbs='operation', type='dict')

    # 获取货柜号的仓库信息
    if len(all_container) > 1:
        select_container_sql = "select * from schedule_container where container_num in %s;" % str(tuple(all_container))
    elif len(all_container) == 1:
        select_container_sql = "select * from schedule_container where container_num='%s';" % all_container[0]
    else:
        select_container_sql = "select * from schedule_container where container_num='';"
    select_container_res = conf_fun.connect_mysql_operation(sql_text=select_container_sql, dbs='operation', type='dict')

    res = {"code": 200, "data": data, "all_row": all_row,
           "sku_object": select_sku_res, "container_object": select_container_res}
    return JsonResponse(res)


# 按sku货柜检索 查询2.0
def select_container_by_sku(request):
    print("\n", "按sku货柜检索 查询", "\n")
    print(request.GET)

    country = request.GET.get("country", "")
    site = request.GET.get("site", "")
    product_type = request.GET.get("product_type", "")
    sku = request.GET.get("sku", "")
    page = int(request.GET.get("page", "1"))

    select_sql = "select * from order_integrate where id!=''"
    if country:
        select_sql += " and country='%s'" % country
    if site:
        select_sql += " and store='%s'" % site
    if product_type:
        select_sql += " and product_type='%s'" % product_type
    if sku:
        select_sql += " and sku='%s'" % sku
    select_sql += " order by container_code desc;"
    select_res = conf_fun.connect_mysql_operation(select_sql, "supply_chain", "dict")

    all_row = len(select_res)
    start_row = 50 * page - 50
    end_row = 50 * page
    select_res = select_res[start_row:end_row]

    all_container_list = list()
    for select_res_item in select_res:
        if select_res_item['container_code'] not in all_container_list:
            all_container_list.append(select_res_item['container_code'])

    select_storage_sql = "select * from oversea_location_data;"
    select_storage_res = conf_fun.connect_mysql_operation(select_storage_sql, "product_supplier", "dict")

    if len(all_container_list) > 1:
        select_arrival_sql = "select * from arrival_receive where container in %s;" % str(tuple(all_container_list))
    elif len(all_container_list) == 1:
        select_arrival_sql = "select * from arrival_receive where container='%s';" % all_container_list[0]
    else:
        select_arrival_sql = "select * from arrival_receive where container='';"
    select_arrival_res = conf_fun.connect_mysql_operation(select_arrival_sql, "product_supplier", "dict")

    for select_res_item in select_res:
        for select_arrival_res_item in select_arrival_res:
            if select_res_item['container_code'] == select_arrival_res_item['container']:
                select_res_item['delivery_date'] = select_arrival_res_item['delivery_date']
                select_res_item['plan_arrival_date'] = select_arrival_res_item['arrival_date']
                select_res_item['storage_date'] = select_arrival_res_item['warehousing_date']
        for select_storage_res_item in select_storage_res:
            if select_res_item['warehouse_name'] == select_storage_res_item['warehouse_name']:
                select_res_item['warehouse_type'] = select_storage_res_item['warehouse_type']

    res = {"code": 200, "all_row": all_row, "data": select_res}
    return JsonResponse(res)
