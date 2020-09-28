from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):  # create class to serializer model
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Message
        fields = ('id', 'title', 'body', 'read', 'send', 'author')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer usermodel
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'messages')
