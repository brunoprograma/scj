import re
from django import forms
from .models import EnderecoDeputado


class FormEnderecoDeputado(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', self.cleaned_data.get('telefone', ''))

        if data and (len(data) not in (10, 11)):
            raise forms.ValidationError('O Telefone deve ter 10 ou 11 números, você digitou {}.'.format(len(data)))

        return data

    def clean_fax(self):
        data = re.sub('\D', '', self.cleaned_data.get('fax', ''))

        if data and (len(data) not in (10, 11)):
            raise forms.ValidationError('O Fax deve ter 10 ou 11 números, você digitou {}.'.format(len(data)))

        return data

    def clean_whatsapp(self):
        data = re.sub('\D', '', self.cleaned_data.get('whatsapp', ''))

        if data and (len(data) not in (11,)):
            raise forms.ValidationError('O WhatsApp deve ter 11 números, você digitou {}.'.format(len(data)))

        return data

    class Meta:
        model = EnderecoDeputado
        exclude = []