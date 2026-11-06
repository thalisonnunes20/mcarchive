import mimetypes
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET
from django.db import models

from apps.core.models import Category
from .models import Modpack, ModpackDownloadLog


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def modpack_lista(request):
    modpacks   = Modpack.objects.filter(is_published=True).select_related("category")
    categorias = Category.objects.all()
    versoes    = (
        Modpack.objects.filter(is_published=True)
        .values_list("minecraft_version", flat=True)
        .distinct()
        .order_by("minecraft_version")
    )
    versao_sel = request.GET.get("versao", "")
    if versao_sel:
        modpacks = modpacks.filter(minecraft_version=versao_sel)

    return render(request, "modpacks/lista.html", {
        "modpacks":   modpacks,
        "categorias": categorias,
        "versoes":    versoes,
        "versao_sel": versao_sel,
    })


def modpack_detalhe(request, slug):
    modpack      = get_object_or_404(Modpack, slug=slug, is_published=True)
    relacionados = Modpack.objects.filter(
        is_published=True
    ).exclude(pk=modpack.pk)[:4]

    return render(request, "modpacks/detalhe.html", {
        "modpack":      modpack,
        "relacionados": relacionados,
    })


def modpack_por_categoria(request, slug):
    categoria  = get_object_or_404(Category, slug=slug)
    modpacks   = Modpack.objects.filter(
                     category=categoria,
                     is_published=True,
                 ).select_related("category")
    categorias = Category.objects.all()

    return render(request, "modpacks/lista.html", {
        "modpacks":       modpacks,
        "categorias":     categorias,
        "categoria_ativa": categoria,
        "versoes":        [],
        "versao_sel":     "",
    })


@require_GET
def modpack_download(request, slug):
    modpack = get_object_or_404(Modpack, slug=slug, is_published=True)
    ip      = _get_client_ip(request)

    ModpackDownloadLog.objects.create(modpack=modpack, ip_address=ip)
    Modpack.objects.filter(pk=modpack.pk).update(
        download_count=models.F("download_count") + 1
    )

    if modpack.has_local_file:
        caminho = modpack.download_file.path
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

    if modpack.download_url:
        return redirect(modpack.download_url)

    raise Http404("Nenhuma fonte de download disponível.")