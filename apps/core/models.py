from django.db import models
from django.utils.text import slugify


class Category(models.Model):

    class Icon(models.TextChoices):
        PUZZLE     = "puzzle",        "Puzzle"
        LAYERS     = "layers",        "Layers"
        TOOLS      = "tools",         "Tools"
        MAP        = "map",           "Map"
        IMAGE      = "image",         "Image"
        BOOK       = "book",          "Book"

    name        = models.CharField(max_length=50, unique=True)
    slug        = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon        = models.CharField(
                    max_length=30,
                    choices=Icon.choices,
                    default=Icon.PUZZLE,
                  )
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Categoria"
        verbose_name_plural = "Categorias"
        ordering            = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)