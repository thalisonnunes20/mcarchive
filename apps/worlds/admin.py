from django.contrib import admin
from django.utils.html import format_html

from .models import World, WorldDownloadLog, WorldVersion


class WorldVersionInline(admin.TabularInline):
    model   = WorldVersion
    extra   = 1
    fields  = ("minecraft_version", "download_file", "download_url", "download_count")
    readonly_fields = ("download_count",)


class DownloadLogInline(admin.TabularInline):
    model           = WorldDownloadLog
    extra           = 0
    readonly_fields = ("ip_address", "downloaded_at")
    can_delete      = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display  = (
        "title",
        "category",
        "minecraft_version",
        "world_author",
        "download_count",
        "is_published",
        "created_at",
    )
    list_filter   = ("is_published", "minecraft_version", "category")
    search_fields = ("title", "world_author", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("download_count", "created_at", "updated_at", "cover_preview")
    ordering = ("-created_at",)
    inlines  = [WorldVersionInline, DownloadLogInline]

    fieldsets = (
        ("Informações Principais", {
            "fields": (
                "title",
                "slug",
                "category",
                "world_author",
                "minecraft_version",
                "is_published",
            )
        }),
        ("Conteúdo", {
            "fields": (
                "short_description",
                "content",
            )
        }),
        ("Imagem de Capa", {
            "fields": (
                "cover_image",
                "cover_preview",
            )
        }),
        ("Download Principal", {
            "fields": (
                "download_file",
                "download_url",
                "download_count",
            ),
            "description": "Download padrão quando não há versões adicionais cadastradas.",
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Pré-visualização")
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height:120px; border-radius:6px;">',
                obj.cover_image.url,
            )
        return "—"


@admin.register(WorldDownloadLog)
class WorldDownloadLogAdmin(admin.ModelAdmin):
    list_display    = ("world", "ip_address", "downloaded_at")
    list_filter     = ("downloaded_at",)
    search_fields   = ("world__title", "ip_address")
    readonly_fields = ("world", "ip_address", "downloaded_at")
    ordering        = ("-downloaded_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
