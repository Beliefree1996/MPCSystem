# -*- coding: UTF-8 -*-
"""vuesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    # path('', views.index),
    path('admin/', admin.site.urls),
    path('apis/temporary', views.temporary),  # 临时接口
    path('apis/getQuota', views.getQuota),  # 获取授额
    path('apis/renew_HLP_privateKey', views.renew_HLP_privateKey),  # 更新HLP私钥
    path('apis/renew_HLP_other_privateKey', views.renew_HLP_other_privateKey),  # 更新HLP_other私钥
    path('apis/renew_Paillier_privateKey', views.renew_Paillier_privateKey),  # 更新Paillier私钥
    path('apis/renew_BFV_privateKey', views.renew_BFV_privateKey),  # 更新BFV私钥
    path('apis/renew_CKKS_privateKey', views.renew_CKKS_privateKey),  # 更新CKKS私钥
    path('apis/get_info', views.get_info),  # 提供数据接口
    path('apis/add', views.add_data),  # 添加数据
    path('apis/change_data', views.change_data),    # 修改数据
    path('apis/face', views.checkface),  # 人脸识别api
    path('apis/user/getstatus', views.Users.get_status),  # 返回状态 是否登录
    path('apis/user/login', views.Users.login_user),  # 登录
    path('apis/user/logout', views.Users.logout_user),  # 注销
    path('apis/user/register', views.Users.register),   # 注册
]
