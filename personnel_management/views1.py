from django.shortcuts import render
import json
from django.http import JsonResponse
import pymysql
import time
import datetime
import os
import random
import math
# from databases.views1 import connect_mysql1
from dateutil.relativedelta import relativedelta

from settings import conf_fun

# Create your views here.
#判断指定的文件夹存不存在，不存在就创建
def creatDir(dir):
    '''
    判断指定的文件夹存不存在
    :param dir:
    :return:
    '''
    dirlist = dir.split("/")
    for i,name in enumerate(dirlist):
        itemdir = os.path.join(os.getcwd(),name)
        #判断当前文件夹是否存在
        if not os.path.exists(itemdir):
            os.mkdir(itemdir)
        #如果当前文件夹存在并且不是最后一层
        if i < len(dirlist)-1:
            dirlist[i+1] = os.path.join(itemdir,dirlist[i+1])


# 列表不重复式插入
def single_list(target_list, item):
    if item not in target_list:
        target_list.append(item)


# ------------------>人员资料
def personnel_data(request):
    # 查询资料
    sql = "select * from personnel_data;"
    try:
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        return JsonResponse({"code": 200, "msg:":"success","data":data})
    except Exception as e:
        return JsonResponse({"code":500,"msg:":"error" + str(e)})


# 人员资料新增
def personnel_add(request):
    personnel_id = request.POST.get("personnel_id",None)
    user_name = request.POST.get("user_name", None)
    department = request.POST.get("department", None)
    position = request.POST.get("position", None)
    entry_date = request.POST.get("entry_date", None)
    phone = request.POST.get("phone", None)
    work = request.POST.get("work", None)
    print(personnel_id,user_name,department,position,entry_date,phone,work)
    # 判断用户是否存在
    sql = "select * from personnel_data where personnel_id='%s' or user_name='%s';"%(personnel_id,user_name)
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    if len(res) > 0:
        # 用户名或用户编码已存在
        return JsonResponse({"code":500,"msg":"用户名或用户编码已存在"})
    else:
        sql1 = "insert into personnel_data (personnel_id,user_name,department,position,entry_date,phone,work) values " \
               "('%s','%s','%s','%s','%s','%s','%s')"%(personnel_id,user_name,department,position,entry_date,phone,work)
        try:
            conf_fun.connect_mysql_operation(sql1)
            return JsonResponse({"code": 200, "msg": "success"})
        except Exception as e:
            return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 人员资料编辑
def personnel_edit(request):
    personnel_id = request.POST.get("personnel_id", None)
    user_name = request.POST.get("user_name", None)
    department = request.POST.get("department", None)
    position = request.POST.get("position", None)
    entry_date = request.POST.get("entry_date", None)
    phone = request.POST.get("phone", None)
    work = request.POST.get("work", None)

    # 判断用户是否存在
    sql = "select * from personnel_data where personnel_id='%s' and user_name='%s';"%(personnel_id,user_name)
    res = conf_fun.connect_mysql_operation(sql, type='dict')
    if len(res) == 0:
        # 用户名或用户编码已存在
        return JsonResponse({"code": 500, "msg": "用户不存在"})
    else:
        sql1 = "update personnel_data set department='%s',position='%s',entry_date='%s',phone='%s',work='%s' where personnel_id='%s' and user_name='%s';"\
               %(department,position,entry_date,phone,work,personnel_id,user_name)
        try:
            conf_fun.connect_mysql_operation(sql1)
            return JsonResponse({"code": 200, "msg": "success"})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 人员资料删除
def personnel_del(request):
    personnel_id = request.GET.get("personnel_id", None)
    sql = "delete from personnel_data where personnel_id='%s';"%(personnel_id)
    try:
        conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code": 200, "msg": "success"})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})

# ----------------->培训
# 查询
def train(request):
    # 查询培训信息
    sql = "select * from train;"
    # 查询所有用户
    sql1 = "select user_name from personnel_data;"
    # 查询所有主题以及对应的文档
    sql2 = "select * from train_theme_file;"
    try:
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        users = conf_fun.connect_mysql_operation(sql1,type='dict')
        data1 = conf_fun.connect_mysql_operation(sql2,type='dict')
        _list = []
        for i in data1:
            if len(_list) == 0:
                _dic = {
                    "train_theme":i["train_theme"],
                    "train_files":[i["train_file"]]
                }
                _list.append(_dic)
            else:
                for index,j in enumerate(_list):
                    if i["train_theme"] == j["train_theme"]:
                        j["train_files"].append(i["train_file"])
                        break
                    elif i["train_theme"] != j["train_theme"] and index == len(_list)-1:
                        _dic = {
                            "train_theme": i["train_theme"],
                            "train_files": [i["train_file"]]
                        }
                        _list.append(_dic)
                        break

        return JsonResponse({"code": 200, "msg": "success","data":data,"users":users,"train_theme_file_data":_list})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})


