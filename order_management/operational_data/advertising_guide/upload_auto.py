

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from settings import conf_fun

#    这个是广告组和下的自动和手动关系
class Upload_transform_auto(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200}


    def list(self,request):
        data = request.GET
        print(111111111111111,data)
        ser_str = ''
        for k,v in data.items():
            if v and k in ['auto', 'country','site', 'manual_name', 'automatic_name', ]:
                ser_str += " AND {0} ='{1}' ".format(k ,v)
        ser_str = ser_str.rstrip(' ,')
        ser_sql = " SELECT * FROM transform_auto WHERE id > 0 {0}".format(ser_str)
        print('23行',ser_sql)
        ser_data = conf_fun.connect_mysql_re(ser_sql, type='dict')
        self.ret['code'] = 200
        self.ret['re_data'] = ser_data
        return Response(self.ret)

    def create(self,request):
        ret = {}
        data = request.data
        ser_str = ''
        key_str = ''
        value_str = ''
        for key, value in data.items():
            if value and key in ['auto', 'site','country', 'manual_name', 'automatic_name', ]:
                ser_str += " AND %s ='%s'" % (key, value.strip())
                key_str += " %s ," % (key)
                value_str += " '%s' ," % (value.strip())
        key_str = key_str.rstrip(' ,')
        value_str = value_str.rstrip(' ,')
        judge_sql = " SELECT * FROM transform_auto WHERE id > 0 {0}".format(ser_str)
        re_judge_data = conf_fun.connect_mysql_re(judge_sql)
        if re_judge_data:
            ret['code'] = 500
            ret['msg'] = ' 该自动和手段组名称已存在，请勿重复新增'
        else:
            inster_sql = " INSERT INTO transform_auto ( {0} ) VALUES ( {1} )".format(key_str, value_str)
            print('\ninster_sql,47',inster_sql)
            conf_fun.connect_mysql_re(inster_sql)
            ret['code'] = 200
            ret['msg'] = '新增成功'
        return Response(self.ret)

    def alter(self,request):
        data = request.data
        update_str =''
        for k ,v in data.items():
            if v and k in ['auto', 'country', 'manual_name', 'automatic_name', ]:
                update_str += " {0} ='{1}' ,".format(k ,v.strip())
        update_str = update_str.rstrip(' ,')
        id = data.get('id')
        update_sql = " UPDATE transform_auto SET {0} WHERE {1}".format(update_str, " id = '%s'"%(id))
        print('\n62',update_sql)
        conf_fun.connect_mysql_re(update_sql)
        return Response(self.ret)

    def delete(self,request):
        data = request.GET
        id = data.get('id')
        del_sql = " DELETE FROM transform_auto where id ='%s'"%(id)
        conf_fun.connect_mysql_re(del_sql)
        return Response(self.ret)

# 这个是广告组和spu的对应关系
class Upload_auto_ad(ViewSetMixin, APIView):
    def __init__(self):
        self.ret = {'code':200}

    def list(self, request):
        data = request.GET
        ser_str = ''
        for k, v in data.items():
            if v and k in ['auto', 'country', 'company', 'type', 'spu']:
                ser_str += " AND {0} ='{1}' ".format(k, v.strip())
        ser_str = ser_str.rstrip(' ,')
        ser_sql = " SELECT * FROM auto_ad  WHERE id > 0 {0}".format(ser_str)
        print('这个\n',ser_sql)
        ser_data = conf_fun.connect_mysql_re(ser_sql, type='dict')
        self.ret['code'] = 200
        self.ret['re_data'] = ser_data
        return Response(self.ret)

    def create(self, request):

        data = request.POST
        ser_str = ''
        key_str = ''
        value_str = ''
        for key, value in data.items():
            if value and key in ['auto', 'country', 'company', 'type', 'spu','site'] :
                ser_str += " AND %s ='%s'" % (key, value.strip())
                key_str += " %s ," % (key)
                value_str += " '%s' ," % (value.strip())
        key_str = key_str.rstrip(' ,')
        value_str = value_str.rstrip(' ,')
        judge_sql = " SELECT * FROM auto_ad WHERE id > 0 {0}".format(ser_str)
        re_judge_data = conf_fun.connect_mysql_re(judge_sql)
        if re_judge_data:
            self.ret['code'] = 500
            self.ret['msg'] = ' 该自动和手段组名称已存在，请勿重复新增'
        else:
            inster_sql = " INSERT INTO auto_ad ({0}) VALUES ( {1} )".format(key_str, value_str)
            print('\ninsert_sql 120',inster_sql)
            conf_fun.connect_mysql_re(inster_sql)
            self.ret['code'] = 200
            self.ret['msg'] = '新增成功'
        return Response(self.ret)

    def alter(self, request):
        data = request.data
        update_str = ''
        for k, v in data.items():
            if v and k in ['auto', 'country', 'company', 'type', 'spu']:
                update_str += " {0} ='{1}' ,".format(k, v.strip())
        update_str = update_str.rstrip(' ,')
        id = data.get('id')
        update_sql = " UPDATE auto_ad  SET {0} WHERE {1}".format(update_str, " id = '%s'" % (id))
        print('\n126更新sql',update_sql)
        conf_fun.connect_mysql_re(update_sql)
        return Response(self.ret)

    def delete(self, request):
        data = request.GET
        id = data.get('id')
        del_sql = " DELETE FROM auto_ad where id ='%s'" % (id)
        conf_fun.connect_mysql_re(del_sql)
        return Response(self.ret)

