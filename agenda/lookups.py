from ajax_select import register, LookupChannel
from .models import *


@register('companhias')
class CompanhiaLookup(LookupChannel):

    model = Companhia

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='companhia'>{}</span>".format(item)
