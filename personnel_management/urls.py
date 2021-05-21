from django.urls import path

from personnel_management import views1
from personnel_management import views2

from personnel_management import jx_work_order

from personnel_management import authority_management
from personnel_management import bug_page, system_update_log,bug_feedback

urlpatterns = [
    # 人员资料
    path('personnel_data/',views1.personnel_data),
    path('personnel_add/',views1.personnel_add),
    path('personnel_edit/',views1.personnel_edit),
    path('personnel_del/',views1.personnel_del),
    # 培训
    path('train/',views1.train),
    path('train_work_add/',views1.train_work_add),
    path('train_file_add/',views1.train_file_add),
    path('train_file_view/',views1.train_file_view),
    path('train_file_del/',views1.train_file_del),
    path('train_score/',views1.train_score),
    # 绩效
    path('performance/',views1.performance),
    path('staff_performance/',views1.staff_performance),
    path('history_performance/',views1.history_performance),
    path('history_department_performance/',views1.history_department_performance),
    path('staff_performance_save/',views1.staff_performance_save),
    path('staff_performance_submit/',views1.staff_performance_submit),
    # 工单系统2.0
    # 已提交工单-获取所有部门
    path('get_department_down_box/', jx_work_order.get_department_down_box, name='get_department_down_box'),
    # 已提交工单-根据部门获取所有员工数据
    path('get_person_down_box/', jx_work_order.get_person_down_box, name='get_person_down_box'),
    # 已提交工单-点击查询
    path('select_initiate_job/', jx_work_order.select_initiate_job, name='select_initiate_job'),
    # 已提交工单-确认提交工单
    path('insert_initiate_job/', jx_work_order.insert_initiate_job, name='insert_initiate_job'),
    # 已提交工单-编辑弹窗点击确认
    path('update_initiate_job/', jx_work_order.update_initiate_job, name='update_initiate_job'),
    # 已提交工单-点击删除
    path('delete_initiate_job/', jx_work_order.delete_initiate_job, name='delete_initiate_job'),
    # 已提交工单-结单确认
    path('sure_initiate_job/', jx_work_order.sure_initiate_job, name='sure_initiate_job'),
    # 已提交工单-结单驳回
    path('refuse_initiate_job/', jx_work_order.refuse_initiate_job, name='refuse_initiate_job'),
    
    # 已接取工单-查询
    path('select_receive_job/', jx_work_order.select_receive_job, name='select_receive_job'),
    # 已接取工单-结单
    path('update_receive_job/', jx_work_order.update_receive_job, name='update_receive_job'),

    # 待处理工单-查询
    path('select_wait_job/', jx_work_order.select_wait_job, name='select_wait_job'),
    # 待处理工单-接取
    path('receive_wait_job/', jx_work_order.receive_wait_job, name='receive_wait_job'),
    # 待处理工单-转派
    path('turn_wait_job/', jx_work_order.turn_wait_job, name='turn_wait_job'),
    # 待处理工单-驳回
    path('refuse_wait_job/', jx_work_order.refuse_wait_job, name='refuse_wait_job'),

    # 历史工单-查询
    path('select_history_job/', jx_work_order.select_history_job, name='select_history_job'),

    # 所有工单-查询
    path('select_all_department_job/', jx_work_order.select_all_department_job, name='select_all_department_job'),

    # 工单统计-查询
    path('get_management_job/', jx_work_order.get_management_job, name='get_management_job'),
    # 工单统计-条件查询
    path('select_management_job/', jx_work_order.select_management_job, name='select_management_job'),
    # 工单统计-员工详情
    path('select_one_management_job/', jx_work_order.select_one_management_job, name='select_one_management_job'),
    # 工单

    # 权限管理
    path(r'authority_management/', authority_management.Authority_Management.as_view({'get':'list','post':'creat'})),
    path(r'add_user/', authority_management.add_user),
    path(r'get_all_rolas/', authority_management.get_all_rolas),


    # 登陆
    path(r'login/', views2.login),
    path(r'update_pswd/', views2.update_pswd),
    path(r'lock_user/', views2.lock_user),
    path(r'delete_user/', views2.delete_user),
    path(r'area_sign/', views2.area_sign),
    path(r'area_sign_data/', views2.area_sign_data),
    path(r'area_sign1/', views2.area_sign1),
    path(r'get_sign_country/', views2.get_sign_country),
    path(r'get_sign_area/', views2.get_sign_area),
    path(r'get_sign_country1/', views2.get_sign_country1),
    path(r'get_sign_area1/', views2.get_sign_area1),
    path(r'area_sign2/', views2.area_sign2),

    # 错误日志
    path('staff_error_log/',views1.staff_error_log),
    path('error_log_data/',views1.error_log_data),
    path('error_log_add/',views1.error_log_add),
    path('error_log_detail/',views1.error_log_detail),
        # 增  bug提交页面
    path('insert_bug_table/', bug_page.insert_bug_table, name='insert_bug_table'),
    # 删个人提交的bug(未审核或审核不通过的才可)  bug提交页面
    path('delete_bug_table/', bug_page.delete_bug_table, name='delete_bug_table'),
    # 改个人提交的bug  bug提交页面
    path('update_bug_table/', bug_page.update_bug_table, name='update_bug_table'),
    # 查个人提交的bug  bug提交页面
    path('select_bug_table/', bug_page.select_bug_table, name='select_bug_table'),
    # 获取页面名称下拉框
    path('get_page_down_box/', bug_page.get_page_down_box, name='get_page_down_box'),
        # 增  系统更新日志
    path('insert_system_update_log/', system_update_log.insert_system_update_log, name='insert_system_update_log'),
    # 删  系统更新日志
    path('delete_system_update_log/', system_update_log.delete_system_update_log, name='delete_system_update_log'),
    # 改  系统更新日志
    path('update_system_update_log/', system_update_log.update_system_update_log, name='update_system_update_log'),
    # 查  系统更新日志
    path('select_system_update_log/', system_update_log.select_system_update_log, name='select_system_update_log'),
    # 获取侧边栏  系统更新日志
    path('get_down_box_system_update_log/', system_update_log.get_down_box_system_update_log,
         name='get_down_box_system_update_log'),
    # bug反馈新
     path('bug_feedback/',bug_feedback.Bug_Return.as_view( {'get': 'list',
                                                            'post': 'create',
                                                            'put': 'alter',
                                                            'delete': 'delete'})),
    path('delete_page/',bug_feedback.delete_page, name='delete_page')
]