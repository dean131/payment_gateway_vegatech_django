import midtransclient

from django.db import transaction
from django.conf import settings

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.models import User

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
    
    @transaction.atomic
    def create(self, request):
        user_id = request.data.get('user_id')
        nama_bank = request.data.get('nama_bank')

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
        
        pembelian = models.Pembelian.objects.filter(user=user, status_pembelian='keranjang').first()
        if not pembelian:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'Pembelian tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        core = midtransclient.CoreApi(
            is_production=False,
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )

        param = {
            "payment_type": "bank_transfer",
            "transaction_details": {
                "gross_amount": pembelian.total_harga_pembelian,
                "order_id": str(pembelian.pembelian_id),
            },
            "bank_transfer":{
                "bank": nama_bank,
            }
        }

        charge_response = core.charge(param)
        print('charge_response:')
        print(charge_response)

        pembayaran = models.Pembayaran.objects.create(
            pembelian=pembelian,
            transaksi_id=charge_response['transaction_id'],
            nama_bank=nama_bank,
            waktu_pembayaran=charge_response['transaction_time'],
            no_va=charge_response['va_numbers'][0]['va_number']
        )

        pembayaran_serializer = serializers.PembayaranModelSerializer(pembayaran)
        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Pembayaran berhasil ditambahkan',
                'data': pembayaran_serializer.data
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
    
    @action(detail=False, methods=['post'])
    def notification_handler(self, request):
        status_transaksi = request.data.get('transaction_status')
        no_va = request.data.get('va_numbers')[0]['va_number']

        pembayaran = models.Pembayaran.objects.filter(no_va=no_va).first()

        if status_transaksi == 'expire':
            pembayaran.status_pembayaran = 'kadaluarsa'
            pembayaran.save()
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembayaran kadaluarsa',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if status_transaksi == 'cancel':
            pembayaran.status_pembayaran = 'dibatalkan'
            pembayaran.save()
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembayaran dibatalkan',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if status_transaksi == 'settlement':
            pembayaran.status_pembayaran = 'dibayar'
            pembayaran.save()

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Pembayaran berhasil dibayar',
            },
            status=status.HTTP_200_OK
        )

        