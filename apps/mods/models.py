import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.core.models import Category
from .validators import (
    validar_extensao_mod,
    validar_tamanho_mod,
    validar_extensao_imagem,
    validar_tamanho_imagem,
)


class Mod(models.Model):

    class MCVersion(models.TextChoices):
        V1_4_7  = "1.4.7",  "1.4.7"
        V1_5_2  = "1.5.2",  "1.5.2"
        V1_6_4  = "1.6.4",  "1.6.4"
        V1_7_2  = "1.7.2",  "1.7.2"
        V1_7_10 = "1.7.10", "1.7.10"
        V1_8    = "1.8",    "1.8"
        V1_8_9  = "1.8.9",  "1.8.9"
        V1_9_4  = "1.9.4",  "1.9.4"
        V1_10_2 = "1.10.2", "1.10.2"
        V1_12_2 = "1.12.2", "1.12.2"
        V1_16_5 = "1.16.5", "1.16.5"

    title             = models.CharField(max_length=200)
    slug              = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    content           = models.TextField()
    minecraft_version = models.CharField(
                          max_length=20,
                          choices=MCVersion.choices,
                          default=MCVersion.V1_7_10,
                        )
    mod_author        = models.CharField(max_length=100)
    category          = models.ForeignKey(
                          Category,
                          on_delete=models.CASCADE,
                          related_name="mods",
                        )
    cover_image       = models.ImageField(
                          upload_to="mods/covers/",
                          validators=[
                              validar_extensao_imagem,
                              validar_tamanho_imagem,
                          ],
                        )
    download_file     = models.FileField(
                          upload_to="mods/files/",
                          blank=True,
                          null=True,
                          validators=[
                              validar_extensao_mod,
                              validar_tamanho_mod,
                          ],
                        )
    download_url      = models.URLField(blank=True)
    download_count    = models.PositiveIntegerField(default=0)
    is_published      = models.BooleanField(default=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Mod"
        verbose_name_plural = "Mods"
        ordering            = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.minecraft_version})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.download_file and not self.download_url:
            if not self.pk:
                raise ValidationError(
                    "Informe ao menos um arquivo para download ou um link externo. "
                    "Você pode adicionar versões específicas após salvar o mod."
                )
            if not self.versions.exists():
                raise ValidationError(
                    "Informe ao menos um arquivo para download, um link externo, "
                    "ou adicione versões na seção 'Versões do Mod'."
                )

    @property
    def has_local_file(self):
        return bool(self.download_file)

    @property
    def nome_arquivo(self):
        if self.download_file:
            return os.path.basename(self.download_file.name)
        return None

    @property
    def tamanho_arquivo_mb(self):
        if self.download_file:
            try:
                return round(self.download_file.size / (1024 * 1024), 2)
            except (FileNotFoundError, OSError):
                return None
        return None


class DownloadLog(models.Model):

    mod           = models.ForeignKey(
                      Mod,
                      on_delete=models.CASCADE,
                      related_name="download_logs",
                    )
    ip_address    = models.GenericIPAddressField()
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Log de Download"
        verbose_name_plural = "Logs de Download"
        ordering            = ["-downloaded_at"]

    def __str__(self):
        return f"{self.mod.title} — {self.ip_address} — {self.downloaded_at:%d/%m/%Y %H:%M}"
    
class ModVersion(models.Model):

    mod               = models.ForeignKey(
                          Mod,
                          on_delete=models.CASCADE,
                          related_name="versions",
                        )
    minecraft_version = models.CharField(
                          max_length=20,
                          choices=Mod.MCVersion.choices,
                        )
    download_file     = models.FileField(
                          upload_to="mods/files/",
                          blank=True,
                          null=True,
                          validators=[
                              validar_extensao_mod,
                              validar_tamanho_mod,
                          ],
                        )
    download_url      = models.URLField(blank=True)
    download_count    = models.PositiveIntegerField(default=0)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Versão do Mod"
        verbose_name_plural = "Versões do Mod"
        ordering            = ["minecraft_version"]
        unique_together     = ("mod", "minecraft_version")

    def __str__(self):
        return f"{self.mod.title} — {self.minecraft_version}"

    def clean(self):
        if not self.download_file and not self.download_url:
            raise ValidationError(
                "Informe ao menos um arquivo ou link para esta versão."
            )

    @property
    def has_local_file(self):
        return bool(self.download_file)

    @property
    def nome_arquivo(self):
        if self.download_file:
            return os.path.basename(self.download_file.name)
        return None

    @property
    def tamanho_arquivo_mb(self):
        if self.download_file:
            try:
                return round(self.download_file.size / (1024 * 1024), 2)
            except (FileNotFoundError, OSError):
                return None
        return None


@receiver(post_delete, sender=ModVersion)
def deletar_arquivos_modversion(sender, instance, **kwargs):
    if instance.download_file:
        try:
            instance.download_file.delete(save=False)
        except Exception:
            pass
    
@receiver(post_delete, sender=Mod)
def deletar_arquivos_mod(sender, instance, **kwargs):
    if instance.cover_image:
        try:
            instance.cover_image.delete(save=False)
        except Exception:
            pass

    if instance.download_file:
        try:
            instance.download_file.delete(save=False)
        except Exception:
            pass