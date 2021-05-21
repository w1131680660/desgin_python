from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
import pymysql, os, time
from operator import itemgetter
from itertools import groupby
from settings import conf_fun

# def connect_mysql_supply_chain(sql_text, dbs='supply_chain', type='tuple'):
#     conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql',
#                            passwd='Bymy2021_', db=dbs)
#     if type == 'tuple':
#         cursor = conn.cursor()
#         # ((值, 值),)
#     else:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # [{字段：值},]
#     cursor.execute(sql_text)
#     response = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return response


def down_box():
    down_sql = ' SELECT DISTINCT factory,container_num FROM delivery_product_copy1 where  status ="0"'
    down_data = conf_fun.connect_mysql_factory(down_sql, type='dict')
    re_data = {}
    for factory, items in groupby(down_data, key=itemgetter('factory')):
        if factory not in re_data.keys():
            re_data[factory] = []
        for i in items:
            re_data[factory].append(i.get('container_num'))

    return re_data


def master_upload_file(data):
    import requests
    import json
    url = 'https://www.beyoung.group/add_invoice/'
    # url = ' http://106.53.250.215:9126/add_invoice/'
    # data ={'user_name':'IT-测试','container':'T1000','factory':'合迪'}
    print(data)
    res = requests.get(url, data)
    print(res)
    data_dict = json.loads(res.content)
    file_path = data_dict.get('file_path')
    print(file_path)
    return file_path


class Outhound_Audit(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {}

    def list(self, request):
        # 供应链的出库单sql
        data = request.GET
        factory = data.get('factory')
        container = data.get('container')
        down_data = down_box()
        self.ret['down_data'] = down_data
        if factory and container:
            supply_chain_sql = " SELECT de.delivery_container as container_num ," \
                               " de.delivery_supplier as factory,dp.product_code as product_code," \
                               " dp.product_name, dp.number as number ,dp.rough_weight, dp.net_weight,dp.volume FROM delivery as de  " \
                               " LEFT JOIN delivery_product as dp ON de.delivery_code = dp.delivery_code " \
                               " WHERE de.delivery_supplier ='{0}' and de.delivery_container ='{1}' ".format(factory,
                                                                                                             container)

            factory_sql = " SELECT container_num,  factory,product_code ,product_name,number,rough_weight, net_weight,volume " \
                          " FROM delivery_product_copy1 WHERE status ='0' and  factory='{0}' AND container_num ='{1}'".format(
                factory, container)

            # supply_chain_dict ={}
            # factory_dict = {}
            different_dict = {}
            same_dict = {}
            index_duct = {}  # 这个是相同的
            index_duct_1 = {}  # 这个不同的
            supply_chain_data = conf_fun.connect_mysql_supply(supply_chain_sql, type='dict')
            factory_data = conf_fun.connect_mysql_factory(factory_sql, type='dict')

            for index, supply_chain_dict in enumerate(supply_chain_data):
                for index_1, factory_dict in enumerate(factory_data):
                    print(factory_dict.values(), type(factory_dict.values()), '\n', supply_chain_dict.values(), '\n\n')
                    if len(factory_dict.items() - supply_chain_dict.items()) == 0:

                        same_dict[index] = [supply_chain_dict, factory_dict]
                        index_duct[index] = index_1
                    elif factory_dict.items() - supply_chain_dict.items() and \
                            supply_chain_dict.get('product_code') == factory_dict.get('product_code'):
                        different_dict[index] = [supply_chain_dict, factory_dict]
            print(index_duct, index_duct_1)
            self.ret['different_data'] = different_dict
            self.ret['same_data'] = same_dict

        return Response(self.ret)

    def create(self, request):
        data = request.data

        factory = data.get('factory')
        container = data.get('container')
        user_name = data.get('user_name')

        go_data = {'factory': factory, 'container': container, 'user_name': user_name}
        file_path = master_upload_file(go_data)
        update_sql = " update delivery_product_copy1 set status ='1' where container_num ='{0}' " \
                     "and factory ='{1}'".format(container, factory)

        judge_sql = " SELECT * FROM invoice WHERE container ='{0}' AND factory ='{1}'".format(container, factory)
        re_judge_data = conf_fun.connect_mysql_factory(judge_sql, type='dict')
        if not re_judge_data:
            insert_sql = " INSERT invoice (container,factory,invoice_path ) VALUES ( '{0}', '{1}','{2}')".format(
                container, factory, file_path)
            conf_fun.connect_mysql_factory(insert_sql, type='dict')
        conf_fun.connect_mysql_factory(update_sql, type='dict')
        return Response(self.ret)

    def alter(self, request):
        data = request.data
        factory = data.get('factory')
        container = data.get('container')
        update_sql = " update delivery_product_copy1 set status ='2' where container_num ='{0}' " \
                     "and factory ='{1}'".format(container, factory)
        conf_fun.connect_mysql_factory(update_sql, type='dict')
        return Response(self.ret)

    def delete(self, request):
        pass
