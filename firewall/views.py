from django.shortcuts import render,HttpResponse
import requests
import json
from django.http import JsonResponse
import time


# for packet capture
from scapy.all import *
from scapy.utils import wireshark

from .capture import CaptureThread
from siteList.models import SiteList
'''
Success structure
{"status":"success","result":"1","queryIP":"66.228.119.72","queryFlags":"m","queryFormat":"json","contact":"AValidEmailAddress"}
'''

'''
Failure structure
{"status":"error","result":"-2","message":"Invalid IP address","queryIP":"10.10.10.10,8.8.8.8","queryFlags":null,"queryFormat":"json","contact":"AValidEmailAddress"}
'''

def get_score(ip_addr):
    # url = "http://check.getipintel.net/check.php?ip="+ip_addr+"&format=json&flag=f&contact=bhaskar.rahul25@gmail.com"
    # payload = {}
    # headers = {
    # 'Cookie': '__cfduid=dccae4c03485c13d70073a98ccaf35b251602771240'
    # }
    # response = requests.request("GET", url, headers=headers, data = payload)
    # print(response.text.encode('utf8'))
    # result = json.loads(response.text)
    result = json.loads('{"status":"success","result":"0.5","queryIP":"66.228.119.72","queryFlags":"m","queryFormat":"json","contact":"AValidEmailAddress"}')
    # result = json.loads('{"status":"error","result":"-2","message":"Invalid IP address","queryIP":"10.10.10.10,8.8.8.8","queryFlags":null,"queryFormat":"json","contact":"AValidEmailAddress"}')
    return result

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    if request.method == 'GET':
        ipAddr = get_client_ip(request)
        result = get_score(ipAddr)
        querySet = SiteList.objects.filter(ip_addr=ipAddr)
        if(querySet.exists()):
            if(querySet.valid == True):
                return render(request,"welcome.html",context=result)
        if result['status'] == 'success':
            if float(result['result']) <= 0.1:
                return render(request,"welcome.html",context=result)
            elif float(result['result']) >= 0.8:
                return render(request,"badIP.html",context=result)
            else:
                startCapture(ipAddr)
                return render(request,"index.html",context=result)
        else:
            return render(request,"error.html",context=result)

def dummyRequest(request):
    if request.method == 'GET':
        ipAddr = get_client_ip(request)
        querySet = SiteList.objects.filter(ip_addr=ipAddr)
        siteList = querySet.exists()
        if(siteList):
            data = {
                'para': "Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis, architecto nesciunt blanditiis error animi soluta reiciendis debitis vel et sequi quibusdam tenetur optio excepturi illum quasi eum libero. Eum, laboriosam.",
                'result': siteList.valid
            }
        else:
            data = {
                'para': "Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis, architecto nesciunt blanditiis error animi soluta reiciendis debitis vel et sequi quibusdam tenetur optio excepturi illum quasi eum libero. Eum, laboriosam."
            }
        return JsonResponse(data)

# def get_res(request):
#     if request.method == 'GET':
#         time.sleep(2)
#         # result = stopCapture()
#         result = 1
#         data = {
#             'result':result
#         }
#         return JsonResponse(data)

def startCapture(ip):
    # TODO: start the capture
    # _filter = ip
    # capture = AsyncSniffer(iface={"lo":"localhost"},filter="ip host 127.0.0.1 and port 8000")
    # capture.start()
    # time.sleep(5)
    captureThread = CaptureThread(ip)