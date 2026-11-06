from django.urls import path
from . import views

app_name = "modpacks"

urlpatterns = [
    path("",                          views.modpack_lista,          name="lista"),
    path("categoria/<slug:slug>/",    views.modpack_por_categoria,  name="por_categoria"),
    path("<slug:slug>/",              views.modpack_detalhe,        name="detalhe"),
    path("<slug:slug>/download/",     views.modpack_download,       name="download"),
]