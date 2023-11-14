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
    user = serializers.SerializerMethodField('get_user')
    pengiriman = serializers.SerializerMethodField('get_pengiriman')
    pembayaran = serializers.SerializerMethodField('get_pembayaran')
    class Meta:
        model = models.Pembelian
        fields = '__all__'

    def get_user(self, obj):
        serializer = UserModelSerializer(obj.user, context=self.context)
        return serializer.data

    def get_pengiriman(self, obj):
        if obj.status_pembelian == 'keranjang':
            return None
        pengiriman = models.Pengiriman.objects.filter(pembelian=obj).first()
        serializer = PengirimanModelSerializer(pengiriman)
        return serializer.data
    
    def get_pembayaran(self, obj):
        pembayaran = obj.pembayaran_set.first()
        serializer = PembayaranSerializer(pembayaran)
        return serializer.data


class ItemModelSerializer(serializers.ModelSerializer):
    produk = serializers.SerializerMethodField('get_produk')
    class Meta:
        model = models.Item
        fields = '__all__'

    def get_produk(self, obj):
        serializer = ProdukModelSerializer(obj.produk, context=self.context)
        return serializer.data


class PembayaranModelSerializer(serializers.ModelSerializer):
    pembelian = serializers.SerializerMethodField('get_pembelian')
    class Meta:
        model = models.Pembayaran
        fields = '__all__'

    def get_pembelian(self, obj):
        serializer = PembelianModelSerializer(obj.pembelian)
        return serializer.data
    

# untuk dipanggil di PembelianModelSerializer (agar tidak error)
class PembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pembayaran
        exclude = ('pembelian',)
    

