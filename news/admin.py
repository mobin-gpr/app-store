from django.contrib import admin
from .models import NewsModel, TagsModel, NewsVisitModel, NewsCommentsModel


@admin.register(NewsModel)
class NewsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TagsModel)
class TagsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsVisitModel)
class NewsVisitAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsCommentsModel)
class NewsCommentsModelAdmin(admin.ModelAdmin):
    pass
