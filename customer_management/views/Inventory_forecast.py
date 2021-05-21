import pymysql
import time
from settings import conf_fun

date = time.strftime('%Y-%m', time.localtime())
day = time.strftime('%d', time.localtime())
print( day, type(day))
sku_sql = ''' 
SELECT 
 pp.spu, 
pp.site,
pp.sku,
			'{0}' as date,
		  pp.country_code as country,
--      SUM( CASE WHEN pp.date ='2021-02' THEN pp.spu_num END ) as 'ready_month',
     SUM( CASE WHEN pp.date = DATE_FORMAT(date_sub(now(),interval 1 month), '%Y-%m')  THEN pp.sku_num END ) as 'before_month',
     SUM( CASE WHEN pp.date = DATE_FORMAT(date_sub(now(),interval 2 month), '%Y-%m')  THEN pp.sku_num END ) as 'before_month_1',
     SUM( CASE WHEN pp.date = DATE_FORMAT(date_sub(now(),interval 3 month), '%Y-%m') THEN pp.sku_num END ) as 'before_month_2'
FROM
(SELECT
	ci.spu,
	ci.sku,
	SUM(sku_num) as sku_num,
	p.date,
	p.site,
	p.country_code
FROM
	commodity_information ci,
	(
		SELECT
			count(sku) AS sku_num,
			sku,
			site,
			country_code,
			DATE_FORMAT(purchase_date, '%Y-%m') AS date
		FROM
			order_record
		WHERE
			DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(purchase_date)
	
		AND quantity >=1
		GROUP BY
			sku,
			purchase_date,
      site,
			country_code
		ORDER BY
			purchase_date DESC,
			sku
	) p
WHERE
	p.sku LIKE CONCAT(ci.sku, '%')

GROUP BY ci.sku, ci.spu, p.date,	p.site,p.country_code
ORDER BY  date DESC,spu DESC ) as pp
GROUP BY pp.spu,pp.site,pp.country_code,pp.sku
ORDER BY pp.spu 
'''.format(date)


spu_sql ='''
 SELECT
	pp.spu,
	pp.site,
	'{0}' AS date,
	pp.country_code,
	SUM(
		CASE
		WHEN pp.date = '{0}' THEN
			pp.spu_num
		END
	) *2  AS 'ready_month',
	SUM(
		CASE
		WHEN pp.date = DATE_FORMAT(
			date_sub(now(), INTERVAL 1 MONTH),
			'%Y-%m'
		) THEN
			pp.spu_num
		END
	) AS 'before_month',
	SUM(
		CASE
		WHEN pp.date = DATE_FORMAT(
			date_sub(now(), INTERVAL 2 MONTH),
			'%Y-%m'
		) THEN
			pp.spu_num
		END
	) AS 'before_month_1',
	SUM(
		CASE
		WHEN pp.date = DATE_FORMAT(
			date_sub(now(), INTERVAL 3 MONTH),
			'%Y-%m'
		) THEN
			pp.spu_num
		END
	) AS 'before_month_2'
FROM
	(
		SELECT
			ci.spu,
			p.site,
			p.country_code,
			SUM(sku_num) AS spu_num,
			date
		FROM
			commodity_information AS ci,
			(
				SELECT
					count(sku) AS sku_num,
					sku,
					site,
					country_code,
					DATE_FORMAT(purchase_date, '%Y-%m') AS date
				FROM
					order_record
				WHERE
					DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(purchase_date)
				AND country_code IN (
					'美国',
					'加拿大',
					'英国',
					'法国',
					'德国',
					'意大利',
					'西班牙',
					'日本',
					'澳洲',
					'墨西哥'
				)
				AND quantity >= 1
				GROUP BY
					sku,
					site,
					country_code,
					purchase_date
				ORDER BY
					purchase_date DESC,
					sku
			) p
		WHERE
			p.sku LIKE CONCAT(ci.sku, '%')
		GROUP BY
			spu,
			p.site,
			p.country_code,
			p.date
		ORDER BY
			p.date DESC
	) AS pp
GROUP BY
	pp.spu,
	pp.site,
	pp.country_code
ORDER BY
	pp.spu
'''.format(date)

