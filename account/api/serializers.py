from rest_framework import serializers

from account.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }