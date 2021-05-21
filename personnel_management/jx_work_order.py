import datetime
import pymysql
from urllib.parse import unquote
from django.http import JsonResponse
from settings import conf_fun

# # 连接总数据库
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


# ---------------------------------- 已提交工单

# 已提交工单-获取所有部门
def get_department_down_box(request):
    print("\n", "已提交工单-获取所有部门: ", request.GET)

    department_list = list()

    select_sql = "select * from department;"
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    for select_res_item in select_res:
        if select_res_item['department_name'] not in department_list:
            department_list.append(select_res_item['department_name'])

    res = {"code": 200, "data": department_list}
    return JsonResponse(res)


# 已提交工单-根据部门获取所有员工数据
def get_person_down_box(request):
    print("\n", "已提交工单-根据部门获取所有员工数据: ", request.GET)

    department_name = request.GET.get("department_name", "")

    person_list = list()

    select_sql = "select * from department_person where department_name='%s';" % department_name
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    for select_res_item in select_res:
        if select_res_item['person_name'] not in person_list:
            person_list.append(select_res_item['person_name'])

    res = {"code": 200, "data": person_list}
    return JsonResponse(res)


# 已提交工单-点击查询
def select_initiate_job(request):
    print("\n", "已提交工单-点击查询: ", request.GET)

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    login_user = user_info.split("@")[0]

    receive_department = request.GET.get("receive_department", "")  # 接单部门
    receive_person = request.GET.get("receive_person", "")  # 接单人
    job_type = request.GET.get("job_type", "")  # 工单类型
    out_date = request.GET.get("out_time", "")  # 截止时间

    page = int(request.GET.get("page", "1"))

    select_sql = "select * from job where id!=''"
    if receive_department:
        select_sql += " and receive_department='" + receive_department + "'"
    if receive_person:
        select_sql += " and receive_person='" + receive_person + "'"
    if job_type:
        select_sql += " and job_type='" + job_type + "'"
    if out_date:
        next_date = datetime.datetime.strftime(
            datetime.datetime.strptime(out_date, "%Y/%m/%d") + datetime.timedelta(days=1), "%Y/%m/%d")

        select_sql += " and out_time<'" + next_date + "' and out_time>='" + out_date + "'"
    select_sql += " and initiate_department='运营增长部' and initiate_person='%s'  order by id desc;" % login_user
    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    # 获取总行数
    all_num = len(select_res)
    # 分页
    page_start = (page - 1) * 20
    page_end = page * 20
    res_data = select_res[page_start: page_end]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    return JsonResponse(res)


