from django.db import transaction

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from account.models import User
from base.api import serializers
from base import models
   

class PembelianViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = models.Pembelian.objects.all()
        user_id = self.request.query_params.get('user_id')
        status_pembelian = self.request.query_params.get('status_pembelian')

        if user_id:
            queryset = queryset.filter(user__user_id=user_id)

        if status_pembelian:
            queryset = queryset.filter(status_pembelian=status_pembelian)

        return queryset

    def list(self, request):
        pembelians = self.get_queryset()
        serializer = serializers.PembelianModelSerializer(pembelians, many=True)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'List pembelian berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, pk=None):
        if not models.Pembelian.objects.filter(pembelian_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pembelian = models.Pembelian.objects.get(pembelian_id=pk)
        serializer = serializers.PembelianModelSerializer(pembelian)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Detail pembelian berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @transaction.atomic
    def create(self, request):
        user_id = request.data.get('user_id')
        produk_id = request.data.get('produk_id')
        kuantitas = request.data.get('kuantitas')

        user = User.objects.filter(user_id=user_id).first()
        produk = models.Produk.objects.filter(produk_id=produk_id).first()

        if not user:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'User tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not produk:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Produk tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        pembelian, created = models.Pembelian.objects.get_or_create(user=user, status_pembelian='keranjang')

        item, created = models.Item.objects.get_or_create(pembelian=pembelian, produk=produk)
        if kuantitas <= 0:
            item.delete()
            pembelian.total_harga_pembelian = sum([item.total_harga_item for item in pembelian.item_set.all()])
            pembelian.save()
            return Response(
                {
                    'code': status.HTTP_200_OK,
                    'success': True,
                    'message': 'Item berhasil dihapus',
                },
                status=status.HTTP_200_OK
            )
        item.kuantitas = kuantitas
        item.total_harga_item = produk.harga_produk * kuantitas
        item.save()

        pembelian.total_harga_pembelian = sum([item.total_harga_item for item in pembelian.item_set.all()])
        pembelian.save()

        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Pembelian berhasil ditambahkan',
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, pk=None):
        if not models.Pembelian.objects.filter(pembelian_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        pembelian = models.Pembelian.objects.get(pembelian_id=pk)
        serializer = serializers.PembelianModelSerializer(pembelian, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembelian gagal diupdate',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pembelian berhasil diupdate',
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, pk=None):
        if not models.Pembelian.objects.filter(pembelian_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        pembelian = models.Pembelian.objects.get(pembelian_id=pk)
        pembelian.delete()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pembelian berhasil dihapus',
            },
            status=status.HTTP_200_OK
        )


