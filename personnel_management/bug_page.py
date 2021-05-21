from django.http import JsonResponse
import pymysql
import time
import datetime
import requests
import json
from urllib.parse import unquote
from settings import conf_fun

# def connect_mysql(sql_text, dbs='operation', type='tuple'):
#     conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql',
#                            passwd='Bymy2021_', db=dbs)
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
# 增  bug提交页面

def insert_bug_table(request):
    print("\n", "增  bug提交页面", "\n")
    print(request.POST)
    user_msg = unquote(request.META.get('HTTP_AUTHORIZATION'))
    user_name = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[0]
    print('请求权限1111111111', user_msg )
    login_user = user_name
    project_name = "运营系统"
    page_name = request.POST.get("page_name", "")
    bug_details = request.POST.get("bug_details", "")
    picture = request.FILES.get("picture", "")

    timestamp = int(time.time())
    time_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")

    select_only_id_sql = "select * from task where product_name='%s' and task_name='%s';" % (project_name, page_name)
    select_only_id_res = conf_fun.connect_mysql_operation(select_only_id_sql, "task_distribution", "dict")
    # leading_end
    leading_end_only_id = ""
    leading_end_point = ""
    leading_end_receiver = ""
    # back_end
    back_end_only_id = ""
    back_end_point = ""
    back_end_receiver = ""

    for select_only_id_res_item in select_only_id_res:
        if select_only_id_res_item['type'] == "前端":
            leading_end_only_id = select_only_id_res_item['id']
            leading_end_point = select_only_id_res_item['point']
            leading_end_receiver = select_only_id_res_item['receiver']
        if select_only_id_res_item['type'] == "后端":
            back_end_only_id = select_only_id_res_item['id']
            back_end_point = select_only_id_res_item['point']
            back_end_receiver = select_only_id_res_item['receiver']

    save_path = ""
    # 保存图片
    if picture:
        upload_path = "images/upload_bug/" + picture.name
        get_url = "http://106.53.250.215:8897/server/upload_file/"
        file_obj = {"file_obj": picture}
        get_res = requests.post(url=get_url, files=file_obj, data={"save_path": upload_path})
        print(get_res)
        print(get_res.text)
        get_data = json.loads(get_res.text)
        if get_data['code'] != 200:
            res = {"code": 4041, "msg": "上传失败"}
            return JsonResponse(res)

        save_path = "http://106.53.250.215:8897/static/" + upload_path
        save_catalog = "/home/by_operate/static/operation/bug_file/" + picture.name
        # save_catalog = "/home/beyong_supply_chain/static/images/upload_bug/" + picture.name

        with open(save_catalog, "wb") as fw:
            for i in picture:
                fw.write(i)

    insert_leading_end_sql = "insert into bug_table(product_name,only_id," \
                             "task_name,point,only_time,receiver,complete," \
                             "bug_detail,type,is_trans,bug_picture,change_exmine," \
                             "release_bug_time,release_bug_people,is_pick_up) " \
                             "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                             "'%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                             % (project_name, leading_end_only_id, page_name,
                                leading_end_point, timestamp, leading_end_receiver, 0,
                                bug_details, "前端", 0, save_path, 0, time_str, login_user, 0)

    insert_back_end_sql = "insert into bug_table(product_name,only_id," \
                          "task_name,point,only_time,receiver,complete," \
                          "bug_detail,type,is_trans,bug_picture,change_exmine," \
                          "release_bug_time,release_bug_people,is_pick_up) " \
                          "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                          "'%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
                          % (project_name, back_end_only_id, page_name,
                             back_end_point, timestamp, back_end_receiver, 0,
                             bug_details, "后端", 0, save_path, 0, time_str, login_user, 0)

    print("insert_leading_end_sql: ", insert_leading_end_sql)
    print("insert_back_end_sql: ", insert_back_end_sql)
    conf_fun.connect_mysql_operation(insert_leading_end_sql, "task_distribution")
    conf_fun.connect_mysql_operation(insert_back_end_sql, "task_distribution")

    res = {"code": 200}
    return JsonResponse(res)


