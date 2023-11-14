from django.utils.crypto import get_random_string

from django.db import models
from django.conf import settings


def generate_id():
    return get_random_string(6)


class Pembelian(models.Model):
    STATUS_CHOICES = (
        ('keranjang', 'Keranjang'),
        ('menunggu', 'Menunggu'),

        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),

        ('dibatalkan', 'Dibatalkan'),
    )
    pembelian_id = models.CharField(max_length=20, default=generate_id, primary_key=True, editable=False)
    waktu_pembelian = models.DateTimeField(auto_now=True)
    status_pembelian = models.CharField(max_length=20, default='keranjang', choices=STATUS_CHOICES)
    total_harga_pembelian = models.IntegerField(default=0)
    total_berat = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pembelian_id)
    
    def save(self, *args, **kwargs):
        self.total_harga_pembelian = sum([item.total_harga_item for item in self.item_set.all()])
        self.total_berat = sum([item.produk.berat_produk * item.kuantitas  for item in self.item_set.all()])
        if self.item_set.all().count() == 0:
            self.delete()
        super().save(*args, **kwargs)
    

class Produk(models.Model):
    STOK_CHOICES = (
        ('tersedia', 'Tersedia'),
        ('habis', 'Habis'),
    )
    KATEGORI_CHOICES = (
        ('komputer', 'Komputer'),
        ('hardware', 'Hardware'),
        ('aksesoris', 'Aksesoris'),
    )
    produk_id = models.CharField(max_length=20, default=generate_id, primary_key=True, editable=False)
    nama_produk = models.CharField(max_length=200)
    deskripsi_produk = models.TextField(blank=True, null=True)
    harga_produk = models.IntegerField()
    berat_produk = models.IntegerField(blank=True, null=True)
    kategori_produk = models.CharField(max_length=200, choices=KATEGORI_CHOICES)
    stok_produk = models.CharField(max_length=200, default='tersedia', choices=STOK_CHOICES)
    gambar_produk = models.ImageField(upload_to='produk/', blank=True, null=True)

    def __str__(self):
        return self.nama_produk


class Item(models.Model):
    item_id = models.CharField(max_length=20, default=generate_id, primary_key=True, editable=False)
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    kuantitas = models.IntegerField(default=0)
    catatan = models.TextField(blank=True, null=True)
    total_harga_item = models.IntegerField(default=0)

    def __str__(self):
        return str(self.item_id)
    
    def save(self, *args, **kwargs):
        self.total_harga_item = self.kuantitas * self.produk.harga_produk
        super().save(*args, **kwargs)


class Pengiriman(models.Model):
    METODE_CHOICES = (
        ('jne', 'JNE'),
        ('ambil_sendiri', 'Ambil sendiri')
    )
    STATUS_CHOICES = (
        ('belum_dikirim', 'Belum dikirim'),
        ('belum_diambil', 'Belum diambil'),

        ('dikirim', 'Dikirim'),
        ('diterima', 'Diterima'),

        ('dibatalkan', 'Dibatalkan')
    )
    pengiriman_id = models.CharField(max_length=20, default=generate_id, primary_key=True, editable=False)
    pembelian = models.OneToOneField(Pembelian, on_delete=models.CASCADE)
    metode_pengiriman = models.CharField(max_length=20, choices=METODE_CHOICES)
    alamat_pengiriman = models.TextField(null=True, blank=True)
    status_pengiriman = models.CharField(max_length=20, choices=STATUS_CHOICES)
    no_resi = models.CharField(max_length=255, blank=True, null=True)
    ongkos_kirim = models.IntegerField(default=0)
    no_telp_penerima = models.CharField(max_length=255, blank=True, null=True)
    nama_penerima = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.pengiriman_id)


class Pembayaran(models.Model):
    STATUS_CHOICES = (
        ('belum_bayar', 'Belum bayar'),
        ('kadaluarsa', 'Kadaluarsa'),
        ('lunas', 'Lunas'),
        ('dibatalkan', 'Dibatalkan')
    )

    pembayaran_id = models.CharField(max_length=20, default=generate_id, primary_key=True, editable=False)
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    transaksi_id = models.CharField(max_length=255, blank=True, null=True)
    nama_bank = models.CharField(max_length=20)
    status_pembayaran = models.CharField(max_length=20, default='belum_bayar', choices=STATUS_CHOICES)
    waktu_pembayaran = models.DateTimeField(auto_now=True)
    no_va = models.CharField(max_length=255, blank=True, null=True)
    total_pembayaran = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pembayaran_id)

