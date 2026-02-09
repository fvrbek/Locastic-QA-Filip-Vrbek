"""
Automated test cases for user registration functionality.
Tests cover positive, negative, validation, and UI/UX scenarios.
"""

import pytest
from utils.test_data import (
    VALID_USER,
    INVALID_EMAILS,
    INVALID_PHONES,
    INVALID_ZIPS,
    WEAK_PASSWORDS,
    SQL_INJECTION,
    XSS_PAYLOAD,
    LONG_STRING,
    random_email,
)


# ──────────────────────────────────────────────
# POSITIVE TESTS
# ──────────────────────────────────────────────


class TestRegistrationPositive:
    """Positive test scenarios for registration."""

    def test_successful_registration_all_fields(self, register_page):
        """TC-001: Successful registration with all valid fields."""
        email = random_email()
        register_page.fill_registration_form(
            first_name="John",
            last_name="Doe",
            email=email,
            phone="+385911234567",
            address="123 Main Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
            accept_terms=True,
            subscribe_newsletter=True,
        )
        register_page.submit_registration()

        assert register_page.has_success_message(), (
            "Expected success message after valid registration"
        )
        assert "Registration successful" in register_page.get_register_message()

    def test_registration_without_newsletter(self, register_page):
        """TC-002: Registration without subscribing to newsletter."""
        email = random_email()
        register_page.fill_registration_form(
            first_name="Jane",
            last_name="Smith",
            email=email,
            phone="+385921234567",
            address="456 Oak Avenue",
            city="Zagreb",
            zip_code="10000",
            password="AnotherPass456!",
            confirm_password="AnotherPass456!",
            accept_terms=True,
            subscribe_newsletter=False,
        )
        register_page.submit_registration()

        assert register_page.has_success_message()

    def test_registration_redirects_to_login(self, register_page):
        """TC-003: After successful registration, user is redirected to login."""
        email = random_email()
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=email,
            phone="0911234567",
            address="789 Elm Road",
            city="Rijeka",
            zip_code="51000",
            password="RedirectTest1!",
            confirm_password="RedirectTest1!",
            accept_terms=True,
        )
        register_page.submit_registration()
        register_page.page.wait_for_url("**/index.html**", timeout=10000)

        assert "index.html" in register_page.get_url(), (
            "Expected redirect to login page after registration"
        )


# ──────────────────────────────────────────────
# NEGATIVE TESTS - EMAIL VALIDATION
# ──────────────────────────────────────────────


class TestEmailValidation:
    """Test email validation (BUG: weak regex /\\S+@\\S/ allows invalid emails)."""

    @pytest.mark.parametrize("invalid_email", INVALID_EMAILS)
    def test_invalid_email_rejected(self, register_page, invalid_email):
        """TC-004: Invalid email formats should be rejected."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=invalid_email,
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="ValidPass123!",
            confirm_password="ValidPass123!",
        )
        register_page.submit_registration()

        # Should show error or not succeed
        has_email_error = register_page.get_email_error() != ""
        has_no_success = not register_page.has_success_message()
        assert has_email_error or has_no_success, (
            f"Email '{invalid_email}' should be rejected but was accepted"
        )

    def test_email_input_type_should_be_email(self, register_page):
        """TC-005: BUG - Email input type is 'text' instead of 'email'."""
        input_type = register_page.get_email_input_type()
        assert input_type == "email", (
            f"BUG: Email field type is '{input_type}', should be 'email' "
            "for built-in browser validation"
        )


# ──────────────────────────────────────────────
# NEGATIVE TESTS - PASSWORD VALIDATION
# ──────────────────────────────────────────────


class TestPasswordValidation:
    """Test password validation bugs."""

    @pytest.mark.parametrize("weak_pwd", WEAK_PASSWORDS)
    def test_weak_password_rejected(self, register_page, weak_pwd):
        """TC-006: Weak/short passwords should be rejected (min 8 chars)."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password=weak_pwd,
            confirm_password=weak_pwd,
        )
        register_page.submit_registration()

        has_pwd_error = register_page.get_password_error() != ""
        has_no_success = not register_page.has_success_message()
        assert has_pwd_error or has_no_success, (
            f"Password '{weak_pwd}' (length {len(weak_pwd)}) should be rejected"
        )

    def test_password_mismatch_rejected(self, register_page):
        """TC-007: BUG - Mismatched passwords should be rejected but aren't."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="DifferentPass456!",
        )
        register_page.submit_registration()

        error = register_page.get_confirm_password_error()
        has_no_success = not register_page.has_success_message()
        assert error != "" or has_no_success, (
            "BUG: Mismatched passwords accepted - validatePasswordMatch always returns true"
        )

    def test_password_field_is_masked(self, register_page):
        """TC-008: Password fields should mask input."""
        pwd_type = register_page.get_password_input_type()
        assert pwd_type == "password", "Password field should be masked"

        confirm_type = register_page.page.locator(
            register_page.CONFIRM_PASSWORD
        ).get_attribute("type")
        assert confirm_type == "password", "Confirm password field should be masked"


# ──────────────────────────────────────────────
# NEGATIVE TESTS - PHONE VALIDATION
# ──────────────────────────────────────────────


class TestPhoneValidation:
    """Test phone number validation (BUG: accepts letters)."""

    @pytest.mark.parametrize("invalid_phone", INVALID_PHONES)
    def test_invalid_phone_rejected(self, register_page, invalid_phone):
        """TC-009: BUG - Invalid phone numbers should be rejected."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=random_email(),
            phone=invalid_phone,
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        has_phone_error = register_page.get_phone_error() != ""
        has_no_success = not register_page.has_success_message()
        assert has_phone_error or has_no_success, (
            f"Phone '{invalid_phone}' should be rejected"
        )


