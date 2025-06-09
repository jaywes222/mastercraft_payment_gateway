from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

class InitiatePaymentViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:initiate_payment')
        self.valid_payload = {
            "customer_name": "Jane Doe",
            "customer_email": "jane@example.com",
            "amount": 100.00
        }
        self.invalid_payload = {
            "customer_name": "",
            "customer_email": "invalid-email",
            "amount": -10
        }
        
    
    @patch('payments.paystack.PaystackAPI.initiate_payment')
    def test_initiate_payment_success(self, mock_initiate):
        mock_initiate.return_value = {
            "status": True,
            "message": "Authorization URL created",
            "data": {
                "reference": "abc123",
                "authorization_url": "https://paystack.com/pay/abc123"
            }
        }

        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['status'])
        self.assertIn('data', response.json())
    
    
    @patch('payments.paystack.PaystackAPI.initiate_payment')
    def test_initiate_payment_failure(self, mock_initiate):
        mock_initiate.return_value = {
            "status": False,
            "message": "Invalid data"
        }

        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_initiate_payment_invalid_payload(self):
        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class PaymentStatusViewTests(APITestCase):
    def setUp(self):
        self.valid_reference = 'abc123'
        self.invalid_reference = 'invalidref'
        self.url_valid = reverse('api:payment_status', kwargs={'payment_id': self.valid_reference})
        self.url_invalid = reverse('api:payment_status', kwargs={'payment_id': self.invalid_reference})


        from payments.models import Payment
        Payment.objects.create(
            reference=self.valid_reference,
            customer_name="Jane Doe",
            customer_email="jane@example.com",
            amount=100.00,
            status="pending"
        )

    @patch('payments.paystack.PaystackAPI.verify_payment')
    def test_payment_status_success(self, mock_verify):
        mock_verify.return_value = {
            "status": True,
            "data": {
                "status": "success",
                "reference": self.valid_reference,
                "amount": 10000,
                "customer": {
                    "email": "jane@example.com",
                    "name": "Jane Doe"
                }
            }
        }

        response = self.client.get(self.url_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['payment']['id'], self.valid_reference)
        self.assertEqual(response.json()['payment']['status'], 'success')

    def test_payment_status_not_found(self):
        response = self.client.get(self.url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('payments.paystack.PaystackAPI.verify_payment')
    def test_payment_status_failure(self, mock_verify):
        mock_verify.return_value = {
            "status": False,
            "message": "Transaction not found"
        }

        response = self.client.get(self.url_valid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


