from django.urls import path, include
from . import views

deputado = views.DeputadoCRUD()

urlpatterns = [
    path('oficios', views.IndexView.as_view(), name='entidades'),
    path('', include(deputado.get_urls())),
]