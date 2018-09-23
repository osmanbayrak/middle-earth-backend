
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.authtoken import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from appName.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'towns', TownViewSet, base_name='townofsalem')
router.register(r'profiles', ProfileViewSet, base_name='profiles')
router.register(r'buildings', BuildingViewSet, base_name='buildings')
router.register(r'troops', TroopViewSet, base_name='troops')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token)
]