# 已提交工单-确认提交工单
def insert_initiate_job(request):
    print("\n", "已提交工单-确认提交工单:", request.POST)
    receive_department = request.POST.get("receive_department", None)  # 接取部门
    receive_person = request.POST.get("receive_person", None)  # 接取人
    job_type = request.POST.get("job_type", None)  # 工单类型
    out_time = request.POST.get("out_time", None)  # 截止时间

    out_time = out_time.replace("-", "/").replace("T", " ")

    now_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "%Y/%m/%d %H:%M")
                + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M")
    if now_time > out_time:
        res = {"code": 4041, "msg": "截单日期比当前时间早!"}
        print("out_time: ", out_time)
        return JsonResponse(res)

    need = request.POST.get("need", None)

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = user_info.split("@")[0]
    print("user_name: ", user_name)

    # 获取提交人部门
    initiate_department = "运营增长部"
    # 插入语句
    insert_sql = "insert into job(initiate_department,initiate_person,receive_department," \
                 "receive_person,job_type,initiate_time,out_time,need,status) " \
                 "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                 % (initiate_department, user_name, receive_department, receive_person,
                    job_type, now_time, out_time, need, "已发起")
    print("insert_sql: ", insert_sql)
    conf_fun.connect_mysql_operation(insert_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-编辑弹窗点击确认
def update_initiate_job(request):
    print("\n", "已提交工单-编辑弹窗点击确认: ", request.POST)
    job_id = request.POST.get("job_id", None)
    out_time = request.POST.get("out_time", None)
    need = request.POST.get("need", None)
    next_info = request.POST.get("next_info", None)

    if out_time:
        out_time = out_time.replace("-", "/").replace("T", " ")

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = user_info.split("@")[0]

    select_next_info_sql = "select out_time,need,next_info from job where id='%s';" % job_id
    select_next_info_res = conf_fun.connect_mysql_operation(select_next_info_sql, "operation", "dict")
    if not out_time:
        out_time = select_next_info_res[0]['out_time']
    if not need:
        need = select_next_info_res[0]['need']
    if select_next_info_res[0]['next_info'] and next_info:
        next_info = select_next_info_res[0]['next_info'] + "\n" + user_name + ":" + next_info
    elif next_info:
        next_info = user_name + ":" + next_info
    update_sql = "update job set out_time='%s',need='%s',next_info='%s' where id='%s';" \
                 % (out_time, need, next_info, job_id)
    print("update_sql: ", update_sql)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-点击删除
def delete_initiate_job(request):
    print("\n", "已提交工单-点击删除:", request.GET)
    job_id = request.GET.getlist("job_id[]", None)
    for item in job_id:
        delete_sql = "delete from job where id='%s';" % item
        conf_fun.connect_mysql_operation(delete_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-结单确认
def sure_initiate_job(request):
    print("\n", "已提交工单-结单确认:", request.GET)
    job_id = request.GET.get("job_id", None)

    # 逾期检测
    now_time = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "%Y/%m/%d %H:%M")
                + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M")

    select_time_sql = "select out_time from job where id='%s';" % job_id
    select_time_res = conf_fun.connect_mysql_operation(select_time_sql, "operation", "dict")

    if now_time > select_time_res[0]['out_time']:
        update_sql = "update job set status='%s' where id='%s';" \
                     % ("逾期完成", job_id)
    else:
        update_sql = "update job set status='%s' where id='%s';" \
                     % ("已完成", job_id)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# 已提交工单-结单驳回
def refuse_initiate_job(request):
    print("\n", "已提交工单-结单驳回:", request.GET)
    job_id = request.GET.get("job_id", None)
    update_sql = "update job set status='%s' where id='%s';" \
                 % ("进行中", job_id)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# ---------------------------------- 已接取工单

# 已接工单-查询
def select_receive_job(request):
    print("\n", "已接工单-查询:", request.GET)

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    login_user = user_info.split("@")[0]

    select_sql = "select * from job where (status='进行中' or status='结单中') and receive_person='%s';" % login_user
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")
    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


# 已接工单-结单
def update_receive_job(request):
    print("\n", "已接工单-结单:", request.GET)
    job_id = request.GET.get("job_id", None)
    update_sql = "update job set status='%s' where id='%s';" \
                 % ("结单中", job_id)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# ---------------------------------- 待处理工单

# 待处理工单-查询
def select_wait_job(request):
    print("\n", "待处理工单-查询:", request.GET)

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = user_info.split("@")[0]

    select_sql = "select * from job where receive_person='%s' and status='%s';" \
                 % (user_name, "已发起")
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


# 待处理工单-接取
def receive_wait_job(request):
    print("\n", "待处理工单-接取:", request.GET)
    job_id = request.GET.get("job_id", None)
    update_sql = "update job set status='%s' where id='%s';" \
                 % ("进行中", job_id)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# 待处理工单-转派
def turn_wait_job(request):
    print("\n", "待处理工单-转派:", request.GET)
    job_id = request.GET.get("job_id", None)
    receive_department = request.GET.get("receive_department", None)
    receive_person = request.GET.get("receive_person", None)
    update_sql = "update job set receive_department='%s',receive_person='%s' where id='%s';" \
                 % (receive_department, receive_person, job_id)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# 待处理工单-驳回
def refuse_wait_job(request):
    print("\n", "待处理工单-驳回:", request.GET)
    job_id = request.GET.get("job_id", "")
    refuse_reason = request.GET.get("refuse_reason", "")
    update_sql = "update job set refuse_reason='%s',status='%s' where id='%s';" \
                 % (refuse_reason, "被驳回", job_id)
    conf_fun.connect_mysql_operation(update_sql, "operation")
    res = {"code": 200}
    return JsonResponse(res)


# ---------------------------------- 历史工单

# 历史工单-查询
def select_history_job(request):
    print("\n", "历史工单-查询:", request.GET)

    out_date = request.GET.get("out_date", None)
    page = int(request.GET.get("page", "1"))

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = user_info.split("@")[0]

    if out_date:
        next_date = datetime.datetime.strftime(
            datetime.datetime.strptime(out_date, "%Y/%m/%d") + datetime.timedelta(days=1), "%Y/%m/%d")

        select_sql = "select * from job where out_time<'" + next_date + "' and out_time>='" + out_date + \
                     "' and receive_person='%s' " \
                     "and (status='已完成' or status='逾期完成');" \
                     % user_name
    else:
        select_sql = "select * from job where receive_person='%s' " \
                     "and (status='已完成' or status='逾期完成');" % user_name

    print("select_sql: ", select_sql)
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    # 发单部门、发单人、接单部门、接单人、工单类型、发单时间、截单时间、需求、跟进、状态
    # 获取总行数
    all_num = len(select_res)
    # 分页
    page_start = (page - 1) * 20
    page_end = page * 20
    res_data = select_res[page_start: page_end]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    return JsonResponse(res)


# ---------------------------------- 所有工单

# 所有工单-查询
def select_all_department_job(request):
    print("\n", "所有工单-查询:", request.GET)

    select_sql = "select * from job where receive_department='运营增长部' order by id desc;"
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


# ---------------------------------- 工单统计

# 工单统计-查询
def get_management_job(request):
    print("\n", "工单管理-查询:", request.GET)

    page = int(request.GET.get("page", "1"))

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = user_info.split("@")[0]

    allow_person = ["何鹏", "黄凤媛", "IT测试"]

    # 权限认证
    if user_name not in allow_person:
        res = {"code": 4041, "msg": "权限不足!"}
        return JsonResponse(res)

    department_name = "运营增长部"
    # 今天的日期
    now_date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=8), "%Y/%m/%d")
    # 本周周一的日期
    week_start_date = datetime.datetime.strftime(
        datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday()), "%Y/%m/%d")
    # 明天的日期
    next_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")

    # 部门工单统计

    # 该部门当日工单数量
    select_day_sql = "select count(id) from job where receive_department='%s' " \
                     "and out_time<'%s' and out_time>'%s';" \
                     % (department_name, next_date, now_date)
    print("select_day_sql:", select_day_sql)
    select_day_res = conf_fun.connect_mysql_operation(select_day_sql, "operation")
    if len(select_day_res) > 0:
        day_number = select_day_res[0][0]
    else:
        day_number = "0"
    # 该部门本周工单数量
    select_week_sql = "select count(id) from job where receive_department='%s' " \
                      "and out_time<'%s' and out_time>'%s';" \
                      % (department_name, next_date, week_start_date)
    print("select_week_sql:", select_week_sql)
    select_week_res = conf_fun.connect_mysql_operation(select_week_sql, "operation")
    if len(select_week_res) > 0:
        week_number = select_day_res[0][0]
    else:
        week_number = "0"
    # 该部门本周逾期工单数量
    select_out_sql = "select count(id) from job where receive_department='%s' " \
                     "and out_time<'%s' and out_time>'%s' and status='%s';" \
                     % (department_name, next_date, week_start_date, "逾期完成")
    print("select_out_sql:", select_out_sql)
    select_out_res = conf_fun.connect_mysql_operation(select_out_sql, "operation")
    if len(select_out_res) > 0:
        out_number = select_day_res[0][0]
    else:
        out_number = "0"

    department_list = [day_number, week_number, out_number]

    # 员工工单统计

    person_list = []
    select_person_sql = "select * from department_person where department_name='%s';" % department_name
    select_person_res = conf_fun.connect_mysql_operation(select_person_sql, "operation", "dict")
    for item in select_person_res:
        small_list = list()
        small_list.append(item['person_name'])
        # 该人员的即时工单数量
        select_person_num_sql = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                % (item['person_name'], "即时")
        select_person_num_res = conf_fun.connect_mysql_operation(select_person_num_sql, "operation")
        if len(select_person_num_res) > 0:
            small_list.append(select_person_num_res[0][0])
        else:
            small_list.append("0")
        # 该人员远期工单数量
        select_person_num_sql2 = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                 % (item['person_name'], "远期")
        select_person_num_res2 = conf_fun.connect_mysql_operation(select_person_num_sql2, "operation")
        if len(select_person_num_res2) > 0:
            small_list.append(select_person_num_res2[0][0])
        else:
            small_list.append("0")

        person_list.append(small_list)

    # 逾期工单统计

    select_department_out_sql = "select * from job where receive_department='%s' and status='逾期完成';" % department_name
    select_department_out_res = conf_fun.connect_mysql_operation(select_department_out_sql, "operation", "dict")
    # 获取总行数
    all_num = len(select_department_out_res)
    # 分页
    page_start = (page - 1) * 50
    page_end = page * 50
    select_department_out_res = select_department_out_res[page_start:page_end]
    res = {"code": 200, "department_list": department_list, "person_list": person_list,
           "out_time_list": select_department_out_res, "all_num": all_num}
    return JsonResponse(res)


