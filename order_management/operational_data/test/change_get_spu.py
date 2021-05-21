# 老服务器
import pandas as pd
import os
import  pymysql
import datetime

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

country_dict ={ '澳洲':'AU',
 '加拿大':'CA',
 '西班牙':'ES',
 '英国' :'UK',
 '法国':'FR',
 '意大利':'IT',
'德国' :'DE',
 '日本':'JP',
'美国': 'US',
 '墨西哥':'MX'
    }
rate_dict ={
    '美国':1,
    '英国':1,

    '法国':1,
    '西班牙':1,
    '德国' :1,
    '意大利':1,

    '日本':1,
    '墨西哥':1,
    '澳洲':1,
    '加拿大':1,
}


site_dict = {
    '胤佑': 'YY',
    '京汇': 'JH',
    '中睿': 'ZR',
    '爱瑙': 'AN',
    '利百锐': 'LBR',
    '笔漾教育': 'BYJY',
    '景瑞': 'JR'}

def add_data():
    pass

def get_func(ad_re_dict, country, auto,spu, site):
    times = ad_re_dict.get('times')
    auto_ad_cost = ad_re_dict.get('auto_ad_cost') # 自动组实际手动花费
    rate = rate_dict.get(country)
    auto_ad_cost = float(round(float(auto_ad_cost), 2)) /rate if auto_ad_cost else 0

    no_auto_ad_cost = ad_re_dict.get('no_auto_ad_cost') # 手动组实际广告花费
    no_auto_ad_cost = float(round(float(no_auto_ad_cost ), 2))/rate if no_auto_ad_cost else  0

    manual_guidance = ad_re_dict.get('manual_guidance') # 手动指导费用
    manual_guidance = float(round(float(manual_guidance  ), 2))/rate  if manual_guidance else 0

    automatic_guidance = ad_re_dict.get('automatic_guidance') # 自动指导费用
    automatic_guidance = float(round(float(automatic_guidance ), 2))/rate if automatic_guidance else 0

    sales = ad_re_dict.get('sales') # 广告费用
    if sales:
        sales = float(sales)/rate
    cost_rate = ad_re_dict.get('cost_rate') # 花费比率
    cost_rate= cost_rate if cost_rate else 0
    print(site ,'1',country  ,'1', auto  ,'1',spu ,'1',times ,'1',auto_ad_cost  ,'1', no_auto_ad_cost  ,'1',manual_guidance,
                         cost_rate  ,'1', automatic_guidance  ,'1',sales )

    judge_sql = " SELECT * FROM advertising_adjustment where site = '{0}' and " \
                " country ='{1}' and auto ='{2}' and dates ='{3}' and spu='{4}' ".format(site, country, auto ,times,spu)

    re_judge_data = connect_mysql_master(judge_sql, type='dict')
    if re_judge_data:
        id = re_judge_data[0].get('id')
        update_sql = " UPDATE advertising_adjustment SET   " \
                     "  cost_rate  = '{1}', sales  ='{3}'" \
                     " where id ='{4}'"\
                    .format( manual_guidance,cost_rate , automatic_guidance ,sales , id)
        print(update_sql)
        connect_mysql_master(update_sql)
    else:
        inster_sql = " INSERT  IGNORE  INTO advertising_adjustment ( site,  country,  auto,  spu , dates ," \
                     "  manual_guidance , cost_rate , " \
                     " automatic_guidance , sales) VALUES " \
                     " ('{0}' ,'{1}' ,'{2}' ,'{3}' ,'{4}', " \
                     "  '{7}', '{8}', " \
                     " '{9}','{10}')"\
                     .format(site ,country , auto , spu, times, auto_ad_cost , no_auto_ad_cost , manual_guidance,
                             cost_rate , automatic_guidance ,sales )
        print(inster_sql,'\n')
        connect_mysql_master(inster_sql)


def change_func():
    sql = " SELECT * FROM auto_ad WHERE type ='手动' "
    re_auto_data = connect_mysql_master(sql, type='dict')
    for data_dict in re_auto_data:
        # print(data_dict)
        country = data_dict.get('country')
        site  = data_dict.get('company')
        spu = data_dict.get('spu')
        spu_list = spu.split(',')
        auto = data_dict.get('auto')
        country_change = country_dict.get(country)
        site_change = site_dict.get(site)

        if len(spu_list) >1:
            print(country,site,auto,spu_list)

            spu_str =''
            for i in spu_list:
                spu_str += " '{0}' ,".format(i)
            spu_str= spu_str.rstrip(' ,')
            print(spu_str)

            ad_sql_new = " SELECT times," \
                         " ROUND (SUM(advertising_costs),2) AS advertising_costs," \
                         " ROUND (SUM(sales),2) AS sales, " \
                         " ROUND (SUM(auto_ad_cost), 2) AS auto_ad_cost, " \
                         " ROUND (SUM(no_auto_ad_cost),2) as no_auto_ad_cost," \
                         " CONCAT(ROUND(SUM(advertising_costs)/SUM(sales) * 100,2),'%' )as cost_rate " \
                         " FROM advertising_report WHERE countries = '{0}' AND company = '{1}' AND " \
                         " spu IN ( {2} )  GROUP BY times ORDER BY times DESC".format(country_change, site_change,spu_str)
            ad_re_data = connect_mysql_master(ad_sql_new, type='dict')
            for ad_re_dict in ad_re_data:
                now_day = datetime.date.today().strftime("%Y-%m-%d")
                y_7_day = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
                judge_time = ad_re_dict.get('times')
                if judge_time:
                    if y_7_day <= judge_time and now_day >= judge_time:
                        get_func(ad_re_dict, country, auto, spu, site)


        else:
            ad_sql = " SELECT * FROM advertising_report WHERE countries ='{0}' " \
                     " and company ='{1}' and spu ='{2}'  ".format(country_change, site_change, spu)

            ad_re_data = connect_mysql_master(ad_sql, type='dict')
            print(ad_re_data)
            for ad_re_dict in ad_re_data:
                now_day = datetime.date.today().strftime("%Y-%m-%d")
                y_7_day = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
                judge_time = ad_re_dict.get('times')
                if judge_time:
                    if y_7_day <= judge_time and now_day >= judge_time:

                        get_func(ad_re_dict, country, auto, spu, site)

change_func()
