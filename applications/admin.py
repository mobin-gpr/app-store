from django.contrib import admin

from .models import (
    ApplicationLinkModel,
    ApplicationScreenShotModel,
    ApplicationModel,
    ApplicationImporterModel,
    ApplicationMainCaregoryModel,
    SuggestedAppsModel,
    AppsHelpModel,
    AppRequestModel,
    AppsCommentsModel,
)


class LinksInline(admin.TabularInline):
    model = ApplicationLinkModel


class ScreenShotInline(admin.TabularInline):
    model = ApplicationScreenShotModel


@admin.register(ApplicationModel)
class ModelNameAdmin(admin.ModelAdmin):
    inlines = [LinksInline, ScreenShotInline]
    list_display = ("title", "group", "main_caregory", "author", "is_active")
    list_editable = ("group", "main_caregory", "author", "is_active")
    search_fields = ("title",)
    list_filter = ("author", "group", "main_caregory", "is_active")


@admin.register(ApplicationImporterModel)
class ApplicationImporterModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

    readonly_fields = ("author",)


@admin.register(ApplicationMainCaregoryModel)
class ApplicationMainCaregoryModelAdmin(admin.ModelAdmin):
    list_display = ("category", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)


@admin.register(SuggestedAppsModel)
class SuggestedAppsModelAdmin(admin.ModelAdmin):
    list_display = ("suggestion", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)


@admin.register(AppsHelpModel)
class AppsHelpModelAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title",)
    list_filter = (
        "title",
        "is_active",
    )


@admin.register(AppRequestModel)
class AppRequestModelAdmin(admin.ModelAdmin):
    list_display = ("user", "app_link")


@admin.register(AppsCommentsModel)
class AppsCommentsModelAdmin(admin.ModelAdmin):
    list_display = ("app_title", "user_username", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)

    def user_username(self, obj):
        return obj.user.username

    def app_title(self, obj):
        return obj.app.title
