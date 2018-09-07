from django.contrib.auth.models import User
from rest_framework import serializers
from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'is_staff')


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('id','type', 'level', 'town', 'img', 'created_date', 'construction_time')


class TownSerializer(serializers.ModelSerializer):
    buildings = BuildingSerializer(many=True)

    class Meta:
        model = Towns
        fields = ('id', 'name', 'military', 'buildings')


class ReadOnlyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    town = TownSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"


class CreateUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'point')




