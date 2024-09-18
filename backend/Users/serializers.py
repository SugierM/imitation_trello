from Users.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'bio',
                  'phone',
                  'nickname',
                  'password',
                  ]
    extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        return user


class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'bio',
                  'phone',
                  'nickname',
                  'pk' # Just for now
                  ]
        