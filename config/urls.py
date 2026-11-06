from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Minecraft Archive"
admin.site.site_title  = "Minecraft Archive Admin"
admin.site.index_title = "Painel Administrativo"

urlpatterns = [
    path("mca-painel/",   admin.site.urls),
    path("",              include("apps.core.urls")),
    path("mods/",         include("apps.mods.urls")),
    path("modpacks/",     include("apps.modpacks.urls")),
    path("serverjars/",   include("apps.serverjars.urls")),
    path("worlds/",       include("apps.worlds.urls")),
    path("tutoriais/",    include("apps.tutorials.urls")),
    path("accounts/",     include("apps.accounts.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
