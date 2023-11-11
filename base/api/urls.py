from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api.views import (
    produk,
    pembelian,
    item,
    pengiriman,
    pembayaran
)


router = DefaultRouter()
router.register('produk', produk.ProdukViewSet, basename='produk')
router.register('pembelian', pembelian.PembelianViewSet, basename='pembelian')
router.register('item', item.ItemViewSet, basename='item')
router.register('pengiriman', pengiriman.PengirimanViewSet, basename='pengiriman')
router.register('pembayaran', pembayaran.PembayaranViewSet, basename='pembayaran')

urlpatterns = [
    path('', include(router.urls))
]