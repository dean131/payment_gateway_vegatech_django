# Generated by Django 3.2.23 on 2023-11-11 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20231111_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produk',
            name='kategori_produk',
            field=models.CharField(choices=[('komputer', 'Komputer'), ('hardware', 'Hardware'), ('aksesoris', 'Aksesoris')], max_length=200),
        ),
    ]
