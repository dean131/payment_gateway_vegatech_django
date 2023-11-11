import uuid

from django.db import models
from django.conf import settings


class Pembelian(models.Model):
    STATUS_CHOICES = (
        ('keranjang', 'Keranjang'),
        ('belum_bayar', 'Belum bayar'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
    )
    pembelian_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    waktu_pembelian = models.DateTimeField(auto_now=True)
    status_pembelian = models.CharField(max_length=20, default='keranjang', choices=STATUS_CHOICES)
    total_harga_pembelian = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

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
    produk_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) 
    nama_produk = models.CharField(max_length=200)
    deskripsi_produk = models.TextField(blank=True, null=True)
    harga_produk = models.IntegerField()
    kategori_produk = models.CharField(max_length=200, choices=KATEGORI_CHOICES)
    stok_produk = models.CharField(max_length=200, default='tersedia', choices=STOK_CHOICES)
    gambar_produk = models.ImageField(upload_to='produk/', blank=True, null=True)


class Item(models.Model):
    item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    kuantitas = models.IntegerField(default=0)
    catatan = models.TextField(blank=True, null=True)
    total_harga_item = models.IntegerField(default=0)


class Pengiriman(models.Model):
    METODE_CHOICES = (
        ('jne', 'JNE'),
        ('ambil_sendiri', 'Ambil sendiri')
    )
    STATUS_CHOICES = (
        ('belum_dikirim', 'Belum dikirim'),
        ('dikirim', 'Dikirim'),
        ('diterima', 'Diterima'),
    )
    pengiriman_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    metode_pengiriman = models.CharField(max_length=20, choices=METODE_CHOICES)
    alamat_pengiriman = models.TextField()
    status_pengiriman = models.CharField(max_length=20, default='belum_dikirim', choices=STATUS_CHOICES)
    no_resi = models.CharField(max_length=255, blank=True, null=True)


class Pembayaran(models.Model):
    pembayaran_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    transaksi_id = models.CharField(max_length=255, blank=True, null=True)
    nama_bank = models.CharField(max_length=20)
    is_bayar = models.BooleanField(default=False)
    waktu_pembayaran = models.DateTimeField(auto_now=True)
    waktu_kedaluarsa = models.DateTimeField(blank=True, null=True)
    no_va = models.CharField(max_length=255, blank=True, null=True)

