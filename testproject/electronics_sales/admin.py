from decimal import Decimal
from django.contrib import admin
from django import forms

from .models import Equipment, Contact, SaleNet


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_arrears(modeladmin, request, queryset):
    updated = queryset.update(arrears=Decimal("0"))
    modeladmin.message_user(request, f"Обнулено задолженностей: {updated}")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "equipment_name", "equipment_model", "market_release_date")
    search_fields = ("equipment_name", "equipment_model")
    list_filter = ("market_release_date",)
    ordering = ("equipment_name", "equipment_model")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "country", "city", "street", "house_number")
    search_fields = ("email", "country", "city", "street", "house_number")
    list_filter = ("country", "city")


class SaleNetAdminForm(forms.ModelForm):
    class Meta:
        model = SaleNet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = SaleNet.objects.all()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        self.fields["supplier"].queryset = qs


@admin.register(SaleNet)
class SaleNetAdmin(admin.ModelAdmin):
    form = SaleNetAdminForm
    actions = [clear_arrears]

    list_display = (
        "id", "net_name", "get_contact_city", "supplier", "hierarchy_level", "arrears", "created_at",
    )
    search_fields = ("net_name", "net_contacts__city", "net_contacts__street", "net_contacts__email")
    list_filter = ("net_contacts__city", "supplier")
    readonly_fields = ("created_at",)
    list_select_related = ("supplier", "net_contacts")
    filter_horizontal = ("equipments",)  # удобно выбирать M2M

    def get_contact_city(self, obj):
        return obj.net_contacts.city if obj.net_contacts_id else "-"
    get_contact_city.short_description = "Город"
