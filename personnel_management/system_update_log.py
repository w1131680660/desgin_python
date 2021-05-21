import datetime

from django.http import JsonResponse

from settings import conf_fun


# 增  系统更新日志
def insert_system_update_log(request):
    print("\n", "增  系统更新日志", "\n")
    print(request.POST)

    update_time = request.POST.get("update_time", "")
    update_person = request.POST.get("update_person", "")
    update_area = request.POST.get("update_area", "")
    update_info = request.POST.get("update_info", "")

    insert_sql = "insert into system_update_log(update_time,update_person,update_area,update_info) " \
                 "values('%s', '%s', '%s', '%s');" \
                 % (update_time, update_person, update_area, update_info)
    conf_fun.connect_mysql_operation(insert_sql, )
    res = {"code": 200}
    return JsonResponse(res)


# 删  系统更新日志
def delete_system_update_log(request):
    print("\n", "删  系统更新日志", "\n")
    print(request.GET)

    data_id = request.GET.getlist("data_id[]", "")
    print(data_id)
    delete_sql = ""
    if len(data_id) > 1:
        delete_sql = "delete from system_update_log where id in %s;" % str(tuple(data_id))
    elif len(data_id) == 1:
        delete_sql = "delete from system_update_log where id='%s';" % data_id[0]
    print(delete_sql)
    conf_fun.connect_mysql_operation(delete_sql)

    res = {"code": 200}
    return JsonResponse(res)


# 改  系统更新日志
def update_system_update_log(request):
    print("\n", "改  系统更新日志", "\n")
    print(request.POST)

    data_id = request.POST.get("data_id", "")
    update_time = request.POST.get("update_time", "")
    update_person = request.POST.get("update_person", "")
    update_area = request.POST.get("update_area", "")
    update_info = request.POST.get("update_info", "")

    update_sql = "update system_update_log set update_time='%s',update_person='%s'," \
                 "update_area='%s',update_info='%s' where id='%s';" \
                 % (update_time, update_person, update_area, update_info, data_id)
    print(update_sql)
    conf_fun.connect_mysql_operation(update_sql)
    res = {"code": 200}
    return JsonResponse(res)


# 查  系统更新日志
def select_system_update_log(request):
    print("\n", "查  系统更新日志", "\n")
    print(request.GET)

    update_area = request.GET.get("update_area", "")
    data_date = request.GET.get("data_date", "")

    select_sql = "select * from system_update_log where id!=''"
    if update_area:
        select_sql += " and update_area='%s'" % update_area
    if data_date:
        start_date = data_date.split("至")[0]
        end_date = data_date.split("至")[1]
        select_sql += " and update_time>='" + start_date + "'"
        select_sql += " and update_time<='" + end_date + "'"
    select_sql += " order by id desc;"
    select_res = conf_fun.connect_mysql_operation(select_sql, type='dict')
    res = {"code": 200, "data": select_res}
    return JsonResponse(res)


# 获取侧边栏  系统更新日志
def get_down_box_system_update_log(request):
    print("\n", "获取侧边栏  系统更新日志", "\n")
    print(request.GET)

    res_data = list()

    now_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    now_weekday = datetime.datetime.now().weekday()

    # 获取第一条数据的星期一的日期和星期日的日期
    select_first_data_week_sql = "select * from system_update_log order by update_time limit 1;"
    select_first_data_week_res = conf_fun.connect_mysql_operation(select_first_data_week_sql, type="dict")
    if len(select_first_data_week_res) == 0:
        res = {"code": 200, "data": res_data}
        return JsonResponse(res)
    first_data_weekday = datetime.datetime.strptime(select_first_data_week_res[0]['update_time'], "%Y-%m-%d").weekday()
    data_first_week_start_date = datetime.datetime.strftime(
        datetime.datetime.strptime(
            select_first_data_week_res[0]['update_time'], "%Y-%m-%d") - datetime.timedelta(
            days=first_data_weekday), "%Y-%m-%d")
    print("第一条数据的周一: ", data_first_week_start_date)
    data_first_week_end_date = datetime.datetime.strftime(
        datetime.datetime.strptime(data_first_week_start_date, "%Y-%m-%d") + datetime.timedelta(days=6), "%Y-%m-%d")
    print("第一条数据的周日: ", data_first_week_end_date)
    data_first_week = data_first_week_start_date + "至" + data_first_week_end_date

    # 获取当天所在的星期的星期一的日期和星期日的日期
    now_week_start_date = datetime.datetime.strftime(
        datetime.datetime.now() - datetime.timedelta(days=now_weekday), "%Y-%m-%d")
    now_week = now_week_start_date + "至" + now_date
    print("当天的周一: ", now_week_start_date)
    print("当天的日期: ", now_date)
    res_data.append(now_week)

    if now_week_start_date <= select_first_data_week_res[0]['update_time'] <= now_date:
        pass
    else:
        interval_day = 7
        while True:
            week_start = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    now_week_start_date, "%Y-%m-%d") - datetime.timedelta(days=interval_day), "%Y-%m-%d")
            week_end = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    now_week_start_date, "%Y-%m-%d") - datetime.timedelta(days=(interval_day - 6)), "%Y-%m-%d")
            interval_day += 7
            mark_week = week_start + "至" + week_end
            if mark_week != data_first_week:
                res_data.append(mark_week)
            else:
                res_data.append(mark_week)
                break

    res = {"code": 200, "data": res_data}
    return JsonResponse(res)
