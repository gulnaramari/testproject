from rest_framework import serializers

from .models import Contact, Equipment, SaleNet


class ContactSerializer(serializers.ModelSerializer):
    """Преобразование данных модели "Контакты" из БД в нужный формат"""
    class Meta:
        model = Contact
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    """Преобразование данных модели "оборудованиние" из БД в нужный формат"""
    class Meta:
        model = Equipment
        fields = "__all__"


class SaleNetCreateSerializer(serializers.ModelSerializer):
    """Создание и обновление объектов модели "сеть продаж"""
    class Meta:
        model = SaleNet
        fields = '__all__'


class SaleNetSerializer(serializers.ModelSerializer):
    """Класс для сериализации данных модели "сеть продаж" из базы данных"""
    hierarchy_level = serializers.ReadOnlyField()
    # указываем серилизаторы отдельных объектов, чтобы данные этих объектов отображались корректно в API
    contacts = ContactSerializer(many=True, read_only=True) # используем "OneToOneField" - это отдельный объект
    equipments = EquipmentSerializer(many=True, read_only=True) # используем "ManyToManyField" - это список объектов

    class Meta:
        model = SaleNet
        exclude = ("created_at",)


class SaleNetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleNet
        fields = "__all__"
        read_only_fields = ("created_at", "arrears")

