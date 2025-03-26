from django.contrib import admin
from django.urls import path, include
from cotacoes.views import CotacaoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cotacoes', CotacaoViewSet, basename='cotacao')

urlpatterns = [
    path('api/', include(router.urls)),
]
