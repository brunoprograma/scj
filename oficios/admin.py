from django.contrib import admin
from .models import *
from .forms import FormEntidade, FormContatoEntidade, FormOficio


class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome')


admin.site.register(Cargo)
admin.site.register(Entidade)
admin.site.register(Oficio)