from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, AudioTrack, ScheduledSession, FriendRequest
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'nationality')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name','username', 'is_active', 'is_superuser', 'nationality')

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        nationality = validated_data['nationality']
        is_superuser = validated_data.get('is_superuser', False)

        if is_superuser:
            user = User.objects.create_superuser(email, password, first_name=first_name, last_name=last_name)
        else:
            user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Email and password are required.')

        data['user'] = user
        return data


class AudioTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTrack
        fields = '__all__'


class ScheduledSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledSession
        fields = '__all__'


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'recipient', 'status', 'created_at']

