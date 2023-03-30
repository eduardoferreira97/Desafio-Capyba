from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'confirm_email', 'password', 'confirm_password']

    def validate(self, data):
        if data['email'] != data.pop('confirm_email'):
            raise serializers.ValidationError("Os endereços de e-mail não coincidem.")
        
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("As senhas não coincidem.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # profile_image=validated_data.get('profile_image', None),
            # date_of_birth=validated_data.get('date_of_birth', None),
            is_active=False
        )
        return user
