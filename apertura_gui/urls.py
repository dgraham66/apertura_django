"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.contrib.auth.models import User
import django.contrib.auth.views
from rest_framework import routers, serializers, viewsets
from django.views.generic import TemplateView
from plink import urls
import views
from views import Docs

# Serializers define the API representation.


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'is_staff')
#
# # ViewSets define the view behavior.
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class PlinkViewSet(viewsets.ModelViewSet):
#     queryset = Plink.objects.all()
#     serializer_class = PlinkSerializer
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'plink', PlinkViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^about/", views.about, name="about"),
    url(r"^docs/", views.docs, name="docs"),
    # Auth urls
    url(r'^accounts/login$', django.contrib.auth.views.login,
        {'template_name': 'login.html'},
        name="login"),
    url(r'^accounts/logout$', django.contrib.auth.views.logout,
        {'template_name': 'logout.html'},
        name="logout"),
    url(r'^accounts/change_password$',
        django.contrib.auth.views.password_change,
        {'template_name': 'password_change.html',
         'post_change_redirect':
             'django.contrib.auth.views.password_change_done'},
        name="change_password"),
    url(r'^accounts/change_password_done$',
        django.contrib.auth.views.password_change_done,
        {'template_name': 'password_change_done.html'}),
    url(r'', include(urls)),
]
