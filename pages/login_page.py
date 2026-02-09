"""Page object for the Login page (index.html)."""

from pages.base_page import BasePage

BASE_URL = "https://qa-test-web-app.vercel.app"


class LoginPage(BasePage):
    """Page object for the login page.

    Locators based on index.html:
    - Form: #loginForm
    - Email: #loginEmail (type="text" - BUG: should be "email")
    - Password: #loginPassword
    - Remember Me: #rememberMe (has mobile-hidden overlay)
    - Login button: button[type='submit']
    - Message: #loginMessage
    """

    URL = f"{BASE_URL}/index.html"

    # Form locators
    LOGIN_EMAIL = "#loginEmail"
    LOGIN_PASSWORD = "#loginPassword"
    REMEMBER_ME = "#rememberMe"
    LOGIN_BUTTON = "button[type='submit']"

    # Error/message locators
    LOGIN_EMAIL_ERROR = "#loginEmailError"
    LOGIN_PASSWORD_ERROR = "#loginPasswordError"
    LOGIN_MESSAGE = "#loginMessage"

    # Navigation links
    FORGOT_PASSWORD_LINK = "a[href='forgot-password.html']"
    REGISTER_LINK = "a[href='register.html']"

    def open(self):
        self.navigate(self.URL)
        return self

    def fill_email(self, value: str):
        self.page.fill(self.LOGIN_EMAIL, value)
        return self

    def fill_password(self, value: str):
        self.page.fill(self.LOGIN_PASSWORD, value)
        return self

    def check_remember_me(self):
        self.page.check(self.REMEMBER_ME)
        return self

    def click_login(self):
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(500)
        return self

    def click_forgot_password(self):
        self.page.click(self.FORGOT_PASSWORD_LINK)

    def click_register(self):
        self.page.click(self.REGISTER_LINK)

    def login(self, email: str, password: str):
        """Fill credentials and submit login form."""
        self.fill_email(email)
        self.fill_password(password)
        self.click_login()
        return self

    def get_login_message(self) -> str:
        return self.get_element_text(self.LOGIN_MESSAGE)

    def has_success_message(self) -> bool:
        msg = self.page.locator(self.LOGIN_MESSAGE)
        return msg.is_visible() and "success" in (msg.get_attribute("class") or "")

    def has_error_message(self) -> bool:
        msg = self.page.locator(self.LOGIN_MESSAGE)
        return msg.is_visible() and "error" in (msg.get_attribute("class") or "")

    def get_email_error(self) -> str:
        return self.get_element_text(self.LOGIN_EMAIL_ERROR)

    def get_email_input_type(self) -> str:
        return self.page.locator(self.LOGIN_EMAIL).get_attribute("type") or ""
