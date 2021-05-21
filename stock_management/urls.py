from django.urls import path


from stock_management import jx_views
from stock_management import jx_views1
from stock_management import jx_select_container
from stock_management.scheduling_management import schedule_demo,operating_data,\
    container_serach,sku_search,schedule_detail,order_confirmation,production_management,\
    Inventory_forecast,build_warehouse_script,order_form_generate
urlpatterns = [

    # 按sku货柜检索 查询
    path('select_container_by_sku/',jx_select_container.select_container_by_sku),
    # 货柜检索 获取侧边栏
    path('get_sidebar_select_container/',jx_select_container.get_sidebar_select_container),
    # 货柜检索 查询
    path('select_container/',jx_select_container.select_container),
    # 库存管理-获取侧边栏
    path('get_calculated_inventory_sidebar/',jx_views1.get_calculated_inventory_sidebar),
    # 库存管理-库存测算
    path('calculated_inventory/',jx_views.calculated_inventory),
    # 库存管理-库存测算2.0
#    path('calculate_inventory/',jx_views.calculate_inventory),
    # 库存测算主函数3.0
    path('calculate_inventory/',jx_views1.calculate_inventory_three),
    # 库存管理-库存测算3.0版本-编辑
    path('update_variable/',jx_views1.update_variable),
    # 库存管理-库存测算2.0版本-获取公共数据
    path('get_public_data/',jx_views.get_public_data),
    # 库存管理-库存监控
#    path('monitor_inventory/',jx_views.monitor_inventory),
    # 库存管理-库存监控3.0
    path('monitor_inventory1/',jx_views1.monitor_inventory),
    # 库存管理-订单需求-生成
    path('insert_order_request/',jx_views.insert_order_request),
    # 库存管理-订单需求-查询
    path('select_order_request/',jx_views.select_order_request),
    # 排期管理
    path('schedule_home_page' , schedule_demo.Schedule_Calendar.as_view({'get': 'list', 'post':'create'})),
    # 海外仓接口
#    path('oversea_location_sku/', operating_data.oversea_location_sku),
#    path('oversea_location_create_file/', operating_data.oversea_location_create_file),
    #运营资料上传
    path('operating_upload' , operating_data.Operating_Data_upload.as_view( { 'get':'list', 'post': 'create',
                                                                              'put':'alter','delete': 'delete'})),
     # 货柜检索
    path('container_search/', container_serach.container_search , name = 'container_search'),
   # sku检索
    path('sku_search/', sku_search.sku_search, name='sku_search'),
	path('place_order_page/', schedule_demo.place_order , name ='place_order_page'),
     # 货柜详情
    path('schedule_detail/', schedule_detail.schedule_detail , name ='schedule_detail'),
        # 新增货柜的sku搜索
#    path('schedule_sku_search/' ,schedule_demo.sku_search ,  name ='schedule_sku_search'),
        # 订单集成
    path('order_confirmation/', order_confirmation.Order_Confirmation.as_view({ 'get':'list','post':'create'})),

    # path('is_open/',views.is_open),
    # path('auto_place_order/',views.auto_place_order),
    # 每日库存盘点
    path(r'daily_inventory/', production_management.daily_inventory, name='daily_inventory'),
    # 每日盘点
    path('get_order_distribution_supplier/', production_management.get_order_distribution_supplier, name='get_order_distribution_supplier'),
      # 库存预测已经补货
    path('Inventory_forecast/', Inventory_forecast.Inventory_Forcast.as_view({'get':'list',
                                                                              'post': 'create'})),
                                                                               # 建立参考信息表
    # 建仓函数脚本
    path('warehouse_script/', build_warehouse_script.warehouse_script, name='warehouse_script'),
    # 返回分配工厂的sku和数量
     path('get_distribution_sku/', build_warehouse_script.get_distribution_sku, name='get_distribution_sku'),
    # 重新生成下单表
    path('order_form_generate/', order_form_generate.order_from, name='order_form_generate'),
    # 生成海外仓
    path('fbm_warehouse/',build_warehouse_script.fbm_warehouse, name ='fbm_warehouse'),
    # 货柜建设新
    path('container_serach_v2/',container_serach.Container_serch_v2.as_view({'get':'list'})),

]