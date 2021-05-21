sql = ' SELECT id,dates as times,site as company,country as countries,spu,auto_ad_cost,' \
      ' automatic_guidance ,no_auto_ad_cost , manual_guidance, sales ,cost_rate,remakes' \
      ' from advertising_adjustment where  id> 0  {0} order by times  limit 0,50'

front_sql = " SELECT URL,spu,dates,country,comment_amount,star_level,ranking, small_rank ,aging" \
            " FROM front_display WHERE id >0 AND ranking !='' {0} "

eu_sql = " SELECT spu, SUM(fba) as sum_num, times FROM {0} WHERE id >0 {1} GROUP BY spu,times ORDER BY times DESC"

other_sql = "select * from sku_report where company='{0}' and countries='{1}' and sku='{2}' order by id desc "

auto_sql = " select * from auto_ad where type ='手动' {0} "

# 这是每日订单的最大日期sql
date_every_sql = '''SELECT DISTINCT times FROM {2} WHERE company='{0}' and countries='{1}' ORDER BY times desc'''
# 每日订单页面的sku订单汇总sql
sku_sql = '''
SELECT DISTINCT cor.spu as SPU ,cor.sku AS SKU,cor.fbm AS FBM, IFNULL(cor.fbm,0) + IFNULL(ordc.FBA,0) as sum_spu, ordc.*  FROM 
(
 SELECT cor.sku,cor.spu,IFNULL(fbm_ord.nums,0) as fbm from
 (SELECT spu,sku,product_code FROM  commodity_information WHERE  country ='{0}' AND site ='{1}' )as cor
LEFT JOIN (SELECT SUM(nums) as nums,product_code   from fbm_data 
WHERE times = (SELECT DISTINCT times FROM fbm_data WHERE area in {8} ORDER BY times DESC LIMIT 0,1)
 and area in {8} GROUP BY product_code ) as  fbm_ord on cor.product_code = fbm_ord.product_code

 )as cor  LEFT JOIN ( 
select spu, sku,
SUM(CASE WHEN times ='{6}' THEN fba  END) as 'FBA',
SUM(
		CASE
		WHEN times = '{6}' THEN
			fba
		END
	) AS 'sum_spu',
 SUM(nums) as nums_count,
    {5}
 from {7} where times in ({4})  and company='{2}' and countries='{3}' 
 GROUP BY spu,sku		
ORDER BY spu DESC )  ordc
on cor.spu = ordc.spu and  ordc.sku LIKE CONCAT('%',cor.sku,'%')
ORDER BY ordc.spu DESC

'''

# 每日订单页面的SPU的订单汇总sql
spu_sql = ''' SELECT DISTINCT spu_ord.*,IFNULL(fbm_ord.fbm,0) as FBM ,IFNULL(fbm_ord.fbm ,0) + IFNULL(spu_ord.FBA ,0)  as sum_spu FROM
        ( select spu AS SPU ,SUM(CASE WHEN times ='{4}' THEN fba  END) as 'FBA',
{3} from spu_report where times in ({2}) and company='{0}' and countries='{1}' group  by spu ) as spu_ord 
LEFT JOIN  
 (SELECT cor.spu,IFNULL(SUM(fbm_ord.nums),0) as fbm from
 (SELECT spu,product_code FROM  commodity_information WHERE  country ='{6}' AND site ='{7}' )as cor
LEFT JOIN (SELECT SUM(nums) as nums,product_code   from fbm_data 
WHERE times = (SELECT DISTINCT times FROM fbm_data WHERE area in {5} ORDER BY times DESC LIMIT 0,1)
 and area in {5}) GROUP BY product_code ) as  fbm_ord 
on cor.product_code = fbm_ord.product_code
GROUP BY cor.spu)
as fbm_ord

on spu_ord.SPU = fbm_ord.spu
'''

# 每日营业额sql
turnover_sql = ''' SELECT {3} FROM gy_report  WHERE company ='{0}' AND countries ='{1}' and dates in ({2}) '''

spu_category_sql = '''
SELECT ood.category, SUM(ood.nums) as sum_ord,
 {0}  
  from 
(SELECT  ord.nums, com.category,ord.times FROM 
(select spu,FORMAT(sum(nums),0) as nums,times from {4} where  times in ({1}) and company='{2}'  and countries ='{3}'								and countries='{3}' GROUP BY spu,times )
 as ord LEFT JOIN
(SELECT DISTINCT spu,category FROM `order`.commodity_information ) 
as com on ord.spu =com.spu 
WHERE LENGTH(com.category) >1 ) as ood
GROUP BY ood.category

'''

