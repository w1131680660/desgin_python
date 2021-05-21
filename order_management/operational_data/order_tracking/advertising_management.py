from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from customer_management.settings import conf_fun
import uuid
from operator import itemgetter
from itertools import groupby
from customer_management.settings import sql
from settings import conf_fun









class Advertising_management(ViewSetMixin,APIView):
    def __init__(self):
        self.ret = {'code':200,'msg':200}

    def list(self,request):

        return Response(self.ret)