# 删个人提交的bug(未审核或审核不通过的才可)  bug提交页面
def delete_bug_table(request):
    print("\n", "删个人提交的bug(未审核或审核不通过的才可)  bug提交页面", "\n")
    print(request.GET)

    data_id = request.GET.getlist("data_id", "")
    print(data_id)

    # 查询数据状态，如果已审核通过，拒绝
    for data_id_item in data_id:
        select_sql = "select * from bug_table where bug_only_id='%s';" % data_id_item
        print(select_sql)
        select_res = conf_fun.connect_mysql_operation(select_sql, "task_distribution", "dict")
        if select_res:
            if select_res[0]['complete'] != "0":
                res = {"code": 4041, "msg": "有任务已在处理中,删除请联系IT部。"}
                return JsonResponse(res)

    if len(data_id) > 1:
        delete_sql = "delete from bug_table where bug_only_id in %s;" % str(tuple(data_id))
    elif len(data_id) == 1:
        delete_sql = "delete from bug_table where bug_only_id=%s;" % int(data_id[0])
    else:
        delete_sql = "delete from bug_table where bug_only_id='';"
    print(delete_sql)
    conf_fun.connect_mysql_operation(delete_sql, "task_distribution")
    res = {"code": 200}
    return JsonResponse(res)


# 改个人提交的bug  bug提交页面
def update_bug_table(request):
    print("\n", "改个人提交的bug  bug提交页面", "\n")
    print(request.POST)

    data_id = request.POST.get("data_id", "")
    bug_details = request.POST.get("bug_details", "")
    picture = request.FILES.get("picture", "")

    # 查询数据状态，如果已审核通过，拒绝
    select_sql = "select * from bug_table where bug_only_id='%s';" % data_id
    select_res = conf_fun.connect_mysql_operation(select_sql, "task_distribution", "dict")
    if select_res[0]['complete'] != "0":
        res = {"code": 4041, "msg": "该任务已在处理中,修改请联系IT部。"}
        return JsonResponse(res)

    save_path = ""
    if picture:
        # 保存图片
        upload_path = "images/upload_bug/" + picture.name
        get_url = "http://106.53.250.215:8897/server/upload_file/"
        file_obj = {"file_obj": picture}
        get_res = requests.post(url=get_url, files=file_obj, data={"save_path": upload_path})
        print(get_res)
        print(get_res.text)
        get_data = json.loads(get_res.text)
        if get_data['code'] != 200:
            res = {"code": 4041, "msg": "上传失败"}
            return JsonResponse(res)

        save_path = "http://106.53.250.215:8897/static/" + upload_path

    update_sql = "update bug_table set bug_detail='%s',bug_picture='%s' where bug_only_id='%s';" \
                 % (bug_details, save_path, data_id)
    conf_fun.connect_mysql_operation(update_sql, "task_distribution")

    res = {"code": 200}
    return JsonResponse(res)


# 查个人提交的bug  bug提交页面
def select_bug_table(request):
    print("\n", "查个人提交的bug  bug提交页面", "\n")
    print(request.GET)

    # permission = eval(request.session.get("permissions", ""))
    user_name = unquote(request.META.get('HTTP_AUTHORIZATION')).split('@')[0]
    login_user = user_name

    select_sql = "select * from bug_table where release_bug_people='%s';" % login_user
    select_res = conf_fun.connect_mysql_operation(select_sql, "task_distribution", "dict")

    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


# 获取页面下拉框数据  bug提交页面
def get_page_down_box(request):
    print("\n", "获取页面下拉框数据  bug提交页面", "\n")

    page_list = list()

    select_sql = "select * from task where product_name='运营系统' and done_time is not null;"
    select_res = conf_fun.connect_mysql_operation(select_sql, "task_distribution", "dict")

    for select_res_item in select_res:
        if select_res_item['task_name'] not in page_list:
            page_list.append(select_res_item['task_name'])

    res = {"code": 200, "data": page_list}
    return JsonResponse(res)
