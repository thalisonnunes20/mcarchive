from django.urls import path
from . import views

app_name = "serverjars"

urlpatterns = [
    path("",                          views.serverjar_lista,          name="lista"),
    path("categoria/<slug:slug>/",    views.serverjar_por_categoria,  name="por_categoria"),
    path("<slug:slug>/",              views.serverjar_detalhe,        name="detalhe"),
    path("<slug:slug>/download/",     views.serverjar_download,       name="download"),
]