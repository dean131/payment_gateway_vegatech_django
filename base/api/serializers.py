from rest_framework import serializers

from account.api.serializers import UserModelSerializer

from base import models


class ProdukModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Produk
        fields = '__all__'


class PengirimanModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pengiriman
        fields = '__all__'


class PembelianModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    pengiriman = serializers.SerializerMethodField('get_pengiriman')
    class Meta:
        model = models.Pembelian
        fields = '__all__'

    def get_pengiriman(self, obj):
        if obj.status_pembelian == 'keranjang':
            return None
        pengiriman = models.Pengiriman.objects.filter(pembelian=obj).first()
        serializer = PengirimanModelSerializer(pengiriman)
        return serializer.data


class ItemModelSerializer(serializers.ModelSerializer):
    produk = ProdukModelSerializer()
    class Meta:
        model = models.Item
        fields = '__all__'


class PembayaranModelSerializer(serializers.ModelSerializer):
    pembelian = PembelianModelSerializer()
    class Meta:
        model = models.Pembayaran
        fields = '__all__'