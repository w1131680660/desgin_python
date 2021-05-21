
# 查询美国的所有订单
sql_usa = "SELECT  r.platform_channels,COUNT(o.sku) as sku_count ,r.the_store,o.country_code, o.sku " \
          "from `order`.manually_create_order as  o  ,reports.commodity_codes_zr as r " \
          "WHERE o.sku = r.sku AND o.country_code = r.countries {}" \
          " GROUP BY r.platform_channels,o.country_code,r.the_store,o.sku"


'''查询美国的日期订单'''

sql_date_usa = " SELECT r.platform_channels, o.country_code, r.the_store, o.sku, COUNT(o.sku) as count, DATE_FORMAT(o.get_dates ,'%Y-%m' ) months " \
               "FROM manually_create_order AS o, reports.commodity_codes_zr AS r " \
               "WHERE o.sku = r.sku  AND o.country_code = r.countries {}" \
               "GROUP BY r.platform_channels, o.country_code, r.the_store, DATE_FORMAT(o.get_dates,'%Y-%m'), o.sku " \
               "ORDER BY DATE_FORMAT(o.get_dates,'%Y-%m') DESC"
# 美国的总和
sql_usa_count =" SELECT COUNT(*) AS count_num" \
               " FROM (SELECT r.platform_channels, o.country_code, r.the_store, o.sku, COUNT(o.sku) as count, DATE_FORMAT(o.get_dates ,'%Y-%m' ) months " \
                "FROM manually_create_order AS o, reports.commodity_codes_zr AS r " \
                "WHERE o.sku = r.sku  AND o.country_code = r.countries {}" \
                "GROUP BY r.platform_channels, o.country_code, r.the_store, DATE_FORMAT(o.get_dates,'%Y-%m'), o.sku " \
                "ORDER BY DATE_FORMAT(o.get_dates,'%Y-%m') DESC ) as  scale "
# sql_usa = sql_usa.format(1231)
# print(sql_usa)
# 查询欧洲订单
sql_eu_count  = " SELECT COUNT(*) AS count_num " \
                 " from ( SELECT  r.platform_channels,COUNT(o.product_sku) as sku_count ,r.the_store,o.country_code,o.product_sku " \
                 "from `order`.manually_create_order_yc as  o  ,reports.commodity_codes_zr as r " \
                 "WHERE o.product_sku = r.sku  {} " \
                 " GROUP BY r.platform_channels,o.country_code,r.the_store,o.product_sku ) as s"

sql_eu_se_count =  " SELECT COUNT(*) AS count_num " \
                 " from ( SELECT  r.platform_channels,COUNT(o.product_sku) as sku_count ,r.the_store,o.country_code,o.product_sku " \
                 "from `order`.manually_create_order_yc as  o  ,reports.commodity_codes_zr as r " \
                 "WHERE o.product_sku = r.sku  {} " \
                 " GROUP BY r.platform_channels,o.country_code,r.the_store,o.product_sku,  DATE_FORMAT(o.dates,'%Y-%m')" \
                "ORDER BY DATE_FORMAT(o.dates,'%Y-%m') ) as s"

sql_eu =  " SELECT  r.platform_channels,COUNT(o.product_sku) as sku_count ,r.the_store,o.country_code,o.product_sku " \
         "from `order`.manually_create_order_yc as  o  ,reports.commodity_codes_zr as r " \
         "WHERE o.product_sku = r.sku  {} " \
         " GROUP BY r.platform_channels,o.country_code,r.the_store,o.product_sku"

sql_eu_data = " SELECT  r.platform_channels,COUNT(o.product_sku) as count ,r.the_store,o.country_code,o.product_sku, DATE_FORMAT(o.dates,'%Y-%m') as date " \
             "from `order`.manually_create_order_yc as  o  ,reports.commodity_codes_zr as r " \
             "WHERE o.product_sku = r.sku  {} " \
             " GROUP BY r.platform_channels,o.country_code,r.the_store,o.product_sku, DATE_FORMAT(o.dates,'%Y-%m') " \
             "ORDER BY DATE_FORMAT(o.dates,'%Y-%m') DESC"