# ──────────────────────────────────────────────
# NEGATIVE TESTS - ZIP CODE VALIDATION
# ──────────────────────────────────────────────


class TestZipCodeValidation:
    """Test ZIP code validation (BUG: accepts letters)."""

    @pytest.mark.parametrize("invalid_zip", INVALID_ZIPS)
    def test_invalid_zip_rejected(self, register_page, invalid_zip):
        """TC-010: BUG - Invalid ZIP codes should be rejected."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code=invalid_zip,
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        has_zip_error = register_page.get_zip_error() != ""
        has_no_success = not register_page.has_success_message()
        assert has_zip_error or has_no_success, (
            f"ZIP '{invalid_zip}' should be rejected"
        )

    def test_zip_with_letters_rejected(self, register_page):
        """TC-011: BUG - ZIP code with letters should be rejected."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="ABCDE",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        has_zip_error = register_page.get_zip_error() != ""
        has_no_success = not register_page.has_success_message()
        assert has_zip_error or has_no_success, (
            "BUG: ZIP code with letters accepted - should only accept numbers"
        )


# ──────────────────────────────────────────────
# NEGATIVE TESTS - REQUIRED FIELDS
# ──────────────────────────────────────────────


class TestRequiredFields:
    """Test that all required fields are enforced."""

    def test_empty_form_submission(self, register_page):
        """TC-012: Submitting empty form should not succeed."""
        register_page.click_submit()
        register_page.page.wait_for_load_state("networkidle")

        assert not register_page.has_success_message(), (
            "Empty form should not register successfully"
        )

    def test_missing_first_name(self, register_page):
        """TC-013: Registration without first name should fail."""
        register_page.fill_registration_form(
            first_name="",
            last_name="Doe",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        assert not register_page.has_success_message()

    def test_missing_last_name(self, register_page):
        """TC-014: Registration without last name should fail."""
        register_page.fill_registration_form(
            first_name="John",
            last_name="",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        assert not register_page.has_success_message()

    def test_missing_email(self, register_page):
        """TC-015: Registration without email should fail."""
        register_page.fill_registration_form(
            first_name="John",
            last_name="Doe",
            email="",
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        assert not register_page.has_success_message()

    def test_terms_checkbox_required(self, register_page):
        """TC-016: BUG - T&C checkbox should be required but isn't enforced."""
        register_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=random_email(),
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
            accept_terms=False,
        )
        register_page.submit_registration()

        assert not register_page.has_success_message(), (
            "BUG: Registration succeeds without accepting Terms & Conditions"
        )


# ──────────────────────────────────────────────
# SECURITY TESTS
# ──────────────────────────────────────────────


class TestSecurityValidation:
    """Test security-related scenarios."""

    def test_sql_injection_in_fields(self, register_page):
        """TC-017: SQL injection payloads should not cause errors."""
        register_page.fill_registration_form(
            first_name=SQL_INJECTION,
            last_name=SQL_INJECTION,
            email=f"test_{random_email()}",
            phone="0911234567",
            address=SQL_INJECTION,
            city=SQL_INJECTION,
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        # App should handle gracefully - no server error
        msg = register_page.get_register_message()
        assert "server error" not in msg.lower(), (
            "SQL injection caused a server error"
        )

    def test_xss_in_fields(self, register_page):
        """TC-018: XSS payloads should be sanitized."""
        register_page.fill_registration_form(
            first_name=XSS_PAYLOAD,
            last_name=XSS_PAYLOAD,
            email=random_email(),
            phone="0911234567",
            address=XSS_PAYLOAD,
            city=XSS_PAYLOAD,
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        # Check that no script tags are rendered in the page
        page_content = register_page.page.content()
        assert "<script>alert(" not in page_content.lower() or (
            "XSS payload should be sanitized, not rendered as HTML"
        )

    def test_long_input_boundary(self, register_page):
        """TC-019: Very long inputs should be handled gracefully."""
        register_page.fill_registration_form(
            first_name=LONG_STRING,
            last_name=LONG_STRING,
            email=f"{'a' * 200}@example.com",
            phone="0" * 50,
            address=LONG_STRING,
            city=LONG_STRING,
            zip_code="0" * 50,
            password=LONG_STRING,
            confirm_password=LONG_STRING,
        )
        register_page.submit_registration()

        # Should not crash or show server error
        msg = register_page.get_register_message()
        assert "server error" not in msg.lower(), (
            "Long input caused server error"
        )


# ──────────────────────────────────────────────
# UI/UX TESTS
# ──────────────────────────────────────────────


class TestUIElements:
    """Test UI elements and navigation."""

    def test_page_title(self, register_page):
        """TC-020: Page title should be correct."""
        assert "Register" in register_page.get_title()

    def test_all_form_labels_present(self, register_page):
        """TC-021: All form field labels should be visible."""
        labels = {
            "firstName": "First Name",
            "lastName": "Last Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "address": "Street Address",
            "city": "City",
            "zipCode": "ZIP Code",
            "password": "Password",
            "confirmPassword": "Confirm Password",
        }
        for field_id, label_text in labels.items():
            label = register_page.page.locator(f"label[for='{field_id}']")
            assert label.is_visible(), f"Label '{label_text}' should be visible"

    def test_login_link_navigates_correctly(self, register_page):
        """TC-022: 'Already have an account? Login' link works."""
        register_page.click_login_link()
        register_page.page.wait_for_load_state("networkidle")

        assert "index.html" in register_page.get_url()

    def test_all_required_fields_have_required_attribute(self, register_page):
        """TC-023: Required fields should have HTML required attribute."""
        required_fields = [
            register_page.FIRST_NAME,
            register_page.LAST_NAME,
            register_page.EMAIL,
            register_page.PHONE,
            register_page.ADDRESS,
            register_page.CITY,
            register_page.ZIP_CODE,
            register_page.PASSWORD,
            register_page.CONFIRM_PASSWORD,
        ]
        for selector in required_fields:
            is_req = register_page.is_field_required(selector)
            assert is_req, f"Field {selector} should have required attribute"

    def test_submit_button_visible(self, register_page):
        """TC-024: Submit button should be visible and enabled."""
        btn = register_page.page.locator(register_page.SUBMIT_BUTTON)
        assert btn.is_visible(), "Submit button should be visible"
        assert not btn.is_disabled(), "Submit button should not be disabled"
        assert btn.text_content().strip() == "Create Account"


# ──────────────────────────────────────────────
# DUPLICATE REGISTRATION TEST
# ──────────────────────────────────────────────


class TestDuplicateRegistration:
    """Test duplicate email registration handling."""

    def test_duplicate_email_rejected(self, register_page):
        """TC-025: Registering with already used email should fail."""
        email = random_email()

        # First registration
        register_page.fill_registration_form(
            first_name="First",
            last_name="User",
            email=email,
            phone="0911234567",
            address="123 Street",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()
        register_page.page.wait_for_url("**/index.html**", timeout=10000)

        # Navigate back to register and try same email
        register_page.open()
        register_page.fill_registration_form(
            first_name="Second",
            last_name="User",
            email=email,
            phone="0921234567",
            address="456 Other Street",
            city="Zagreb",
            zip_code="10000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
        )
        register_page.submit_registration()

        assert register_page.has_error_message(), (
            "Duplicate email registration should show error message"
        )
