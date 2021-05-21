
import pandas as pd
import pymysql
import os
from django.http import JsonResponse, HttpResponse



# 连接数据库

''' 运营的 '''


def connect_mysql(sql_text, dbs='operation', type='dict'):

    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql',
                           passwd='By1590123!@', db=dbs)
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


def logistics_file_analysis(path,site ):

    print(213123123123123,path,site,'\n\n')
    df = pd.read_table(path)

    print(df.columns)

    for index, row in df.iterrows():
        # print(row)
        platform = row['fulfillment-channel'].strip("'")
        order_id = row['amazon-order-id'].strip("'")
        sku = row['sku'].split('*')[0]
        asin = row['asin'].strip("'")
        quantity = row['quantity']
        price = row['item-price']
        city = str(row['ship-city']).replace('�', '')
        state = str(row['ship-state']).replace('�', '')
        postal_code = row['ship-postal-code']
        country_code = row['ship-country']
        purchase_date = row['purchase-date']
        z = purchase_date.split('T')
        ww = z[0]
        # fulfillment - channel
        Warehouse =row['fulfillment-channel']
        if Warehouse =='Amazon':
            warehouse_type = 'FBA'
        elif Warehouse =='Merchant':
            warehouse_type ='海外仓'
        else:
            warehouse_type =Warehouse
        # print(platform, order_id, sku,asin,quantity,price,city,state,postal_code,country_code, ww, '\n\n\n')
        sql = 'INSERT INTO order_record ( platform, order_id, sku, asin, quantity, price, city, state, postal_code, ' \
              'country_code, purchase_date ,warehouse_type,site) ' \
              ' VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}", "{10}", "{11}" ,"{12}")' \
            .format(platform, order_id, sku, asin, quantity, price, city, state, postal_code, country_code, ww,warehouse_type,site)
        print( sql)
        try:
            connect_mysql(sql, type='dict')
        except:
            pass






