
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

from settings import conf_fun

return_sql = ''' 
        SELECT {3} FROM (
SELECT site, country, sku,  product_code,product_name, name_shop, COUNT(sku) AS return_sku
FROM
	refund_dbs
WHERE
	id > 0
{0}
GROUP BY
	site,country,sku,product_code,product_name,name_shop
) as return_1
LEFT JOIN (SELECT site,country_code,sku,COUNT(sku) as ord_sku FROM order_record 
WHERE id > 0 {1}
GROUP BY site,country_code,sku ) as ord_1
ON return_1.sku = ord_1.sku
WHERE return_1.sku is not null and LENGTH(trim(return_1.sku))>0
ORDER BY return_1.return_sku  DESC,return_1.sku DESC  {2} 
'''

class Order_Return(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200}

    def list(self, request):
        data = request.GET
        page = data.get('page') if data.get('page') else 1
        page = (int(page) - 1) * 50
        ser_str = ""
        ord_ser_str =''
        for k, v in data.items():
            if k == 'country':
                ord_ser_str += " and country_code = '{0}'".format(v)
            elif k == 'site':
                ord_ser_str += "and  site ='{0}' ".format(v)
            if k in ['platform', 'country', 'site', 'sku'] and v:
                ser_str += " and {0} ='{1}' ".format(k, v)
            elif k =='date' and v:
                ord_ser_str +=' and  DATE_SUB(CURDATE(), INTERVAL {0} DAY) <= date(purchase_date)'.format(v)
                ser_str += ' and  DATE_SUB(CURDATE(), INTERVAL {0} DAY) <= date(date)'.format(v)

        limit = " limit {0}, 50".format(page)
        sql = return_sql.format(ser_str,ord_ser_str, limit,'return_1.*,ord_1.ord_sku')
        count_sql = return_sql.format(ser_str,ord_ser_str,'','  COUNT(return_1.sku) as count_data')
        print(count_sql)
        re_data = conf_fun.connect_mysql_operation(sql, type='dict')
        count_data = conf_fun.connect_mysql_operation(count_sql, type='dict')
        self.ret['re_data'] = re_data
        self.ret['count_data'] = count_data
        return Response(self.ret)
