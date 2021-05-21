import requests, json, re


def store_country_code(store, country, language, type=''):
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
    return store, country


# 用检测信息确认表来生成条码 2020-1-20 肖飞
#
# 条码文件   直接用

import os


def upload_file(files, file_path):
    path2 = os.path.join(r'static/operation/operating_data/', file_path, str(files))
    if not os.path.exists(os.path.join(r'static/operation/operating_data/', file_path)):
        os.makedirs(os.path.join(r'static/operation/operating_data/', file_path))
    path = os.path.join(os.getcwd(), path2)
    print('只是路径\n', path)
    with open(path, 'wb') as f:
        for line in files:
            f.write(line)
    return path2


def create_post_generation(data_1):
    file_name = str(data_1.get('file_name'))

    file_name_str = file_name.split('-')[1]
    container_num = data_1.get('container_num')
    site = data_1.get('site')
    country = data_1.get('country')
    #    code = re.findall("\d+",file_name_str)[0]
    print('\n213123', file_name_str)
    send_file_name = "{0}-{1}{2}-{3}".format(container_num, site, country, file_name_str)
    store_low, country_low = store_country_code(site, country, 'en', 'low')

    area = "%s_%s" % (store_low, country_low)
    url = 'http://www.beyoung.group/tm_file_create/'
    # url = 'http://106.53.250.215:9126/tm_file_create/'
    data = {'filename': send_file_name, 'area': area}
    print(data_1.get('file_name'), data)

    res = requests.post(url, data, files={'files': data_1.get('file_name')})
    # print('\n\n1111111111111111',res.content)
    print(res)

    re_data = json.loads(res.content)
    print('\n这是返回的数据', re_data)
    error_msg = re_data.get('msg')
    fab_tm = re_data.get('fba_tm')
    cp_tm = re_data.get('cp_tm')
    print(fab_tm, '111', cp_tm)
    # "fba_tm": zip_name, 'cp_tm': zip_name_cp
    return fab_tm, cp_tm, error_msg
