"""
API views для сущности SaleNet.

Здесь реализованы CRUD-эндпоинты с базовой фильтрацией и сортировкой.
Для списков используем select_related/prefetch_related, чтобы сократить
количество SQL-запросов при работе с FK/M2M.
"""

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
    """ POST /salenets/
    Создаёт новую торговую сеть (SaleNet).
    Тело запроса валидируется через SaleNetCreateSerializer.
    """
    queryset = SaleNet.objects.all()
    serializer_class = SaleNetCreateSerializer


class SaleNetListAPIView(generics.ListAPIView):
    """GET /salenets/
    Возвращает список торговых сетей.
    Поддерживает:
      - фильтрацию по стране контакта (net_contacts__country)
      - сортировку по стране контакта
    """
    serializer_class = SaleNetSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["net_contacts__country"]
    ordering_fields = ["net_contacts__country"]

    def get_queryset(self):
        # Оптимизация JOIN'ов: тянем FK и M2M заранее
        return (
            SaleNet.objects
            .select_related("net_contacts", "supplier")
            .prefetch_related("equipments")
        )


class SaleNetRetrieveAPIView(generics.RetrieveAPIView):
    """GET /salenets/{id}/
    Возвращает одну сеть по ID.
    """
    queryset = SaleNet.objects.select_related("net_contacts", "supplier").prefetch_related("equipments")
    serializer_class = SaleNetSerializer


class SaleNetUpdateAPIView(generics.UpdateAPIView):
    """PUT/PATCH /salenets/{id}/
    Обновляет сеть по ID.
    Поля с ограничениями смотрите в SaleNetUpdateSerializer (например, arrears read-only).
    """
    queryset = SaleNet.objects.all()
    serializer_class = SaleNetUpdateSerializer


class SaleNetDestroyAPIView(generics.DestroyAPIView):
    """DELETE /salenets/{id}/ Удаляет сеть по ID. """
    queryset = SaleNet.objects.all()