# 培训任务新增
def train_work_add(request):
    train_date = request.POST.get("train_date",None)
    train_theme = request.POST.get("train_theme",None)
    train_file = request.POST.get("train_file",None)
    train_user = request.POST.get("train_user", None)
    train_remarks = request.POST.get("train_remarks", None)

    sql = "insert into train (train_date,train_theme,train_files,train_user,remarks) values "
    try:
        _list = train_user.split(',')
        for i in _list:
            sql += "('" + train_date + "','" + train_theme + "','" + train_file + "','" + i + "','" + train_remarks + "'),"
        sql = sql[:-1] + ";"
        conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code":200,"msg":"success"})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:"+str(e)})

# 培训文档新增
def train_file_add(request):
    train_theme = request.POST.get("train_theme",None)
    train_files = [request.FILES.get("train_file",None)]
    print(train_files)
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    try:
        sql = "insert into train_theme_file (train_theme,train_file,upload_date) values "
        # 文件存储
        path = "/static/data/train_data/" + train_theme
        creatDir(path)
        for i in train_files:
            path += "/" + i.name
            with open("/home/by_operate" + path, "wb") as f:
                for line in i:
                    f.write(line)
            sql += "('"+train_theme+"','"+i.name+"','"+now+"'),"
        # 存入数据库
        sql = sql[:-1] + ";"
        conf_fun.connect_mysql_operation(sql)
        # 查询所有主题以及对应的文档
        sql2 = "select * from train_theme_file;"
        data1 = conf_fun.connect_mysql_operation(sql2, type='dict')
        _list = []
        for i in data1:
            if len(_list) == 0:
                _dic = {
                    "train_theme": i["train_theme"],
                    "train_files": [i["train_file"]]
                }
                _list.append(_dic)
            else:
                for index, j in enumerate(_list):
                    if i["train_theme"] == j["train_theme"]:
                        j["train_files"].append(i["train_file"])
                        break
                    elif i["train_theme"] != j["train_theme"] and index == len(_list) - 1:
                        _dic = {
                            "train_theme": i["train_theme"],
                            "train_files": [i["train_file"]]
                        }
                        _list.append(_dic)
                        break
        return JsonResponse({"code": 200, "msg": "success","data":_list})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 培训文档汇总
