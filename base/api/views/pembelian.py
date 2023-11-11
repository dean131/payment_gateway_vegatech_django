from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from account.models import User
from base.api import serializers
from base import models
   

class PembelianViewSet(viewsets.ViewSet):
    def list(self, request):
        pembelians = models.Pembelian.objects.all()
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
    
    def create(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'User tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        request.data.update({'user': user.user_id})
        serializer = serializers.PembelianModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembelian gagal ditambahkan',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pembelian, created = models.Pembelian.objects.get_or_create(**serializer.validated_data)
        
        if not created:
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembelian telah dibuat',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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
    
