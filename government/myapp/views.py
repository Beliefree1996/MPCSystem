from django.shortcuts import render
from django.http import JsonResponse
from .models import HLPPublicKey, HLP_otherPublicKey, PaillierPublicKey, SealBFVPublicKey, SealCKKSPublicKey, \
    En_Algorithm, Linear_Function, Multiple_Function, Cateory, Content, GetNum, Wage, \
    UserIC
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.utils.six import BytesIO
import requests
import json
import time
import os
import psutil
# import face_recognition
import hashlib
from PIL import Image, ImageDraw
import base64
from . import paillier
from . import CC_getongtaiN as HLP
from . import NCC_getongtai2N as HLP_other


# Create your views here.

def renew_publicKey(request):
    # Key - Global variables
    enalth = En_Algorithm.objects.last()
    if enalth.normal == 1 or enalth.operation == 1:  # paillier
        n, g, r, lamda, u = paillier.paillier_generation()
        puk1 = PaillierPublicKey.objects.get(id=1)
        puk1.n = n
        puk1.r = r
        # puk1 = PaillierPublicKey(n=n, r=r)
        puk1.save()
        url = 'http://127.0.0.1:8000/apis/renew_Paillier_privateKey'
        data = {'g': g, 'lamda': lamda, 'n': n, 'u': u}
        requests.post(url, data=data)
    if enalth.normal == 2 or enalth.operation == 2:  # HLP
        N, l, Mhard, Msoft, random_numbers, mods, Deta, A, B, q, ns, sigema_max, l_0, sigma, r = HLP.key_generartion()  # 密钥生成
        # puk2 = HLPPublicKey(N=N, ns=ns, mods=mods, Mhard=Mhard, Msoft=Msoft, random_numbers=random_numbers)
        puk2 = HLPPublicKey.objects.get(id=1)
        puk2.N = N
        puk2.ns = ns
        puk2.mods = mods
        puk2.Mhard = Mhard
        puk2.Msoft = Msoft
        puk2.random_numbers = random_numbers
        puk2.save()
        url = 'http://127.0.0.1:8000/apis/renew_HLP_privateKey'
        data = {'Deta': str(Deta), 'A': str(A), 'B': str(B), 'N': N, 'mods': mods, 'q': q}
        requests.post(url, data=data)
    if enalth.normal == 3 or enalth.operation == 3:  # HLP_other
        N, l, Mhard, Msoft, random_numbers, mods, Deta, A, B, q, ns, sigema_max, l_0, sigma, r = HLP_other.key_generartion()  # 密钥生成
        # puk3 = HLP_otherPublicKey(N=N, ns=ns, mods=mods, Mhard=Mhard, Msoft=Msoft, random_numbers=random_numbers)
        puk3 = HLP_otherPublicKey.objects.get(id=1)
        puk3.N = N
        puk3.ns = ns
        puk3.mods = mods
        puk3.Mhard = Mhard
        puk3.Msoft = Msoft
        puk3.random_numbers = random_numbers
        puk3.save()
        url = 'http://127.0.0.1:8000/apis/renew_HLP_other_privateKey'
        data = {'Deta': str(Deta), 'A': str(A), 'B': str(B), 'N': N, 'mods': mods, 'q': q}
        requests.post(url, data=data)
    if enalth.normal == 4 or enalth.operation == 4:  # BFV
        url = 'http://39.102.39.63:9000/seal/BFV_kengen'
        data = requests.get(url)
        result = data.json()
        # puk4 = SealBFVPublicKey(public_key=result['public_key'], relin_keys=result['relin_keys'])
        puk4 = SealBFVPublicKey.objects.get(id=1)
        puk4.public_key = result['public_key']
        puk4.relin_keys = result['relin_keys']
        puk4.save()
        url1 = 'http://127.0.0.1:8000/apis/renew_BFV_privateKey'
        data1 = {'secret_key': result['secret_key']}
        requests.post(url1, data=data1)
        # print(requests.post(url1, data=data1).text)
    if enalth.normal == 5 or enalth.operation == 5:  # CKKS
        url = 'http://39.102.39.63:9000/seal/CKKS_kengen'
        data = requests.get(url)
        result = data.json()
        # puk5 = SealCKKSPublicKey(public_key=result['public_key'], relin_keys=result['relin_keys'])
        puk5 = SealCKKSPublicKey.objects.get(id=1)
        puk5.public_key = result['public_key']
        puk5.relin_keys = result['relin_keys']
        puk5.save()
        url1 = 'http://127.0.0.1:8000/apis/renew_CKKS_privateKey'
        data1 = {'secret_key': result['secret_key']}
        requests.post(url1, data=data1)
    return JsonResponse({
        "status_code": 0,
        "data": "renew success!"
    })


