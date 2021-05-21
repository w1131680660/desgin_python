from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from operator import itemgetter
from itertools import groupby
from settings import conf_fun,settins_func



def upload_file(file_list):
    path =''
    for i in file_list:
        path += "%s@"%(settins_func.bug_upload(i,'bug_file'))
    path = path.strip('@')
    return path

def fuzzy_matching(condition, field_list):
    field_str = " "
    for i in field_list:
        field_str += " IFNULL(%s, '') ," % (i)
    field_str = field_str.rstrip(' ,')
    where_str = " AND CONCAT( {0} ) LIKE CONCAT('%', '{1}', '%')".format(field_str, condition)
    return where_str

class Bug_Return(ViewSetMixin, APIView):


    def __init__(self):
        self.ret = {'code' : 200}
        self.system_name = '运营系统'

    def list(self, request):
        data = request.GET
        field_list = ['initiator','initiate_time','system_name','project_name','data_status']
        condition = data.get('condition')
        if condition and field_list:
            where_str = fuzzy_matching(condition, field_list)
        else:
            where_str = ''
        down_sql = " SELECT * FROM page_mg WHERE system_name ='%s' "%(self.system_name)
        ser_sql = ''' SELECT id,initiator,project_name,page_name,description,suggest,
                   expect_time,it_time,data_status,cp_note,zj_note,pic_url FROM feedback_task 
                   where system_name ='{0}' {1} 
                   ORDER BY FIELD(`data_status`, '已提起', '待分配', '进行中', '已完成','已驳回') 
                   '''.format(self.system_name, where_str)
        print(ser_sql)
        down_dict = {}
        down_data = conf_fun.connect_mysql_operation(down_sql, dbs='task_distribution', type='dict')
        for project_name,items in groupby(down_data,key=itemgetter('project_name')):
            if project_name not in down_dict:
                down_dict[project_name] = []
            for i in items:
                page_name = i.get('page_name')
                down_dict[project_name].append(page_name)

        ser_sql += " and need_type!='IT'"
        print("查询语句: ", ser_sql)
        re_data = conf_fun.connect_mysql_operation(ser_sql, dbs='task_distribution', type='dict')
        self.ret['down_data'] = down_dict
        self.ret['re_data'] = re_data
        return Response(self.ret)

    def create(self,request):
        data = request.data
        key_str = ''
        value_str = ''
        for k,v in data.items():
            if k == 'pic_url' and v:
                key_str +=" %s ,"%(k)
                value_str += " '%s',"%upload_file(data.getlist('pic_url'))
            else:
                key_str += " %s , " %(k)
                value_str += " '%s' , "%(v)
        key_str += ' system_name,data_status'
        value_str += ''' '%s','已提起' '''%(self.system_name)

        insert_sql = " INSERT INTO feedback_task ( {0} ) VALUES ({1} )".format(key_str, value_str)
        print(insert_sql)
        conf_fun.connect_mysql_operation(insert_sql, dbs='task_distribution', type='dict')
        return Response(self.ret)

    def alter(self,request):
        data = request.data
        update_str = ''
        for k,v in data.items():
            if k =='pic_url' and v:
                update_str += " {0} ='{1}'".format(k,upload_file(data.getlist('pic_url')))
            elif k in ['description','suggest'] and v:
                update_str += " {0} = '{1}' , ".format(k ,v)
        update_str = update_str.strip(' , ')
        update_sql = " UPDATE feedback_task SET {0} WHERE  id ='{1}'".format(update_str ,data.get('id'))
        print(update_sql)
        conf_fun.connect_mysql_operation(update_sql, dbs='task_distribution', type='dict')
        return Response(self.ret)

    def delete(self, request):
        data = request.GET
        id_list = data.getlist('id')
        for id in id_list: 
            sql = " DELETE FROM feedback_task where  id ='%s' and data_status='已提起' " %(id)
            print(sql)
            conf_fun.connect_mysql_operation(sql, dbs='task_distribution', type='dict')
        return Response(self.ret)

from django.http import JsonResponse

def delete_page(request):
    data = request.GET
    id_list = data.getlist('id')
    for id in id_list: 
        sql = " DELETE FROM feedback_task where  id ='%s' and data_status='已提起' " %(id)
        print(sql)
        conf_fun.connect_mysql_operation(sql, dbs='task_distribution', type='dict')
    ret ={'code':200}
    return JsonResponse(ret)