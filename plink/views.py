import django.views.generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import os, subprocess
import yaml
from forms import UploadFileForm

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from serializers import UserSerializer, GroupSerializer, PlinkSerializer

from models import Plink
from models import PlinkPrefabs
from models import PlinkJob
from models import PlinkOption

from forms import PlinkForm
from forms import PlinkPrefabsForm
from forms import PlinkJobForm
from forms import PlinkOptionForm
from forms import AddPlinkOptionForm


# Class-based Views
class Home(django.views.generic.TemplateView):
    template_name = "home.html"
home = Home.as_view()
#
#
# class About(django.views.generic.TemplateView):
#     template_name = "about.html"
# about = About.as_view()
#
#
# class Docs(django.views.generic.TemplateView):
#     template_name = "docs.html"
# docs = Docs.as_view()


class CreatePlinkView(CreateView):
    template_name = "plink/create_plink.html"
    form_class = PlinkForm
    model = Plink


class CreatePlinkJobView(CreateView):
    template_name = "plink/create_plink_job.html"
    form_class = PlinkJobForm
    model = PlinkJob


class CreatePrefabsView(CreateView):
    template_name = "plink/plink_list.html"
    form_class = PlinkPrefabsForm
    model = PlinkPrefabs


class CreatePlinkOptionMinView(CreateView):
    template_name = "plink/create_plink_option_min.html"
    form_class = PlinkOptionForm
    model = PlinkOption


class CreatePlinkOptionView(CreateView):
    template_name = "plink/create_plink_option.html"
    form_class = PlinkOptionForm
    model = PlinkOption


# class AddPlinkOptionView(CreateView):
#     template_name = "plink/add_plink_option.html"
#     form_class = AddPlinkOptionForm
#     model = PlinkOption
#
#     def get_form_kwargs(self):
#         kwargs = super(AddPlinkOptionView, self).get_form_kwargs()
#         # update the kwargs for the form init method with yours
#         kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
#         return kwargs


# List Views
class PlinkList(ListView):
    model = Plink


class PlinkDetailList(CreateView):
    pass


class JobList(ListView):
    model = PlinkJob


# Detail Views


# Function-based Views
def add_plink_option(request, plink_id):
    plink = get_object_or_404(Plink, plink_id=plink_id)
    if request.method == 'POST':
        form = AddPlinkOptionForm(request.POST)
        # form.plink_id = plink_id
        if form.is_valid():
            option = PlinkOption(
                plink_id=plink,
                key=form['key'],
                value=form['value'],
                type=form['type']
            )
            option.save()
            return render(
                request,
                'plink/detail.html',
                {'plink': plink})
    else:
        form = AddPlinkOptionForm()
        # form.fields['plink_id'] = plink.plink_id
    return render(request, 'plink/add_plink_option.html', {'form': form, 'plink': plink})


def plink_dash(request):
    return render(
        request,
        'plink/plink_dash.html'
    )


def detail(request, plink_id):
    plink = get_object_or_404(Plink, plink_id=plink_id)
    return render(
        request,
        'plink/detail.html',
        {'plink': plink}
    )


def job_detail(request, job_id):
    job = get_object_or_404(PlinkJob, pk=job_id)
    plink = get_object_or_404(Plink, plink_id=job.plink_id)
    return render(
        request,
        'plink/plinkjob_detail.html',
        {'job': job, 'plink': plink}
    )


def job_run(request, job_id):
    job = PlinkJob.objects.get(pk=job_id)
    plink = Plink.objects.get(plink_id=job.plink_id)
    results = run_pipeline(job_id=job.pk, template_path=plink.prefab_path)
    # Store results
    job.status = '121' if results['called'] else '141'
    job.status = '999' if results['complete'] else '141'
    job.result_text = "cmd:\n%s\nresults:\n%s\n" % (
        results['cmd'],
        results['results']
    )
    job.save()

    return render(
        request,
        'plink/plinkjob_detail.html',
        {'job': get_object_or_404(PlinkJob, pk=job_id), 'plink': plink}
    )


# Utility Functions
def run_pipeline(job_id, template_path):
    entry = EntryPoint(job_id=job_id, template_path=template_path, run_local=False)
    result_dict = {
        'cmd': str(entry.cmd),
        'called': str(entry.was_called),
        'complete': str(entry.has_completed),
        'results': str(entry.result_string)
    }
    return result_dict


