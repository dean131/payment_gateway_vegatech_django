from django.contrib import admin

from . import models


admin.site.register(models.Pembelian)
admin.site.register(models.Produk)
admin.site.register(models.Item)
admin.site.register(models.Pengiriman)
