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
                  "last_login", # singal last logged in from frotend
                  ]
        extra_kwargs = {
                'password': {'write_only': True}
            }
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
    
        email: str = representation.get('email')

        if email and email.endswith('@admin.pl'):
            representation['email'] = 'hidden@hidden.com'

        return representation
    
    def update(self, instance, validated_data):
        phone = validated_data.get('phone', None)
        if phone and not phone.startswith('+48'):
            validated_data['phone'] = '+48' + phone # change it later
        return super().update(instance, validated_data)


class OtherUserProfileSerializer(UserProfileSerializer):
    boards = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'bio',
                  'phone',
                  'nickname',
                  'password',
                  "last_login",
                  "boards",
                  ]

    def get_boards(self, obj):
        from Boards.serializers import BoardMembershipSerializer
        user1 = self.context.get("user1")
        user2 = obj
        boards = BoardMembershipSerializer.get_common_boards(user1, user2, context=self.context)[:6]
        return boards


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        return user


class UserLookupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="user-detail-lookup",
        lookup_field="pk"
    )
    class Meta:
        model = User
        fields = [
            "email",
            "nickname",
            "first_name",
            "last_name",
            "url",
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        email: str = representation.get("email")
        if email and email.endswith("@admin.pl"):
            representation["email"] = "hidden@hidden.pl"
        return representation