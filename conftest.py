"""
Pytest fixtures for QA Test Application test suite.

Provides page object fixtures for all pages and helper fixtures
for authenticated flows (register -> login -> dashboard).
Includes pytest-html report customization hooks.
"""

import os
import html as html_lib
from datetime import datetime

import pytest
from playwright.sync_api import Page

from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.dashboard_page import DashboardPage
from utils.test_data import random_email

BASE_URL = "https://qa-test-web-app.vercel.app"

# Category mapping from test file to display name
CATEGORY_MAP = {
    "test_registration": "Registration",
    "test_login": "Login",
    "test_forgot_password": "Forgot Password",
    "test_dashboard": "Dashboard",
    "test_responsive": "Responsive Design",
    "test_api": "API",
    "test_security": "Security",
}


# ──────────────────────────────────────────────
# PYTEST-HTML REPORT CUSTOMIZATION
# ──────────────────────────────────────────────


def pytest_configure(config):
    """Auto-create reports directory and set timestamped report filename."""
    os.makedirs("reports", exist_ok=True)
    if hasattr(config.option, "htmlpath") and config.option.htmlpath:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        config.option.htmlpath = f"reports/report_{timestamp}.html"


def pytest_html_report_title(report):
    """Set custom report title."""
    report.title = "QA Test Application - Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Extract test docstring and category for report columns."""
    outcome = yield
    report = outcome.get_result()

    # Extract docstring
    doc = getattr(item.function, "__doc__", "") or ""
    first_line = doc.strip().split("\n")[0] if doc.strip() else ""
    report.description = first_line

    # Store full docstring for expanded detail
    report.description_full = doc.strip() if doc.strip() else ""

    # Extract category from file name
    file_name = item.location[0] if hasattr(item, "location") else ""
    for key, label in CATEGORY_MAP.items():
        if key in str(file_name):
            report.category = label
            break
    else:
        report.category = "Other"

    # Add full docstring as extra HTML in the expanded section
    if report.when == "call" and doc.strip():
        from pytest_html import extras as pytest_extras

        extra_list = getattr(report, "extras", [])
        escaped_doc = html_lib.escape(doc.strip())
        extra_list.append(
            pytest_extras.html(
                '<div class="test-doc">'
                "<strong>Test Details:</strong><br>"
                f"<pre>{escaped_doc}</pre>"
                "</div>"
            )
        )
        report.extras = extra_list


def pytest_html_results_table_header(cells):
    """Add Category and Description columns to the report table."""
    cells.insert(1, '<th class="sortable" data-column-type="category">Category</th>')
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    """Populate Category and Description columns for each test row."""
    category = getattr(report, "category", "")
    description = getattr(report, "description", "")
    cells.insert(1, f"<td>{category}</td>")
    cells.insert(2, f"<td>{description}</td>")


# ──────────────────────────────────────────────
# PAGE OBJECT FIXTURES
# ──────────────────────────────────────────────


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    """Open the registration page."""
    reg = RegisterPage(page)
    reg.open()
    return reg


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Open the login page."""
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def forgot_password_page(page: Page) -> ForgotPasswordPage:
    """Open the forgot password page."""
    fp = ForgotPasswordPage(page)
    fp.open()
    return fp


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    """Provides a DashboardPage (not authenticated - use for redirect tests)."""
    return DashboardPage(page)


@pytest.fixture
def registered_user(page: Page) -> dict:
    """Register a new user and return credentials.

    Returns dict with keys: email, password, first_name, last_name.
    """
    email = random_email()
    password = "SecurePass123!"
    first_name = "Test"
    last_name = "User"

    reg = RegisterPage(page)
    reg.open()
    reg.fill_registration_form(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone="0911234567",
        address="123 Test Street",
        city="Split",
        zip_code="21000",
        password=password,
        confirm_password=password,
        accept_terms=True,
    )
    reg.submit_registration()
    page.wait_for_url("**/index.html**", timeout=10000)

    return {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }


@pytest.fixture
def authenticated_page(page: Page, registered_user: dict) -> tuple[DashboardPage, dict]:
    """Register user, log in, and return (DashboardPage, user_data).

    Use this fixture when you need an authenticated dashboard session.
    """
    login = LoginPage(page)
    login.open()
    login.login(registered_user["email"], registered_user["password"])
    page.wait_for_url("**/dashboard.html**", timeout=10000)

    dashboard = DashboardPage(page)
    return dashboard, registered_user