def train_file_view(request):
    sql = "select * from train_theme_file;"
    try:
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        # 排序
        if len(data) > 1:
            data.sort(key=lambda x: x['upload_date'])
        return JsonResponse({"code": 200, "msg": "success","data":data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 培训文档删除
def train_file_del(request):
    train_theme = request.GET.get("train_theme",None)
    file = request.GET.get("train_file",None)
    # 删除
    try:
        path = "/home/by_operate/static/data/train_data/" + train_theme + "/" + file
        os.remove(path)

        # 直接删除此主题
        sql1 = "delete from train_theme_file where train_theme='%s' and train_file='%s';" % (train_theme,file)
        conf_fun.connect_mysql_operation(sql1)

        # 查询主题文档表
        sql2 = "select * from train_theme_file;"
        res = conf_fun.connect_mysql_operation(sql2,type='dict')
        return JsonResponse({"code": 200, "msg": "success","data":res})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 培训评分
def train_score(request):
    train_user = request.GET.get("train_user",None)
    train_theme = request.GET.get("train_theme",None)
    score = request.GET.get("score",None)
    sql = "update train set score='%s' where train_theme='%s' and train_user='%s';"%(score,train_theme,train_user)
    try:
        conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code": 200, "msg": "success"})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# ------------> 绩效
# 个人绩效
def performance(request):
    user_name = "黄凤媛"
    # 获取以往12个月的年月
    _list = []
    for i in range(12):
        _date = datetime.datetime.strftime(datetime.datetime.now() - relativedelta(months=i),"%Y-%m")
        _list.append(_date)
    # 查询数据库
    sql = "select * from staff_performance where personnel_name='"+user_name+"';"
    print(sql)
    try:
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        # 计算绩效比例
        print(_list)
        _list1 = []
        for i in data:
            if i["evaluate_date"][0:7] in _list:
                num =  "%.2f%%" % (int(i["month_actual_money"])/int(i["performance_base"])*100)
                i["proportion"] = num
                _list1.append(i)
        return JsonResponse({"code": 200, "msg": "success","data":_list1})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 员工绩效
def staff_performance(request):
    user_name = "黄凤媛"
    # 获取当前用户同部门所有人
    sql = "select user_name from personnel_data where department in (select department from personnel_data where user_name='%s')"%(user_name)
    res = conf_fun.connect_mysql_operation(sql,type="dict")
    _list = [i["user_name"] for i in res]
    _str = "','".join(_list)
    print(_list)
    print(_str)
    # 查询所有人绩效
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m")
    sql1 = "select p.*,s.performance_base,s.month_top_performance,s.month_top_money,s.month_actual_performance," \
           "s.month_actual_money,s.evaluate from personnel_data as p left join staff_performance as s on " \
           "p.user_name=s.personnel_name where s.evaluate_date like'%"+now+"%' and p.user_name in ('"+_str+"');"
    print(sql1)
    # 查询部门绩效
    sql2 = "select * from department_performence where evaluate_date like'%"+now+"%' and department=(select department from userinfo where real_name='"+user_name+"');"
    try:
        data1 = conf_fun.connect_mysql_operation(sql1,type='dict')
        print(data1)
        data2 = conf_fun.connect_mysql_operation(sql2,type='dict')
        if len(data2) == 0:
            data2 = []
        print("data2---",data2)
        return JsonResponse({"code":200,"msg":"success","data":data1,"department":data2})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 查看历史员工绩效
def history_performance(request):
    user_name = "黄凤媛"
    # 获取当前用户同部门所有人
    sql = "select user_name from personnel_data where department in (select department from personnel_data where user_name='%s')" % (user_name)
    res = conf_fun.connect_mysql_operation(sql, type="dict")
    users = [i["user_name"] for i in res if i["user_name"] != user_name]
    print(users)
    _str = "','".join(users)
    # 查看历史绩效
    sql1 = "select p.*,s.performance_base,s.month_top_performance,s.month_top_money,s.month_actual_performance," \
           "s.month_actual_money,s.evaluate,s.evaluate_date from personnel_data as p left join staff_performance as s on " \
           "p.user_name=s.personnel_name where p.user_name in ('"+_str+"');"
    try:
        data = conf_fun.connect_mysql_operation(sql1,type='dict')
        return JsonResponse({"code": 200, "msg": "success", "data": data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 查看部门历史数据
def history_department_performance(request):
    user_name = "黄凤媛"
    sql = "select department from personnel_data where user_name='%s'"%(user_name)
    department = conf_fun.connect_mysql_operation(sql,type='dict')[0]["department"]
    now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m")
    sql2 = "select * from department_performence where evaluate_date not like'%"+now+"%' and department='"+department+"';"
    try:
        data = conf_fun.connect_mysql_operation(sql2,type='dict')
        return JsonResponse({"code": 200, "msg": "success", "department_data": data})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 保存
def staff_performance_save(request):
    staff_performance_list = request.POST.get("staff_performance_list",[])
    if staff_performance_list != []:
        staff_performance_list = json.loads(staff_performance_list)
    try:
        print("staff_performance_list==", staff_performance_list)
        print(type(staff_performance_list))
        evaluate_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        for i in staff_performance_list:
            personnel_name = i["personnel_name"]
            month_actual_performance = i["month_actual_performance"]
            month_actual_money = i["month_actual_money"]
            evaluate = i["evaluate"]
            # 修改数据库
            sql = "update staff_performance set month_actual_performance='%s',month_actual_money='%s',evaluate_date='%s',evaluate='%s' where " \
                  "personnel_name='%s';" % (month_actual_performance, month_actual_money,evaluate_date, evaluate,personnel_name)
            conf_fun.connect_mysql_operation(sql)
        return JsonResponse({"code": 200, "msg": "success"})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# 提交
def staff_performance_submit(request):
    staff_performance_list = request.POST.get("staff_performance_list", [])
    if staff_performance_list != []:
        staff_performance_list = json.loads(staff_performance_list)
    try:
        print("staff_performance_list==", staff_performance_list)
        print(type(staff_performance_list))
        evaluate_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        for i in staff_performance_list:
            personnel_name = i["personnel_name"]
            month_actual_performance = i["month_actual_performance"]
            month_actual_money = i["month_actual_money"]
            evaluate = i["evaluate"]
            # 修改数据库
            sql = "update human_staff_performance set month_actual_performance='%s',month_actual_money='%s',evaluate_date='%s',evaluate='%s' where " \
                  "personnel_name='%s';" % (
                  month_actual_performance, month_actual_money, evaluate_date, evaluate, personnel_name)
            sql1 = "update staff_performance set month_actual_performance='%s',month_actual_money='%s',evaluate_date='%s',evaluate='%s' where " \
                  "personnel_name='%s';" % (
                      month_actual_performance, month_actual_money, evaluate_date, evaluate, personnel_name)
            conf_fun.connect_mysql_operation(sql)
            conf_fun.connect_mysql_operation(sql1)
        return JsonResponse({"code": 200, "msg": "success"})
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "error:" + str(e)})


# ---------------->工单
# 根据用户名获取其部门
def get_department(user_name):
    print("---------------根据用户名获取其部门:", user_name)
    select_sql = "select department from personnel_data where user_name='%s';" % user_name
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)[0][0]
    print("select_res:", select_res)
    return select_res


# 获取下拉框数据(部门/员工)
def get_select_job(request):
    print("------------获取下拉框数据(部门/员工):", request.GET)
    receive_department = request.GET.get("receive_department", None)
    receive_person = request.GET.get("receive_person", None)
    department_list = []
    person_list = []
    mark = 0
    select_sql = "select department,user_name from personnel_data"
    if receive_department:
        select_sql += " where department='" + receive_department + "'"
        mark = 1
    if receive_person:
        if mark == 0:
            select_sql += " where user_name='" + receive_person + "'"
        else:
            select_sql += " and user_name='" + receive_person + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    for item in select_res:
        single_list(department_list, item[0])
        single_list(person_list, item[1])
    res = {"code": 200, "department_list": department_list, "person_list": person_list}
    print("res: ", res)
    return JsonResponse(res)


# 获得X天前的日期
def get_date(day):
    now_date = datetime.datetime.now()
    target_stamp = now_date - datetime.timedelta(days=day)
    target_date = str(datetime.datetime(target_stamp.year, target_stamp.month, target_stamp.day))[0:10]
    return target_date


# 从请求头获取用户名
def get_user(data):
    print("------从请求头获取用户名-------")
    user_token = data.session.get("user_name", None)
    print("user_token: ", user_token)
    select_user_sql = "select real_name from userinfo where token='%s';" % user_token
    select_user_res = conf_fun.connect_mysql_operation(sql_text=select_user_sql)
    if not select_user_res:
        return "许日成"
    return select_user_res[0][0]


# ==========================================已提交工单


# 已提交工单-点击查询
def select_initiate_job(request):
    print("-------------已提交工单-点击查询:", request.GET)
    receive_department = request.GET.get("receive_department", None)
    receive_person = request.GET.get("receive_person", None)
    job_type = request.GET.get("job_type", None)
    out_date = request.GET.get("out_time", None)
    if out_date:
        next_date = datetime.datetime.strftime(datetime.datetime.strptime(out_date, "%Y/%m/%d") + datetime.timedelta(days=1), "%Y/%m/%d")
    page = int(request.GET.get("page", None))
    res_data = []
    mark = 0
    select_sql = "select * from job"
    if receive_department:
        select_sql += " where receive_department='" + receive_department + "'"
        mark = 1
    if receive_person:
        if mark == 0:
            select_sql += " where receive_person='" + receive_person + "'"
        else:
            select_sql += " and receive_person='" + receive_person + "'"
        mark = 1
    if job_type:
        if mark == 0:
            select_sql += " where job_type='" + job_type + "'"
        else:
            select_sql += " and job_type='" + job_type + "'"
        mark = 1
    if out_date:
        if mark == 0:
            select_sql += " where out_time<'" + next_date + "' and out_time>'" + out_date + "'"
        else:
            select_sql += " and out_time<'" + next_date + "' and out_time>'" + out_date + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    for item in select_res:
        small_list = []
        # id
        small_list.append(item[0])
        # 接单人
        small_list.append(item[4])
        # 发单时间/截单时间/内容需求/跟进信息
        small_list.extend(item[6:10])
        # 工单类型
        small_list.append(item[5])
        # 状态
        small_list.append(item[10])
        res_data.append(small_list)
    # 获取总行数
    all_num = len(res_data)
    # 分页
    page_start = (page - 1) * 20
    page_end = page * 20
    try:
        res_data = res_data[page_start: page_end]
    except:
        res_data = res_data[page_start:]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    print("res: ", res)
    return JsonResponse(res)


# 已提交工单-确认提交工单
def insert_initiate_job(request):
    print("-------------已提交工单-确认提交工单:", request.POST)
    receive_department = request.POST.get("receive_department", None)
    receive_person = request.POST.get("receive_person", None)
    job_type = request.POST.get("job_type", None)
    out_time = request.POST.get("out_time", None)

    now_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "%Y/%m/%d %H:%M")
                + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M")
    if now_time > out_time:
        res = {"code": 4041, "msg": "截单日期有误。"}
        print("out_time: ", out_time)
        return JsonResponse(res)

    need = request.POST.get("need", None)
    # permission = eval(request.session.get("permissions", "{'user_name': '路飞'}"))
    # user_name = permission["user_name"]
    user_name = get_user(request)
    print("user_name: ", user_name)
    # 获取提交人部门
    initiate_department = get_department(user_name)
    # 获取发单时间
    initiate_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "%Y/%m/%d %H:%M")
                     + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M")
    insert_sql = "insert into job(initiate_department,initiate_person,receive_department," \
                 "receive_person,job_type,initiate_time,out_time,need,status) " \
                 "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                 % (initiate_department, user_name, receive_department, receive_person,
                    job_type, initiate_time, out_time, need, "已发起")
    print("insert_sql: ", insert_sql)
    conf_fun.connect_mysql_operation(sql_text=insert_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-点击编辑获取原信息(截单时间、需求、跟进信息)
def get_update_initiate_job(request):
    print("-------------已提交工单-点击编辑获取原信息:", request.GET)
    job_id = request.GET.get("job_id", None)
    select_sql = "select out_time,need,next_info from job where id='%s';" % job_id
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    res = {"code": 200, "data": select_res[0]}
    print("res: ", res)
    return JsonResponse(res)


# 已提交工单-编辑弹窗点击确认
def update_initiate_job(request):
    print("-------------已提交工单-编辑弹窗点击确认:", request.POST)
    job_id = request.POST.get("job_id", None)
    out_time = request.POST.get("out_time", None)
    need = request.POST.get("need", None)
    next_info = request.POST.get("next_info", None)
    # permission = eval(request.session.get("permissions", "{'user_name': '路飞'}"))
    # user_name = permission["user_name"]
    user_name = get_user(request)
    select_next_info_sql = "select out_time,need,next_info from job where id='%s';" % job_id
    select_next_info_res = conf_fun.connect_mysql_operation(sql_text=select_next_info_sql)
    if not out_time:
        out_time = select_next_info_res[0][0]
    if not need:
        need = select_next_info_res[0][1]
    if select_next_info_res[0][2] and next_info:
        next_info = select_next_info_res[0][2] + user_name + ":" + next_info + "\n"
    elif next_info:
        next_info = user_name + ":" + next_info + "\n"
    update_sql = "update job set out_time='%s',need='%s',next_info='%s' where id='%s';" \
                 % (out_time, need, next_info, job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-点击删除
def delete_initiate_job(request):
    print("-------------已提交工单-点击删除:", request.GET)
    job_id = request.GET.getlist("job_id[]", None)
    for item in job_id:
        delete_sql = "delete from job where id='%s';" % item
        conf_fun.connect_mysql_operation(sql_text=delete_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-结单确认
def sure_initiate_job(request):
    print("-------------已提交工单-结单确认:", request.GET)
    job_id = request.GET.get("job_id", None)
    # 逾期检测
    now_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "%Y/%m/%d %H:%M")
                + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M")
    select_time_sql = "select out_time from job where id='%s';" % job_id
    select_time_res = conf_fun.connect_mysql_operation(sql_text=select_time_sql)
    print("now_time: ", now_time)
    print("out_time: ", select_time_res[0][0])
    if now_time > select_time_res[0][0]:
        update_sql = "update job set status='%s' where id='%s';" \
                     % ("逾期完成", job_id)
    else:
        update_sql = "update job set status='%s' where id='%s';" \
                     % ("已完成", job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-结单驳回
def refuse_initiate_job(request):
    print("-------------已提交工单-结单驳回:", request.GET)
    job_id = request.GET.get("job_id", None)
    update_sql = "update job set status='%s' where id='%s';" \
                 % ("进行中", job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# ==========================================已提交工单end

# ==========================================待处理工单


# 待处理工单-查询
def select_wait_job(request):
    print("-------------待处理工单-查询:", request.GET)
    page = int(request.GET.get("page", None))
    # permission = eval(request.session.get("permissions", "{'user_name': '路飞'}"))
    # user_name = permission["user_name"]
    user_name = get_user(request)
    res_data = []
    select_sql = "select * from job where receive_person='%s' and status='%s';" \
                 % (user_name, "已发起")
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    # id/发单部门/发单人/发单时间/截单时间/工单类型/需求
    for item in select_res:
        small_list = []
        small_list.extend(item[:3])
        small_list.extend(item[6:8])
        small_list.append(item[5])
        small_list.append(item[8])
        res_data.append(small_list)
    # 获取总行数
    all_num = len(res_data)
    # 分页
    page_start = (page - 1) * 20
    page_end = page * 20
    res_data = res_data[page_start: page_end]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    print("res: ", res)
    return JsonResponse(res)


# 待处理工单-接取
def receive_wait_job(request):
    print("-------------待处理工单-接取:", request.GET)
    job_id = request.GET.get("job_id", None)
    update_sql = "update job set status='%s' where id='%s';" \
                 % ("进行中", job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 待处理工单-转派
def turn_wait_job(request):
    print("-------------待处理工单-转派:", request.GET)
    job_id = request.GET.get("job_id", None)
    receive_department = request.GET.get("receive_department", None)
    receive_person = request.GET.get("receive_person", None)
    update_sql = "update job set receive_department='%s',receive_person='%s' where id='%s';" \
                 % (receive_department, receive_person, job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 待处理工单-驳回
def refuse_wait_job(request):
    print("-------------待处理工单-驳回:", request.GET)
    job_id = request.GET.get("job_id", None)
    refuse_reason = request.GET.get("refuse_reason", None)
    update_sql = "update job set refuse_reason='%s',status='%s' where id='%s';" \
                 % (refuse_reason, "被驳回", job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# ==========================================待处理工单end

# ==========================================已接工单


# 已接工单-查询
def select_receive_job(request):
    print("-------------已接工单-查询:", request.GET)
    initiate_department = request.GET.get("initiate_department", None)
    initiate_person = request.GET.get("initiate_person", None)
    job_type = request.GET.get("job_type", None)
    out_date = request.GET.get("out_time", None)
    page = int(request.GET.get("page", None))
    res_data = []
    select_sql = "select * from job where (status='进行中' or status='结单中')"
    if initiate_department:
        select_sql += " and initiate_department='" + initiate_department + "'"
    if initiate_person:
        select_sql += " and initiate_person='" + initiate_person + "'"
    if job_type:
        select_sql += " and job_type='" + job_type + "'"
    if out_date:
        next_date = datetime.datetime.strftime(
            datetime.datetime.strptime(out_date, "%Y/%m/%d") + datetime.timedelta(days=1), "%Y/%m/%d")
        select_sql += " and out_time>'" + out_date + "' and out_time<'" + next_date + "'"
    select_sql += ";"
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    for item in select_res:
        small_list = []
        small_list.append(item[0])
        small_list.append(item[2])
        small_list.extend(item[6:10])
        small_list.append(item[5])
        small_list.append(item[10])
        res_data.append(small_list)
    # 获取总行数
    all_num = len(res_data)
    # 分页
    page_start = (page - 1) * 20
    page_end = page * 20
    try:
        res_data = res_data[page_start: page_end]
    except:
        res_data = res_data[page_start:]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    print("res: ", res)
    return JsonResponse(res)


# 已接工单-结单
def update_receive_job(request):
    print("-------------已接工单-结单:", request.GET)
    job_id = request.GET.get("job_id", None)
    update_sql = "update job set status='%s' where id='%s';" \
                 % ("结单中", job_id)
    conf_fun.connect_mysql_operation(sql_text=update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# ==========================================已接工单end

# ==========================================历史工单


# 历史工单-查询
def select_history_job(request):
    print("-------------历史工单-查询:", request.GET)
    out_date = request.GET.get("out_date", None)
    if out_date:
        next_date = datetime.datetime.strftime(datetime.datetime.strptime(out_date, "%Y/%m/%d") + datetime.timedelta(days=1), "%Y/%m/%d")
    page = int(request.GET.get("page", None))
    # permission = eval(request.session.get("permissions", "{'user_name': '路飞'}"))
    # user_name = permission["user_name"]
    user_name = get_user(request)
    res_data = []
    if out_date:
        select_sql = "select * from job where out_time<'" + next_date + "' and out_time>'" + out_date + \
                     "' and (initiate_person='%s' or receive_person='%s');" \
                     % (user_name, user_name)
    else:
        select_sql = "select * from job where initiate_person='%s' or receive_person='%s';" % (user_name, user_name)
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    # 发单部门、发单人、接单部门、接单人、工单类型、发单时间、截单时间、需求、跟进、状态
    for item in select_res:
        small_list = []
        small_list.extend(item[1:11])
        res_data.append(small_list)
    # 获取总行数
    all_num = len(res_data)
    # 分页
    page_start = (page - 1) * 20
    page_end = page * 20
    res_data = res_data[page_start: page_end]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    print("res: ", res)
    return JsonResponse(res)


# ==========================================已接工单end

# ==========================================工单管理


# 工单管理-查询
def get_management_job(request):
    print("-------------工单管理-查询:", request.GET)
    page = int(request.GET.get("page", None))

    # permission = eval(request.session.get("permissions", "{'user_name': '路飞'}"))
    # user_name = permission["user_name"]
    user_name = get_user(request)
    select_department_sql = "select department from personnel_data where user_name='%s';" % user_name
    department = conf_fun.connect_mysql_operation(sql_text=select_department_sql)[0][0] if len(conf_fun.connect_mysql_operation(sql_text=select_department_sql)) > 0 else ''

    now_date = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
                + datetime.timedelta(hours=8)).strftime("%Y/%m/%d")
    last_week = get_date(7).replace("-", "/")
    next_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")
    # last_month = ((datetime.date.today()).replace(day=1) - datetime.timedelta(days=1)).strftime("%Y/%m")

    # 部门工单统计
    select_day_sql = "select count(id) from job where receive_department='%s' " \
                     "and out_time<'%s' and out_time>'%s';" \
                     % (department, next_date, now_date)
    print("select_day_sql:", select_day_sql)
    day_number = conf_fun.connect_mysql_operation(sql_text=select_day_sql)[0][0] if len(conf_fun.connect_mysql_operation(sql_text=select_day_sql)) > 0 else ''
    select_week_sql = "select count(id) from job where receive_department='%s' " \
                      "and out_time<'%s' and out_time>'%s';" \
                      % (department, next_date, last_week)
    print("select_week_sql:", select_week_sql)
    week_number = conf_fun.connect_mysql_operation(sql_text=select_week_sql)[0][0]
    select_out_sql = "select count(id) from job where receive_department='%s' " \
                     "and out_time<'%s' and out_time>'%s' and status='%s';" \
                     % (department, next_date, last_week, "逾期完成")
    print("select_out_sql:", select_out_sql)
    out_number = conf_fun.connect_mysql_operation(sql_text=select_out_sql)[0][0] if len(conf_fun.connect_mysql_operation(sql_text=select_out_sql)) > 0 else ''
    department_list = [day_number, week_number, out_number]
    # 员工工单统计
    """获取该部门所有员工，然后获取该员工的各工单类型(日常、即时、远期)的数量"""
    person_list = []
    select_person_sql = "select user_name from personnel_data where department='%s';" % department
    select_person_res = conf_fun.connect_mysql_operation(sql_text=select_person_sql)
    for item in select_person_res:
        small_list = []
        if len(select_person_res) > 0:
            small_list.append(item[0])

            select_person_num_sql = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                    % (item[0], "日常")
            select_person_num_res = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql)
            small_list.append(select_person_num_res[0][0])

            select_person_num_sql1 = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                     % (item[0], "即时")
            select_person_num_res1 = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql1)
            small_list.append(select_person_num_res1[0][0])

            select_person_num_sql2 = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                     % (item[0], "远期")
            select_person_num_res2 = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql2)
            small_list.append(select_person_num_res2[0][0])
        person_list.append(small_list)
    # 逾期工单统计
    select_department_out_sql = "select * from job where receive_department='%s' and status='逾期完成';" % department
    select_department_out_res = conf_fun.connect_mysql_operation(sql_text=select_department_out_sql)
    out_time_list = []
    # 发单部门、发单人、接单人、工单类型、发单时间、截单时间、需求、原因
    for select_department_out_item in select_department_out_res:
        small_list = []
        if len(select_department_out_res) > 0:
            small_list.extend(select_department_out_item[1:3])
            small_list.extend(select_department_out_item[4:9])
            small_list.append(select_department_out_item[-1])
        out_time_list.append(small_list)
    # 获取总行数
    all_num = len(out_time_list)
    # 分页
    page_start = (page - 1) * 50
    page_end = page * 50
    out_time_list = out_time_list[page_start: page_end]
    res = {"code": 200, "department_list": department_list, "person_list": person_list, "out_time_list": out_time_list, "all_num": all_num}
    print("res: ", res)
    return JsonResponse(res)


# 工单管理-条件查询
def select_management_job(request):
    print("-------------工单管理-查询:", request.GET)
    # permission = eval(request.session.get("permissions", "{'user_name': '路飞'}"))
    # user_name = permission["user_name"]
    user_name = get_user(request)
    select_department_sql = "select department from personnel_data where user_name='%s';" % user_name
    department = conf_fun.connect_mysql_operation(sql_text=select_department_sql)[0][0] if len(conf_fun.connect_mysql_operation(sql_text=select_department_sql)) > 0 else ''
    target_date = request.GET.get("target_date", None)
    next_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")
    if target_date:
        start_date = get_date(int(target_date))
        person_list = []
        select_person_sql = "select user_name from personnel_data where department='%s';" % department
        select_person_res = conf_fun.connect_mysql_operation(sql_text=select_person_sql)
        for item in select_person_res:
            small_list = []
            if len(select_person_res) > 0:
                small_list.append(item[0])

                select_person_num_sql = "select count(id) from job where receive_person='%s' and job_type='%s' " \
                                        "and out_time>'%s' and out_time<'%s';" \
                                        % (item[0], "日常", start_date, next_date)
                select_person_num_res = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql)
                small_list.append(select_person_num_res[0][0])

                select_person_num_sql1 = "select count(id) from job where receive_person='%s' and job_type='%s' " \
                                         "and out_time>'%s' and out_time<'%s';" \
                                         % (item[0], "即时", start_date, next_date)
                select_person_num_res1 = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql1)
                small_list.append(select_person_num_res1[0][0])

                select_person_num_sql2 = "select count(id) from job where receive_person='%s' and job_type='%s' " \
                                         "and out_time>'%s' and out_time<'%s';" \
                                         % (item[0], "远期", start_date, next_date)
                select_person_num_res2 = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql2)
                small_list.append(select_person_num_res2[0][0])
            person_list.append(small_list)
    else:
        person_list = []
        select_person_sql = "select user_name from personnel_data where department='%s';" % department
        select_person_res = conf_fun.connect_mysql_operation(sql_text=select_person_sql)
        for item in select_person_res:
            small_list = []
            if len(select_person_res) > 0:
                small_list.append(item[0])

                select_person_num_sql = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                        % (item[0], "日常")
                select_person_num_res = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql)
                small_list.append(select_person_num_res[0][0])

                select_person_num_sql1 = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                         % (item[0], "即时")
                select_person_num_res1 = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql1)
                small_list.append(select_person_num_res1[0][0])

                select_person_num_sql2 = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                         % (item[0], "远期")
                select_person_num_res2 = conf_fun.connect_mysql_operation(sql_text=select_person_num_sql2)
                small_list.append(select_person_num_res2[0][0])
            person_list.append(small_list)
    res = {"code": 200, "person_list": person_list}
    print("res: ", res)
    return JsonResponse(res)


