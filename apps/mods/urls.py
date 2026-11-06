from django.urls import path
from . import views

app_name = "mods"

urlpatterns = [
    path("",                                      views.mod_lista,             name="lista"),
    path("categoria/<slug:slug>/",                views.mod_por_categoria,     name="por_categoria"),
    path("<slug:slug>/",                          views.mod_detalhe,           name="detalhe"),
    path("<slug:slug>/download/",                 views.mod_download,          name="download"),
    path("<slug:slug>/download/<int:version_id>/", views.mod_version_download, name="version_download"),
]
