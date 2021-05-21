import calendar
from datetime import date, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
import time
from order_management.settings import order_sql
from settings import conf_fun
from datetime import date, datetime, timedelta


def change_site_country(site, country):
    if country in ['德国', '法国', '意大利', '西班牙', '英国']:
        country = '欧洲'
    site_sql = " SELECT * FROM area_contrast WHERE area_cn ='{0}' ".format(site)
    site_data = conf_fun.connect_mysql_operation(site_sql, type='dict')

    country_sql = " SELECT * FROM country_contrast WHERE country_cn ='{0}'".format(country)
    country_data = conf_fun.connect_mysql_operation(country_sql, type='dict')
    try:
        site_cn = site_data[0].get('area') if site_data else ''
        country_cn = country_data[0].get('country') if country_data else ''
    except:
        site_cn = ''
        country_cn = ''
    return site_cn, country_cn


class Inventory_page(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': ''}

    def list(self, request):
        data = request.GET
        re_data = []
        site = data.get('site')
        country = data.get('country')

        table_name = 'order_sublist' if country in ['英国', '法国', '意大利', '西班牙'] else 'sku_report'
        site_en, country_en = change_site_country(site, country)
        if country_en in ['US', 'EU', 'CA', 'UK', 'IT', 'DE', 'FR', 'ES']:
            if country_en in ['EU', 'UK', 'IT', 'DE', 'FR', 'ES']:
                fbm_country = ('UKPJ', 'DEPJ', 'FRWH', 'ITWH')
            elif country_en == 'CA':
                fbm_country = ('CA_YYZ', 'CA_YOW')
            else:
                fbm_country = ('PJWL', 'NJPJ', 'USA_LA')
        else:
            fbm_country = ('xxx', 'zzzz')

        ser_str = ""
        product_msg_str = ""
        order_msg_str = ""
        for k, v in data.items():
            if k in ['country', 'site'] and v:
                if k == 'site':
                    ser_str += " AND ci.store ='%s'" % (v)
                    product_msg_str = " AND %s ='%s'" % (k, v)
                    order_msg_str = " AND %s ='%s'" % (k, v)
                elif k =='country':
                    ser_str += " AND ci.%s ='%s' " % (k, v)
                    if v in['英国','法国','德国','意大利','西班牙']:
                        pro_v = '欧洲'
                    else: pro_v = v
                    product_msg_str += " AND %s ='%s'" % (k, pro_v)
                    order_msg_str += " AND country_code ='%s'" % (v)
        date_every_sql = order_sql.date_every_sql.format(site_en, country_en, table_name)
        print('\n71获取fba最近的日期',date_every_sql)
        fba_date = conf_fun.connect_mysql_re(date_every_sql, type='dict')

        try:
            fba_date = fba_date[0].get('times')
        except:
            fba_date = time.strftime('%Y-%m-%d', time.localtime())

        product_msg_sql = order_sql.product_msg_sql.format(product_msg_str)
        print('product_msg_sql\n', product_msg_sql)
        if country in ['英国','法国','德国','意大利','西班牙']:
            country_ch = '欧洲'
        else: country_ch = country
        inventory_sql = order_sql.inventory_sql.format(country_ch, site, site_en, country_en, table_name, fba_date,
                                                       fbm_country)
        recent_order_sql = order_sql.recent_order_sql.format(order_msg_str)
        in_transit_inventory_sql = order_sql.in_transit_inventory.format(ser_str)

        in_transit_inventory_data = conf_fun.connect_mysql_product_supplier(in_transit_inventory_sql, type='dict')

        product_msg_data = conf_fun.connect_mysql_operation(product_msg_sql, type='dict')

        print('inventory_sql\n', inventory_sql)
        inventory_date = conf_fun.connect_mysql_re(inventory_sql, type='dict')

        recent_order_data = conf_fun.connect_mysql_operation(recent_order_sql, type='dict')
        print(recent_order_sql)

        for product_msg_dict in product_msg_data:
            temporary_dict = {}
            temporary_dict['platform'] = 'Amazon'
            temporary_dict['order_num'] = 0
            temporary_dict['price'] = 0
            site = product_msg_dict.get('site')
            country = product_msg_dict.get('country')
            product_code = product_msg_dict.get('product_code')
            product_name = product_msg_dict.get('product_name')
            spu = product_msg_dict.get('spu')
            sku = product_msg_dict.get('sku')
            temporary_dict['site'] = site
            temporary_dict['country'] = country
            temporary_dict['product_code'] = product_code
            temporary_dict['product_name'] = product_name
            temporary_dict['spu'] = spu
            temporary_dict['sku'] = sku

            temporary_dict['inventory_fbm'] = 0
            temporary_dict['inventory_fba'] = 0
            temporary_dict['inventory_num'] = 0

            temporary_dict['in_transit_inventory_fbm'] = 0
            temporary_dict['in_transit_inventory_fba'] = 0
            temporary_dict['in_transit_inventory_nums'] = 0

            temporary_dict['order_num'] = 0
            temporary_dict['price'] = 0
            for inventory_dict in inventory_date:
                # 这是查找库存的
                inventory_product_code = inventory_dict.get('product_code')
                inventory_sku = inventory_dict.get('SKU')
                inventory_fbm = float(inventory_dict.get('FBM')) if inventory_dict.get('FBM') else 0
                inventory_fba = float(inventory_dict.get('FBA')) if inventory_dict.get('FBA') else 0
                inventory_num = float(inventory_dict.get('sum_spu')) if inventory_dict.get('sum_spu') else 0
                #                print(product_code == inventory_product_code,sku == inventory_sku)
                if product_code == inventory_product_code and sku == inventory_sku:

                    temporary_dict['inventory_fbm'] = inventory_fbm
                    temporary_dict['inventory_fba'] = inventory_fba
                    temporary_dict['inventory_num'] = inventory_num
                    break

            for in_transit_inventory_dict in in_transit_inventory_data:
                # 这是查找在途的
                in_transit_inventory_product = in_transit_inventory_dict.get('product_number')
                in_transit_inventory_sku = in_transit_inventory_dict.get('sku')
                in_transit_inventory_fbm = float(in_transit_inventory_dict.get('FBM')) if in_transit_inventory_dict.get(
                    'FBM') else 0
                in_transit_inventory_fba = float(in_transit_inventory_dict.get('FBA')) if in_transit_inventory_dict.get(
                    'FBA') else 0
                in_transit_inventory_nums = float(
                    in_transit_inventory_dict.get('sum_num')) if in_transit_inventory_dict.get('sum_num') else 0
                if product_code == in_transit_inventory_product and sku == in_transit_inventory_sku:
                    temporary_dict['in_transit_inventory_fbm'] = in_transit_inventory_fbm
                    temporary_dict['in_transit_inventory_fba'] = in_transit_inventory_fba
                    temporary_dict['in_transit_inventory_nums'] = in_transit_inventory_nums
                    break


            for order_dict in recent_order_data:
                # 这是查找最近订单的
                order_sku = order_dict.get('sku')
                order_num = float(order_dict.get('order_num')) if order_dict.get('order_num') else 0

                price = float(order_dict.get('price')) if order_dict.get('price') else 0
                if sku in order_sku:
                    z = temporary_dict['order_num']
                    y = temporary_dict['price']
                    temporary_dict['order_num'] = z + order_num
                    temporary_dict['price'] = round((y + price) / 2, 2) if y > 0 else price


            sum_inventory = temporary_dict.get('inventory_num') + temporary_dict.get('in_transit_inventory_nums')

            expected_turnover = float(sum_inventory) * temporary_dict.get('price')

            order_num = temporary_dict['order_num']

            expected_days = int(sum_inventory / order_num) if order_num > 0 else 0
            day = date.today()
            now = datetime.now()
            delta = timedelta(days=expected_days)
            n_days_after = now + delta
            temporary_dict['sum_inventory'] = sum_inventory  # 总库存
            temporary_dict['expected_turnover'] = round(expected_turnover, 2)  # 预期营业额
            temporary_dict['days'] = expected_days  # 预期售空天数
            temporary_dict['expected_days'] = n_days_after.strftime('%Y-%m-%d')  # 预期售空日期
            re_data.append(temporary_dict)
        #            temporary_dict.clear()
        page = int(data.get('page')) if data.get('page') else 1
        begin = (page - 1) * 50
        end = (page) * 50
        print(begin, end)
        self.ret['re_leng'] = len(re_data)

        try:

            re_data = re_data
        except:
            re_data = re_data
        self.ret['re_data'] = re_data

        return Response(self.ret)