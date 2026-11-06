from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from apps.mods.models import Mod
from apps.modpacks.models import Modpack
from apps.serverjars.models import ServerJar
from apps.worlds.models import World
from apps.tutorials.models import Tutorial
from apps.core.models import Category


def home(request):
    mods_recentes      = Mod.objects.filter(is_published=True).select_related("category")[:3]
    modpacks_recentes  = Modpack.objects.filter(is_published=True)[:3]
    jars_recentes      = ServerJar.objects.filter(is_published=True)[:3]
    worlds_recentes    = World.objects.filter(is_published=True)[:3]
    tutoriais_recentes = Tutorial.objects.filter(is_published=True)[:3]
    categorias         = Category.objects.all()

    recentes = []

    for mod in mods_recentes:
        recentes.append({
            "titulo":    mod.title,
            "versao":    mod.minecraft_version,
            "downloads": mod.download_count,
            "capa":      mod.cover_image,
            "url":       f"/mods/{mod.slug}/",
            "tipo":      "Mod",
        })

    for mp in modpacks_recentes:
        recentes.append({
            "titulo":    mp.title,
            "versao":    mp.minecraft_version,
            "downloads": mp.download_count,
            "capa":      mp.cover_image,
            "url":       f"/modpacks/{mp.slug}/",
            "tipo":      "Modpack",
        })

    for jar in jars_recentes:
        recentes.append({
            "titulo":    jar.title,
            "versao":    jar.minecraft_version,
            "downloads": jar.download_count,
            "capa":      jar.cover_image,
            "url":       f"/serverjars/{jar.slug}/",
            "tipo":      "Server Jar",
        })

    for world in worlds_recentes:
        recentes.append({
            "titulo":    world.title,
            "versao":    world.minecraft_version,
            "downloads": world.download_count,
            "capa":      world.cover_image,
            "url":       f"/worlds/{world.slug}/",
            "tipo":      "World",
        })

    recentes = recentes[:6]

    return render(request, "core/home.html", {
        "recentes":           recentes,
        "tutoriais_recentes": tutoriais_recentes,
        "categorias":         categorias,
    })


def busca(request):
    query = request.GET.get("q", "").strip()

    mods       = Mod.objects.none()
    modpacks   = Modpack.objects.none()
    serverjars = ServerJar.objects.none()
    worlds     = World.objects.none()
    tutoriais  = Tutorial.objects.none()

    if query:
        mods = Mod.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(mod_author__icontains=query) |
            Q(content__icontains=query)
        ).select_related("category")

        modpacks = Modpack.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(pack_author__icontains=query) |
            Q(content__icontains=query)
        )

        serverjars = ServerJar.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(content__icontains=query)
        )

        worlds = World.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(world_author__icontains=query) |
            Q(content__icontains=query)
        )

        tutoriais = Tutorial.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    paginator_mods = Paginator(mods, 9)
    mods_paginados = paginator_mods.get_page(request.GET.get("page_mods", 1))

    paginator_mp = Paginator(modpacks, 9)
    mp_paginados = paginator_mp.get_page(request.GET.get("page_mp", 1))

    paginator_jars = Paginator(serverjars, 9)
    jars_paginados = paginator_jars.get_page(request.GET.get("page_jars", 1))

    paginator_worlds = Paginator(worlds, 9)
    worlds_paginados = paginator_worlds.get_page(request.GET.get("page_worlds", 1))

    paginator_tut = Paginator(tutoriais, 6)
    tut_paginados = paginator_tut.get_page(request.GET.get("page_tut", 1))

    return render(request, "core/busca.html", {
        "query":            query,
        "mods":             mods_paginados,
        "modpacks":         mp_paginados,
        "serverjars":       jars_paginados,
        "worlds":           worlds_paginados,
        "tutoriais":        tut_paginados,
        "total_mods":       paginator_mods.count,
        "total_modpacks":   paginator_mp.count,
        "total_serverjars": paginator_jars.count,
        "total_worlds":     paginator_worlds.count,
        "total_tutoriais":  paginator_tut.count,
    })

