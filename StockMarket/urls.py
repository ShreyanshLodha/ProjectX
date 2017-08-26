"""StockMarket URL Configuration

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
from Project.views import *
import Project.PreviousData

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^about/', about),
    url(r'^contact/', contact),
    url(r'^equity/', equity),
    url(r'^home/$', home),
    url(r'^home-registered/$',register_user),
    url(r'^news/', news),
    url(r'^portfolio/', portfolio),
    url(r'^products/', products),
    url(r'^service', services),
    url(r'^single/', single),
    url(r'^sitemap/', sitemap),
    url(r'^dashboard/$',dashboard),
    url(r'^user/$',user),
    url(r'^past-transaction/$',pasttransaction),

    # Login related URL
    url(r'^login/$', login),
    url(r'^login-required/$', login),
    url(r'^login-wrong-password/$', login),


    # Signup related URLs
    url(r'^signup/$', signup),
    url(r'^signup-registered/$', signup),
    url(r'^signup-unregistered/$', signup),

    # logout
    url(r'^logout/$', logout),

    url(r'^typography/$', typography),
]
# Project.PreviousData.dataFetcher()