def changeStrategy(request):
    if request.method == "POST":  # 当提交表单时
        data = json.loads(request.body)
        cateory_normal = int(data.get('cateory_normal'))
        cateory_operation = int(data.get('cateory_operation'))
        flag = data.get('flag')
        if flag == 0:  # 下拉框选择
            functionId = int(data.get('functionId'))
            enlog = En_Algorithm.objects.get(id=1)
            enlog.normal = cateory_normal
            enlog.power = 1
            enlog.operation = cateory_operation
            enlog.functionId = functionId
            enlog.save()
        if flag == 1:  # 添加一次函数
            a1 = data.get('a1')
            a2 = data.get('a2')
            c = data.get('c')
            LDivisor = data.get('LDivisor')
            enlog = En_Algorithm.objects.get(id=1)
            enlog.normal = cateory_normal
            enlog.operation = cateory_operation
            enlog.power = 1
            obj = Linear_Function(a1=a1, a2=a2, c=c, LDivisor=LDivisor)
            obj.save()
            enlog.functionId = obj.id
            enlog.save()
        if flag == 2:  # 添加二次函数
            coefficientArray = data.get('coefficientArray')
            powerArray = data.get('powerArray')
            lastC = data.get('lastC')
            MDivisor = data.get('MDivisor')
            enlog = En_Algorithm.objects.get(id=1)
            enlog.normal = cateory_normal
            enlog.operation = cateory_operation
            enlog.power = 2
            obj = Multiple_Function(coefficientArray=coefficientArray, powerArray=powerArray, lastC=lastC,
                                    MDivisor=MDivisor)
            obj.save()
            enlog.functionId = obj.id
            enlog.save()
        return JsonResponse({
            "status_code": 0,
            "data": "renew success!"
        })