def get_prefab_path_dict():
    template_dir = os.path.abspath("static/script_templates/")
    path_dict = {}
    for file in os.listdir(template_dir):
        p_id = os.path.splitext(file)[0]
        path = os.path.join(template_dir, file)
        path_dict[p_id] = path
    return path_dict


class EntryPoint(object):
    def __init__(self, job_id, template_path, auto_run=True, run_local=True):
        self.job_id = job_id
        self.template_path = os.path.abspath(template_path)
        self.was_called = False
        self.has_completed = False
        self.result_string = ''
        self.cmd = []
        self.run_local = run_local

        self.param_dict = {
            'luigi_call': 'luigi',
            'module_name_1': 'APERTURA.pipeline',
            'module_name_2': 'PlinkCommand',
            'job_id': str(self.job_id),
            'template_path': str(self.template_path)
        }
        if run_local:
            self.param_dict['scheduler'] = '--local-scheduler'
        if auto_run:
            self.was_called = True
            self.has_completed = self.__execute_cmd__()

    def __execute_cmd__(self):
        try:
            self.cmd = self.__build_command__()
            # self.result_string += "call_cmd:\n%s\n" % str(self.cmd)
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE)
            output = process.communicate()[0]
            process.wait()
            self.result_string += "\n\nPlink Call Output:\n%s\n\n" % output
            # print(self.result_string)
        except:
            return False

        return True

    def __build_command__(self):
        tmp_cmd = []
        tmp_cmd.append(self.param_dict['luigi_call'])
        tmp_cmd.append('--module')
        tmp_cmd.append(self.param_dict['module_name_1'])
        tmp_cmd.append(self.param_dict['module_name_2'])
        if self.run_local:
            tmp_cmd.append(self.param_dict['scheduler'])
        tmp_cmd.append('--jobid')
        tmp_cmd.append(self.param_dict['job_id'])
        tmp_cmd.append('--templatepath')
        tmp_cmd.append(self.param_dict['template_path'])
        return tmp_cmd


def get_prefab_id_list():
    template_dir = os.path.abspath("static/script_templates/")
    template_list = [os.path.splitext(f)[0] for f in os.listdir(template_dir) if
                     os.path.isfile(os.path.join(template_dir, f))]
    return template_list


def load_prefabs(request):
    output = []
    tmp_str = ''
    path_dict = get_prefab_path_dict()
    for key, value in path_dict.iteritems():
        data = yaml.load(open(value))
        pk_name = data['pk_name']
        pretty_name = data['pretty_name']
        description = data['description']
        options = data['plink_options']
        tmp_str = "plink_id:\n%s\nprefab_path:\n%s\noptions_str:\n%s\n" % (key, value, str(options))
        output.append(tmp_str)
        p = Plink(
            plink_id=pk_name,
            description=description,
            prefab_path=value,
            options_str=str(options),
            pretty_name=pretty_name
        )
        p.save()
        for opt_dict in options:
            option = PlinkOption(
                plink_id=p,
                key=opt_dict['opt_key'],
                value=opt_dict['opt_value'],
                type=opt_dict['opt_type']
            )
            option.save()
    return HttpResponse(output)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(
                'success/'
            )
    else:
        form = UploadFileForm()
    return render(request, 'plink/upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('data/tmp/upload_test_file.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_success(request):
    return render(
        request,
        'plink/upload_success.html'
    )


# def load_prefabs(request):
#     output = []
#     tmp_str = ''
#     path_dict = get_prefab_path_dict()
#     for key, value in path_dict.iteritems():
#         data = yaml.load(open(value))
#         options = data['plink_options']
#         tmp_str = "plink_id: %s\nprefab_path: %s\noptions_str: %s\n\n" % (key, value, str(options))
#         output.append(tmp_str)
#         p = Plink(
#             plink_id=key,
#             description='',
#             prefab_path=value,
#             options_str=str(options)
#         )
#         p.save()
#         for o_key, o_value in dict(options).iteritems():
#             if o_value is None:
#                 o_value = ''
#             option = PlinkOption(
#                 plink_id=p,
#                 key=o_key,
#                 value=o_value
#             )
#             option.save()
#     return HttpResponse(output)


# Old

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer