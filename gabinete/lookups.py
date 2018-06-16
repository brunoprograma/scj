from ajax_select import register, LookupChannel
from .models import Regional


@register('regionais')
class TagsLookup(LookupChannel):

    model = Regional

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q, ativo=True)[:50]

    def format_item_display(self, item):
        return u"<span class='regional'>{}</span>".format(item)