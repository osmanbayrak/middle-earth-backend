# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from Serializer import *

# Create your views here.
from appName.models import Troop


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class TownViewSet(viewsets.ModelViewSet):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Towns.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateUpdateTownSerializer
        return ReadOnlyTownSerializer


class ProfileViewSet(viewsets.ModelViewSet):
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


class TroopViewSet(viewsets.ModelViewSet):
    queryset = Troop.objects.all()
    serializer_class = TroopSerializer

