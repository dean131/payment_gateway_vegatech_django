from rest_framework import serializers

from base import models


class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Produk
        fields = '__all__'


class PembelianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pembelian
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class PengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pengiriman
        fields = '__all__'