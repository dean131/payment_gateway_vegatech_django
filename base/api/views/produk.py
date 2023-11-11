from django.db.models import Q

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from base.api import serializers
from base import models


class ProdukViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProdukModelSerializer

    def get_queryset(self):
        queryset = models.Produk.objects.all()
        search = self.request.query_params.get('search')
        kategori = self.request.query_params.get('kategori_produk')

        if search:
            queryset = queryset.filter(
                Q(nama_produk__icontains=search) | 
                Q(kategori_produk__icontains=search)
            )

        if kategori:
            queryset = queryset.filter(kategori_produk=kategori)
        return queryset
    
    def list(self, request):
        produks = self.get_queryset()
        serializer = self.get_serializer(produks, many=True)
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

        serializer = self.get_serializer(data=request.data)
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
        serializer = self.get_serializer(produk)
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
        serializer = self.get_serializer(produk, data=request.data, partial=True)
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