import mimetypes
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET
from django.db import models

from apps.core.models import Category
from .models import World, WorldDownloadLog, WorldVersion


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def world_lista(request):
    worlds     = World.objects.filter(is_published=True).select_related("category")
    categorias = Category.objects.all()

    versao_sel = request.GET.get("versao", "")
    versoes = (
        World.objects.filter(is_published=True)
        .values_list("minecraft_version", flat=True)
        .distinct()
        .order_by("minecraft_version")
    )
    if versao_sel:
        worlds = worlds.filter(minecraft_version=versao_sel)

    return render(request, "worlds/lista.html", {
        "worlds":          worlds,
        "categorias":      categorias,
        "versoes":         versoes,
        "versao_sel":      versao_sel,
        "categoria_ativa": None,
    })


def world_detalhe(request, slug):
    world        = get_object_or_404(World, slug=slug, is_published=True)
    versoes      = world.versions.all().order_by("minecraft_version")
    relacionados = World.objects.filter(
        is_published=True
    ).exclude(pk=world.pk)[:4]

    return render(request, "worlds/detalhe.html", {
        "world":        world,
        "versoes":      versoes,
        "relacionados": relacionados,
    })


def world_por_categoria(request, slug):
    categoria  = get_object_or_404(Category, slug=slug)
    worlds     = World.objects.filter(
                     category=categoria,
                     is_published=True,
                 ).select_related("category")
    categorias = Category.objects.all()

    return render(request, "worlds/lista.html", {
        "worlds":          worlds,
        "categorias":      categorias,
        "versoes":         [],
        "versao_sel":      "",
        "categoria_ativa": categoria,
    })


@require_GET
def world_download(request, slug):
    world = get_object_or_404(World, slug=slug, is_published=True)
    ip    = _get_client_ip(request)

    WorldDownloadLog.objects.create(world=world, ip_address=ip)
    World.objects.filter(pk=world.pk).update(
        download_count=models.F("download_count") + 1
    )

    if world.has_local_file:
        caminho = world.download_file.path
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

    if world.download_url:
        return redirect(world.download_url)

    raise Http404("Nenhuma fonte de download disponível.")


@require_GET
def world_version_download(request, slug, version_id):
    world   = get_object_or_404(World, slug=slug, is_published=True)
    version = get_object_or_404(WorldVersion, pk=version_id, world=world)
    ip      = _get_client_ip(request)

    WorldDownloadLog.objects.create(world=world, ip_address=ip)
    World.objects.filter(pk=world.pk).update(
        download_count=models.F("download_count") + 1
    )
    WorldVersion.objects.filter(pk=version.pk).update(
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
