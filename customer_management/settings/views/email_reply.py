import time
from django.http import JsonResponse
from customer_management.settings import conf_fun
from django.views.decorators.csrf import csrf_exempt
from customer_management.settings import conf_fun,settings,email_class
def sql_inquire(sql):
    data = conf_fun.connect_mysql_re(sql, type='dict')
    return data

''' 订单数据查询 查询order表  '''
def order_search_all(order_num ):

    us_sql = "SELECT o.warehouse_code ,o.quantity, o.customer_order_number,o.country_code,countries, the_store,r.platform_channels,r.product_code, r.sku ,r.product_name " \
             "FROM `order`.manually_create_order as  o ,reports.commodity_codes_zr as r " \
             "WHERE o.sku like CONCAT('%',r.sku,'%') AND o.country_code = r.countries AND " \
             "o.customer_order_number = '{0}'".format(order_num)
    print(us_sql)
    data = sql_inquire(us_sql)
    if not data:
        eu_sql = "SELECT o.warehouse_code ,o.quantity, o.reference_no, o.country_code," \
                 "o.quantity,o.product_sku,r.product_name,r.product_code, r.sku ,r.product_name" \
                 "r.platform_channels, r.the_store FROM `order`.manually_create_order_yc as o,reports.commodity_codes_zr as r " \
                 "WHERE o.product_sku like CONCAT('%',r.sku,'%')" \
                 "AND o.reference_no = '{}'".format (order_num)
        data = sql_inquire(eu_sql)

    return data

def order_retrieval(order_code):
    commodity_data = ''
    ser_sql = " SELECT  ord.*, co.product_name,co.product_code FROM order_record as ord ,commodity_codes_zr as co " \
              "  WHERE order_id ='%s' AND ord.sku = co.sku "%(order_code)
    data = conf_fun.connect_mysql(ser_sql, type='dict')
    if data:
        product_code = data[0].get('product_code')
        sql  = "SELECT * FROM products_components WHERE product_code = '{0}'".format(product_code)
        print('\n', sql)
        commodity_data = conf_fun.connect_mysql(sql, type='dict')
        print(commodity_data)
    return data,commodity_data


'''订单的数据查询'''
def order_search(request):
    ret = {'code': 200, 'msg': 'ok'}
    order_num = request.GET.get('order_num')
    # data = order_search_all(order_num)
    data,commodity_data = order_retrieval(order_num)
    ret['data'] = data
    ret['commodity_data'] = commodity_data

    ret['country_dict'] = settings.country_le_dict
    print('\n\n\n',ret['country_dict'])
    return JsonResponse(ret)


''' 零件查询'''
def part_sql(product_code ):
    sql = "SELECT * FROM products_components WHERE product_code ='%s'"%(product_code)

    data = conf_fun.connect_mysql(sql, type='dict')
    return data


'''模板查询'''
def template_sql(match_language , keyword):

    str1 = ''

    for word in keyword:
        str1 += " problem_type LIKE '%{0}%' or ".format(word)
    str1 = str1.rstrip(' or ')
    if match_language =='en':
        sql = "select DISTINCT email_content, problem_type,email_translation, country from email_reply_template " \
              "WHERE match_language  = '{0}' and country ='美国'" \
              "AND  ({1})" \
            .format(match_language, str1)
    else:
        sql = "select DISTINCT email_content, problem_type,email_translation, country from email_reply_template " \
              "WHERE match_language  = '{0}'" \
              "AND  ({1})" \
            .format( match_language , str1)

    print(sql)
    re_data = conf_fun.connect_mysql(sql, type='dict')

    return re_data


''' 翻译+模板选择'''


