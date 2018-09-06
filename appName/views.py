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


class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


class ProfileCrudView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
