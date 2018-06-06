from django.views.generic import TemplateView
from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from .models import Cargo, Entidade, ContatoEntidade, Oficio


class Cargo_CRUD(CRUDView):
    model = Cargo


class ContatoEntidade_AjaxCRUD(InlineAjaxCRUD):
    model = ContatoEntidade
    base_model = Entidade
    inline_field = 'entidade'


class Entidade_CRUD(CRUDView):
    model = Entidade
    inlines = [ContatoEntidade_AjaxCRUD]


class Oficio_CRUD(CRUDView):
    model = Oficio