from django.contrib import admin

from . import models

class PembayaranAdmin(admin.ModelAdmin):
    list_display = ('pembayaran_id', 'waktu_pembayaran', 'status_pembayaran')
    list_filter = ('status_pembayaran',)
    search_fields = ('pembayaran_id', 'user__username', 'user__email')
    ordering = ('-waktu_pembayaran',)


admin.site.register(models.Pembelian)
admin.site.register(models.Produk)
admin.site.register(models.Item)
admin.site.register(models.Pengiriman)
admin.site.register(models.Pembayaran, PembayaranAdmin)
