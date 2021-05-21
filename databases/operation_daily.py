import os
import re
import time
from itertools import groupby
from operator import itemgetter
import requests,json
import pandas as pd
import pymysql
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

from stock_management import scheduling_settings
from stock_management.scheduling_management import post_generation
from stock_management.scheduling_management import scheduling_func

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from settings import conf_fun

class operation_excel(ViewSetMixin,APIView):

    def __init__(self):
        self.ret = {'code':200}

    def list(self,request):
        area = request.GET.get("area", None)
        name = request.GET.get("name", None)
        # page = request.GET.get("page", 1)
        dates = request.GET.get("dates", None)
        print(request.GET.get("area"))
        print('513\n', area, '--', name, '-', dates)
        if dates is None:
            dates = "None"
        type = "all"
        try:
            # 106.53.250.215:8003    www.beyoung.group
            url = 'http://www.beyoung.group/get_sku_order_summary?' + area + '?' + name + '?' + type + '?' + dates
            re = requests.get(url=url)
            data_res = json.loads(re.text)
            res = data_res
            # 分页显示
            return Response(res)
        except Exception as e:
            return Response({"code": 500, "msg": "error:" + str(e)})


