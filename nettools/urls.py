"""nettools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from zabbix.views import add_host
from devices.views import generate_config, display_db, create_device
from vsi.views import display_all_vsi
from phones.views import display_phone_book


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add/$', add_host),
    url(r'^generate/$', generate_config),
    url(r'^list/$', display_db),
    url(r'^$', display_db),
    url(r'^create/$', create_device),
    url(r'^vsi/$', display_all_vsi),
    url(r'^phones/$', display_phone_book)
]
