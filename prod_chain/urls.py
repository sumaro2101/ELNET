from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views
from .apps import ProdChainConfig


app_name = ProdChainConfig.name


router = DefaultRouter()
router.register(r'api/products',
                views.ProductAPIViewset,
                )
router.register(r'api/contacts',
                views.ContactAPIViewset,
                )


urlpatterns = [
    path('', include(router.urls)),
]
