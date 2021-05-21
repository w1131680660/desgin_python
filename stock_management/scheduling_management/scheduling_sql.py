



# 排期日历sql
dschedu_sql = "SELECT S.id ,S.schedule_date, S.container_num, S.container_data,S.factory,S.color  " \
             "FROM schedule_container AS S " \
             "WHERE DATE_SUB(CURDATE(), INTERVAL 7 day) <= date(S.schedule_date) {}" \
             "ORDER BY schedule_date"


# 仓库名称sql

warehouse_sql  =    "SELECT warehouse_name,warehouse_type FROM oversea_location_data where warehouse_name !='废弃'"

# 国家
country_sql = "SELECT DISTINCT country FROM parameter where country !=''"

# 类别
product_type_sql = "SELECT DISTINCT product_type FROM parameter where product_type !='' "
# 柜形
container_type_sql = "SELECT DISTINCT container_type FROM parameter where container_type !='' "

# 平台/渠道
channel_sql =  "SELECT DISTINCT platform FROM parameter where platform !=''"
# 站点

site_sql  =  "SELECT DISTINCT site FROM parameter where  site !=''"

# 工厂
factory_sql =  "SELECT DISTINCT factory FROM parameter where  factory !=''"

# 获取商品和对应sku
sku_sql  =  "SELECT sku,commodity_name,product_code,country,site,platform " \
            "FROM commodity_information where  id>0  {0} "

# 新增带运营上传的货柜号
# 待运营上传的资料

# 运营上传的资料 sql 语言

operating_data = ''' SELECT
                    od.*
                FROM
                    operating_data AS od INNER JOIN
                 schedule_container AS sc on od.id > 0  and od.container_num = sc.container_num
                AND od.`status` = '已回传' {0}
                ORDER BY od.container_num desc LIMIT {1},50
'''
# operating_data = "SELECT * FROM  operating_data where id > 0 {0} AND `status` ={2}  " \
#                  "order by container_num DESC LIMIT {1},50"

operating_no_data = ''' SELECT
                    od.*
                FROM
                    operating_data AS od INNER JOIN
                 schedule_container AS sc on od.id > 0  and od.container_num = sc.container_num
                AND od.`status` = '未回传' {0}
                ORDER BY od.container_num desc LIMIT {1},50
'''

# operating_no_data = "SELECT * FROM  operating_data where id > 0 {0} AND `status` ={2}  " \
#                  "order by container_num DESC LIMIT {1},50"

# 更新运营上传文件资料
update_file_sql = "UPDATE operating_data SET {} WHERE id >0{}"

# 货柜建设的前50条数据
container_search_sql = " SELECT ar.*, su.delivery_date AS shipping_date,ca.warehouse_name , ca.warehouse_no,ca.sku,cargo_num " \
                       " FROM arrival_receive AS ar LEFT JOIN supply_chain.delivery AS su ON ( SUBSTRING_INDEX(ar.container, '-', 1) = su.delivery_container) " \
                       " LEFT JOIN cargo_information as ca on( SUBSTRING_INDEX(ar.container, '-', 1) = ca.container_num ) " \
                       "WHERE ar.id > 0 {0} order by ar.container DESC limit {1},50"

count_sql =   " SELECT count(ar.id) as count_data" \
              " FROM arrival_receive AS ar LEFT JOIN supply_chain.delivery AS su ON ( SUBSTRING_INDEX(ar.container, '-', 1) = su.delivery_container) " \
              " LEFT JOIN cargo_information as ca on( SUBSTRING_INDEX(ar.container, '-', 1) = ca.container_num ) " \
                "WHERE ar.id > 0 {0} "

# sku 前50调数据
container_search_sku_sql = "  SELECT ar.*,ca.warehouse_name,ca.warehouse_no,ca.sku,ca.cargo_num " \
                       "FROM arrival_receive as ar ,cargo_information as ca " \
                       "WHERE ar.container = ca.container_num {0} limit {1},50"

# SKU的搜索
sku_search_sql = "  SELECT distinct ca.sku as sku " \
                       "FROM arrival_receive as ar ,cargo_information as ca " \
                       "WHERE ar.container = ca.container_num {0} "



count_sku_sql =  "  SELECT count(ar.id) as count_data" \
                       " FROM arrival_receive as ar ,cargo_information as ca " \
                       " WHERE ar.container = ca.container_num {0} "
# 货柜检索下拉框数据
country_ser_sql  = " SELECT DISTINCT country FROM arrival_receive where  country != '' "

store_ser_sql = "SELECT DISTINCT store FROM arrival_receive where  store != '' "

