from rest_framework import serializers

from .models import Contact, Equipment, SaleNet


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор контактных данных (email, страна/город, улица, дом).
    Используется как вложенный read-only сериализатор при чтении SaleNet
    и как самостоятельный CRUD при необходимости.
    """
    class Meta:
        model = Contact
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор оборудования (название, модель, дата выхода).
    Используется как вложенный read-only сериализатор при чтении SaleNet.
    """
    class Meta:
        model = Equipment
        fields = "__all__"


class SaleNetCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания SaleNet.

    По умолчанию принимает:
      - net_name (str)
      - net_contacts (ID существующего Contact)
      - supplier (ID существующего SaleNet или null)
      - equipments (список ID Equipment)
      - arrears (Decimal) — если разрешено политикой
      - прочие разрешённые поля

    Примечание:
      вложенные объекты здесь НЕ создаются; передаём только их IDs.
    """
    class Meta:
        model = SaleNet
        fields = '__all__'


class SaleNetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения SaleNet (list/retrieve).
    Включает:
      - computed поле hierarchy_level (read-only), если определено в модели
      - вложенный объект контакта (net_contacts)
      - вложенный список оборудования (equipments)
    """
    hierarchy_level = serializers.ReadOnlyField()
    net_contacts = ContactSerializer(read_only=True)                 # FK → один объект
    equipments = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = SaleNet
        fields = "__all__"


class SaleNetUpdateSerializer(serializers.ModelSerializer):
    """
        Сериализатор для обновления SaleNet.
        По умолчанию разрешает обновлять все поля, кроме отмеченных read-only.
        Например, arrears/created_at — только для чтения.
        """
    class Meta:
        model = SaleNet
        fields = "__all__"
        read_only_fields = ("created_at", "arrears")

