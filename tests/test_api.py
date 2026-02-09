"""
Automated API test cases for backend endpoints.

Tests the /api/register and /api/login endpoints directly
using Playwright's request context.

Known bugs tested:
- BUG-019: No CSRF protection on any endpoint
"""

import pytest
from playwright.sync_api import APIRequestContext
from utils.test_data import random_email, API_REGISTER, API_LOGIN


@pytest.fixture
def api_context(playwright) -> APIRequestContext:
    """Create an API request context for direct endpoint testing."""
    context = playwright.request.new_context()
    yield context
    context.dispose()


class TestRegisterAPI:
    """Test /api/register endpoint directly."""

    def test_register_valid_data(self, api_context):
        """TC-A01: POST /api/register with valid data returns success."""
        email = random_email()
        response = api_context.post(API_REGISTER, data={
            "firstName": "API",
            "lastName": "Test",
            "email": email,
            "phone": "0911234567",
            "address": "123 API Street",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        })

        assert response.status == 200, f"Expected 200, got {response.status}"
        data = response.json()
        assert data.get("success") is True, f"Expected success, got: {data}"

    def test_register_duplicate_email(self, api_context):
        """TC-A02: Registering same email twice returns error."""
        email = random_email()
        payload = {
            "firstName": "Dup",
            "lastName": "Test",
            "email": email,
            "phone": "0911234567",
            "address": "123 St",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        }

        # First registration
        resp1 = api_context.post(API_REGISTER, data=payload)
        assert resp1.json().get("success") is True

        # Duplicate
        resp2 = api_context.post(API_REGISTER, data=payload)
        data2 = resp2.json()
        assert data2.get("success") is not True, (
            f"Duplicate email should be rejected, got: {data2}"
        )

    def test_register_missing_fields(self, api_context):
        """TC-A03: Registration with missing required fields."""
        response = api_context.post(API_REGISTER, data={
            "email": random_email(),
        })

        # Should handle gracefully (not crash)
        assert response.status in (200, 400, 422), (
            f"Unexpected status code: {response.status}"
        )

    def test_register_response_structure(self, api_context):
        """TC-A04: Register response contains expected fields."""
        email = random_email()
        response = api_context.post(API_REGISTER, data={
            "firstName": "Struct",
            "lastName": "Test",
            "email": email,
            "phone": "0911234567",
            "address": "123 St",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        })

        data = response.json()
        assert "success" in data, "Response should contain 'success' field"


class TestLoginAPI:
    """Test /api/login endpoint directly."""

    def test_login_valid_credentials(self, api_context):
        """TC-A05: POST /api/login with valid credentials returns success."""
        email = random_email()
        # Register first
        api_context.post(API_REGISTER, data={
            "firstName": "Login",
            "lastName": "Test",
            "email": email,
            "phone": "0911234567",
            "address": "123 St",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        })

        # Login
        response = api_context.post(API_LOGIN, data={
            "email": email,
            "password": "SecurePass123!",
        })

        data = response.json()
        assert data.get("success") is True, f"Login should succeed, got: {data}"

    def test_login_wrong_password(self, api_context):
        """TC-A06: Login with wrong password returns error."""
        email = random_email()
        api_context.post(API_REGISTER, data={
            "firstName": "Wrong",
            "lastName": "Pwd",
            "email": email,
            "phone": "0911234567",
            "address": "123 St",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        })

        response = api_context.post(API_LOGIN, data={
            "email": email,
            "password": "WrongPassword!",
        })

        data = response.json()
        assert data.get("success") is not True, (
            f"Wrong password should fail, got: {data}"
        )

    def test_login_nonexistent_email(self, api_context):
        """TC-A07: Login with non-existent email returns error."""
        response = api_context.post(API_LOGIN, data={
            "email": "nonexistent_api_test_12345@example.com",
            "password": "SomePassword123!",
        })

        data = response.json()
        assert data.get("success") is not True

    def test_login_response_contains_user_data(self, api_context):
        """TC-A08: Successful login response contains user object."""
        email = random_email()
        api_context.post(API_REGISTER, data={
            "firstName": "Data",
            "lastName": "Check",
            "email": email,
            "phone": "0911234567",
            "address": "123 St",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        })

        response = api_context.post(API_LOGIN, data={
            "email": email,
            "password": "SecurePass123!",
        })

        data = response.json()
        assert "user" in data, "Login response should contain 'user' field"
        assert data["user"].get("email") == email

    def test_no_csrf_token_required(self, api_context):
        """TC-A09: BUG - API accepts requests without CSRF token.

        No CSRF protection means the API is vulnerable to
        Cross-Site Request Forgery attacks.
        """
        email = random_email()
        # This request has no CSRF token - should ideally be rejected
        response = api_context.post(API_REGISTER, data={
            "firstName": "CSRF",
            "lastName": "Test",
            "email": email,
            "phone": "0911234567",
            "address": "123 St",
            "city": "Split",
            "zipCode": "21000",
            "password": "SecurePass123!",
        })

        # BUG: Request succeeds without CSRF token
        data = response.json()
        assert data.get("success") is not True, (
            "BUG: API accepts requests without CSRF token - "
            "vulnerable to Cross-Site Request Forgery"
        )