# 查询加拿大
sql_ups = " SELECT  r.platform_channels, COUNT(o.sku) as sku_count ,r.the_store,o.country_code,o.sku " \
          "from `order`.manually_create_order_ups as  o  ,reports.commodity_codes_zr as r " \
          "WHERE o.sku = r.sku AND o.country_code = r.countries  {}" \
          " GROUP BY r.platform_channels,o.country_code,r.the_store,o.sku"

sql_ups_count = " SELECT COUNT(*) AS count_num from  " \
          "( SELECT  r.platform_channels, COUNT(o.sku) as sku_count ,r.the_store,o.country_code,o.sku " \
          "from `order`.manually_create_order_ups as  o  ,reports.commodity_codes_zr as r " \
          "WHERE o.sku = r.sku AND o.country_code = r.countries  {}" \
          " GROUP BY r.platform_channels,o.country_code,r.the_store,o.sku ) as s"

# 所有问题邮件的sku的sql
problem_sql = "SELECT platform,site,problem_type,country,COUNT(sku) as sku_count ,sku from reply_customers {}" \
              "GROUP BY platform,site,country,sku,problem_type"


nice_comment_sql =  "SELECT platform, site, country, COUNT(Praise) as count_praise, Praise,upload_people" \
             " FROM reply_customers  WHERE Praise ='是' {}" \
                "GROUP BY platform, site, country, Praise ,upload_people"


nice_comment_charge_sql = "SELECT COUNT(Praise) as count_all, upload_people FROM reply_customers  " \
                          "where  id >=0 {} GROUP BY upload_people"

nice_comment_ser_sql = "SELECT platform, site, country,	COUNT(Praise) AS count_praise, Praise, upload_people, DATE_FORMAT(upload_time, '%Y-%m') as date " \
                       "FROM reply_customers WHERE Praise = '是' {} " \
                       "GROUP BY platform,site, country, Praise, upload_people, DATE_FORMAT(upload_time, '%Y-%m') " \
                       "ORDER BY DATE_FORMAT(upload_time, '%Y-%m') DESC"

nice_comment_charge_ser_sql ="SELECT COUNT(Praise) as count_all, upload_people,DATE_FORMAT(upload_time, '%Y-%m') as date FROM reply_customers  " \
                              "where  id >=0 {} GROUP BY upload_people,DATE_FORMAT(upload_time, '%Y-%m') " \
                             "ORDER BY DATE_FORMAT(upload_time, '%Y-%m') DESC"


# 问题邮件的汇总sql

# 邮件分析 站点sql
an_site_sql = "SELECT DISTINCT site FROM reply_customers"

# 邮件分析 国家sql
an_country_sql = "SELECT DISTINCT country FROM reply_customers WHERE country !=''"

# 邮件分析的sku 的sql
an_sku_sql = "SELECT DISTINCT sku FROM reply_customers WHERE sku !=''"

# 邮件分析的工厂的sql
an_factory_sql  = "SELECT DISTINCT  factory FROM factory_feedback_1 WHERE factory !=''"

# 邮件分析问题追溯
an_essence_sql = "SELECT DISTINCT  problem_reason FROM reply_customers WHERE problem_reason !=''"

# 邮件分析的问题类型
an_problem_type_sql = "SELECT DISTINCT  problem_type  FROM reply_customers WHERE problem_type !=''"

# 邮件运营人员
an_people_sql = "SELECT DISTINCT  upload_people  FROM reply_customers WHERE upload_people !=''"



# 汇总表
# all_sql  = "SELECT * FROM reply_customers  {0} ORDER BY platform,site,country LIMIT {1},50"

all_sql = "SELECT r.upload_time,r.platform, r.site, r.country,r.order_number,r.sku ," \
          "r.product_name ,f.factory ,r.warehouse_code, r.upload_people,r.problem_reason, r.problem_type" \
          " FROM reply_customers as r , factory_feedback_1 as f " \
          "WHERE r.order_number = f.order_number  {0} " \
          "ORDER BY r.country, r.site,r.upload_time LIMIT {1},50"

