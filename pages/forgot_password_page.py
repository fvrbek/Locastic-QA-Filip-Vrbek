"""Page object for the Forgot Password page (forgot-password.html)."""

from pages.base_page import BasePage

BASE_URL = "https://qa-test-web-app.vercel.app"


class ForgotPasswordPage(BasePage):
    """Page object for the forgot password page.

    Locators based on forgot-password.html:
    - Form: #forgotPasswordForm
    - Email: #resetEmail (type="text" - BUG: should be "email")
    - Security Question: #securityQuestion (select, optional, mobile-hidden-section overlay)
    - Security Answer: #securityAnswer (not validated - BUG)
    - Submit: button[type='submit'] "Send Reset Link"
    - Message: #forgotPasswordMessage
    - BUG: Always shows success, no actual email sent, security answer ignored
    """

    URL = f"{BASE_URL}/forgot-password.html"

    # Form locators
    RESET_EMAIL = "#resetEmail"
    SECURITY_QUESTION = "#securityQuestion"
    SECURITY_ANSWER = "#securityAnswer"
    SUBMIT_BUTTON = "button[type='submit']"

    # Error/message locators
    RESET_EMAIL_ERROR = "#resetEmailError"
    FORGOT_PASSWORD_MESSAGE = "#forgotPasswordMessage"

    # Navigation links
    LOGIN_LINK = "a[href='index.html']"
    REGISTER_LINK = "a[href='register.html']"

    # Security question option values
    QUESTION_PET = "pet"
    QUESTION_CITY = "city"
    QUESTION_SCHOOL = "school"

    def open(self):
        self.navigate(self.URL)
        return self

    def fill_email(self, value: str):
        self.page.fill(self.RESET_EMAIL, value)
        return self

    def select_security_question(self, value: str):
        self.page.select_option(self.SECURITY_QUESTION, value)
        return self

    def fill_security_answer(self, value: str):
        self.page.fill(self.SECURITY_ANSWER, value)
        return self

    def click_send_reset(self):
        self.page.click(self.SUBMIT_BUTTON)
        self.page.wait_for_timeout(500)
        return self

    def click_login_link(self):
        self.page.click(self.LOGIN_LINK)

    def click_register_link(self):
        self.page.click(self.REGISTER_LINK)

    def get_message(self) -> str:
        return self.get_element_text(self.FORGOT_PASSWORD_MESSAGE)

    def has_success_message(self) -> bool:
        msg = self.page.locator(self.FORGOT_PASSWORD_MESSAGE)
        return msg.is_visible() and "success" in (msg.get_attribute("class") or "")

    def has_error_message(self) -> bool:
        msg = self.page.locator(self.FORGOT_PASSWORD_MESSAGE)
        return msg.is_visible() and "error" in (msg.get_attribute("class") or "")

    def get_email_error(self) -> str:
        return self.get_element_text(self.RESET_EMAIL_ERROR)

    def get_email_input_type(self) -> str:
        return self.page.locator(self.RESET_EMAIL).get_attribute("type") or ""

    def get_security_question_options(self) -> list[str]:
        """Return all option values from the security question dropdown."""
        return self.page.locator(f"{self.SECURITY_QUESTION} option").all_text_contents()
