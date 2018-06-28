from ajax_select import register, LookupChannel
from .models import *


@register('deputados')
class DeputadoLookup(LookupChannel):

    model = Deputado

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='deputado'>{}</span>".format(item)


@register('cidades')
class CidadeLookup(LookupChannel):

    model = Cidade

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q)[:50]

    def format_item_display(self, item):
        return u"<span class='cidade'>{}</span>".format(item)


@register('estados')
class EstadoLookup(LookupChannel):

    model = Estado

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='estado'>{}</span>".format(item)


@register('paises')
class PaisLookup(LookupChannel):

    model = Pais

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='pais'>{}</span>".format(item)


@register('regionais')
class RegionalLookup(LookupChannel):

    model = Regional

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='regional'>{}</span>".format(item)


@register('partidos')
class PartidoLookup(LookupChannel):

    model = Partido

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='partido'>{}</span>".format(item)
