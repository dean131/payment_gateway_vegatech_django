import uuid

from django.db import models
from django.conf import settings


class Pembelian(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    waktu_pembelian = models.DateTimeField(auto_now_add=True)
    status_pembelian = models.CharField(max_length=20, default='pending')
    total_harga_pembelian = models.IntegerField(blank=True, null=True)
    

class Produk(models.Model):
    nama_produk = models.CharField(max_length=200)
    deskripsi_produk = models.TextField(blank=True, null=True)
    harga_produk = models.IntegerField()
    kategori_produk = models.CharField(max_length=200)
    gambar_produk = models.ImageField(upload_to='produk/', blank=True, null=True)


class Item(models.Model):
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    kuantitas = models.IntegerField()
    catatan = models.TextField(blank=True, null=True)
    total_harga_item = models.IntegerField()


class Pengiriman(models.Model):
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    metode_pengiriman = models.CharField(max_length=20)
    alamat_pengiriman = models.TextField()
    status_pengiriman = models.CharField(max_length=20, default='pending')
    no_resi = models.CharField(max_length=255, blank=True, null=True)


class Pembayaran(models.Model):
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    nama_bank = models.CharField(max_length=20)
    status_pembayaran = models.CharField(max_length=20, default='pending')
    waktu_pembayaran = models.DateTimeField(auto_now_add=True)
    no_va = models.CharField(max_length=255, blank=True, null=True)