def temporary(request):
    if request.method == "POST":
        IC_num = request.POST.get("IC_num")
        # db_data = Wage.objects.all().aggregate(Max('date'))
        db_data = Wage.objects.filter(IC_num=IC_num).order_by("date").reverse()[:1]
        ss = db_data[0].ss
        pf = db_data[0].pf
        enalg = En_Algorithm.objects.last()
        if enalg.power == 1:
            if enalg.operation == 1:
                puk = PaillierPublicKey.objects.get(id=1)
                temp = paillier.paillier_encryption(ss * 100, int(puk.n) + 1, int(puk.r), int(puk.n))
                temp = paillier.paillier_encryption(pf * 100, int(puk.n) + 1, int(puk.r), int(puk.n))
            elif enalg.operation == 2 or enalg.operation == 3:
                puk = HLPPublicKey.objects.get(id=1)
                temp = HLP.lattice_encryption(HLP.long_to_two(ss * 100, puk.N), eval(str(puk.Mhard)),
                                              eval(str(puk.Msoft)), eval(str(puk.random_numbers)), puk.N, puk.ns,
                                              puk.mods)
                temp = HLP.lattice_encryption(HLP.long_to_two(pf * 100, puk.N), eval(str(puk.Mhard)),
                                              eval(str(puk.Msoft)), eval(str(puk.random_numbers)), puk.N, puk.ns,
                                              puk.mods)
            elif enalg.operation == 4 or enalg.operation == 5:
                puk = SealBFVPublicKey.objects.get(id=1)
                url = 'http://39.102.39.63:9000/seal/BFV_Encrypt'
                temp = json.loads(
                    requests.post(url, data={'x': int(ss * 100), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                temp = json.loads(
                    requests.post(url, data={'x': int(pf * 100), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
            functionT = Linear_Function.objects.get(id=enalg.functionId)
            data = int((functionT.a1 * ss + functionT.a2 * pf + functionT.c) / functionT.LDivisor)
        elif enalg.power == 2:
            data = 0
            functionT = Multiple_Function.objects.get(id=enalg.functionId)
            for i in range(len(functionT.coefficientArray)):
                data = data + functionT.coefficientArray[i] * pow(ss, functionT.powerArray[i][0]) * pow(pf,
                                                                                                        functionT.powerArray[
                                                                                                            i][1])
            data = int(data / functionT.MDivisor)
    return JsonResponse({
        "status_code": 0,
        "data": data
    })


def getQuota(request):
    if request.method == "GET":
        IC_num = request.GET.get("IC_num")
        db_data = Wage.objects.filter(IC_num=IC_num).order_by("date").reverse()[:1]
        ss = db_data[0].ss
        pf = db_data[0].pf
        enalg = En_Algorithm.objects.last()
        if enalg.power == 1:
            functionT = Linear_Function.objects.get(id=enalg.functionId)
            enter_url = "http://127.0.0.1:8010/enter/getQuota_linear"
            setdata = {'operation': enalg.operation,
                       'a1': functionT.a1, 'a2': functionT.a2, 'c': functionT.c,
                       'ss': int(ss), 'pf': int(pf)}
            # TODO 每一种情况数据得相应得加密
            if enalg.operation == 1:
                puk = PaillierPublicKey.objects.get(id=1)
                setdata['n'] = puk.n
                setdata['ss'] = paillier.paillier_encryption(setdata['ss'], int(puk.n) + 1, int(puk.r), int(puk.n))
                setdata['pf'] = paillier.paillier_encryption(setdata['pf'], int(puk.n) + 1, int(puk.r), int(puk.n))
                setdata['c'] = paillier.paillier_encryption(setdata['c'], int(puk.n) + 1, int(puk.r), int(puk.n))
            elif enalg.operation == 2 or enalg.operation == 3:
                puk = HLPPublicKey.objects.get(id=1)
                setdata['N'] = puk.N
                setdata['mods'] = puk.mods
                setdata['ss'] = str(HLP.lattice_encryption(HLP.long_to_two(setdata['ss'], puk.N), eval(puk.Mhard),
                                                       eval(puk.Msoft), eval(puk.random_numbers), puk.N, puk.ns,
                                                       puk.mods))
                setdata['pf'] = str(HLP.lattice_encryption(HLP.long_to_two(setdata['pf'], puk.N), eval(puk.Mhard),
                                                       eval(puk.Msoft), eval(puk.random_numbers), puk.N, puk.ns,
                                                       puk.mods))
                setdata['c'] = str(HLP.lattice_encryption(HLP.long_to_two(setdata['c'], puk.N), eval(puk.Mhard),
                                                      eval(puk.Msoft), eval(puk.random_numbers), puk.N, puk.ns,
                                                      puk.mods))
            # elif enalg.operation == 3:
            #     puk = HLP_otherPublicKey.objects.get(id=1)
            #     setdata['N'] = puk.N
            #     setdata['mods'] = puk.mods
            #     setdata['ss'] = str(HLP_other.lattice_encryption(HLP.long_to_two(setdata['ss'], puk.N), eval(puk.Mhard),
            #                                                  eval(puk.Msoft), eval(puk.random_numbers), puk.N, puk.ns,
            #                                                  puk.mods))
            #     setdata['pf'] = str(HLP_other.lattice_encryption(HLP.long_to_two(setdata['pf'], puk.N), eval(puk.Mhard),
            #                                                  eval(puk.Msoft), eval(puk.random_numbers), puk.N, puk.ns,
            #                                                  puk.mods))
            #     setdata['c'] = str(HLP_other.lattice_encryption(HLP.long_to_two(setdata['c'], puk.N), eval(puk.Mhard),
            #                                                  eval(puk.Msoft), eval(puk.random_numbers), puk.N, puk.ns,
            #                                                  puk.mods))
            elif enalg.operation == 4:
                url = 'http://39.102.39.63:9000/seal/BFV_Encrypt'
                puk = SealBFVPublicKey.objects.get(id=1)
                setdata['rel'] = puk.relin_keys
                setdata['pub'] = puk.public_key
                # print("+++++++++++++")
                # print(json.loads(requests.post(url, data={'x': int(setdata['ss']), 'public_key': puk.public_key}).text)['x_encrypted'])
                setdata['ss'] = json.loads(requests.post(url, data={'x': int(setdata['ss']), 'public_key': puk.public_key}).text)['x_encrypted']
                setdata['pf'] = json.loads(requests.post(url, data={'x': int(setdata['pf']), 'public_key': puk.public_key}).text)['x_encrypted']
                setdata['c'] = json.loads(requests.post(url, data={'x': int(setdata['c']), 'public_key': puk.public_key}).text)['x_encrypted']
            elif enalg.operation == 5:
                url = 'http://39.102.39.63:9000/seal/CKKS_Encrypt'
                puk = SealCKKSPublicKey.objects.get(id=1)
                setdata['rel'] = puk.relin_keys
                setdata['pub'] = puk.public_key
                setdata['ss'] = json.loads(requests.post(url, data={'x': int(setdata['ss']), 'public_key': puk.public_key}).text)['x_encrypted']
                setdata['pf'] = json.loads(requests.post(url, data={'x': int(setdata['pf']), 'public_key': puk.public_key}).text)['x_encrypted']
                setdata['c'] = json.loads(requests.post(url, data={'x': int(setdata['c']), 'public_key': puk.public_key}).text)['x_encrypted']
            # print("+++++++++++++")
            # print(requests.post(url, data=setdata).text)
            data = json.loads(requests.post(enter_url, data=setdata).text)['data']
        elif enalg.power == 2:
            functionT = Multiple_Function.objects.get(id=enalg.functionId)
            enter_url = "http://127.0.0.1:8010/enter/getQuota_multiple"
            setdata = {'operation': enalg.operation,
                       'coefficientArray': functionT.coefficientArray,
                       'powerArray': functionT.powerArray, 'lastC': functionT.lastC,
                       'ss': ss, 'pf': pf}
            if enalg.operation == 4:
                url = 'http://39.102.39.63:9000/seal/BFV_Encrypt'
                puk = SealBFVPublicKey.objects.get(id=1)
                setdata['rel'] = puk.relin_keys
                setdata['pub'] = puk.public_key
                setdata['ss'] = \
                json.loads(requests.post(url, data={'x': int(setdata['ss']), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                setdata['pf'] = \
                json.loads(requests.post(url, data={'x': int(setdata['pf']), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                setdata['lastC'] = \
                json.loads(requests.post(url, data={'x': int(setdata['lastC']), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                url = 'http://39.102.39.63:9000/seal/BFV_mul'
                setdata['x_mul'] = json.loads(requests.post(url, data={'lis': str([setdata['ss'], setdata['pf']]), 'relin_keys': puk.relin_keys}).text)[
                    'mul_encrypted']    # PyRunSeal与RMF参数不一样
            elif enalg.operation == 5:
                url = 'http://39.102.39.63:9000/seal/CKKS_Encrypt'
                puk = SealCKKSPublicKey.objects.get(id=1)
                setdata['rel'] = puk.relin_keys
                setdata['pub'] = puk.public_key
                setdata['ss'] = \
                json.loads(requests.post(url, data={'x': int(setdata['ss']), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                setdata['pf'] = \
                json.loads(requests.post(url, data={'x': int(setdata['pf']), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                setdata['lastC'] = \
                json.loads(requests.post(url, data={'x': int(setdata['lastC']), 'public_key': puk.public_key}).text)[
                    'x_encrypted']
                url = 'http://39.102.39.63:9000/seal/CKKS_mul'
                setdata['x_mul'] = json.loads(requests.post(url, data={'lis': str([setdata['ss'], setdata['pf']]),
                                                                       'relin_keys': puk.relin_keys}).text)[
                    'mul_encrypted']  # PyRunSeal与RMF参数不一样
            data = json.loads(requests.post(enter_url, data=setdata).text)['data'],
    return JsonResponse({
        "status_code": 0,
        'enalg': enalg.operation,
        'LDivisor': functionT.LDivisor,
        "data": data
    })


# /apis/get_info
def get_info(request):
    """
    用于提供数据
    :param request: HttpRequest
    :return: Json
    """

    if request.method == "GET":
        # 如果是要获取分类列表则加上这个参数  需要提供的内容为: 1ds2ppJu2I9dl1
        user_id = request.GET.get("user_id")
        IC_num = request.GET.get("IC_num")
        cateory_list = request.GET.get("cateory")
        user_list = request.GET.get("users")
        get_page_arr = request.GET.get("page")
        get_access_num = request.GET.get("num")
        get_blog_list = request.GET.get("blog_list")
        get_mp3 = request.GET.get("mp3")
        get_status = request.GET.get("status")
        get_wage = request.GET.get("wage")
        get_date = request.GET.get("date")
        get_user_detail = request.GET.get("user_detail")
        get_username = request.GET.get("username")

        # 页码
        if get_page_arr is not None:
            get_page = int(get_page_arr)
        else:
            get_page = 1
        pagesize = 5
        start = (get_page - 1) * pagesize
        end = get_page * pagesize

        # 获取分类列表
        if cateory_list is not None and cateory_list == "1ds2ppJu2I9dl1":
            return JsonResponse({
                "status_code": 0,
                "data": [i[0] for i in list(Cateory.objects.values_list("cateory_name"))]
            })

        if user_list is not None and user_list == "2ds2ppJu2I9dl1":
            return JsonResponse({
                "status_code": 0,
                "data": [i[0] for i in list(User.objects.values_list("username"))]
            })

        if get_access_num is not None and get_access_num == "true":
            db = GetNum.objects.get(date=time.strftime("%Y-%m-%d"))
            return JsonResponse({
                "status_code": 0,
                "num": int(db.number)
            })

        # 获取公告列表
        if get_blog_list is not None and get_blog_list == "true":
            db = Content.objects.all()
            data = [
                {
                    "title": i.title,
                    "content": i.content,
                    "cateory": i.cateory.cateory_name,
                    "user": i.user.username,
                    "time": i.time
                }
                for i in db[start:end]]

            return JsonResponse({
                "status_code": 0,
                "total": len(db),
                "data": data
            })

        # 查询工资
        if get_wage is not None and get_wage == "true" and IC_num is not None:
            # user_ic = UserIC.objects.get(user_id=user_id)
            if get_date is not None:
                db_data = Wage.objects.filter(IC_num=IC_num, date=get_date)
            else:
                db_data = Wage.objects.filter(IC_num=IC_num).order_by("date").reverse()[:6]
            enalg = En_Algorithm.objects.last()
            if enalg.normal == 1:
                puk = PaillierPublicKey.objects.last()
                data = [
                    {
                        "id": data_i.id,
                        "date": data_i.date,
                        "pf": paillier.paillier_encryption(data_i.pf * 100, int(puk.n) + 1, int(puk.r), int(puk.n)),
                        "ss": paillier.paillier_encryption(data_i.ss * 100, int(puk.n) + 1, int(puk.r), int(puk.n)),
                    }
                    for data_i in db_data]
            elif enalg.normal == 2:
                puk = HLPPublicKey.objects.last()
                data = [
                    {
                        "id": data_i.id,
                        "date": data_i.date,
                        "pf": HLP.lattice_encryption(HLP.long_to_two(data_i.pf * 100, puk.N), eval(str(puk.Mhard)),
                                                     eval(str(puk.Msoft)), eval(str(puk.random_numbers)), puk.N, puk.ns,
                                                     puk.mods),
                        "ss": HLP.lattice_encryption(HLP.long_to_two(data_i.ss * 100, puk.N), eval(str(puk.Mhard)),
                                                     eval(str(puk.Msoft)), eval(str(puk.random_numbers)), puk.N, puk.ns,
                                                     puk.mods),
                    }
                    for data_i in db_data]
            elif enalg.normal == 3:
                puk = HLP_otherPublicKey.objects.last()
                data = [
                    {
                        "id": data_i.id,
                        "date": data_i.date,
                        "pf": HLP_other.lattice_encryption(HLP_other.long_to_two(data_i.pf * 100, puk.N),
                                                           eval(str(puk.Mhard)),
                                                           eval(str(puk.Msoft)), eval(str(puk.random_numbers)), puk.N,
                                                           puk.ns,
                                                           puk.mods),
                        "ss": HLP_other.lattice_encryption(HLP_other.long_to_two(data_i.ss * 100, puk.N),
                                                           eval(str(puk.Mhard)),
                                                           eval(str(puk.Msoft)), eval(str(puk.random_numbers)), puk.N,
                                                           puk.ns,
                                                           puk.mods),
                    }
                    for data_i in db_data]
            elif enalg.normal == 4:
                puk = SealBFVPublicKey.objects.last()
                url = 'http://39.102.39.63:9000/seal/BFV_Encrypt'
                # data = {'x': str(int(db_data[1].pf * 100)), 'public_key': puk.public_key}
                # print(json.loads(requests.post(url, data=data).text)['x_encrypted'])
                # data['pf'] = json.loads(
                #     requests.post(url, data={'x': str(int(db_data[0].pf * 100)), 'public_key': puk.public_key}).text)[
                #     'x_encrypted']
                data = [
                    {
                        "id": data_i.id,
                        "date": data_i.date,
                        "pf": json.loads(
                            requests.post(url, data={'x': int(data_i.pf * 100), 'public_key': puk.public_key}).text)[
                            'x_encrypted'],
                        "ss": json.loads(
                            requests.post(url, data={'x': int(data_i.ss * 100), 'public_key': puk.public_key}).text)[
                            'x_encrypted'],
                    }
                    for data_i in db_data]
            elif enalg.normal == 5:
                puk = SealCKKSPublicKey.objects.last()
                url = 'http://39.102.39.63:9000/seal/CKKS_Encrypt'
                data = [
                    {
                        "id": data_i.id,
                        "date": data_i.date,
                        "pf": json.loads(
                            requests.post(url, data={'x': int(data_i.pf * 100), 'public_key': puk.public_key}).text)[
                            'x_encrypted'],
                        "ss": json.loads(
                            requests.post(url, data={'x': int(data_i.ss * 100), 'public_key': puk.public_key}).text)[
                            'x_encrypted'],
                    }
                    for data_i in db_data]
            return JsonResponse({
                "status_code": 0,
                "enalg": enalg.normal,
                "data": data
            })

        # 获取用户详细信息
        if get_user_detail is not None and get_user_detail == "true":
            if get_username is not None:
                db_data = User.objects.filter(is_superuser=0).filter(username__contains=get_username)
            else:
                db_data = User.objects.filter(is_superuser=0)
            data = [
                {
                    "id": i.id,
                    "username": i.username,
                    "is_staff": i.is_staff,
                    "is_active": i.is_active,
                    "email": i.email,
                    "date_joined": i.date_joined,
                    "last_login": i.last_login,
                    "IC_num": UserIC.objects.get(user_id=i.id).IC_num
                }
                for i in db_data[start:end]]
            return JsonResponse({
                "status_code": 0,
                "total": len(db_data),
                "data": data
            })

        if get_mp3 is not None:
            data = []
            for i in os.listdir("static/mp3"):
                data.append({"url": f"/apis/static/mp3/{i}",
                             "name": i})

            return JsonResponse({
                "status_code": 0,
                "data": data
            })

        def getMemorystate():
            phymem = psutil.virtual_memory()
            line = "Memory: %5s%% %6s/%s" % (
                phymem.percent,
                str(int(phymem.used / 1024 / 1024)) + "M",
                str(int(phymem.total / 1024 / 1024)) + "M"
            )
            return line

        if get_status is not None:
            data = {}
            data["status_code"] = 0
            # data["cpu_status"] = int(math.fsum(psutil.cpu_percent(interval=1, percpu=True)) // 4)  # 获得cpu当前使用率
            data["cpu_status"] = max(psutil.cpu_percent(interval=1, percpu=True))  # 获得cpu当前使用率
            data["memory_status"] = int(psutil.virtual_memory().percent)  # 获取当前内存使用情况
            data["disk_status"] = int(psutil.disk_usage("/").percent)

            return JsonResponse(data)

        # =====================================================================================
        return JsonResponse({
            "status_code": 1,
            "error": "not data"
        })


#
def change_data(request):
    if request.method == "GET":
        change_active = request.GET.get("change_active")
        user_id = request.GET.get("user_id")
        certification = request.GET.get("certification")
        IC_num = request.GET.get("IC_num")
        # 更改锁定状态
        if change_active is not None and change_active == "true" and user_id is not None:
            db_data = User.objects.get(id=user_id)
            if db_data.is_active == 1:
                db_data.is_active = 0
            else:
                db_data.is_active = 1
            db_data.save()
            return JsonResponse({
                "status_code": 0,
            })

        # 认证，身份证绑定
        if certification is not None and certification == "true" and user_id is not None and IC_num is not None:
            db_data = UserIC.objects.get(user_id=user_id)
            db_data.IC_num = IC_num
            db_data.save()
            return JsonResponse({
                "status_code": 0,
            })


# /apis/add
def add_data(request):
    if request.method == "POST":
        add_blog = request.GET.get("add_data")
        add_access = request.GET.get("access")
        # 添加blog
        if add_blog is not None and add_blog == "1bs2ppJu2I9dl1":
            # 将json转换为python dict格式
            data = json.loads(request.body)
            if data.get("title") is not None and data.get("content") is not None and data.get(
                    "cateory") is not None and data.get("author") is not None:

                # try:
                cateory = Cateory.objects.get(cateory_name=data["cateory"])
                user = User.objects.get(username=data["author"])
                db = Content(title=data["title"], content=data["content"], cateory=cateory, user=user)
                db.save()
                # except:
                #     return JsonResponse({
                #         "status_code": 1,
                #         "error": "save define"
                #     })

                return JsonResponse({
                    "status_code": 0,
                    "data": "success"
                })
            else:
                return JsonResponse({
                    "status_code": 1,
                    "error": "data is vaild"
                })
        # 添加访问数
        if add_access is not None and add_access == "add_access":
            try:
                db = GetNum.objects.get(date=time.strftime("%Y-%m-%d"))
                db.number += 1
                db.save()
                return JsonResponse({
                    "status_code": 0,
                    "data": "first user access"
                })
            except:
                db = GetNum()
                db.number = 1
                db.save()
                return JsonResponse({
                    "status_code": 0,
                    "data": "access success!"
                })

        return JsonResponse({
            "status_code": 1,
            "error": "not done"
        })


# /apis/face  0d62f4e0ccdf47c235e34ba512a882c388f667eae540169c7bfd9a415de303494eea5076f90f21cb2ca0299de4cb3bb2
def checkface(request):
    try:
        files = request.FILES.get("file")
        type_image = files.name.split('.')[-1]
        filename = "./upload/" + hashlib.sha3_384(files.name.encode()).hexdigest() + f".{type_image}"
        with open(filename, "ab+") as fp:
            fp.write(files.read())
        img = BytesIO()
        image = face_recognition.load_image_file(filename)
        locations = face_recognition.face_locations(img=image)
        result_image = Image.fromarray(image)
        for pos in locations:
            d = ImageDraw.Draw(result_image, 'RGBA')
            d.rectangle((pos[3], pos[0], pos[1], pos[2]))
        result_image.save(img, 'png')

        return JsonResponse({
            "status": 0,
            "filename": files.name,
            "face_count": len(locations),
            "resultImg_base": str(base64.b64encode(img.getvalue()).decode())
        })
    except:
        return JsonResponse({
            "status": 1,
            "message": "重试一下吧. 你的照片有问题哦."
        })


class Users:
    @staticmethod
    def get_status(request):
        if request.user.is_authenticated:
            user_ic = UserIC.objects.get(user_id=request.user.id)
            if user_ic.IC_num == "":
                return JsonResponse({
                    "status": 2,  # 登陆未认证
                    "id": str(request.user.id),
                    "is_superuser": User.objects.get(id=request.user.id).is_superuser,
                    "is_staff": User.objects.get(id=request.user.id).is_staff,
                    "username": str(request.user),
                    "email": str(request.user.email)
                })
            else:
                return JsonResponse({
                    "status": 0,  # 登陆且认证
                    "id": str(request.user.id),
                    "is_superuser": User.objects.get(id=request.user.id).is_superuser,
                    "is_staff": User.objects.get(id=request.user.id).is_staff,
                    "username": str(request.user),
                    "email": str(request.user.email)
                })
        else:
            return JsonResponse({
                "status": 1  # 未登陆
            })

    @staticmethod
    def login_user(request):
        if request.method == "POST":
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            if username is not None and password is not None:
                islogin = authenticate(request, username=username, password=password)
                if islogin:
                    login(request, islogin)
                    return JsonResponse({
                        "status": 0,
                        "message": "Login Success",
                        "username": username
                    })
                else:
                    return JsonResponse({
                        "status": 1,
                        "message": "登录失败, 请检查用户名或者密码是否输入正确."
                    })
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "参数错误"
                })

    @staticmethod
    def logout_user(request):
        logout(request)
        return JsonResponse({
            "status": 0
        })

    @staticmethod
    def register(request):
        if request.method == "POST":
            data = json.loads(request.body)

            if request.GET.get("select") is not None:
                select_username = data.get("select_username")
                print(select_username)
                try:
                    User.objects.get(username=select_username)
                    return JsonResponse({
                        "status": 0,
                        "is_indb": 1
                    })
                except:
                    return JsonResponse({
                        'status': 0,
                        "is_indb": 0
                    })
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            if username is not None and password is not None and email is not None:
                try:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    user_ic = UserIC(user_id=user.id)
                    user_ic.save()
                    login_user = authenticate(request, username=username, password=password)
                    if login_user:
                        login(request, login_user)
                        return JsonResponse({
                            "status": 0,
                            "message": "Register and Login Success"
                        })

                except:
                    return JsonResponse({
                        "status": 2,
                        "message": "注册失败, 该用户名已经存在."
                    })

        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })
