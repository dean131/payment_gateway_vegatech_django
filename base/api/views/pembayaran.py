from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from base.api import serializers
from base import models


class PembayaranViewSet(viewsets.ViewSet):
    def list(self, request):
        pembayarans = models.Pembayaran.objects.all()
        serializer = serializers.PembayaranModelSerializer(pembayarans, many=True)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'List pembayaran berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, pk=None):
        if not models.Pembayaran.objects.filter(pembayaran_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembayaran tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pembayaran = models.Pembayaran.objects.get(pembayaran_id=pk)
        serializer = serializers.PembayaranModelSerializer(pembayaran)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Detail pembayaran berhasil didapatkan',
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
        
        request.data.update({'pembelian': request.data.get('pembelian_id')})
        serializer = serializers.PembayaranModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembayaran gagal ditambahkan',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Pembayaran berhasil ditambahkan',
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, pk=None):
        if not models.Pembayaran.objects.filter(pembayaran_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembayaran tidak ditemukan',
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
        pembelian = models.Pembelian.objects.get(pembelian_id=request.data.get('pembelian_id'))
        request.data.update({'pembelian': pembelian.pembelian_id})
        pembayaran = models.Pembayaran.objects.get(pembayaran_id=pk)
        serializer = serializers.PembayaranModelSerializer(pembayaran, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembayaran gagal diupdate',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pembayaran berhasil diupdate',
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, pk=None):
        if not models.Pembayaran.objects.filter(pembayaran_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembayaran tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pembayaran = models.Pembayaran.objects.get(pembayaran_id=pk)
        pembayaran.delete()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pembayaran berhasil dihapus',
            },
            status=status.HTTP_200_OK
        )
