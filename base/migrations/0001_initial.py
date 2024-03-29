# Generated by Django 3.2.23 on 2023-11-14 12:16

import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pembelian',
            fields=[
                ('pembelian_id', models.CharField(default=base.models.generate_id, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('waktu_pembelian', models.DateTimeField(auto_now=True)),
                ('status_pembelian', models.CharField(choices=[('keranjang', 'Keranjang'), ('menunggu', 'Menunggu'), ('diproses', 'Diproses'), ('selesai', 'Selesai'), ('dibatalkan', 'Dibatalkan')], default='keranjang', max_length=20)),
                ('total_harga_pembelian', models.IntegerField(default=0)),
                ('total_berat', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('produk_id', models.CharField(default=base.models.generate_id, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('nama_produk', models.CharField(max_length=200)),
                ('deskripsi_produk', models.TextField(blank=True, null=True)),
                ('harga_produk', models.IntegerField()),
                ('berat_produk', models.IntegerField(blank=True, null=True)),
                ('kategori_produk', models.CharField(choices=[('komputer', 'Komputer'), ('hardware', 'Hardware'), ('aksesoris', 'Aksesoris')], max_length=200)),
                ('stok_produk', models.CharField(choices=[('tersedia', 'Tersedia'), ('habis', 'Habis')], default='tersedia', max_length=200)),
                ('gambar_produk', models.ImageField(blank=True, null=True, upload_to='produk/')),
            ],
        ),
        migrations.CreateModel(
            name='Pengiriman',
            fields=[
                ('pengiriman_id', models.CharField(default=base.models.generate_id, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('metode_pengiriman', models.CharField(choices=[('jne', 'JNE'), ('ambil_sendiri', 'Ambil sendiri')], max_length=20)),
                ('alamat_pengiriman', models.TextField(blank=True, null=True)),
                ('status_pengiriman', models.CharField(choices=[('belum_dikirim', 'Belum dikirim'), ('belum_diambil', 'Belum diambil'), ('dikirim', 'Dikirim'), ('diterima', 'Diterima'), ('dibatalkan', 'Dibatalkan')], max_length=20)),
                ('no_resi', models.CharField(blank=True, max_length=255, null=True)),
                ('ongkos_kirim', models.IntegerField(default=0)),
                ('no_telp_penerima', models.CharField(blank=True, max_length=255, null=True)),
                ('nama_penerima', models.CharField(blank=True, max_length=255, null=True)),
                ('pembelian', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.pembelian')),
            ],
        ),
        migrations.CreateModel(
            name='Pembayaran',
            fields=[
                ('pembayaran_id', models.CharField(default=base.models.generate_id, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('transaksi_id', models.CharField(blank=True, max_length=255, null=True)),
                ('nama_bank', models.CharField(max_length=20)),
                ('status_pembayaran', models.CharField(choices=[('belum_bayar', 'Belum bayar'), ('kadaluarsa', 'Kadaluarsa'), ('lunas', 'Lunas'), ('dibatalkan', 'Dibatalkan')], default='belum_bayar', max_length=20)),
                ('waktu_pembayaran', models.DateTimeField(auto_now=True)),
                ('no_va', models.CharField(blank=True, max_length=255, null=True)),
                ('total_pembayaran', models.IntegerField(default=0)),
                ('pembelian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.pembelian')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.CharField(default=base.models.generate_id, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('kuantitas', models.IntegerField(default=0)),
                ('catatan', models.TextField(blank=True, null=True)),
                ('total_harga_item', models.IntegerField(default=0)),
                ('pembelian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.pembelian')),
                ('produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.produk')),
            ],
        ),
    ]