# 工单管理-员工详情
def select_one_management_job(request):
    print("-------------工单管理-员工详情:", request.GET)
    receive_person = request.GET.get("receive_person", None)
    page = int(request.GET.get("page", None))
    res_data = []
    select_sql = "select * from job where receive_person='%s';" % receive_person
    select_res = conf_fun.connect_mysql_operation(sql_text=select_sql)
    # 发单部门、发单人、接单人、工单类型、发单时间、截单时间、需求、跟进、状态
    for select_item in select_res:
        small_list = []
        if len(select_res) > 0:
            small_list.extend(select_item[1:3])
            small_list.extend(select_item[4:11])
        res_data.append(small_list)
    # 获取总行数
    all_num = len(res_data)
    # 分页
    page_start = (page - 1) * 50
    page_end = page * 50
    res_data = res_data[page_start: page_end]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    print("res: ", res)
    return JsonResponse(res)


# ==========================================工单管理end


# 员工错误日志
def staff_error_log(request):
    # 查询人员信息表
    sql = "select * from staff_data;"
    res = conf_fun.connect_mysql_operation(sql,type='dict')
    sql1 = "select * from error_log;"
    res1 = conf_fun.connect_mysql_operation(sql1,type='dict')
    theme_list = list(set([i["theme"] for i in res1]))
    # 数据整理
    data = []
    for i in res:
        if len(data) == 0:
            _dict = {
                "department":i["department"],
                "organization_personnel":[i["name"]]
            }
            data.append(_dict)
        else:
            for index,j in enumerate(data):
                if i["department"] == j["department"]:
                    j["organization_personnel"].append(i["name"])
                elif i["department"] != j["department"] and index == len(data)-1:
                    _dict = {
                        "department": i["department"],
                        "organization_personnel": [i["name"]]
                    }
                    data.append(_dict)
                    break
    return JsonResponse({"code":200,"msg":"success","data":data,"theme_list":theme_list})


