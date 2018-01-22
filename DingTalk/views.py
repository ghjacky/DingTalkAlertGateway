# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse

# Create your views here.


class AlertGateway(View):
    def post(self, request):
        print(request.POST.get('version', "empty"))
        print(request.POST.get('alerts', "empty"))
        return HttpResponse(request)