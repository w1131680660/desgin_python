import datetime
from django.http import JsonResponse

# from stock_management import scheduling_settings
from settings import conf_fun

# 每日盘点

def daily_calculate(factory,date,date_1,date_2,page ):
    sql = "  SELECT pdd.*, nmm.sum_delivery,nmm.avg_delivery,(pdd.num_pro- nmm.sum_delivery ) as stock_num ," \
          " ( pdd.distribution_num - pdd.num_pro ) as no_produce from " \
          " (SELECT pdd.*, nmm.produce_num from ( SELECT pd.*, nm.num_pro, nm.avg_pro " \
          " FROM ( SELECT product_number AS product_code, product_name,SUM(distribution_num) AS distribution_num " \
          "FROM order_distribution WHERE factory = '{0}' AND dates LIKE '{2}%' GROUP BY product_number, product_name " \
          " ORDER BY product_number) AS pd LEFT JOIN ( SELECT product_code, SUM(number) AS num_pro, ROUND(AVG(number), 1) AS avg_pro " \
          " FROM product_storage WHERE supplier = '{0}' AND finished_type = '成品' AND date LIKE '{3}%' GROUP BY product_code ) AS nm " \
          " ON pd.product_code = nm.product_code ) as pdd LEFT JOIN ( " \
          " SELECT p.date, product_code, p.number AS produce_num " \
          " FROM  product_storage AS p WHERE finished_type = '成品' AND supplier = '{0}' AND date LIKE '{1}' ORDER BY product_code) as nmm " \
          " on pdd.product_code = nmm.product_code) as pdd LEFT JOIN (SELECT del.product_code AS products_code, SUM(del.number) AS sum_delivery, " \
          " ROUND(AVG(del.number), 1) AS avg_delivery FROM delivery as de , delivery_product as del WHERE de.delivery_code = del.delivery_code AND " \
          " de.delivery_date LIKE '{3}%' AND de.delivery_supplier = '{0}' GROUP BY del.product_code ORDER BY del.product_code) as nmm " \
          " on pdd.product_code = nmm.products_code LIMIT {4},50".format(factory, date,date_1,date_2, page)
    print('\n\n',sql)

    count_sql =  "  SELECT COUNT(pdd.product_code) as count_num from " \
          " (SELECT pdd.*, nmm.produce_num from ( SELECT pd.*, nm.num_pro, nm.avg_pro " \
          " FROM ( SELECT product_number AS product_code, product_name,SUM(distribution_num) AS distribution_num " \
          "FROM order_distribution WHERE factory = '{0}' AND dates LIKE '{2}%' GROUP BY product_number, product_name " \
          " ORDER BY product_number) AS pd LEFT JOIN ( SELECT product_code, SUM(number) AS num_pro, ROUND(AVG(number), 1) AS avg_pro " \
          " FROM product_storage WHERE supplier = '{0}' AND finished_type = '成品' AND date LIKE '{3}%' GROUP BY product_code ) AS nm " \
          " ON pd.product_code = nm.product_code ) as pdd LEFT JOIN ( " \
          " SELECT p.date,  product_code, p.number AS produce_num " \
          " FROM  product_storage AS p WHERE finished_type = '成品'  AND supplier = '{0}' AND date LIKE '{1}' ORDER BY product_code) as nmm " \
          " on pdd.product_code = nmm.product_code) as pdd LEFT JOIN (SELECT del.product_code AS products_code, SUM(del.number) AS sum_delivery, " \
          " ROUND(AVG(del.number), 1) AS avg_delivery FROM delivery as de , delivery_product as del WHERE de.delivery_code = del.delivery_code AND " \
          " de.delivery_date LIKE '{3}%' AND de.delivery_supplier = '{0}' GROUP BY del.product_code ORDER BY del.product_code) as nmm " \
          " on pdd.product_code = nmm.products_code".format(factory, date,date_1,date_2)
    return sql,count_sql

def daily_inventory(request):
    ret = {'code': 200, 'data': '无'}
    data = request.GET

    factory = data.get('factory')
    page = int(data.get('page')) if data.get('page') else 1
    page = 1 if str(page) == '0' else page
    print('\n',1231313213,page, type(page))
    page = (int(page)-1) * 50
    date = data.get('date')
    if not factory:
        factory = '合迪'
    if not date:
        date = str(datetime.date.today())
    date2 = '-'.join(date.split('-')[0:2])
    date1 = '/'.join(date.split('-')[0:2])
    print(factory, date, date1, date2)
    sql ,count_sql= daily_calculate(factory,date,date1,date2,page)
    re_data = conf_fun.connect_mysql_supply(sql, type='dict')
    re_count_data = conf_fun.connect_mysql_supply(count_sql, type='dict')
    ret['data'] = re_data
    ret['count_data'] = re_count_data
    return JsonResponse(ret)


# 每日盘点-获取分配表所有工厂
def get_order_distribution_supplier(request):
    select_distribution_sql = "select distinct factory from order_distribution;"
    select_distribution_res = conf_fun.connect_mysql_supply(sql_text=select_distribution_sql)
    res = {"code": 200, "data": select_distribution_res}
    return JsonResponse(res)
