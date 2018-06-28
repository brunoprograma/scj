import re
from ajax_select.fields import AutoCompleteSelectField
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from agenda.forms import MyModelForm
from .models import *


class UserCreationForm(BaseUserCreationForm, MyModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)

    class Meta:
        model = User
        fields = ("deputado", "email", "password1", "password2")


class UserChangeForm(BaseUserChangeForm, MyModelForm):
    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)


class FormRegional(MyModelForm):

    class Meta:
        model = Regional
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)


class FormDeputado(forms.ModelForm):

    class Meta:
        model = Deputado
        exclude = []

    partido = AutoCompleteSelectField('partidos', label='Partido', help_text=None)
    estado = AutoCompleteSelectField('estados', label='Estado de atuação', help_text=None)


class FormEnderecoDeputado(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', str(self.cleaned_data.get('telefone', '')))

        if len(data) not in (10, 11):
            raise forms.ValidationError('Telefone inválido!')

        return data

    def clean_fax(self):
        data = re.sub('\D', '', str(self.cleaned_data.get('fax', '')))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Fax inválido!')

        return data

    def clean_celular(self):
        data = re.sub('\D', '', str(self.cleaned_data.get('celular', '')))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Celular inválido!')

        return data

    class Meta:
        model = EnderecoDeputado
        exclude = []

    cidade = AutoCompleteSelectField('cidades', label='Cidade', help_text=None)
