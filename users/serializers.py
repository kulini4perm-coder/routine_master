from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "tg_chat_id")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
