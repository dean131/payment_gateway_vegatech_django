# Generated by Django 3.2.23 on 2023-11-10 23:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('nama_lengkap', models.CharField(max_length=255)),
                ('jenis_kelamin', models.CharField(max_length=255)),
                ('tanggal_lahir', models.DateField(blank=True, null=True)),
                ('no_telepon', models.CharField(max_length=25)),
                ('foto_profil', models.ImageField(blank=True, null=True, upload_to='foto_profil')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