# 在途貨櫃的货柜好sql
transit_sql = ''' SELECT DISTINCT container FROM
                arrival_receive AS ar
            INNER JOIN (SELECT dde.*,ordd.sku,ordd.country,ordd.store ,ordd.product_type from  ( SELECT del.* , sc.warehouse_type as transport  FROM
( SELECT del.delivery_container as container_code ,dep.product_code as 
product_number,dep.number as distribution_num FROM supply_chain.delivery as del INNER JOIN supply_chain.delivery_product as dep
on del.delivery_code = dep.delivery_code ) as del
INNER JOIN operation.schedule_container as sc
on del.container_code = sc.container_num ) as dde
INNER JOIN supply_chain.order_distribution  as ordd
on dde.container_code = ordd.container_code and dde.product_number = ordd.product_number) AS ci ON ar.container = ci.container_code
            WHERE
                (ar.warehousing_date IS NULL
            OR ar.warehousing_date = '') and sku  is NOT NULL  {0} 
            '''

# 在途货柜的对于产品编号的sql
transit_product_sql = '''
SELECT ci.product_number, {1} SUM(IF(ci.transport='FBA' OR ci.transport='海外仓',ci.distribution_num,0)) as sum_num  ,
SUM(IF(ci.transport='FBA',ci.distribution_num,0)) AS 'FBA',
SUM(IF(ci.transport='海外仓',ci.distribution_num,0)) AS 'FBM'
{2}
FROM
	arrival_receive AS ar
INNER JOIN (SELECT dde.*,ordd.distribution_num,ordd.sku ,ordd.store as site,ordd.country from  ( SELECT del.* , sc.warehouse_type as transport  FROM
( SELECT del.delivery_container as container_code ,dep.product_code as 
product_number,dep.number FROM supply_chain.delivery as del INNER JOIN supply_chain.delivery_product as dep
on del.delivery_code = dep.delivery_code ) as del
INNER JOIN operation.schedule_container as sc
on del.container_code = sc.container_num ) as dde
INNER JOIN supply_chain.order_distribution  as ordd
on dde.container_code = ordd.container_code and dde.product_number = ordd.product_number) AS ci ON ar.container = ci.container_code
WHERE
	(ar.warehousing_date IS NULL
OR ar.warehousing_date = '') 
GROUP BY product_number {2} 
ORDER BY product_number
'''
# 对应产品编码的对于的产品的FBA和FBM库存
inventory_sql = '''
SELECT cor.product_code ,cor.sku AS SKU,cor.fbm AS FBM, IFNULL(ordc.FBA,0) AS FBA ,
IFNULL(cor.fbm,0) + IFNULL(ordc.FBA,0) as sum_spu FROM 
( SELECT cor.product_code,cor.sku,cor.spu,IFNULL(fbm_ord.nums,0) as fbm from
 (SELECT spu,sku,product_code FROM  commodity_information WHERE  country ='{0}' AND site ='{1}' )as cor
LEFT JOIN (SELECT spu,sku,nums  from fbm_data 
WHERE times = (SELECT DISTINCT times FROM fbm_data WHERE area in {6} ORDER BY times DESC LIMIT 0,1)
 and area in {6} ) as fbm_ord on cor.spu = fbm_ord.spu and cor.sku = fbm_ord.sku
 )as cor  LEFT JOIN ( 
select spu, sku,
SUM(CASE WHEN times ='{5}' THEN fba  END) as 'FBA',
SUM( CASE WHEN times = '{5}' THEN fba END ) AS 'sum_spu',
 SUM(nums) as nums_count
 from {4} where  company='{2}' and countries='{3}' 
 GROUP BY spu,sku               
ORDER BY spu DESC )  ordc
on cor.spu = ordc.spu and  ordc.sku LIKE CONCAT('%',cor.sku,'%')
ORDER BY cor.product_code

'''
# 在途的产品编码的产品的FBA和FBM库存
in_transit_inventory = '''
        SELECT ci.product_number,ci.sku,
        SUM(IF(ci.transport='FBA',ci.distribution_num,0)) AS 'FBA',
        SUM(IF(ci.transport='海外仓',ci.distribution_num,0)) AS 'FBM',
        SUM(IF(ci.transport='海外仓' OR ci.transport='FBA',ci.distribution_num,0)) AS sum_num

        FROM
                arrival_receive AS ar
        INNER JOIN supply_chain.order_distribution AS ci ON ar.container = ci.container_code
        WHERE
                (ar.warehousing_date IS NULL
        OR ar.warehousing_date = '') and sku  is NOT NULL {0}
        GROUP BY product_number,sku
        ORDER BY product_number

        '''
# 所有国家站点下的产品信息
product_msg_sql = '''
    SELECT site,country,product_type,cor.product_code,product_name,cor.spu,cor.sku 
    FROM product_message as pr INNER JOIN commodity_information as cor 
WHERE pr.product_code = cor.product_code {0}
ORDER BY country,site,cor.product_code
'''

# order_sql

recent_order_sql = '''
SELECT sku, convert(COUNT(sku)/10,decimal(10,2)) as order_num, convert(SUM(price)/10,decimal(10,2)) as price FROM order_record 
WHERE DATE_SUB(CURDATE(), INTERVAL 10 DAY) <= date(purchase_date) {0}
GROUP BY sku
'''