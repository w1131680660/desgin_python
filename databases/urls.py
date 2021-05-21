from django.urls import path
from databases import views1
from databases import jx_views4
from databases import jx_views
from databases import store_information,product_information, commodity_information,return_report, withdrawal_page,commodity_script
from databases import operation_daily
from databases import  overseas_warehouse_barcode
urlpatterns = [
    # 结算报告
    path('get_all_order/',views1.get_all_order),
    path('get_store_country/',views1.get_store_country),
    # 历史运营数据
    path('get_history_report/',views1.get_history_report),
    path('get_sku_order_summary/',views1.get_sku_order_summary),
    #每日运营日报
    path('get_report_beside/',views1.get_report_beside),
    path('get_everyday_report/',views1.get_everyday_report),
    path('get_everyday_sku_order_summary/',views1.get_everyday_sku_order_summary),
    path('get_gy_data/',views1.get_gy_data),
    path('get_eu_gy_data/',views1.get_eu_gy_data),
    path('get_eu_order_data/',views1.get_eu_order_data),
    # 库存
    path('get_search/',views1.get_search),
    path('get_search_data/',views1.get_search_data),
    path('get_stock_data/',views1.get_stock_data),
    # 店铺信息
    path('store_information', store_information.Store_Information.as_view({'get':'list',
                                                                           'post':'create',
                                                                           'put':'alter'})),
    # 产品信息
    path('product_information', product_information.Product_Information.as_view({'get':'list',
                                                                           'post':'create',
                                                                           'put':'alter',
                                                                            'delete':'delete'})), 
       # 产品信息详情
    path('product_information_detail', product_information.detail_product, name= 'product_information'),
    # 商品信息                                                                           
    path('commodity_information', commodity_information.Commodity_Information.as_view({'get': 'list',
                                                                                 'post': 'create',
                                                                                 'put': 'alter',
                                                                                 'delete': 'delete'})),  
    # 商品信息核对时间
    path('commodity_check_time/',jx_views.commodity_check_time),                                        	                                                                
    # 产品条码
    path('select_barcode/',jx_views4.select_barcode),
    path('get_barcode/',jx_views4.get_barcode),
    path('upload_barcode/',jx_views4.upload_barcode),
    path('delete_barcode/',jx_views4.delete_barcode),
    # 一键下载未上传文件的商品数据
    path('export_without_barcode_data/',jx_views4.export_without_barcode_data),
    # 数据库-产品条码-获取待审核数据
    path('get_check_barcode/',jx_views4.get_check_barcode),
    # 数据库-产品条码-审核
    path('check_barcode/',jx_views4.check_barcode),
    # 文字文档
    path('select_text/',jx_views4.select_text),
    path('get_select_text/',jx_views4.get_select_text),
    path('update_text/',jx_views4.update_text),
    path('delete_text/',jx_views4.delete_text),
    path('insert_text/',jx_views4.insert_text),
    # 设计图片
    path('select_picture/',jx_views4.select_picture),
    # 数据库-设计图片-查询(说明书pdf需要)
    path('old_select_picture/',jx_views4.old_select_picture),
    path('get_select_picture/',jx_views4.get_select_picture),
    # 数据库-设计图片-单个下载
    path('batch_download/',jx_views4.batch_download),
    # 数据库-设计图片-查看大图
    path('get_big_pic/',jx_views4.get_big_pic),
    # 数据库-设计图片-查看链接
    path('show_url/',jx_views4.show_url),
    # VAT报告-查询
    path('select_vat_report/',jx_views.select_vat_report),
    # VAT报告-上传
    path('upload_vat_report/',jx_views.upload_vat_report),
    # 库存报告-查询
    path('select_inventory_report/',jx_views.select_inventory_report),
    # 库存报告-获取下拉框数据
    path('get_select_inventory_report/',jx_views.get_select_inventory_report),
    # 下载文件接口
    path('download_file/',jx_views.download_file),
    # 交易报告/汇总报告/周期结算报告-上传
    path('upload_many_report/',jx_views.upload_many_report),
    # 交易报告/汇总报告/周期结算报告-查询
    path('select_many_report/',jx_views.select_many_report),
    # 交易报告/汇总报告/周期结算报告-获取下拉框数据
    path('get_select_many_report/',jx_views.get_select_many_report),
       # 退款报告
    path('return_report/', return_report.Reruen_Report.as_view({'get': 'list',
                                                                'post': 'create'})),
    path('withdrawal_page/' , withdrawal_page.Withdrawal.as_view({'get': 'list',
                                                                'post': 'create'})),
                                                                 #商品文件上传
    path('commodity_script/',commodity_script.create_com_func,name ='commodity_script'),
    path('operation_daily/', operation_daily.operation_excel.as_view({'get': 'list'})),
    # 海外仓条码
    path('overseas_warehouse_barcode/',overseas_warehouse_barcode.Oversea_warehouse_barcode.as_view({'get': 'list',
                                                                                 'post': 'create',
                                                                                 'put': 'alter',
                                                                                 'delete': 'delete'}))
]