# 货物，仓库类型
type_ser_sql = "SELECT DISTINCT type FROM arrival_receive where  type != '' "

# 仓库,仓库号类型
warehouse_ser_sql = " SELECT warehouse_name, warehouse_no from cargo_information where warehouse_name !=''  and warehouse_no != '' GROUP BY warehouse_name,warehouse_no"


'''   订单集成 '''
# order_confirmation_sql = " SELECT sc.*, ord.id AS ord_id, ord.*, pr.product_type, pr.product_name, ov.wharf, ov.code as warehouse_id " \
#                          " FROM schedule_container AS sc, order_integration AS ord, product_message AS pr, product_supplier.oversea_location_data as ov " \
#                          " WHERE sc.container_num = ord.container_num AND ord.product_code = pr.product_code AND ov.warehouse_type = sc.warehouse_type  " \
#                          " AND ov.warehouse_name = sc.warehouse_name AND sc.integrated_state = '未集成'  {0}  ORDER BY sc.container_num desc limit {1},50 "

order_confirmation_sql= " SELECT f.* FROM( SELECT f.*,pr.product_type,pr.product_name FROM " \
      " (SELECT sc.unique_id,sc.warehouse_name,sc.platform,sc.site,sc.warehouse_type,sc.schedule_date, " \
      " sc.container_num,sc.country ,ord.product_code,ord.sku,ord.sku_num ,ord.id as ord_id,ord.integrated_state from " \
      " schedule_container AS sc LEFT JOIN order_integration AS ord ON  sc.unique_id = ord.unique_id ) as f " \
      " LEFT JOIN product_message AS pr ON f.product_code = pr.product_code) as f WHERE f.integrated_state = '未集成' {0} " \
                        " ORDER BY f.container_num DESC limit {1},50"

# count_order_sql = " SELECT count(sc.id) as count_data  FROM schedule_container AS sc, order_integration AS ord, product_message AS pr," \
#                   " product_supplier.oversea_location_data as ov " \
#                  " WHERE sc.container_num = ord.container_num AND ord.product_code = pr.product_code AND ov.warehouse_type = sc.warehouse_type  " \
#                  " AND ov.warehouse_name = sc.warehouse_name AND sc.integrated_state = '未集成'  {0} limit {1},50 "

count_order_sql = " SELECT count(f.ord_id) as count_count_data FROM( SELECT f.*,pr.product_type,pr.product_name FROM " \
      " (SELECT sc.id, ord.integrated_state,sc.warehouse_name,sc.platform,sc.site,sc.warehouse_type," \
     " sc.schedule_date, sc.container_num,sc.country ,ord.product_code,ord.sku,ord.sku_num, ord.id as ord_id from " \
      " schedule_container AS sc LEFT JOIN order_integration AS ord ON  sc.unique_id = ord.unique_id ) as f " \
      " LEFT JOIN product_message AS pr ON f.product_code = pr.product_code) as f WHERE f.integrated_state = '未集成' {0} " \
                        " ORDER BY f.container_num "

# 货柜检索的sql

container_true_sql= '''
  SELECT * FROM ( SELECT * FROM (
SELECT * FROM (
SELECT container_num,schedule_date,country,site,container_type,factory,warehouse_type,warehouse_name FROM schedule_container ORDER BY schedule_date desc)
as sco
LEFT JOIN
(
SELECT ordd.*,deld.delivery_num FROM 
( SELECT ord.*,con.plan_order_nums from ( SELECT container_code,SUM(distribution_num) as distribution_nums,product_type FROM supply_chain.order_distribution 
WHERE id>0
GROUP BY container_code,product_type ) as ord
LEFT JOIN (SELECT container_code,SUM(plan_order) as plan_order_nums FROM supply_chain.order_integrate WHERE id>0 GROUP BY container_code) as con
on ord.container_code = con.container_code )  as ordd
LEFT  JOIN 
(SELECT delivery_container, SUM(numbers) as delivery_num FROM supply_chain.delivery WHERE id>0  GROUP BY delivery_container ) as deld
on ordd.container_code = deld.delivery_container ) as delo
ON sco.container_num =delo.container_code
ORDER BY sco.schedule_date DESC) as scr_o 
LEFT JOIN
 (SELECT container,carrier,arrival_date,reality_arrival_date,receive_count,issue_count FROM product_supplier.arrival_receive WHERE id>0) as are_o
ON scr_o.container_num = are_o.container
) as ood

WHERE ood.container_num is not NULL {0}
ORDER BY ood.container_num DESC
{1}
'''