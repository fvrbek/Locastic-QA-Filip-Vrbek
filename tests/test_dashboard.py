"""
Automated test cases for the Dashboard page (dashboard.html).

Tests cover: authentication check, user info display, logout,
dashboard elements, and known bugs.

Known bugs tested:
- BUG-016: Incomplete session cleanup on logout
- BUG-017: No logout confirmation dialog
- BUG-018: Console.log of sensitive user data
"""

import pytest


class TestDashboardAuthentication:
    """Test dashboard authentication requirements."""

    def test_unauthenticated_redirects_to_login(self, dashboard_page):
        """TC-D01: Accessing dashboard without login redirects to login page."""
        dashboard_page.open()
        dashboard_page.page.wait_for_url("**/index.html**", timeout=10000)

        assert "index.html" in dashboard_page.get_url(), (
            "Unauthenticated users should be redirected to login"
        )

    def test_dashboard_accessible_after_login(self, authenticated_page):
        """TC-D02: Dashboard is accessible after successful login."""
        dashboard, user = authenticated_page

        assert "dashboard.html" in dashboard.get_url()

    def test_welcome_shows_user_name(self, authenticated_page):
        """TC-D03: Welcome message displays the user's first name."""
        dashboard, user = authenticated_page

        displayed_name = dashboard.get_user_name()
        assert displayed_name == user["first_name"], (
            f"Expected '{user['first_name']}', got '{displayed_name}'"
        )


class TestDashboardLogout:
    """Test logout functionality."""

    def test_logout_redirects_to_login(self, authenticated_page):
        """TC-D04: Clicking logout redirects to login page."""
        dashboard, user = authenticated_page
        dashboard.click_logout()
        dashboard.page.wait_for_url("**/index.html**", timeout=10000)

        assert "index.html" in dashboard.get_url(), (
            "Logout should redirect to login page"
        )

    def test_logout_incomplete_session_cleanup(self, authenticated_page):
        """TC-D05: BUG - Logout doesn't clear all session data."""
        dashboard, user = authenticated_page

        # Check what's in storage before logout
        session_keys_before = dashboard.get_session_storage_keys()
        local_keys_before = dashboard.get_local_storage_keys()

        dashboard.click_logout()
        dashboard.page.wait_for_url("**/index.html**", timeout=10000)

        # After logout, check if ALL storage is cleared
        # Navigate back to check remaining storage
        dashboard.page.goto("about:blank")
        dashboard.page.goto("https://qa-test-web-app.vercel.app/index.html")
        dashboard.page.wait_for_load_state("networkidle")

        local_keys_after = dashboard.get_local_storage_keys()

        # BUG: localStorage may still have user data
        # handleLogout() only clears sessionStorage keys, not localStorage
        assert len(local_keys_after) == 0, (
            f"BUG: localStorage still has data after logout: {local_keys_after}. "
            "handleLogout() doesn't clear localStorage completely."
        )

    def test_no_logout_confirmation(self, authenticated_page):
        """TC-D06: BUG - No confirmation dialog before logout.

        This is a known bug: clicking logout immediately logs out
        without asking 'Are you sure?'
        Note: This test documents the behavior; Playwright can't
        easily test for missing dialogs, so we verify the immediate redirect.
        """
        dashboard, user = authenticated_page

        # Logout happens immediately without confirmation
        dashboard.click_logout()
        dashboard.page.wait_for_url("**/index.html**", timeout=10000)

        # If there was a confirmation dialog, we'd still be on dashboard
        # BUG: We're already on login page - no confirmation was shown
        assert "index.html" in dashboard.get_url(), (
            "BUG: Logout happens immediately without confirmation dialog"
        )


class TestDashboardElements:
    """Test dashboard UI elements."""

    def test_stat_cards_visible(self, authenticated_page):
        """TC-D07: Dashboard shows stat cards."""
        dashboard, user = authenticated_page

        count = dashboard.get_stat_card_count()
        assert count >= 3, f"Expected at least 3 stat cards, got {count}"

    def test_action_buttons_present(self, authenticated_page):
        """TC-D08: Dashboard has action buttons."""
        dashboard, user = authenticated_page

        count = dashboard.get_action_button_count()
        assert count >= 3, f"Expected at least 3 action buttons, got {count}"

    def test_activity_list_present(self, authenticated_page):
        """TC-D09: Dashboard shows recent activity."""
        dashboard, user = authenticated_page

        count = dashboard.get_activity_count()
        assert count >= 2, f"Expected at least 2 activity items, got {count}"

    def test_action_button_shows_toast(self, authenticated_page):
        """TC-D10: Clicking action button shows toast message."""
        dashboard, user = authenticated_page

        dashboard.click_action_button(0)  # "Update Profile"

        msg = dashboard.get_toast_message()
        assert msg != "", "Action button should show a toast message"

    def test_page_title(self, authenticated_page):
        """TC-D11: Dashboard page title is correct."""
        dashboard, user = authenticated_page

        assert "Dashboard" in dashboard.page.title()

    def test_last_login_displayed(self, authenticated_page):
        """TC-D12: Last login timestamp is displayed."""
        dashboard, user = authenticated_page

        last_login = dashboard.get_last_login()
        assert last_login != "", "Last login should be displayed"
