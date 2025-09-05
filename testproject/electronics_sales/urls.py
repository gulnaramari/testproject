from django.urls import path
from .views import (
    SaleNetCreateAPIView,
    SaleNetDestroyAPIView,
    SaleNetListAPIView,
    SaleNetRetrieveAPIView,
    SaleNetUpdateAPIView,
)

app_name = "electronics_sales"

urlpatterns = [
    path("salenets/create/", SaleNetCreateAPIView.as_view(), name="salenets-create"),
    path("salenets/", SaleNetListAPIView.as_view(), name="salenets-list"),
    path(
        "salenets/<int:pk>/", SaleNetRetrieveAPIView.as_view(), name="salenets-detail"
    ),
    path(
        "salenets/<int:pk>/update/",
        SaleNetUpdateAPIView.as_view(),
        name="salenets-update",
    ),
    path(
        "salenets/<int:pk>/destroy/",
        SaleNetDestroyAPIView.as_view(),
        name="salenets-destroy",
    ),
]
