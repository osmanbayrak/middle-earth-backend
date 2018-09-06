from django.contrib.auth.models import User
from rest_framework import serializers
from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'is_staff')


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Towns
        fields = ('name', 'military')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    town = TownSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"

