"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from . import view

urlpatterns = [
    url(r'^sellhome$', view.show_sells),
    url(r'^show_all_sell$', view.show_all_sell),
    url(r'^allgoods$', view.allgoods),
    url(r'^show_goods_sell/(?P<goods_id>\d+)$', view.show_goods_sell,name='show_goods_sell'),
]
