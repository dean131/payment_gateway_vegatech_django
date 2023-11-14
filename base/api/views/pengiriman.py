from rest_framework.decorators import action

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from base.api import serializers

from base import models


class PengirimanViewSet(ViewSet):
    def list(self, request):
        pengirimans = models.Pengiriman.objects.all()
        serializer = serializers.PengirimanModelSerializer(pengirimans, many=True)
        return Response(
            {
                'code': 200,
                'success': True,
                'message': 'List pengiriman berhasil didapatkan',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, pk=None):
        if not models.Pengiriman.objects.filter(pengiriman_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pengiriman tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pengiriman = models.Pengiriman.objects.get(pengiriman_id=pk)
        serializer = serializers.PengirimanModelSerializer(pengiriman)
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Detail pengiriman berhasil didapatkan',
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
        serializer = serializers.PengirimanModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pengiriman gagal ditambahkan',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Pengiriman berhasil ditambahkan',
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, pk=None):
        if not models.Pengiriman.objects.filter(pengiriman_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pengiriman tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pengiriman = models.Pengiriman.objects.get(pengiriman_id=pk)
        serializer = serializers.PengirimanModelSerializer(pengiriman, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pengiriman gagal diupdate',
                    # 'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pengiriman berhasil diupdate',
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, pk=None):
        if not models.Pengiriman.objects.filter(pengiriman_id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pengiriman tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pengiriman = models.Pengiriman.objects.get(pengiriman_id=pk)
        pengiriman.delete()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pengiriman berhasil dihapus',
            },
            status=status.HTTP_200_OK
        )
    
    @action(methods=['post'], detail=False)
    def kirim(self, request):
        pembelian_id = request.data.get('pembelian_id')
        no_resi = request.data.get('no_resi')

        pembelian = models.Pembelian.objects.filter(pembelian_id=pembelian_id).first()

        pengiriman = models.Pengiriman.objects.filter(pembelian=pembelian).first()
        if not pengiriman:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pengiriman tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pengiriman.status_pengiriman = 'dikirim'
        pengiriman.no_resi = no_resi
        pengiriman.save()

        pengiriman.pembelian.status_pembelian = 'diproses'
        pengiriman.pembelian.save()

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pengiriman berhasil dikirim',
            },
            status=status.HTTP_200_OK
        )
    
    @action(methods=['post'], detail=False)
    def terima(self, request):
        pembelian_id = request.data.get('pembelian_id')
        pembelian = models.Pembelian.objects.filter(pembelian_id=pembelian_id).first()
        
        if not pembelian:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pengiriman = models.Pengiriman.objects.filter(pembelian=pembelian).first()
        if not pengiriman:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pengiriman tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        pengiriman.status_pengiriman = 'diterima'
        pengiriman.save()

        pembelian.status_pembelian = 'selesai'
        pembelian.save()

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pengiriman berhasil diterima',
            },
            status=status.HTTP_200_OK
        )




