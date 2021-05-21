import hashlib
import uuid
from rest_framework.views import APIView
import pymysql
from datetime import datetime
from urllib.parse import unquote

from django.utils.deprecation import MiddlewareMixin

from settings import conf_fun


# 连接运营系统数据库
# 连接总数据库
# def connect_mysql(sql_text, dbs='operation', type='tuple'):
#     conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_', db=dbs)
#     if type == 'tuple':
#         cursor = conn.cursor()
#     else:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql_text)
#     response = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return response


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        """
        用户登录认证
        """
        res = {'code': 200}
        data = request.data
        user = data.get('user')
        pwd = data.get('pwd')
        print(data)
        pwd_md5 = hashlib.md5()
        pwd_md5.update(pwd.encode(encoding='utf-8'))
        pwd_true = pwd_md5.hexdigest()
        user_data_sql = "SELECT account,token,permissions_id,state FROM userinfo,Role " \
                        "WHERE account ='{0}' and " \
                        "password ='{1}' " \
                        "AND roles = role_name".format(user, pwd_true)
        user_data = conf_fun.connect_mysql_operation(user_data_sql, type='dict')
        print(user_data)
        print(123, request.data)
        if not user_data:
            res['code'] = 1001
            res['error'] = '用户名或密码错误'
        else:
            uid = str(uuid.uuid4())
            print('uid', uid)
            update_sql = "UPDATE userinfo SET token ='{0}' WHERE account= '{1}' AND password ='{2}'".format(uid, user,
                                                                                                            pwd_true)
            print(update_sql)
            conf_fun.connect_mysql_operation(update_sql)

            request.session[settings.UUID_KEY] = uid
            ''' 获取用户的权限信息'''
            user_data = user_data[0]

            permissions_id_list = user_data.get('permissions_id').split(',')

            ee = ','.join(permissions_id_list)
            print(ee)
            permission_queryset_sql = "SELECT * from permission WHERE id in (%s)" % ee
            print(123, permission_queryset_sql)
            permission_queryset = conf_fun.connect_mysql_operation(permission_queryset_sql, type='dict')
            permission_list = [item['permissions_url'] for item in permission_queryset]
            print('权限路由列表', permission_list)
            request.session[settings.PERMISSION_SESSION_KEY] = permission_list
            res['token'] = uid
        print(res)
        return Response(res)


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """
    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        对用户行为进行监控 用户名/请求路由/携带的参数/日期/时间/
        """

        user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
        user_name = user_info.split("@")[0]
        current_url = request.path_info
        print("+++++++++++++++++++++++++++++++++++++")
        print(current_url)
        request_method = request.method
        print("request_method: ", request_method)
        if request_method == "GET":
            request_param = request.GET
        if request_method == "POST":
            request_param = request.POST
        if request_method == 'PUT':
            request_param = request.POST
        if request_method == 'DELETE':
            request_param = request.GET
        request_data = ""
        for k, v in request_param.items():
            request_data += k + ": " + v + "& "
        request_data = request_data[:-2]
        print("request_data: ", request_data)
        now_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
        print("now_date: ", now_date)
        now_time = datetime.strftime(datetime.today(), "%H:%M:%S")
        print("now_time: ", now_time)
        print("+++++++++++++++++++++++++++++++++++++")
        insert_monitor_log_sql = 'insert into monitor_log(user_name,request_url,' \
                                 'carry_param,request_date,request_time) ' \
                                 'values("%s", "%s", "%s", "%s", "%s");' \
                                 % (user_name, current_url, pymysql.escape_string(request_data), now_date, now_time)
        print("insert_monitor_log_sql: ", insert_monitor_log_sql)
        conf_fun.connect_mysql_operation(sql_text=insert_monitor_log_sql)
