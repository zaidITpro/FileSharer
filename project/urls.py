"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from project import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','log.views.home',name='home'),
    url(r'^signup/','log.views.signup',name='signup'),
    url(r'^loggedin/','log.views.loggedin',name='loggedin'),
    url(r'^signin/','log.views.signin',name='signin'),
    url(r'^user/','log.views.user',name='user'),
    url(r'^logout/','log.views.logout_view',name='logout_view'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()
