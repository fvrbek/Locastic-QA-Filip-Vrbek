"""
Automated test cases for the Forgot Password page (forgot-password.html).

Tests cover: password reset flow, email validation, security questions,
navigation links, and known bugs.

Known bugs tested:
- BUG-012: Always shows fake success message regardless of email
- BUG-013: Security answer is never validated
- BUG-001: Weak email regex (shared bug)
"""

import pytest
from utils.test_data import random_email, SECURITY_QUESTIONS


class TestForgotPasswordFlow:
    """Test the password reset flow."""

    def test_reset_with_valid_email(self, forgot_password_page):
        """TC-FP01: Submitting valid email shows success message."""
        forgot_password_page.fill_email("existing@example.com")
        forgot_password_page.click_send_reset()

        assert forgot_password_page.has_success_message()
        assert "reset link" in forgot_password_page.get_message().lower()

    def test_reset_with_nonexistent_email_still_succeeds(self, forgot_password_page):
        """TC-FP02: BUG - Non-existent email still shows success (fake reset)."""
        forgot_password_page.fill_email("absolutely_fake_email_999@nonexistent.xyz")
        forgot_password_page.click_send_reset()

        # BUG: Should show error for non-existent email
        # Actual: Shows success "Password reset link has been sent to your email!"
        assert not forgot_password_page.has_success_message(), (
            "BUG: Fake success shown for non-existent email - "
            "no actual verification of email existence"
        )

    def test_security_answer_not_validated(self, forgot_password_page):
        """TC-FP03: BUG - Security answer is never checked."""
        forgot_password_page.fill_email("test@example.com")
        forgot_password_page.select_security_question("pet")
        forgot_password_page.fill_security_answer("COMPLETELY WRONG ANSWER 12345")
        forgot_password_page.click_send_reset()

        # BUG: Should verify answer against stored data
        # Actual: Ignores security answer entirely
        assert not forgot_password_page.has_success_message(), (
            "BUG: Wrong security answer accepted - answer is never validated"
        )

    def test_reset_without_security_answer(self, forgot_password_page):
        """TC-FP04: Reset works even with empty security answer."""
        forgot_password_page.fill_email("test@example.com")
        forgot_password_page.select_security_question("city")
        # Intentionally leave security answer empty
        forgot_password_page.click_send_reset()

        # This should technically work since security question is optional
        msg = forgot_password_page.get_message()
        assert msg != "", "Should show some message after submission"


class TestForgotPasswordValidation:
    """Test form validation on forgot password page."""

    def test_empty_email_rejected(self, forgot_password_page):
        """TC-FP05: Empty email should not submit."""
        forgot_password_page.click_send_reset()

        assert not forgot_password_page.has_success_message()

    def test_invalid_email_rejected(self, forgot_password_page):
        """TC-FP06: Invalid email format should show error."""
        forgot_password_page.fill_email("plaintext")
        forgot_password_page.click_send_reset()

        email_error = forgot_password_page.get_email_error()
        has_no_success = not forgot_password_page.has_success_message()
        assert email_error != "" or has_no_success

    def test_email_input_type(self, forgot_password_page):
        """TC-FP07: BUG - Email input type is 'text' instead of 'email'."""
        input_type = forgot_password_page.get_email_input_type()
        assert input_type == "email", (
            f"BUG: Forgot password email type is '{input_type}', should be 'email'"
        )


class TestForgotPasswordSecurityQuestions:
    """Test security question dropdown."""

    def test_security_question_has_correct_options(self, forgot_password_page):
        """TC-FP08: Security question dropdown has expected options."""
        options = forgot_password_page.get_security_question_options()

        assert "Select a question" in options
        assert "What was your first pet's name?" in options
        assert "What city were you born in?" in options
        assert "What was your high school name?" in options

    def test_security_question_is_optional(self, forgot_password_page):
        """TC-FP09: Security question is labeled as optional."""
        label = forgot_password_page.page.locator("label[for='securityQuestion']")
        assert "Optional" in label.text_content()


class TestForgotPasswordNavigation:
    """Test navigation links."""

    def test_back_to_login_link(self, forgot_password_page):
        """TC-FP10: 'Back to Login' link navigates to login page."""
        forgot_password_page.click_login_link()
        forgot_password_page.page.wait_for_load_state("networkidle")

        assert "index.html" in forgot_password_page.get_url()

    def test_create_account_link(self, forgot_password_page):
        """TC-FP11: 'Create New Account' link navigates to register page."""
        forgot_password_page.click_register_link()
        forgot_password_page.page.wait_for_load_state("networkidle")

        assert "register.html" in forgot_password_page.get_url()

    def test_page_title(self, forgot_password_page):
        """TC-FP12: Page title should mention Forgot Password."""
        assert "Forgot Password" in forgot_password_page.get_title()
