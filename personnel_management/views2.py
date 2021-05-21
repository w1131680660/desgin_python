import hashlib
import uuid
from django.http import JsonResponse
import pymysql
import re
from django.utils.deprecation import MiddlewareMixin

from urllib.parse import unquote
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
PERMISSION_SESSION_KEY = "beyoung_permission_url_list_key"
UUID_KEY = 'UUID_KEY'


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """

        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        print(request.session)
        current_url = request.path_info
        print('UUID', request.session.get('UUID_KEY'))
        UUID = request.session.get('UUID_KEY')
        if not UUID:
            print('没有登录')
            # return HttpResponse('返回登录页面')


        sql2 = "SELECT * FROM permission WHERE permissions_url ='%s' AND method ='%s'" % (current_url, request.method)
        sql2_data = conf_fun.connect_mysql_operation(sql2, type='dict')
        if not sql2_data:
            sql = "INSERT IGNORE INTO permission (permissions_url, method) VALUES ('%s','%s')" % (
            current_url, request.method)
            print(sql)
        #            conf_fun.connect_mysql_operation(sql)

        for valid_url in ['/server/personnel_management/login/', '/admin/.*']:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None
        #
        print('对应请求的所有权限路由', request.session.get('PERMISSION_SESSION_KEY'))
        print('请求路由', current_url)
        print('请求方法', request.method, type(request.method))
        method = request.method
        args_str =''
        if method in ['GET','DELETE']:
            data = request.GET
        elif method in ['POST','PUT']:
            data = request.POST
        else:
            data = {}
        for k, v in data.items():
            args_str += " {0} ={1} ,".format(k,v)
        print(data)
        # permission_list = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[2]
        # print('请求权限1111111111', unquote(request.META.get('HTTP_AUTHORIZATION')))
        # permission_list = permission_list.split(',')
        #	   if type(permission_list) == str:
        #	       permission_list = permission_list.split('')
        #        if not permission_list:
        #            return HttpResponse('未获取到用户权限信息，请登录！')
        #
        # flag = False
        #
        # if permission_list == 'all':
        #     return None
        #
        # for url in permission_list:
        #
        #     reg = "^%s$" % url
        #     print(reg, '-----', current_url)
        #     if re.findall(reg, current_url):
        #         ret = {'code': 500, 'msg': '无权访问'}
        #         print(ret)
        #         return JsonResponse(ret)


# 登陆
def login(request):
    """
    用户登录认证
    :param request:
    :param args:
    :return:
    """
    ret = {'code': 200}
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    print(user, pwd)
    pwd_md5 = hashlib.md5()
    pwd_md5.update(pwd.encode(encoding='utf-8'))
    pwd_true = pwd_md5.hexdigest()
    user_data_sql = "SELECT account,token,permissions_id,state FROM userinfo,Role " \
                    "WHERE account ='{0}' and " \
                    "password ='{1}' " \
                    "AND roles = role_name".format(user, pwd_true)
    # user_data_sql ="SELECT * FROM userinfo WHERE name ='{0}' AND password ='{1}'".format(user,pwd_true)
    user_data = conf_fun.connect_mysql_operation(user_data_sql, type='dict')

    if not user_data:
        ret['code'] = 1001
        ret['error'] = '用户名或密码错误'
    else:
        uid = str(uuid.uuid4())
        print('uid', uid)
        update_sql = "UPDATE userinfo SET token ='{0}' WHERE account= '{1}' AND password ='{2}'".format(uid, user,
                                                                                                        pwd_true)
        print(update_sql)
        conf_fun.connect_mysql_operation(update_sql)

        request.session['UUID_KEY'] = uid
        sql = "select real_name,area from userinfo where account='{}'"
        sql = sql.format(user)
        res = conf_fun.connect_mysql_operation(sql)
        request.session['user_name'] = res[0][0]
        request.session['area'] = res[0][1]
        #     ''' 获取用户的权限信息'''
        user_data = user_data[0].get('permissions_id')

        if user_data != 'all':
            permissions_id_list = user_data.split(',')
            #
            #     ee = ','.join(permissions_id_list)
            #     print(ee)
            permission_queryset_sql = "SELECT * from permission WHERE id in {}"
            permission_queryset_sql = permission_queryset_sql.format(tuple(permissions_id_list))
            #     print(123,permission_queryset_sql)
            permission_queryset = conf_fun.connect_mysql_operation(permission_queryset_sql, type='dict')
            permission_list = [item['permissions_url'] for item in permission_queryset]
        #     print('权限路由列表', permission_list)
        #        request.session[settings.PERMISSION_SESSION_KEY] = permission_list
        else:
            permission_list = 'all'
        #
        ret['token'] = uid
        ret['user_name'] = res[0][0]
        ret['area'] = res[0][1]
        ret['PERMISSION_SESSION_KEY'] = permission_list
    #        response = JsonResponse({'res': '1'})
    #        response.set_cookie('user_name', res[0][0])
    #        response.set_cookie('area', res[0][1])
    #        response.set_cookie('token', uid)
    # print(ret)
    return JsonResponse(ret)


# 修改密码
def update_pswd(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    pwd_md5 = hashlib.md5()
    pwd_md5.update(password.encode(encoding='utf-8'))
    pwd_true = pwd_md5.hexdigest()

    sql = "update userinfo set password='{}' where account='{}'"
    sql = sql.format(pwd_true, account)
    conf_fun.connect_mysql_operation(sql)
    return JsonResponse({"code": 200, "msg": "修改成功!"})


# 锁定
def lock_user(request):
    account = request.POST.get('account')
    sql = "update userinfo set state='1' where account='{}'"
    sql = sql.format(account)
    conf_fun.connect_mysql_operation(sql)
    return JsonResponse({"code": 200, "msg": "锁定成功!"})


# 删除
def delete_user(request):
    account = request.POST.get('account')
    sql = "delete from userinfo where account='{}'"
    sql = sql.format(account)
    conf_fun.connect_mysql_operation(sql)
    return JsonResponse({"code": 200, "msg": "删除成功!"})


# 站点标记
def area_sign(request):
    area = request.POST.get('area')
    account = request.POST.get('account')
    if 'all' in area:
        area = 'all'
    sql = "update userinfo set area='{}' where account='{}'"
    sql = sql.format(area, account)
    conf_fun.connect_mysql_operation(sql)
    return JsonResponse({"code": 200, "msg": "标记成功!"})


# 获取站点标记的数据
def area_sign_data(request):
    account = request.GET.get('account')
    sql = "select area from userinfo where account='{}'"
    sql = sql.format(account)
    res = conf_fun.connect_mysql_operation(sql)
    if len(res) > 0:
        try:
            data = res[0][0].split(',')
        except:
            data = res[0][0]
    else:
        data = []

    sql = "select site,country from store_information where state='在售'"
    res_data = conf_fun.connect_mysql_operation(sql)
    data1 = [{"value": "all", "label": "全部"}]
    for i in res_data:
        data1.append({"value": i[0] + '_' + i[1], "label": i[0] + i[1]})
    #    data1 = [{"value": "all", "label": "全部"}, {"value": "胤佑_美国", "label": "胤佑美国"}, {"value": "爱瑙_美国", "label": "爱瑙美国"},
    #             {"value": "笔漾教育_美国", "label": "笔漾教育美国"}, {"value": "京汇_美国", "label": "京汇美国"},
    #             {"value": "胤佑_加拿大", "label": "胤佑加拿大"}, {"value": "爱瑙_加拿大", "label": "爱瑙加拿大"},
    #             {"value": "胤佑_墨西哥", "label": "胤佑墨西哥"}, {"value": "胤佑_日本", "label": "胤佑日本"},
    #             {"value": "胤佑_澳洲", "label": "胤佑澳洲"}, {"value": "利百锐_日本", "label": "利百锐日本"},
    #             {"value": "中睿_英国", "label": "中睿英国"}, {"value": "京汇_英国", "label": "京汇英国"},
    #             {"value": "爱瑙_英国", "label": "爱瑙英国"}, {"value": "中睿_法国", "label": "中睿法国"},
    #             {"value": "京汇_法国", "label": "京汇法国"}, {"value": "爱瑙_法国", "label": "爱瑙法国"},
    #             {"value": "中睿_德国", "label": "中睿德国"}, {"value": "京汇_德国", "label": "京汇德国"},
    #             {"value": "爱瑙_德国", "label": "爱瑙德国"}, {"value": "中睿_意大利", "label": "中睿意大利"},
    #             {"value": "京汇_意大利", "label": "京汇意大利"}, {"value": "爱瑙_意大利", "label": "爱瑙意大利"},
    #             {"value": "中睿_西班牙", "label": "中睿西班牙"}, {"value": "京汇_西班牙", "label": "京汇西班牙"},
    #             {"value": "爱瑙_西班牙", "label": "爱瑙西班牙"}]
    return JsonResponse({"code": 200, "data": data, "data1": data1})


# 黄健宵 修改于2021-01-20 14:38
# 判断站点标记
def area_sign1(request):
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    print("请求头携带的权限: ", area)
    jx_area = ['Amazon']
    if area == 'all':
        sql = "SELECT site,country FROM store_information"
        data = conf_fun.connect_mysql_operation(sql)
        print("所有权限的侧边栏查询结果", data)
        # jx_area_country = list(set([x[1] for x in data]))
        jx_area_country = []
        for data_item in data:
            if data_item[1] not in jx_area_country:
                jx_area_country.append(data_item[1])
        jx_area_site = []
        for i in range(len(jx_area_country)):
            jx_area_site1 = []
            for j in data:
                if jx_area_country[i] == j[1]:
                    jx_area_site1.append(j[0])
            jx_area_site.append(jx_area_site1)

    else:
        try:
            area_res = area.split(',')
            jx_area_site = []
            jx_area_country = []
            area_all = []

            country_order = ["美国", "加拿大", "英国", "德国", "法国", "意大利", "西班牙", "墨西哥", "日本", "澳洲"]

            # for i in area_res:
            #     print(i)
            # jx_area_country.append(i.split('_')[1])
            # jx_area_country = list(set(jx_area_country))
            jx_area_country = []
            for country_order_item in country_order:
                for area_res_item in area_res:
                    if area_res_item.split('_')[1] == country_order_item:
                        if area_res_item.split('_')[1] not in jx_area_country:
                            jx_area_country.append(area_res_item.split('_')[1])

            for area_res_item in area_res:
                if area_res_item.split('_')[1] not in jx_area_country:
                    jx_area_country.append(area_res_item.split('_')[1])

            for i in range(len(jx_area_country)):
                jx_area_site1 = []
                for j in area_res:
                    print(j.split('_')[1], jx_area_country[i])
                    if jx_area_country[i] == j.split('_')[1]:
                        jx_area_site1.append(j.split('_')[0])
                jx_area_site.append(jx_area_site1)
        except:
            jx_area_site = [[area.split('_')[0]]]
            jx_area_country = [[area.split('_')[1]]]
    return JsonResponse({"code": 200, "data1": jx_area, "data2": [jx_area_country], "data3": [jx_area_site]})


# 获取标记国家
def get_sign_country(request):
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    print('123', area)
    if area == 'all':
        sql = "SELECT DISTINCT country FROM store_information"
        data = conf_fun.connect_mysql_operation(sql)
        area_country = list([x[0] for x in data])
    else:
        try:
            area_res = area.split(',')
            area_country = []
            for i in area_res:
                print(i)
                area_country.append(i.split('_')[1])
            area_country = list(set(area_country))
        except:
            area_country = [[area.split('_')[1]]]
    return JsonResponse({"code": 200, "data": area_country, "data1": "Amazon"})


# 获取标记地区
def get_sign_area(request):
    country = request.GET.get('country')
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    if area == 'all':
        sql = "SELECT site FROM store_information where country='{}'"
        sql = sql.format(country)
        data = conf_fun.connect_mysql_operation(sql)
        area_site = list(set([x[0] for x in data]))
    else:
        try:
            area_res = area.split(',')
            area_site = []
            for i in area_res:
                if i.split('_')[1] == country:
                    area_site.append(i.split('_')[0])
        except:
            area_site = [[area.split('_')[0]]]
    return JsonResponse({"code": 200, "data": area_site})


# 判断站点标记_伟群
def area_sign2(request):
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    print('111111')
    print(area)
    #    data = {"Amazon": {"加拿大":['爱瑙'],{"美国":['爱瑙']}}
    data_dic = {"Amazon": ""}
    data_list = {}
    data_dic1 = {"Amazon": ""}
    data_list1 = {}
    if area == 'all':
        sql = "SELECT site,country FROM store_information"
        data = conf_fun.connect_mysql_operation(sql)
        jx_area_country = list(set([x[1] for x in data]))
        jx_area_site = []
        for i in range(len(jx_area_country)):
            jx_area_site1 = []
            for j in data:
                if jx_area_country[i] == j[1]:
                    jx_area_site1.append(j[0])
            jx_area_site.append(jx_area_site1)

    else:
        try:
            area_res = area.split(',')

            jx_area_site = []
            jx_area_country = []
            area_all = []
            for i in area_res:
                print(i)
                jx_area_country.append(i.split('_')[1])
            jx_area_country = list(set(jx_area_country))
            for i in range(len(jx_area_country)):
                jx_area_site1 = []
                for j in area_res:
                    print(j.split('_')[1], jx_area_country[i])
                    if jx_area_country[i] == j.split('_')[1]:
                        jx_area_site1.append(j.split('_')[0])
                jx_area_site.append(jx_area_site1)

        except:
            jx_area_site = [[area.split('_')[0]]]
            jx_area_country = [[area.split('_')[1]]]
    print(jx_area_country)
    print(jx_area_site)
    for i in range(len(jx_area_country)):
        data_list[jx_area_country[i]] = jx_area_site[i]
        if jx_area_country[i] == '日本':
            country_language = ['日语']
        elif jx_area_country[i] == '德国':
            country_language = ['德语']
        elif jx_area_country[i] == '法国':
            country_language = ['法语']
        elif jx_area_country[i] == '意大利':
            country_language = ['意大利语']
        elif jx_area_country[i] == '西班牙':
            country_language = ['西班牙语']
        else:
            country_language = ['英语']
        data_list1[jx_area_country[i]] = country_language
    data_dic['Amazon'] = data_list
    data_dic1['Amazon'] = data_list1

    return JsonResponse({"code": 200, "data": data_dic, "data1": data_dic1})


# 获取标记国家
def get_sign_country1(request):
    area1 = request.GET.get('area')
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    print('123', area)
    if area == 'all':
        sql = "SELECT DISTINCT country FROM store_information where site='{}'"
        sql = sql.format(area1)
        data = conf_fun.connect_mysql_operation(sql)
        area_country = [x[0] for x in data]
    else:
        try:
            area_res = area.split(',')
            area_country = []
            for i in area_res:
                if i.split('_')[0] == area1:
                    area_country.append(i.split('_')[1])
            area_country = list(set(area_country))
        except:
            area_country = [[area.split('_')[1]]]
    return JsonResponse({"code": 200, "data": area_country})


# 获取标记地区
def get_sign_area1(request):
    area = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[1]
    if area == 'all':
        sql = "SELECT DISTINCT site FROM store_information"
        data = conf_fun.connect_mysql_operation(sql)
        area_site = [x[0] for x in data]
    else:
        try:
            area_res = area.split(',')
            area_site = []
            for i in area_res:
                area_site.append(i.split('_')[0])
            area_site = list(set(area_site))
        except:
            area_site = [[area.split('_')[0]]]
    return JsonResponse({"code": 200, "data": area_site, "data1": "Amazon"})