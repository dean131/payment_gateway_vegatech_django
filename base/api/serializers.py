from rest_framework import serializers

from base import models


class ProdukModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Produk
        fields = '__all__'


class PembelianModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pembelian
        fields = '__all__'


class ItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class PengirimanModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pengiriman
        fields = '__all__'


class PembayaranModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pembayaran
        fields = '__all__'