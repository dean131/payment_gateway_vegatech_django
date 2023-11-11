from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from base.api import serializers
from base import models


class ProdukViewSet(viewsets.ViewSet):
    def list(self, request):
        produks = models.Produk.objects.all()
        serializer = serializers.ProdukModelSerializer(produks, many=True)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'List produk berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def create(self, request):
        for key in request.data:
            if key == 'deskripsi_produk' or key == 'gambar_produk': 
                continue
            if not request.data[key]:
                return Response(
                    {
                        'code': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                        'message': f'Field {key} tidak boleh kosong',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = serializers.ProdukModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Produk gagal ditambahkan',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Produk berhasil ditambahkan',
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        if not models.Produk.objects.filter(produk_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Produk tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        produk = models.Produk.objects.get(produk_id=pk)
        serializer = serializers.ProdukModelSerializer(produk)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Detail produk berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        if not models.Produk.objects.filter(produk_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Produk tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        for key in request.data:
            if key == 'deskripsi_produk' or key == 'gambar_produk': 
                continue
            if not request.data[key]:
                return Response(
                    {
                        'code': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                        'message': f'Field {key} tidak boleh kosong',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        produk = models.Produk.objects.get(produk_id=pk)
        serializer = serializers.ProdukModelSerializer(produk, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Produk gagal diupdate',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Produk berhasil diupdate',
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        if not models.Produk.objects.filter(produk_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Produk tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        produk = models.Produk.objects.get(produk_id=pk)
        produk.delete()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Produk berhasil dihapus',
            },
            status=status.HTTP_200_OK
        )