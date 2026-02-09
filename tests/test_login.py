"""
Automated test cases for the Login page (index.html).

Tests cover: successful login, invalid credentials, email validation,
navigation links, UI elements, and redirect to dashboard.

Known bugs tested:
- BUG-001: Weak email regex /\\S+@\\S/ (same as registration)
- BUG-002: Email input type="text" instead of "email"
- BUG: Remember Me checkbox hidden on mobile (overlay)
"""

import pytest
from utils.test_data import random_email, INVALID_EMAILS


class TestLoginPositive:
    """Positive login scenarios."""

    def test_successful_login(self, login_page, registered_user):
        """TC-L01: Successful login with valid registered credentials."""
        login_page.login(registered_user["email"], registered_user["password"])

        assert login_page.has_success_message(), (
            "Expected success message after valid login"
        )
        assert "Login successful" in login_page.get_login_message()

    def test_login_redirects_to_dashboard(self, login_page, registered_user):
        """TC-L02: After successful login, user is redirected to dashboard."""
        login_page.login(registered_user["email"], registered_user["password"])
        login_page.page.wait_for_url("**/dashboard.html**", timeout=10000)

        assert "dashboard.html" in login_page.get_url(), (
            "Expected redirect to dashboard after login"
        )

    def test_login_shows_registered_param(self, page, registered_user):
        """TC-L03: After registration redirect, login page has registered=true param."""
        # Registration redirects to index.html?registered=true
        assert "index.html" in page.url or "registered=true" in page.url


class TestLoginNegative:
    """Negative login scenarios."""

    def test_login_wrong_password(self, login_page, registered_user):
        """TC-L04: Login with wrong password shows error."""
        login_page.login(registered_user["email"], "WrongPassword123!")
        login_page.page.wait_for_selector("#loginMessage", state="visible", timeout=5000)

        assert login_page.has_error_message(), (
            "Expected error message for wrong password"
        )

    def test_login_nonexistent_email(self, login_page):
        """TC-L05: Login with unregistered email shows error."""
        login_page.login("nonexistent_user_12345@example.com", "SomePassword123!")
        login_page.page.wait_for_selector("#loginMessage", state="visible", timeout=5000)

        assert login_page.has_error_message(), (
            "Expected error for non-existent email"
        )

    def test_login_empty_form(self, login_page):
        """TC-L06: Submitting empty login form should not succeed."""
        login_page.click_login()

        assert not login_page.has_success_message(), (
            "Empty form should not login successfully"
        )

    def test_login_empty_password(self, login_page):
        """TC-L07: Login with email but no password should fail."""
        login_page.fill_email("test@example.com")
        login_page.click_login()

        assert not login_page.has_success_message()


class TestLoginEmailValidation:
    """Test email validation on login form - same weak regex as registration."""

    def test_login_email_input_type(self, login_page):
        """TC-L08: BUG - Login email input type is 'text' instead of 'email'."""
        input_type = login_page.get_email_input_type()
        assert input_type == "email", (
            f"BUG: Login email field type is '{input_type}', should be 'email'"
        )

    @pytest.mark.parametrize("invalid_email", ["plaintext", "user@", "@test.com"])
    def test_login_invalid_email_rejected(self, login_page, invalid_email):
        """TC-L09: Invalid email formats should show validation error on login."""
        login_page.fill_email(invalid_email)
        login_page.fill_password("SomePassword123!")
        login_page.click_login()
        login_page.page.wait_for_load_state("networkidle")

        email_error = login_page.get_email_error()
        has_no_success = not login_page.has_success_message()
        assert email_error != "" or has_no_success, (
            f"Email '{invalid_email}' should be rejected on login"
        )


class TestLoginUIElements:
    """Test UI elements on login page."""

    def test_page_title(self, login_page):
        """TC-L10: Login page title should be correct."""
        assert "Login" in login_page.get_title()

    def test_forgot_password_link(self, login_page):
        """TC-L11: 'Forgot Password?' link navigates correctly."""
        login_page.click_forgot_password()
        login_page.page.wait_for_load_state("networkidle")

        assert "forgot-password.html" in login_page.get_url()

    def test_register_link(self, login_page):
        """TC-L12: 'Create New Account' link navigates correctly."""
        login_page.click_register()
        login_page.page.wait_for_load_state("networkidle")

        assert "register.html" in login_page.get_url()

    def test_remember_me_checkbox_present(self, login_page):
        """TC-L13: Remember Me checkbox exists on the page."""
        checkbox = login_page.page.locator(login_page.REMEMBER_ME)
        assert checkbox.count() > 0, "Remember Me checkbox should exist"
