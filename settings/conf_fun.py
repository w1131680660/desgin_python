import pymysql

#from connect_mysql import connect_mysql
from settings.connect_mysql import connect_mysql

# 运营
def connect_mysql_operation(sql_text, dbs='operation', type='tuple') -> object:
    response = connect_mysql(sql_text,dbs,type,'new_system')
    return response

''' 发货的 order'''
def connect_mysql_or(sql_text, dbs='order', type='tuple'):
    response = connect_mysql(sql_text, dbs, type, 'old_system')
    return response


''' 发货的'''
def connect_mysql_re(sql_text, dbs='reports', type='tuple'):
    print(sql_text)
    response = connect_mysql(sql_text, dbs, type, 'old_system')
    return response

''' 供应链'''

def connect_mysql_supply(sql_text, dbs='supply_chain', type='tuple'):
    print(sql_text)
    response = connect_mysql(sql_text,dbs,type,'new_system')
    return response

# 工厂的
def connect_mysql_factory(sql_text, dbs='factory', type='tuple'):
    response = connect_mysql(sql_text, dbs, type, 'new_system')
    return response

# 财务
def connect_mysql_financial(sql_text, dbs='financial', type ='tuple'):
    response = connect_mysql(sql_text, dbs, type, 'new_system')
    return response


# 物流
def connect_mysql_product_supplier(sql_text, dbs='product_supplier', type ='dict'):
    response = connect_mysql(sql_text,dbs,type,'new_system')
    return response