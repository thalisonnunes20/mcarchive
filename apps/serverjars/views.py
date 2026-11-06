import mimetypes
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET
from django.db import models

from apps.core.models import Category
from .models import ServerJar, ServerJarDownloadLog


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def serverjar_lista(request):
    serverjars = ServerJar.objects.filter(is_published=True)
    categorias = Category.objects.all()

    versao_sel = request.GET.get("versao", "")
    tipo_sel   = request.GET.get("tipo", "")

    versoes = (
        ServerJar.objects.filter(is_published=True)
        .values_list("minecraft_version", flat=True)
        .distinct()
        .order_by("minecraft_version")
    )
    tipos = (
        ServerJar.objects.filter(is_published=True)
        .values_list("server_type", flat=True)
        .distinct()
        .order_by("server_type")
    )

    if versao_sel:
        serverjars = serverjars.filter(minecraft_version=versao_sel)
    if tipo_sel:
        serverjars = serverjars.filter(server_type=tipo_sel)

    return render(request, "serverjars/lista.html", {
        "serverjars":     serverjars,
        "categorias":     categorias,
        "versoes":        versoes,
        "tipos":          tipos,
        "versao_sel":     versao_sel,
        "tipo_sel":       tipo_sel,
        "categoria_ativa": None,
    })


def serverjar_detalhe(request, slug):
    serverjar    = get_object_or_404(ServerJar, slug=slug, is_published=True)
    relacionados = ServerJar.objects.filter(
        is_published=True,
        minecraft_version=serverjar.minecraft_version,
    ).exclude(pk=serverjar.pk)[:4]

    return render(request, "serverjars/detalhe.html", {
        "serverjar":    serverjar,
        "relacionados": relacionados,
    })


def serverjar_por_categoria(request, slug):
    categoria  = get_object_or_404(Category, slug=slug)
    serverjars = ServerJar.objects.filter(
                     category=categoria,
                     is_published=True,
                 )
    categorias = Category.objects.all()

    return render(request, "serverjars/lista.html", {
        "serverjars":      serverjars,
        "categorias":      categorias,
        "versoes":         [],
        "tipos":           [],
        "versao_sel":      "",
        "tipo_sel":        "",
        "categoria_ativa": categoria,
    })


@require_GET
def serverjar_download(request, slug):
    serverjar = get_object_or_404(ServerJar, slug=slug, is_published=True)
    ip        = _get_client_ip(request)

    ServerJarDownloadLog.objects.create(serverjar=serverjar, ip_address=ip)
    ServerJar.objects.filter(pk=serverjar.pk).update(
        download_count=models.F("download_count") + 1
    )

    if serverjar.has_local_file:
        caminho = serverjar.download_file.path
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

    if serverjar.download_url:
        return redirect(serverjar.download_url)

    raise Http404("Nenhuma fonte de download disponível.")