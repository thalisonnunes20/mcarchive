from django.contrib import admin

from .models import Tutorial, TutorialImage


class TutorialImageInline(admin.TabularInline):
    model   = TutorialImage
    extra   = 1
    fields  = ("image", "caption", "order")
    ordering = ("order",)


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display  = ("title", "category", "is_published", "created_at", "updated_at")
    list_filter   = ("is_published", "category")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines  = [TutorialImageInline]

    fieldsets = (
        ("Informações Principais", {
            "fields": (
                "title",
                "slug",
                "category",
                "is_published",
            )
        }),
        ("Conteúdo", {
            "fields": (
                "content",
                "youtube_url",
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


@admin.register(TutorialImage)
class TutorialImageAdmin(admin.ModelAdmin):
    list_display = ("tutorial", "caption", "order")
    list_filter  = ("tutorial",)
    ordering     = ("tutorial", "order")
