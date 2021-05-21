from stock_management.scheduling_management import scheduling_sql

from django.http import JsonResponse
from settings import conf_fun


def down_box():
    ''' 站点'''
    store_sql = "select distinct store FROM arrival_receive where store !='' "

    ''' 国家 '''
    country_sql = "select distinct country FROM  arrival_receive where country !=''"

    '''货物类型'''
    type_sql = "select distinct type FROM  arrival_receive where  type!=''"

    store_data = conf_fun.connect_mysql_product_supplier(store_sql)
    country_data = conf_fun.connect_mysql_product_supplier(country_sql)
    type_data = conf_fun.connect_mysql_product_supplier(type_sql)
    return change_element_ui(store_data,  country_data ,type_data )

def change_element_ui(store_data,  country_data ,type_data ):
    store_data_list, country_data_list, type_data_list =[] ,[] ,[]
    re_list = [   store_data_list, country_data_list, type_data_list  ]
    an_list =  [ store_data,  country_data ,type_data ]
    for_list =[ 'store', 'country' ,'type']

    for index, object_list in enumerate(an_list):
        for channel_dict in object_list:
            q = {}

            q['value'] = channel_dict.get(for_list[index])
            q['label'] = channel_dict.get(for_list[index])
            re_list[index].append(q)

    return re_list

# 搜索
def search_sku(data):
    ser_str =''
    sku = data.get('sku')
    print('SKU请求数据',data)
    if sku :
        ser_str += " AND ca.sku = '{0}'".format(sku)
        return ser_str
    for key,value in data.items():
        if key !='page' and value:
            if key in ['store', 'country' ,'type'] and value:
                ser_str += " AND ar.{0} = '{1}'".format(key,value)
            elif key =='sku':
                ser_str +=" AND ca.sku = '{0}'".format(value)
    print(ser_str)
    return ser_str

def sku_search(request):
    ret = {'code':200,'msg':'无'}
    data = request.GET
    page = data.get('page') if data.get('page') else 1
    page = (int(page)-1)*50
    sku_data =''
    if len(data.keys()) == 1:
        sku_search_sql = scheduling_sql.container_search_sku_sql.format('', page)
        count_sql = scheduling_sql.count_sku_sql.format('' )
    else:
        sku_search_sql = scheduling_sql.container_search_sku_sql.format(search_sku(data), page)
        sku_sql = scheduling_sql.sku_search_sql.format(search_sku(data))
        sku_data = conf_fun.connect_mysql_product_supplier(sku_sql)
        count_sql = scheduling_sql.count_sku_sql.format(search_sku(data))
    re_data = conf_fun.connect_mysql_product_supplier(sku_search_sql)
    print(123123123, count_sql)
    count_data = conf_fun.connect_mysql_product_supplier(count_sql)

    re_list =  down_box()
    ret['re_data'] = re_data
    ret['re_list'] = re_list
    ret['re_count'] = count_data
    ret['sku_data'] =sku_data
    return JsonResponse(ret)
