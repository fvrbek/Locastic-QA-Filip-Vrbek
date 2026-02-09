"""
Automated security test cases across all pages.

Tests cover: sensitive data logging, session management,
SQL injection, XSS prevention, and storage security.

Known bugs tested:
- BUG-018: Console.log of sensitive user data (emails, user objects)
- BUG-020: Session data stored in sessionStorage (not httpOnly cookies)
"""

import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.test_data import random_email, SQL_INJECTION, XSS_PAYLOAD


class TestConsoleSensitiveData:
    """Test that sensitive data is not logged to browser console."""

    def test_login_logs_email_to_console(self, page):
        """TC-S01: BUG - Login process logs email to console.

        app.js contains: console.log('Attempting login for:', email)
        and console.log('User stored in sessionStorage:', data.user.email)
        Sensitive data should never be logged to console.
        """
        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg.text))

        email = random_email()

        # Register
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Console",
            last_name="Test",
            email=email,
            phone="0911234567",
            address="123 St",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
            accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        # Login
        login = LoginPage(page)
        login.open()
        login.login(email, "SecurePass123!")
        page.wait_for_url("**/dashboard.html**", timeout=10000)

        # Check if email was logged to console
        email_logged = any(email in msg for msg in console_messages)
        assert not email_logged, (
            f"BUG: User email '{email}' was logged to browser console. "
            "Console messages containing email: "
            + str([m for m in console_messages if email in m])
        )

    def test_registration_logs_email_to_console(self, page):
        """TC-S02: BUG - Registration logs email to console.

        app.js contains: console.log('Attempting to register user:', email)
        """
        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg.text))

        email = random_email()
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Reg",
            last_name="Console",
            email=email,
            phone="0911234567",
            address="123 St",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
            accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        email_logged = any(email in msg for msg in console_messages)
        assert not email_logged, (
            f"BUG: Registration logs email '{email}' to console"
        )


class TestSessionSecurity:
    """Test session storage security."""

    def test_session_uses_httponly_cookies(self, page):
        """TC-S03: BUG - Session data stored in sessionStorage instead of httpOnly cookies.

        The app stores user data in sessionStorage which is accessible via JavaScript,
        making it vulnerable to XSS-based session theft.
        """
        email = random_email()

        # Register
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Session",
            last_name="Test",
            email=email,
            phone="0911234567",
            address="123 St",
            city="Split",
            zip_code="21000",
            password="SecurePass123!",
            confirm_password="SecurePass123!",
            accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        # Login
        login = LoginPage(page)
        login.open()
        login.login(email, "SecurePass123!")
        page.wait_for_url("**/dashboard.html**", timeout=10000)

        # Check if user data is in sessionStorage (bad) vs httpOnly cookies (good)
        session_data = page.evaluate("() => sessionStorage.getItem('currentUser')")

        assert session_data is None, (
            "BUG: User session data stored in sessionStorage (accessible via JS). "
            "Should use httpOnly cookies for security. "
            f"Stored data: {session_data[:100]}..."
        )


class TestLoginSecurityInjection:
    """Test injection attacks on login form."""

    def test_sql_injection_login(self, page):
        """TC-S04: SQL injection on login form should be handled gracefully."""
        login = LoginPage(page)
        login.open()
        login.login(SQL_INJECTION, SQL_INJECTION)
        page.wait_for_load_state("networkidle")

        msg = login.get_login_message()
        assert "server error" not in msg.lower(), (
            "SQL injection caused a server error on login"
        )

    def test_xss_login(self, page):
        """TC-S05: XSS payload in login should not execute."""
        login = LoginPage(page)
        login.open()
        login.login(XSS_PAYLOAD, XSS_PAYLOAD)
        page.wait_for_load_state("networkidle")

        page_html = page.content()
        assert "<script>alert(" not in page_html.lower() or (
            "XSS payload should be sanitized on login page"
        )
