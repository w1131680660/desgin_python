
import pymysql, os, time

''' 运营的 '''

# def connect_mysql_operate(sql_text, dbs='operation', type='dict'):
#     # conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)
#     # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
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
# # 物流的
# def connect_mysql_logistics(sql_text, dbs='product_supplier', type='dict'):
#     # gz-cdb-lwqgjirt.sql.tencentcdb.com
#     # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
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
# # 供应链的
# def connect_mysql_supply(sql_text, dbs='supply_chain', type='tuple'):
#     # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
#     conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_', db=dbs)
#     #                        passwd='By1590123!@', db=dbs)
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
# # 连接主数据库
# def connect_mysql_master(sql_text, dbs='reports', type='tuple'):
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

operating_data_dict = {
    '测算表': ['calculation_file','calculation_file_date' , 'calculation_file_path' ,'calculation_file_state'],
    '下单表' : ['place_order', 'place_order_date'  ,'place_order' , 'place_order_state'],
    '建仓信息确认表' :['establish_warehouse', 'establish_warehouse_date' , 'establish_warehouse' ,'establish_warehouse_state'],
    '箱贴' : ['box_stuck','box_stuck_date' ,'box_stuck' ,'box_stuck_state'],
    '海外仓信息确认表' :['establish_warehouse', 'establish_warehouse_date' , 'establish_warehouse' ,'establish_warehouse_state'],
    '条码附件': ['bar_code', 'bar_code_date','bar_code','bar_code_state'],
    '产品条码附件':['bar_code_new', 'bar_code_date_new', 'bar_code_new','bar_code_state_new']
}

# print(operating_data_dict.keys())