@csrf_exempt
def translate_semantic_analysis(request):
    keyword = ['破损', '缺件' ,'提供订单号码',]

    ret = {'code': 200, 'msg': 'ok'}
    po_data = request.POST
    content = request.POST.get('content')

    re_data ,match_language = conf_fun.translate_func(content)

    semantic_analysis_data = conf_fun.keyword_func(re_data) # 关键字提取
    for i in semantic_analysis_data:
        try:
            for key,value in settings.keyword_dict.items():
                if i.get("item") in value and key not in keyword:
                    keyword.append(key)
        except:
            pass

    print('这是关键字',keyword)
    te_data = template_sql(match_language , keyword)
    ret['tem_data'] = te_data

    product_code = po_data.get('product_code')
    ret['part_data'] = part_sql(product_code)
    ret['data'] = re_data


    return JsonResponse(ret)


# 回复客户邮件提交
def customer_reply_email(request):
    ret = {'code': 200, 'msg': 'ok'}
    data = request.POST
    print(data)
    return JsonResponse(ret)

'''新增回复工厂信息'''
def add_factory_feedback(data):
    try:
        order_number = data.get('order_number')  # 订单号
        problem_type = data.get('problem_type') # 问题类型
        lack_part = data.get('lack_part') #   缺件
        damaged = data.get('damaged')   # 损坏
        problem_content = "%s,%s"%(lack_part, damaged)  # 问题类型 缺件+损坏
        attachment_address = data.get('attachment_address')  # 附件地址
        now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 上传时间

        order_data = order_retrieval(order_number)[0] # 产品订单号数据
        country = settings.country_dict.get(order_data.get('country_code'))[0] # 国家
        product_code = order_data.get('product_code')   # 产品号
        sku = order_data.get('sku')

        fact_data = part_sql(product_code)[0]  # 零件数据
        container_code = fact_data.get('container_code')
        supplier = fact_data.get('supplier')
        sql = " INSERT INTO factory_feedback_1  (" \
              "order_number , sku, country,  container_num, factory," \
              "problem_type,problem_content, attachment_address,upload_time )" \
              " VALUES ('{0}', '{1}', '{2}' ,'{3}' ,'{4}', '{5}' ,'{6}', '{7}','{8}')"\
            .format( order_number, sku , country , container_code , supplier,
                     problem_type , problem_content , attachment_address ,now_time)
        print(sql)
        res = conf_fun.connect_mysql(sql, type='dict')
    except:pass

# 新增客户回复数据
def add_customer_data(data):
    key_list =[]
    value_list = []
    for key,value in data.items():
        if key != 'id':
            key_list.append(key)
            value_list.append(r'"{}"'.format(value))
    now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    key_list.append('upload_time')
    value_list.append("'%s'"%now_time)
    key_str = ','.join(key_list) # 新增的字段
    value_str = ','.join(value_list)
    sql = "INSERT INTO reply_customers  ( %s ) VALUES (%s)"%(key_str, value_str)
    print(sql)
    try:
        conf_fun.connect_mysql(sql, type='dict')
    except:
        ret ={'code':501,'msg':'该订单号对于的客户已被处理，无需重复提交'}
        return JsonResponse(ret)



'''修改 客户问题邮件状态  回复状态'''
def update_email_handing(data):
    id = data.get('id')

    platform = data.get('platform')
    country =  data.get('country')
    site = data.get('site')
    dispose_person = data.get('upload_people')
    problem_type = data.get('problem_type')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    order_number = data.get('order_number')
    type = data.get('type')
    if type:
        sql =" INSERT IGNORE INTO email_handling  (reply_situation, platform ,country ," \
             "site, dispose_person  , processing_time , order_number , problem_type ) values " \
             "( '{0}' ,'{1}', '{2}', '{3}', '{4}', '{5}', '{6}','{7}' )" \
             .format('已回复',platform, country ,site ,dispose_person, now_time, order_number,  problem_type )
    else:
        sql ="UPDATE email_handling SET reply_situation = '已回复' ,platform = '{0}' ,country = '{1}'," \
             "site = '{2}' , dispose_person ='{3}' , processing_time = '{4}' , order_number = '{5}' , problem_type = '{6}' " \
             "WHERE id = {7}".format(platform, country ,site ,dispose_person, now_time, order_number,  problem_type ,int(id) ,)
    print(sql)
    conf_fun.connect_mysql(sql)

