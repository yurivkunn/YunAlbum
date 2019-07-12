"""YunAlbum URL Configuration

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
from django.urls import path, re_path
from MyAlbum import views
from django.conf.urls import url

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index),
    url(r'^admin_login/$', views.login, name='admin_login'),
    url(r'^change_to_homepage/$', views.change_to_homepage, name='change_to_homepage'),
    url(r'^get_checkCode/$', views.email_auth, name='get_checkCode'),
    path('admin_register', views.register, name='admin_register'),
    path('showPict', views.getAllPict, name='showPict'),
    url(r'^change_to_homepage/getInfo_Album/$', views.getInfo_Album, name='getAlbum'),
    url(r'^change_to_homepage/getAllPict/$', views.getAllPict, name='getAllPict'),
    url(r'^change_to_homepage/recycle/$', views.recycle, name='recycle'),
    url(r'^change_to_homepage/showRecycle/$', views.showRecycle, name='showRecycle'),
    url(r'^change_to_homepage/logout/$', views.logout, name='logout'),
    url(r'^change_to_homepage/addAlbum/$', views.addAlbum, name='addAlbum'),
    url(r'^change_to_homepage/getPictByAlbum/$', views.getPictByAlbum, name='getPictByAlbum'),
    url(r'^change_to_homepage/upload/$', views.upload, name='upload'),
    url(r'^change_to_homepage/xinxi/$', views.changToInfo, name='xinxi'),
    url(r'^change_to_homepage/shezhi/$', views.changToSetting, name='shezhi'),
    url(r'^change_to_homepage/fankui/$', views.changToFankui, name='fankui'),
    url(r'^change_to_homepage/success/$', views.success, name='success'),
    url(r'^change_to_homepage/bangzhu/$', views.changToHelp, name='bangzhu'),
    url(r'^change_to_homepage/editTag/$', views.editTag, name='editTag'),
    url(r'^change_to_homepage/deleteAlbum/$', views.deleteAlbum, name='deleteAlbum'),
    url(r'^change_to_homepage/deletePhoto/$', views.deletePhoto, name='deletePhoto'),

    url(r'^change_to_homepage/deleteComplete/$', views.deleteComplete, name='deleteComplete'),
    re_path(r'^change_to_homepage/search/(?P<content>.*)$', views.search, name='search'),

    url(r'^change_to_homepage/shezhi/changeSetting/$', views.changSetting, name='changeSetting'),
    url(r'^upload/$', views.upload, name='upload'),
]
