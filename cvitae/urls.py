# arquivos/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MarkdownCreateView,CVitaeViewSet
router = DefaultRouter()
router.register(r'', CVitaeViewSet)
urlpatterns = [
    path('criar-markdown/', MarkdownCreateView.as_view(), name='criar-markdown'),
    path('cv/', include(router.urls)),
]
