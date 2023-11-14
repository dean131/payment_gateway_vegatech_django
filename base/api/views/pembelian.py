from django.db import transaction
from django.conf import settings

from rest_framework.decorators import action 
from rest_framework import status, viewsets
from rest_framework.response import Response

from account.models import User
from base.api import serializers
from base import models

import midtransclient
   

class PembelianViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PembelianModelSerializer

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
        serializer = self.get_serializer(pembelians, many=True)
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
        serializer = self.get_serializer(pembelian)
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
        item.save()
        pembelian.save()

        serializer = serializers.ItemModelSerializer(item)

        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Pembelian berhasil ditambahkan',
                'data': serializer.data,
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
        serializer = self.get_serializer(pembelian, data=request.data, partial=True)
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

    @action(detail=False, methods=['post'])
    def batalkan_pembelian(self, request):
        pembelian_id=request.data.get('pembelian_id')
        pembelian = models.Pembelian.objects.filter(pembelian_id=pembelian_id, status_pembelian='menunggu').first()

        if not pembelian:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pembayaran = pembelian.pembayaran_set.first()
        if not pembayaran:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembayaran tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if pembayaran.status_pembayaran == 'lunas':
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembayaran sudah lunas. Tidak bisa dibatalkan',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        core = midtransclient.CoreApi(
            is_production=False,
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )
        
        res = core.transactions.cancel(pembelian.pembelian_id)
        if res.status_code != '200':
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembatalan pembelian gagal',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        pembayaran.status_pembayaran = 'dibatalkan'
        pembayaran.save()
        pembelian.status_pembelian = 'dibatalkan'
        pembelian.save()
        pengiriman = pembelian.pengiriman_set.first()
        pengiriman.status_pengiriman = 'dibatalkan'
        pengiriman.save()

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pembelian berhasil dibatalkan',
            },
            status=status.HTTP_200_OK
        )
        