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
        alamat_pengiriman = request.data.get('alamat_pengiriman')
        metode_pengiriman = request.data.get('metode_pengiriman')
        ongkos_kirim = request.data.get('ongkos_kirim', 0)
        nama_penerima = request.data.get('nama_penerima')
        no_telp_penerima = request.data.get('no_telp_penerima')

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

        if metode_pengiriman == 'ambil_sendiri':
            models.Pengiriman.objects.create(
                pembelian=pembelian,
                metode_pengiriman=metode_pengiriman,
                alamat_pengiriman='Ambil di Toko',
                status_pengiriman='belum_diambil',
                ongkos_kirim=0,
                nama_penerima=nama_penerima,
                no_telp_penerima=no_telp_penerima
            )
            ongkos_kirim = 0
        else:
            models.Pengiriman.objects.create(
                pembelian=pembelian,
                metode_pengiriman=metode_pengiriman,
                alamat_pengiriman=alamat_pengiriman,
                status_pengiriman='belum_dikirim',
                ongkos_kirim=ongkos_kirim,
                nama_penerima=nama_penerima,
                no_telp_penerima=no_telp_penerima
            )
        
        core = midtransclient.CoreApi(
            is_production=False,
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )

        param = {
            "payment_type": "bank_transfer",
            "transaction_details": {
                "gross_amount": pembelian.total_harga_pembelian + ongkos_kirim,
                "order_id": str(pembelian.pembelian_id),
            },
            "bank_transfer":{
                "bank": nama_bank,
            }
        }

        charge_response = core.charge(param)
        if charge_response['status_code'] != '201':
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Pembayaran gagal ditambahkan',
                    'data': charge_response['status_message']
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        pembayaran = models.Pembayaran.objects.create(
            pembelian=pembelian,
            transaksi_id=charge_response['transaction_id'],
            nama_bank=nama_bank,
            waktu_pembayaran=charge_response['transaction_time'],
            no_va=charge_response['va_numbers'][0]['va_number'],
            total_pembayaran=float(charge_response['gross_amount'])
        )
        pembayaran_serializer = serializers.PembayaranModelSerializer(pembayaran)

        pembelian.status_pembelian = 'menunggu'
        pembelian.save()


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
        pengiriman = models.Pengiriman.objects.filter(pembelian=pembayaran.pembelian).first()

        if status_transaksi == 'settlement':
            pembayaran.status_pembayaran = 'lunas'
            pembayaran.save()

            if pengiriman.metode_pengiriman == 'ambil_sendiri':
                pembayaran.pembelian.status_pembelian = 'diproses'
                pembayaran.pembelian.save()

            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'status_message': 'Pembayaran berhasil dibayar',
                },
                status=status.HTTP_200_OK
            )
        
        if status_transaksi == 'expire':
            pembayaran.status_pembayaran = 'kadaluarsa'
            pembayaran.save()
            pembayaran.pembelian.status_pembelian = 'dibatalkan'
            pembayaran.pembelian.save()
            pengiriman = models.Pengiriman.objects.filter(pembelian=pembayaran.pembelian).first()
            pengiriman.status_pengiriman = 'dibatalkan'
            pengiriman.save()
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'status_message': 'Pembayaran kadaluarsa',
                },
                status=status.HTTP_200_OK
            )

        if status_transaksi == 'cancel':
            pembayaran.status_pembayaran = 'dibatalkan'
            pembayaran.save()
            pembayaran.pembelian.status_pembelian = 'dibatalkan'
            pembayaran.pembelian.save()
            pengiriman = models.Pengiriman.objects.filter(pembelian=pembayaran.pembelian).first()
            pengiriman.status_pengiriman = 'dibatalkan'
            pengiriman.save()
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'status_message': 'Pembayaran dibatalkan',
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status_message': 'Pembayaran gagal',
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        