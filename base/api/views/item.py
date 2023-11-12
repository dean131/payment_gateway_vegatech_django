from django.db import transaction

from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status
from base.api import serializers

from base import models


class ItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = models.Item.objects.all()
        pembelian_id = self.request.query_params.get('pembelian_id')

        if pembelian_id:
            queryset = queryset.filter(pembelian__pembelian_id=pembelian_id)

        return queryset

    def list(self, request):
        items = self.get_queryset()
        serializer = serializers.ItemModelSerializer(items, many=True)
        return Response(
            {
                'code': 200,
                'success': True,
                'message': 'List item berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, pk=None):
        if not models.Item.objects.filter(item_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Item tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        item = models.Item.objects.get(item_id=pk)
        serializer = serializers.ItemModelSerializer(item)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Detail item berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def create(self, request):
        if not models.Pembelian.objects.filter(pembelian_id=request.data.get('pembelian_id')).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not models.Produk.objects.filter(produk_id=request.data.get('produk_id')).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Produk tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.ItemModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Item gagal ditambahkan',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Item berhasil ditambahkan',
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, pk=None):
        if not models.Item.objects.filter(item_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Item tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not models.Pembelian.objects.filter(pembelian_id=request.data.get('pembelian_id')).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not models.Produk.objects.filter(produk_id=request.data.get('produk_id')).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Produk tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        item = models.Item.objects.get(item_id=pk)
        serializer = serializers.ItemModelSerializer(item, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Item gagal diupdate',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Item berhasil diupdate',
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, pk=None):
        if not models.Item.objects.filter(item_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Item tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        item = models.Item.objects.get(item_id=pk)
        pembelian = item.pembelian

        if pembelian.status_pembelian == 'selesai':
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembelian sudah selesai, tidak bisa menghapus item',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
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



