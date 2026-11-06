from django.contrib import admin
from django.utils.html import format_html

from .models import ServerJar, ServerJarDownloadLog


class DownloadLogInline(admin.TabularInline):
    model           = ServerJarDownloadLog
    extra           = 0
    readonly_fields = ("ip_address", "downloaded_at")
    can_delete      = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ServerJar)
class ServerJarAdmin(admin.ModelAdmin):
    list_display  = (
        "title",
        "minecraft_version",
        "server_type",
        "download_count",
        "is_published",
        "created_at",
    )
    list_filter   = ("is_published", "minecraft_version", "server_type")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("download_count", "created_at", "updated_at", "cover_preview")
    ordering = ("-created_at",)
    inlines  = [DownloadLogInline]

    fieldsets = (
        ("Informações Principais", {
            "fields": (
                "title",
                "slug",
                "minecraft_version",
                "server_type",
                "category",
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
        ("Download", {
            "fields": (
                "download_file",
                "download_url",
                "download_count",
            )
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


@admin.register(ServerJarDownloadLog)
class ServerJarDownloadLogAdmin(admin.ModelAdmin):
    list_display    = ("serverjar", "ip_address", "downloaded_at")
    list_filter     = ("downloaded_at",)
    search_fields   = ("serverjar__title", "ip_address")
    readonly_fields = ("serverjar", "ip_address", "downloaded_at")
    ordering        = ("-downloaded_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
