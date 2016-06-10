from django.conf.urls import url

from . import views

from views import CreatePlinkView
from views import CreatePrefabsView
from views import PlinkList
from views import CreatePlinkJobView
from views import JobList
from views import CreatePlinkOptionView

urlpatterns = [
    # Base Urls
    url(r"^$", views.home, name="home"),
    # Plink Urls
    url(r'^plink/detail/(?P<plink_id>[\w]+)/$', views.detail, name='detail'),
    url(r'^plink/create/', views.CreatePlinkView.as_view(), name='plink_create'),
    url(r'^plink/upload/success/$', views.upload_success, name='upload_success'),
    url(r'^plink/upload/$', views.upload_file, name='upload'),
    url(r'^plink/$', views.plink_dash, name='plink'),
    # Prefabs Urls
    url(r'^plink/prefabs/load/', views.load_prefabs, name="load_prefabs"),
    url(r'^plink/prefabs/$', views.PlinkList.as_view(), name="prefabs"),
    # Options Urls
    url(r'^plink/options/create/$', views.CreatePlinkOptionView.as_view(), name='plinkoption_create'),
    url(r'^plink/options/add/(?P<plink_id>[\w]+)/$', views.add_plink_option, name='plinkoption_add'),
    url(r'^plink/options/create/min/', views.CreatePlinkOptionMinView.as_view(), name='plinkoption_create_min'),
    # Job Urls
    url(r'^plink/jobs/create/$', views.CreatePlinkJobView.as_view(), name="plinkjob_create"),
    url(r'^plink/jobs/detail/(?P<job_id>[\w]+)/', views.job_detail, name="plinkjob_detail"),
    url(r'^plink/jobs/run/(?P<job_id>[\w]+)/', views.job_run, name="plinkjob_run"),
    url(r'^plink/jobs/$', views.JobList.as_view(), name="plinkjob_list"),
]
