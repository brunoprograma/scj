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
            self.fields['deputado'].initial = self.request.user.deputado_id

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
        data_ini = cleaned_data.get('data_hora_inicio')
        data_fim = cleaned_data.get('data_hora_fim')

        if data_ini and data_fim and data_ini >= data_fim:
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
        data_p = cleaned_data.get('data_hora_partida')
        cidade_p = cleaned_data.get('cidade_partida')
        data_c = cleaned_data.get('data_hora_chegada')
        cidade_c = cleaned_data.get('cidade_chegada')

        if data_p and data_c and data_p >= data_c:
            raise forms.ValidationError('Data e hora de partida anterior a data e hora de chegada!')

        if cidade_p and cidade_c and cidade_p == cidade_c:
            raise forms.ValidationError('A cidade de chegada deve ser diferente da cidade de partida!')

        return cleaned_data

    class Meta:
        model = Voo
        exclude = []

    deputado = AutoCompleteSelectField('deputados', label='Deputado', help_text=None)
    cidade_partida = AutoCompleteSelectField('cidades', label='Cidade de partida', help_text=None)
    cidade_chegada = AutoCompleteSelectField('cidades', label='Cidade de chegada', help_text=None)
    companhia = AutoCompleteSelectField('companhias', label='Companhia aérea', help_text=None)
