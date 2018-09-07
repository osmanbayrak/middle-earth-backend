# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from Serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from models import *
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets, generics, mixins
from Serializer import *

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TownViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Towns.objects.all()
    serializer_class = TownSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Profile.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateUpdateProfileSerializer
        return ReadOnlyProfileSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

