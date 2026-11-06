from django.urls import path
from . import views

app_name = "tutorials"

urlpatterns = [
    path("",                          views.tutorial_lista,          name="lista"),
    path("categoria/<slug:slug>/",    views.tutorial_por_categoria,  name="por_categoria"),
    path("<slug:slug>/",              views.tutorial_detalhe,        name="detalhe"),
]
