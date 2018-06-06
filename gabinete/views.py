from django.views.generic import TemplateView
from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from .forms import FormEnderecoDeputado
from .models import Deputado, EnderecoDeputado, Partido, Pais, Estado, Cidade, Regional


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
    views_available = ['create', 'update', 'delete']
    title = 'ok'


class Deputado_CRUD(CRUDView):
    model = Deputado
    inlines = [EnderecoDeputado_AjaxCRUD]


class Pais_CRUD(CRUDView):
    model = Pais


class Estado_CRUD(CRUDView):
    model = Estado


class Cidade_CRUD(CRUDView):
    model = Cidade


class Partido_CRUD(CRUDView):
    model = Partido


class Regional_CRUD(CRUDView):
    model = Regional