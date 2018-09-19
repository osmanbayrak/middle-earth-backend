from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
import unicodedata

from models import Building, Towns, Profile
import json
import ast


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

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr == "resources":
                value = ast.literal_eval(value)
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance




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




