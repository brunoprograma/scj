from ajax_select import register, LookupChannel
from .models import Entidade


@register('entidades')
class TagsLookup(LookupChannel):

    model = Entidade

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='entidade'>{}</span>".format(item)
