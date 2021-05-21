from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from settings import conf_fun
def store_country_code(store,country,language,type=''):
    if language == "en":
        if type == "low":
            if store == "胤佑":
                store = "yy"
            elif store == "爱瑙":
                store = "an"
            elif store == "中睿":
                store = "zr"
            elif store == "京汇":
                store = "jh"
            if country == "美国":
                country = "us"
            elif country == "英国":
                country = "uk"
            elif country == "加拿大":
                country = "ca"
            elif country == "日本":
                country = "jp"
            elif country == "欧洲":
                country = "eu"
            elif country == "澳洲":
                country = "au"
            elif country == "法国":
                country = "fr"
            elif country == "德国":
                country = "de"
            elif country == "意大利":
                country = "it"
            elif country == "西班牙":
                country = "es"
            elif country == "墨西哥":
                country = "mx"
            elif country == "西班牙":
                country = "ie"
            elif country == "葡萄牙":
                country = "pt"
            elif country == "瑞典":
                country = "se"
        else:
            if store == "胤佑":
                store = "YY"
            elif store == "爱瑙":
                store = "AN"
            elif store == "中睿":
                store = "ZR"
            elif store == "京汇":
                store = "JH"
            if country == "美国":
                country = "US"
            elif country == "英国":
                country = "UK"
            elif country == "加拿大":
                country = "CA"
            elif country == "日本":
                country = "JP"
            elif country == "欧洲":
                country = "EU"
            elif country == "澳洲":
                country = "AU"
            elif country == "法国":
                country = "FR"
            elif country == "德国":
                country = "DE"
            elif country == "意大利":
                country = "IT"
            elif country == "西班牙":
                country = "ES"
            elif country == "墨西哥":
                country = "MX"
            elif country == "西班牙":
                country = "IE"
            elif country == "葡萄牙":
                country = "PT"
            elif country == "瑞典":
                country = "SE"
    else:
        if store == "yy" or store == "YY":
            store = "胤佑"
        elif store == "an" or store == "AN":
            store = "爱瑙"
        elif store == "zr" or store == "ZR":
            store = "中睿"
        elif store == "jh" or store == "JH":
            store = "京汇"
        if country == "us" or country == "US":
            country = "美国"
        elif country == "uk" or country == "UK" or country == "GB":
            country = "英国"
        elif country == "ca" or country == "CA":
            country = "加拿大"
        elif country == "jp" or country == "JP":
            country = "日本"
        elif country == "eu" or country == "EU":
            country = "欧洲"
        elif country == "au" or country == "AU":
            country = "澳洲"
        elif country == "fr" or country == "FR":
            country = "法国"
        elif country == "de" or country == "DE":
            country = "德国"
        elif country == "it" or country == "IT":
            country = "意大利"
        elif country == "es" or country == "ES":
            country = "西班牙"
        elif country == "mx" or country == "MX":
            country = "墨西哥"
        elif country == "ie" or country == "IE":
            country = "西班牙"
        elif country == "pt" or country == "PT":
            country = "葡萄牙"
        elif country == "se" or country == "SE":
            country = "瑞典"
    return store,country


@csrf_exempt
def upload_rank(request):
    ret = {}
    if request.method == 'POST':
        print(22222222)
        data = request.POST
        print(data,type(data))
        country = data.get('country')
        site = data.get('site')
        SPU = data.get('spu')

        ranking = data.get('ranking')
        comment_amount = data.get('comment_amount')
        star_level = data.get('star_level')
        small_rank =  data.get('small_rank')
        date = data.get('date')
        date_change = '.'.join(date.split('-'))
        area,country_low = store_country_code(site,country,'en','low')
        sql =  " SELECT * FROM commodity_information where  spu ='{0}' and country='{1}' and site='{2}'".format(SPU,country,site)
        print(sql,'\n')
        re_data = conf_fun.connect_mysql_operation(sql ,type='dict')
        if re_data:
            for data_dict in re_data:
                sku = data_dict.get('sku')
                judge_sql =  " SELECT * FROM front_display where country ='{0}' and area ='{1}' and  SPU ='{2}' and " \
                             " SKU ='{3}'and dates ='{4}' ".format(country,area,SPU,sku, date_change)
                print(judge_sql,'\n')
                re_judge_data = conf_fun.connect_mysql_operation(judge_sql,type='dict')

                if re_judge_data:
                    update_str = ''
                    for key,value in data.items():
                        if key in ['comment_amount','star_level','small_rank','ranking' ] and value:
                            update_str += " {0} ='{1}' ,".format(key,value)
                    update_str = update_str.rstrip(' ,')
                    update_sql = " UPDATE front_display SET {5} where country ='{0}' and area ='{1}' and  SPU ='{2}' and " \
                             " SKU ='{3}'and dates ='{4}'".format(country, area, SPU, sku ,date_change, update_str)
                    print(update_sql,'\n')
                    conf_fun.connect_mysql_operation(update_sql)
                else:
                    inster_sql = " INSERT INTO front_display (ranking, country , area, " \
                                 "SPU ,SKU,dates,comment_amount,star_level,small_rank ) VALUES " \
                                 " ('{0}' ,'{1}' ,'{2}' ,'{3}', '{4}' ,'{5}' ,'{6}','{7}', '{8}')"\
                        .format(ranking, country, area,SPU,sku, date_change ,comment_amount, star_level,small_rank)
                    print(inster_sql)
                    conf_fun.connect_mysql_operation(inster_sql)
                ret['code'] = 200
                ret['msg'] = '新增排名成功'
    else:
        ret['code'] =500
        ret['msg'] ='请求方法错误'
    return JsonResponse(ret)
