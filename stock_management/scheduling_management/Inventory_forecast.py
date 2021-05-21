from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from stock_management import scheduling_settings

from itertools import groupby
from operator import itemgetter

from settings import conf_fun
country_dict = {
    '澳洲': 'AU',
    '加拿大': 'CA',
    '西班牙': 'ES',
    '英国': 'UK',
    '法国': 'FR',
    '意大利': 'IT',
    '德国': 'DE',
    '日本': 'JP',
    '美国': 'US',
    '墨西哥': 'MX',
    '新加坡': 'SG',
    '马来西亚': 'MY',
}

site_dict = {
    '胤佑': 'YY',
    '京汇': 'JH',
    '中睿': 'ZR',
    '爱瑙': 'AN',
    '利百锐': 'LBR',
    '笔漾教育': 'BYJY',
    '景瑞': 'JR'}

def inventory_func(data):
    country = data.get('country')
    ser_str = ''
    for k , v in data.items():
        if k == 'country' and v:
            ser_str += "  AND countries = '{0}'".format(country_dict.get(v))
        elif k == 'site' and v:
            ser_str += " AND company = '%s'" % (site_dict.get(v))
        elif k =='spu':
            ser_str += " AND spu ='%s'"%(v)

    eu_sql = " SELECT spu, SUM(fba) as sum_num, times FROM {0} WHERE id >0 {1} " \
             "GROUP BY spu,times ORDER BY times DESC limit 0,1"
    if country in ['德国', '英国', '法国', '意大利', '西班牙']:
        inventory_sql = eu_sql.format('order_sublist', ser_str)
    else:
        inventory_sql = eu_sql.format('sku_report', ser_str)

    inventory_data = conf_fun.connect_mysql_re(inventory_sql, type='dict')
    if inventory_data:
        inventory_data = inventory_data[0]
    else:
        inventory_data = [{}]

    return inventory_data

class Inventory_Forcast(ViewSetMixin, APIView):

    def __init__(self):

        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        data = request.GET
        page = data.get('page') if data.get('page') else 1
        page_num = (int(page) - 1) * 50
        sql = " SELECT * FROM Inventory_forecast WHERE id >0 {0}  order by ready_month desc limit {1},50 "
        count_sql = " SELECT count(id) as count_num FROM Inventory_forecast WHERE id >0 {0} "
        ser_str = ""
        spu_1 = data.get('spu')

        for k, v in data.items():
            if k in ['country', 'site', 'spu'] and v:
                ser_str += "AND {0} ='{1}'".format(k, v)
        sql = sql.format(ser_str, page_num)
        sku_spu_sql = " SELECT * FROM sku_inventory_forecast where  id >0 {0}".format(ser_str)
        print(sql)
        print(sku_spu_sql)
        count_sql = count_sql.format(ser_str)
        re_data = scheduling_settings.connect_mysql_operate(sql, type='dict')
        re_count = scheduling_settings.connect_mysql_operate(count_sql, type='dict')
        sku_spu_data = scheduling_settings.connect_mysql_operate(sku_spu_sql, type='dict')
        re_data_dict = {}
        re_data_list = []

        ''' 计算库存和发货数量'''
        re_inventory_data = inventory_func(data)
        for spu, items in groupby(re_data, key=itemgetter('spu')):
            if spu not in re_data_dict.keys():
                re_data_dict[spu] = {}
            if spu not in re_data_list :
                re_data_list.append(spu)
            if spu_1:
                self.ret['re_sku_data'] = sku_spu_data
                for i in items:
                    id = i.get('id')
                    before_month_2 = i.get('before_month_2')
                    before_month_1 = i.get('before_month_1')
                    before_month = float(i.get('before_month')) if i.get('before_month') else 0
                    ready_month = float(i.get('ready_month'))  if i.get('ready_month') else 0
                    coefficient = float(i.get('coefficient')) if i.get('coefficient') else 0
                    date = i.get('date')
                    #预期修正
                    expected_num = ready_month * coefficient
                    # 下个月剩余库存
                    last_month_inventory = expected_num * coefficient
                    # 应有库存
                    should_inventory = before_month * coefficient
                    # 实际库存
                    actual_inventory = float(re_inventory_data.get('sum_num')) if re_inventory_data.get('sum_num') else 0
                    # 安全库存
                    safety_inventory = last_month_inventory - expected_num
                    # 发货数量
                    ship_num = last_month_inventory + expected_num - actual_inventory
                    re_data_dict[spu] = {
                        'before_month_2': before_month_2, 'before_month_1': before_month_1,
                         'id': id, 'before_month': before_month, 'ready_month': ready_month,
                         'coefficient': coefficient, 'date': date,'expected_num':expected_num,
                        'last_month_inventory':last_month_inventory,'should_inventory':should_inventory,
                        'safety_inventory':safety_inventory, 'ship_num':ship_num,'actual_inventory':actual_inventory,
                    }

        self.ret['re_spu_list'] = re_data_list
        self.ret['re_spu_data'] = re_data_dict
        # self.ret['re_count'] = re_count

        return Response(self.ret)

    def create(self, request):
        data = request.data
        id = data.get('id')
        coefficient = data.get('coefficient').strip()
        sql = " UPDATE Inventory_forecast SET coefficient ='{0}'  WHERE  id ='{1}'".format(coefficient,id)
        print('\n',136,sql)
        scheduling_settings.connect_mysql_operate(sql)
        return Response(self.ret)


