from cruds_adminlte.crud import CRUDView
from .models import *


class TipoCompromisso_CRUD(CRUDView):
    model = TipoCompromisso


class Compromisso_CRUD(CRUDView):
    model = Compromisso


class Compania_CRUD(CRUDView):
    model = Companhia


class Voo_CRUD(CRUDView):
    model = Voo