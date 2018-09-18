from django.contrib.auth.models import User
from rest_framework import serializers
from models import Building, Towns, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'profile')


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('id', 'type', 'level', 'town', 'img', 'created_date', 'change_date', 'construction_time', 'status', 'cost')


class ReadOnlyTownSerializer(serializers.ModelSerializer):
    buildings = BuildingSerializer(many=True, read_only=True)

    class Meta:
        model = Towns
        fields = ('id', 'name', 'military', 'buildings', 'whom', 'resources')


class CreateUpdateTownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Towns
        fields = ('id', 'name', 'military', 'whom', 'resources')


class ReadOnlyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    town = ReadOnlyTownSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ("bio", 'user', 'score', 'town')


class CreateUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'user', 'town')




