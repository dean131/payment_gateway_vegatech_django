from django.contrib import admin
from . import models


class UserModelAdmin(admin.ModelAdmin):
    list_display = ("user_id", "nama_lengkap", "email", "is_admin")
    search_fields = ("user_id", "nama_lengkap", "email", "is_admin")


admin.site.register(models.User, UserModelAdmin)
