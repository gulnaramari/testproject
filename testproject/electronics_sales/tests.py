from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contact, SaleNet, Equipment
from users.models import User


class SaleNetAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="gulnara")

        self.contact = Contact.objects.create(
            email="contact@example.com",
            country="Россия",
            city="Казань",
            street="Пушкинская",
            house_number="33"
        )

        self.equipment = Equipment.objects.create(
            equipment_name="Laptop",
            equipment_model="rt",
            market_release_date="2025-04-01"
        )

        self.network = SaleNet.objects.create(
            net_name="Test 1",
            arrears="0.00",
            net_contacts=self.contact
        )
        self.network.equipments.add(self.equipment)

        self.client.force_authenticate(user=self.user)

    def test_create_network(self):
        url = reverse("electronics_sales:salenets-create")
        data = {
            "net_name": "New Network",
            "net_contacts": self.contact.id,
            "equipments": [self.equipment.id],
            "supplier": None,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["net_name"], data["net_name"])

    def test_list_networks(self):
        url = reverse("electronics_sales:salenets-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        # если пагинации нет — data это список; если есть — dict с ключом "results"
        results = data if isinstance(data, list) else data.get("results", [])
        self.assertGreaterEqual(len(results), 1)

    def test_retrieve_network(self):
        url = reverse("electronics_sales:salenets-detail", args=[self.network.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["net_name"], self.network.net_name)

    def test_update_network(self):
        url = reverse("electronics_sales:salenets-update", args=[self.network.id])
        data = {
            "net_name": "Updated Network",
            "net_contacts": self.contact.id,
            "equipments": [self.equipment.id],
            "supplier": None,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["net_name"], "Updated Network")

    def test_delete_network(self):
        url = reverse("electronics_sales:salenets-destroy", args=[self.network.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SaleNet.objects.filter(id=self.network.id).exists())

    def test_partial_update_network(self):
        url = reverse("electronics_sales:salenets-update", args=[self.network.id])
        data = {"net_name": "Test Update"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["net_name"], "Test Update")


class SaleNetModelTest(TestCase):
    def setUp(self):
        self.net0 = SaleNet.objects.create(net_name="Завод", arrears="0.00")
        self.net1 = SaleNet.objects.create(net_name="Уровень 1", arrears="0.00", supplier=self.net0)
        self.net2 = SaleNet.objects.create(net_name="Уровень 2", arrears="0.00", supplier=self.net1)

    def test_supplier_wrong(self):
        self.net0.supplier = self.net0
        with self.assertRaises(ValidationError) as cm:
            self.net0.clean()
        self.assertIn("Поставщик не может быть самим собой", cm.exception.message_dict["supplier"][
            0])

    def test_cycle_detection(self):
        self.net0.supplier = self.net2
        self.net0.save()
        with self.assertRaises(ValidationError) as cm:
            self.net1.supplier = self.net0
            self.net1.clean()
        self.assertIn("Обнаружен цикл в цепочке поставщиков", cm.exception.message_dict["supplier"][
            0])

    def test_valid_structure_does_not_raise(self):
        try:
            self.net2.clean()
        except ValidationError:
            self.fail("ValidationError")


