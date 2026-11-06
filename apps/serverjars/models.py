import os
from apps.core.models import Category
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.mods.validators import (
    validar_extensao_mod,
    validar_tamanho_mod,
    validar_extensao_imagem,
    validar_tamanho_imagem,
)


class ServerJar(models.Model):

    class MCVersion(models.TextChoices):
        V1_0    = "1.0",    "1.0"
        V1_1    = "1.1",    "1.1"
        V1_2_5  = "1.2.5",  "1.2.5"
        V1_3_2  = "1.3.2",  "1.3.2"
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

    class ServerType(models.TextChoices):
        VANILLA  = "vanilla",  "Vanilla"
        CRAFTBUKKIT = "craftbukkit", "CraftBukkit"
        SPIGOT   = "spigot",   "Spigot"
        PAPER    = "paper",    "Paper"
        FORGE    = "forge",    "Forge"
        FABRIC   = "fabric",   "Fabric"
        SPONGE   = "sponge",   "Sponge"
        OTHER    = "other",    "Outro"

    title             = models.CharField(max_length=200)
    slug              = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    content           = models.TextField()
    minecraft_version = models.CharField(
                          max_length=20,
                          choices=MCVersion.choices,
                          default=MCVersion.V1_7_10,
                        )
    server_type       = models.CharField(
                        max_length=20,
                        choices=ServerType.choices,
                        default=ServerType.VANILLA,
                        )
    category          = models.ForeignKey(          # ← adicionar
                        Category,
                        on_delete=models.CASCADE,
                        related_name="serverjars",
                        null=True,
                        blank=True,
                        )
    cover_image       = models.ImageField(
                          upload_to="serverjars/covers/",
                          validators=[
                              validar_extensao_imagem,
                              validar_tamanho_imagem,
                          ],
                        )
    download_file     = models.FileField(
                          upload_to="serverjars/files/",
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
        verbose_name        = "Server Jar"
        verbose_name_plural = "Server Jars"
        ordering            = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.minecraft_version} — {self.server_type})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.download_file and not self.download_url:
            raise ValidationError(
                "Informe ao menos um arquivo para download ou um link externo."
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


class ServerJarDownloadLog(models.Model):

    serverjar     = models.ForeignKey(
                      ServerJar,
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
        return f"{self.serverjar.title} — {self.ip_address} — {self.downloaded_at:%d/%m/%Y %H:%M}"

class ServerJarVersion(models.Model):

    serverjar         = models.ForeignKey(
                          ServerJar,
                          on_delete=models.CASCADE,
                          related_name="versions",
                        )
    minecraft_version = models.CharField(
                          max_length=20,
                          choices=ServerJar.MCVersion.choices,
                        )
    server_type       = models.CharField(
                          max_length=20,
                          choices=ServerJar.ServerType.choices,
                          default=ServerJar.ServerType.VANILLA,
                        )
    download_file     = models.FileField(
                          upload_to="serverjars/files/",
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
        verbose_name        = "Versão do Server Jar"
        verbose_name_plural = "Versões do Server Jar"
        ordering            = ["minecraft_version"]
        unique_together     = ("serverjar", "minecraft_version", "server_type")

    def __str__(self):
        return f"{self.serverjar.title} — {self.minecraft_version} ({self.server_type})"

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


@receiver(post_delete, sender=ServerJarVersion)
def deletar_arquivos_serverjarversion(sender, instance, **kwargs):
    if instance.download_file:
        try:
            instance.download_file.delete(save=False)
        except Exception:
            pass

@receiver(post_delete, sender=ServerJar)
def deletar_arquivos_serverjar(sender, instance, **kwargs):
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