# 获取数据
def error_log_data(request):
    log_code = request.POST.get("log_code",None)
    dates = request.POST.get("dates", None)
    department = request.POST.get("department", None)
    organization_personnel = request.POST.get("organization_personnel", None)
    theme = request.POST.get("theme",None)
    _list = [
        {"key":"log_code","value":log_code},
        {"key": "dates", "value": dates},
        {"key": "organization_personnel", "value": organization_personnel},
        {"key": "department", "value": department},
        {"key": "theme", "value": theme}
    ]
    try:
        sql = "select * from error_log"
        count = 0
        for i in _list:
            if count == 0:
                if i["value"] is not None:
                    if i["key"] == "dates":
                        sql += " where dates like'%" + i["value"] + "%' and "
                    elif i["key"] == "theme":
                        sql += " where theme like'%" + i["value"] + "%' and "
                    else:
                        sql += " where " + i["key"] + "='" + i["value"] + "' and "
                    count += 1
            else:
                if i["value"] is not None:
                    if i["key"] == "dates":
                        sql += "dates like'%" + i["value"] + "%' and "
                    elif i["key"] == "theme":
                        sql += "theme like'%" + i["value"] + "%' and "
                    else:
                        sql += i["key"] + "='" + i["value"] + "' and "
                    count += 1
        if count > 0:
            sql = sql[:-5]
        data = conf_fun.connect_mysql_operation(sql,type='dict')
        return JsonResponse({"code": 200, "msg": "success", "data": data})
    except Exception as e:
        return JsonResponse({"code":500,"msg":"error:" + str(e)})


