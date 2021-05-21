import pandas as pd
import os
import  pymysql

# 老服务器
def connect_mysql_master(sql_text, dbs='reports', type='dict'):
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

# file_name = '广告组与SPU对照表.xlsx'
file_name ='auto_ad.xls'
def get_spu():
    path = os.path.join(os.getcwd(), r'place_order/' ,file_name)
    print(path)
    pd_data = pd.read_excel(path)
    # print(pd_data)
    for i,data_list in pd_data.iterrows():
        # print(i ,'--------',data_list)
        auto = data_list['auto']
        spu = data_list['spu']
        type = data_list['type']
        site  = data_list['company']
        country = data_list['country']
        insert = " '{0}', '{1}', '{2}', '{3}','{4}'".format(auto,country,site,type,spu)
        sql = " INSERT into auto_ad (auto,country, company,type,spu) values  ({0})".format(insert)
        print(sql)
        judge_sql = " select * from auto_ad where auto ='{0}' and country ='{1}' and company ='{2}'" \
                    " and type ='{3}'".format(auto, country, site, type)
        re_data = connect_mysql_master(judge_sql,type='dict')
        if re_data:
            uodate_sql =  " UPDATE auto_ad set spu ='{4}' where auto ='{0}' and country ='{1}' and company ='{2}'" \
                    " and type ='{3}'".format(auto, country, site, type,spu)
            print(uodate_sql)
            connect_mysql_master(uodate_sql)
        else:
            print(sql)
            connect_mysql_master(sql)


get_spu()