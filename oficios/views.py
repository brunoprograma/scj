from django.views.generic import View
from django.shortcuts import get_object_or_404
from .models import *
from .render import Render


class Pdf(View):
    def get(self, request, id_oficio):
        oficio = get_object_or_404(Oficio, id=id_oficio)
        regional = oficio.regional

        for entidade in Entidade.objects.filter(regional=regional, ativo=True):
            params = {
                'oficio': oficio,
                'regional': oficio.regional,
                'entidade': entidade.objects,
                'endereco': oficio.deputado.endereco_principal
            }
            return Render.render('oficio.html', params)