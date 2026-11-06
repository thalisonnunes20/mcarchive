from django.db import models
import mimetypes
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, StreamingHttpResponse
from django.views.decorators.http import require_GET

from apps.core.models import Category
from .models import Mod, DownloadLog


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def mod_lista(request):
    mods       = Mod.objects.filter(is_published=True).select_related("category")
    categorias = Category.objects.all()

    return render(request, "mods/lista.html", {
        "mods":       mods,
        "categorias": categorias,
    })


def mod_detalhe(request, slug):
    mod          = get_object_or_404(Mod, slug=slug, is_published=True)
    versoes      = mod.versions.all().order_by("minecraft_version")
    relacionados = Mod.objects.filter(
        category=mod.category,
        is_published=True,
    ).exclude(pk=mod.pk)[:4]

    return render(request, "mods/detalhe.html", {
        "mod":          mod,
        "versoes":      versoes,
        "relacionados": relacionados,
    })

@require_GET
def mod_download(request, slug):
    mod = get_object_or_404(Mod, slug=slug, is_published=True)
    ip  = _get_client_ip(request)

    # Registra log e incrementa contador atomicamente
    DownloadLog.objects.create(mod=mod, ip_address=ip)
    Mod.objects.filter(pk=mod.pk).update(
        download_count=models.F("download_count") + 1
    )

    # Download de arquivo local
    if mod.has_local_file:
        caminho = mod.download_file.path

        if not os.path.exists(caminho):
            raise Http404("Arquivo não encontrado no servidor.")

        nome_arquivo  = os.path.basename(caminho)
        tipo_mime, _  = mimetypes.guess_type(caminho)
        tipo_mime     = tipo_mime or "application/octet-stream"

        response = FileResponse(
            open(caminho, "rb"),
            content_type=tipo_mime,
            as_attachment=True,
            filename=nome_arquivo,
        )

        # Header com tamanho para barra de progresso no browser
        response["Content-Length"] = os.path.getsize(caminho)
        return response

    # Redirect para link externo
    if mod.download_url:
        return redirect(mod.download_url)

    raise Http404("Nenhuma fonte de download disponível.")


def mod_por_categoria(request, slug):
    categoria  = get_object_or_404(Category, slug=slug)
    mods       = Mod.objects.filter(
                     category=categoria,
                     is_published=True,
                 ).select_related("category")
    categorias = Category.objects.all()

    return render(request, "mods/por_categoria.html", {
        "categoria":  categoria,
        "mods":       mods,
        "categorias": categorias,
    })

@require_GET
def mod_version_download(request, slug, version_id):
    from .models import ModVersion
    mod     = get_object_or_404(Mod, slug=slug, is_published=True)
    version = get_object_or_404(ModVersion, pk=version_id, mod=mod)
    ip      = _get_client_ip(request)

    DownloadLog.objects.create(mod=mod, ip_address=ip)
    Mod.objects.filter(pk=mod.pk).update(
        download_count=models.F("download_count") + 1
    )
    ModVersion.objects.filter(pk=version.pk).update(
        download_count=models.F("download_count") + 1
    )

    if version.has_local_file:
        caminho = version.download_file.path
        if not os.path.exists(caminho):
            raise Http404("Arquivo não encontrado no servidor.")
        nome_arquivo = os.path.basename(caminho)
        tipo_mime, _ = mimetypes.guess_type(caminho)
        tipo_mime    = tipo_mime or "application/octet-stream"
        response = FileResponse(
            open(caminho, "rb"),
            content_type=tipo_mime,
            as_attachment=True,
            filename=nome_arquivo,
        )
        response["Content-Length"] = os.path.getsize(caminho)
        return response

    if version.download_url:
        return redirect(version.download_url)

    raise Http404("Nenhuma fonte de download disponível para esta versão.")
