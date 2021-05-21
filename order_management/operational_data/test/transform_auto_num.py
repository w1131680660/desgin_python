import datetime
from itertools import groupby
from operator import itemgetter

import pymysql


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


site_dict = {
    '胤佑': 'YY',
    '京汇': 'JH',
    '中睿': 'ZR',
    '爱瑙': 'AN',
    '利百锐': 'LBR',
    '笔漾教育': 'BYJY',
    '景瑞': 'JR'}

country_dict = {'澳洲': 'AU',
                '加拿大': 'CA',
                '西班牙': 'ES',
                '英国': 'UK',
                '法国': 'FR',
                '意大利': 'IT',
                '德国': 'DE',
                '日本': 'JP',
                '美国': 'US',
                '墨西哥': 'MX'
                }


def change_func():
    transform_auto_sql = " SELECT * FROM transform_auto"
    re_transform_auto = connect_mysql_master(transform_auto_sql, type='dict')
    for transform_auto_dict in re_transform_auto:
        site = transform_auto_dict.get('site')
        country = transform_auto_dict.get('country')
        country_en = country_dict.get(country)
        site_en = site_dict.get(site)
        manual_name = transform_auto_dict.get('manual_name')  # 手动组
        automatic_name = transform_auto_dict.get('automatic_name')  # 自动组

        manual_sql = " SELECT * FROM adgroup WHERE site='{0}' and country ='{1}' and adgroup ='{2}' and type='手动'" \
            .format(site_en, country_en, manual_name)
        automatic_sql = " SELECT * FROM adgroup WHERE site='{0}' and country ='{1}' and adgroup = '{2}' and type='自动'" \
            .format(site_en, country_en, manual_name)
        manual_data = connect_mysql_master(manual_sql, type='dict')
        automatic_data = connect_mysql_master(automatic_sql, type='dict')

        data_dict = {}

        for dates, items in groupby(manual_data, key=itemgetter('dates')):
            data_dict[dates] = {}
            for type, items_1 in groupby(items, key=itemgetter('type')):
                if type not in data_dict[dates]:
                    data_dict[dates][type] = []
                    for i in items_1:
                        data_dict[dates][type].append(i)

        for dates, items in groupby(automatic_data, key=itemgetter('dates')):
            if not data_dict.get(dates):
                data_dict[dates] = {}

            for type, items_1 in groupby(items, key=itemgetter('type')):
                if type not in data_dict[dates]:
                    data_dict[dates][type] = []
                    for i in items_1:
                        data_dict[dates][type].append(i)

        if data_dict.keys():
            max_date = max(data_dict.keys())

        for key, value in data_dict.items():
            # 手动
            date_time = key
            ww = datetime.datetime.strptime(date_time, "%Y-%m-%d")
            zz = ww.strftime("%Y-%m-%d")
            date_time = zz if country in ['加拿大', '美国'] else (ww + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

            manual = value.get('手动')
            manual_sales = manual[0].get('sales') if manual else 0
            # 自动
            automatic = value.get('自动')
            automatic_sales = automatic[0].get('sales') if automatic else 0
            judge_sql = " SELECT * FROM advertising_adjustment WHERE site ='{0}' and country ='{1}' and auto='{2}' and dates ='{3}'" \
                .format(site, country, manual_name, date_time)
            re_judge_data = connect_mysql_master(judge_sql, type='dict')
            print(101,'\n',judge_sql)
            if re_judge_data:
                update_sql = " UPDATE advertising_adjustment set no_auto_ad_cost='{0}' ,auto_ad_cost ='{1}'" \
                             " where site ='{2}' and country ='{3}' and auto='{4}' and dates ='{5}'" \
                    .format(manual_sales, automatic_sales, site, country, manual_name, date_time)
                if country in ['加拿大', '美国']:
                    print('\n',update_sql)
                connect_mysql_master(update_sql)
            if key == max_date:
                spu_sql = " SELECT spu FROM  auto_ad WHERE  company='{0}' and country ='{1}'" \
                          " and auto='{2}' and  type='手动' ".format(site, country, manual_name)

                spu_data = connect_mysql_master(spu_sql, type='dict')
                if spu_data:
                    spu = spu_data[0].get('spu')
                else:
                    spu = ""

                max_ad_sql = " SELECT * FROM advertising_adjustment WHERE site ='{0}' and country ='{1}' and auto='{2}' and dates ='{3}'" \
                    .format(site, country, manual_name, max_date)
                re_judge_data = connect_mysql_master(max_ad_sql, type='dict')

                if not re_judge_data:
                    advertising_report_sql = " SELECT * FROM advertising_report WHERE countries ='{0}' " \
                                             "  and company ='{1}' and spu ='{2}' and  times='{3}' ".format(country_en,
                                                                                                            site_en,
                                                                                                            spu,
                                                                                                            max_date)
                    re_advertising_report_data = connect_mysql_master(advertising_report_sql, type='dict')
                    if not re_advertising_report_data:
                        insert_sql = " INSERT INTO advertising_adjustment " \
                                     " ( site, country, auto, spu, dates, sales,     " \
                                     "  cost_rate ) VALUES " \
                                     " ('{0}' ,'{1}' ,'{2}' ,'{3}','{4}' ,'{5}'," \
                                     " '{6}' )".format(site, country, manual_name, spu, max_date, 0, 0,
                                                       manual_sales, automatic_sales)
                        if country == '美国' and site == '胤佑':
                            print(insert_sql)
                        connect_mysql_master(insert_sql)


change_func()
