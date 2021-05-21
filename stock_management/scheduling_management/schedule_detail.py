# from stock_management import scheduling_settings
from itertools import groupby
from operator import itemgetter

from django.http import JsonResponse

from settings import conf_fun

''' 运营资料查询sql'''

'''订舱信息sql查询  配舱信息sql查询'''


def shipping_record(container_num):
    shipping_record_sql = "select * from ship_information  WHERE container_num ='%s'" % (container_num)
    print(shipping_record_sql)
    shipping_record_data = conf_fun.connect_mysql_product_supplier(shipping_record_sql, type='dict')
    if shipping_record_data: shipping_record_data = shipping_record_data[0]
    return shipping_record_data


'''是否截单sql查询'''


def cut_off_data(container_num):
    cut_off_data_sql = ""
    _cut_off_data = conf_fun.connect_mysql_product_supplier(cut_off_data_sql, type='dict')
    return _cut_off_data


'''资料上传sql,报清关查询 唯一'''


def data_query(container_num):
    data_query_sql = " select * from container_file WHERE container_code ='%s'" % (container_num)
    print(data_query_sql)
    data_query_data = conf_fun.connect_mysql_product_supplier(data_query_sql, type='dict')
    if data_query_data: data_query_data = data_query_data[0]
    return data_query_data


'''报请关数据查询 物流审核后完毕为true'''


def customs_clearance(container_num):
    customs_clearance_sql = ""
    customs_clearance_data = conf_fun.connect_mysql_product_supplier(customs_clearance_sql, type='dict')
    if customs_clearance_data: customs_clearance_data = customs_clearance_data[0]
    return customs_clearance_data


''' 預計裝櫃'''


def expect_container(container_num):
    expect_container_sql = "SELECT container, date FROM motorcade_data  WHERE container ='%s'" % (container_num)
    expect_container = conf_fun.connect_mysql_product_supplier(expect_container_sql, type='dict')
    if expect_container: expect_container = expect_container[0]
    return expect_container


''' 到港接受'''


def port_receiving(container_num):
    port_receiving_sql = "SELECT container, receive_count FROM arrival_receive  WHERE container ='%s'" % (container_num)
    port_receiving_data = conf_fun.connect_mysql_product_supplier(port_receiving_sql, type='dict')
    if port_receiving_data: port_receiving_data = port_receiving_data[0]
    return port_receiving_data


# 运营资料上传
def operating_data_ser(container_num):
    operating_data_sql = " SELECT  calculation_file_path ," \
                         " establish_warehouse ,box_stuck ,bar_code FROM operating_data " \
                         "WHERE container_num='%s'" % (container_num)
    operating_data_re = conf_fun.connect_mysql_operation(operating_data_sql, type='dict')
    type_sql = "SELECT DISTINCT product_type FROM order_integration oi , product_message pr WHERE oi.container_num ='{0}' and oi.product_code = pr.product_code".format(
        container_num)
    type_data = conf_fun.connect_mysql_operation(type_sql, type='dict')
    operating_data_statue = '点亮'
    container_list = []
    print(78, '\n', operating_data_re)
    for container_dict in operating_data_re:
        for k, v in container_dict.items():
            if v not in container_list and v:
                container_list.append(v)
    if type_data:
        type = type_data[0].get('product_type')
        print(type, '\n', container_list)
        if type == '钢木':
            list_string = ['测算', '建仓', '条码', '附件']
            all_words = set([word for word in list_string for text in container_list if word in text])
            if len(all_words) >= 3:
                operating_data_statue = '点亮'
            else:
                operating_data_statue = ''
        else:
            list_string = ['测算', '建仓', '条码', '下单', '附件']
            all_words = set([word for word in list_string for text in container_list if word in text])
            if len(all_words) >= 4:
                operating_data_statue = '点亮'
            else:
                operating_data_statue = ''
    container_dict = {'container_list': container_list, 'operating_data_statue': operating_data_statue}
    return container_dict


