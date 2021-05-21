from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from django.http import FileResponse
import pymysql, os, time
import datetime
from django import forms
from operator import itemgetter
from itertools import groupby
from settings import conf_fun

currency_dict = {'USD': 6.46,
                 'CAD': 5.06,
                 'GBP': 8.87,
                 'EUR': 7.78,
                 'MXN': 0.32,
                 'JPY': 0.061,
                 'AUD': 4.96}


class Withdrawal(ViewSetMixin, APIView):

    def __init__(self):
        self.ret = {'code': 200, 'msg': '无'}

    def list(self, request):
        dow_sql = "SELECT site,country,platform,currency FROM store_information "
        re_data = conf_fun.connect_mysql_operation(dow_sql, type='dict')
        re_dict = {}
        for platform, items in groupby(re_data, key=itemgetter('platform')):
            if platform not in re_dict:
                re_dict[platform] = {}
            for site, items_1 in groupby(items, key=itemgetter('site')):
                if not re_dict[platform].get(site):
                    re_dict[platform][site] = []
                for i in items_1:
                    re_dict[platform][site].append(
                        {'country': i.get('country'), 'currency': i.get('currency')})

        self.ret['re_data'] = re_dict
        return Response(self.ret)

    def create(self, request):
#        date = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        date = (datetime.datetime.now() + datetime.timedelta(minutes=8)).strftime("%Y-%m-%d %H:%M")
        data = request.data
        key_str = ""
        value_str = ""
        currency = data.get('currency')
        if currency:
            amount = data.get('amount')
            x = currency_dict.get(currency)
            if x:
                payment_rmb = float(amount) * float(x)
                key_str += "payment_rmb ,"
                value_str += "'{0}' ,".format(payment_rmb)
        for k, v in data.items():
            if k in ['site', 'country', 'payment_account'] and v:
                key_str += "{0} ,".format(k)
                value_str += "'{0}' ,".format(v.strip())
            elif k == 'platform' and v:
                key_str += "{0} , source ,".format(k)
                value_str += " '{0}' , '{0}' ,".format(v)
            elif k == 'currency' and v:
                key_str += "withdrawal_currency , payment_currency ,"
                value_str += "'{0}' , '{0}' ,".format(v)
            elif k == 'amount' and v:
                key_str += "withdrawal_amount ,payment_amount ,"
                value_str += "'{0}' , '{0}' ,".format(v)
        key_str += " date,path,handling_fee,type"
        value_str += "'{0}','P卡','0','2C'".format(date)
        insert_sql = " INSERT INTO public_account ( {0}) values  ({1})".format(key_str, value_str)
        print(insert_sql)
        conf_fun.connect_mysql_financial(insert_sql)
        return Response(self.ret)
