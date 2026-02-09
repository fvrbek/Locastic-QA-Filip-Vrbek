"""
Automated test cases for responsive design bugs.

Tests viewport-specific CSS issues on mobile (375x667)
and tablet (768x1024) breakpoints.

Known bugs tested:
- BUG-008: Error messages hidden on mobile (display: none !important)
- BUG-009: Submit button reduced height on mobile (max-height: 35px)
- BUG-010: Street address overlay on tablet
- BUG-011: Newsletter checkbox overlay on mobile
- BUG-015: Security section overlay on mobile (forgot-password)
- BUG-021: Rewards card overlay on tablet (dashboard)
- BUG-022: Activity item overlay on tablet (dashboard)
- BUG-023: Download Report button overlay on mobile (dashboard)
- BUG-024: Dashboard stat card overlay on tablet (dashboard)
- BUG-025: Remember Me checkbox overlay on mobile (login)
"""

import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from utils.test_data import MOBILE_VIEWPORT, TABLET_VIEWPORT, random_email


class TestMobileRegistration:
    """Test mobile viewport issues on registration page."""

    def test_error_messages_visible_on_mobile(self, page):
        """TC-R01: BUG - Error messages hidden on mobile via CSS.

        CSS rule: @media (max-width: 767px) { .error-message { display: none !important; } }
        Users on mobile cannot see validation errors.
        """
        page.set_viewport_size(MOBILE_VIEWPORT)
        reg = RegisterPage(page)
        reg.open()

        # Trigger an email validation error
        reg.fill_email("invalid")
        reg.fill_first_name("Test")
        reg.fill_last_name("User")
        reg.fill_phone("0911234567")
        reg.fill_address("123 St")
        reg.fill_city("Split")
        reg.fill_zip_code("21000")
        reg.fill_password("SecurePass123!")
        reg.fill_confirm_password("SecurePass123!")
        reg.check_terms()
        reg.submit_registration()

        # Check if error message element is visible
        error_el = page.locator("#emailError")
        is_visible = error_el.is_visible()

        assert is_visible, (
            "BUG: Error messages are hidden on mobile! "
            "CSS sets .error-message { display: none !important; } at max-width: 767px"
        )

    def test_submit_button_fully_visible_on_mobile(self, page):
        """TC-R02: BUG - Submit button has reduced height on mobile.

        CSS rule: @media (max-width: 767px) { .btn-primary { max-height: 35px; margin-bottom: -25px; } }
        The button is still visible and functional, but its height is reduced compared to desktop.
        """
        page.set_viewport_size(MOBILE_VIEWPORT)
        reg = RegisterPage(page)
        reg.open()

        btn = page.locator("button[type='submit']")
        box = btn.bounding_box()

        assert box is not None, "Submit button should have a bounding box"
        assert box["height"] >= 40, (
            f"BUG: Submit button height is {box['height']}px on mobile "
            "(expected >= 40px). CSS max-height: 35px reduces it below desktop size."
        )

    def test_newsletter_checkbox_not_overlaid_on_mobile(self, page):
        """TC-R03: BUG - Newsletter checkbox has overlay on mobile.

        The .mobile-hidden-checkbox class shows an overlay-image-small on mobile.
        """
        page.set_viewport_size(MOBILE_VIEWPORT)
        reg = RegisterPage(page)
        reg.open()

        overlay = page.locator(".mobile-hidden-checkbox .overlay-image-small")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Newsletter checkbox has an overlay covering it on mobile"
        )


class TestTabletRegistration:
    """Test tablet viewport issues on registration page."""

    def test_address_field_not_overlaid_on_tablet(self, page):
        """TC-R04: BUG - Street address field has overlay on tablet.

        The .tablet-hidden class shows an overlay-image-tablet on tablet viewports.
        """
        page.set_viewport_size(TABLET_VIEWPORT)
        reg = RegisterPage(page)
        reg.open()

        overlay = page.locator(".tablet-hidden .overlay-image-tablet")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Street address field has an advertisement overlay on tablet viewport"
        )


class TestMobileForgotPassword:
    """Test mobile issues on forgot password page."""

    def test_security_section_not_overlaid_on_mobile(self, page):
        """TC-R05: BUG - Security question section has overlay on mobile.

        The .mobile-hidden-section class shows overlay-image-security on mobile.
        """
        page.set_viewport_size(MOBILE_VIEWPORT)
        fp = ForgotPasswordPage(page)
        fp.open()

        overlay = page.locator(".mobile-hidden-section .overlay-image-security")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Security question section has overlay on mobile viewport"
        )


class TestMobileLogin:
    """Test mobile issues on login page."""

    def test_remember_me_not_overlaid_on_mobile(self, page):
        """TC-R06: BUG - Remember Me checkbox has overlay on mobile.

        The .mobile-hidden class shows an overlay-image on mobile.
        """
        page.set_viewport_size(MOBILE_VIEWPORT)
        page.goto("https://qa-test-web-app.vercel.app/index.html")
        page.wait_for_load_state("networkidle")
        page.reload()
        page.wait_for_load_state("networkidle")

        overlay = page.locator(".mobile-hidden .overlay-image")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Remember Me checkbox has overlay covering it on mobile"
        )


