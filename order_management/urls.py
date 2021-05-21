from django.urls import path

from order_management import views1
from order_management import views2

from order_management.operational_data.order_tracking import timeout_orders,every_order,container_transit,inventory_page
from order_management.operational_data.advertising_guide import advertising_guide
from order_management.operational_data.advertising_guide import upload_rank,upload_auto
from order_management.operational_data.order_analysis import order_refund,return_goods
urlpatterns = [
    # 公共获取渠道、站点、国家
    path('get_channel_site_country/',views1.get_channel_site_country),
    # 在途库存盘点——获取部分下拉数据
    path('get_search/',views1.get_search),
     # 在途库存盘点——获取盘点数据
    path('on_way_container/',views1.on_way_container),
    # 广告管理——获取渠道/站点/国家（目前用颜劲的接口，此接口未用）
    path('get_arg/',views1.get_arg),
    # 广告管理——获取spu
    path('get_spu/',views1.get_spu),
    # 广告管理——获取数据
    path('get_data/',views1.get_data),
    # 广告词监控——上传数据
    path('advertising_monitor_upload/',views1.advertising_monitor_upload),
    # 广告词监控——获取评分数据
    path('get_star_data/',views1.get_star_data),
    # 广告词监控——获取排名数据
    path('get_rank_data/',views1.get_rank_data),
    # 广告词监控——编辑提交
    path('advertising_edit_submit/',views1.advertising_edit_submit),
    # 广告词监控——获取广告词监控数据
    path('advertising_monitor_data/',views1.advertising_monitor_data),
    path('advertising_monitor_edit/',views1.advertising_monitor_edit),
    # 一键同步广告指导
    path('advertisement_guidance_synchro/',views1.advertisement_guidance_synchro),
    # 广告管理——店铺
    path('advertising_shop_country/',views1.advertising_shop_country),
    path('advertising_shop/',views1.advertising_shop),
    path('get_spu_advertising_data/',views1.get_spu_advertising_data),
    path('upload_advertising_shop_data/',views1.upload_advertising_shop_data),
    path('choose_advertising_shop_data/',views1.choose_advertising_shop_data),
    path('edit_advertising_shop_data/',views1.edit_advertising_shop_data),
    # FBM
    path('yc_batch_create_order/',views1.yc_batch_create_order),
    path('txt_order/',views1.txt_order),
    path('download_err_report/',views1.download_err_report),
    # 问题订单
    path('get_warehouse/',views1.get_warehouse),
    path('get_bad_order/',views1.get_bad_order),
    path('order_edit/',views1.order_edit),
    path('err_order_select/',views1.err_order_select),
    path('err_order_detail/',views1.err_order_detail),
    path('err_order_delete/',views1.err_order_delete),
    path('usa_order_deliver/',views1.usa_order_deliver),
    path('repair_defeated_order/',views1.repair_defeated_order),
    path('address_overlength/',views1.address_overlength),
    path('fake_tracking_no_view/',views1.fake_tracking_no_view),
    path('edit_remark/',views1.edit_remark),
    path('fake_tracking_no_export/',views1.fake_tracking_no_export),
    path('ca_shipment_data/',views1.ca_shipment_data),
    path('ca_shipment_update_data/',views1.ca_shipment_update_data),
    path('ca_update_tracking_no/',views1.ca_update_tracking_no),
    path('ca_warehouse_data/',views1.ca_warehouse_data),
    path('ca_update_warehouse_data/',views1.ca_update_warehouse_data),
    path('ca_insert_warehouse_data/',views1.ca_insert_warehouse_data),
    path('update_delivery_date/',views2.update_delivery_date),
    path('upload_no_deliver_num/',views1.upload_no_deliver_num),
    path('ca_export_data/',views1.ca_export_data),
    path('ca_export_data1/',views1.ca_export_data1),
    path('oversea_location_sku_contrast_detail/',views1.oversea_location_sku_contrast_detail),
    path('oversea_location_sku_contrast_template/',views1.oversea_location_sku_contrast_template),
    path('oversea_location_sku_contrast_upload/',views1.oversea_location_sku_contrast_upload),
    path('sf_update_order_id/',views1.sf_update_order_id),
    path('sf_order_id_remark/',views1.sf_order_id_remark),
    path('err_order_remark/',views1.err_order_remark),
    path('ca_update_state/',views1.ca_update_state),
    path('oversea_location_sku_update/',views1.oversea_location_sku_update),
    path('oversea_location_sku_delete/',views1.oversea_location_sku_delete),
    path('ca_warehouse_data_template_download/',views1.ca_warehouse_data_template_download),
    path('ca_warehouse_data_template_upload/',views1.ca_warehouse_data_template_upload),
    path('no_deliver_order_data/',views1.no_deliver_order_data),
    path('count_invoice_data/',views1.count_invoice_data),
    path('create_invoice_data/',views1.create_invoice_data),
    path('get_US_error_order/',views1.get_US_error_order),
    path('get_upload_file_country/',views1.get_upload_file_country),
    path('upload_advertising_report/',views2.upload_advertising_report),

    # 订单跟踪
    path('warehouse_datas/',views1.warehouse_datas),
    path('order_track/',views1.order_track),
    path('single_order_deliver/',views1.single_order_deliver),
    # 一键导出订单数据
    path('order_track_download/',views1.order_track_download),
    # 超时订单
    path('get_search_data/',views1.get_search_data),
    path('get_timeout_order/',timeout_orders.Timeout_Order.as_view({'get':'list','put':'alter'})),
    # 订单统计
    path('order_statistics/',views1.order_statistics),
    path('get_warehouse_data/',views1.get_warehouse_data),
    # 订单查询
    path('get_order_detail/',views1.get_order_detail),
    # 海外仓配送模板
    path('get_template/',views1.get_template),
    path('get_template_data/',views1.get_template_data),
    path('upload_template/',views1.upload_template),
    path('add_work/',views1.add_work),
    path('get_examined_data/',views1.get_examined_data),
    path('examined_template_update/',views1.examined_template_update),
    path('template_datas/',views1.template_datas),
    path('template_datas_update/',views1.template_datas_update),
    # 订单分析
    # 订单退款率
    path('refund_rate/',views1.refund_rate),
    path('refund_rate_data/',views1.refund_rate_data),
    # 退货时间监控
    path('refund_times/',views1.refund_times),
    path('refund_times_monitor/',views1.refund_times_monitor),
    path('refund_times_deatil_data/',views1.refund_times_deatil_data),
    # 退货原因分析
    path('refund_reason/',views1.refund_reason),
    path('refund_reason_date/',views1.refund_reason_date),
       # 自动调整广告 new
    path('advertising_guide/',advertising_guide.Advertising_Guide.as_view( {'get':'list','put':'alter'})),
    path('get_auto_data/', advertising_guide.gey_auto_name , name ='get_auto_data'),
     # 上传排名接口
    path('upload_rank/', upload_rank.upload_rank, name='upload_rank'),
         # 这是手动组和广告组的对应关系
    path('Upload_transform_auto/', upload_auto.Upload_transform_auto.as_view( {'get':'list','put':'alter',
                                                                               'post':'create','delete':'delete'})),
    # 这是广告组和手动组的的对应关系
    path('upload_auto/', upload_auto.Upload_auto_ad.as_view( {'get':'list','put':'alter',
                                                                               'post':'create','delete':'delete'})),
                                                                                   # 订单分析
    path('order_refund/', order_refund.Order_Return.as_view({'get': 'list' })),
    # 退货分析
    path('return_goods/', return_goods.Return_Goods.as_view({'get': 'list'})),

    # 每日订单新
    path('every_order/',every_order.Sku_Order_every.as_view({'get': 'list'})),
    # 在途货柜盘点新
    path('container_transit/', container_transit.Container_transit.as_view({'get': 'list'})),
    # 库存页面新
    path('inventory_page/',inventory_page.Inventory_page.as_view({'get': 'list'}))
]