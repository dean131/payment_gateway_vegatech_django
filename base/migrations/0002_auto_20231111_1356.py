# Generated by Django 3.2.23 on 2023-11-11 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='kuantitas',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='total_harga_item',
            field=models.IntegerField(default=0),
        ),
    ]