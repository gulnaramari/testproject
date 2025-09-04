from django.urls import path

from .apps import ElectronicsSalesConfig
from .views import (
    SaleNetCreateAPIView,
    SaleNetDestroyAPIView,
    SaleNetListAPIView,
    SaleNetRetrieveAPIView,
    SaleNetUpdateAPIView,
)

app_name = ElectronicsSalesConfig

urlpatterns = [
    path("salenet/create/", SaleNetCreateAPIView.as_view(), name="salenet-create"),
    path("salenet/", SaleNetListAPIView.as_view(), name="salenet-list"),
    path(
        "salenet/<int:pk>/", SaleNetRetrieveAPIView.as_view(), name="salenet-detail"
    ),
    path(
        "salenet/<int:pk>/update/",
        SaleNetUpdateAPIView.as_view(),
        name="salenet-update",
    ),
    path(
        "salenet/<int:pk>/destroy/",
        SaleNetDestroyAPIView.as_view(),
        name="salenet-destroy",
    ),
]
