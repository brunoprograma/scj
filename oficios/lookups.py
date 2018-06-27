from ajax_select import register, LookupChannel
from .models import *


@register('entidades')
class EntidadeLookup(LookupChannel):

    model = Entidade

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='entidade'>{}</span>".format(item)


@register('pessoas')
class PessoaLookup(LookupChannel):

    model = Pessoa

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='pessoa'>{}</span>".format(item)


@register('oficios')
class OficioLookup(LookupChannel):

    model = Oficio

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='oficio'>{}</span>".format(item)
