from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api import views


router = DefaultRouter()
router.register('produk', views.ProdukViewSet, basename='produk')

urlpatterns = [
    path('', include(router.urls))
]