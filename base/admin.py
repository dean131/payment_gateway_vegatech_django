from django.contrib import admin

from . import models

class PembayaranAdmin(admin.ModelAdmin):
    list_display = ('pembayaran_id', 'nama_bank','status_pembayaran','waktu_pembayaran','no_va')
    list_filter = ('status_pembayaran',)
    search_fields = ('pembayaran_id', 'nama_bank','no_va')


class PengirimanAdmin(admin.ModelAdmin):
    list_display = ('pengiriman_id','metode_pengiriman', 'pembelian', 'status_pengiriman','no_resi', 'alamat_pengiriman')
    list_filter = ('status_pengiriman','metode_pengiriman')
    search_fields = ('pengiriman_id', 'no_resi')


class PembelianAdmin(admin.ModelAdmin):
    list_display = ('pembelian_id', 'user', 'waktu_pembelian','status_pembelian','total_harga_pembelian')
    list_filter = ('status_pembelian',)
    search_fields = ('pembelian_id', 'user__nama_lengkap', 'status_pembelian')


admin.site.register(models.Pembelian, PembelianAdmin)
admin.site.register(models.Produk)
admin.site.register(models.Item)
admin.site.register(models.Pengiriman, PengirimanAdmin)
admin.site.register(models.Pembayaran, PembayaranAdmin)

