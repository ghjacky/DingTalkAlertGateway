# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
import json
import requests
import datetime
# Create your views here.


class AlertGateway(View):
    def post(self, request):
        type = dict()
        title = ""      #告警标题
        status = ""     #告警状态（未解决或解决）
        severity = ""   #告警级别
        content = ""    #内容
        link = ""       #链接
        type.update({
            'firing': '故障',
            'resolved': '恢复',
        })

        data = json.loads(request.body.decode('utf-8'))     #获取alertmanager的POST数据
        message = dict()    #告警信息
        DingPayload = dict()
        headers = {"Content-Type": "application/json; charset=utf-8"}
        WebHook = "https://oapi.dingtalk.com/robot/send?access_token=86a49cbe1761ca0d9267892412384242a26938ee3cb1cd0ebc548abf791935a6"
        print("[v1/api/DingTalk:] {0}".format(data))

        for event in data['alerts']:
            if "sba" != data.get("source", ""):
                message.update({
                    "generatorURL": event["generatorURL"],
                    "severity": event["labels"]["severity"],
                })

            print(message)
            message.update({
                "alertName": event["labels"]["alertname"],
                "instance": event["labels"]["instance"],
                "node": event["labels"]["node"],
                "job": event["labels"]["job"],
                "service": event["labels"]["service"],
                "env": event["labels"]["env"],
                "status": event["status"],
                "startsAt": event["startsAt"],
                "summary": event["annotations"]["summary"],
                "description": event["annotations"]["description"],

            })
            title = message.get("alertName", "告警")
            status = type[message.get("status", "firing")]
            content = message.get("description", "Unkown！")
            instance = message.get("instance", "Unkown")
            service = message.get("service", "Unkown")
            env = message.get("env", "Unkown")
            severity = message.get("severity", "critical")
            link = message.get("generatorURL", "https://www.baidu.com/s?wd=%E4%BA%94%E7%99%BE%E5%B9%B4%E5%89%8D%E7%9B%98%E4%B8%9D%E6%B4%9E")
            startsAt = message.get("startsAt", "五百年前盘丝大仙")
            DingPayload.update({
                "msgtype": "markdown",
                "markdown": {
                   "title": title,
                   "text":  "###### 类型：" + status + "\n" +
                            "###### 环境：" + env + "\n" +
                            "###### 级别：" + severity + "\n" +
                            "###### 服务：" + service + "\n" +
                            "###### 实例：" + instance + "\n" +
                            "###### 内容：" + content + "\n" +
                            "###### 时间：" + startsAt + "\n"
                            "###### 链接：" + "[查看详情](" + link + ")",
                }
            })
            try:
                requests.post(WebHook, data=json.dumps(DingPayload), headers=headers)
            except Exception as e:
                print("[v1/api/DingTalk:] 钉钉消息发送失败！")
        return HttpResponse(request)
