from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from .models import SaleNet
from .serializers import (
    SaleNetCreateSerializer,
    SaleNetSerializer,
    SaleNetUpdateSerializer,
)


class SaleNetCreateAPIView(generics.CreateAPIView):
    serializer_class = SaleNetCreateSerializer


class SaleNetListAPIView(generics.ListAPIView):
    queryset = SaleNet.objects.all()
    serializer_class = SaleNetSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["contacts__country"]
    ordering_fields = ["contacts__country"]


class SaleNetRetrieveAPIView(generics.RetrieveAPIView):
    queryset = SaleNet.objects.all()
    serializer_class = SaleNetSerializer


class SaleNetUpdateAPIView(generics.UpdateAPIView):
    queryset = SaleNet.objects.all()
    serializer_class = SaleNetUpdateSerializer


class SaleNetDestroyAPIView(generics.DestroyAPIView):
    queryset = SaleNet.objects.all()
