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
            self.fields['pessoas'].queryset = Pessoa.objects.ativo(deputado=self.oficio.deputado, regional=self.oficio.regional)

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    pessoas = forms.ModelMultipleChoiceField(Pessoa.objects.ativo(), label='',
                                               widget=FilteredSelectMultiple(verbose_name='Pessoas',
                                                                             is_stacked=False))


class FormInstituicao(MyModelForm):

    class Meta:
        model = Instituicao
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    regional = AutoCompleteSelectField('regionais', label='Regional', help_text=None)
    cidade = AutoCompleteSelectField('cidades', label='Cidade', help_text=None)


class FormPessoa(MyModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        ini = cleaned_data.get('inicio_mandato')
        fim = cleaned_data.get('fim_mandato')

        if (ini and fim) and (ini > fim):
            raise forms.ValidationError('O inicio do mandato não pode ser posterior ao fim do mandato!')

    class Meta:
        model = Pessoa
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    instituicao = AutoCompleteSelectField('instituicao', label='Instituição', help_text=None)
    cargo = AutoCompleteSelectField('cargos', label='Cargo', help_text=None)
    partido = AutoCompleteSelectField('partidos', label='Partido', help_text=None)


class FormTelefonePessoa(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', str(self.cleaned_data.get('telefone', '')))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Telefone inválido!')

        return data

    class Meta:
        model = TelefonePessoa
        exclude = []


class FormEmailPessoa(forms.ModelForm):

    class Meta:
        model = EmailPessoa
        exclude = []


class FormEnderecoPessoa(forms.ModelForm):

    class Meta:
        model = EnderecoPessoa
        exclude = []

    cidade = AutoCompleteSelectField('cidades', label='Cidade', help_text=None)


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
