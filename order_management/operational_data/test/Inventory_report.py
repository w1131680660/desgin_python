import pymysql

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

#  financial
country_dict = {
    '澳洲': 'AU',
    '加拿大': 'CA',
    '西班牙': 'ES',
    '英国': 'UK',
    '法国': 'FR',
    '意大利': 'IT',
    '德国': 'DE',
    '日本': 'JP',
    '美国': 'US',
    '墨西哥': 'MX',
    '新加坡': 'SG',
    '马来西亚': 'MY',
}

site_dict = {
    '胤佑': 'YY',
    '京汇': 'JH',
    '中睿': 'ZR',
    '爱瑙': 'AN',
    '利百锐': 'LBR',
    '笔漾教育': 'BYJY',
    '景瑞': 'JR'}
def inventory_report():

    eu_sql = ''' SELECT oo.country,pp.site,pp.product_code,oo.sku as sku,product_name,fnsku,product_type,
                fba, overseas_warehouse,date
     from (SELECT DISTINCT sku,spu, 
                CASE 
                    countries 
                    WHEN 'UK' THEN '欧洲' 
                    WHEN 'DE' THEN '欧洲'
                  WHEN 'FR' THEN '欧洲'
                    WHEN 'IT' THEN '欧洲'
                    WHEN 'ES' THEN '欧洲'
                END as country,
                CASE 
                    company
                    WHEN 'ZR' THEN '中睿'
                  WHEN 'JH' THEN '京汇'
                  WHEN  'AN' THEN '爱瑙'
                END as site,
                nums as overseas_warehouse,
                fba,
                times as date
                FROM order_sublist
                ORDER BY times DESC, sku DESC)  as oo
                INNER JOIN (SELECT co.platform,co.country,co.spu,co.site,co.product_code,co.sku,pr.product_name,co.fnsku,pr.product_type FROM commodity_information  as co RIGHT JOIN product_message as pr
                on co.product_code = pr.product_code
                ORDER BY co.spu DESC,country DESC,pr.product_code DESC) as pp
                on oo.sku =pp.sku and oo.country =pp.country and oo.site =pp.site
                '''
    eu_data = connect_mysql1(eu_sql, type='dict')
    print('\n\n')

    for data_dict in eu_data:
        k_str = ''
        v_str = ''
        # print(data_dict.get('fnsku'))
        for k,v in data_dict.items():
            k_str += " {0} ,".format(k)
            v_str += " '{0}' ,".format(v)
        fba = float(data_dict.get('fba')) if data_dict.get('fba') else 0
        overseas_warehouse = float(data_dict.get('overseas_warehouse')) if data_dict.get('overseas_warehouse')  else 0
        num = fba+overseas_warehouse
        k_str = k_str.rstrip(' ,')
        v_str = v_str.rstrip(' ,')
        insert_sql = " INSERT IGNORE INTO Inventory_report ({0},type,platform,num) values ({1},'{5}','2C','Amazon' )" \
                     "ON DUPLICATE KEY UPDATE num ='{2}',fba ='{3}',overseas_warehouse='{4}'"\
            .format(k_str, v_str, num ,fba, overseas_warehouse,num)
        print(insert_sql,'\n')
        connect_mysql(insert_sql,dbs='financial')
inventory_report()