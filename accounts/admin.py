from django.contrib import admin
from .models import User, AvatarImagesModel


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(AvatarImagesModel)
class AvatarImagesModelAdmin(admin.ModelAdmin):
    pass
