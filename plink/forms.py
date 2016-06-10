from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from django.http import HttpResponseRedirect

from models import Plink
from models import PlinkPrefabs
from models import PlinkJob
from models import PlinkOption

from django.forms.widgets import ChoiceInput

__author__ = 'dgraham'


class PlinkJobForm(forms.ModelForm):
    class Meta:
        model = PlinkJob
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PlinkJobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.fields['job_id'].widget.attrs['readonly'] = True
        # # self.fields['status'].widget.attrs['readonly'] = True
        # # self.fields['status'].widget.attrs['disabled'] = True
        self.fields['plink_id'] = forms.ChoiceField(
            choices=get_plink_choices()
        )
        # self.fields['result_text'] = forms.ChoiceField(
        #     choices=get_plink_choices(),
        #     widget=forms.HiddenInput()
        # )
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            )
        )


class PlinkForm(forms.ModelForm):
    class Meta:
        model = Plink
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PlinkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML(
                    """<a role="button" class="btn btn-default"
                href="{% url "home" %}">Cancel</a>"""
                ),
                Submit(
                    'save',
                    'Submit'
                ),
            )
        )


class AddPlinkOptionForm(forms.Form):
    plink_id = forms.CharField(
        max_length=50
    )
    key = forms.CharField(max_length=64)
    value = forms.CharField(max_length=255)
    type = forms.ChoiceField(
        choices=PlinkOption.TYPE_CHOICES
    )


class PlinkOptionForm(forms.ModelForm):
    class Meta:
        model = PlinkOption
        fields = ('plink_id', 'key', 'value', 'type')

    def __init__(self, *args, **kwargs):
        super(PlinkOptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                Submit(
                    'save',
                       'Submit'
                ),
            )
        )


class LoaderForm(forms.ModelForm):
    class Meta:
        model = Plink
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LoaderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            )
        )


class PlinkPrefabsForm(forms.Form):
    class Meta:
        model = PlinkPrefabs
        fields = ('plink_id', 'description', 'prefab_path', 'options_str')

    def __init__(self, *args, **kwargs):
        super(LoaderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            )
        )


# Ref: https://docs.djangoproject.com/en/1.9/topics/http/file-uploads/
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def get_plink_choices():
    choice_list = []
    for plink in Plink.objects.all():
        tmp_tuple = (plink.plink_id, plink.plink_id)
        choice_list.append(tmp_tuple)
    print(choice_list)
    return choice_list