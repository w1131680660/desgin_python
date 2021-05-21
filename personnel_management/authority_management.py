from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import FileResponse, JsonResponse
import pymysql, os, time, hashlib

from settings import conf_fun


# def connect_mysql(sql_text, dbs='operation', type='tuple'):
#     conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='Bymy2021_', db=dbs)
#
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


""" 获取所有人员的对应的角色和账户状态的sql"""


def person_admin():
    admin_sql = "SELECT * FROM userinfo"
    admin_data = conf_fun.connect_mysql_operation(admin_sql, type='dict')

    return admin_data


''' 获取所有的角色和权限'''


def role_permission():
    role_sql = "SELECT * FROM Role"

    role_data = conf_fun.connect_mysql_operation(role_sql, type='dict')

    permission_data = permission()
    for key in permission_data:
        print(key)
    print('\n')
    for num, role_dict in enumerate(role_data):
        role_data[num]['title'] = []
        for permission_dict in permission_data:
            if str(permission_dict['id']) in role_dict['permissions_id']:
                role_data[num]['title'].append(permission_dict['title'])
    print(role_data)
    return role_data


'''获取所有权限和权限路由'''


def permission():
    permission_sql = "SELECT * FROM permission"
    permission_data = conf_fun.connect_mysql_operation(permission_sql, type='dict')

    return permission_data


'''用户角色状态修改语句'''


def user_role_update(roles, real_name, state, account):
    update = "UPDATE  userinfo SET roles ='{0}' ,state='{1}' " \
             "WHERE real_name ='{2}' and account = '{3}'" \
        .format(roles, state, real_name, account)
    print('修改用户状态', update)
    conf_fun.connect_mysql_operation(update)


'''角色权限更新'''


def role_update(role_name, permission_id_str):
    role_date_sql = "UPDATE Role SET permissions_id ='{0}' WHERE role_name ='{1}'".format(role_name, permission_id_str)
    print(role_date_sql)
    conf_fun.connect_mysql_operation(role_date_sql)


'''角色以及权限新增'''


def role_add(role_name, permission_id_str):
    role_add = "INSERT INTO Role (role_name, permissions_id) VALUES ('{0}', '{1}')".format(role_name, permission_id_str)
    conf_fun.connect_mysql_operation(role_add)


class Authority_Management(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request, *args, **kwargs):
        admin_data = person_admin()
        role_data = role_permission()
        permission_data = permission()
        self.ret['user_data'] = admin_data
        self.ret['role_data'] = role_data
        self.ret['permission_data'] = permission_data
        return Response(self.ret)

    def creat(self, request, *args, **kwargs):
        data = request.data
        '''  有关用户信息的  '''
        account = data.get('account')
        state = data.get('state')  # 状态
        real_name = data.get('real_name')  # 真实姓名
        roles = data.get('roles') # 角色
        if account and state and real_name and roles:
            user_role_update(roles, real_name, state, account)
            admin_data = person_admin()
            role_data = role_permission()
            permission_data = permission()
            self.ret['user_data'] = admin_data
            self.ret['role_data'] = role_data
            self.ret['permission_data'] = permission_data
            return Response(self.ret)

        '''有关角色配置的'''
        role_name = data.get('role_name')
        permission_id_list = data.get('permission_id')
        # 判断role是否存在角色表
        print('23232',account, state, real_name, roles)
        if role_name and permission_id_list:
            # 判断role是否存在角色表 存在修改，不在新增
            judge_sql = "SELECT * FROM Role WHERE role_name ='%s'" % (role_name)
            judge_role = conf_fun.connect_mysql_operation(judge_sql, type='dict')
            permission_id_str = ''.join(permission_id_list)
            if judge_role:
                print(judge_role)
                role_update(role_name, permission_id_str)
            else:
                role_add(role_name, permission_id_str)

        return Response(self.ret)


# 新增用户
def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        roles = request.POST.get('roles')

        sql = "select id from userinfo where phone='{}'"
        sql = sql.format(tel)
        res = conf_fun.connect_mysql_operation(sql)
        if len(res) > 0:
            return JsonResponse({"code": "403", "msg": "账号已经存在!"})

        a = hashlib.md5()
        a.update(password.encode(encoding='utf-8'))
        passwd = a.hexdigest()

        sql = "insert into userinfo(account,real_name,password,roles,phone,state,department) values " \
              "('{}','{}','{}','{}','{}','{}','{}')"
        sql = sql.format(tel, name, passwd, roles, tel, '1', '运营')
        conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code": "200", "msg": "新增账号成功!"})
    else:
        return JsonResponse({"code": "404", "msg": "ERROR!"})


# 获取所有职位
def get_all_rolas(request):
    if request.method == 'GET':
        sql = "select distinct role_name from Role"
        res = conf_fun.connect_mysql_operation(sql)
        data = [{"roles": x[0]} for x in res]
        return JsonResponse({"code": "200", "data": data})
    else:
        return JsonResponse({"code": "404", "msg": "ERROR!"})


# 删除用户
def delete_user(request):
    if request.method == 'POST':
        tel = request.POST.get('tel')
        sql = "delete from userinfo where phone='{}'"
        sql = sql.format(tel)
        conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code": "200", "msg": "删除成功!"})
    else:
        return JsonResponse({"code": "404", "msg": "ERROR!"})