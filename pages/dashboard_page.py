"""Page object for the Dashboard page (dashboard.html)."""

from pages.base_page import BasePage

BASE_URL = "https://qa-test-web-app.vercel.app"


class DashboardPage(BasePage):
    """Page object for the dashboard page.

    Locators based on dashboard.html:
    - User name: #userName
    - Last login: #lastLogin
    - Logout: button with onclick="handleLogout()"
    - Stat cards: .stat-card (4 cards, some with overlays)
    - Action buttons: .btn-action (4 buttons, Download Report has mobile overlay)
    - Activity list: .activity-list li (3 items, last has tablet overlay)
    - Toast message: #dashboardMessage
    - BUG: Incomplete logout (only clears 2 sessionStorage keys)
    - BUG: No logout confirmation dialog
    - BUG: Console logs sensitive user data
    """

    URL = f"{BASE_URL}/dashboard.html"

    # User info
    USER_NAME = "#userName"
    LAST_LOGIN = "#lastLogin"

    # Navigation
    LOGOUT_BUTTON = "button.btn-secondary"

    # Stat cards
    STAT_CARDS = ".stat-card"
    PROFILE_COMPLETION = ".stat-card:nth-child(1) .stat-value"
    ACCOUNT_STATUS = ".stat-card:nth-child(2) .stat-value"
    NOTIFICATIONS = ".stat-card:nth-child(3) .stat-value"
    REWARDS_POINTS = ".stat-card:nth-child(4) .stat-value"

    # Action buttons
    ACTION_BUTTONS = ".btn-action"

    # Activity
    ACTIVITY_LIST = ".activity-list li"

    # Toast
    DASHBOARD_MESSAGE = "#dashboardMessage"

    def open(self):
        self.navigate(self.URL)
        return self

    def get_user_name(self) -> str:
        return self.get_element_text(self.USER_NAME)

    def get_last_login(self) -> str:
        return self.get_element_text(self.LAST_LOGIN)

    def click_logout(self):
        self.page.click(self.LOGOUT_BUTTON)
        self.page.wait_for_timeout(500)

    def get_stat_card_count(self) -> int:
        return self.page.locator(self.STAT_CARDS).count()

    def get_action_button_count(self) -> int:
        return self.page.locator(self.ACTION_BUTTONS).count()

    def get_activity_count(self) -> int:
        return self.page.locator(self.ACTIVITY_LIST).count()

    def get_notifications_count(self) -> str:
        return self.get_element_text(self.NOTIFICATIONS)

    def click_action_button(self, index: int):
        self.page.locator(self.ACTION_BUTTONS).nth(index).click()
        self.page.wait_for_timeout(500)

    def get_toast_message(self) -> str:
        return self.get_element_text(self.DASHBOARD_MESSAGE)

    def is_toast_visible(self) -> bool:
        return self.is_visible(self.DASHBOARD_MESSAGE)

    def get_session_storage_keys(self) -> list[str]:
        """Get all sessionStorage keys via JavaScript."""
        return self.page.evaluate("() => Object.keys(sessionStorage)")

    def get_local_storage_keys(self) -> list[str]:
        """Get all localStorage keys via JavaScript."""
        return self.page.evaluate("() => Object.keys(localStorage)")