count_all_sql = "SELECT count(r.id) as count_data" \
              " FROM reply_customers as r , factory_feedback_1 as f " \
              "WHERE r.order_number = f.order_number  {0} " \


# 按照sku/按照商品的来查询
# sku_sql = "SELECT platform,country,site,product_name,sku,problem_reason,problem_type, COUNT(sku) as count_sku " \
#           "from reply_customers where id > 0 {0}" \
#           "GROUP BY platform, country,product_name,site,sku,problem_reason,problem_type LIMIT {1},50"

sku_sql = "SELECT r.platform,r.site,r.country, r.sku,r.product_name, r.problem_reason ,r.problem_type,COUNT(r.order_number) as count_sku " \
          "FROM reply_customers as r , factory_feedback_1 as f " \
          "WHERE r.order_number = f.order_number  {0}" \
          "GROUP BY r.platform,r.site, r.country, r.sku,r.product_name, r.problem_reason ,r.problem_type LIMIT {1},50"

count_sku_sql = "SELECT count(r.id) as count_data " \
          "FROM reply_customers as r , factory_feedback_1 as f " \
          "WHERE r.order_number = f.order_number  {0}"
# 按照工厂来查询

# factory_sql = "SELECT platform,factory,f.container_num,site,r.sku,problem_reason,r.problem_type,COUNT(r.sku) as count_num,r.upload_time " \
#               "from reply_customers as r , factory_feedback_1 as f " \
#               "WHERE  r.order_number = f.order_number  {0}" \
#               "GROUP BY platform, factory,f.container_num,site,r.sku,problem_reason,r.problem_type,r.upload_time LIMIT {1},50"

factory_sql = "SELECT f.factory,f.container_num, r.problem_reason ,r.sku,r.product_name,r.problem_type,COUNT(r.order_number) as  count_num " \
              "FROM reply_customers as r , factory_feedback_1 as f " \
              "WHERE r.order_number = f.order_number  {0}" \
              "GROUP BY  f.factory,f.container_num, r.sku,r.product_name, r.problem_reason ,r.problem_type LIMIT {1},50"

count_factory_sql = "SELECT count(r.id) as count_data " \
                  "FROM reply_customers as r , factory_feedback_1 as f " \
                  "WHERE r.order_number = f.order_number  {0}" \
 \


# 按照海外仓库类型-+
warehouse_sql ="SELECT r.platform, r.country, r.site, r.problem_reason, r.problem_type, COUNT(r.order_number) AS count_order, r.warehouse_code, f.container_num " \
              "FROM reply_customers as r , factory_feedback_1 as f " \
              "WHERE r.order_number = f.order_number  {0}" \
              "GROUP BY	r.platform, r.country, r.site, r.problem_reason, r.problem_type, r.warehouse_code, f.container_num " \
              "ORDER BY r.country, r.site LIMIT {1},50"

count_warehouse_sql ="SELECT count(r.id) count_data " \
              "FROM reply_customers as r , factory_feedback_1 as f " \
              "WHERE r.order_number = f.order_number  {0}" \


# 按照运营人员
operate_sql ="SELECT r.platform, r.country, r.site, r.problem_reason, r.problem_type, r.upload_people , COUNT(r.order_number) count_order " \
              "FROM reply_customers as r , factory_feedback_1 as f " \
              "WHERE r.order_number = f.order_number {0} " \
              "GROUP BY  r.platform ,r.country , r.site ,r.problem_reason, r.problem_type ,r.upload_people LIMIT {1},50"

count_operate_sql = "SELECT count(r.id) as count_data " \
                  "FROM reply_customers as r , factory_feedback_1 as f " \
                  "WHERE r.order_number = f.order_number {0} "



''' 商品推送 (测评 suprise)'''
# 店铺邮箱
shop_email = "SELECT DISTINCT email , name_shop from store_information"

# 新产品
new_product = "SELECT  * FROM new_product LIMIT 0,20 "

# 老产品
old_product = "SELECT product_code, product_name FROM product_message LIMIT 0,20"

# 国家
country_sql = "SELECT DISTINCT country FROM parameter where country !=''"

# 客户邮箱
customer_sql = "select customer_name, mail FROM customer_information"




