
product_sql ="SELECT c.product_code,c.product_name,c.category, c.countries,c.the_store,c.sku ,fba,times, nums FROM commodity_codes_zr as c,sku_report as s " \
             " WHERE c.sku =s.sku  AND c.product_code ='{}' " \
             " AND DATE(times)  = CURDATE() -1" \
             " ORDER BY times DESC"

ret = {'code': 200, 'msg':'无'}