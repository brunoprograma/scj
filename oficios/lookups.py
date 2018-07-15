from ajax_select import register, LookupChannel
from .models import *


@register('pessoa')
class PessoaLookup(LookupChannel):

    model = Pessoa

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='pessoa'>{}</span>".format(item)


@register('instituicao')
class InstituicaoLookup(LookupChannel):

    model = Instituicao

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='instituicao'>{}</span>".format(item)


@register('oficios')
class OficioLookup(LookupChannel):

    model = Oficio

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='oficio'>{}</span>".format(item)


@register('cargos')
class CargoLookup(LookupChannel):

    model = Cargo

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='cargo'>{}</span>".format(item)
