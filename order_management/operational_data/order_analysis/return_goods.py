
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from settings import conf_fun


sql = ''' 
        SELECT
        {0}
FROM
    return_goods AS reg
LEFT JOIN order_record AS ore ON reg.order_id = ore.order_id
WHERE reg.id > 0
'''

class Return_Goods(ViewSetMixin,APIView):

    def __init__(self):
        self.ret = {'code': 200}

    def list(self, request):
        data = request.GET
        page = int(data.get('page')) if data.get('page') else 1
        page = (page-1) * 50
        str_1 = ''' reg.*, ore.purchase_date, ore.warehouse_type '''
        str_2 = ''' count(reg.id) as count_data '''
        limit = '  LIMIT {0},50 '.format(page)
        ser_str = ''
        for k, v in data.items():
            if k in ['site', 'country'] and v:
                ser_str += " reg.{0} = '{1}'".format(k, v)
        return_goods_sql = sql.format(str_1, ser_str, limit)
        count_sql = sql.format(str_2, ser_str)
        re_data = conf_fun.connect_mysql_operation(return_goods_sql, type='dict')
        re_count_data = conf_fun.connect_mysql_operation(count_sql, type='dict')
        self.ret['re_data'] = re_data
        self.ret['re_count_data'] = re_count_data
        return Response(self.ret)
