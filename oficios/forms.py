import re
from ajax_select.fields import AutoCompleteSelectField
from django import forms
from django.utils import timezone
from django.contrib.admin.widgets import FilteredSelectMultiple
from agenda.forms import MyModelForm
from .models import *


class FormEscolheEntidade(forms.Form):
    def __init__(self, *args, **kwargs):
        self.oficio = kwargs.pop('oficio')
        super(FormEscolheEntidade, self).__init__(*args, **kwargs)
        if self.oficio:
            self.fields['entidades'].queryset = Entidade.objects.ativo(deputado=self.oficio.deputado, regional=self.oficio.regional)

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    entidades = forms.ModelMultipleChoiceField(Entidade.objects.ativo(), label='',
                                               widget=FilteredSelectMultiple(verbose_name='Pessoas ou Entidades',
                                                                             is_stacked=False))


class FormEntidade(MyModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        ini = cleaned_data.get('inicio_mandato')
        fim = cleaned_data.get('fim_mandato')

        if (ini and fim) and (ini > fim):
            raise forms.ValidationError('O inicio do mandato não pode ser posterior ao fim do mandato!')

    class Meta:
        model = Entidade
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    regional = AutoCompleteSelectField('regionais', label='Regional', help_text=None)
    cargo = AutoCompleteSelectField('cargos', label='Cargo', help_text=None)
    partido = AutoCompleteSelectField('partidos', label='Partido', help_text=None)
    cidade = AutoCompleteSelectField('cidades', label='Cidade', help_text=None)


class FormContatoEntidade(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', str(self.cleaned_data.get('telefone', '')))

        if len(data) not in (0, 10, 11):
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

        if data < timezone.now().date():
            raise forms.ValidationError('O ofício não pode ser anterior a data atual!')

        return data

    class Meta:
        model = Oficio
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    regional = AutoCompleteSelectField('regionais', label='Regional', help_text=None)


class FormCargo(MyModelForm):

    class Meta:
        model = Cargo
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