# 工单统计-条件查询
def select_management_job(request):
    print("\n", "工单管理-条件查询:", request.GET)

    select_range = request.GET.get("select_range", "")

    user_info = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = user_info.split("@")[0]

    allow_person = ["何鹏", "黄凤媛", "IT测试"]

    # 权限认证
    if user_name not in allow_person:
        res = {"code": 4041, "msg": "权限不足!"}
        return JsonResponse(res)

    department_name = "运营增长部"

    person_list = []
    select_person_sql = "select * from department_person where department_name='%s';" % department_name
    select_person_res = conf_fun.connect_mysql_operation(select_person_sql, "operation", "dict")
    for item in select_person_res:
        small_list = list()
        small_list.append(item['person_name'])

        if select_range == "本月":
            month_start_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/")
            month_start_date += "00"
            # 该人员的即时工单数量
            select_person_num_sql = "select count(id) from job where receive_person='%s' " \
                                    "and job_type='%s' and out_time>'%s';" \
                                    % (item['person_name'], "即时", month_start_date)
            # 该人员远期工单数量
            select_person_num_sql2 = "select count(id) from job where receive_person='%s' " \
                                     "and job_type='%s' and out_time>'%s';" \
                                     % (item['person_name'], "远期", month_start_date)
        elif select_range == "本周":
            week_start_date = datetime.datetime.strftime(
                datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday()), "%Y/%m/%d")
            # 该人员的即时工单数量
            select_person_num_sql = "select count(id) from job where receive_person='%s' " \
                                    "and job_type='%s' and out_time>'%s';" \
                                    % (item['person_name'], "即时", week_start_date)
            # 该人员远期工单数量
            select_person_num_sql2 = "select count(id) from job where receive_person='%s' " \
                                     "and job_type='%s' and out_time>'%s';" \
                                     % (item['person_name'], "远期", week_start_date)
        elif select_range == "今天":
            today_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d")
            # 该人员的即时工单数量
            select_person_num_sql = "select count(id) from job where receive_person='%s' " \
                                    "and job_type='%s' and out_time>'%s';" \
                                    % (item['person_name'], "即时", today_date)
            # 该人员远期工单数量
            select_person_num_sql2 = "select count(id) from job where receive_person='%s' " \
                                     "and job_type='%s' and out_time>'%s';" \
                                     % (item['person_name'], "远期", today_date)
        else:
            # 该人员的即时工单数量
            select_person_num_sql = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                    % (item['person_name'], "即时")
            # 该人员远期工单数量
            select_person_num_sql2 = "select count(id) from job where receive_person='%s' and job_type='%s';" \
                                     % (item['person_name'], "远期")
        # 查询该人员的即时工单数量
        select_person_num_res = conf_fun.connect_mysql_operation(select_person_num_sql, "operation")
        if len(select_person_num_res) > 0:
            small_list.append(select_person_num_res[0][0])
        else:
            small_list.append("0")
        # 查询该人员远期工单数量
        select_person_num_res2 = conf_fun.connect_mysql_operation(select_person_num_sql2, "operation")
        if len(select_person_num_res2) > 0:
            small_list.append(select_person_num_res2[0][0])
        else:
            small_list.append("0")

        person_list.append(small_list)

    res = {"code": 200, "person_list": person_list}
    return JsonResponse(res)


# 工单统计-员工详情
def select_one_management_job(request):
    print("\n", "工单管理-员工详情:", request.GET)

    receive_person = request.GET.get("receive_person", None)
    page = int(request.GET.get("page", "1"))

    select_sql = "select * from job where receive_person='%s';" % receive_person
    select_res = conf_fun.connect_mysql_operation(select_sql, "operation", "dict")

    # 获取总行数
    all_num = len(select_res)
    # 分页
    page_start = (page - 1) * 50
    page_end = page * 50
    res_data = select_res[page_start: page_end]
    res = {"code": 200, "data": res_data, "all_num": all_num}
    return JsonResponse(res)
