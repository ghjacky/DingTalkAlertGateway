# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render

# Create your views here.


class AlertGateway(View):
    def post(self, request):
        print(request.POST['version'])
        print(request.POST['alerts'])