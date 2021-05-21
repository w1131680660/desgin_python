import pymysql
import  pandas as pd
import os

from settings import conf_fun
from django.http import JsonResponse


import chardet
def com_script(save_path):
    f = open(save_path, 'rb')
    r = f.read()
    f_charInfo = chardet.detect(r)
    pd_data = pd.read_excel(save_path, header=0, keep_default_na=False)
    
    for k,v in pd_data.iterrows():

        country = v.get('国家')
        site = v.get('站点')
        product_code = v.get('产品编码')
        spu = v.get('spu')
        sku = v.get('sku')
        category = v.get('类别')
        commodity_name = v.get('品名')
        Asin = v.get('Asin')
        product_link = v.get('产品链接')
        judge_sql = " select * from  commodity_information  where country='{0}' " \
                    " and site = '{1}' and sku ='{2}'  ".format(country, site, sku)
        print(252, '\n', judge_sql)
        re_data = conf_fun.connect_mysql_operation(judge_sql)
        if not re_data:
            insert_sql = ''' INSERT INTO commodity_information 
            (country,site,product_code,spu,sku,category,commodity_name,Asin,product_link ,platform, commodity_state) 
            VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','Amazon','在售' )  '''\
                .format(country, site, product_code, spu, sku, category, commodity_name, Asin, product_link)
            print(insert_sql)
            conf_fun.connect_mysql_operation(insert_sql)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def create_com_func(request):
    data = request.POST
    site = data.get('site')
    file = request.FILES.get('files')
    print(request.FILES)
    path = os.path.join(os.getcwd(), 'static/data/commodity_data')
    if not os.path.exists(path):
        os.mkdir(path)
    save_path = os.path.join(path, str(file))
    with open(save_path, 'wb', ) as f:
        for line in file:
            f.write(line)
    com_script(save_path)
    ret = {'code':200}
    return JsonResponse(ret)
