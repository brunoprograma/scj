import re
from django import forms
from .models import EnderecoDeputado


class FormEnderecoDeputado(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', self.cleaned_data.get('telefone', ''))

        if len(data) not in (10, 11):
            raise forms.ValidationError('Telefone inválido!')

        return data

    def clean_fax(self):
        data = re.sub('\D', '', self.cleaned_data.get('fax', ''))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Fax inválido!')

        return data

    def clean_celular(self):
        data = re.sub('\D', '', self.cleaned_data.get('celular', ''))

        if len(data) not in (0, 10, 11):
            raise forms.ValidationError('Celular inválido!')

        return data

    def clean(self):
        cleaned_data = self.cleaned_data
        telefone = re.sub('\D','', self.cleaned_data.get('telefone',''))
        fax = re.sub('\D', '', self.cleaned_data.get('fax',''))
        whatsapp = re.sub('\D', '', self.cleaned_data.get('celular',''))

        if telefone == fax or telefone == whatsapp or fax == whatsapp :
            raise forms.ValidationError('Telefones não devem ser iguais!')

        return cleaned_data

    class Meta:
        model = EnderecoDeputado
        exclude = []