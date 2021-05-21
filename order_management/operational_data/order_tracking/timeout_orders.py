
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from settings import conf_fun



# 获取超时订单

#     ''' 肖飞 2020-1-21 10:05'''
class Timeout_Order(ViewSetMixin , APIView):

    def __init__(self):
        self.ret = {'code':200,'msg':'无'}

    def list(self,request):
        data = request.GET
        print(data)
        page = data.get("page")
        page_num = (int(page) - 1) * 50 if page else 0

        timeout_sql = "select * from timeout_orders where status_name ='未处理'  {0} order by dates desc LIMIT {1},50  "
        timeout_count_sql = " select count(id) as count_id from  timeout_orders where id >0 {0}"

        ser_str = ''
        for key, value in data.items():
            if key not in ['page', 'id', 'dates',] and value:
                ser_str += " AND %s = '%s'" % (key, value)

        # 查询所有超时
        timeout_sql = timeout_sql.format(ser_str, page_num)
        timeout_count_sql = timeout_count_sql.format(ser_str)
        print(timeout_sql,'\n')
        print(timeout_count_sql)
        try:
            re_data = conf_fun.connect_mysql_operation(timeout_sql, type='dict')
            print('\n\n',re_data)
            re_count_data = conf_fun.connect_mysql_operation(timeout_count_sql, type='dict')
            self.ret['data'] =re_data
            self.ret['re_count_data'] =re_count_data
            self.ret['msg'] ="success"
            return Response(self.ret)
        except Exception as e:
            self.ret["msg"] = "error:" + str(e)
            return Response(self.ret)


    def alter(self,request):
        data = request.data
        id = data.get('id')
        update_sql = " UPDATE timeout_orders set status_name ='已处理' where id ='%s'"%(id)
        conf_fun.connect_mysql_operation(update_sql)
        return Response(self.ret)
