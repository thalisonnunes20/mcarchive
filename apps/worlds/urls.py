from django.urls import path
from . import views

app_name = "worlds"

urlpatterns = [
    path("",                                       views.world_lista,            name="lista"),
    path("categoria/<slug:slug>/",                 views.world_por_categoria,    name="por_categoria"),
    path("<slug:slug>/",                           views.world_detalhe,          name="detalhe"),
    path("<slug:slug>/download/",                  views.world_download,         name="download"),
    path("<slug:slug>/download/<int:version_id>/", views.world_version_download, name="version_download"),
]
