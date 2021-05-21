from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

import os
from settings import conf_fun

import requests


def master_upload_file(files, file_path):
    url = 'https://www.beyoung.group/file_upload/'
    path2 = os.path.join(r'operation/operating_data/', file_path, )
    data = {'path': path2}
    print(data)
    res = requests.post(url, data, files={'file': files})
    path3 = os.path.join(r'operation/operating_data/', "%s/"%(file_path), str(files))
    print('这是什么路径\n', path3)
    return path3


class Reruen_Report(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        data = request.GET
        ser_str = ''
        for k , v in data.items():
            if k in ['platform', 'country', 'site', 'month', 'type'] and v:
                ser_str += " AND {0} ='{1}'".format(k, v)
        ser_str = " SELECT * FROM return_report where id >=0 {0}".format(ser_str)
        re_data = conf_fun.connect_mysql_operation(ser_str, type='dict')
        self.ret['re_data'] = re_data
        return Response(self.ret)

    def create(self, request):
        data = request.data
        k_str = ''
        v_str = ''
        judge_str = ''
        update_str = ''
        for k, v in data.items():
            if k in ['platform', 'country', 'site', 'month', 'type'] and v:
                k_str += " {0} ,".format(k)
                v_str += " '{0}' ,".format(v)
                judge_str += " AND {0} ='{1}'".format(k, v)
            elif k == 'file_path':
                k_str += " {0}".format(k)
                v_1 = master_upload_file(v, 'return_report')
                v_str += " '{0}' ".format(v_1)
                update_str += " {0} ='{1}'".format(k, v_1)
        k_str = k_str.strip(' , ')
        v_str = v_str.strip(' , ')
        judge_sql = " SELECT * FROM return_report where id >=0 {0}".format(judge_str)
        print(judge_sql,'\n55')
        re_judge_data = conf_fun.connect_mysql_operation(judge_sql, type='dict')
        if not re_judge_data:
            insert_sql = " INSERT INTO return_report ( {0} ) VALUE ( {1} )".format(k_str, v_str)
            print(insert_sql)
            conf_fun.connect_mysql_operation(insert_sql)
        else:
            id = re_judge_data[0].get('id')
            update_sql = " UPDATE return_report SET  {0} where id ='{1}'".format(update_str,id)
            conf_fun.connect_mysql_operation(update_sql)
            print(update_sql)
        return Response(self.ret)
