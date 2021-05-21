from django.urls import path
from customer_management.settings import get_email_qq,conf_fun
from customer_management.views import customer_information, email_analysis, email_manage, \
    email_reply, template_manage,product_delivery


urlpatterns = [
    # 邮件上传模板管理
    path('email_template_manage', template_manage.Email_Upload_Manage.as_view({
        'get':'list',
        'post':'create',
        'delete':'delete',
        'put':'alter'
    })),
    # 邮件模板管理
    path('email_template_detail/', template_manage.email_template_detail, name ='email_template_detail'),

    # 邮件站内站外管理中
    path('email_manage', email_manage.Email_Manage.as_view({'get': 'list'})),

    # 站内 站外邮件客户回复 '''订单的数据查询'''
    path('order_num_inquire/', email_reply.order_search, name ='order_num_inquire'),
    # 邮件回复详情

    path('email_manage_detail/',email_manage.email_manage_detail, name ='email_manage_detail'),

   # 邮件翻译和模板匹配
    path('translate_semantic_analysis/', email_reply.translate_semantic_analysis, name='translate_semantic_analysis'),
    # 爬邮件
    path('reptile_email/', get_email_qq.run_get_email, name ='reptile_email'),
    #  回复客户用户
    path('customer_reply_email/', email_reply.customer_reply_email, name ='customer_reply_email'),
    #查询工厂反馈
    path('factory_feedback/', email_reply.factory_feedback, name ='factory_feedback'),

    # 客户数据库
    path('customer_database', customer_information.Customer_Information.as_view({'get': 'list',
                                                                                 'post': 'create',
                                                                                 'put':'alter',
                                                                              'delete':'delete'})),

    # 邮件分析
    path('email_analysis', email_analysis.Mail_Analysis.as_view({'get': 'list'})),
    # 好评分析
    path('nice_comment', email_analysis.Nice_Comment.as_view({'get': 'list'})),
    # 问题邮件分析汇总
    path('email_analysis_all/', email_analysis.email_analysis_all, name ='email_analysis_all'),

    # 产品推送
    path('product_delivery', product_delivery.Product_delivery.as_view({'get':'list','post':'create'})),
    # 站内翻译接口
    path('re_message_translate/', email_reply.message_translate, name ='message_translate'),
    #
    path('down_load_file/', conf_fun.down_load_file, name = 'down_load_file'),
    
]

