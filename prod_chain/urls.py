from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views
from .apps import ProdChainConfig


app_name = ProdChainConfig.name


router = DefaultRouter()
router.register(r'api/products',
                views.ProductAPIView,
                )


urlpatterns = [
    path('', include(router.urls)),
]
