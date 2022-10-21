from rest_framework import serializers
from ...models import User, Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerilizer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=25, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):

        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail': 'passwords dosent match'})

        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})

        return super().validate(attrs)

    # chon user khodemun dadim inja nesbat be modele taqir midahim
    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)



class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({'detail': 'user is not verifed!'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'detail': 'user is not verifed!'})
        data['email'] = self.user.email
        return data

#az ModelSerializer estefade nemikonim be dalile confilicte ehtemali
class ChangePasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField(required=True )
    new_pass = serializers.CharField(required=True)
    new_pass1 = serializers.CharField(required=True)

    def validate(self, attrs):

        if attrs.get('new_pass') != attrs.get('new_pass1'):
            raise serializers.ValidationError({'detail': 'passwords dosent match'})

        try:
            validate_password(attrs.get('new_pass'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_pass': list(e.messages)})

        return super().validate(attrs)

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'email', 'first_name', 'last_name', 'image', 'description']
        read_only_fields = ['email', 'user']

class ActivationResendApiSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'user dosent exist'})
        if user_obj.is_verified:
            raise serializers.ValidationError({'detail': 'user has already verified!'})
        attrs['user'] = user_obj

        return super().validate(attrs)