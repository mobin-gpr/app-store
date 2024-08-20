from django.contrib import admin
from .models import FooterModel, LogoModel


@admin.register(FooterModel)
class FooterModelAdmin(admin.ModelAdmin):
    pass


@admin.register(LogoModel)
class LogoModelAdmin(admin.ModelAdmin):
    pass
