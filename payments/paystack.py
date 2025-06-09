from django.conf import settings
import requests

class PaystackAPI:
    BASE_URL = settings.PAYSTACK_BASE_URL
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    HEADERS = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    @classmethod
    def initiate_payment(cls, email, amount, name):
        url = f"{cls.BASE_URL}/transaction/initialize"
        payload = {
            "email": email,
            "amount": int(amount * 100),
            "metadata": {
                "custom_fields": [
                    {"display_name": "Customer Name", "value": name}
                    ]
                }
        }
        response = requests.post(url, json=payload, headers=cls.HEADERS)
        return response.json()
    
    @classmethod
    def verify_payment(cls, reference):
        url = f"{cls.BASE_URL}/transaction/verify/{reference}"
        response = requests.get(url, headers=cls.HEADERS)
        return response.json()
    