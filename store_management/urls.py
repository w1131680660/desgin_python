from django.urls import path

from store_management import jx_views4

urlpatterns = [

    # 品牌维护
    path('get_data_brand/',jx_views4.get_data_brand),
    path('insert_brand/',jx_views4.insert_brand),
    # 店铺管理-品牌维护-获取侧边栏
    path('get_select_brand/',jx_views4.get_select_brand),
    path('select_brand/',jx_views4.select_brand),
    path('insert_complain/',jx_views4.insert_complain),
    path('select_complain/',jx_views4.select_complain),
    # 店铺管理-申诉-编辑
    path('update_complain/',jx_views4.update_complain),
    # 店铺管理-申诉-删除
    path('delete_complain/',jx_views4.delete_complain),
    # 店铺管理-申诉-删除文件
    path('delete_file_complain/',jx_views4.delete_file_complain),
#    path('select_negative_comment/',jx_views4.select_negative_comment),
    path('update_negative_comment/',jx_views4.update_negative_comment),
    # 店铺管理-差评管理-查询2.0
    path('select_negative_comment/',jx_views4.select_negative_comment_two),
    
    path('select_q_a/',jx_views4.select_q_a),
    path('update_q_a/',jx_views4.update_q_a),
    path('select_email_alert/',jx_views4.select_email_alert),
    path('get_select_email_alert/',jx_views4.get_select_email_alert),
    # 店铺管理-店铺绩效-查询
    path('select_performance/',jx_views4.select_performance),
    # 店铺管理-店铺绩效-获取所有待审核指标
    path('get_index_performance/',jx_views4.get_index_performance),
    # 店铺管理-店铺绩效-插入
    path('insert_performance/',jx_views4.insert_performance),
    # 店铺管理-店铺绩效-编辑
    path('update_performance/',jx_views4.update_performance),
    # 店铺管理-店铺绩效-增加新指标
    path('add_index_performance/',jx_views4.add_index_performance),
    # 店铺管理-店铺绩效-审核新指标
    path('check_index_performance/',jx_views4.check_index_performance),
    # 店铺管理-邮件预警-获取问题类型(已审核)
    path('get_check_alert_type/',jx_views4.get_check_alert_type),
    # 店铺管理-邮件预警-获取待审核的问题类型(新增待审核/删除待确认,关键词为空)
    path('get_alert_type/',jx_views4.get_alert_type),
    # 店铺管理-邮件预警-问题类型新增(新增待审核)
    path('insert_alert_type/',jx_views4.insert_alert_type),
    # 店铺管理-邮件预警-问题类型删除(删除待确认)
    path('delete_alert_type/',jx_views4.delete_alert_type),
    # 店铺管理-邮件预警-问题类型管理-某一问题类型的关键词获取(已审核/删除待确认)
    path('get_keyword/',jx_views4.get_keyword),
    # 店铺管理-邮件预警-问题类型管理-某一问题类型的关键词编辑（增加/删除）
    path('update_keyword/',jx_views4.update_keyword),
    # 店铺管理-邮件预警-问题类型/关键词管理-审核
    path('check_keyword/',jx_views4.check_keyword),
    # 获取一个表的所有字段名
    path('get_columns/',jx_views4.get_columns),
    
]