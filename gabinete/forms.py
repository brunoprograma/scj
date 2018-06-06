import re
from django import forms
from .models import EnderecoDeputado


class FormEnderecoDeputado(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', self.cleaned_data.get('telefone', ''))

        if len(data) not in (10, 11):
            raise forms.ValidationError('Telefone inválido.')

        return data

    def clean_fax(self):
        data = re.sub('\D', '', self.cleaned_data.get('fax', ''))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Fax inválido.')

        return data

    def clean_whatsapp(self):
        data = re.sub('\D', '', self.cleaned_data.get('whatsapp', ''))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Whatsapp inválido.')

        return data

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('fax') == cleaned_data.get('whatsapp'):
            raise forms.ValidationError('telefones nao devem ser iguais')

        return cleaned_data

    class Meta:
        model = EnderecoDeputado
        exclude = []