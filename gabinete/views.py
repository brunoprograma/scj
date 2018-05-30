from django.views.generic import TemplateView
from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from .forms import FormEnderecoDeputado
from .models import Deputado, EnderecoDeputado


class IndexView(TemplateView):
    """
    View da home do sistema
    """
    template_name = 'adminlte/index.html'


class EnderecoDeputado_AjaxCRUD(InlineAjaxCRUD):
    model = EnderecoDeputado
    base_model = Deputado
    # add_form = FormEnderecoDeputado
    # update_form = FormEnderecoDeputado
    inline_field = 'deputado'
    fields = ['telefone']
    views_available = ['create', 'update', 'delete']
    title = 'ok'


class DeputadoCRUD(CRUDView):
    model = Deputado
    inlines = [EnderecoDeputado_AjaxCRUD]