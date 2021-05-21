from operator import itemgetter
from itertools import groupby

from urllib.parse import unquote
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from settings import conf_fun
import json
import os
import requests

def master_upload_file(files,file_path):
    url = 'https://www.beyoung.group/file_upload/'
    path2 = os.path.join(r'operation/operating_data/', file_path, )
    data = {'path':path2}
    print(data)
    res = requests.post(url,data,files={'file':files})
    path3= os.path.join(r'operation/operating_data/',file_path, str(files))
    print('这是什么路径\n',path3)
    return path3

class Oversea_warehouse_barcode(ViewSetMixin, APIView):

    ret = {'code':200,'msg':'无'}

    def list(self,request):
        data = request.GET
        country = data.get('country')
        if country in ['英国','德国','意大利','西班牙','法国']:
            ser_country = '欧洲'
        else: ser_country = country
        site = data.get('site')
        ser_str =''
        for k,v in data.items():
            ser_str +="AND '{0}' ='{1}'".format(k,v)
        sku_sql = ''' SELECT sku FROM commodity_information WHERE country = '{0}' and site ='{1}' '''.format(ser_country,site)
        sku_data = conf_fun.connect_mysql_operation(sku_sql,type='tuple')

        overseas_sql = ''' SELECT * FROM warehouse_barcode WHERE  id >0 {0}'''.format(ser_str)
        overseas_data = conf_fun.connect_mysql_operation(overseas_sql, type='dict')
        self.ret['sku_data'] = sku_data
        self.ret['overseas_data'] = overseas_data

        return Response(self.ret)


    def create(self,request):
        data =request.data
        data_list = data.get('data_list')
        data_list = json.dumps(data_list)
        file = data.get('file')

        for data_dict in data_list:
            country = data_dict.get('country')
            site = data_dict.get('site')
            sku = data_dict.get('sku')
            file_path = master_upload_file(file,'warehouse_barcode')
            insert_sql = ''' INSERT IGNORE INTO warehouse_barcode (country, site, sku,file_path,file_name) 
                    VALUES ('{0}' ,'{1}','{2}' ,'{3}', '{4}') '''.format(country,site,sku,file_path,str(file))
            conf_fun.connect_mysql_operation(insert_sql)

        return Response(self.ret)

    def alter(self,request):
        data =request.data
        country = data.get('country')
        site = data.get('site')
        sku = data.get('sku')

        id = data.get('id')
        file = data.get('file')
        change_str = ''
        if file:
            file_path = master_upload_file(file, 'warehouse_barcode')
            change_str += ",file_path ='{0}',file_name='{1}'".format(file_path,str(file))
        update_sql = ''' UPDATE warehouse_barcode SET country ='{0}', site ='{1}',sku ='{2}' {4}
                            where  id ='{3}' '''.format(country,site,sku,id,change_str)
        conf_fun.connect_mysql_operation(update_sql)

    def delete(self,request):
        data = request.GET
        id = data.get('id')
        delet_sql ="DELETE FROM warehouse_barcode where  id ='{0}' ".format(id)
        conf_fun.connect_mysql_operation(delet_sql)
        return Response(self.ret)

