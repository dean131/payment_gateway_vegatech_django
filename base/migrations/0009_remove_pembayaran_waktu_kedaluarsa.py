# Generated by Django 3.2.23 on 2023-11-11 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_pembayaran_transaksi_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pembayaran',
            name='waktu_kedaluarsa',
        ),
    ]