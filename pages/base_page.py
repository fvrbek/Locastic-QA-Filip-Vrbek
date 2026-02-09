from playwright.sync_api import Page


class BasePage:
    """Base page object with common methods."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def get_element_text(self, selector: str) -> str:
        return self.page.locator(selector).text_content() or ""

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_url(self, url_pattern: str, timeout: int = 5000):
        self.page.wait_for_url(url_pattern, timeout=timeout)
