from django.contrib.auth import authenticate, login, logout

from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import status

from account import models
from .serializers import UserModelSerializer


class UserViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        if not models.User.objects.filter(id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'User tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = models.User.objects.get(id=pk)

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Berhasil mendapatkan data user',
                'data': UserModelSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )
    
    def update(self, request, pk=None):
        if not models.User.objects.filter(id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'User tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user = models.User.objects.get(pk=pk)

        if models.User.objects.filter(email=request.data.get('email')).exclude(id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Gagal mengubah data user, email sudah terdaftar.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserModelSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Gagal mengubah data user',
                    # 'errors': serializer._errors.values(),
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Berhasil mengubah data user',
                'data': serializer.data,
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, pk=None):
        if not models.User.objects.filter(id=pk).exists():
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'success': False,
                    'message': 'User tidak ditemukan',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = models.User.objects.get(pk=pk)
        user.delete()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Berhasil menghapus data user',
            },
            status=status.HTTP_200_OK
        )


class RegisterAPIView(views.APIView):
    def post(self, request):
        for key in request.data.keys():
            if key == 'foto_profil':
                continue
            if not request.data.get(key):
                return Response(
                    {
                        'code': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                        'message': f'Registrasi gagal, {key} tidak boleh kosong',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        if request.data.get('password') != request.data.get('konfirmasi_password'):
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Registrasi gagal, password dan konfirmasi password tidak sama.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if models.User.objects.filter(email=request.data.get('email')).exists():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Registrasi gagal, email sudah terdaftar.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Registrasi gagal, silahkan cek data yang anda masukkan.',
                    # 'errors': serializer._errors.values(),
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        models.User.objects.create_user(
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
            nama_lengkap=serializer.validated_data.get('nama_lengkap'),
            no_telepon=serializer.validated_data.get('no_telepon'),
            jenis_kelamin=serializer.validated_data.get('jenis_kelamin'),
            tanggal_lahir=serializer.validated_data.get('tanggal_lahir'),
            foto_profil=serializer.validated_data.get('foto_profil'),
        )

        return Response(
            {
                'code': status.HTTP_201_CREATED,
                'success': True,
                'message': 'Registrasi berhasil',
            },
            status=status.HTTP_201_CREATED
        )
    

class UserLoginAPIView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Login gagal, email atau password salah.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        login(request, user)
        
        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Login berhasil',
                'data': UserModelSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )
    

class UserLogoutAPIView(views.APIView):
    def post(self, request):
        logout(request)

        return Response(
            {
                'code': status.HTTP_200_OK,
                'success': True,
                'message': 'Logout berhasil',
            },
            status=status.HTTP_200_OK
        )
