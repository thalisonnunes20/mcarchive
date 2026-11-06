from django.contrib import admin
from django.utils.html import format_html

from .models import Modpack, ModpackDownloadLog


class DownloadLogInline(admin.TabularInline):
    model           = ModpackDownloadLog
    extra           = 0
    readonly_fields = ("ip_address", "downloaded_at")
    can_delete      = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Modpack)
class ModpackAdmin(admin.ModelAdmin):
    list_display  = (
        "title", "minecraft_version", "pack_author",
        "download_count", "is_published", "created_at",
    )
    list_filter   = ("is_published", "minecraft_version")
    search_fields = ("title", "pack_author", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("download_count", "created_at", "updated_at", "cover_preview")
    ordering = ("-created_at",)
    inlines  = [DownloadLogInline]

    fieldsets = (
        ("Informações Principais", {
            "fields": 
            (
                "title",
                "slug",
                "pack_author",
                "category",           # ← adicionar
                "minecraft_version",
                "is_published",
            )
        }),
        ("Conteúdo", {
            "fields": ("short_description", "content")
        }),
        ("Imagem de Capa", {
            "fields": ("cover_image", "cover_preview")
        }),
        ("Download", {
            "fields": ("download_file", "download_url", "download_count")
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at"),
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


@admin.register(ModpackDownloadLog)
class ModpackDownloadLogAdmin(admin.ModelAdmin):
    list_display  = ("modpack", "ip_address", "downloaded_at")
    list_filter   = ("downloaded_at",)
    search_fields = ("modpack__title", "ip_address")
    readonly_fields = ("modpack", "ip_address", "downloaded_at")
    ordering = ("-downloaded_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False