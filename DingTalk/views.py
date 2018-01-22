# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
import json
# Create your views here.


class AlertGateway(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(type(data))
        print(data)
        return HttpResponse(request)

    def get(self, request):
        print(request)
        print(request.GET)
        print(request.GET.get('version', "empty"))
        print(request.GET.get('alerts', "empty"))
        return HttpResponse(request)