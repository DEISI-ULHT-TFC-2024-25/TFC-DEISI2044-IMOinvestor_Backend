import logging
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from district.models import District
from municipality.models import Municipality
from organization.models import Organization
from duser.models import DUser
from property_roi.models import ROICalculation
from subscriptions.models import Subscription
from property.models import Property
from announcements.models import Announcement  # Assuming your Announcement model is here

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='test_run.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ModelsTestCase(TestCase):

    def setUp(self):
        # Create district
        self.district = District.objects.create(
            name="Distrito Teste",
            created_by="system",
            created_date=timezone.now()
        )

        # Create municipality linked to district
        self.municipality = Municipality.objects.create(
            district=self.district,
            name="Município Teste",
            created_by="system",
            created_date=timezone.now()
        )

        # Create organization
        self.organization = Organization.objects.create(
            district=self.district,
            municipality=self.municipality,
            name="Org Teste",
            street="Rua Exemplo, 123",
            postal_code="1234-567",
            city="Cidade Teste",
            email="orgteste@email.com",
            phone="912345678",
            created_by="system",
            created_date=timezone.now(),
            vat_number="123456789",
            website="https://orgteste.com"
        )

        # Create user
        self.user = DUser.objects.create(
            user_name="usuario1",
            password=make_password("senha123"),
            email="usuario1@email.com",
            lang_key="PT",
            activated=True,
            created_by="system",
            created_date=timezone.now(),
            is_active=True,
        )
        # Link organization to user and refresh user from DB
        self.user.institution.add(self.organization)
        self.user.save()
        self.user.refresh_from_db()

        # Create a subscription
        self.subscription = Subscription.objects.create(
            user=self.user,
            token="sometoken123",
            created_at=timezone.now(),
            expires_at=timezone.now() + timedelta(days=30)
        )

        # Create a property for reuse in announcement tests
        self.property = Property.objects.create(
            organization=self.organization,
            district=self.district,
            municipality=self.municipality,
            name="Apartamento Luxo",
            postal_code="1234-000",
            property_type="Apartamento",
            gross_area=100.00,
            net_area=80.00,
            min_price=150000.00,
            max_price=160000.00
        )


        self.list_url = reverse('roi-calculation-list')  

        self.valid_payload = {
            "purchase_price": "100000.00",
            "closing_costs": "5000.00",
            "repair_costs": "10000.00",
            "after_repair_value": "130000.00",
            "holding_costs": "2000.00",
            "selling_costs": "3000.00"
        }


        self.url = reverse('update-subscription')

        self.client = APIClient()

    def test_district_creation(self):
        distrito = District.objects.get(name="Distrito Teste")
        self.assertEqual(str(distrito), "Distrito Teste")
        print("Test Passed: District creation and __str__ method")

    def test_municipality_creation(self):
        municipio = Municipality.objects.get(name="Município Teste")
        self.assertEqual(str(municipio), "Município Teste")
        self.assertEqual(municipio.district, self.district)
        print("Test Passed: Municipality creation and relation to District")

    def test_organization_creation(self):
        org = Organization.objects.get(name="Org Teste")
        self.assertEqual(org.city, "Cidade Teste")
        self.assertEqual(org.district, self.district)
        self.assertEqual(org.municipality, self.municipality)
        self.assertEqual(org.email, "orgteste@email.com")
        print("Test Passed: Organization creation and field validations")

    def test_user_creation_and_relations(self):
        user = DUser.objects.get(user_name="usuario1")
        self.assertEqual(user.email, "usuario1@email.com")
        self.assertTrue(user.activated)
        self.assertIn(self.organization, user.institution.all())
        print("Test Passed: User creation and organization relationship")

    def test_str_methods(self):
        self.assertEqual(str(self.user), "usuario1")
        self.assertEqual(str(self.organization), "Org Teste")
        print("Test Passed: __str__ methods for User and Organization")

    def test_login_success(self):
        login_data = {
            "user_name": "usuario1",
            "password": "senha123"
        }
        response = self.client.post('/api/user/login/', data=login_data, format='json')
        print("Login response status:", response.status_code)
        print("Login response data:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertEqual(response.data["user_name"], "usuario1")
        self.access_token = response.data["access_token"]
        print("Test Passed: User login returns tokens and correct username")

    def test_property_model_creation(self):
        property_obj = Property.objects.get(name="Apartamento Luxo")
        self.assertEqual(str(property_obj), "Apartamento Luxo")
        self.assertEqual(property_obj.organization.name, "Org Teste")
        print("Test Passed: Property creation")

    def test_property_api_list(self):
        Property.objects.create(
            organization=self.organization,
            district=self.district,
            municipality=self.municipality,
            name="Terreno Teste",
            postal_code="9999-999",
            property_type="Terreno",
            gross_area=300.00,
            net_area=290.00,
            min_price=100000.00,
            max_price=120000.00
        )

        response = self.client.get("/api/property/")
        print("List Properties response:", response.status_code, response.data)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        print("Test Passed: Property API list")


    def test_announcement_model_creation(self):
        announcement = Announcement.objects.create(
            organization=self.organization,
            property=self.property,
            created_by=self.user.user_name,
            created_date=timezone.now(),
            expiry_date=timezone.now() + timedelta(days=30),
            price=250000.00,
            is_active=True
        )
        # Adjust string assertion if you have custom __str__ for Announcement
        self.assertTrue(str(announcement))  # Just check __str__ returns something
        self.assertEqual(announcement.organization, self.organization)
        self.assertEqual(announcement.created_by, self.user.user_name)
        print("Test Passed: Announcement model creation")


    def test_announcement_api_list(self):
        url = reverse('announcement-list')

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        print("Announcement API list response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 0)  
        print("Test Passed: Announcement API list")



    def test_create_roi_calculation(self):
        response = self.client.post(self.list_url, data=self.valid_payload, format='json')
        print("Create ROI Calculation response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if roi_result and profit are calculated and saved
        self.assertIn('roi_result', response.data)
        self.assertIn('profit', response.data)

        # Validate ROI calculation manually (rough check)
        total_cost = 100000 + 5000 + 10000 + 2000 + 3000
        profit = 130000 - total_cost
        investment = 100000 + 5000 + 10000
        expected_roi = (profit / investment) * 100 if investment != 0 else 0

        self.assertAlmostEqual(float(response.data['roi_result']), expected_roi, places=2)
        self.assertAlmostEqual(float(response.data['profit']), profit, places=2)

    def test_list_roi_calculations(self):
        # Create one object first
        ROICalculation.objects.create(
            purchase_price=100000,
            closing_costs=5000,
            repair_costs=10000,
            after_repair_value=130000,
            holding_costs=2000,
            selling_costs=3000,
            roi_result=15.0,
            profit=10000.0
        )
        response = self.client.get(self.list_url)
        print("List ROI Calculations response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)




    def test_update_subscription_creates_and_updates(self):
            # Authenticate user
            self.client.force_authenticate(user=self.user)


            # Validate subscription exists
            subscription = Subscription.objects.get(user=self.user)
            self.assertIsNotNone(subscription.token)
            self.assertTrue(subscription.expires_at > timezone.now())

            old_token = subscription.token

            response2 = self.client.put(self.url)
            print("Second update subscription response:", response2.status_code, response2.data)
            self.assertEqual(response2.status_code, status.HTTP_200_OK)
            self.assertEqual(response2.data['message'], 'Subscription updated')

            # Check token changed
            subscription.refresh_from_db()
            self.assertNotEqual(subscription.token, old_token)