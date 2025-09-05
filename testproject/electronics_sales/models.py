from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal


class Equipment(models.Model):
    equipment_name = models.CharField(
        max_length=280, verbose_name="Название оборудования",
        help_text="Введите название оборудования"
    )
    equipment_model = models.CharField(
        max_length=280, verbose_name="Тип (модель) оборудования",
        help_text="Введите наименование модели оборудования"
    )
    # Если дату вводит пользователь — обычное поле (без auto_now_add)
    market_release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата выхода на рынок",
        help_text="Укажите дату выхода на рынок"
    )

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["equipment_name", "equipment_model"]

    def __str__(self):
        return f"{self.equipment_name} — ({self.equipment_model})"


class Contact(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите адрес электронной почты"
    )
    country = models.CharField(
        max_length=140,
        verbose_name="Страна",
        help_text="Введите страну",
        db_index=True
    )
    city = models.CharField(
        max_length=140,
        verbose_name="Город",
        help_text="Введите город",
        db_index=True
    )
    street = models.CharField(
        max_length=140,
        verbose_name="Улица",
        help_text="Введите улицу"
    )

    house_number = models.CharField(
        max_length=20,
        verbose_name="Номер дома",
        help_text="Введите номер дома"
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["city", "street", "house_number"]

    def __str__(self):
        return self.email


class SaleNet(models.Model):
    net_name = models.CharField(max_length=200, verbose_name="Название")
    # контакты
    net_contacts = models.ForeignKey(
        Contact,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="salenets"
    )
    equipments = models.ManyToManyField(
        Equipment,
        blank=True,
        related_name="salenets",
        verbose_name="Оборудование"
    )
    # самоссылка: поставщик/родитель в иерархии
    supplier = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="clients"
    )

    arrears = models.DecimalField(
        max_digits=28, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
        verbose_name="Задолженность перед поставщиком",
        help_text="Укажите задолженность перед поставщиком (неотрицательное число)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    class Meta:
        indexes = [
            models.Index(fields=["net_name"]),
            ]


    def __str__(self):
        return self.net_name

    @property
    def hierarchy_level(self) -> int:
        level = 0
        node = self
        while node.supplier:
            node = node.supplier
            level += 1
        return level

    def clean(self):
        super().clean()

        if self.supplier and self.supplier == self:
            raise ValidationError({"supplier": "Поставщик не может быть самим собой"})

        seen = set()
        supplier = self.supplier
        while supplier:
            if supplier == self:
                raise ValidationError({"supplier": "Обнаружен цикл в цепочке поставщиков."})
            if supplier.pk in seen:
                # Повторная встреча любого узла = цикл (на любом уровне)
                raise ValidationError({"supplier": "Обнаружен цикл в цепочке поставщиков."})
            seen.add(supplier.pk)
            supplier = supplier.supplier
