import re
from datetime import datetime
from django import forms
from agenda.forms import MyModelForm
from .models import *


class FormEntidade(MyModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('inicio_mandato') > cleaned_data.get('fim_mandato'):
            raise forms.ValidationError('O inicio do mandato não pode ser posterior ao fim do mandato!')

    class Meta:
        model = Entidade
        exclude = []


class FormContatoEntidade(forms.ModelForm):

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
        model = ContatoEntidade
        exclude = []


class FormOficio(MyModelForm):

    def clean_data(self):
        data = self.cleaned_data.get('data', '')

        if datetime.now().today() > data:
            raise forms.ValidationError('O oficio não pode ser anterior a data atual!')

        return data

    class Meta:
        model = Oficio
        exclude = []


class FormCargo(MyModelForm):

    class Meta:
        model = Cargo
        exclude = []