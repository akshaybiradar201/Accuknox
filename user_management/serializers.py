from rest_framework import serializers

from .models import CustomUser, Request

class CustomUserSerializer(serializers.ModelSerializer):
    num_friends = serializers.ReadOnlyField(source='friends.count')  
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'num_friends') 

class RequestSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    receiver = CustomUserSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'sender', 'receiver')