class TestTabletDashboard:
    """Test tablet viewport issues on dashboard page."""

    def test_rewards_card_not_overlaid_on_tablet(self, page):
        """TC-R07: BUG - Rewards card has overlay on tablet.

        The .mobile-hidden-card class shows overlay-image-rewards on tablet viewports.
        Requires authenticated access to dashboard.
        """
        # Register and login to access dashboard
        email = random_email()
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Test", last_name="User", email=email,
            phone="0911234567", address="123 St", city="Split",
            zip_code="21000", password="SecurePass123!",
            confirm_password="SecurePass123!", accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        login = LoginPage(page)
        login.open()
        login.login(email, "SecurePass123!")
        page.wait_for_url("**/dashboard.html**", timeout=10000)
        page.wait_for_load_state("networkidle")

        # Set tablet viewport and check for overlay
        page.set_viewport_size(TABLET_VIEWPORT)
        page.reload()
        page.wait_for_load_state("networkidle")

        overlay = page.locator(".mobile-hidden-card .overlay-image-rewards")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Rewards card has an overlay covering it on tablet viewport"
        )

    def test_activity_item_not_overlaid_on_tablet(self, page):
        """TC-R08: BUG - Activity list item has overlay on tablet.

        The .tablet-hidden-activity class shows overlay-image-activity on tablet viewports.
        Requires authenticated access to dashboard.
        """
        # Register and login to access dashboard
        email = random_email()
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Test", last_name="User", email=email,
            phone="0911234567", address="123 St", city="Split",
            zip_code="21000", password="SecurePass123!",
            confirm_password="SecurePass123!", accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        login = LoginPage(page)
        login.open()
        login.login(email, "SecurePass123!")
        page.wait_for_url("**/dashboard.html**", timeout=10000)
        page.wait_for_load_state("networkidle")

        # Set tablet viewport and check for overlay
        page.set_viewport_size(TABLET_VIEWPORT)
        page.reload()
        page.wait_for_load_state("networkidle")

        overlay = page.locator(".tablet-hidden-activity .overlay-image-activity")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Activity list item has an overlay covering it on tablet viewport"
        )

    def test_dashboard_card_not_overlaid_on_tablet(self, page):
        """TC-R09: BUG - Dashboard stat card has overlay on tablet.

        The .tablet-hidden-card class shows overlay-image-dashboard on tablet viewports.
        Requires authenticated access to dashboard.
        """
        # Register and login to access dashboard
        email = random_email()
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Test", last_name="User", email=email,
            phone="0911234567", address="123 St", city="Split",
            zip_code="21000", password="SecurePass123!",
            confirm_password="SecurePass123!", accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        login = LoginPage(page)
        login.open()
        login.login(email, "SecurePass123!")
        page.wait_for_url("**/dashboard.html**", timeout=10000)
        page.wait_for_load_state("networkidle")

        # Set tablet viewport and check for overlay
        page.set_viewport_size(TABLET_VIEWPORT)
        page.reload()
        page.wait_for_load_state("networkidle")

        overlay = page.locator(".tablet-hidden-card .overlay-image-dashboard")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Dashboard stat card has an overlay covering it on tablet viewport"
        )


class TestMobileDashboard:
    """Test mobile viewport issues on dashboard page."""

    def test_download_report_button_not_overlaid_on_mobile(self, page):
        """TC-R10: BUG - Download Report button has overlay on mobile.

        The .mobile-hidden-action class shows a button-overlay on mobile viewports.
        Requires authenticated access to dashboard.
        """
        # Register and login to access dashboard
        email = random_email()
        reg = RegisterPage(page)
        reg.open()
        reg.fill_registration_form(
            first_name="Test", last_name="User", email=email,
            phone="0911234567", address="123 St", city="Split",
            zip_code="21000", password="SecurePass123!",
            confirm_password="SecurePass123!", accept_terms=True,
        )
        reg.submit_registration()
        page.wait_for_url("**/index.html**", timeout=10000)

        login = LoginPage(page)
        login.open()
        login.login(email, "SecurePass123!")
        page.wait_for_url("**/dashboard.html**", timeout=10000)
        page.wait_for_load_state("networkidle")

        # Set mobile viewport and check for overlay
        page.set_viewport_size(MOBILE_VIEWPORT)
        page.reload()
        page.wait_for_load_state("networkidle")

        overlay = page.locator(".mobile-hidden-action .button-overlay")
        overlay_visible = overlay.is_visible()

        assert not overlay_visible, (
            "BUG: Download Report button has an overlay covering it on mobile viewport"
        )
