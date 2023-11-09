from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


routers = DefaultRouter()
routers.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(routers.urls)),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
]