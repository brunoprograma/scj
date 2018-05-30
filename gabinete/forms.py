import re
from django import forms


class FormEnderecoDeputado(forms.ModelForm):

    def clean_telefone(self):
        data = re.sub('\D', '', self.cleaned_data.get('telefone', ''))

        if len(data) not in (10, 11):
            raise forms.ValidationError('Telefone inválido.')

        return data