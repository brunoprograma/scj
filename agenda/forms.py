from django import forms
from .models import Voo, Compromisso


class FormCompromisso(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('data_hora_inicio') >= cleaned_data.get('data_hora_fim'):
            raise forms.ValidationError('Data e hora de início anterior a data e hora de termino!')

        return cleaned_data

    class Meta:
        model = Compromisso
        exclude = []


class FormVoo(forms.ModelForm):

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
        #fields = '__all__'