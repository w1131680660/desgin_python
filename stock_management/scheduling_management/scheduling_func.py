# 新增数据的统一模板

import os
# from stock_management import scheduling_settings
import time,json,requests
import datetime
from datetime import timedelta
# 更新的函数、
from settings import conf_fun


def update_conn_sql(table_name,update_str,where_str):
    sql = "UPDATE {0}  SET  {1}  WHERE id >0 {2}".format(table_name, update_str,where_str)
    print('\n连接运营的更新的sql',sql,'\n')
    res = conf_fun.connect_mysql_operation(sql, type='dict')
    return 123

# 新增的运营的链接数据库
def conn_sql_demo(table_name, key_str, value_str):
    sql = "INSERT INTO  {0}  ( {1} ) VALUES ({2})".format(table_name, key_str, value_str)
    print('新增的sql',sql,'\n')
    conf_fun.connect_mysql_operation(sql, type='dict')

# 新增供应链的
def conn_supply_demo(table_name, key_str, value_str):
    sql = "INSERT INTO  {0}  ( {1} ) VALUES ({2})".format(table_name, key_str, value_str)
    print('新增的供应链sql',sql,'\n')

    conf_fun.connect_mysql_supply(sql, type='dict')

def conn_sql_select(sql):
    print('\n', '连接运营' ,sql,'\n')
    res =  conf_fun.connect_mysql_operation(sql, type='dict')
    return res


def conn_sql_logistics(sql):
    print('\n连接物流的',sql)
    res = conf_fun.connect_mysql_product_supplier(sql,type='dict')
    return res





# 将数据转换为element_ui
def change_type( country_data,container_type_data ,  channel_data ,  site_data ,factory_data ):
    country_data_list, container_type_data_list ,channel_list ,site_list, factory_list = [], [], [] ,[] ,[]
    re_list = [country_data_list, container_type_data_list ,channel_list ,site_list,factory_list]
    an_list =  [ country_data, container_type_data ,channel_data ,  site_data , factory_data ]
    for_list =['country', 'container_type' ,'platform', 'site', 'factory']


    for index, object_list in enumerate(an_list):
        for channel_dict in object_list:
            q = {}

            q['value'] = channel_dict.get(for_list[index])
            q['label'] = channel_dict.get(for_list[index])
            re_list[index].append(q)

    return re_list


# 新增排期模板的数据
def add_template_data(data, table_name,unique_id ):
    ''' 肖飞 2020-01-18'''
    key_list =[]
    value_list = []

    print(datetime.datetime.strftime(datetime.datetime.now() + timedelta(hours=8), "%Y-%m-%d %H:%M:%S"))
    now_date = datetime.datetime.strftime(datetime.datetime.now() + timedelta(hours=8), "%Y-%m-%d %H:%M:%S")

    print('新增的排期数据',data,'\n')
    for key,value in data.items():
        if key not in  ['sku_num' ,'calculation_file_path','user_name']:
            key_list.append(key)
            value_list.append(r'"{}"'.format(value))
    key_list.append('unique_id')
    value_list.append('"%s"'%(unique_id))
    key_list.append('create_date')
    value_list.append('"%s"'%(now_date))
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)
    print(key_str ,'\n', value_str, '\n')
    conn_sql_demo( table_name, key_str, value_str )
    # res =''    return res

# 新增订单集成的数据
def add_order_confirmation(data , table_name,unique_id):

    print('\n', data , '\n')
    container = data.get('container_num')

    sku_list = json.loads(data.get('sku_num'))
    print('\n\n\n',sku_list)
    for sku_str in sku_list:
        # sql = " INSERT INTO  {0} ( container_num, sku ) VALUES  ( '{1}', '{2}' )".format(table_name,container,sku_str )
        key_str = 'container_num, sku, product_code, sku_num ,integrated_state,unique_id'
        conn_sql_demo(table_name,key_str," '{0}' , '{1}' ,'{2}' ,'{3}','{4}','{5}'"
                      .format(container, sku_str[0], sku_str[1],sku_str[2],'未集成',unique_id) ,)



# 新增 待测算上传的资料
def add_operating_data(data , table_name,unique_id):
    key_list =[]
    value_list = []

    localtime = time.strftime("%Y-%m-%d", time.localtime())
    print('当前时间')
    for key,value in data.items():
        if key in ['platform','site','country','container_num','user_name']:

            key_list.append(key)
            value_list.append(r'"{}"'.format(value))
        elif key == 'calculation_file_path':
            path = master_upload_file(value, 'calculation_file/')

            key_list.append(key)
            value_list.append(r'"{}"'.format(path))

    key_list.append('calculation_file_date')
    value_list.append(r'"{}"'.format(localtime))
    key_list.append('calculation_file_state')
    value_list.append("'已审核'")
    key_list.append('unique_id')
    value_list.append('"{}"'.format(unique_id))
    key_list.append('status')
    value_list.append("'未回传'")
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)

    res = conn_sql_demo( table_name, key_str, value_str )


def master_upload_file(files,file_path):
    url = 'https://www.beyoung.group/file_upload/'
    path2 = os.path.join(r'operation/operating_data/', file_path, )
    data = {'path':path2}
    print(data)
    res =requests.post(url,data,files={'file':files})
    path3=  os.path.join(r'operation/operating_data/',file_path, str(files))
    print('这是什么路径\n',path3)
    return path3




