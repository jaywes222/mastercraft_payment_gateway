# mastercraft_payment_gateway

A Django RESTful API service for initiating and verifying payments using Paystack.  
This service is designed for small businesses to easily accept payments with a modular and scalable architecture.

The API is hosted on Render at https://mastercraft-payment-gateway.onrender.com It has the following two endpoints as per the specification:
GET /api/v1/payments/{id}
POST /api/v1/payments/

---

## Features

- Initiate payments via Paystack API  
- Verify payment status  
- Input validation using DRF serializers  
- Unit and integration tests with mocks  
- Ready for CI/CD deployment  

---

## Table of Contents

- [mastercraft\_payment\_gateway](#mastercraft_payment_gateway)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Running the Service Locally](#running-the-service-locally)
  - [Understanding the Tests](#understanding-the-tests)
  - [GitHub Actions Workflow (CI/CD)](#github-actions-workflow-cicd)
  - [Project Structure](#project-structure)
  - [🌐 Live Deployment](#-live-deployment)
  - [API Access with Versioning](#api-access-with-versioning)
    - [🔹 Base URL](#-base-url)
    - [⚙️ ALLOWED\_HOSTS Setup](#️-allowed_hosts-setup)
---

## Running the Service Locally

1. **Clone the repository**

    ```bash
    git clone https://github.com/jaywes222/mastercraft_payment_gateway.git
    cd payment_gateway
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv penv

    # Windows
    .\penv\Scripts\activate

    # Git Bash
    source penv/Scripts/activate

    # macOS/Linux
    source penv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**

    Create a `.env` file or export these variables:

    ```env
    PAYSTACK_SECRET_KEY=your_paystack_secret_key
    DJANGO_SECRET_KEY=your_django_secret_key
    DEBUG=True        # Set False for production
    ALLOWED_HOSTS=[]  # Add your hostnames or IPs here
    ```

5. **Run migrations**

    ```bash
    python manage.py migrate
    ```

6. **Run the development server**

    ```bash
    python manage.py runserver
    ```

7. **Test the endpoint**

    Use `curl`, Postman, or any HTTP client to POST to:

    ```
    http://localhost:8000/api/vi/payments
    ```

    with the appropriate JSON payload.

---

## Understanding the Tests

- Tests use Django REST Framework testing tools and `unittest.mock` to mock external API calls.
- Test location: `payments/tests.py`
- Types of tests:
  - Unit tests: Mock Paystack API to test views and serializers independently.
  - Integration tests: Verify the entire payment initiation flow.
- Tests verify:
  - HTTP status codes (200 for success, 400 for validation or initiation failure)
  - Response structure and data correctness
- Run tests:

    ```bash
    python manage.py test payments
    ```

---

## GitHub Actions Workflow (CI/CD)

- Triggers on every push or pull request to `main` and `release` branches.
- Runs tests automatically.
- Optionally builds and lints code (if configured).
- On merge to `main` or `release` branches:
  - Deploys to your hosting platform (e.g., Render, Netlify, Heroku, AWS, Azure).

- Workflow config located at `.github/workflows/ci-cd.yml`:

    ```yaml
    name: CI/CD Pipeline

    on:
      push:
        branches:
          - main
          - release
      pull_request:

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.12'
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
          - name: Run tests
            run: python manage.py test
      deploy:
        needs: test
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/release'
        steps:
          - uses: actions/checkout@v3
          # Add your deployment steps here 
          - name: Deploy to Platform
            run: |
              echo "Deploy commands here"
    ```

- **Important:**  
  Store your Paystack API keys, Django secret key, and any deployment credentials securely as GitHub repository secrets (Settings > Secrets and variables).

---

## Project Structure
payment_gateway/
├── payments/
│   ├── migrations/
│   ├── tests.py
│   ├── views.py
│   ├── serializers.py
│   ├── models.py
│   └── ...
├── payment_gateway/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
├── requirements.txt
└── README.md


---

## 🌐 Live Deployment

The API is deployed and accessible publicly at:

**🔗 [https://mastercraft-payment-gateway.onrender.com](https://mastercraft-payment-gateway.onrender.com)**

---

## API Access with Versioning

All endpoints are prefixed with a version for scalability.  
**Current version: `v1`**

### 🔹 Base URL

  ```
    https://mastercraft-payment-gateway.onrender.com/api/v1/
    ```


### 🔹 Example Endpoints

#### Initiate Payment

```http
POST https://mastercraft-payment-gateway.onrender.com/api/v1/payments

** Request Payload **
```bash
{
  "email": "customer@example.com",
  "amount": 5000
}
```

** Verify Payment **
```http
    GET https://mastercraft-payment-gateway.onrender.com/api/v1/payments/{id}
```

### ⚙️ ALLOWED_HOSTS Setup 

** In settings.py
```bash
ALLOWED_HOSTS = [
    'mastercraft-payment-gateway.onrender.com',
    'localhost',
    '127.0.0.1',
]
```












