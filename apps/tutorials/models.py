from django.db import models
from django.utils.text import slugify
from apps.core.models import Category

class Tutorial(models.Model):

    title        = models.CharField(max_length=200)
    slug         = models.SlugField(max_length=220, unique=True, blank=True)
    content      = models.TextField()
    category     = models.ForeignKey(
                 Category,
                 on_delete=models.CASCADE,
                 related_name="tutorials",
                 null=True,
                 blank=True,
               )
    youtube_url  = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Tutorial"
        verbose_name_plural = "Tutoriais"
        ordering            = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def youtube_embed_url(self):
        """Converte URL do YouTube para formato embed."""
        if not self.youtube_url:
            return None
        url = self.youtube_url
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url


class TutorialImage(models.Model):

    tutorial = models.ForeignKey(
                 Tutorial,
                 on_delete=models.CASCADE,
                 related_name="images",
               )
    image   = models.ImageField(upload_to="tutorials/images/")
    caption = models.CharField(max_length=150, blank=True)
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name        = "Imagem do Tutorial"
        verbose_name_plural = "Imagens do Tutorial"
        ordering            = ["order"]

    def __str__(self):
        return f"Imagem {self.order} — {self.tutorial.title}"