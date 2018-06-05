from django.views.generic import TemplateView
from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from .forms import *
from .models import *


class IndexView(TemplateView):
    """
    View da home do sistema
    """
    template_name = 'adminlte/index.html'


class EnderecoDeputado_AjaxCRUD(InlineAjaxCRUD):
    model = EnderecoDeputado
    base_model = Deputado
    add_form = FormEnderecoDeputado
    update_form = FormEnderecoDeputado
    inline_field = 'deputado'
    fields = ['telefone']
    # views_available = ['list', 'create', 'update', 'delete']
    title = 'ok'
    check_login = False
    check_perms = False

class DeputadoCRUD(CRUDView):
    model = Deputado
    inlines = [EnderecoDeputado_AjaxCRUD,]
    check_login = False
    check_perms = False