from django.urls import path

from . import views

urlpatterns = [
    path('pdf/<int:id_oficio>/', views.Pdf.as_view()),
]