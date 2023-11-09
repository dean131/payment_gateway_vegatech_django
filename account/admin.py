from django.contrib import admin
from . import models


class UserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "nama_lengkap", "email", "is_admin")
    search_fields = ("id", "nama_lengkap", "email", "is_admin")


admin.site.register(models.User, UserModelAdmin)
