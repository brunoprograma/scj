from datetime import datetime
from django.utils import timezone
from django import forms


class FormCompromisso(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('data_hora_inicio') > cleaned_data.get('data_hora_fim'):
            raise forms.ValidationError('Data de início anterior a data de termino!')

        return cleaned_data