# 进行订单文件的状态最终
def order_file(container_num):
    # 1.货柜是否集成
    integrated_sql = " SELECT DISTINCT integrated_state FROM order_integration WHERE container_num ='{0}'".format(
        container_num)
    # 2.货柜是否分发
    order_distribution_sql = " SELECT DISTINCT `status`,factory, product_type FROM order_distribution WHERE container_code ='{0}'".format(
        container_num)
    # 3.对应工厂的货柜好资料是否上传齐全，
    data_sql = " SELECT *  FROM operating_data WHERE container_num ='{0}';".format(container_num)
    # 4.查看发票是否上传
    invoice_sql = ''' SELECT DISTINCT  up.factory_upload_site, up.signed_data_site ,sup.supplier from upload_shipment_information as up INNER JOIN supplier as sup 
            on up.factory = sup.gc_code  WHERE data_name like '%{0}%' '''.format(container_num)

    # 5.验证柜子是海外仓还是FBA
    warehouse_type_sql = ''' SELECT warehouse_type FROM schedule_container WHERE container_num='{0}' '''.format(
        container_num)

    integrated_data = conf_fun.connect_mysql_operation(integrated_sql, type='dict') #运营集成
    order_distribution_data = conf_fun.connect_mysql_supply(order_distribution_sql, type='dict') # 供应链集成
    data_data = conf_fun.connect_mysql_operation(data_sql, type='dict')  # 运营资料
    invoice_data = conf_fun.connect_mysql_re(invoice_sql, type='dict')# 发票
    warehouse_type = conf_fun.connect_mysql_operation(warehouse_type_sql, type='dict')
    # 仓库类型
    warehouse_type = warehouse_type[0].get('warehouse_type') if warehouse_type else ''
    data_dict = {}
    product_type = ''  # 是魔片还钢木
    integrated_statue = 1 if integrated_data else 0  # 是否集成
    distribution_statue = 1 if order_distribution_data else 0 # 是否分发
    data_dict_1 = {'integrated_statue': integrated_statue, 'distribution_statue':distribution_statue}
    if order_distribution_data:
        for factory, items in groupby(order_distribution_data, key=itemgetter('factory')):
            if factory not in data_dict.keys():
                for i in items:
                    print(i)
                    product_type = i.get('product_type')
                    data_dict[factory] = {}

    if data_data:
        for factory, items_1 in groupby(data_data, key=itemgetter('factory')):
            for items in items_1:
                if warehouse_type != 'FBA':
                    bar_code_new = 1 if items.get('bar_code_new') else 0 # 海外仓
                else:
                    bar_code_new = 1
                if product_type == '魔片':
                    place_order = 1 if items.get('place_order') else 0 # 下单表
                else:
                    place_order = 1
                establish_state = 1 if items.get('establish_warehouse') else 0 # 建仓表
                box_stuck = 1 if items.get('box_stuck') else 0 # 相贴
                bar_code = 1 if items.get('bar_code') else 0
                z = bar_code_new + place_order + establish_state + box_stuck+ bar_code
                print(z,bar_code_new , place_order ,establish_state ,box_stuck ,bar_code)
                data_statue = 1 if z ==5 else 0
                data_dict[factory] = {'data_statue': data_statue, 'es_upload':0}

    if invoice_data:
        for factory, items_1 in groupby(invoice_data, key=itemgetter('supplier')):
            for items in items_1:
                factory_statue = items.get('factory_upload_site')
                signed_data_site = items.get('signed_data_site')
                # 财务是否回传
                data_dict[factory]['factory_statue'] = 1 if factory_statue else 0
                data_dict[factory]['signed_data_site'] =1 if signed_data_site else 0
                data_dict[factory]['es_upload'] =1
    print(data_dict,'\n',data_dict_1)
    return data_dict,data_dict_1


def schedule_detail(request):
    container = request.GET.get('container_num')
    ret = {'code': 200, 'msg': '无'}
    container_num = container
    print('\n', container)
    shipping_record_data = shipping_record(container_num)  # '''订舱信息sql查询  配舱信息sql查询'''
    data_query_data = data_query(container_num)  # '''资料上传sql,报清关查询 唯一'''
    expect_container_data = expect_container(container_num)
    port_receiving_data = port_receiving(container_num)
    operating_data_data = operating_data_ser(container_num)
    data_1,data_2 = order_file(container_num)
    ret['shipping_record_data'] = shipping_record_data  # 订舱信息   配舱信息
    ret['data_query_data'] = data_query_data  # 资料上传，报清关数据'''
    ret['port_receiving_data'] = port_receiving_data  # 确认入仓
    ret['expect_container'] = expect_container_data
    ret['operating_data_data'] = operating_data_data  # 运营文件
    ret['data_1'] = data_1 # 订单 文件状态
    ret['data_2'] = data_2
    return JsonResponse(ret)
