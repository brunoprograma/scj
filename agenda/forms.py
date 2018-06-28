from ajax_select.fields import AutoCompleteSelectField
from django import forms
from .models import Voo, Compromisso, TipoCompromisso


class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.is_customer = self.request and not self.request.user.is_superuser
        super(MyModelForm, self).__init__(*args, **kwargs)
        if self.is_customer:
            self.fields['deputado'].widget = forms.HiddenInput()
            self.fields['deputado'].initial = self.request.user.deputado

    def clean_deputado(self):
        data = self.cleaned_data.get('deputado')

        if self.is_customer:
            return self.request.user.deputado

        return data


class FormTipoCompromisso(MyModelForm):
    class Meta:
        model = TipoCompromisso
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)


class FormCompromisso(MyModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('data_hora_inicio') >= cleaned_data.get('data_hora_fim'):
            raise forms.ValidationError('Data e hora de início anterior a data e hora de termino!')

        return cleaned_data

    class Meta:
        model = Compromisso
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    cidade = AutoCompleteSelectField('cidades', label='Cidade', help_text=None)


class FormVoo(MyModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('data_hora_partida') >= cleaned_data.get('data_hora_chegada'):
            raise forms.ValidationError('Data e hora de partida anterior a data e hora de chegada!')

        if cleaned_data.get('cidade_partida') == cleaned_data.get('cidade_chegada'):
            raise forms.ValidationError('A cidade de chegada deve ser diferente da cidade de partida!')

        return cleaned_data

    class Meta:
        model = Voo
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    cidade_partida = AutoCompleteSelectField('cidades', label='Cidade de partida', help_text=None)
    cidade_chegada = AutoCompleteSelectField('cidades', label='Cidade de chegada', help_text=None)
    companhia = AutoCompleteSelectField('companhias', label='Companhia aérea', help_text=None)
