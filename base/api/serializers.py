from rest_framework import serializers

from account.api.serializers import UserModelSerializer

from base import models


class ProdukModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Produk
        fields = '__all__'


class PembelianModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    class Meta:
        model = models.Pembelian
        fields = '__all__'


class ItemModelSerializer(serializers.ModelSerializer):
    produk = ProdukModelSerializer()
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