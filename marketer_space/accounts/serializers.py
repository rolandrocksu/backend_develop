from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Account,
    Organization,
    Invitation
)
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())]
    )
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(AccountSerializer, self).create(validated_data)

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = Account.objects.create(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #
    #     return user
    class Meta:
        model = Account
        fields = ('id', 'email', 'organization', 'first_name', 'last_name',
                  'country', 'profile_picture', 'password', 'created', 'modified')


class OrganizationSerializer(serializers.ModelSerializer):
    users = AccountSerializer(many=True, read_only=True)

    def validate(self, attrs):
        if Organization.objects.filter(
                domain=self.data.get('domain')).exists():
            raise serializers.ValidationError(
                {"message": "Domain exists"})

        return attrs

    class Meta:
        model = Organization
        fields = ('domain', 'name', 'users')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        # token['username'] = user.username
        token['email'] = user.email
        return token


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('id', 'organization', 'token', 'invitor', 'receiver', 'status', 'created_at')
