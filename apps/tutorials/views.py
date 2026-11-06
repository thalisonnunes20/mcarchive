from django.shortcuts import render, get_object_or_404

from apps.core.models import Category
from .models import Tutorial


def tutorial_lista(request):
    tutoriais  = Tutorial.objects.filter(is_published=True)
    categorias = Category.objects.all()

    return render(request, "tutorials/lista.html", {
        "tutoriais":       tutoriais,
        "categorias":      categorias,
        "categoria_ativa": None,
    })


def tutorial_detalhe(request, slug):
    tutorial     = get_object_or_404(Tutorial, slug=slug, is_published=True)
    imagens      = tutorial.images.all()
    relacionados = Tutorial.objects.filter(
        is_published=True
    ).exclude(pk=tutorial.pk)[:3]

    return render(request, "tutorials/detalhe.html", {
        "tutorial":     tutorial,
        "imagens":      imagens,
        "relacionados": relacionados,
    })


def tutorial_por_categoria(request, slug):
    categoria  = get_object_or_404(Category, slug=slug)
    tutoriais  = Tutorial.objects.filter(
                     category=categoria,
                     is_published=True,
                 )
    categorias = Category.objects.all()

    return render(request, "tutorials/lista.html", {
        "tutoriais":       tutoriais,
        "categorias":      categorias,
        "categoria_ativa": categoria,
    })
