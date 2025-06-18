from rest_framework import serializers
from .models import CustomUser, UserChat

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'online_status']

class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['id', 'user_sender', 'user_receiver', 'message', 'timestamp']
        read_only_fields = ['timestamp']
    