from pages.base_page import BasePage

BASE_URL = "https://qa-test-web-app.vercel.app"


class RegisterPage(BasePage):
    """Page object for the registration page."""

    URL = f"{BASE_URL}/register.html"

    # Locators
    FIRST_NAME = "#firstName"
    LAST_NAME = "#lastName"
    EMAIL = "#email"
    PHONE = "#phone"
    ADDRESS = "#address"
    CITY = "#city"
    ZIP_CODE = "#zipCode"
    PASSWORD = "#password"
    CONFIRM_PASSWORD = "#confirmPassword"
    TERMS_CHECKBOX = "#terms"
    NEWSLETTER_CHECKBOX = "#newsletter"
    SUBMIT_BUTTON = "button[type='submit']"
    LOGIN_LINK = "a[href='index.html']"

    # Error message locators
    EMAIL_ERROR = "#emailError"
    PHONE_ERROR = "#phoneError"
    ZIP_ERROR = "#zipError"
    PASSWORD_ERROR = "#passwordError"
    CONFIRM_PASSWORD_ERROR = "#confirmPasswordError"
    REGISTER_MESSAGE = "#registerMessage"

    # Form
    FORM = "#registerForm"

    def open(self):
        self.navigate(self.URL)
        return self

    def fill_first_name(self, value: str):
        self.page.fill(self.FIRST_NAME, value)
        return self

    def fill_last_name(self, value: str):
        self.page.fill(self.LAST_NAME, value)
        return self

    def fill_email(self, value: str):
        self.page.fill(self.EMAIL, value)
        return self

    def fill_phone(self, value: str):
        self.page.fill(self.PHONE, value)
        return self

    def fill_address(self, value: str):
        self.page.fill(self.ADDRESS, value)
        return self

    def fill_city(self, value: str):
        self.page.fill(self.CITY, value)
        return self

    def fill_zip_code(self, value: str):
        self.page.fill(self.ZIP_CODE, value)
        return self

    def fill_password(self, value: str):
        self.page.fill(self.PASSWORD, value)
        return self

    def fill_confirm_password(self, value: str):
        self.page.fill(self.CONFIRM_PASSWORD, value)
        return self

    def check_terms(self):
        self.page.check(self.TERMS_CHECKBOX)
        return self

    def uncheck_terms(self):
        self.page.uncheck(self.TERMS_CHECKBOX)
        return self

    def check_newsletter(self):
        self.page.check(self.NEWSLETTER_CHECKBOX)
        return self

    def click_submit(self):
        self.page.click(self.SUBMIT_BUTTON)
        return self

    def click_login_link(self):
        self.page.click(self.LOGIN_LINK)

    def fill_registration_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        zip_code: str,
        password: str,
        confirm_password: str,
        accept_terms: bool = True,
        subscribe_newsletter: bool = False,
    ):
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.fill_phone(phone)
        self.fill_address(address)
        self.fill_city(city)
        self.fill_zip_code(zip_code)
        self.fill_password(password)
        self.fill_confirm_password(confirm_password)
        if accept_terms:
            self.check_terms()
        if subscribe_newsletter:
            self.check_newsletter()
        return self

    def submit_registration(self):
        self.click_submit()
        self.page.wait_for_timeout(500)
        return self

    # Getters for error messages
    def get_email_error(self) -> str:
        return self.get_element_text(self.EMAIL_ERROR)

    def get_phone_error(self) -> str:
        return self.get_element_text(self.PHONE_ERROR)

    def get_zip_error(self) -> str:
        return self.get_element_text(self.ZIP_ERROR)

    def get_password_error(self) -> str:
        return self.get_element_text(self.PASSWORD_ERROR)

    def get_confirm_password_error(self) -> str:
        return self.get_element_text(self.CONFIRM_PASSWORD_ERROR)

    def get_register_message(self) -> str:
        return self.get_element_text(self.REGISTER_MESSAGE)

    def is_register_message_visible(self) -> bool:
        return self.is_visible(self.REGISTER_MESSAGE)

    def has_success_message(self) -> bool:
        msg = self.page.locator(self.REGISTER_MESSAGE)
        return msg.is_visible() and "success" in (msg.get_attribute("class") or "")

    def has_error_message(self) -> bool:
        msg = self.page.locator(self.REGISTER_MESSAGE)
        return msg.is_visible() and "error" in (msg.get_attribute("class") or "")

    def get_field_validation_message(self, field_selector: str) -> str:
        return self.page.locator(field_selector).evaluate(
            "el => el.validationMessage"
        )

    def is_field_required(self, field_selector: str) -> bool:
        return self.page.locator(field_selector).evaluate("el => el.required")

    def get_email_input_type(self) -> str:
        return self.page.locator(self.EMAIL).get_attribute("type") or ""

    def get_password_input_type(self) -> str:
        return self.page.locator(self.PASSWORD).get_attribute("type") or ""
