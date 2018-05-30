from django.urls import path, include
from . import views

deputado = views.DeputadoCRUD()

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include(deputado.get_urls())),
]