def send_email(data):
    to_list = '' #收件人邮箱
    th1 ='' #邮件内容
    subject ='' #邮件主题
    end_email ='' # 发件人邮箱
    email_class.Mailer(to_list, th1, subject, '', type)
    return None
# 回复客户邮件提交
@csrf_exempt
def customer_reply_email(request):
    ret = {'code': 200, 'msg': 'ok'}
    data = request.POST
    add_customer_data(data)
    add_factory_feedback(data)
    update_email_handing(data)
    return JsonResponse(ret)


''' 在平台，国家，语言的条件下进行搜索'''
def search_template(data):
    sql = " SELECT * FROM email_reply_template "
    count_sql = 'SELECT COUNT(id) as count FROM email_reply_template'

    page = int(data.get('page')) - 1
    LIMIT = " LIMIT %s,20"%(page*20)
    print('data', data ,'\n')
    if data and 'page' in data and len(data.keys()) >1 \
        and data.get('country') and data.get('platform') and data.get('language'):
        sql += ' WHERE '
        count_sql += ' WHERE '
        search_list = []
        for key,value in data.items():
            if key !='page':
                search_list.append("%s = '%s'" % (key, value))
        search_str = ' AND '.join(search_list)
        sql +=  search_str
        sql += LIMIT
        count_sql += search_str
        count = conf_fun.sql_data(count_sql)
        re_data = conf_fun.sql_data(sql)
    else:
        sql += LIMIT
        count = conf_fun.sql_data(count_sql)
        re_data = conf_fun.sql_data(sql)
    return re_data,count

''' 工厂 国家 '''
def factory_feedback_sql(data):
    page = data.get('page')
    sql = "SELECT fa.*,co.commodity_name FROM factory_feedback_1 as fa,commodity_information as co WHERE fa.sku = co.sku "
    sql_1 = "select DISTINCT country from factory_feedback_1 "
    factory_sql = "select DISTINCT factory from factory_feedback_1 "
    sql_2 = 'SELECT COUNT(id) as count FROM factory_feedback_1 as fa where id>0'
    print(data)
    ser_str = ''
    if data and  len(data.keys()) >1 :
        search_list = []
        for key,value in data.items():

            print(key,value)
            if key in ['country','factory'] and value:
                ser_str += " AND fa.%s = '%s'"%(key, value)
            elif key =='begin_time' and value:
                ser_str += " AND '%s' <= upload_time "%(value)
            elif key == 'over_time' and value:
                ser_str += "  AND '%s'  >= upload_time" %(value)

        sql += ser_str
        sql_2 += ser_str
    sql += " LIMIT %s,50"%((int(page)-1)*50)
    print(sql,'\n',sql_2,'\n',sql_1,'\n',factory_sql)
    data_all = conf_fun.connect_mysql(sql, type='dict')
    country_data = conf_fun.connect_mysql(sql_1, type='dict')
    factory_data = conf_fun.connect_mysql(factory_sql, type='dict')
    count = conf_fun.sql_data(sql_2)
    return data_all,country_data,count,factory_data

@csrf_exempt
def  factory_feedback(request):
    data = request.GET
    ret = {'code' : 200, 'msg': '无'}
    data,country_data ,count,factory_data = factory_feedback_sql(data)
    ret['country_data'] = country_data
    ret['count'] = count
    ret['data'] = data
    ret['factory_data'] =factory_data
    return  JsonResponse(ret)


def message_translate(request):
    content = request.GET.get('content')
    re_content = conf_fun.translate_func(content)
    ret ={}
    ret['re_content'] =re_content
    return JsonResponse(ret)


