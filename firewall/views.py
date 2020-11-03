from django.shortcuts import render,HttpResponse
import requests
import json

'''
Success structure
{"status":"success","result":"1","queryIP":"66.228.119.72","queryFlags":"m","queryFormat":"json","contact":"AValidEmailAddress"}
'''

'''
Failure structure
{"status":"error","result":"-2","message":"Invalid IP address","queryIP":"10.10.10.10,8.8.8.8","queryFlags":null,"queryFormat":"json","contact":"AValidEmailAddress"}
'''

def get_score(ip_addr):
    url = "http://check.getipintel.net/check.php?ip="+ip_addr+"&format=json&flag=f&contact=bhaskar.rahul25@gmail.com"
    payload = {}
    headers = {
    'Cookie': '__cfduid=dccae4c03485c13d70073a98ccaf35b251602771240'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    result = json.loads(response.text)
    # result = json.loads('{"status":"success","result":"0.1","queryIP":"66.228.119.72","queryFlags":"m","queryFormat":"json","contact":"AValidEmailAddress"}')
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
        if result['status'] == 'success':
            if float(result['result']) >= 0.8:
                return render(request,"badIP.html",context=result)
            elif float(result['result']) <= 0.1:
                return render(request,"index.html",context=result)
            else:
                return render(request,"notSure.html",context=result)
        else:
            return render(request,"error.html",context=result)