# 错误日志新增
def error_log_add(request):
    department = request.POST.get("department", None)
    organization_personnel = request.POST.get("organization_personnel", None)
    theme = request.POST.get("theme",None)
    content = request.POST.get("content", None)
    file = request.FILES.get("file", None)

    # 查询员工编号
    select = "select * from staff_data where name='%s';"%(organization_personnel)
    res = conf_fun.connect_mysql_operation(select,type='dict')
    code = res[0]["code"]
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    log_code = math.ceil(time.time())
    # 判断是否上传附件
    if file is not None:
        # 存储文件
        try:
            path = "/static/data/error_log_data/" + organization_personnel + "/" + now
            creatDir(path)
            path1 = "/home/by_operate" + path + "/" + file.name + "_" + log_code
            with open(path1, "wb") as f:
                for line in i:
                    f.write(line)
            # 存入数据库
            times = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
            sql = "insert into error_log (log_code,dates,organization_personnel,staff_code,department,theme,content,files)" \
                  " values ('%s','%s','%s','%s','%s','%s','%s','%s')"%(str(log_code),times,organization_personnel,code,department,theme,content,file.name + "_" + log_code)
            conf_fun.connect_mysql_operation(sql)
            return JsonResponse({"code":200,"msg":"success"})
        except Exception as e:
            return JsonResponse({"code":200,"msg":"error:"+str(e)})
    else:
        try:
            # 存入数据库
            times = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            sql = "insert into error_log (log_code,dates,organization_personnel,staff_code,department,theme,content)" \
                  " values ('%s','%s','%s','%s','%s','%s','%s')" % (str(log_code), times, organization_personnel, code, department, theme, content)
            conf_fun.connect_mysql_operation(sql)

            sql1 = "select * from error_log;"
            res = conf_fun.connect_mysql_operation(sql1,type='dict')
            return JsonResponse({"code": 200, "msg": "success","data":res})
        except Exception as e:
            return JsonResponse({"code": 200, "msg": "error:" + str(e)})


# 错误日志详情
def error_log_detail(request):
    log_code = request.GET.get("log_code",None)
    try:
        sql = "select * from error_log where log_code='%s';"%(log_code)
        data = conf_fun.connect_mysql_operation(sql, type='dict')
        return JsonResponse({"code": 200, "msg": "success","data":data})
    except Exception as e:
        return JsonResponse({"code": 200, "msg": "error:" + str(e)})





