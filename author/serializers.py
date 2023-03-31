from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):

    email_confirmation = serializers.EmailField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username','first_name', 'last_name', 'email', 'email_confirmation', 'profile_pic', 'birthdate']

    def validate(self, data):
        if data['email'] != data['email_confirmation']:
            raise serializers.ValidationError("O email e sua confirmação não conferem.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data.pop('email_confirmation')

        return get_user_model().objects.create(**validated_data)