spu_sql_1 = ''' 
    SELECT
	pp.spu,
	pp.site,
	'2021-02' AS date,
	pp.country_code,
	SUM(
		CASE
		WHEN pp.date = '2021-02' THEN
			pp.spu_num
		END
	) AS 'ready_month',
	SUM(
		CASE
		WHEN pp.date = DATE_FORMAT(
			date_sub(now(), INTERVAL 1 MONTH),
			'%Y-%m'
		) THEN
			pp.spu_num
		END
	) AS 'before_month',
	SUM(
		CASE
		WHEN pp.date = DATE_FORMAT(
			date_sub(now(), INTERVAL 2 MONTH),
			'%Y-%m'
		) THEN
			pp.spu_num
		END
	) AS 'before_month_1',
	SUM(
		CASE
		WHEN pp.date = DATE_FORMAT(
			date_sub(now(), INTERVAL 3 MONTH),
			'%Y-%m'
		) THEN
			pp.spu_num
		END
	) AS 'before_month_2'
FROM
	(
		SELECT
			ci.spu,
			p.site,
			p.country_code,
			SUM(sku_num) AS spu_num,
			date
		FROM
			commodity_information AS ci,
			(
				SELECT
					count(sku) AS sku_num,
					sku,
					site,
					country_code,
					DATE_FORMAT(purchase_date, '%Y-%m') AS date
				FROM
					order_record
				WHERE
					DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(purchase_date)
				AND country_code IN (
					'美国',
					'加拿大',
					'英国',
					'法国',
					'德国',
					'意大利',
					'西班牙',
					'日本',
					'澳洲',
					'墨西哥'
				)
				AND quantity >= 1
				GROUP BY
					sku,
					site,
					country_code,
					purchase_date
				ORDER BY
					purchase_date DESC,
					sku
			) p
		WHERE
			p.sku LIKE CONCAT(ci.sku, '%')
		GROUP BY
			spu,
			p.site,
			p.country_code,
			p.date
		ORDER BY
			p.date DESC
	) AS pp
GROUP BY
	pp.spu,
	pp.site,
	pp.country_code
ORDER BY
	pp.spu
'''

def early_month():
    ''' 上旬数据 '''
    pass

def late_month():
    ''' 下旬数据'''
    sku_data = conf_fun.connect_mysql_operation(sku_sql, type='dict')
    for data_dict in sku_data:
        print(data_dict)
        spu = data_dict.get('spu')
        sku = data_dict.get('sku')
        date_1 = data_dict.get('date')
        site = data_dict.get('site')
        country = data_dict.get('country')
        before_month = data_dict.get('before_month') if data_dict.get('before_month') else ''
        before_month_1 = data_dict.get('before_month_1') if data_dict.get('before_month_1') else ''
        before_month_2 = data_dict.get('before_month_2') if data_dict.get('before_month_2') else ''



        insert_update_sql = ''' INSERT INTO  sku_inventory_forecast
                                (spu, sku,date, site, country,before_month,before_month_1,before_month_2 )
                                values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
                                ON DUPLICATE KEY UPDATE
                                before_month = '{5}',
                                before_month_1 = '{6}',before_month_2 ='{7}' ;
                                '''.format(spu,sku,date_1,site,country,before_month,before_month_1,before_month_2)
        print(insert_update_sql)
        conf_fun.connect_mysql_operation(insert_update_sql)

    print(spu_sql)
    spu_date = conf_fun.connect_mysql_operation(spu_sql, type='dict')
    for spu_dict in spu_date:

        spu = spu_dict.get('spu')
        site = spu_dict.get('site')
        date_1 = spu_dict.get('date')
        country = spu_dict.get('country_code')
        before_month = spu_dict.get('before_month') if spu_dict.get('before_month') else ''
        before_month_1 = spu_dict.get('before_month_1') if spu_dict.get('before_month_1') else ''
        before_month_2 = spu_dict.get('before_month_2') if spu_dict.get('before_month_2') else ''
        if day > '15':
            ready_month = spu_dict.get('ready_month') if spu_dict.get('ready_month') else ''
        else:
            day_1 = float(spu_dict.get('before_month')) if spu_dict.get('before_month') else 0
            day_2 = float(spu_dict.get('before_month_1')) if spu_dict.get('before_month_1') else 0
            day_3 = float(spu_dict.get('before_month_2')) if spu_dict.get('before_month_2') else 0
            day_list = [day_1, day_2,day_3]

            while 0 in day_list:
                day_list.remove(0)
            if day_list >0:
                ready_month =  sum(day_list)/ len(day_list)
            else:ready_month = 0
        insert_spu_update_sql = '''
                                 INSERT INTO Inventory_forecast
                                 (spu, site,date,country, ready_month, before_month ,
                                  before_month_1,before_month_2) 
                                 values ('{0}','{1}', '{2}', '{3}','{4}' ,'{5}' ,'{6}','{7}')
                                  ON DUPLICATE KEY UPDATE
                                  ready_month = '{4}',
                                  before_month = '{5}',
                                 before_month_1 = '{6}',before_month_2 ='{7}' ;
                                 '''.format(spu, site, date_1 ,country, ready_month, before_month, before_month_1 , before_month_2)
        print(insert_spu_update_sql)
        conf_fun.connect_mysql_operation(insert_spu_update_sql)


late_month()
